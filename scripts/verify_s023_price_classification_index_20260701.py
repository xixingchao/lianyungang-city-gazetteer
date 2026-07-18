# -*- coding: utf-8 -*-
"""Verify LYG-上-T023 price classification index continuation."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
DATA = ROOT / "workbench" / "table_entries" / "上" / "data" / "LYG-上-T023.json"

COLUMNS = ["类别", "1983", "1984", "1985", "1986", "1987", "1988", "1989", "1990"]

ROWS = [
    ["肉禽蛋", "101.4", "112.2", "117.6", "104.2", "120.5", "131.8", "111.0", "100.9"],
    ["水产品", "106.1", "130.7", "164.4", "107.3", "126.1", "131.5", "105.5", "109.0"],
    ["调味品", "100.0", "100.4", "100.0", "103.4", "111.2", "106.3", "110.5", "120.1"],
    ["食糖", "100.0", "100.0", "100.0", "100.0", "100.0", "127.4", "118.3", "108.1"],
    ["(3)烟酒类", "99.1", "99.7", "100.7", "100.8", "104.2", "126.4", "112.8", "99.5"],
    ["烟", "100.0", "100.0", "100.0", "100.0", "100.0", "133.4", "111.7", "98.1"],
    ["酒", "100.0", "99.8", "102.1", "102.1", "109.8", "117.6", "112.3", "100.5"],
    ["茶", "87.2", "92.3", "100.0", "100.0", "100.0", "111.9", "134.3", "113.2"],
    ["(4)其它食品", "100.0", "100.5", "116.5", "110.2", "109.1", "128.1", "114.4", "100.1"],
    ["鲜果", "100.0", "100.5", "139.6", "115.9", "116.3", "139.2", "112.2", "96.4"],
    ["干果", "97.0", "105.1", "120.4", "121.9", "110.0", "112.4", "129.4", "93.9"],
    ["糖果", "100.0", "100.0", "100.0", "100.0", "100.0", "114.9", "118.1", "103.8"],
    ["糕点", "100.0", "100.0", "103.2", "103.4", "101.0", "123.6", "120.4", "106.7"],
    ["奶及奶制品", "100.6", "100.0", "104.2", "105.8", "104.8", "127.7", "103.6", "106.6"],
    ["罐头", "100.6", "100.0", "104.3", "102.0", "102.8", "118.4", "104.6", "99.1"],
    ["饮料类", "112.8", "105.5", "", "", "", "", "", ""],
    ["2、衣着类", "100.3", "98.2", "100.1", "100.5", "100.0", "115.3", "", ""],
]

PATCH = {
    "title": "1983~1990年连云港市职工生活费用价格和零售物价分类指数表续表",
    "table_number": "表8-17",
    "page": 513,
    "pages": [513],
    "part": "part02",
    "vol": "上",
    "volume": "上",
    "columns": COLUMNS,
    "rows": ROWS,
    "row_count": len(ROWS),
    "col_count": len(COLUMNS),
    "status": "verified",
    "notes": "已据页级OCR核录：workbench/ocr/paddle_ocr/上/part02/page_0213.txt；表题、表号和年份表头据前页 workbench/ocr/paddle_ocr/上/part02/page_0212.txt。并参考 raw 文本 workbench/table_entries/上/raw/LYG-上-T023_513.txt。本条原题名串章为排水工程情况表，实际为表8-17续页；仅录入 page_0213 可见分类指数记录，源页未见数值处保留空值。",
}


def patch_entry(entry: dict) -> bool:
    if entry.get("table_id") != "LYG-上-T023":
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
