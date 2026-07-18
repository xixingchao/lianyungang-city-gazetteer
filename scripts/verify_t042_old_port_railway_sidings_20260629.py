# -*- coding: utf-8 -*-
"""Verify LYG-中-T042 old port railway sidings table from page OCR."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
DATA = ROOT / "workbench" / "table_entries" / "中" / "data" / "LYG-中-T042.json"

COLUMNS = ["码头", "道别", "线长(米)", "建成时间"]
ROWS = [
    ["一码头", "7~10道", "1518", "7道1957年，8~10道1979年"],
    ["二码头", "11~17道", "2830", "15~17道1957年，11~13道1979年"],
    ["三码头", "15~22道", "4150", "21~22道1974年，15~20道1987年"],
]

PATCH = {
    "title": "1990年连云港老港区铁路专线分布表",
    "table_number": "表29-1",
    "page": 1348,
    "pages": [1348],
    "columns": COLUMNS,
    "rows": ROWS,
    "row_count": len(ROWS),
    "col_count": len(COLUMNS),
    "status": "verified",
    "notes": "已据页级OCR回源核录：workbench/ocr/paddle_ocr/中/part01/page_0445.txt；表号OCR作表29- 1，规范为表29-1。",
}


def patch_entry(entry: dict) -> bool:
    if entry.get("table_id") != "LYG-中-T042":
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
