# -*- coding: utf-8 -*-
"""Verify LYG-中-T010 canned food enterprise continuation table."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
DATA = ROOT / "workbench" / "table_entries" / "中" / "data" / "LYG-中-T010.json"

COLUMNS = [
    "企业名称",
    "地址",
    "企业性质",
    "职工人数(人)",
    "占地面积(万平方米)",
    "建筑面积(万平方米)",
    "固定资产原值(万元)",
    "产值(万元)",
    "利税(万元)",
    "产量(吨)",
    "年生产能力(吨)",
    "主要产品",
]

ROWS = [
    ["东海县太平渔业公司水产食品厂", "东海县浦南乡太平村", "集体", "50", "0.20", "0.02", "45", "60", "3.50", "150", "250", "鱼类罐头"],
    ["东海县龙门罐头食品厂", "东海县山左口乡", "集体", "11", "0.20", "0.05", "68", "34", "-1.00", "120", "2000", "水果罐头"],
]

PATCH = {
    "title": "1990年连云港市罐头食品加工企业基本情况表（续表）",
    "table_number": "表18-3",
    "page": 985,
    "pages": [985],
    "columns": COLUMNS,
    "rows": ROWS,
    "row_count": len(ROWS),
    "col_count": len(COLUMNS),
    "status": "verified",
    "notes": "已据页级OCR回源核录：workbench/ocr/paddle_ocr/中/part01/page_0082.txt；表题、表号和列头据上一页page_0081.txt确认。本页为表18-3续表尾段，仅录入续表两家企业；后文已进入第四章饮料，未纳入本表。",
}


def patch_entry(entry: dict) -> bool:
    if entry.get("table_id") != "LYG-中-T010":
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
