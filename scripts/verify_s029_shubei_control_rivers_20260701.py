# -*- coding: utf-8 -*-
"""Verify LYG-上-T029 Shubei control river table."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
DATA = ROOT / "workbench" / "table_entries" / "上" / "data" / "LYG-上-T029.json"

COLUMNS = [
    "河名",
    "境内起迄位置",
    "长度(公里)",
    "排水面积(平方公里)",
    "流量(立方米/秒)",
    "河底宽(米)",
    "河底高程(米)",
    "堤顶宽(米)",
    "堤顶高程(米)",
    "堤坡比",
]

ROWS = [
    ["塔山截洪沟", "夹谷山水库一小塔山水库", "16.0", "17", "92.3", "7.5~15", "57.5~43.3", "8.5", "", "1:1~1:2"],
    ["石梁河水库截洪沟", "三清河一石梁河水库", "11.0", "20", "119.0", "16~21", "37.3~24.4", "6~8", "", "1:2"],
    ["沭北一级截洪沟", "夹谷山水库；四号渡槽一小塔山水库", "13.0", "21", "西段136；东段83", "9~25", "43.2~32.4", "8~10", "西段49~40", ""],
    ["沭北二级截洪沟", "石梁河水库一青口渡槽截洪沟口", "17.7", "55", "137.5", "12~35", "30.0~9.7", "", "上游段；老河长6000米；18.88~16.34", "1:2"],
]

PATCH = {
    "title": "1990年连云港市沭北样板控制河道基本情况表",
    "table_number": "表10-13",
    "page": 598,
    "pages": [598],
    "part": "part02",
    "vol": "上",
    "volume": "上",
    "columns": COLUMNS,
    "rows": ROWS,
    "row_count": len(ROWS),
    "col_count": len(COLUMNS),
    "status": "verified",
    "notes": "已据页级OCR核录：workbench/ocr/paddle_ocr/上/part02/page_0298.txt；并参考 raw 坐标 OCR：workbench/ocr/raw/上/part02/page_0298.json 与 raw 文本 workbench/table_entries/上/raw/LYG-上-T029_598.txt。OCR 将“沭北”误作“述北”，已按章节语义和前后文更正；本条仅录入表10-13的4条控制河道记录，后续表10-14未并入。多行单元格按同列位置合并，源页未见数值处保留空值。",
}


def patch_entry(entry: dict) -> bool:
    if entry.get("table_id") != "LYG-上-T029":
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
