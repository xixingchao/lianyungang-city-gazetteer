# -*- coding: utf-8 -*-
"""Verify LYG-下-T046 primary school list page with county boundary."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
DATA = ROOT / "workbench" / "table_entries" / "下" / "data" / "LYG-下-T046.json"

COLUMNS = ["表段", "校名", "班数(个)", "学生数(人)", "创办年份", "所辖一般小学数(所)"]

ROWS = [
    ["1990年赣榆县小学一览表（续表）", "马站中心小学", "9", "439", "1949", "21"],
    ["1990年赣榆县小学一览表（续表）", "黑林中心小学", "10", "417", "1929", "17"],
    ["1990年赣榆县小学一览表（续表）", "殷庄中心小学", "8", "311", "1929", "12"],
    ["1990年赣榆县小学一览表（续表）", "大岭中心小学", "9", "410", "1958", "18"],
    ["1990年赣榆县小学一览表（续表）", "宋庄中心小学", "9", "361", "1958", "12"],
    ["1990年赣榆县小学一览表（续表）", "城东中心小学", "7", "326", "1968", "10"],
    ["1990年赣榆县小学一览表（续表）", "夹山中心小学", "6", "261", "1952", "10"],
    ["1990年赣榆县小学一览表（续表）", "九里中心小学", "10", "380", "1950", "11"],
    ["1990年赣榆县小学一览表（续表）", "徐山中心小学", "8", "315", "1949", "8"],
    ["1990年赣榆县小学一览表（续表）", "柘汪中心小学", "7", "344", "1929", "9"],
    ["1990年赣榆县小学一览表（续表）", "吴山中心小学", "7", "264", "1942", "4"],
    ["1990年赣榆县小学一览表（续表）", "塔山中心小学", "5", "137", "1962", "3"],
    ["1990年赣榆县小学一览表（续表）", "实验小学", "14", "909", "1948", ""],
    ["1990年赣榆县小学一览表（续表）", "其它", "", "", "", "3"],
    ["1990年东海县小学一览表", "青湖中心小学", "15", "589", "1925", "21"],
    ["1990年东海县小学一览表", "牛山镇中心小学", "12", "571", "1973", "6"],
    ["1990年东海县小学一览表", "牛山乡中心小学", "6", "188", "1964", "15"],
    ["1990年东海县小学一览表", "双店中心小学", "10", "362", "1943", "23"],
    ["1990年东海县小学一览表", "驼峰中心小学", "12", "518", "1948", "22"],
    ["1990年东海县小学一览表", "石湖中心小学", "10", "331", "1950", "14"],
    ["1990年东海县小学一览表", "房山中心小学", "15", "711", "1915", "28"],
    ["1990年东海县小学一览表", "浦南中心小学", "10", "413", "1953", "26"],
    ["1990年东海县小学一览表", "南辰中心小学", "10", "289", "1943", "9"],
    ["1990年东海县小学一览表", "平明中心小学", "5", "225", "1916", "30"],
    ["1990年东海县小学一览表", "洪庄中心小学", "7", "222", "1948", "14"],
    ["1990年东海县小学一览表", "山左口中心小学", "8", "290", "1950", "19"],
]

PATCH = {
    "title": "1990年赣榆县小学一览表末段及东海县小学一览表首页",
    "table_number": "表50-2；表50-3",
    "page": 2334,
    "pages": [2334],
    "part": "part01",
    "vol": "下",
    "volume": "下",
    "columns": COLUMNS,
    "rows": ROWS,
    "row_count": len(ROWS),
    "col_count": len(COLUMNS),
    "status": "verified",
    "notes": "已据页级OCR核录：workbench/ocr/paddle_ocr/下/part01/page_0363.txt；表50-2标题依据前页 workbench/ocr/paddle_ocr/下/part01/page_0362.txt，表50-3标题见本页；并参考 raw 文本 workbench/table_entries/下/raw/LYG-下-T046_2334.txt。此页包含赣榆县小学一览表末段和东海县小学一览表首页，故新增表段列区分来源；实验小学源页未见所辖一般小学数，保留空值。",
}


def patch_entry(entry: dict) -> bool:
    if entry.get("table_id") != "LYG-下-T046":
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
