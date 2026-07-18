# -*- coding: utf-8 -*-
"""Verify budgetary state-owned enterprise income table from page OCR."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
DATA_DIR = ROOT / "workbench" / "table_entries" / "中" / "data"

PATCHES = {
    "LYG-中-T105": {
        "title": "1952~1990年连云港市预算内全民企业收入统计表",
        "table_number": "表38-4",
        "page": 1711,
        "pages": [1711],
        "columns": ["年份", "企业收入(万元)"],
        "rows": [
            ["1952", "3"],
            ["1953", "85"],
            ["1954", "90"],
            ["1955", "153"],
            ["1956", "80"],
            ["1957", "88"],
            ["1958", "1861"],
            ["1959", "1989"],
            ["1960", "1741"],
            ["1961", "1061"],
            ["1962", "397"],
            ["1963", "594"],
            ["1964", "377"],
            ["1965", "552"],
            ["1966", "406"],
            ["1967", "209"],
            ["1968", "-183"],
            ["1969", "-1006"],
            ["1970", "423"],
            ["1971", "1056"],
            ["1972", "1502"],
            ["1973", "1812"],
            ["1974", "180"],
            ["1975", "348"],
            ["1976", "-54"],
            ["1977", "768"],
            ["1978", "1953"],
            ["1979", "1289"],
            ["1980", "1528"],
            ["1981", "1211"],
            ["1982", "1533"],
            ["1983", "1293"],
            ["1984", "815"],
            ["1985", "1045"],
            ["1986", "1480"],
            ["1987", "1447"],
            ["1988", "1185"],
            ["1989", "-1366"],
            ["1990", "-1496"],
        ],
        "status": "verified",
        "notes": "已据页级OCR回源核录：workbench/ocr/paddle_ocr/中/part02/page_0291.txt。单位为万元；原三组横排展开为年份、企业收入两列，负数按源保留。",
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
