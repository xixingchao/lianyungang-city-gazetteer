# -*- coding: utf-8 -*-
"""Verify LYG-下-T010 criminal case detection continuation table."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
DATA = ROOT / "workbench" / "table_entries" / "下" / "data" / "LYG-下-T010.json"

COLUMNS = [
    "年份",
    "全部案件发案数(件)",
    "全部案件破案数(件)",
    "全部案件破案率(%)",
    "其中重大案件发案数(件)",
    "其中重大案件破案数(件)",
    "其中重大案件破案率(%)",
]

ROWS = [
    ["1986", "596", "499", "83.70", "9", "9", "100.00"],
    ["1987", "711", "604", "84.95", "8", "7", "87.50"],
    ["1988", "905", "750", "82.90", "21", "16", "76.19"],
    ["1989", "1779", "1247", "70.10", "41", "34", "82.92"],
    ["1990", "3557", "1870", "52.60", "53", "38", "71.69"],
]

PATCH = {
    "title": "1956~1990年连云港市刑事案件侦破统计表（续表）",
    "table_number": "表44-3",
    "page": 2048,
    "pages": [2048],
    "part": "part01",
    "vol": "下",
    "volume": "下",
    "columns": COLUMNS,
    "rows": ROWS,
    "row_count": len(ROWS),
    "col_count": len(COLUMNS),
    "status": "verified",
    "notes": "已据页级OCR核录续页：workbench/ocr/paddle_ocr/下/part01/page_0077.txt；表题、表号、单位据前页 workbench/ocr/paddle_ocr/下/part01/page_0076.txt。参考 raw OCR：workbench/table_entries/下/raw/LYG-下-T010_2048.txt。本条仅录入续页1986-1990年；源注为1983-1990年含东海县、赣榆县、灌云县刑事案件侦破数。",
}


def patch_entry(entry: dict) -> bool:
    if entry.get("table_id") != "LYG-下-T010":
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
