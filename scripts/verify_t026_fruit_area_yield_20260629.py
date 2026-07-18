# -*- coding: utf-8 -*-
"""Verify LYG-上-T026 against page-level OCR and mark it deliverable."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
DATA = ROOT / "workbench" / "table_entries" / "上" / "data" / "LYG-上-T026.json"

ROWS = [
    ["1949", "2959", "730"],
    ["1957", "25359", "1664"],
    ["1960", "96312", "2652"],
    ["1966", "51436", "2521"],
    ["1970", "45941", "4085"],
    ["1976", "57366", "9048"],
    ["1978", "63516", "12653"],
    ["1982", "77441", "24129"],
    ["1985", "91966", "29908"],
    ["1986", "150336", "35612"],
    ["1987", "216405", "33327"],
    ["1988", "261437", "35028"],
    ["1989", "281356", "38495"],
    ["1990", "297246", "35149"],
]

PATCH = {
    "title": "1949~1990年部分年份连云港市果树面积、产量统计表",
    "table_number": "表9-5",
    "pages": [559],
    "columns": ["年份", "面积(亩)", "产量(吨)"],
    "rows": ROWS,
    "row_count": len(ROWS),
    "col_count": 3,
    "status": "verified",
    "notes": "已据页级OCR回源核录：上册part02/page_0259，对齐年份、面积、产量三行。",
}


def patch_entry(entry: dict) -> bool:
    if entry.get("table_id") != "LYG-上-T026":
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
