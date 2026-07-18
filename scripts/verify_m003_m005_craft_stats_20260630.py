# -*- coding: utf-8 -*-
"""Verify craft-industry production/business statistics tables."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
DATA_DIR = ROOT / "workbench" / "table_entries" / "中" / "data"

GENERAL_COLUMNS = ["年份", "产量(万件)", "产值(万元)", "销售(万元)", "利税总额(万元)", "利润(万元)"]
CARPET_COLUMNS = ["年份", "产量(平方米)", "产值(万元)", "销售(万元)", "利税总额(万元)", "利润(万元)"]
FIREWORKS_COLUMNS = ["年份", "爆竹产量(箱)", "烟花产量(箱)", "产值(万元)", "销售(万元)", "利税总额(万元)", "利润(万元)"]

PATCHES = {
    "LYG-中-T003": {
        "title": "1963~1990年连云港市柳制品生产经营情况表",
        "table_number": "表17-7",
        "page": 942,
        "pages": [942],
        "part": "part01",
        "vol": "中",
        "volume": "中",
        "columns": GENERAL_COLUMNS,
        "rows": [
            ["1963", "1.80", "3.76", "3.14", "0.36", "0.16"],
            ["1964", "1.79", "3.74", "3.64", "0.40", "0.19"],
            ["1965", "1.46", "5.56", "4.52", "0.43", "0.20"],
            ["1966", "1.10", "8.54", "9.38", "1.09", "0.63"],
            ["1967", "3.95", "7.44", "7.33", "0.59", "0.23"],
            ["1968", "5.04", "7.05", "4.04", "-0.54", "-0.74"],
            ["1969", "0.91", "0.73", "1.02", "0.10", "0.04"],
            ["1970", "7.68", "10.75", "13.66", "0.90", "0.37"],
            ["1971", "9.56", "13.42", "13.84", "1.09", "1.01"],
            ["1972", "12.24", "15.42", "15.48", "-3.02", "-3.80"],
            ["1973", "11.76", "14.82", "14.82", "0.78", "0.07"],
            ["1974", "19.90", "25.07", "20.71", "3.22", "2.27"],
            ["1975", "22.86", "28.80", "31.23", "3.57", "2.20"],
            ["1976", "41.04", "43.17", "43.21", "10.09", "7.93"],
            ["1977", "45.54", "55.88", "49.07", "7.95", "5.57"],
            ["1978", "59.10", "76.24", "55.59", "10.41", "7.64"],
            ["1979", "94.96", "127.44", "51.08", "6.07", "5.11"],
            ["1980", "50.69", "69.93", "42.75", "8.62", "3.30"],
            ["1981", "89.20", "63.08", "41.04", "4.92", "2.76"],
            ["1982", "35.95", "39.14", "30.00", "2.02", "0.54"],
            ["1983", "32.48", "47.92", "35.85", "2.61", "1.12"],
            ["1984", "36.35", "59.36", "60.42", "3.60", "1.93"],
            ["1985", "105.05", "84.55", "65.10", "5.07", "1.42"],
            ["1986", "45.36", "202.40", "172.38", "9.38", "1.52"],
            ["1987", "182.02", "309.61", "246.46", "23.36", "13.76"],
            ["1988", "144.02", "285.56", "228.06", "18.32", "10.80"],
            ["1989", "169.59", "533.79", "398.64", "28.84", "12.52"],
            ["1990", "230.72", "800.95", "650.71", "37.77", "9.33"],
        ],
        "status": "verified",
        "notes": "已据页级OCR回源核录：workbench/ocr/paddle_ocr/中/part01/page_0039.txt，并参考 raw OCR：workbench/table_entries/中/raw/LYG-中-T003_942.txt。原JSON为单列骨架。负数按源页录入。",
    },
    "LYG-中-T004": {
        "title": "1958~1990年连云港市手工羊毛地毯生产经营情况表（续表）",
        "table_number": "表17-9",
        "page": 949,
        "pages": [949],
        "part": "part01",
        "vol": "中",
        "volume": "中",
        "columns": CARPET_COLUMNS,
        "rows": [
            ["1979", "5168.07", "82.69", "78.56", "12.92", "8.08"],
            ["1980", "6429.84", "102.88", "120.89", "10.04", "4.00"],
            ["1981", "8046.61", "129.52", "150.92", "16.00", "8.47"],
            ["1982", "7014.00", "114.03", "130.75", "0.12", "-6.66"],
            ["1983", "6148.05", "90.83", "120.23", "5.96", "4.89"],
            ["1984", "3983.48", "59.76", "64.15", "-12.78", "-12.85"],
            ["1985", "2402.92", "42.70", "69.81", "-25.07", "-25.44"],
            ["1986", "3009.49", "120.04", "202.31", "11.57", "0.55"],
            ["1987", "5349.97", "160.89", "278.72", "27.53", "7.97"],
            ["1988", "8301.10", "311.02", "383.98", "26.80", "3.60"],
            ["1989", "11143.45", "340.30", "418.50", "27.60", "4.60"],
            ["1990", "14434.77", "486.25", "352.33", "50.00", "5.50"],
        ],
        "status": "verified",
        "notes": "已据页级OCR回源核录：workbench/ocr/paddle_ocr/中/part01/page_0046.txt，并参考 raw OCR：workbench/table_entries/中/raw/LYG-中-T004_949.txt。表题、表号、单位据前页表头 workbench/ocr/paddle_ocr/中/part01/page_0045.txt 补定。本页为续上表，原JSON沿用柳制品标题有误。负数按源页录入。",
    },
    "LYG-中-T005": {
        "title": "1976~1990年连云港市烟花爆竹生产经营情况表（续表）",
        "table_number": "表17-11",
        "page": 954,
        "pages": [954],
        "part": "part01",
        "vol": "中",
        "volume": "中",
        "columns": FIREWORKS_COLUMNS,
        "rows": [
            ["1987", "3800", "800", "85.03", "80.27", "26.50", "2.54"],
            ["1988", "3400", "840", "60.01", "45.31", "14.93", "1.47"],
            ["1989", "3250", "960", "40.02", "38.26", "12.64", "1.23"],
            ["1990", "3470", "1530", "86.00", "85.01", "28.10", "2.60"],
        ],
        "status": "verified",
        "notes": "已据页级OCR回源核录：workbench/ocr/paddle_ocr/中/part01/page_0051.txt，并参考 raw OCR：workbench/table_entries/中/raw/LYG-中-T005_954.txt。表题、表号、列组据前页表头 workbench/ocr/paddle_ocr/中/part01/page_0050.txt 补定。本页为续上表，原JSON沿用柳制品标题有误。",
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
