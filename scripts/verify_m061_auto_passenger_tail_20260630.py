# -*- coding: utf-8 -*-
"""Verify automobile passenger transport continuation table T061."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
DATA = ROOT / "workbench" / "table_entries" / "中" / "data" / "LYG-中-T061.json"

COLUMNS = [
    "地区",
    "年份",
    "客车(座/辆)",
    "运量(万人次)",
    "周转量(万人公里)",
]

ROWS = [
    ["市区", "1965", "1129/28", "225.46", "4911.48"],
    ["市区", "1975", "3180/58", "543.08", "9495.41"],
    ["市区", "1985", "1509/268", "1875.40", "49727.51"],
    ["市区", "1990", "11995/251", "1956.80", "55959"],
    ["赣榆县", "1975", "", "75", "190"],
    ["赣榆县", "1985", "", "202", "392"],
    ["赣榆县", "1990", "", "168", "8127"],
    ["东海县", "1955", "40/1", "1.70", "106"],
    ["东海县", "1965", "/2", "7.20", "173"],
    ["东海县", "1975", "660/11", "85.60", "1805"],
    ["东海县", "1985", "/42", "275.60", "6819"],
    ["东海县", "1990", "2086/47", "282.00", "8362"],
    ["灌云县", "1965", "126/3", "31.50", "785"],
    ["灌云县", "1975", "168/4", "10.50", "174"],
    ["灌云县", "1985", "1830/32", "269.30", "8194"],
    ["灌云县", "1990", "1700/36", "184.80", "8628"],
]

PATCH = {
    "table_id": "LYG-中-T061",
    "title": "1955~1990年部分年份连云港市汽车客运情况表（续表）",
    "table_number": "表30-7",
    "page": 1452,
    "pages": [1452],
    "part": "part02",
    "vol": "中",
    "volume": "中",
    "columns": COLUMNS,
    "rows": ROWS,
    "row_count": len(ROWS),
    "col_count": len(COLUMNS),
    "status": "verified",
    "notes": "已据页级OCR回源核录：表题、表号和表头见 workbench/ocr/paddle_ocr/中/part02/page_0031.txt；续表内容见 workbench/ocr/paddle_ocr/中/part02/page_0032.txt，并参考 raw OCR workbench/table_entries/中/raw/LYG-中-T061_1452.txt。原JSON为单列骨架且标题误列为新浦汽车站客运发车情况表；源页未见数值的单元格保留空值，未按相邻地区或年份推算。",
}


def patch_entry(entry: dict) -> bool:
    if entry.get("table_id") != PATCH["table_id"]:
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
    changed = sum(1 for table in tables if patch_entry(table))
    if changed:
        text = text[: match.start(1)] + json.dumps(tables, ensure_ascii=False) + text[match.end(1) :]
        SITE.write_text(text, encoding="utf-8")
    return changed


def main() -> None:
    print(f"json_files_changed={patch_json()}")
    print(f"site_entries_changed={patch_site()}")


if __name__ == "__main__":
    main()
