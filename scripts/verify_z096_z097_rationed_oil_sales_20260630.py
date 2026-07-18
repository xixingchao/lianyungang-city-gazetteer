# -*- coding: utf-8 -*-
"""Verify rationed edible oil sales table from page OCR."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
DATA_DIR = ROOT / "workbench" / "table_entries" / "中" / "data"

COLUMNS = ["年份", "合计", "市区", "赣榆县", "东海县", "灌云县"]

PATCHES = {
    "LYG-中-T096": {
        "title": "1957~1990年连云港市市镇定量食油销售统计表",
        "table_number": "表36-6",
        "page": 1641,
        "pages": [1641],
        "columns": COLUMNS,
        "rows": [
            ["1957", "969", "667", "91", "82", "129"],
            ["1958", "800", "483", "110", "67", "140"],
            ["1959", "846", "454", "155", "102", "135"],
            ["1960", "679", "401", "77", "66", "135"],
            ["1961", "522", "238", "75", "85", "124"],
            ["1962", "396", "244", "36", "30", "86"],
            ["1963", "368", "243", "38", "24", "63"],
            ["1964", "665", "455", "70", "35", "105"],
            ["1965", "940", "620", "98", "62", "160"],
            ["1966", "935", "610", "85", "50", "190"],
            ["1967", "995", "625", "115", "50", "205"],
        ],
        "status": "verified",
        "notes": "已据页级OCR回源核录：workbench/ocr/paddle_ocr/中/part02/page_0221.txt。单位为吨；页首含上一表续表残段，本轮仅录入表36-6首页。",
    },
    "LYG-中-T097": {
        "title": "1957~1990年连云港市市镇定量食油销售统计表（续表）",
        "table_number": "表36-6",
        "page": 1642,
        "pages": [1642],
        "columns": COLUMNS,
        "rows": [
            ["1968", "1100", "700", "120", "55", "225"],
            ["1969", "1180", "760", "115", "65", "240"],
            ["1970", "1124", "645", "144", "60", "275"],
            ["1971", "1014", "645", "114", "60", "195"],
            ["1972", "988", "643", "108", "57", "180"],
            ["1973", "997", "640", "96", "73", "188"],
            ["1974", "1081", "753", "86", "69", "173"],
            ["1975", "1043", "729", "93", "67", "154"],
            ["1976", "1037", "711", "101", "69", "156"],
            ["1977", "1036", "712", "89", "63", "172"],
            ["1978", "1087", "766", "95", "62", "164"],
            ["1979", "1182", "822", "96", "77", "187"],
            ["1980", "1261", "888", "115", "75", "183"],
            ["1981", "1433", "969", "119", "103", "242"],
            ["1982", "2139", "1417", "188", "177", "357"],
            ["1983", "1793", "1211", "149", "144", "289"],
            ["1984", "1753", "1242", "161", "123", "227"],
            ["1985", "1790", "1296", "145", "112", "237"],
            ["1986", "1534", "997", "144", "119", "274"],
            ["1987", "1730", "1159", "166", "131", "274"],
            ["1988", "1947", "1318", "183", "150", "296"],
            ["1989", "1766", "1147", "179", "165", "275"],
            ["1990", "2355", "1515", "235", "237", "368"],
        ],
        "status": "verified",
        "notes": "已据页级OCR回源核录：workbench/ocr/paddle_ocr/中/part02/page_0222.txt。单位为吨；本页为表36-6续表尾段。1971年灌云县列 OCR 作“195.”，按表内整数口径录为195。",
    },
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
