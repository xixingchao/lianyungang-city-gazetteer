# -*- coding: utf-8 -*-
"""Verify LYG-下-T067/T068 technical staff tables for 1979 and 1983."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
DATA_DIR = ROOT / "workbench" / "table_entries" / "下" / "data"

BASE_COLUMNS = [
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
MIXED_COLUMNS = ["年份", "表号", *BASE_COLUMNS]

ROWS_1979_HEAD = [
    ["工程技术人员", "410", "77", "182", "172", "106", "24", "3", "9", "74", "137", "267", "487"],
    ["农业技术人员", "24", "5", "10", "13", "3", "1", "2", "1", "18", "10", "", "29"],
    ["社会科学研究人员", "1", "", "", "", "1", "", "", "", "1", "", "", "1"],
    ["经济专业人员", "43", "5", "1", "30", "14", "1", "2", "2", "7", "29", "10", "48"],
    ["会计人员", "32", "29", "21", "20", "12", "5", "3", "", "12", "18", "31", "61"],
    ["统计人员", "1", "5", "3", "2", "1", "", "", "", "2", "2", "2", "6"],
    ["工艺美术人员", "14", "5", "3", "12", "4", "", "", "3", "5", "4", "7", "19"],
    ["高等学校教师", "68", "16", "8", "12", "32", "27", "5", "", "50", "33", "1", "84"],
    ["实验人员", "9", "6", "4", "7", "4", "", "", "", "4", "8", "3", "15"],
]

ROWS_1979_TAIL = [
    ["1979", "表51-1", "中专校教师", "1", "", "", "", "1", "", "", "", "1", "", "", "1"],
    ["1979", "表51-1", "中学教师", "28", "20", "", "17", "31", "", "", "", "", "48", "", "48"],
    ["1979", "表51-1", "小学教师", "2", "", "", "", "2", "", "", "", "2", "", "", "2"],
    ["1979", "表51-1", "技工学校教师", "20", "2", "8", "13", "1", "", "", "", "1", "21", "", "22"],
    ["1979", "表51-1", "卫生技术人员", "757", "930", "807", "666", "175", "27", "12", "2", "40", "1202", "443", "1687"],
    ["1979", "表51-1", "图书资料人员", "7", "9", "7", "2", "4", "1", "2", "1", "9", "6", "", "16"],
    ["1979", "表51-1", "船舶技术人员", "25", "", "9", "13", "", "1", "1", "11", "5", "9", "", "25"],
    ["1979", "表51-1", "政工专业人员", "", "", "", "", "", "", "", "", "", "", "", ""],
    ["1979", "表51-1", "合计", "1440", "1111", "1059", "979", "391", "92", "30", "72", "202", "1427", "850", "2551"],
]

ROWS_1983_HEAD = [
    ["1983", "表51-2", "工程技术人员", "2182", "449", "773", "1007", "660", "144", "47", "2", "575", "1101", "953", "2631"],
    ["1983", "表51-2", "农业技术人员", "550", "61", "97", "207", "219", "73", "15", "", "175", "276", "160", "611"],
    ["1983", "表51-2", "自然科学研究人员", "9", "2", "2", "4", "5", "", "", "4", "5", "2", "", "11"],
    ["1983", "表51-2", "社会科学研究人员", "1", "2", "2", "", "1", "", "", "", "1", "2", "", "3"],
    ["1983", "表51-2", "经济专业人员", "55", "18", "7", "24", "30", "12", "", "", "15", "39", "19", "73"],
    ["1983", "表51-2", "会计人员", "636", "481", "188", "645", "215", "59", "10", "53", "267", "797", "", "1117"],
    ["1983", "表51-2", "统计人员", "196", "132", "90", "140", "85", "8", "5", "16", "68", "244", "", "328"],
    ["1983", "表51-2", "工艺美术人员", "3", "", "3", "", "", "", "", "", "3", "", "", "3"],
    ["1983", "表51-2", "高等学校教师", "51", "6", "17", "11", "28", "1", "", "", "57", "", "", "57"],
    ["1983", "表51-2", "实验人员", "1", "1", "2", "", "", "", "", "", "2", "", "", "2"],
    ["1983", "表51-2", "中专校教师", "12", "3", "4", "3", "6", "1", "1", "", "8", "7", "", "15"],
    ["1983", "表51-2", "中学教师", "9", "4", "1", "2", "8", "2", "", "", "11", "2", "", "13"],
    ["1983", "表51-2", "小学教师", "1", "", "1", "", "", "", "", "", "1", "", "", "1"],
]

PATCHES = {
    "LYG-下-T067": {
        "title": "1979年连云港市有技术职称(职务)的科技人员情况一览表",
        "table_number": "表51-1",
        "page": 2390,
        "pages": [2390],
        "part": "part01",
        "vol": "下",
        "volume": "下",
        "columns": BASE_COLUMNS,
        "rows": ROWS_1979_HEAD,
        "status": "verified",
        "notes": "已据页级OCR核录：workbench/ocr/paddle_ocr/下/part01/page_0419.txt；并参考 raw 坐标OCR workbench/ocr/raw/下/part01/page_0419.json 与 raw 文本 workbench/table_entries/下/raw/LYG-下-T067_2390.txt。表头展开承接源页的性别结构、年龄结构、职称结构；本页录入1979年表首页可见的工程技术人员至实验人员记录。源页横线或未见数值处保留空值；按性别、年龄、职称三组分项与总计关系核验。",
    },
    "LYG-下-T068": {
        "title": "1979年科技人员情况表续页及1983年科技人员情况表首页",
        "table_number": "表51-1、表51-2",
        "page": 2391,
        "pages": [2391],
        "part": "part01",
        "vol": "下",
        "volume": "下",
        "columns": MIXED_COLUMNS,
        "rows": ROWS_1979_TAIL + ROWS_1983_HEAD,
        "status": "verified",
        "notes": "已据页级OCR核录：workbench/ocr/paddle_ocr/下/part01/page_0420.txt；并参考 raw 坐标OCR workbench/ocr/raw/下/part01/page_0420.json 与 raw 文本 workbench/table_entries/下/raw/LYG-下-T068_2391.txt。源页上半为表51-1的1979年续页，下半为表51-2的1983年首页，因此增加年份、表号两列区分来源。源页横线或未见数值处保留空值；按性别、年龄、职称三组分项与总计关系核验，政工专业人员行源页未见分项数值，仅保留行名。",
    },
}

for patch in PATCHES.values():
    patch["row_count"] = len(patch["rows"])
    patch["col_count"] = len(patch["columns"])


def patch_entry(entry: dict) -> bool:
    patch = PATCHES.get(entry.get("table_id"))
    if not patch:
        return False
    changed = False
    for key, value in patch.items():
        if entry.get(key) != value:
            entry[key] = value
            changed = True
    return changed


def patch_json() -> int:
    changed = 0
    for table_id in PATCHES:
        path = DATA_DIR / f"{table_id}.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        if patch_entry(data):
            path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            changed += 1
    return changed


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
