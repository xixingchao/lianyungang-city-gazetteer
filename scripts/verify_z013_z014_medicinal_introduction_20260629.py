# -*- coding: utf-8 -*-
"""Verify LYG-中-T013/T014 medicinal material introduction table."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
DATA_DIR = ROOT / "workbench" / "table_entries" / "中" / "data"

COLUMNS = ["品种", "年份", "种苗来源", "栽培地区", "平均亩产(公斤)", "最高亩产产量(公斤)", "最高亩产年份"]

PATCHES = {
    "LYG-中-T013": {
        "title": "连云港市主要药材引种情况一览表",
        "table_number": "表19-3",
        "page": 1021,
        "pages": [1021],
        "columns": COLUMNS,
        "rows": [
            ["太子参", "1957", "山东临沭", "赣榆、东海", "139", "268", "1969"],
            ["玄参", "1958", "山东郯城", "赣榆", "205", "385", "1976"],
            ["北沙参", "1959", "山东莱阳", "赣榆", "131", "313", "1969"],
            ["白芍", "1959", "杭州", "赣榆、东海、灌云", "466", "844", "1975"],
            ["佩兰", "1965", "淮阴", "灌云", "750", "810", "1984"],
            ["薏苡", "1968", "徐州", "赣榆、东海、灌云", "163", "410", "1977"],
        ],
        "status": "verified",
        "notes": "已据页级OCR回源核录：workbench/ocr/paddle_ocr/中/part01/page_0118.txt，并与raw OCR workbench/table_entries/中/raw/LYG-中-T013_1021.txt互校。复合表头展开为平均亩产、最高亩产产量、最高亩产年份。续表见LYG-中-T014。",
    },
    "LYG-中-T014": {
        "title": "连云港市主要药材引种情况一览表（续表）",
        "table_number": "表19-3",
        "page": 1022,
        "pages": [1022],
        "columns": COLUMNS,
        "rows": [
            ["地黄", "1968", "邳县", "赣榆、东海、灌云", "218", "435", "1979"],
            ["牡丹", "1971", "徐州", "赣榆、东海、灌云", "310", "620", "1979"],
            ["延胡索", "1972", "南通", "赣榆、东海、灌云", "144", "190", "1978"],
            ["板蓝根", "1973", "安徽", "东海、灌云", "151", "186", "1978"],
            ["黄芪", "1973", "黑龙江依兰县", "赣榆、东海、灌云", "170", "261", "1979"],
            ["桔梗", "1979", "山东临沭", "赣榆、东海、灌云", "120", "252", "1982"],
        ],
        "status": "verified",
        "notes": "已据页级OCR回源核录：workbench/ocr/paddle_ocr/中/part01/page_0119.txt，并与raw OCR workbench/table_entries/中/raw/LYG-中-T014_1022.txt互校。本页为表19-3续表；续表结束后转入正文，未纳入本表。",
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
