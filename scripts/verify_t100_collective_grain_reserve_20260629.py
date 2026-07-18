# -*- coding: utf-8 -*-
"""Verify LYG-中-T100 rural collective grain reserve table from raw OCR."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
DATA = ROOT / "workbench" / "table_entries" / "中" / "data" / "LYG-中-T100.json"

COLUMNS = ["年份", "合计(吨)", "市区(吨)", "赣榆县(吨)", "灌云县(吨)", "东海县(吨)"]
ROWS = [
    ["1966", "9040", "1150", "1075", "135", "6680"],
    ["1967", "7155", "875", "950", "105", "5225"],
    ["1968", "10815", "915", "855", "175", "8870"],
    ["1969", "8520", "825", "790", "", "6905"],
    ["1970", "2780", "725", "695", "", "1360"],
    ["1971", "5550", "525", "575", "655", "3795"],
    ["1972", "9320", "725", "1540", "1015", "6040"],
    ["1973", "31305", "1130", "10330", "15630", "4215"],
    ["1974", "27740", "1325", "6995", "18725", "695"],
    ["1975", "50120", "1480", "18920", "28645", "1075"],
    ["1976", "48100", "2235", "11135", "33020", "1710"],
    ["1977", "49570", "2450", "35400", "11055", "665"],
    ["1978", "53330", "3260", "12025", "37240", "805"],
    ["1979", "57535", "3395", "11330", "37100", "5710"],
    ["1980", "57645", "3575", "10595", "37620", "5855"],
    ["1981", "55800", "3470", "9985", "36920", "5425"],
    ["1982", "56080", "4080", "10595", "4520", "36885"],
    ["1983", "61140", "4290", "9720", "36820", "10310"],
]

PATCH = {
    "title": "1966~1983年连云港市农村集体储备粮统计表",
    "table_number": "表36-13",
    "page": 1660,
    "pages": [1660],
    "columns": COLUMNS,
    "rows": ROWS,
    "row_count": len(ROWS),
    "col_count": len(COLUMNS),
    "status": "verified",
    "notes": "已据raw OCR回源核录：workbench/table_entries/中/raw/LYG-中-T100_1660.txt；1969、1970年灌云县栏OCR未见数字，保留空值。",
}


def patch_entry(entry: dict) -> bool:
    if entry.get("table_id") != "LYG-中-T100":
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
