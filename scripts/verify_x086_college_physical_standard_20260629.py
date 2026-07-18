# -*- coding: utf-8 -*-
"""Verify LYG-下-T086 college physical standard table from raw OCR."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
DATA = ROOT / "workbench" / "table_entries" / "下" / "data" / "LYG-下-T086.json"

COLUMNS = ["指标", "1985~1986", "1986~1987", "1987~1988", "1988~1989", "1989~1990"]
ROWS = [
    ["施行学校数(所)", "", "", "", "", ""],
    ["施行学校应测适龄生总数(人)", "467", "643", "797", "855", "901"],
    ["施行学校病残生数(人)", "12", "", "", "", ""],
    ["施行学校应测适龄生数(人)", "465", "641", "793", "898", "843"],
    ["及格级", "335", "391", "303", "207", "228"],
    ["良好级", "215", "354", "318", "474", "433"],
    ["优秀级", "13", "69", "51", "49", "44"],
    ["人数", "435", "615", "740", "873", "821"],
    ["占施行学校应测适龄生(%)", "93.32", "97.22", "97.39", "93.55", "95.94"],
    ["占全市应测适龄生总数(%)", "95.61", "93.12", "96.90", "96.01", "92.80"],
]

PATCH = {
    "title": "连云港市大专校推行《国家体育锻炼标准》发展人数统计表",
    "table_number": "表56-45",
    "page": 2665,
    "pages": [2665],
    "columns": COLUMNS,
    "rows": ROWS,
    "row_count": len(ROWS),
    "col_count": len(COLUMNS),
    "status": "verified",
    "notes": "已据raw OCR回源核录：workbench/table_entries/下/raw/LYG-下-T086_2665.txt；施行学校数、部分病残生数栏OCR未见数字，保留空值。",
}


def patch_entry(entry: dict) -> bool:
    if entry.get("table_id") != "LYG-下-T086":
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
