# -*- coding: utf-8 -*-
"""Verify LYG-下-T020 demobilized cadres placement table from raw OCR."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
DATA = ROOT / "workbench" / "table_entries" / "下" / "data" / "LYG-下-T020.json"

COLUMNS = ["年份", "人数(人)"]
ROWS = [
    ["合计", "476"],
    ["1949", ""],
    ["1950", ""],
    ["1951", "18"],
    ["1952", "273"],
    ["1953", "49"],
    ["1954", "19"],
    ["1955", ""],
    ["1956", ""],
    ["1957", "25"],
    ["1958", "26"],
    ["1959", "10"],
]

PATCH = {
    "title": "1949~1959年连云港市历年接收安置军队转业干部统计表",
    "table_number": "表46-3",
    "page": 2170,
    "pages": [2170],
    "columns": COLUMNS,
    "rows": ROWS,
    "row_count": len(ROWS),
    "col_count": len(COLUMNS),
    "status": "verified",
    "notes": "已据raw OCR回源核录：workbench/table_entries/下/raw/LYG-下-T020_2170.txt；原表为横向年份表，结构化为年份/人数两列；1949、1950、1955、1956年人数栏OCR未见数字，保留空值。",
}


def patch_entry(entry: dict) -> bool:
    if entry.get("table_id") != "LYG-下-T020":
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
