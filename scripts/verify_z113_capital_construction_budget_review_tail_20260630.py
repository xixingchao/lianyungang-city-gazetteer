# -*- coding: utf-8 -*-
"""Verify capital construction budget review continuation table from page OCR."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
DATA_DIR = ROOT / "workbench" / "table_entries" / "中" / "data"

PATCHES = {
    "LYG-中-T113": {
        "title": "1980~1990年连云港市基建预(决)算审查统计表（续表）",
        "table_number": "表40-17",
        "page": 1812,
        "pages": [1812],
        "columns": [
            "年份",
            "本年度累计收到份数",
            "本年度累计收到价值(万元)",
            "本年度累计审查份数",
            "本年度累计审查价值(万元)",
            "本年度累计审查核减价值(万元)",
            "本年度累计审查核增价值(万元)",
            "本年度累计案定份数",
            "本年度累计案定价值(万元)",
            "本年度累计案定核增价值(万元)",
            "本年度累计案定核减价值(万元)",
        ],
        "rows": [
            ["1986", "475", "7523", "470", "7469", "942", "51", "473", "7469", "942", "51"],
            ["1987", "577", "10190", "577", "10490", "799", "75", "577", "10490", "799", "75"],
            ["1988", "700", "14970", "683", "14318", "1629", "85", "674", "14200", "1575", "85"],
            ["1989", "537", "13618", "522", "13173", "1570", "268", "518", "12616", "1570", "268"],
            ["1990", "552", "12639", "532", "11880", "1901", "253", "532", "10880", "1901", "253"],
        ],
        "status": "verified",
        "notes": "已据页级OCR回源核录：workbench/ocr/paddle_ocr/中/part02/page_0392.txt，并参考 raw OCR：workbench/table_entries/中/raw/LYG-中-T113_1812.txt。表题和表号依据前页 workbench/ocr/paddle_ocr/中/part02/page_0391.txt；本页为表40-17续表，单位为万元。1990年案定核增价值按页级OCR录为1901。",
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
