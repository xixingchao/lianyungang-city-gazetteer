# -*- coding: utf-8 -*-
"""Verify non-party people arrangement table T128."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
DATA = ROOT / "workbench" / "table_entries" / "中" / "data" / "LYG-中-T128.json"

COLUMNS = [
    "届次",
    "人大代表总数",
    "人大代表党外",
    "人大代表比例",
    "人大常委会总数",
    "人大常委会党外",
    "人大常委会比例",
    "市长副市长总数",
    "市长副市长党外",
    "市长副市长比例",
]

ROWS = [
    ["第一届(1954.6~1957.1)", "", "", "", "", "", "", "8", "1", "12.5%"],
    ["第二届(1957.1~1958.5)", "", "", "", "", "", "", "8", "1", "12.5%"],
    ["第三届(1958.5~1961.9)", "", "", "", "", "", "", "6", "1", "16.7%"],
    ["第四届(1961.9~1963.12)", "", "", "", "", "", "", "", "", ""],
    ["第五届(1963.12~1966.12)", "", "", "", "", "", "", "172", "49", "8.5%"],
    ["第六届(1980.2~1983.4)", "", "", "", "", "", "", "9", "1", "11.1%"],
    ["第七届(1983.4~1988.1)", "580", "194", "33.4%", "35", "4", "11.4%", "8", "2", "25.0%"],
    ["第八届(1988.1~)", "460", "99", "21.5%", "35", "4", "11.4%", "4", "1", "25.0%"],
]

PATCH = {
    "table_id": "LYG-中-T128",
    "title": "连云港市历届人民代表大会党外人士安排情况表",
    "table_number": "表41-16",
    "page": 1875,
    "pages": [1875],
    "part": "part02",
    "vol": "中",
    "volume": "中",
    "columns": COLUMNS,
    "rows": ROWS,
    "row_count": len(ROWS),
    "col_count": len(COLUMNS),
    "status": "verified",
    "notes": "已据页级OCR回源核录：workbench/ocr/paddle_ocr/中/part02/page_0455.txt，并参考 raw OCR workbench/table_entries/中/raw/LYG-中-T128_1875.txt。原JSON为单列骨架；源页未见数值的单元格保留空值，未按比例反推。",
}


def patch_entry(entry: dict) -> bool:
    if entry.get("table_id") != PATCH["table_id"]:
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
    changed = sum(1 for table in tables if patch_entry(table))
    if changed:
        text = text[: match.start(1)] + json.dumps(tables, ensure_ascii=False) + text[match.end(1) :]
        SITE.write_text(text, encoding="utf-8")
    return changed


def main() -> None:
    print(f"json_files_changed={patch_json()}")
    print(f"site_entries_changed={patch_site()}")


if __name__ == "__main__":
    main()
