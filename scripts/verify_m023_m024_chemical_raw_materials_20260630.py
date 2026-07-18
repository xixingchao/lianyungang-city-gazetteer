# -*- coding: utf-8 -*-
"""Verify chemical raw-material product output tables."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
DATA_DIR = ROOT / "workbench" / "table_entries" / "中" / "data"

SALT_COLUMNS = [
    "年份",
    "有水硫酸钠(吨)",
    "无水亚硫酸钠(吨)",
    "焦亚硫酸钠产量(吨)",
    "焦亚硫酸钠其中出口(吨)",
    "硅酸钠(吨)",
    "轻质氧化镁(吨)",
    "氢氧化镁(吨)",
    "电熔镁(吨)",
]

INTERMEDIATE_COLUMNS = [
    "年份",
    "电石(吨)",
    "三氯化磷(吨)",
    "甘露醇产量(吨)",
    "甘露醇其中出口(吨)",
    "海藻酸钠产量(吨)",
    "海藻酸钠其中出口(吨)",
    "五硫化二磷(吨)",
    "二甲基甲酰胺(吨)",
    "单甲基甲酰胺(吨)",
    "氯化苄(吨)",
    "苯甲醛(吨)",
]

PATCHES = {
    "LYG-中-T023": {
        "title": "1973~1990年连云港市硫酸钠、硅酸钠、氧化镁主要产品产量统计表",
        "table_number": "表20-5",
        "page": 1055,
        "pages": [1055],
        "part": "part01",
        "vol": "中",
        "volume": "中",
        "columns": SALT_COLUMNS,
        "rows": [
            ["1973", "162", "", "", "", "2282", "30", "", ""],
            ["1974", "", "", "", "", "2695", "", "", ""],
            ["1975", "", "", "", "", "", "", "", ""],
            ["1976", "628", "", "", "", "4234", "", "", ""],
            ["1977", "1234", "", "", "", "4100", "69", "", ""],
            ["1978", "1846", "7", "", "", "4151", "", "", ""],
            ["1979", "1641", "130", "", "", "4187", "", "", ""],
            ["1980", "2413", "375", "", "", "2949", "111", "", "2.14"],
            ["1981", "1611", "112", "", "", "3517", "83", "31", ""],
            ["1982", "785", "168", "", "", "2515", "97", "46", "1.52"],
            ["1983", "615", "148", "", "", "4119", "74", "", "4.75"],
            ["1984", "", "", "", "", "3684", "213", "60", "3.84"],
            ["1985", "", "", "", "", "2793", "40", "173", "6.59"],
            ["1986", "", "", "", "", "3667", "235", "1000", "5.72"],
            ["1987", "1722", "423", "163", "60", "2000", "237", "", ""],
            ["1988", "515", "795", "680", "", "3000", "215", "12", "5.48"],
            ["1989", "4354", "393", "767", "342", "3200", "117", "3", "0.64"],
            ["1990", "3944", "407", "943", "461", "3500", "223", "16", "8.01"],
        ],
        "status": "verified",
        "notes": "已据页级OCR回源核录：workbench/ocr/paddle_ocr/中/part01/page_0152.txt，并参考 raw OCR：workbench/table_entries/中/raw/LYG-中-T023_1055.txt。原JSON为单列骨架。源页未见数值的单元格保留空值；焦亚硫酸钠列组按源页列头产量/其中出口拆列。",
    },
    "LYG-中-T024": {
        "title": "1964~1990年连云港市化工中间体产量统计表（续表）",
        "table_number": "表20-8",
        "page": 1063,
        "pages": [1063],
        "part": "part01",
        "vol": "中",
        "volume": "中",
        "columns": INTERMEDIATE_COLUMNS,
        "rows": [
            ["1975", "142", "", "765", "", "1287", "1166", "185", "", "", "", ""],
            ["1976", "78", "", "759", "", "1520", "1348", "316", "105", "", "", ""],
            ["1977", "146", "17", "795", "", "2051", "1602", "279", "100", "200", "10", ""],
            ["1978", "166", "", "884", "", "2297", "1718", "420", "180", "4", "360", "17"],
            ["1979", "216", "", "941", "", "4114", "1505", "409", "366", "19", "445", ""],
            ["1980", "146", "63", "683", "", "4437", "1203", "419", "612", "60", "803", "12"],
            ["1981", "144", "79", "546", "56", "3019", "1111", "374", "933", "62", "619", "20"],
            ["1982", "240", "140", "753", "102", "4496", "1298", "977", "736", "47", "804", "40"],
            ["1983", "336", "35", "868", "350", "4468", "1228", "1024", "1618", "73", "700", "130"],
            ["1984", "379", "20", "822", "483", "3152", "575", "1229", "1706", "123", "925", "116"],
            ["1985", "306", "20", "674", "319", "4124", "263", "497", "741", "163", "1184", "127"],
            ["1986", "287", "10", "677", "439", "4524", "338", "1015", "", "159", "1180", "136"],
            ["1987", "389", "8", "818", "516", "3917", "1117", "900", "", "139", "1484", "161"],
            ["1988", "275", "10", "800", "620", "3551", "1895", "1024", "", "93", "921", "179"],
            ["1989", "190", "", "976", "761", "3926", "1976", "936", "", "101", "841", "260"],
            ["1990", "339", "", "1053", "792", "2009", "1508", "1321", "", "114", "714", "564"],
        ],
        "status": "verified",
        "notes": "已据页级OCR回源核录：workbench/ocr/paddle_ocr/中/part01/page_0160.txt，并参考 raw OCR：workbench/table_entries/中/raw/LYG-中-T024_1063.txt。表题、表号、单位和列组据前页 workbench/ocr/paddle_ocr/中/part01/page_0159.txt 补定。原JSON误沿用硫酸钠、硅酸钠、氧化镁表题；本页为表20-8续上表。源页未见数值的单元格保留空值。",
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
