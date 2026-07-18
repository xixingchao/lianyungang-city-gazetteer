# -*- coding: utf-8 -*-
"""Verify LYG-下-T021 cadre transfer table from raw OCR."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
DATA = ROOT / "workbench" / "table_entries" / "下" / "data" / "LYG-下-T021.json"

COLUMNS = ["类别", "合计(人)", "1980", "1981", "1982", "1983", "1984", "1985", "1986", "1987", "1988", "1989", "1990"]
ROWS = [
    ["调进", "3989", "221", "259", "526", "363", "285", "535", "405", "475", "380", "290", "250"],
    ["调出", "1400", "146", "161", "154", "101", "91", "89", "123", "100", "130", "141", "134"],
]

PATCH = {
    "title": "1980~1990年连云港市（不含三县）干部易地调动统计表",
    "table_number": "表46-5",
    "page": 2172,
    "pages": [2172],
    "columns": COLUMNS,
    "rows": ROWS,
    "row_count": len(ROWS),
    "col_count": len(COLUMNS),
    "status": "verified",
    "notes": "已据raw OCR回源核录：workbench/table_entries/下/raw/LYG-下-T021_2172.txt；原JSON标题误串为化工产量表，本轮修正为干部易地调动统计表。",
}


def patch_entry(entry: dict) -> bool:
    if entry.get("table_id") != "LYG-下-T021":
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
