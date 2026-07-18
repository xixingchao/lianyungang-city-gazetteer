# -*- coding: utf-8 -*-
"""Verify LYG-上-T020 GDP structure table."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
DATA = ROOT / "workbench" / "table_entries" / "上" / "data" / "LYG-上-T020.json"

COLUMNS = [
    "年份",
    "国内生产总值(万元)",
    "第一产业总值(万元)",
    "第一产业占比重(%)",
    "第二产业总值(万元)",
    "第二产业占比重(%)",
    "第三产业总值(万元)",
    "第三产业占比重(%)",
]

ROWS = [
    ["1978", "96003", "41903", "43.6", "37207", "38.8", "16893", "17.6"],
    ["1979", "105727", "47921", "45.3", "38996", "36.9", "18810", "17.8"],
    ["1980", "115206", "53108", "46.1", "41792", "36.3", "20306", "17.6"],
    ["1981", "131130", "62437", "47.6", "45581", "34.8", "23112", "17.6"],
    ["1982", "163559", "81479", "49.8", "51505", "31.5", "30575", "18.7"],
    ["1983", "186512", "90972", "48.8", "58977", "31.6", "36563", "19.6"],
    ["1984", "216235", "103388", "47.8", "67164", "31.1", "45683", "21.1"],
    ["1985", "275332", "124848", "45.3", "83033", "30.2", "67451", "24.5"],
    ["1986", "325888", "152557", "46.8", "96324", "29.6", "77007", "23.6"],
    ["1987", "357424", "163730", "45.8", "108637", "30.4", "85057", "23.8"],
    ["1988", "415100", "184679", "44.5", "121064", "29.2", "109357", "26.3"],
    ["1989", "448375", "200215", "44.7", "129051", "28.8", "119109", "26.5"],
    ["1990", "501403", "226441", "45.2", "134934", "26.9", "140028", "27.9"],
]

PATCH = {
    "title": "1978~1990年连云港市国内生产总值结构表",
    "table_number": "表7-9",
    "page": 445,
    "pages": [445],
    "part": "part02",
    "vol": "上",
    "volume": "上",
    "columns": COLUMNS,
    "rows": ROWS,
    "row_count": len(ROWS),
    "col_count": len(COLUMNS),
    "status": "verified",
    "notes": "已据页级OCR核录：workbench/ocr/paddle_ocr/上/part02/page_0145.txt；并参考 raw 坐标 OCR：workbench/ocr/raw/上/part02/page_0145.json 与 raw 文本 workbench/table_entries/上/raw/LYG-上-T020_445.txt。表7-9实际位于 page_0145，本条仅录入该表 1978-1990 年记录；源页注释为以当年价格计算。",
}


def patch_entry(entry: dict) -> bool:
    if entry.get("table_id") != "LYG-上-T020":
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
