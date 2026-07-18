# -*- coding: utf-8 -*-
"""Verify Huaibei salt field tax/profit continuation table T038."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
DATA = ROOT / "workbench" / "table_entries" / "上" / "data" / "LYG-上-T038.json"

COLUMNS = ["年份", "税收(万元)", "利润(万元)"]

ROWS = [
    ["1967", "9413", "795.94"],
    ["1968", "7673", "718.29"],
    ["1969", "11720", "386.57"],
    ["1970", "16454", "-211.63"],
    ["1971", "14891", "345.59"],
    ["1972", "15070", "585.59"],
    ["1973", "8621", "1.17"],
    ["1974", "12229", "330.89"],
    ["1975", "13460", "555.53"],
    ["1976", "13592", "64.90"],
    ["1977", "14982", "516.10"],
    ["1978", "13357", "1184.96"],
    ["1979", "14468", "1041.21"],
    ["1980", "13640", "606.73"],
    ["1981", "10717", "51.92"],
    ["1982", "11459", "106.25"],
    ["1983", "12333", "305.06"],
    ["1984", "11790", "436.43"],
    ["1985", "13196", "649.96"],
    ["1986", "12246", "894.42"],
    ["1987", "11448", "1478.67"],
    ["1988", "8660", "2080.35"],
    ["1989", "8802", "957.70"],
    ["1990", "6317", "-575.70"],
]

PATCH = {
    "table_id": "LYG-上-T038",
    "title": "1949~1990年淮北盐场盐税收入利润统计表（续表）",
    "table_number": "表13-17",
    "page": 774,
    "pages": [774],
    "part": "part03",
    "vol": "上",
    "volume": "上",
    "columns": COLUMNS,
    "rows": ROWS,
    "row_count": len(ROWS),
    "col_count": len(COLUMNS),
    "status": "verified",
    "notes": "已据页级OCR回源核录：表题、表号、单位和首页数据见 workbench/ocr/paddle_ocr/上/part03/page_0168.txt；本条续表内容见 workbench/ocr/paddle_ocr/上/part03/page_0169.txt，并参考 raw OCR workbench/table_entries/上/raw/LYG-上-T038_774.txt。原JSON串入其他行业年度统计表；本次仅录入续页可见的 1967~1990 年数据。",
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
