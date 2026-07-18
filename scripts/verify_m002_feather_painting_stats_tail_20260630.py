# -*- coding: utf-8 -*-
"""Verify feather-painting production statistics continuation."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
DATA_DIR = ROOT / "workbench" / "table_entries" / "中" / "data"

COLUMNS = ["年份", "产量(万幅)", "产值(万元)", "销售(万元)", "利税总额(万元)", "利润(万元)"]

PATCHES = {
    "LYG-中-T002": {
        "title": "1969~1990年连云港市羽毛画生产经营情况表（续表）",
        "table_number": "",
        "page": 929,
        "pages": [929],
        "part": "part01",
        "vol": "中",
        "columns": COLUMNS,
        "rows": [
            ["1969", "0.44", "8.81", "0.88", "0.55", "-0.43"],
            ["1970", "0.21", "4.17", "2.99", "0.51", "0.26"],
            ["1971", "0.24", "5.46", "5.06", "1.22", "0.90"],
            ["1972", "0.35", "8.43", "6.80", "1.48", "0.93"],
            ["1973", "0.65", "16.76", "11.00", "1.97", "1.42"],
            ["1974", "0.62", "17.63", "13.01", "3.35", "2.43"],
            ["1975", "0.66", "16.20", "16.00", "2.30", "1.72"],
            ["1976", "0.87", "14.74", "13.80", "1.85", "0.88"],
            ["1977", "0.86", "18.50", "19.91", "2.38", "1.42"],
            ["1978", "1.00", "21.46", "19.83", "3.48", "2.50"],
            ["1979", "0.87", "23.75", "23.24", "2.32", "1.11"],
            ["1980", "1.88", "41.12", "35.11", "4.52", "2.71"],
            ["1981", "2.35", "49.38", "39.26", "5.39", "3.09"],
            ["1982", "2.41", "68.74", "63.50", "8.82", "5.40"],
            ["1983", "3.83", "170.30", "86.90", "13.52", "9.15"],
            ["1984", "5.30", "149.58", "107.05", "20.25", "14.90"],
            ["1985", "7.35", "220.84", "190.42", "47.85", "37.60"],
            ["1986", "9.17", "290.22", "249.32", "52.17", "44.05"],
            ["1987", "8.66", "330.77", "279.41", "52.51", "40.85"],
            ["1988", "8.01", "265.03", "295.69", "46.18", "25.91"],
            ["1989", "5.09", "228.60", "167.90", "10.62", "-1.53"],
            ["1990", "5.02", "338.20", "251.45", "2.01", "-12.36"],
        ],
        "status": "verified",
        "notes": "已据页级OCR回源核录：workbench/ocr/paddle_ocr/中/part01/page_0026.txt，并参考 raw OCR：workbench/table_entries/中/raw/LYG-中-T002_929.txt。本页为羽毛画生产经营统计续上表；源页未见表号。表题依据本页表尾紧接的“二、羽毛画”正文及同章相邻产品统计表格式补定。负数按源页录入。",
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
