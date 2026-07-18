# -*- coding: utf-8 -*-
"""Verify LYG-下-T019 notary business statistics continuation page."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
DATA = ROOT / "workbench" / "table_entries" / "下" / "data" / "LYG-下-T019.json"

COLUMNS = [
    "年份",
    "办证数合计(件)",
    "外证件数(件)",
    "外证占比(%)",
    "内证件数(件)",
    "内证占比(%)",
    "国内公证合计(件)",
    "民事件数(件)",
    "民事占比(%)",
    "经济合同件数(件)",
    "经济合同占比(%)",
    "收费合计(万元)",
    "外证收费(元)",
]

ROWS = [
    ["1989", "5682", "148", "2.6", "5534", "97.4", "5534", "1171", "21.2", "4363", "78.8", "14.4", "3500"],
    ["1990", "4089", "161", "3.9", "3928", "96.1", "3923", "1259", "32.1", "2664", "67.9", "10.2", "3552"],
    ["合计", "33226", "623", "1.9", "32603", "98.1", "32603", "5782", "17.7", "26816", "82.3", "81.4", "12264"],
]

PATCH = {
    "title": "1981~1990年连云港市公证业务综合统计表（续表）",
    "table_number": "表44-38",
    "page": 2118,
    "pages": [2118],
    "part": "part01",
    "vol": "下",
    "volume": "下",
    "columns": COLUMNS,
    "rows": ROWS,
    "row_count": len(ROWS),
    "col_count": len(COLUMNS),
    "status": "verified",
    "notes": "已据页级OCR核录：workbench/ocr/paddle_ocr/下/part01/page_0147.txt；表题、表号和列组依据前页 workbench/ocr/paddle_ocr/下/part01/page_0146.txt；并参考 raw 坐标 OCR：workbench/ocr/raw/下/part01/page_0147.json 与 raw 文本 workbench/table_entries/下/raw/LYG-下-T019_2118.txt。此条仅录入表44-38末页续表 1989、1990、合计三行；1990年办证数合计页级OCR误识为4.24，按外证161+内证3928及表内合计关系核定为4089。",
}


def patch_entry(entry: dict) -> bool:
    if entry.get("table_id") != "LYG-下-T019":
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
