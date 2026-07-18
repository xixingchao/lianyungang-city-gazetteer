# -*- coding: utf-8 -*-
"""Verify LYG-中-T074/T075 state commerce cloth sales table."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
DATA_DIR = ROOT / "workbench" / "table_entries" / "中" / "data"

COLUMNS = ["年份", "棉布(万米)", "混纺布(万米)", "化纤布(万米)", "呢料(万米)"]

PATCHES = {
    "LYG-中-T074": {
        "title": "1949~1990年部分年份连云港市市区国营商业主要商品零售量统计表（一）",
        "table_number": "表33-6",
        "page": 1555,
        "pages": [1555],
        "part": "part02",
        "vol": "中",
        "volume": "中",
        "columns": COLUMNS,
        "rows": [
            ["1949", "246", "", "", "0.01"],
            ["1952", "287", "", "", "0.01"],
            ["1957", "306", "", "", "0.11"],
            ["1962", "186", "", "", "0.97"],
            ["1965", "241", "", "", "1.77"],
        ],
        "status": "verified",
        "notes": "已据页级OCR核录：workbench/ocr/paddle_ocr/中/part02/page_0135.txt；并参考 raw 坐标 OCR：workbench/ocr/raw/中/part02/page_0135.json 与 raw 文本 workbench/table_entries/中/raw/LYG-中-T074_1555.txt。本条仅录入表33-6首页 1949-1965 年记录；续页 1970-1990 年记录由 LYG-中-T075 承接。源页未见数值处保留空值。",
    },
    "LYG-中-T075": {
        "title": "1949~1990年部分年份连云港市市区国营商业主要商品零售量统计表（一）续表",
        "table_number": "表33-6",
        "page": 1556,
        "pages": [1556],
        "part": "part02",
        "vol": "中",
        "volume": "中",
        "columns": COLUMNS,
        "rows": [
            ["1970", "349", "", "43", "5.92"],
            ["1971", "394", "", "28", "5.95"],
            ["1972", "415", "", "44", "5.25"],
            ["1973", "350", "", "69", "4.35"],
            ["1974", "366", "", "64", "4.56"],
            ["1975", "415", "27", "64", "4.41"],
            ["1976", "444", "62", "37", "5.21"],
            ["1977", "365", "93", "25", "6.04"],
            ["1978", "292", "105", "39", "4.93"],
            ["1979", "361", "130", "59", "6.39"],
            ["1980", "464", "151", "182", "7.53"],
            ["1981", "428", "180", "61", "5.33"],
            ["1982", "377", "191", "54", "84"],
            ["1983", "370", "248", "123", "24"],
            ["1984", "880", "176", "105", "22"],
            ["1985", "314", "188", "82", "31"],
            ["1986", "387", "479", "63", "19"],
            ["1987", "268", "132", "55", "21"],
            ["1988", "259", "190", "69", "23"],
            ["1989", "236", "171", "64", "18"],
            ["1990", "102", "102", "75", "17"],
        ],
        "status": "verified",
        "notes": "已据页级OCR核录：workbench/ocr/paddle_ocr/中/part02/page_0136.txt；并参考 raw 坐标 OCR：workbench/ocr/raw/中/part02/page_0136.json 与 raw 文本 workbench/table_entries/中/raw/LYG-中-T075_1556.txt。本条仅录入表33-6续页 1970-1990 年记录，同页后续表33-7首页未并入；1975 年化纤布 raw 坐标 OCR 误识为 `t9`，按页级 OCR 更正为 `64`；源页未见数值处保留空值。",
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
