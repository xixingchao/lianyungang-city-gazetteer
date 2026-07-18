# -*- coding: utf-8 -*-
"""Verify LYG-下-T017 economic second-instance continuation table."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
DATA = ROOT / "workbench" / "table_entries" / "下" / "data" / "LYG-下-T017.json"

COLUMNS = [
    "年份",
    "旧存(件)",
    "新收(件)",
    "已结(件)",
    "发回重审(件)",
    "未结(件)",
    "维持(件)",
    "改判(件)",
    "撤诉(件)",
    "其他(件)",
]

ROWS = [
    ["1987", "2", "29", "28", "9", "6", "3", "2", "8", "3"],
    ["1988", "3", "62", "55", "19", "12", "8", "1", "15", "10"],
    ["1989", "10", "75", "81", "36", "13", "10", "22", "4", ""],
    ["1990", "4", "89", "87", "35", "36", "7", "2", "7", "6"],
    ["合计", "", "283", "277", "262", "105", "69", "29", "54", "23"],
]

PATCH = {
    "title": "1985~1990年连云港市中级法院审结经济二审案件统计表（续表）",
    "table_number": "表44-35",
    "page": 2107,
    "pages": [2107],
    "part": "part01",
    "vol": "下",
    "volume": "下",
    "columns": COLUMNS,
    "rows": ROWS,
    "row_count": len(ROWS),
    "col_count": len(COLUMNS),
    "status": "verified",
    "notes": "已据页级OCR核录续页：workbench/ocr/paddle_ocr/下/part01/page_0136.txt；表题、表号、单位据前页 workbench/ocr/paddle_ocr/下/part01/page_0135.txt。参考 raw OCR：workbench/table_entries/下/raw/LYG-下-T017_2107.txt。本条仅录入续页1987-1990年及合计；源页未见数值的单元格保留空值；源注为1985年之前未受理经济二审案件。",
}


def patch_entry(entry: dict) -> bool:
    if entry.get("table_id") != "LYG-下-T017":
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
