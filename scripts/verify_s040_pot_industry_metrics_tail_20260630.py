# -*- coding: utf-8 -*-
"""Verify table 14-5 pot industry metrics continuation."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
DATA_DIR = ROOT / "workbench" / "table_entries" / "上" / "data"

COLUMNS = ["年份", "职工(人)", "产量(万口)", "产值(万元)", "劳动生产率(元/人)"]

PATCHES = {
    "LYG-上-T040": {
        "title": "1969~1988年部分年份连云港市制锅业主要指标统计表（续表）",
        "table_number": "表14-5",
        "pages": [813],
        "columns": COLUMNS,
        "rows": [
            ["1983", "184", "34.00", "81.30", "4329"],
            ["1984", "205", "39.10", "86.90", "4882"],
            ["1985", "210", "42.80", "123.50", "6337"],
            ["1986", "208", "49.90", "161.50", "7864"],
            ["1987", "195", "46.60", "117.40", "5870"],
            ["1988", "190", "41.10", "120.30", "6266"],
        ],
        "status": "verified",
        "notes": "已据页级OCR回源核录：workbench/ocr/paddle_ocr/上/part03/page_0208.txt，并参考 raw OCR：workbench/table_entries/上/raw/LYG-上-T040_813.txt。表题、表号和单位依据前页 workbench/ocr/paddle_ocr/上/part03/page_0207.txt；本页为表14-5续上表。原JSON列序误置为年份、产量、产值、职工、劳动生产率，本轮按源页列序重录为年份、职工、产量、产值、劳动生产率。",
    }
}

for patch in PATCHES.values():
    patch["row_count"] = len(patch["rows"])
    patch["col_count"] = len(patch["columns"])


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
