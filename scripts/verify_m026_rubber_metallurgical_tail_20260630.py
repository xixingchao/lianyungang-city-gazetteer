# -*- coding: utf-8 -*-
"""Verify rubber and chemical-metallurgical products output continuation."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
DATA_DIR = ROOT / "workbench" / "table_entries" / "中" / "data"

PATCHES = {
    "LYG-中-T026": {
        "title": "1966~1990年连云港市橡胶、化冶制品产量统计表（续表）",
        "table_number": "表20-14",
        "page": 1090,
        "pages": [1090],
        "part": "part01",
        "vol": "中",
        "volume": "中",
        "columns": [
            "年份",
            "轮胎翻新(条)",
            "轮胎修补(条)",
            "橡胶杂件(吨)",
            "橡胶丝(吨)",
            "炭素(万吨)",
            "炭砖(吨)",
            "电极(吨)",
            "捣料(吨)",
            "镍合金(吨)",
            "金属镁(吨)",
            "碳化硅产量(吨)",
            "碳化硅其中出口(吨)",
        ],
        "rows": [
            ["1988", "7562", "6953", "21", "302", "1.21", "2791", "89", "7", "32", "", "3470", "4308"],
            ["1989", "4727", "4449", "19", "380", "1.02", "2980", "84", "12", "", "", "2717", "3062"],
            ["1990", "6344", "6084", "24", "476", "0.81", "1445", "48", "", "", "", "3631", "3431"],
        ],
        "row_count": 3,
        "col_count": 13,
        "status": "verified",
        "notes": "已据页级OCR回源核录：workbench/ocr/paddle_ocr/中/part01/page_0187.txt，并参考 raw OCR：workbench/table_entries/中/raw/LYG-中-T026_1090.txt。表题、表号、单位和列组据前页 workbench/ocr/paddle_ocr/中/part01/page_0186.txt 补定。原JSON误沿用主要胶粘剂产量统计表题；本页为表20-14续上表。源页未见数值的单元格保留空值；1990年轮胎修补数按页级OCR核为6084。",
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
