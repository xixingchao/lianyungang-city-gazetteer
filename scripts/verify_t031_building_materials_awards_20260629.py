# -*- coding: utf-8 -*-
"""Verify LYG-中-T031 building materials award products table."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
DATA = ROOT / "workbench" / "table_entries" / "中" / "data" / "LYG-中-T031.json"

COLUMNS = ["产品型号名称", "生产企业", "获奖级别", "获奖年份"]
ROWS = [
    ["0.4级轻质漂珠耐火砖", "市节能材料厂", "国家优秀项目奖", "1987"],
    ["塑料门窗", "连云港市东航建筑塑料制品开发公司", "省优秀新产品“金牛”奖", "1987"],
    ["粘土平瓦", "连云港制瓦厂", "省优", "1988"],
    ["“雄鸡”牌玻璃马赛克", "赣榆县玻璃厂", "省优秀新产品“金牛”奖", "1988"],
    ["“雄鸡”牌玻璃马赛克", "赣榆县玻璃厂", "省优", "1989"],
    ["50立方米耐腐蚀玻璃钢贮罐", "玻纤玻钢总厂", "部优", "1990"],
    ["直径1000毫米以下玻璃钢管道", "连云港玻纤玻钢总厂", "省优秀新产品“金牛”奖", "1990"],
    ["玻璃制品大理石", "连云港市经济开发区石材公司", "省优秀新产品“金牛”奖", "1990"],
]

PATCH = {
    "title": "1987~1990年连云港市建材工业获奖产品一览表",
    "table_number": "表23-5",
    "page": 1198,
    "pages": [1198],
    "columns": COLUMNS,
    "rows": ROWS,
    "row_count": len(ROWS),
    "col_count": len(COLUMNS),
    "status": "verified",
    "notes": "已据页级OCR回源核录：workbench/ocr/paddle_ocr/中/part01/page_0295.txt。",
}


def patch_entry(entry: dict) -> bool:
    if entry.get("table_id") != "LYG-中-T031":
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
