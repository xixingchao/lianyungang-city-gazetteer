# -*- coding: utf-8 -*-
"""Verify LYG-中-T104 Huaibei salt tax income table from raw OCR."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
DATA = ROOT / "workbench" / "table_entries" / "中" / "data" / "LYG-中-T104.json"

COLUMNS = ["年份", "全年税收数(万元)", "占全国(%)"]
ROWS = [
    ["民国3年", "179", "3.5"],
    ["民国4年", "995", "11.8"],
    ["民国5年", "693", "11.0"],
    ["民国6年", "452", "7.0"],
    ["民国7年", "560", "8.1"],
    ["民国8年", "759", "10.3"],
    ["民国9年", "760", "10.0"],
    ["民国10年", "655", "7.8"],
    ["民国11年", "672", "7.6"],
    ["民国12年", "595", "7.5"],
    ["民国13年", "484", "6.4"],
    ["民国14年", "795", "10.1"],
    ["民国15年", "703", "12.7"],
    ["民国16年", "349", "6.1"],
    ["民国17年", "558", "9.5"],
    ["民国18年", "823", "11.3"],
    ["民国19年", "1216", "10.9"],
    ["民国20年", "1174", "10.5"],
    ["民国21年", "1337", ""],
    ["民国22年", "2092", ""],
    ["民国23年", "2192", ""],
    ["民国24年", "1956", ""],
]

PATCH = {
    "title": "民国3~24年淮北盐税收入统计表",
    "table_number": "表38-3",
    "page": 1708,
    "pages": [1708],
    "columns": COLUMNS,
    "rows": ROWS,
    "row_count": len(ROWS),
    "col_count": len(COLUMNS),
    "status": "verified",
    "notes": "已据raw OCR回源核录：workbench/table_entries/中/raw/LYG-中-T104_1708.txt；原表为两组年份/全年税收数/占全国比例并排版式，结构化为三列逐年记录；民国21~24年占全国比例OCR未见数字，保留空值。",
}


def patch_entry(entry: dict) -> bool:
    if entry.get("table_id") != "LYG-中-T104":
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
