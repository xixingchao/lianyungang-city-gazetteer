# -*- coding: utf-8 -*-
"""Verify rural grain three-fixed household table from page OCR."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
DATA_DIR = ROOT / "workbench" / "table_entries" / "中" / "data"

PATCHES = {
    "LYG-中-T094": {
        "title": "1955~1956年度连云港市农村粮食“三定”到户情况统计表",
        "table_number": "表36-2",
        "page": 1635,
        "pages": [1635],
        "columns": [
            "地区",
            "户数(户)",
            "在家人口(人)",
            "粮田面积(亩)",
            "常年产量(吨)",
            "全年必需用粮合计(吨)",
            "全年必需用粮口粮(吨)",
            "全年必需用粮种子(吨)",
            "全年必需用粮饲料(吨)",
            "应交农业税粮(吨)",
            "统购余粮(吨)",
            "缺粮供应(吨)",
        ],
        "rows": [
            ["合计", "370929", "1643642", "5979795", "487890", "371805", "307385", "45850", "18570", "50375", "83765", "24750"],
            ["市区", "11535", "55012", "124432", "10095", "12240", "10735", "1075", "430", "635", "680", "4150"],
            ["赣榆县", "114234", "499477", "1157381", "119365", "105985", "93165", "8275", "4545", "12390", "11225", "8090"],
            ["东海县", "119227", "499119", "2188236", "144880", "113150", "91940", "14650", "6560", "19760", "16710", "6905"],
            ["灌云县", "125933", "590034", "2509746", "213550", "140430", "111545", "21850", "7035", "17590", "55150", "5605"],
        ],
        "status": "verified",
        "notes": "已据页级OCR回源核录：workbench/ocr/paddle_ocr/中/part02/page_0215.txt。复合表头展开为地区、户数、在家人口、粮田面积、常年产量、全年必需用粮分项、应交农业税粮、统购余粮、缺粮供应。",
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
