# -*- coding: utf-8 -*-
"""Verify LYG-中-T028 chemical industry award products continuation table."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
DATA = ROOT / "workbench" / "table_entries" / "中" / "data" / "LYG-中-T028.json"

COLUMNS = ["年份", "产品名称", "获奖级别", "生产厂家"]
ROWS = [
    ["1989", "十溴联苯醚", "省优", "江苏省盐业公司黄海化工厂"],
    ["1989", "工业赤磷", "国家银质", "市锦屏化工厂"],
    ["1989", "食品级磷酸氢钙(复评)", "省优", "市红旗化工厂"],
    ["1990", "辛硫磷乳油", "省优", "市第二农药厂"],
    ["1990", "甲酰胺(复评)", "省优", "市曙光化工厂"],
    ["1990", "咪唑啉两性表面活性剂", "省优", "市日用化工厂"],
    ["1990", "碳化硅", "省优", "市碳化硅厂"],
]

PATCH = {
    "title": "1980~1990年连云港市化学工业获奖产品一览表（续表）",
    "table_number": "表20-16",
    "page": 1094,
    "pages": [1094],
    "columns": COLUMNS,
    "rows": ROWS,
    "row_count": len(ROWS),
    "col_count": len(COLUMNS),
    "status": "verified",
    "notes": "已据页级OCR回源核录：workbench/ocr/paddle_ocr/中/part01/page_0191.txt；主表题和表号见page_0189.txt。表注：省优、部优分别为省优质产品、部优质产品。",
}


def patch_entry(entry: dict) -> bool:
    if entry.get("table_id") != "LYG-中-T028":
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
