# -*- coding: utf-8 -*-
"""Verify LYG-中-T032 survey/design units table from page OCR."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
DATA = ROOT / "workbench" / "table_entries" / "中" / "data" / "LYG-中-T032.json"

COLUMNS = ["单位", "技术人员(人)", "非技术人员(人)", "资质等级", "成立年月"]
ROWS = [
    ["化工部连云港化工矿山设计院", "742", "457", "甲级", "1961.3"],
    ["锦屏磷矿勘察室", "31", "18", "乙级", "1956"],
    ["灌云县建筑设计室", "11", "", "乙级", "1977"],
    ["市建筑设计院", "107", "40", "乙级", "1978.12"],
    ["市市政规划设计院", "38", "13", "乙级", "1985.12"],
    ["市住宅设计室", "46", "6", "丙级", "1982"],
    ["连云港化建公司化工设计所", "30", "", "丙级", "1984"],
    ["市建设开发公司设计室", "39", "3", "丙级", "1987"],
    ["赣榆县建筑设计室", "14", "", "丁级", "1979.9"],
    ["东海县建筑设计室", "19", "2", "丁级", "1981.5"],
]

PATCH = {
    "title": "1990年连云港市主要勘察设计单位一览表",
    "table_number": "表24-2",
    "page": 1204,
    "pages": [1204],
    "columns": COLUMNS,
    "rows": ROWS,
    "row_count": len(ROWS),
    "col_count": len(COLUMNS),
    "status": "verified",
    "notes": "已据页级OCR回源核录：workbench/ocr/paddle_ocr/中/part01/page_0301.txt；灌云县建筑设计室、连云港化建公司化工设计所、赣榆县建筑设计室的非技术人员栏OCR未见数字，保留空值。",
}


def patch_entry(entry: dict) -> bool:
    if entry.get("table_id") != "LYG-中-T032":
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
