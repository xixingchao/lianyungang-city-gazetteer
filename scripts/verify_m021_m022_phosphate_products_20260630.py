# -*- coding: utf-8 -*-
"""Verify phosphate products output statistics tables."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
DATA_DIR = ROOT / "workbench" / "table_entries" / "中" / "data"

COLUMNS = [
    "年份",
    "牙膏级磷酸氢钙产量(吨)",
    "牙膏级磷酸氢钙其中出口(吨)",
    "药用级磷酸氢钙(吨)",
    "食品级磷酸氢钙(吨)",
    "有水焦磷酸钠(吨)",
    "无水焦磷酸钠(吨)",
    "三聚磷酸钠(吨)",
    "磷酸二氢钾(工业级)(吨)",
    "焦磷酸钾(吨)",
]

PATCHES = {
    "LYG-中-T021": {
        "title": "1965~1990年连云港市磷酸盐主要产品产量统计表",
        "table_number": "表20-3",
        "page": 1051,
        "pages": [1051],
        "part": "part01",
        "vol": "中",
        "volume": "中",
        "columns": COLUMNS,
        "rows": [
            ["1965", "221", "84", "", "", "24", "", "", "", ""],
            ["1966", "321", "100", "", "", "88", "", "", "", ""],
            ["1967", "133", "82", "", "", "13", "", "", "", ""],
            ["1968", "", "", "", "", "", "", "", "", ""],
            ["1969", "32", "", "", "", "112", "3", "", "", ""],
        ],
        "status": "verified",
        "notes": "已据页级OCR回源核录：workbench/ocr/paddle_ocr/中/part01/page_0148.txt，并参考 raw OCR：workbench/table_entries/中/raw/LYG-中-T021_1051.txt。原JSON为单列骨架。1968年源页仅见年份，其他栏保留空值；1969年按源页列位录入牙膏级磷酸氢钙产量、有水焦磷酸钠、无水焦磷酸钠。续表见LYG-中-T022。",
    },
    "LYG-中-T022": {
        "title": "1965~1990年连云港市磷酸盐主要产品产量统计表（续表）",
        "table_number": "表20-3",
        "page": 1052,
        "pages": [1052],
        "part": "part01",
        "vol": "中",
        "volume": "中",
        "columns": COLUMNS,
        "rows": [
            ["1970", "612", "294", "", "", "106", "", "", "", ""],
            ["1971", "805", "187", "410", "", "135", "", "", "", ""],
            ["1972", "1158", "161", "", "", "181", "213", "", "", ""],
            ["1973", "1406", "206", "", "", "136", "88", "", "", ""],
            ["1974", "617", "109", "", "", "170", "67", "", "", ""],
            ["1975", "633", "130", "", "", "322", "183", "95", "", ""],
            ["1976", "896", "223", "", "", "403", "137", "55", "", ""],
            ["1977", "1067", "230", "", "", "341", "41", "292", "", "59"],
            ["1978", "1355", "550", "447", "", "372", "44", "15", "", ""],
            ["1979", "1932", "116", "176", "294", "396", "6", "", "", ""],
            ["1980", "2992", "300", "189", "147", "128", "", "", "45", ""],
            ["1981", "2930", "500", "228", "17", "162", "133", "360", "44", ""],
            ["1982", "2515", "1100", "458", "193", "119", "333", "670", "49", ""],
            ["1983", "875", "526", "289", "104", "771", "468", "84", "", ""],
            ["1984", "1498", "176", "397", "294", "96", "853", "704", "22", "84"],
            ["1985", "2668", "640", "486", "362", "215", "855", "1390", "67", "56"],
            ["1986", "3339", "650", "465", "504", "191", "1034", "1437", "150", "67"],
            ["1987", "4179", "882", "674", "646", "330", "860", "231", "382", "360"],
            ["1988", "4670", "438", "737", "728", "385", "931", "365", "336", ""],
            ["1989", "1784", "95", "773", "496", "240", "681", "401", "355", "374"],
            ["1990", "1762", "795", "652", "175", "975", "2141", "265", "353", ""],
        ],
        "status": "verified",
        "notes": "已据页级OCR回源核录：workbench/ocr/paddle_ocr/中/part01/page_0149.txt，并参考 raw OCR：workbench/table_entries/中/raw/LYG-中-T022_1052.txt。表题、表号、单位和列组据前页 workbench/ocr/paddle_ocr/中/part01/page_0148.txt 补定。本页为表20-3续上表；源页未见数值的单元格保留空值。",
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
