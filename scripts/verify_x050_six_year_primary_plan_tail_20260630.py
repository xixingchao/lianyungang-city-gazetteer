# -*- coding: utf-8 -*-
"""Verify LYG-下-T050 six-year primary school teaching plan continuation page."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
DATA = ROOT / "workbench" / "table_entries" / "下" / "data" / "LYG-下-T050.json"

COLUMNS = [
    "活动类别",
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
    ["课外活动", "自习", "3", "3", "3", "3", "", "", "", "每天20分钟"],
    ["课外活动", "科技文娱活动", "2", "2", "2", "2", "2", "2", "", ""],
    ["课外活动", "体育活动", "2", "2", "2", "2", "2", "2", "", ""],
    ["课外活动", "周会、班队活动", "1", "1", "1", "1", "1", "1", "", ""],
    ["课外活动", "早操(课间操)", "3", "3", "3", "3", "3", "3", "", "每天20分钟"],
    ["课外活动", "眼保健操", "1.5", "1.5", "1.5", "1.5", "1.5", "1.5", "", "每天两次共10分钟"],
    ["课外活动", "晨会或夕会", "1.5", "1.5", "1.5", "1.5", "1.5", "1.5", "", "每天10分钟"],
    ["合计", "每周在校活动总量", "35", "35", "39", "39", "40", "40", "", ""],
]

PATCH = {
    "title": "1984年连云港市市区全日制六年制小学教学计划表（续表）",
    "table_number": "表50-6",
    "page": 2339,
    "pages": [2339],
    "part": "part01",
    "vol": "下",
    "volume": "下",
    "columns": COLUMNS,
    "rows": ROWS,
    "row_count": len(ROWS),
    "col_count": len(COLUMNS),
    "status": "verified",
    "notes": "已据页级OCR核录：workbench/ocr/paddle_ocr/下/part01/page_0368.txt；表题和表号依据前页 workbench/ocr/paddle_ocr/下/part01/page_0367.txt；并参考 raw OCR：workbench/table_entries/下/raw/LYG-下-T050_2339.txt。此页为表50-6末页续表，仅录入本页可见课外活动项目；自习五、六年级和上课总时数源页未见数值，保留空值。",
}


def patch_entry(entry: dict) -> bool:
    if entry.get("table_id") != "LYG-下-T050":
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
