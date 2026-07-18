# -*- coding: utf-8 -*-
"""Verify LYG-下-T070 1990 technical staff continuation."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
DATA = ROOT / "workbench" / "table_entries" / "下" / "data" / "LYG-下-T070.json"

COLUMNS = [
    "专业结构",
    "男",
    "女",
    "35岁以下",
    "36-45岁",
    "46-55岁",
    "56-60岁",
    "61岁以上",
    "高级",
    "中级",
    "初级助理级",
    "员级",
    "总计",
]

ROWS = [
    ["技工学校教师", "139", "45", "102", "42", "30", "8", "2", "9", "71", "80", "24", "184"],
    ["卫生技术人员", "3471", "4568", "3634", "2350", "1579", "352", "124", "185", "1741", "3888", "2225", "8039"],
    ["新闻专业人员", "147", "21", "75", "63", "22", "4", "4", "11", "61", "89", "7", "168"],
    ["翻译人员", "66", "31", "43", "27", "18", "2", "7", "3", "63", "31", "", "97"],
    ["播音员", "7", "5", "2", "10", "", "", "", "5", "7", "", "", "12"],
    ["出版专业人员", "34", "6", "7", "13", "15", "3", "2", "1", "30", "9", "", "40"],
    ["图书资料人员", "141", "177", "153", "68", "78", "11", "8", "4", "77", "150", "87", "318"],
    ["文博人员", "27", "19", "10", "20", "8", "8", "", "3", "10", "29", "4", "46"],
    ["档案人员", "318", "364", "351", "220", "96", "7", "8", "5", "79", "367", "231", "682"],
    ["体育教练", "29", "2", "10", "10", "8", "3", "", "4", "16", "11", "", "31"],
    ["艺术人员", "161", "60", "64", "60", "78", "12", "7", "7", "102", "95", "17", "221"],
    ["律师", "58", "5", "35", "16", "5", "7", "", "5", "12", "23", "23", "63"],
    ["公证员", "76", "8", "19", "35", "25", "4", "1", "1", "21", "38", "24", "84"],
    ["船舶技术人员", "43", "2", "20", "9", "14", "2", "", "3", "13", "12", "17", "45"],
    ["海关专业人员", "111", "19", "98", "26", "4", "2", "", "2", "21", "96", "11", "130"],
    ["民航飞行技术人员", "2", "1", "2", "1", "", "", "", "", "1", "2", "", "3"],
    ["政工专业人员", "1320", "232", "512", "521", "377", "84", "58", "47", "428", "655", "422", "1552"],
    ["合计", "51383", "22020", "32223", "20440", "14681", "5178", "881", "2037", "14788", "33201", "23377", "73403"],
]

PATCH = {
    "title": "1990年连云港市有技术职称(职务)的科技人员情况一览表续表",
    "table_number": "表51-3",
    "page": 2393,
    "pages": [2393],
    "part": "part01",
    "vol": "下",
    "volume": "下",
    "columns": COLUMNS,
    "rows": ROWS,
    "row_count": len(ROWS),
    "col_count": len(COLUMNS),
    "status": "verified",
    "notes": "已据页级OCR核录：workbench/ocr/paddle_ocr/下/part01/page_0422.txt；表题、表号和复合表头据前页 workbench/ocr/paddle_ocr/下/part01/page_0421.txt。并参考 raw 坐标OCR workbench/ocr/raw/下/part01/page_0422.json 与 raw 文本 workbench/table_entries/下/raw/LYG-下-T070_2393.txt。本条原题名仅列表号，实际为表51-3续页；按横向坐标与男女性别、年龄结构、职称结构合计关系校验。源页空白单元格保留空值；总计行粘连的51383与22020按坐标拆分。",
}


def patch_entry(entry: dict) -> bool:
    if entry.get("table_id") != "LYG-下-T070":
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
