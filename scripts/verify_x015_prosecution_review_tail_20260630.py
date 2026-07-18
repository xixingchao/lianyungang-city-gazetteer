# -*- coding: utf-8 -*-
"""Verify LYG-下-T015 prosecution review continuation table."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
DATA = ROOT / "workbench" / "table_entries" / "下" / "data" / "LYG-下-T015.json"

COLUMNS = ["年份", "受案(人)", "起诉(人)", "免诉(人)", "不诉(人)", "出庭公诉(次)"]

ROWS = [
    ["1962", "159", "156", "2", "", ""],
    ["1963", "151", "142", "1", "", "40"],
    ["1964", "94", "80", "4", "", ""],
    ["1965", "93", "80", "4", "", ""],
    ["1966", "17", "16", "1", "", ""],
    ["1979", "190", "170", "9", "1", "29"],
    ["1980", "273", "257", "15", "7", "58"],
    ["1981", "398", "373", "15", "2", "115"],
    ["1982", "353", "308", "11", "1", "121"],
    ["1983", "1931", "1850", "60", "3", "1656"],
    ["1984", "2092", "1821", "180", "21", "1705"],
    ["1985", "765", "684", "34", "4", "750"],
    ["1986", "650", "547", "32", "1", "457"],
    ["1987", "570", "535", "25", "2", "397"],
    ["1988", "816", "719", "29", "", "500"],
    ["1989", "1403", "1285", "111", "7", "711"],
    ["1990", "1631", "1490", "185", "", "785"],
]

PATCH = {
    "title": "1955~1990年全市检察受理审查起诉案件统计表（续表）",
    "table_number": "表44-10",
    "page": 2076,
    "pages": [2076],
    "part": "part01",
    "vol": "下",
    "volume": "下",
    "columns": COLUMNS,
    "rows": ROWS,
    "row_count": len(ROWS),
    "col_count": len(COLUMNS),
    "status": "verified",
    "notes": "已据页级OCR核录续页：workbench/ocr/paddle_ocr/下/part01/page_0105.txt；表题和表号据前页 workbench/ocr/paddle_ocr/下/part01/page_0104.txt。参考 raw OCR：workbench/table_entries/下/raw/LYG-下-T015_2076.txt。本条仅录入续页1962-1990年，源页未见数值的单元格保留空值；页级OCR将1988年识别为1968，本次按表序及raw续表上下文校正为1988。",
}


def patch_entry(entry: dict) -> bool:
    if entry.get("table_id") != "LYG-下-T015":
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
