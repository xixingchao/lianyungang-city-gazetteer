# -*- coding: utf-8 -*-
"""Verify LYG-下-T014 arrest request continuation table."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
DATA = ROOT / "workbench" / "table_entries" / "下" / "data" / "LYG-下-T014.json"

COLUMNS = ["年份", "受案(人)", "批捕(人)", "不批捕(人)", "退查(人)", "公安撤回(人)"]

ROWS = [
    ["1960", "548", "301", "91", "", ""],
    ["1961", "698", "320", "190", "", ""],
    ["1962", "226", "101", "76", "", ""],
    ["1963", "370", "279", "62", "", ""],
    ["1964", "168", "109", "8", "", ""],
    ["1965", "135", "68", "38", "4", ""],
    ["1966", "27", "25", "2", "", ""],
    ["1979", "155", "125", "23", "5", ""],
    ["1980", "290", "269", "12", "3", ""],
    ["1981", "455", "406", "22", "11", "2"],
    ["1982", "394", "359", "20", "2", "2"],
    ["1983", "2695", "2635", "26", "9", "15"],
    ["1984", "1605", "1445", "112", "40", "8"],
    ["1985", "801", "688", "63", "", ""],
    ["1986", "544", "489", "33", "23", "7"],
    ["1987", "566", "536", "20", "", ""],
    ["1988", "931", "879", "40", "13", ""],
    ["1989", "1490", "1419", "38", "40", ""],
    ["1990", "1331", "1313", "23", "6", ""],
]

PATCH = {
    "title": "1955~1990年连云港市检察机关受理公安提请批捕人犯统计表（续表）",
    "table_number": "表44-9",
    "page": 2074,
    "pages": [2074],
    "part": "part01",
    "vol": "下",
    "volume": "下",
    "columns": COLUMNS,
    "rows": ROWS,
    "row_count": len(ROWS),
    "col_count": len(COLUMNS),
    "status": "verified",
    "notes": "已据页级OCR核录续页：workbench/ocr/paddle_ocr/下/part01/page_0103.txt；表题、表号、单位据前页 workbench/ocr/paddle_ocr/下/part01/page_0102.txt。参考 raw OCR：workbench/table_entries/下/raw/LYG-下-T014_2074.txt。本条仅录入续页1960-1990年，源页未见数值的单元格保留空值。",
}


def patch_entry(entry: dict) -> bool:
    if entry.get("table_id") != "LYG-下-T014":
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
