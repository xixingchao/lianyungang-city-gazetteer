# -*- coding: utf-8 -*-
"""Verify LYG-中-T123 cadre statistics table head."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
DATA = ROOT / "workbench" / "table_entries" / "中" / "data" / "LYG-中-T123.json"

COLUMNS = ["类别", "项目", "1977", "1978", "1979", "1980", "1981", "1982", "1983"]

ROWS = [
    ["干部总数", "合计", "27206", "28472", "29061", "30280", "32482", "35417", "40680"],
    ["干部总数", "妇女", "6162", "6337", "6673", "7193", "7894", "8591", "8835"],
    ["干部总数", "少数民族", "83", "89", "98", "99", "117", "123", "90"],
    ["年龄", "25岁以下", "1957", "1685", "1593", "1982", "3277", "4383", "5966"],
    ["年龄", "26~35岁", "6437", "6473", "6547", "6858", "8489", "8573", "10479"],
    ["年龄", "36~45岁", "10626", "11147", "11531", "11635", "10713", "11782", "12254"],
    ["年龄", "46~55岁", "6442", "7121", "7609", "8139", "8417", "8878", "10145"],
    ["年龄", "56~60岁", "1258", "1442", "1323", "1242", "1212", "1376", "1411"],
    ["年龄", "61岁以上", "486", "604", "458", "424", "374", "425", "425"],
    ["文化程度", "高等院校毕业者", "4289", "4810", "5347", "5494", "6198", "7116", "8935"],
    ["文化程度", "高等院校相当者", "", "", "", "189", "366", "1497", "2527"],
    ["文化程度", "大专毕业者", "", "", "", "8750", "10065", "10726", "12620"],
    ["文化程度", "大专相当者", "", "", "", "260", "341", "1109", "1758"],
    ["文化程度", "高中", "9092", "9809", "10845", "3030", "3430", "3344", "3310"],
    ["文化程度", "初中以下", "13825", "13853", "12869", "12557", "12082", "11625", "11530"],
    ["政治情况", "共产党员", "11491", "12885", "13085", "13785", "14232", "15317", "18504"],
    ["政治情况", "共青团员", "2381", "2406", "2332", "2473", "3641", "4728", "5887"],
    ["政治情况", "民主党派", "", "", "3", "5", "5", "7", "30"],
    ["政治情况", "无党派", "13334", "13181", "13641", "14017", "14604", "15365", "16259"],
]

PATCH = {
    "title": "1977~1990年连云港市干部统计表",
    "table_number": "表41-13",
    "page": 1859,
    "pages": [1859],
    "part": "part02",
    "vol": "中",
    "volume": "中",
    "columns": COLUMNS,
    "rows": ROWS,
    "row_count": len(ROWS),
    "col_count": len(COLUMNS),
    "status": "verified",
    "notes": "已据页级OCR核录：workbench/ocr/paddle_ocr/中/part02/page_0439.txt；并参考 raw 坐标OCR workbench/ocr/raw/中/part02/page_0439.json 与 raw 文本 workbench/table_entries/中/raw/LYG-中-T123_1859.txt。本条原为单列占位，实际为表41-13首页；录入 page_0439 可见的1977至1983年干部总数、年龄、文化程度、政治情况记录。源页未见数值处保留空值；文盲行本页未见数值，未录入。",
}


def patch_entry(entry: dict) -> bool:
    if entry.get("table_id") != "LYG-中-T123":
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
