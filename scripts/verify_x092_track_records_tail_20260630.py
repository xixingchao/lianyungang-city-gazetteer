# -*- coding: utf-8 -*-
"""Verify LYG-下-T092 track-and-field records continuation page."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
DATA = ROOT / "workbench" / "table_entries" / "下" / "data" / "LYG-下-T092.json"

COLUMNS = [
    "项目",
    "成年男子",
    "成年女子",
    "少年男子",
    "少年女子",
    "小学男子",
    "小学女子",
]

ROWS = [
    ["110米栏", "15\"3", "", "15\"1", "", "", ""],
    ["4×100接力", "44\"3", "52\"5", "47\"", "52\"5", "56\"", "58\"5"],
    ["跳高", "1.81", "1.57", "1.78", "1.48", "1.32", "1.24"],
    ["跳远", "6.81", "5.33", "6.40", "5.33", "5.47", "4.33"],
    ["三级跳远", "14.30", "", "13.58", "", "", ""],
    ["铅球", "14.17(7.26公斤)", "11.21(4公斤)", "14.02(6公斤)", "10.22(4公斤)", "11.14(3公斤)", "8.99(3公斤)"],
    ["铁饼", "40.60(2公斤)", "36.20(1公斤)", "44.44(1.5公斤)", "34.30(1公斤)", "", ""],
    ["标枪", "54.34(0.8公斤)", "40.58(0.6公斤)", "54.42(0.6公斤)", "37.34(0.6公斤)", "", ""],
    ["垒球", "", "", "", "", "56.36", "49.86"],
    ["三项全能", "", "1756", "", "1657", "1061", "1171"],
    ["五项全能", "2373", "3276", "2673", "3276", "", ""],
    ["5000米竞走", "29'11\"6", "29'30\"5", "", "30'38\"1", "", ""],
    ["10000米竞走", "45'20\"3", "", "45'20\"3", "", "", ""],
]

PATCH = {
    "title": "1989年连云港市田径最高纪录（续表）",
    "table_number": "表56-12",
    "page": 2688,
    "pages": [2688],
    "part": "part02",
    "vol": "下",
    "volume": "下",
    "columns": COLUMNS,
    "rows": ROWS,
    "row_count": len(ROWS),
    "col_count": len(COLUMNS),
    "status": "verified",
    "notes": "已据页级OCR核录：workbench/ocr/paddle_ocr/下/part02/page_0256.txt；表题与表号依据前页 workbench/ocr/paddle_ocr/下/part02/page_0255.txt；并参考 raw 坐标 OCR：workbench/ocr/raw/下/part02/page_0256.json 与 raw 文本 workbench/table_entries/下/raw/LYG-下-T092_2688.txt。此条仅录入 page_0256 可见的田径最高纪录续表成绩。",
}


def patch_entry(entry: dict) -> bool:
    if entry.get("table_id") != "LYG-下-T092":
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
