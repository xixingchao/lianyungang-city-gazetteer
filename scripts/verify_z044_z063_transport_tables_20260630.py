# -*- coding: utf-8 -*-
"""Verify two transport-related structured tables from page-level OCR."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
DATA_DIR = ROOT / "workbench" / "table_entries" / "中" / "data"

PATCHES = {
    "LYG-中-T044": {
        "title": "1949~1990年连云港港货物吞吐量统计表",
        "table_number": "表29-8",
        "page": 1358,
        "pages": [1358],
        "columns": ["年份", "吞吐量", "其中外贸"],
        "rows": [
            ["1949", "5.60", ""],
            ["1950", "11.10", ""],
            ["1951", "14.20", ""],
            ["1952", "46.30", ""],
            ["1953", "35.12", ""],
            ["1954", "66.00", "1.00"],
            ["1955", "54.30", "0.30"],
            ["1956", "89.90", "0.60"],
            ["1957", "105.40", "6.00"],
            ["1958", "166.80", "10.00"],
            ["1959", "237.60", "2.00"],
            ["1960", "237.20", "1.00"],
            ["1961", "200.00", "1.60"],
            ["1962", "209.50", "3.20"],
            ["1963", "225.60", "10"],
            ["1964", "226.30", "10"],
            ["1965", "265.30", "28"],
            ["1966", "295.40", "50"],
            ["1967", "237.80", "83"],
            ["1968", "87.30", "13"],
            ["1969", "116.80", "25"],
            ["1970", "256.46", "63"],
            ["1971", "335.40", "590"],
            ["1972", "274.50", "68"],
            ["1973", "244.00", "81"],
            ["1974", "241.60", "65"],
            ["1975", "322.00", "68"],
            ["1976", "303.50", "64"],
            ["1977", "431.80", "152"],
            ["1978", "593.60", "199"],
            ["1979", "681.40", "283"],
            ["1980", "739.00", "293"],
            ["1981", "756.40", "332"],
            ["1982", "805.90", "345"],
            ["1983", "857.80", "408"],
            ["1984", "900.10", "449"],
            ["1985", "929.00", "523"],
            ["1986", "948.50", "536"],
            ["1987", "894.10", "541"],
            ["1988", "1114.00", "690"],
            ["1989", "1125.00", "642"],
            ["1990", "1137.00", "623"],
        ],
        "status": "verified",
        "notes": "已据页级OCR回源核录：workbench/ocr/paddle_ocr/中/part01/page_0455.txt。单位为万吨；1949~1953年外贸列源页为空，按源保留空白。",
    },
    "LYG-中-T063": {
        "title": "1990年连云港市筑路养护机械统计表",
        "table_number": "表30-10",
        "page": 1461,
        "pages": [1461],
        "columns": [
            "单位",
            "压路机(台)",
            "载重汽车(辆)",
            "拖拉机(台)",
            "混凝土搅拌机(台)",
            "沥青洒布机(台)",
            "装载机(台)",
            "洒水车(辆)",
            "翻斗车(辆)",
            "维修机床(台)",
        ],
        "rows": [
            ["连云港市公路管理处", "8", "20", "9", "8", "7", "2", "3", "40", "10"],
            ["赣榆县公路管理站", "11", "4", "12", "1", "2", "2", "", "9", "10"],
            ["东海县公路管理站", "9", "5", "8", "1", "1", "1", "", "24", "1"],
            ["灌云县公路管理站", "8", "4", "10", "", "", "2", "", "3", "7"],
        ],
        "status": "verified",
        "notes": "已据页级OCR回源核录：workbench/ocr/paddle_ocr/中/part02/page_0041.txt。源页未列数值的单元格保留空白；原 OCR 将“洒水车”识为“酒水车”，本轮按表头语义规范。",
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
