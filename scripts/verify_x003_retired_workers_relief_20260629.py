# -*- coding: utf-8 -*-
"""Verify LYG-下-T003 retired workers relief table from raw OCR."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
DATA = ROOT / "workbench" / "table_entries" / "下" / "data" / "LYG-下-T003.json"

COLUMNS = ["年份", "合计(人)", "享受40%救济(人)", "享受定期救济(人)"]
ROWS = [
    ["1980", "54", "40", "14"],
    ["1981", "96", "40", "56"],
    ["1982", "97", "41", "56"],
    ["1983", "1276", "328", "948"],
    ["1984", "1253", "316", "937"],
    ["1985", "1238", "314", "924"],
    ["1986", "1282", "352", "930"],
    ["1987", "1306", "338", "968"],
    ["1988", "1325", "362", "963"],
    ["1989", "1352", "353", "999"],
    ["1990", "1036", "342", "694"],
]

PATCH = {
    "title": "1980~1990年连云港市精简退职老职工救济情况表",
    "table_number": "表43-4",
    "page": 2003,
    "pages": [2003],
    "columns": COLUMNS,
    "rows": ROWS,
    "row_count": len(ROWS),
    "col_count": len(COLUMNS),
    "status": "verified",
    "notes": "已据raw OCR回源核录：workbench/table_entries/下/raw/LYG-下-T003_2003.txt；原JSON标题误串为柳制品生产经营情况表。备注：1983年市管县以后数字包括赣榆、东海、灌云三县。",
}


def patch_entry(entry: dict) -> bool:
    if entry.get("table_id") != "LYG-下-T003":
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
