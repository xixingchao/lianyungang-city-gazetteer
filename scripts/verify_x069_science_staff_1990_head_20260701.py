# -*- coding: utf-8 -*-
"""Verify LYG-下-T069 1990 technical staff table head."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
DATA = ROOT / "workbench" / "table_entries" / "下" / "data" / "LYG-下-T069.json"

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
    ["工程技术人员", "11255", "2331", "6293", "3694", "2824", "678", "97", "737", "2539", "5063", "5247", "13586"],
    ["农业技术人员", "2290", "238", "808", "831", "657", "213", "19", "107", "391", "1104", "926", "2528"],
    ["自然科学研究人员", "393", "105", "224", "28", "203", "43", "", "164", "152", "143", "39", "498"],
    ["社会科学研究人员", "1626", "201", "372", "618", "575", "216", "46", "49", "614", "1127", "37", "1827"],
    ["经济专业人员", "7597", "1574", "3526", "2985", "1420", "1130", "110", "81", "1701", "5483", "1906", "9171"],
    ["会计人员", "4501", "3237", "3735", "2345", "1300", "314", "44", "29", "1220", "3202", "3287", "7738"],
    ["统计人员", "763", "655", "612", "530", "233", "33", "10", "3", "131", "708", "576", "1418"],
    ["工艺美术人员", "102", "33", "67", "43", "19", "3", "3", "1", "14", "48", "72", "135"],
    ["高等学校教师", "367", "93", "253", "44", "126", "36", "1", "53", "196", "210", "1", "460"],
    ["实验人员", "27", "25", "26", "15", "8", "3", "", "", "11", "26", "15", "52"],
    ["中专校教师", "500", "180", "310", "133", "181", "46", "10", "59", "267", "290", "64", "680"],
    ["中学教师", "6599", "2435", "4868", "2088", "1394", "579", "105", "459", "2203", "3923", "2449", "9034"],
    ["小学教师", "9213", "5348", "5994", "3594", "3383", "1378", "212", "5", "2598", "6292", "5666", "14561"],
]

PATCH = {
    "title": "1990年连云港市有技术职称(职务)的科技人员情况一览表",
    "table_number": "表51-3",
    "page": 2392,
    "pages": [2392],
    "part": "part01",
    "vol": "下",
    "volume": "下",
    "columns": COLUMNS,
    "rows": ROWS,
    "row_count": len(ROWS),
    "col_count": len(COLUMNS),
    "status": "verified",
    "notes": "已据页级OCR核录：workbench/ocr/paddle_ocr/下/part01/page_0421.txt；并参考 raw 坐标OCR workbench/ocr/raw/下/part01/page_0421.json 与 raw 文本 workbench/table_entries/下/raw/LYG-下-T069_2392.txt。本条原题名未给出有效表题，实际为表51-3首页；仅录入 page_0421 下半页可见的1990年表记录，页首上一表尾项未并入。按横向坐标与男女性别、年龄结构、职称结构合计关系校验；源页空白单元格保留空值。",
}


def patch_entry(entry: dict) -> bool:
    if entry.get("table_id") != "LYG-下-T069":
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
