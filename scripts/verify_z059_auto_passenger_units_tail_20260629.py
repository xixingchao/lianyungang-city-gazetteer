# -*- coding: utf-8 -*-
"""Verify LYG-中-T059 auto passenger units continuation table from raw OCR."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
DATA = ROOT / "workbench" / "table_entries" / "中" / "data" / "LYG-中-T059.json"

COLUMNS = ["单位名称", "地址", "经理人", "开业时间", "拥有车辆", "行驶路线及主要站点", "里程(公里)", "备注"]
ROWS = [
    ["东华汽车公司", "新浦", "李月清", "民国24年", "大客车4辆；小客车5辆", "新浦至伊山镇；新浦至墟沟；新浦至响水口；新浦至青口", "52；67", ""],
    ["淮北汽车行", "板浦", "孙士伟", "", "小客车5辆", "", "", ""],
    ["试新汽车行", "板浦", "丁振泰", "", "小客车4辆", "", "", ""],
    ["笑颐汽车行", "板浦", "姚笔颐", "", "小客车8辆", "", "", ""],
]

PATCH = {
    "title": "民国13~28年（1924~1939年）连云港市汽车客运单位基本情况表（续表）",
    "table_number": "表30-5",
    "page": 1450,
    "pages": [1450],
    "columns": COLUMNS,
    "rows": ROWS,
    "row_count": len(ROWS),
    "col_count": len(COLUMNS),
    "status": "verified",
    "notes": "已据raw OCR回源核录：workbench/table_entries/中/raw/LYG-中-T059_1450.txt；原JSON为单列待录入骨架。本页为表30-5续表，首页见LYG-中-T058；部分开业时间、路线、里程、备注OCR未清晰读出，保留空值，未猜补。",
}


def patch_entry(entry: dict) -> bool:
    if entry.get("table_id") != "LYG-中-T059":
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
