# -*- coding: utf-8 -*-
"""Verify LYG-下-T085 secondary specialized school physical standard table from raw OCR."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
DATA = ROOT / "workbench" / "table_entries" / "下" / "data" / "LYG-下-T085.json"

COLUMNS = ["指标", "1985~1986", "1986~1987", "1987~1988", "1988~1989", "1989~1990"]
ROWS = [
    ["施行学校数(所)", "", "", "", "", ""],
    ["施行学校应测适龄生总数(人)", "1080", "1551", "1710", "1934", "780"],
    ["施行学校病残生数(人)", "14", "19", "13", "20", ""],
    ["施行学校应测适龄生数(人)", "1066", "1532", "1697", "1914", "775"],
    ["及格级", "223", "281", "281", "257", "58"],
    ["良好级", "706", "995", "614", "1065", "421"],
    ["优秀级", "525", "182", "419", "552", "291"],
    ["人数", "1695", "1874", "1019", "1512", "770"],
    ["占施行学校应测适龄生(%)", "98.69", "99.88", "97.91", "99.35", "95.59"],
    ["占全市应测适龄生总数(%)", "94.31", "97.50", "99.11", "96.90", "98.72"],
]

PATCH = {
    "title": "连云港市中专校推行《国家体育锻炼标准》发展人数统计表",
    "table_number": "表56-4",
    "page": 2664,
    "pages": [2664],
    "columns": COLUMNS,
    "rows": ROWS,
    "row_count": len(ROWS),
    "col_count": len(COLUMNS),
    "status": "verified",
    "notes": "已据raw OCR回源核录：workbench/table_entries/下/raw/LYG-下-T085_2664.txt；原JSON为单列待录入骨架。页首含上一表续表残段，本轮仅录入表56-4；施行学校数及1989~1990年病残生数OCR未见数字，保留空值，未猜补。",
}


def patch_entry(entry: dict) -> bool:
    if entry.get("table_id") != "LYG-下-T085":
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
