# -*- coding: utf-8 -*-
"""Verify road transport enterprise continuation table T062."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
DATA = ROOT / "workbench" / "table_entries" / "中" / "data" / "LYG-中-T062.json"

COLUMNS = [
    "县区",
    "企业名称",
    "经济性质",
    "地址",
    "成立年份",
    "年末职工数(人)",
    "货车(辆/吨)",
    "挂车(辆/吨)",
    "半挂车(辆/吨)",
]

ROWS = [
    ["赣榆县", "县汽车运输公司", "全民", "新浦通灌路", "1967", "184", "23/115", "18/72", "59/590"],
    ["", "县装卸运输公司", "集体", "新浦盐河桥南", "1956", "332", "24/120", "2/10", "8/82"],
    ["", "县第一汽车运输公司", "全民", "新浦海连路24号", "1973", "150", "15/81", "7/32", "105/1050"],
    ["东海县", "县第二汽车运输公司", "集体", "猴嘴镇", "1956", "124", "16/86", "7/35", "30/292"],
    ["", "县第三汽车运输公司", "集体", "板桥镇", "1954", "102", "2/10", "5/25", "11/108"],
    ["", "县运输公司", "集体", "墟沟镇", "1954", "350", "21/90", "3/15", "27/295"],
    ["", "县汽车运输公司", "全民", "连云港镇", "1970", "142", "10/50", "1/5", "36/395"],
    ["", "县运输公司", "集体", "南城镇", "1978", "410", "14/70", "4/20", "11/110"],
    ["灌云县", "县港务管理处", "全民代集体", "新浦区海连路9号", "", "298", "3/15", "", ""],
    ["", "县联运服务公司", "集体", "伊山镇204国道东侧", "1978", "47", "6/30", "6/30", "3/28"],
    ["", "县第二汽车队", "", "", "1985", "44", "2/10", "2/10", "4/40"],
]

PATCH = {
    "table_id": "LYG-中-T062",
    "title": "1990年连云港市公路运输企业基本情况表（续表）",
    "table_number": "表30-9",
    "page": 1457,
    "pages": [1457],
    "part": "part02",
    "vol": "中",
    "volume": "中",
    "columns": COLUMNS,
    "rows": ROWS,
    "row_count": len(ROWS),
    "col_count": len(COLUMNS),
    "status": "verified",
    "notes": "已据页级OCR回源核录：表题、表号和表头见 workbench/ocr/paddle_ocr/中/part02/page_0036.txt；续表内容见 workbench/ocr/paddle_ocr/中/part02/page_0037.txt，并参考 raw OCR workbench/table_entries/中/raw/LYG-中-T062_1457.txt。原JSON为单列骨架且标题误列为新浦汽车站客运发车情况表；灌云县部分经济性质、成立年份在OCR中纵向粘连，源页未清晰给出的单元格保留空值。",
}


def patch_entry(entry: dict) -> bool:
    if entry.get("table_id") != PATCH["table_id"]:
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
    changed = sum(1 for table in tables if patch_entry(table))
    if changed:
        text = text[: match.start(1)] + json.dumps(tables, ensure_ascii=False) + text[match.end(1) :]
        SITE.write_text(text, encoding="utf-8")
    return changed


def main() -> None:
    print(f"json_files_changed={patch_json()}")
    print(f"site_entries_changed={patch_site()}")


if __name__ == "__main__":
    main()
