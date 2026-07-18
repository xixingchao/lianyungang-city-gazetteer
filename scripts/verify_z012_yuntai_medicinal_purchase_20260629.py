# -*- coding: utf-8 -*-
"""Verify LYG-中-T012 Yuntai Mountain medicinal material purchase table."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
DATA = ROOT / "workbench" / "table_entries" / "中" / "data" / "LYG-中-T012.json"

COLUMNS = ["品名", "历史最高收购实绩年份", "历史最高收购实绩数量(公斤)", "1983年收购实绩(公斤)", "1990年收购实绩(公斤)"]
ROWS = [
    ["徐长卿", "1971", "587.5", "75.0", "11"],
    ["威灵仙", "1971", "1934.5", "273.0", "144"],
    ["半夏", "1973", "193.5", "1.2", "10"],
    ["苍术", "1967", "181.5", "0.5", "2"],
    ["玉竹", "1979", "555.7", "85.3", "17"],
    ["白薇", "1967", "664.5", "49.4", "176"],
    ["百部", "1967", "2449.0", "170.6", "520"],
    ["茜草", "1966", "275.0", "61.3", "150"],
    ["拳参", "1971", "13490.0", "5175.0", "625"],
]

PATCH = {
    "title": "建国后部分年份连云港市收购云台山中药材比较表",
    "table_number": "表19-2",
    "page": 1020,
    "pages": [1020],
    "columns": COLUMNS,
    "rows": ROWS,
    "row_count": len(ROWS),
    "col_count": len(COLUMNS),
    "status": "verified",
    "notes": "已据页级OCR回源核录：workbench/ocr/paddle_ocr/中/part01/page_0117.txt，并与raw OCR workbench/table_entries/中/raw/LYG-中-T012_1020.txt互校。单位为公斤；复合表头展开为历史最高收购实绩年份/数量、1983年收购实绩、1990年收购实绩。",
}


def patch_entry(entry: dict) -> bool:
    if entry.get("table_id") != "LYG-中-T012":
        return False
    changed = False
    for key, value in PATCH.items():
        if entry.get(key) != value:
            entry[key] = value
            changed = True
    return changed


def patch_json() -> int:
    data = json.loads(DATA.read_text(encoding="utf-8"))
    if patch_entry(data):
        DATA.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        return 1
    return 0


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
