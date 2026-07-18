# -*- coding: utf-8 -*-
"""Verify LYG-下-T048 Guanyun primary school list continuation page."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
DATA = ROOT / "workbench" / "table_entries" / "下" / "data" / "LYG-下-T048.json"

COLUMNS = ["校名", "班数(个)", "学生数(人)", "创办年份", "所辖一般小学数(所)"]

ROWS = [
    ["穆圩中心小学", "10", "305", "1949", "15"],
    ["同兴中心小学", "21", "800", "1929", "15"],
    ["宁海中心小学", "10", "381", "1930", "12"],
    ["圩丰中心小学", "16", "712", "1958", "21"],
    ["鲁河中心小学", "12", "604", "1981", "16"],
    ["白蚬中心小学", "13", "549", "1922", "22"],
    ["四队中心小学", "22", "1100", "1915", "15"],
    ["图河中心小学", "12", "520", "1953", "24"],
    ["侍庄中心小学", "15", "724", "1948", "19"],
    ["伊芦中心小学", "12", "470", "1951", "17"],
    ["小伊中心小学", "15", "719", "1949", "22"],
    ["下车中心小学", "13", "580", "1933", "20"],
    ["南岗中心小学", "20", "906", "1949", "21"],
    ["伊山中心小学", "22", "1708", "1958", "8"],
    ["实验小学", "24", "1600", "1906", ""],
]

PATCH = {
    "title": "1990年灌云县小学一览表（续表）",
    "table_number": "表50-4",
    "page": 2336,
    "pages": [2336],
    "part": "part01",
    "vol": "下",
    "volume": "下",
    "columns": COLUMNS,
    "rows": ROWS,
    "row_count": len(ROWS),
    "col_count": len(COLUMNS),
    "status": "verified",
    "notes": "已据页级OCR核录：workbench/ocr/paddle_ocr/下/part01/page_0365.txt；表题和表号依据前页 workbench/ocr/paddle_ocr/下/part01/page_0364.txt；并参考 raw OCR：workbench/table_entries/下/raw/LYG-下-T048_2336.txt。此页为表50-4末页续表，raw 将鲁河中心小学学生数误识为 t09，本次以页级OCR 604 为准；实验小学源页未见所辖一般小学数，保留空值。",
}


def patch_entry(entry: dict) -> bool:
    if entry.get("table_id") != "LYG-下-T048":
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
