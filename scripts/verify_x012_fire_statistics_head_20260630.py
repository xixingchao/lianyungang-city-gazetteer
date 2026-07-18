# -*- coding: utf-8 -*-
"""Verify LYG-下-T012 fire statistics head page."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
DATA = ROOT / "workbench" / "table_entries" / "下" / "data" / "LYG-下-T012.json"

COLUMNS = ["年份", "火灾起数(起)", "死亡(人)", "受伤(人)", "损失折款(元)"]

ROWS = [
    ["1954", "20", "", "", "2501"],
    ["1956", "25", "3", "12", "17040"],
    ["1957", "30", "4", "3", "9553"],
    ["1958", "36", "7", "4", "19257"],
    ["1959", "26", "2", "1", "20013"],
    ["1960", "25", "7", "1", "21404"],
    ["1961", "20", "3", "", "59529"],
    ["1962", "15", "1", "", "36653"],
    ["1963", "18", "1", "", "97264"],
    ["1964", "14", "", "", "19280"],
    ["1965", "15", "1", "", "4748"],
    ["1967~1970", "7", "", "", "35775"],
    ["1971", "47", "1", "1", "24000"],
    ["1972", "20", "1", "9", "270905"],
]

PATCH = {
    "title": "1954~1990年连云港市火灾情况统计表",
    "table_number": "表44-6",
    "page": 2065,
    "pages": [2065],
    "part": "part01",
    "vol": "下",
    "volume": "下",
    "columns": COLUMNS,
    "rows": ROWS,
    "row_count": len(ROWS),
    "col_count": len(COLUMNS),
    "status": "verified",
    "notes": "已据页级OCR核录：workbench/ocr/paddle_ocr/下/part01/page_0094.txt；并参考 raw 坐标 OCR：workbench/ocr/raw/下/part01/page_0094.json 与 raw 文本 workbench/table_entries/下/raw/LYG-下-T012_2065.txt。此页仅录入表44-6首页 1954-1972 年记录，续页 1973-1990 年记录已由 LYG-下-T013 承接；源页未见数值处保留空值。",
}


def patch_entry(entry: dict) -> bool:
    if entry.get("table_id") != "LYG-下-T012":
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
