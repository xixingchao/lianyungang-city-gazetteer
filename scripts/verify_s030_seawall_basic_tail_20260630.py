# -*- coding: utf-8 -*-
"""Verify seawall basic information continuation table T030."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
DATA = ROOT / "workbench" / "table_entries" / "上" / "data" / "LYG-上-T030.json"

COLUMNS = [
    "管理单位",
    "地点起",
    "地点迄",
    "堤长(公里)",
    "堤顶高程(米)",
    "堤顶宽(米)",
    "堤坡比迎水坡",
    "堤坡比背水坡",
    "备注",
]

ROWS = [
    ["灌西盐场", "洋桥闸", "天生港", "20.20", "6~6.5", "5", "1:3", "1:3", "防浪墙4.1公里，石护坡4公里"],
    ["灌云县", "天生港", "炮阵地", "1.08", "6.5", "6", "1:3", "1:2", "块石护坡960米"],
    ["灌西盐场", "炮阵地", "运销站", "0.61", "6~6.5", "5", "1:3", "1:3", ""],
    ["", "运销站", "燕尾闸下", "0.49", "5.5", "3", "1:3", "1:3", "岸墙型式"],
    ["灌云县", "团港段", "", "2.18", "5.5", "3", "1:2", "1:2", ""],
    ["灌云县盐场", "六圩港西", "洋桥闸", "17.25", "4.5~5", "3", "1:4~1:8", "1:3", "在灌西盐场海堤外80~120米"],
]

PATCH = {
    "table_id": "LYG-上-T030",
    "title": "1990年连云港市海堤基本情况表（续表）",
    "table_number": "表10-15",
    "page": 603,
    "pages": [603],
    "part": "part02",
    "vol": "上",
    "volume": "上",
    "columns": COLUMNS,
    "rows": ROWS,
    "row_count": len(ROWS),
    "col_count": len(COLUMNS),
    "status": "verified",
    "notes": "已据页级OCR回源核录：表题、表号和表头见 workbench/ocr/paddle_ocr/上/part02/page_0302.txt；续表内容见 workbench/ocr/paddle_ocr/上/part02/page_0303.txt，并参考 raw OCR workbench/table_entries/上/raw/LYG-上-T030_603.txt。原JSON串入气象降水蒸发数据；本次仅录入续页可见的海堤记录。团港段一行源页未单列终点，地点迄保留空值。",
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
