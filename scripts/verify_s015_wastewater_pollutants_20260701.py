# -*- coding: utf-8 -*-
"""Verify LYG-上-T015 wastewater and pollutants table."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
DATA = ROOT / "workbench" / "table_entries" / "上" / "data" / "LYG-上-T015.json"

COLUMNS = ["项目", "1981", "1985", "1986", "1987", "1988", "1989", "1990"]

ROWS = [
    ["工业废水排放量(万吨)", "7861", "7456", "8464", "8123", "8358", "7984", "7358"],
    ["生活污水排放量(万吨)", "", "1765", "1353", "1437", "1518", "1679", "1745"],
    ["化学耗氧量(吨)", "15000", "31189", "43446", "25823", "33809", "44103", "42937"],
    ["总汞(吨)", "0.278", "0.136", "0.136", "0.024", "0.024", "", ""],
    ["总镉(吨)", "0.005", "0.365", "0.252", "0.385", "0.212", "", ""],
    ["六价铬(吨)", "7.420", "1.160", "0.583", "0.713", "1.822", "1.033", "0.256"],
    ["总砷(吨)", "0.134", "21.840", "26.412", "28.331", "53.036", "57.114", "43.750"],
    ["总铅(吨)", "7.957", "18.050", "3.225", "1630", "0.353", "0.182", ""],
    ["挥发酚(吨)", "25.477", "20.270", "17.700", "10.861", "11.372", "14.022", "15.994"],
    ["氰化物(吨)", "16.700", "26.100", "22.112", "69.716", "6.512", "11.129", "17.982"],
    ["石油类(吨)", "40.110", "142.860", "96.630", "38.820", "18.600", "6.570", "100.000"],
    ["悬浮物(吨)", "23737", "", "", "", "", "", ""],
    ["五日生化需氧量(吨)", "6056", "", "", "", "", "", ""],
]

PATCH = {
    "title": "1981~1990年部分年份连云港市废水及污染物排放情况表",
    "table_number": "表6-1",
    "page": 401,
    "pages": [401],
    "part": "part02",
    "vol": "上",
    "volume": "上",
    "columns": COLUMNS,
    "rows": ROWS,
    "row_count": len(ROWS),
    "col_count": len(COLUMNS),
    "status": "verified",
    "notes": "已据页级OCR核录：workbench/ocr/paddle_ocr/上/part02/page_0101.txt；并参考 raw 坐标OCR workbench/ocr/raw/上/part02/page_0101.json 与 raw 文本 workbench/table_entries/上/raw/LYG-上-T015_401.txt。原 pages 串入同章后续水质、海洋、大气等表，本条仅保留表6-1所在书页401。源页未见数值处保留空值；总铅1987年 raw 与页级OCR均识别为1630，按源识别保留。",
}


def patch_entry(entry: dict) -> bool:
    if entry.get("table_id") != "LYG-上-T015":
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
