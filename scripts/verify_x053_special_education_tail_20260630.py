# -*- coding: utf-8 -*-
"""Verify LYG-下-T053 special education class list continuation page."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
DATA = ROOT / "workbench" / "table_entries" / "下" / "data" / "LYG-下-T053.json"

COLUMNS = ["隶属", "学校名称", "班级(个)", "人数(人)"]

ROWS = [
    ["赣榆县", "石桥小学培智班", "1", "14"],
    ["赣榆县", "海头小学培智班", "1", "14"],
    ["东海县", "工农兵小学培智班", "2", "12"],
    ["东海县", "新建小学培智班", "1", "8"],
    ["灌云县", "繁荣小学培智班", "1", "6"],
    ["灌云县", "陡沟小学培智班", "1", "8"],
    ["合计", "", "15", "209"],
]

PATCH = {
    "title": "1990年连云港市培智学校(班)一览表（续表）",
    "table_number": "表50-10",
    "page": 2345,
    "pages": [2345],
    "part": "part01",
    "vol": "下",
    "volume": "下",
    "columns": COLUMNS,
    "rows": ROWS,
    "row_count": len(ROWS),
    "col_count": len(COLUMNS),
    "status": "verified",
    "notes": "已据页级OCR核录：workbench/ocr/paddle_ocr/下/part01/page_0374.txt；表题和表号依据前页 workbench/ocr/paddle_ocr/下/part01/page_0373.txt；并参考 raw OCR：workbench/table_entries/下/raw/LYG-下-T053_2345.txt。原条目题名串章为外轮服务公司表，本次更正为教育章表50-10续页；正文叙述在校学生为211人，但表内合计行为209，本条按表内合计照录。",
}


def patch_entry(entry: dict) -> bool:
    if entry.get("table_id") != "LYG-下-T053":
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
