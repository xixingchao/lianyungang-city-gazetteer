# -*- coding: utf-8 -*-
"""Verify social retail sales table from page OCR."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
DATA_DIR = ROOT / "workbench" / "table_entries" / "中" / "data"

COLUMNS = ["年份", "社会商品零售额", "居民", "农业生产资料", "社会集团"]

PATCHES = {
    "LYG-中-T072": {
        "title": "1949~1990年连云港市社会商品零售额统计表",
        "table_number": "表33-5",
        "page": 1551,
        "pages": [1551],
        "columns": COLUMNS,
        "rows": [
            ["1949", "3187", "2461", "378", "348"],
            ["1950", "3548", "2610", "497", "441"],
            ["1951", "3940", "3006", "463", "471"],
            ["1952", "4570", "3443", "541", "586"],
            ["1953", "5624", "4261", "669", "694"],
            ["1954", "7042", "5273", "760", "1009"],
            ["1955", "7432", "5521", "784", "1127"],
            ["1956", "8803", "6580", "957", "1266"],
            ["1957", "9647", "7180", "1105", "1362"],
            ["1958", "11207", "8165", "1298", "1744"],
            ["1959", "12488", "9191", "1449", "1848"],
            ["1960", "13425", "10293", "1137", "1995"],
            ["1961", "11078", "8551", "930", "1597"],
            ["1962", "11952", "9581", "788", "1583"],
            ["1963", "11924", "10064", "721", "1139"],
            ["1964", "12376", "10177", "862", "1337"],
        ],
        "status": "verified",
        "notes": "已据页级OCR回源核录：workbench/ocr/paddle_ocr/中/part02/page_0131.txt。单位为万元；页首含上一表续表残段，本轮仅录入表33-5首页。",
    },
    "LYG-中-T073": {
        "title": "1949~1990年连云港市社会商品零售额统计表（续表）",
        "table_number": "表33-5",
        "page": 1552,
        "pages": [1552],
        "columns": COLUMNS,
        "rows": [
            ["1965", "14425", "11511", "1053", "1861"],
            ["1966", "14882", "11805", "1149", "1928"],
            ["1967", "15029", "12103", "1120", "1806"],
            ["1968", "15538", "12524", "1149", "1865"],
            ["1969", "15919", "12545", "1181", "2193"],
            ["1970", "19236", "14991", "1858", "2387"],
            ["1971", "21740", "14362", "1908", "5470"],
            ["1972", "23809", "16895", "2178", "4736"],
            ["1973", "28274", "18794", "2272", "7208"],
            ["1974", "29450", "20518", "2592", "6340"],
            ["1975", "32151", "22554", "3187", "6410"],
            ["1976", "36172", "25338", "3875", "6959"],
            ["1977", "36646", "25470", "3398", "7778"],
            ["1978", "41206", "28411", "4094", "8701"],
            ["1979", "49273", "33361", "4174", "11738"],
            ["1980", "57352", "38737", "4845", "13770"],
            ["1981", "63500", "42491", "4640", "16369"],
            ["1982", "71179", "47439", "5502", "18238"],
            ["1983", "82860", "57577", "5555", "19728"],
            ["1984", "95510", "67146", "6877", "21487"],
            ["1985", "112275", "80337", "9999", "21939"],
            ["1986", "131826", "95908", "11166", "24752"],
            ["1987", "157861", "112387", "16170", "29304"],
            ["1988", "206338", "150460", "18169", "37709"],
            ["1989", "216622", "152721", "18617", "45284"],
            ["1990", "222831", "158434", "20134", "44263"],
        ],
        "status": "verified",
        "notes": "已据页级OCR回源核录：workbench/ocr/paddle_ocr/中/part02/page_0132.txt。单位为万元；本页为表33-5续表尾段。",
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
