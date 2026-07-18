# -*- coding: utf-8 -*-
"""Verify staff wage statistics continuation page X040."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
DATA_DIR = ROOT / "workbench" / "table_entries" / "下" / "data"

PATCH = {
    "table_id": "LYG-下-T040",
    "title": "1949~1990年连云港市职工人数、工资总额、年平均工资统计表（续表）",
    "table_number": "表47-11",
    "page": 2243,
    "pages": [2243],
    "part": "part01",
    "vol": "下",
    "volume": "下",
    "columns": ["年份", "职工人数(万人)", "工资总额(万元)", "职工年平均工资(元)"],
    "rows": [
        ["1982", "30.79", "19749", "655"],
        ["1983", "30.94", "21414", "691"],
        ["1984", "32.02", "27385", "873"],
        ["1985", "33.52", "34873", "1064"],
        ["1986", "34.90", "41187", "1215"],
        ["1987", "36.43", "46746", "1323"],
        ["1988", "37.12", "57231", "1573"],
        ["1989", "37.74", "61579", "1650"],
        ["1990", "38.57", "70471", "1864"],
    ],
    "status": "verified",
    "notes": "已据页级OCR回源核录：workbench/ocr/paddle_ocr/下/part01/page_0272.txt。表题、表号和列组依据前页 workbench/ocr/paddle_ocr/下/part01/page_0271.txt；原JSON为单列骨架且未给出有效表题。raw OCR中1983年年平均工资误读为169，页级OCR清楚为691，按页级OCR录入。",
}
PATCH["row_count"] = len(PATCH["rows"])
PATCH["col_count"] = len(PATCH["columns"])


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
    path = DATA_DIR / f"{PATCH['table_id']}.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    if not patch_entry(data):
        return 0
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return 1


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
