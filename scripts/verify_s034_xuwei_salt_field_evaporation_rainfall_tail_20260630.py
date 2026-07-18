# -*- coding: utf-8 -*-
"""Verify table 13-3 Xu Wei salt field evaporation/rainfall continuation."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
DATA_DIR = ROOT / "workbench" / "table_entries" / "上" / "data"

COLUMNS = ["年份", "蒸发量(mm)", "降水量(mm)", "年份", "蒸发量(mm)", "降水量(mm)"]

PATCHES = {
    "LYG-上-T034": {
        "title": "1951~1990年连云港市境内徐圩盐场蒸发量、降水量统计表（续表）",
        "table_number": "表13-3",
        "pages": [739],
        "columns": COLUMNS,
        "rows": [
            ["1969", "2000.6", "879.9", "1980", "1594.0", "625.2"],
            ["1970", "1967.1", "1009.2", "1981", "1834.3", "742.9"],
            ["1971", "2122.8", "1473.3", "1982", "1644.5", "884.1"],
            ["1972", "1977.2", "1016.9", "1983", "1610.2", "810.6"],
            ["1973", "1881.4", "853.5", "1984", "1429.8", "861.9"],
            ["1974", "1816.7", "1044.1", "1985", "1391.6", "917.5"],
            ["1975", "1711.4", "1225.7", "1986", "1881.8", "789.9"],
            ["1976", "1719.6", "724.5", "1987", "1599.0", "971.7"],
            ["1977", "1810.2", "700.6", "1988", "1818.3", "579.1"],
            ["1978", "2105.8", "611.5", "1989", "1633.4", "869.1"],
            ["1979", "1808.3", "1243.6", "1990", "1290.7", "1271.0"],
        ],
        "status": "verified",
        "notes": "已据页级OCR回源核录：workbench/ocr/paddle_ocr/上/part03/page_0134.txt，并参考 raw OCR：workbench/table_entries/上/raw/LYG-上-T034_739.txt。表题、表号和单位依据前页 workbench/ocr/paddle_ocr/上/part03/page_0133.txt；本页为表13-3续上表，单位为毫米。原JSON仅存1985/1990两行摘要，本轮按源页双栏年份结构重录。",
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
