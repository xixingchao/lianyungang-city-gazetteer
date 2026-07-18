# -*- coding: utf-8 -*-
"""Verify LYG-下-T049 six-year primary school teaching plan head page."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
DATA = ROOT / "workbench" / "table_entries" / "下" / "data" / "LYG-下-T049.json"

COLUMNS = [
    "课程类别",
    "项目",
    "一年级",
    "二年级",
    "三年级",
    "四年级",
    "五年级",
    "六年级",
    "上课总时数",
    "备注",
]

ROWS = [
    ["课程", "思想品德", "1", "1", "1", "1", "1", "1", "216", ""],
    ["语文", "小计", "11", "11", "11", "9", "9", "9", "2160", ""],
    ["语文", "讲读", "10", "10", "8", "6", "6", "6", "", ""],
    ["语文", "作文", "", "", "2", "2", "2", "2", "", ""],
    ["语文", "写字指导", "1", "1", "1", "1", "", "1", "", ""],
    ["课程", "数学", "6", "6", "6", "6", "6", "6", "1296", ""],
    ["课程", "自然", "", "", "", "2", "2", "2", "216", ""],
    ["课程", "地理", "", "", "", "", "2", "", "72", ""],
    ["课程", "历史", "", "", "", "", "", "2", "72", ""],
    ["课程", "体育", "2", "2", "2", "2", "2", "2", "430", ""],
    ["课程", "音乐", "2", "2", "2", "2", "2", "2", "430", ""],
    ["课程", "美术", "2", "2", "2", "2", "1", "1", "360", ""],
    ["课程", "劳动", "", "", "1", "1", "1", "1", "144", ""],
    ["合计", "并开科目", "6", "6", "7", "8", "9", "9", "", ""],
    ["合计", "每周总课时", "24", "24", "25", "25", "26", "26", "5400", ""],
]

PATCH = {
    "title": "1984年连云港市市区全日制六年制小学教学计划表",
    "table_number": "表50-6",
    "page": 2338,
    "pages": [2338],
    "part": "part01",
    "vol": "下",
    "volume": "下",
    "columns": COLUMNS,
    "rows": ROWS,
    "row_count": len(ROWS),
    "col_count": len(COLUMNS),
    "status": "verified",
    "notes": "已据页级OCR核录：workbench/ocr/paddle_ocr/下/part01/page_0367.txt；并参考 raw OCR：workbench/table_entries/下/raw/LYG-下-T049_2338.txt。此页为表50-6首页下半页可见课程项目，下一页课外活动续表已由 LYG-下-T050 承接。OCR中横线字形按源页行列与总时数关系处理为空值。",
}


def patch_entry(entry: dict) -> bool:
    if entry.get("table_id") != "LYG-下-T049":
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
