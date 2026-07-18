# -*- coding: utf-8 -*-
"""Verify LYG-中-T090 leasing project table from raw OCR."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
DATA = ROOT / "workbench" / "table_entries" / "中" / "data" / "LYG-中-T090.json"

COLUMNS = ["起租年份", "本市企业名称", "合作企业名称", "项目内容", "金额(万美元)", "期限"]
ROWS = [
    ["1984", "连云港市协作办公室", "日本东方租赁公司", "轿车、面包车", "28.90", "2年"],
    ["1986", "连云港市色织厂", "上海太平洋租赁有限公司", "浆染联合机", "24.80", "1.5年"],
    ["1986", "连云港市造纸厂", "上海联合租赁有限公司", "香巾纸折叠机", "5.00", "2年"],
    ["1986", "连云港市罐头厂", "上海太平洋租赁有限公司", "午餐肉装罐机", "31.40", ""],
    ["1987", "连云港市造纸厂", "", "", "5.40", "6年"],
    ["1987", "连云港连利水表有限公司", "", "水表生产设备", "625.00", ""],
]

PATCH = {
    "title": "1984~1987年连云港市租赁项目一览表",
    "table_number": "表35-7",
    "page": 1621,
    "pages": [1621],
    "columns": COLUMNS,
    "rows": ROWS,
    "row_count": len(ROWS),
    "col_count": len(COLUMNS),
    "status": "verified",
    "notes": "已据raw OCR回源核录：workbench/table_entries/中/raw/LYG-中-T090_1621.txt；原JSON为单列待录入骨架。OCR中1986年罐头厂、1987年造纸厂和连利水表公司部分合作企业/项目内容/期限栏未清晰读出，保留空值，未猜补。",
}


def patch_entry(entry: dict) -> bool:
    if entry.get("table_id") != "LYG-中-T090":
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
