# -*- coding: utf-8 -*-
"""Verify LYG-中-T043 cargo throughput category table from page OCR."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
DATA = ROOT / "workbench" / "table_entries" / "中" / "data" / "LYG-中-T043.json"

COLUMNS = ["货物分类", "合计(万吨)", "出口外贸(万吨)", "出口内贸(万吨)", "进口外贸(万吨)", "进口内贸(万吨)"]
ROWS = [
    ["煤炭", "415.92", "132.90", "283.00", "0.02", ""],
    ["石油", "6.60", "3.20", "0.20", "3.20", ""],
    ["金属矿石", "2.10", "", "", "2.10", ""],
    ["钢铁", "164.30", "", "", "164.30", ""],
    ["矿建材料", "2.71", "0.01", "2.70", "", ""],
    ["水泥", "4.40", "", "4.40", "", ""],
    ["木材", "66.97", "0.83", "0.05", "65.20", "0.89"],
    ["非金属矿石", "4.89", "1.60", "3.29", "", ""],
    ["化肥及农药", "39.12", "0.10", "", "39.00", "0.02"],
    ["盐", "128.20", "16.10", "73.30", "38.80", ""],
    ["粮食", "27.70", "17.10", "0.40", "10.20", ""],
    ["其它", "66.19", "29.60", "0.20", "36.30", "0.09"],
]

PATCH = {
    "title": "1985年连云港货物吞吐量分类统计表",
    "table_number": "表29-6",
    "page": 1357,
    "pages": [1357],
    "columns": COLUMNS,
    "rows": ROWS,
    "row_count": len(ROWS),
    "col_count": len(COLUMNS),
    "status": "verified",
    "notes": "已据页级OCR回源核录：workbench/ocr/paddle_ocr/中/part01/page_0454.txt；原表按出口/进口分外贸、内贸列，OCR未列数值的单元格保留空值。",
}


def patch_entry(entry: dict) -> bool:
    if entry.get("table_id") != "LYG-中-T043":
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
