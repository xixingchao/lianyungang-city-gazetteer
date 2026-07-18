# -*- coding: utf-8 -*-
"""Verify edible oil supply for agricultural population table from page OCR."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
DATA_DIR = ROOT / "workbench" / "table_entries" / "中" / "data"

COLUMNS = ["年份", "合计", "市区", "赣榆县", "东海县", "灌云县"]

PATCHES = {
    "LYG-中-T098": {
        "title": "1957~1990年连云港市供应农业人口食油统计表",
        "table_number": "表36-9",
        "page": 1647,
        "pages": [1647],
        "columns": COLUMNS,
        "rows": [
            ["1957", "1532", "24", "275", "613", "620"],
            ["1958", "1473", "94", "496", "379", "504"],
            ["1959", "1094", "71", "360", "320", "343"],
            ["1960", "1156", "63", "368", "377", "348"],
            ["1961", "315", "20", "93", "67", "135"],
            ["1962", "388", "21", "229", "86", "52"],
            ["1963", "340", "14", "150", "136", "40"],
            ["1964", "730", "85", "170", "220", "255"],
            ["1965", "1052", "115", "315", "237", "385"],
            ["1966", "565", "85", "170", "100", "210"],
            ["1967", "565", "95", "155", "90", "225"],
            ["1968", "625", "70", "145", "110", "300"],
            ["1969", "770", "80", "135", "140", "415"],
        ],
        "status": "verified",
        "notes": "已据页级OCR回源核录：workbench/ocr/paddle_ocr/中/part02/page_0227.txt。单位为吨；页首含上一表续表残段，本轮仅录入表36-9首页。",
    },
    "LYG-中-T099": {
        "title": "1957~1990年连云港市供应农业人口食油统计表（续表）",
        "table_number": "表36-9",
        "page": 1648,
        "pages": [1648],
        "columns": COLUMNS,
        "rows": [
            ["1970", "887", "100", "133", "159", "495"],
            ["1971", "599", "60", "140", "270", "129"],
            ["1972", "464", "96", "121", "112", "135"],
            ["1973", "434", "71", "116", "82", "165"],
            ["1974", "652", "88", "155", "123", "286"],
            ["1975", "527", "102", "154", "135", "136"],
            ["1976", "322", "105", "126", "56", "35"],
            ["1977", "218", "87", "95", "10", "26"],
            ["1978", "215", "86", "93", "10", "26"],
            ["1979", "209", "84", "95", "12", "18"],
            ["1980", "403", "79", "222", "87", "15"],
            ["1981", "587", "94", "208", "252", "33"],
            ["1982", "307", "122", "134", "21", "30"],
            ["1983", "316", "117", "137", "33", "29"],
            ["1984", "313", "116", "145", "25", "27"],
            ["1985", "238", "108", "89", "17", "24"],
            ["1986", "153", "100", "1", "11", "41"],
            ["1987", "169", "79", "", "12", "78"],
            ["1988", "127", "78", "2", "12", "35"],
            ["1989", "129", "72", "11", "", "46"],
            ["1990", "110", "73", "1", "10", "26"],
        ],
        "status": "verified",
        "notes": "已据页级OCR回源核录：workbench/ocr/paddle_ocr/中/part02/page_0228.txt。单位为吨；本页为表36-9续表尾段。1987年赣榆县、1989年东海县列源页OCR未给出数值，按源保留空白。",
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
