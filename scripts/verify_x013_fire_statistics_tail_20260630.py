# -*- coding: utf-8 -*-
"""Verify LYG-下-T013 fire statistics continuation page."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
DATA = ROOT / "workbench" / "table_entries" / "下" / "data" / "LYG-下-T013.json"

COLUMNS = ["年份", "火灾起数(起)", "死亡(人)", "受伤(人)", "损失折款(元)"]

ROWS = [
    ["1973", "25", "4", "8", "88820"],
    ["1974", "27", "27", "", "43960"],
    ["1975", "21", "21", "2", "221878"],
    ["1976", "29", "29", "7", "52866"],
    ["1977", "17", "17", "2", "86812"],
    ["1978", "19", "19", "2", "26560"],
    ["1979", "20", "20", "16", "76665"],
    ["1980", "35", "35", "", "63119"],
    ["1981", "17", "17", "6", "79529"],
    ["1982", "13", "13", "", "8056"],
    ["1983", "56", "56", "2", "116588"],
    ["1984", "41", "41", "1", "136588"],
    ["1985", "53", "53", "15", "464952"],
    ["1986", "69", "69", "8", "803295"],
    ["1987", "64", "64", "6", "185679"],
    ["1988", "69", "69", "4", "656930"],
    ["1989", "45", "45", "8", "331610"],
    ["1990", "114", "114", "", "270260"],
]

PATCH = {
    "title": "1954~1990年连云港市火灾情况统计表（续表）",
    "table_number": "表44-6",
    "page": 2066,
    "pages": [2066],
    "part": "part01",
    "vol": "下",
    "volume": "下",
    "columns": COLUMNS,
    "rows": ROWS,
    "row_count": len(ROWS),
    "col_count": len(COLUMNS),
    "status": "verified",
    "notes": "已据页级OCR核录：workbench/ocr/paddle_ocr/下/part01/page_0095.txt；表题和表号依据前页 workbench/ocr/paddle_ocr/下/part01/page_0094.txt；并参考 raw 坐标 OCR：workbench/ocr/raw/下/part01/page_0095.json 与 raw 文本 workbench/table_entries/下/raw/LYG-下-T013_2066.txt。此页仅录入表44-6续页 1973-1990 年记录，数值按页级 OCR 与坐标 OCR 列位核录。",
}


def patch_entry(entry: dict) -> bool:
    if entry.get("table_id") != "LYG-下-T013":
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
