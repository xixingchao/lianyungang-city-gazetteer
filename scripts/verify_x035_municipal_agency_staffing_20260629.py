# -*- coding: utf-8 -*-
"""Verify LYG-下-T035 municipal agency staffing table from raw OCR."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
DATA = ROOT / "workbench" / "table_entries" / "下" / "data" / "LYG-下-T035.json"

COLUMNS = ["系统", "编制(人)", "实有(人)"]
ROWS = [
    ["党委系统", "130", "125"],
    ["人大常委会", "122", "94"],
    ["政府系统", "2371", "2328"],
    ["政治协商会议", "80", "216"],
    ["民主党派", "31", "27"],
    ["人民团体", "33", "24"],
    ["人民法院", "105", "247"],
    ["人民检察院", "48", "41"],
    ["合计", "3054", "2968"],
]

PATCH = {
    "title": "1990年连云港市市级机关编制情况表",
    "table_number": "表46-21",
    "page": 2203,
    "pages": [2203],
    "columns": COLUMNS,
    "rows": ROWS,
    "row_count": len(ROWS),
    "col_count": len(COLUMNS),
    "status": "verified",
    "notes": "已据raw OCR回源核录：workbench/table_entries/下/raw/LYG-下-T035_2203.txt；原表按系统分编制/实有两列，注：政府系统中含公安编制831人。",
}


def patch_entry(entry: dict) -> bool:
    if entry.get("table_id") != "LYG-下-T035":
        return False
    changed = False
    for key, value in PATCH.items():
        if entry.get(key) != value:
            entry[key] = value
            changed = True
    return changed


def patch_json() -> int:
    data = json.loads(DATA.read_text(encoding="utf-8"))
    if patch_entry(data):
        DATA.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        return 1
    return 0


def patch_site() -> int:
    text = SITE.read_text(encoding="utf-8")
    match = re.search(r"const TABLES = (\[.*?\]);\s*\n\s*function escape", text, re.S)
    if not match:
        raise SystemExit("TABLES payload not found")
    tables = json.loads(match.group(1))
    changed = 0
    for table in tables:
        if patch_entry(table):
            changed += 1
    if changed:
        text = text[: match.start(1)] + json.dumps(tables, ensure_ascii=False) + text[match.end(1) :]
        SITE.write_text(text, encoding="utf-8")
    return changed


def main() -> None:
    print(f"json_files_changed={patch_json()}")
    print(f"site_entries_changed={patch_site()}")


if __name__ == "__main__":
    main()
