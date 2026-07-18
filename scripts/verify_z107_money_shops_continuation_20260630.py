# -*- coding: utf-8 -*-
"""Verify money shops continuation table from page OCR."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
DATA_DIR = ROOT / "workbench" / "table_entries" / "中" / "data"

PATCHES = {
    "LYG-中-T107": {
        "title": "民国时期连云港市钱庄概况表（续表）",
        "table_number": "表40-1",
        "page": 1765,
        "pages": [1765],
        "columns": ["钱庄名称", "开办年份(民国)", "停业年份(民国)", "地址"],
        "rows": [
            ["盛康", "19", "22", ""],
            ["升泰", "19", "23", "板浦"],
            ["谦益", "19", "24", "板浦"],
            ["厚康", "20", "27", ""],
            ["同和公", "20", "23", ""],
            ["源润", "20", "23", ""],
            ["联丰", "20", "23", ""],
            ["源泰", "20", "23", "板浦"],
            ["同德昌", "20", "22", "板浦"],
            ["新生永", "21", "23", ""],
            ["袁怡和", "24", "", "板浦"],
            ["震余", "21", "", "板浦"],
            ["元泰", "21", "", ""],
        ],
        "status": "verified",
        "notes": "已据页级OCR回源核录：workbench/ocr/paddle_ocr/中/part02/page_0345.txt，并参考 raw OCR：workbench/table_entries/中/raw/LYG-中-T107_1765.txt。该页为表40-1续表；源页未列地址或停业年份的单元格保留空白。",
    }
}

for patch in PATCHES.values():
    patch["row_count"] = len(patch["rows"])
    patch["col_count"] = len(patch["columns"])


def patch_entry(entry: dict) -> bool:
    patch = PATCHES.get(entry.get("table_id"))
    if not patch:
        return False
    changed = False
    for key, value in patch.items():
        if entry.get(key) != value:
            entry[key] = value
            changed = True
    return changed


def patch_json() -> int:
    changed = 0
    for table_id in PATCHES:
        path = DATA_DIR / f"{table_id}.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        if patch_entry(data):
            path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            changed += 1
    return changed


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
