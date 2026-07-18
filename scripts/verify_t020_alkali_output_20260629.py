# -*- coding: utf-8 -*-
"""Verify LYG-中-T020 alkali output table from page OCR."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
DATA = ROOT / "workbench" / "table_entries" / "中" / "data" / "LYG-中-T020.json"

COLUMNS = ["年份", "烧碱(液体100%)(吨)", "纯碱产量(吨)", "其中：重质纯碱(吨)", "氢氧化钾(吨)"]
ROWS = [
    ["1970", "232", "1405", "", ""],
    ["1971", "253", "2810", "", ""],
    ["1972", "332", "3270", "", "48"],
    ["1973", "719", "3270", "", "145"],
    ["1974", "225", "1186", "", "151"],
    ["1975", "279", "1820", "", "215"],
    ["1976", "731", "2333", "", "139"],
    ["1977", "1581", "3682", "", "203"],
    ["1978", "2175", "4804", "", "182"],
    ["1979", "2225", "11745", "", "106"],
    ["1980", "5772", "15659", "", "197"],
    ["1981", "5763", "15246", "", "276"],
    ["1982", "6883", "15281", "", "326"],
    ["1983", "8319", "16263", "", "550"],
    ["1984", "9188", "23751", "", "559"],
    ["1985", "11792", "26204", "5467", "853"],
    ["1986", "12734", "26692", "11179", "784"],
    ["1987", "14911", "27274", "12237", "1129"],
    ["1988", "16279", "20263", "10308", "1000"],
    ["1989", "15970", "28284", "6466", "988"],
    ["1990", "15189", "121503", "1369", "955"],
]

PATCH = {
    "title": "1970~1990年连云港市烧碱、纯碱、氢氧化钾产量统计表",
    "table_number": "表20-2",
    "page": 1050,
    "pages": [1050],
    "columns": COLUMNS,
    "rows": ROWS,
    "row_count": len(ROWS),
    "col_count": len(COLUMNS),
    "status": "verified",
    "notes": "已据页级OCR回源核录：workbench/ocr/paddle_ocr/中/part01/page_0147.txt。",
}


def patch_entry(entry: dict) -> bool:
    if entry.get("table_id") != "LYG-中-T020":
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
