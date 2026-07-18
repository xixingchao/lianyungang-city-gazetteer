# -*- coding: utf-8 -*-
"""Verify LYG-中-T036 power line loss rate table from page OCR."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
DATA = ROOT / "workbench" / "table_entries" / "中" / "data" / "LYG-中-T036.json"

COLUMNS = ["年份", "线损率(%)"]
ROWS = [
    ["1949", "20.00"],
    ["1950", "24.44"],
    ["1951", "27.97"],
    ["1952", "16.64"],
    ["1953", "10.70"],
    ["1954", "9.22"],
    ["1955", "10.67"],
    ["1956", "10.24"],
    ["1957", "12.41"],
    ["1958", "10.21"],
    ["1959", "6.49"],
    ["1960", "7.05"],
    ["1961", "8.00"],
    ["1962", "8.08"],
    ["1963", "7.35"],
    ["1964", "7.39"],
    ["1965", "5.13"],
    ["1966", "7.08"],
    ["1967", "11.21"],
    ["1968", "20.01"],
    ["1969", "20.30"],
    ["1970", "5.92"],
    ["1971", "8.94"],
    ["1972", "10.44"],
    ["1973", "9.99"],
    ["1974", "9.17"],
    ["1975", "9.64"],
    ["1976", "8.44"],
    ["1977", "7.35"],
    ["1978", "7.46"],
    ["1979", "5.62"],
    ["1980", "4.96"],
    ["1981", "4.47"],
    ["1982", "7.24"],
    ["1983", "7.29"],
    ["1984", "7.61"],
    ["1985", "7.18"],
    ["1986", "8.07"],
    ["1987", "8.33"],
    ["1988", "7.62"],
    ["1989", "7.02"],
    ["1990", "7.29"],
]

PATCH = {
    "title": "1949~1990年连云港市供电线损率统计表",
    "table_number": "表25-5",
    "page": 1266,
    "pages": [1266],
    "columns": COLUMNS,
    "rows": ROWS,
    "row_count": len(ROWS),
    "col_count": len(COLUMNS),
    "status": "verified",
    "notes": "已据页级OCR回源核录：workbench/ocr/paddle_ocr/中/part01/page_0363.txt；原表为三组年份/线损率并排版式，结构化为两列逐年记录。",
}


def patch_entry(entry: dict) -> bool:
    if entry.get("table_id") != "LYG-中-T036":
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
