# -*- coding: utf-8 -*-
"""Verify LYG-上-T014 real estate transaction table."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
DATA = ROOT / "workbench" / "table_entries" / "上" / "data" / "LYG-上-T014.json"

COLUMNS = ["交易性质", "起数", "建筑面积(万平方米)", "成交额(万元)"]

ROWS = [
    ["买卖", "854", "4.10", "1100.00"],
    ["继承", "55", "0.20", "11.50"],
    ["析产", "95", "0.60", "6.00"],
    ["赠与", "14", "0.10", "8.00"],
    ["交换", "11", "0.06", "6.90"],
    ["抵押", "1", "9.91", "2.50"],
    ["换契", "58", "0.30", ""],
]

PATCH = {
    "title": "1974~1990年连云港市市区房地产交易统计表",
    "table_number": "表5-14",
    "page": 394,
    "pages": [394],
    "part": "part02",
    "vol": "上",
    "volume": "上",
    "columns": COLUMNS,
    "rows": ROWS,
    "row_count": len(ROWS),
    "col_count": len(COLUMNS),
    "status": "verified",
    "notes": "已据页级OCR核录：workbench/ocr/paddle_ocr/上/part02/page_0097.txt；并参考 raw 坐标 OCR：workbench/ocr/raw/上/part02/page_0097.json 与 raw 文本 workbench/table_entries/上/raw/LYG-上-T014_394.txt。源页表5-14为按交易性质列示的汇总表；OCR 将“析产”拆行为近似“分/析”，按房地产交易事项语义与同列位置合并为“析产”；换契行源页未见成交额数值处保留空值。",
}


def patch_entry(entry: dict) -> bool:
    if entry.get("table_id") != "LYG-上-T014":
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
