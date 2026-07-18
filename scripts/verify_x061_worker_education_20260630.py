# -*- coding: utf-8 -*-
"""Verify LYG-下-T061 worker education basic situation table."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
DATA = ROOT / "workbench" / "table_entries" / "下" / "data" / "LYG-下-T061.json"

COLUMNS = [
    "类别",
    "学校类型",
    "学校数(所)",
    "教学班(个)",
    "在校学生数全脱产(人)",
    "在校学生数业余函授(人)",
    "教职工数专任教师(人)",
    "教职工数兼任教师数(人)",
]

ROWS = [
    ["成人中等专业技术学校", "广播电视中专班", "", "8", "", "", "", ""],
    ["成人中等专业技术学校", "职工中专校", "6", "", "639", "", "112", "34"],
    ["成人中等专业技术学校", "干部中专校", "1", "", "79", "", "14", ""],
    ["成人中等专业技术学校", "教师进修学校", "4", "", "4583", "", "76", ""],
    ["成人中等专业技术学校", "职工中学", "17", "52", "195", "2235", "52", "79"],
    ["成人中等专业技术学校", "职工技术培训学校", "51", "357", "2904", "14195", "115", "328"],
]

PATCH = {
    "title": "1990年连云港市职工教育基本情况表",
    "table_number": "表50-19",
    "page": 2369,
    "pages": [2369],
    "part": "part01",
    "vol": "下",
    "volume": "下",
    "columns": COLUMNS,
    "rows": ROWS,
    "row_count": len(ROWS),
    "col_count": len(COLUMNS),
    "status": "verified",
    "notes": "已据页级OCR核录：workbench/ocr/paddle_ocr/下/part01/page_0398.txt，并参考 raw OCR：workbench/table_entries/下/raw/LYG-下-T061_2369.txt。源页左侧成人中等专业技术学校为跨行类目，本轮向下展开；源页未见数值的单元格保留空值。",
}


def patch_entry(entry: dict) -> bool:
    if entry.get("table_id") != "LYG-下-T061":
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
