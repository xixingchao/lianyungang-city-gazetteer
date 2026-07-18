# -*- coding: utf-8 -*-
"""Verify LYG-上-T021 urban residential usable area table."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
DATA = ROOT / "workbench" / "table_entries" / "上" / "data" / "LYG-上-T021.json"

COLUMNS = ["人均住房水平", "全市-户数(户)", "全市-人口(人)", "全市-住宅面积(平方米)", "其中市区-户数(户)", "其中市区-人口(人)", "其中市区-住宅面积(平方米)"]

ROWS = [
    ["合计", "93126", "342336", "3664174", "64081", "227506", "2439969"],
    ["2平方米以下", "98", "462", "683", "45", "208", "341"],
    ["2~4平方米", "1810", "6686", "29095", "1110", "5176", "17397"],
    ["4~6平方米", "7499", "34214", "178252", "5028", "22175", "115307"],
    ["6~8平方米", "14425", "63883", "450224", "10090", "43576", "306628"],
    ["8~10平方米", "18033", "74798", "667253", "12707", "51159", "458355"],
    ["10平方米以上", "51261", "162293", "2338667", "35101", "105212", "1541941"],
]

PATCH = {
    "title": "1985年连云港市城镇居民住宅水平(使用面积)统计表",
    "table_number": "表8-1",
    "page": 465,
    "pages": [465, 466],
    "part": "part02",
    "vol": "上",
    "volume": "上",
    "columns": COLUMNS,
    "rows": ROWS,
    "row_count": len(ROWS),
    "col_count": len(COLUMNS),
    "status": "verified",
    "notes": "已据页级OCR核录：workbench/ocr/paddle_ocr/上/part02/page_0165.txt、page_0166.txt；并参考 raw 文本 workbench/table_entries/上/raw/LYG-上-T021_465.txt。原 pages 串入统计管理章后续多张表，本条收敛为表8-1所在书页465-466；page_0166页末后续正文未并入。",
}


def patch_entry(entry: dict) -> bool:
    if entry.get("table_id") != "LYG-上-T021":
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
