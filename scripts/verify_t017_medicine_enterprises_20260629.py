# -*- coding: utf-8 -*-
"""Verify LYG-中-T017 from raw OCR and mark it deliverable."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
DATA = ROOT / "workbench" / "table_entries" / "中" / "data" / "LYG-中-T017.json"

COLUMNS = [
    "单位名称",
    "企业性质",
    "建厂时间",
    "职工(人)",
    "固定资产原值(万元)",
    "年产值(万元)",
    "利税(万元)",
    "主要产品/生产能力",
]

ROWS = [
    [
        "连云港医疗器械厂",
        "集体",
        "1966.2",
        "305",
        "330",
        "301.00",
        "16.50",
        "医疗用车、系列金属器械橱、各种医疗用床；各种型号救护车1000台",
    ],
    [
        "连云港生化制药厂",
        "全民",
        "1970.5",
        "125",
        "261.20",
        "138.30",
        "19.60",
        "多酶片、胰酶片、ATP片、速效伤风胶囊、复方新诺明混悬剂、小儿感冒冲剂、胰酶、牛黄等；片剂1.5亿片、胶囊0.5亿粒",
    ],
    [
        "连云港市朝阳卫生材料厂",
        "集体",
        "1980",
        "420",
        "1520.00",
        "",
        "19.50(利润)",
        "药用脱脂纱布；年生产炼漂加工脱脂纱布能力2500万米",
    ],
    [
        "连云港医疗设备厂",
        "集体",
        "1981",
        "300",
        "520.00",
        "270.00",
        "62.00",
        "灭菌设备等医疗设备；消毒灭菌器400台",
    ],
]

PATCH = {
    "title": "1990年连云港市医药系统工业企业基本情况表",
    "table_number": "表19-8",
    "page": 1042,
    "pages": [1042],
    "columns": COLUMNS,
    "rows": ROWS,
    "row_count": len(ROWS),
    "col_count": len(COLUMNS),
    "status": "verified",
    "notes": "已据raw OCR回源核录：workbench/table_entries/中/raw/LYG-中-T017_1042.txt。注：简介企业不列入此表。",
}


def patch_entry(entry: dict) -> bool:
    if entry.get("table_id") != "LYG-中-T017":
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
