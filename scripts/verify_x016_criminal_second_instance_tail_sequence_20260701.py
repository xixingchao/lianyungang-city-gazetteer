# -*- coding: utf-8 -*-
"""Verify LYG-下-T016 criminal second-instance case table continuation."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
DATA = ROOT / "workbench" / "table_entries" / "下" / "data" / "LYG-下-T016.json"

COLUMNS = ["年份", "旧存(件)", "新收(件)", "审结(件)", "续页可见数值序列", "说明"]

ROWS = [
    ["1983", "1", "112", "111", "96、96、8、8、8、3、4、2", "承接表44-22复合表头的上诉、抗诉结果栏；右侧小列按源页横向可见顺序保留。"],
    ["1984", "2", "112", "112", "96、150、7、9、8、1、1、2", "承接表44-22复合表头的上诉、抗诉结果栏；右侧小列按源页横向可见顺序保留。"],
    ["1985", "2", "8", "8", "6、9、2、2、11", "承接表44-22复合表头的上诉、抗诉结果栏；右侧小列按源页横向可见顺序保留。"],
    ["1986", "2", "93", "84", "73、96、9、11、2、11", "承接表44-22复合表头的上诉、抗诉结果栏；右侧小列按源页横向可见顺序保留。"],
    ["1987", "11", "38", "79", "65、84、5、8、4、1、1、1、2、4", "承接表44-22复合表头的上诉、抗诉结果栏；右侧小列按源页横向可见顺序保留。"],
    ["1988", "", "78", "76", "63、92、4、6、6、1、1、1、1、4、2", "承接表44-22复合表头的上诉、抗诉结果栏；右侧小列按源页横向可见顺序保留。"],
    ["1989", "2", "61", "62", "50、80、7、10、1、2、2、1、1、1、1", "承接表44-22复合表头的上诉、抗诉结果栏；右侧小列按源页横向可见顺序保留。"],
    ["1990", "1", "105", "91", "77、121、6、7、5、1、1、4、15", "承接表44-22复合表头的上诉、抗诉结果栏；右侧小列按源页横向可见顺序保留。"],
    ["合计", "87", "732", "746", "632、786、67、75、38、11、9、6、8、9、17、27、5", "承接表44-22复合表头的上诉、抗诉结果栏；右侧小列按源页横向可见顺序保留。"],
]

PATCH = {
    "title": "1976~1990年连云港市中级人民法院审结刑事二审案件统计表续表",
    "table_number": "表44-22",
    "page": 2096,
    "pages": [2096],
    "part": "part01",
    "vol": "下",
    "volume": "下",
    "columns": COLUMNS,
    "rows": ROWS,
    "row_count": len(ROWS),
    "col_count": len(COLUMNS),
    "status": "verified",
    "notes": "已据页级OCR核录续页：workbench/ocr/paddle_ocr/下/part01/page_0125.txt；表题、表号和复合表头承接前页 workbench/ocr/paddle_ocr/下/part01/page_0124.txt。并参考 raw 坐标OCR workbench/ocr/raw/下/part01/page_0125.json 与 raw 文本 workbench/table_entries/下/raw/LYG-下-T016_2096.txt。因源页右侧结果栏小列密集，续页可见数值按横向顺序保留为序列，未据合计关系反推缺失小格；页末正文未并入。",
}


def patch_entry(entry: dict) -> bool:
    if entry.get("table_id") != "LYG-下-T016":
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
