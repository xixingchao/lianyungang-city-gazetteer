# -*- coding: utf-8 -*-
"""Verify LYG-下-T045 primary school list page with county boundary."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
DATA = ROOT / "workbench" / "table_entries" / "下" / "data" / "LYG-下-T045.json"

COLUMNS = ["表段", "校名", "班数(个)", "学生数(人)", "创办年份", "教职工数(人)", "所辖一般小学数(所)"]

ROWS = [
    ["1988年连云港市市区小学一览表（末段）", "西山小学", "2", "43", "不详", "3", ""],
    ["1988年连云港市市区小学一览表（末段）", "大竹园小学", "2", "35", "不详", "3", ""],
    ["1988年连云港市市区小学一览表（末段）", "高公岛学校", "9", "360", "1946", "30", ""],
    ["1988年连云港市市区小学一览表（末段）", "黄窝小学", "2", "59", "1946", "2", ""],
    ["1988年连云港市市区小学一览表（末段）", "白沙小学", "6", "207", "不详", "16", ""],
    ["1988年连云港市市区小学一览表（末段）", "西山小学(连岛)", "5", "173", "不详", "6", ""],
    ["1988年连云港市市区小学一览表（末段）", "东山小学", "4", "132", "不详", "6", ""],
    ["1988年连云港市市区小学一览表（末段）", "东连岛小学", "3", "49", "1946", "4", ""],
    ["1990年赣榆县小学一览表", "青口中心小学", "22", "1124", "1898", "", "5"],
    ["1990年赣榆县小学一览表", "赣马中心小学", "10", "404", "1903", "", "18"],
    ["1990年赣榆县小学一览表", "沙河中心小学", "12", "427", "1912", "", "26"],
    ["1990年赣榆县小学一览表", "金山中心小学", "11", "514", "1914", "", "28"],
    ["1990年赣榆县小学一览表", "城头中心小学", "10", "542", "1914", "", "24"],
    ["1990年赣榆县小学一览表", "石桥中心小学", "12", "508", "1929", "", "17"],
    ["1990年赣榆县小学一览表", "墩尚中心小学", "10", "423", "1914", "", "21"],
    ["1990年赣榆县小学一览表", "朱堵中心小学", "9", "424", "1949", "", "15"],
    ["1990年赣榆县小学一览表", "海头中心小学", "10", "441", "1914", "", "12"],
    ["1990年赣榆县小学一览表", "欢墩中心小学", "8", "325", "1914", "", "14"],
    ["1990年赣榆县小学一览表", "厉庄中心小学", "8", "348", "1934", "", "23"],
    ["1990年赣榆县小学一览表", "城南中心小学", "9", "405", "1958", "", "15"],
    ["1990年赣榆县小学一览表", "罗阳中心小学", "8", "289", "1949", "", "15"],
    ["1990年赣榆县小学一览表", "龙河中心小学", "8", "310", "1952", "", "16"],
    ["1990年赣榆县小学一览表", "土城中心小学", "10", "484", "1929", "", "14"],
    ["1990年赣榆县小学一览表", "门河中心小学", "9", "350", "1929", "", "18"],
    ["1990年赣榆县小学一览表", "官河中心小学", "9", "369", "1949", "", "18"],
    ["1990年赣榆县小学一览表", "班庄中心小学", "8", "300", "1929", "", "12"],
]

PATCH = {
    "title": "1988年市区小学一览表末段及1990年赣榆县小学一览表首页",
    "table_number": "表50-1；表50-2",
    "page": 2333,
    "pages": [2333],
    "part": "part01",
    "vol": "下",
    "volume": "下",
    "columns": COLUMNS,
    "rows": ROWS,
    "row_count": len(ROWS),
    "col_count": len(COLUMNS),
    "status": "verified",
    "notes": "已据页级OCR核录：workbench/ocr/paddle_ocr/下/part01/page_0362.txt；表50-1标题依据前页 workbench/ocr/paddle_ocr/下/part01/page_0357.txt，表50-2标题见本页；并参考 raw 文本 workbench/table_entries/下/raw/LYG-下-T045_2333.txt。此页包含市区小学一览表末段和赣榆县小学一览表首页，故新增表段列区分来源；市区小学段使用教职工数列，赣榆县小学段使用所辖一般小学数列，另一侧保留空值。",
}


def patch_entry(entry: dict) -> bool:
    if entry.get("table_id") != "LYG-下-T045":
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
