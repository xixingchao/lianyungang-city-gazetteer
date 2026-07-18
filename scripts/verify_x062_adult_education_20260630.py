# -*- coding: utf-8 -*-
"""Verify LYG-下-T062 adult education basic situation table."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
DATA = ROOT / "workbench" / "table_entries" / "下" / "data" / "LYG-下-T062.json"

COLUMNS = ["类别", "指标", "全市", "其中：市区", "备注"]
ROWS = [
    ["成人高校", "学校数(班)(个)", "3", "", ""],
    ["成人高校", "学生数(人)", "1281", "", ""],
    ["成人高校", "教职工(人)", "295", "", ""],
    ["成人高校", "其中：专任教师", "146", "", ""],
    ["成人中等专业技术学校", "学校数(班)(个)", "11", "6", "1985年后为成人中专校数字，此前为成人农民职业技术学校数字。"],
    ["成人中等专业技术学校", "学生数(人)", "5301", "1523", ""],
    ["成人中等专业技术学校", "教职工(人)", "423", "194", ""],
    ["成人中等专业技术学校", "其中：专任教师", "210", "99", ""],
    ["成人中专", "学校数(班)(个)", "20", "7", ""],
    ["成人中专", "学生数(人)", "3342", "1727", ""],
    ["成人中专", "教职工(人)", "165", "41", ""],
    ["成人中专", "其中：专任教师", "110", "9", ""],
    ["成人中专", "兼任教师", "114", "60", ""],
    ["成人初等教育", "学校数(班)(个)", "1886", "105", ""],
    ["成人初等教育", "学生数(人)", "79871", "4600", ""],
    ["成人初等教育", "教职工数(人)", "206", "100", ""],
    ["成人初等教育", "其中：专任教师", "106", "14", ""],
    ["成人初等教育", "兼任教师", "1667", "102", ""],
    ["成人农民职业技术学校", "学校数(班)(个)", "127", "22", ""],
    ["成人农民职业技术学校", "学生数(人)", "75506", "17295", ""],
    ["成人农民职业技术学校", "教职工数(人)", "434", "131", ""],
    ["成人农民职业技术学校", "其中：专任教师", "245", "16", ""],
    ["成人农民职业技术学校", "兼任教师", "1270", "423", ""],
]

PATCH = {
    "title": "1990年连云港市成人教育基本情况表",
    "table_number": "表50-20",
    "page": 2370,
    "pages": [2370, 2371],
    "part": "part01",
    "vol": "下",
    "volume": "下",
    "columns": COLUMNS,
    "rows": ROWS,
    "row_count": len(ROWS),
    "col_count": len(COLUMNS),
    "status": "verified",
    "notes": "已据页级OCR核录：workbench/ocr/paddle_ocr/下/part01/page_0399.txt、page_0400.txt，并参考 raw OCR：workbench/table_entries/下/raw/LYG-下-T062_2370.txt、LYG-下-T063_2371.txt。原表为复合行头，结构化为类别、指标、全市、其中市区、备注五列；源页未见数值的市区栏保留空值。",
}


def patch_entry(entry: dict) -> bool:
    if entry.get("table_id") != "LYG-下-T062":
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
