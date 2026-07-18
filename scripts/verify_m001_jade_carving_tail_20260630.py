# -*- coding: utf-8 -*-
"""Verify jade carving production/business statistics continuation."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
DATA_DIR = ROOT / "workbench" / "table_entries" / "中" / "data"

PATCHES = {
    "LYG-中-T001": {
        "title": "1981~1990年连云港市玉雕工艺品生产经营情况表（续表）",
        "table_number": "表17-1",
        "page": 925,
        "pages": [925],
        "part": "part01",
        "vol": "中",
        "volume": "中",
        "columns": ["年份", "产量(万件)", "产值(万元)", "销售(万元)", "利税总额(万元)", "利润(万元)"],
        "rows": [
            ["1989", "0.21", "20.50", "8.13", "-0.30", "-1.20"],
            ["1990", "0.07", "23.85", "12.90", "-2.30", "-2.60"],
        ],
        "row_count": 2,
        "col_count": 6,
        "status": "verified",
        "notes": "已据页级OCR回源核录：workbench/ocr/paddle_ocr/中/part01/page_0022.txt，并参考 raw OCR：workbench/table_entries/中/raw/LYG-中-T001_925.txt。表题、表号和列组据前页表头 workbench/ocr/paddle_ocr/中/part01/page_0021.txt 补定。本页为续上表，仅录入源页可见的1989、1990两行；负数按源页录入。",
    }
}


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
