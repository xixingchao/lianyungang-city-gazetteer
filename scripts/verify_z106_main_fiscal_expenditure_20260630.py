# -*- coding: utf-8 -*-
"""Verify main fiscal expenditure table from page OCR."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
DATA_DIR = ROOT / "workbench" / "table_entries" / "中" / "data"

PATCHES = {
    "LYG-中-T106": {
        "title": "1949~1990年连云港市主要财政支出统计表",
        "table_number": "表38-6",
        "page": 1719,
        "pages": [1719],
        "columns": ["年份", "金额(万元)", "经济建设支出(万元)", "文教科卫事业费(万元)", "行政管理费和公检法司支出(万元)"],
        "rows": [
            ["合计", "158510", "53295", "74719", "30496"],
            ["1949", "48", "4", "20", "24"],
            ["1950", "64", "8", "24", "32"],
            ["1951", "88", "13", "37", "38"],
            ["1952", "78", "6", "26", "46"],
            ["1953", "129", "26", "43", "60"],
            ["1954", "140", "20", "50", "70"],
            ["1955", "192", "69", "41", "82"],
            ["1956", "294", "69", "112", "113"],
            ["1957", "307", "92", "103", "112"],
            ["1958", "2581", "2309", "163", "109"],
            ["1959", "1350", "1011", "203", "136"],
            ["1960", "616", "228", "267", "121"],
            ["1961", "336", "38", "188", "110"],
            ["1962", "318", "42", "176", "100"],
            ["1963", "332", "61", "166", "105"],
            ["1964", "406", "84", "211", "111"],
            ["1965", "495", "153", "225", "117"],
            ["1966", "637", "264", "258", "115"],
            ["1967", "450", "101", "256", "93"],
            ["1968", "313", "52", "180", "81"],
            ["1969", "754", "418", "210", "126"],
            ["1970", "1238", "832", "258", "148"],
            ["1971", "1067", "620", "273", "174"],
            ["1972", "1980", "1488", "306", "186"],
            ["1973", "2451", "1869", "373", "209"],
            ["1974", "1053", "481", "396", "176"],
            ["1975", "1172", "566", "404", "202"],
            ["1976", "1278", "606", "446", "226"],
            ["1977", "1795", "1075", "482", "238"],
            ["1978", "2169", "1251", "611", "307"],
            ["1979", "2506", "1452", "724", "330"],
            ["1980", "2563", "1312", "900", "351"],
            ["1981", "2273", "787", "1109", "377"],
            ["1982", "2923", "1148", "1344", "431"],
            ["1983", "9737", "3685", "4448", "1604"],
            ["1984", "13128", "5088", "5639", "2401"],
            ["1985", "12799", "4184", "6354", "2261"],
            ["1986", "13689", "3944", "7168", "2577"],
            ["1987", "14391", "3949", "7746", "2696"],
            ["1988", "17446", "3998", "9573", "3875"],
            ["1989", "19684", "4219", "10846", "4619"],
            ["1990", "23240", "5673", "12360", "5207"],
        ],
        "status": "verified",
        "notes": "已据页级OCR回源核录：workbench/ocr/paddle_ocr/中/part02/page_0299.txt。单位为万元；原双栏横排展开为年份、金额、经济建设支出、文教科卫事业费、行政管理费和公检法司支出。",
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
