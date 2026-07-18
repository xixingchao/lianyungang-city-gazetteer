# -*- coding: utf-8 -*-
"""Verify LYG-中-T050 foreign currency deposit table from raw OCR."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
DATA = ROOT / "workbench" / "table_entries" / "中" / "data" / "LYG-中-T050.json"

COLUMNS = ["年份", "存款余额(万美元)"]
ROWS = [
    ["1984", "571.50"],
    ["1985", "802.80"],
    ["1986", "873.70"],
    ["1987", "1298.00"],
    ["1988", "1150.00"],
    ["1989", "1850.00"],
    ["1990", "2263.00"],
]

PATCH = {
    "title": "1984~1990年中国银行连云港分行企业外币存款余额统计表",
    "table_number": "表29-17",
    "page": 1383,
    "pages": [1383],
    "columns": COLUMNS,
    "rows": ROWS,
    "row_count": len(ROWS),
    "col_count": len(COLUMNS),
    "status": "verified",
    "notes": "已据raw OCR回源核录：workbench/table_entries/中/raw/LYG-中-T050_1383.txt。",
}


def patch_entry(entry: dict) -> bool:
    if entry.get("table_id") != "LYG-中-T050":
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
