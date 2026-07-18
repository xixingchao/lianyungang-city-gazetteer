# -*- coding: utf-8 -*-
"""Verify LYG-中-T051 bank account settlement table from page OCR."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
DATA = ROOT / "workbench" / "table_entries" / "中" / "data" / "LYG-中-T051.json"

COLUMNS = ["年份", "笔数", "金额(万美元)", "备注"]
ROWS = [
    ["1979", "47", "", "1979~1984年因资料原因无金额统计"],
    ["1980", "67", "", "1979~1984年因资料原因无金额统计"],
    ["1981", "25", "", "1979~1984年因资料原因无金额统计"],
    ["1982", "21", "", "1979~1984年因资料原因无金额统计"],
    ["1983", "51", "", "1979~1984年因资料原因无金额统计"],
    ["1984", "59", "", "1979~1984年因资料原因无金额统计"],
    ["1985", "59", "", "页级OCR未见金额数字"],
    ["1986", "138", "", "页级OCR未见金额数字"],
    ["1987", "", "", "无资料"],
    ["1988", "221", "1501", ""],
    ["1989", "209", "1392", ""],
    ["1990", "256", "1087", ""],
]

PATCH = {
    "title": "1979~1990年中国银行连云港分行记帐结算统计表",
    "table_number": "表29-21",
    "page": 1385,
    "pages": [1385],
    "columns": COLUMNS,
    "rows": ROWS,
    "row_count": len(ROWS),
    "col_count": len(COLUMNS),
    "status": "verified",
    "notes": "已据页级OCR回源核录：workbench/ocr/paddle_ocr/中/part01/page_0482.txt；1985、1986金额栏OCR未见数字，保留空值。",
}


def patch_entry(entry: dict) -> bool:
    if entry.get("table_id") != "LYG-中-T051":
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
