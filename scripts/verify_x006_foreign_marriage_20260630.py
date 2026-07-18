# -*- coding: utf-8 -*-
"""Verify LYG-下-T006 foreign marriage table from page-level OCR."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
DATA = ROOT / "workbench" / "table_entries" / "下" / "data" / "LYG-下-T006.json"

COLUMNS = [
    "年份",
    "中国公民小计(人)",
    "中国公民男(人)",
    "中国公民女(人)",
    "港澳同胞小计(人)",
    "港澳同胞男(人)",
    "港澳同胞女(人)",
    "外国籍小计(人)",
    "外国籍男(人)",
    "外国籍女(人)",
]

ROWS = [
    ["1985", "1", "", "1", "1", "", "1", "", "", ""],
    ["1987", "2", "", "2", "1", "", "1", "1", "", "1"],
    ["1988", "2", "", "2", "", "", "", "2", "2", ""],
    ["1989", "2", "1", "1", "1", "", "1", "1", "", "1"],
    ["1990", "5", "1", "4", "4", "", "4", "1", "1", ""],
    ["合计", "12", "2", "10", "7", "", "7", "5", "3", "2"],
]

PATCH = {
    "title": "1985~1990年连云港市涉外婚姻情况表",
    "table_number": "表43-11",
    "page": 2017,
    "pages": [2017],
    "part": "part01",
    "vol": "下",
    "volume": "下",
    "columns": COLUMNS,
    "rows": ROWS,
    "row_count": len(ROWS),
    "col_count": len(COLUMNS),
    "status": "verified",
    "notes": "已据页级OCR核录：workbench/ocr/paddle_ocr/下/part01/page_0046.txt，并参考 raw OCR：workbench/table_entries/下/raw/LYG-下-T006_2017.txt。单位为人；源页未见数值的性别栏保留空值；分组按中国公民小计=港澳同胞小计+外国籍小计及合计行校验。",
}


def patch_entry(entry: dict) -> bool:
    if entry.get("table_id") != "LYG-下-T006":
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
