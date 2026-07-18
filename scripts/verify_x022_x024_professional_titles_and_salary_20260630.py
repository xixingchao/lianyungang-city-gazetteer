# -*- coding: utf-8 -*-
"""Verify table 46-6 tail and table 46-7 salary pages."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
DATA_DIR = ROOT / "workbench" / "table_entries" / "下" / "data"

PROFESSIONAL_COLUMNS = ["系列", "合计", "未评聘", "高级", "中级", "初级"]
SALARY_COLUMNS = ["职别", "人数", "每人月支数", "每月共支数", "全年合计数"]

PATCHES = {
    "LYG-下-T022": {
        "title": "1990年底连云港市专业干部技术职务情况表（续表）",
        "table_number": "表46-6",
        "page": 2174,
        "pages": [2174],
        "columns": PROFESSIONAL_COLUMNS,
        "rows": [
            ["工艺美术", "29", "2", "7", "17", "3"],
            ["体育", "41", "2", "18", "9", "12"],
            ["艺术", "20", "13", "5", "2", ""],
        ],
        "status": "verified",
        "notes": "已据页级OCR回源核录：workbench/ocr/paddle_ocr/下/part01/page_0203.txt，并参考 raw OCR：workbench/table_entries/下/raw/LYG-下-T022_2174.txt。表题、表号、单位和列组依据前页 workbench/ocr/paddle_ocr/下/part01/page_0202.txt；本页为表46-6续上表，单位为人。艺术行末列源页/OCR未见数值，保留空值。注释见源页：不含驻连部、省属单位专业人员数；不含集体所有制单位专业人员数2121人。",
    },
    "LYG-下-T023": {
        "title": "民国36年连云市政府员役俸给费表",
        "table_number": "表46-7",
        "page": 2175,
        "pages": [2175],
        "columns": SALARY_COLUMNS,
        "rows": [
            ["市长", "1", "680", "680", "8160"],
            ["秘书长", "1", "520", "520", "6240"],
            ["秘书", "4", "400", "1600", "19200"],
            ["科长", "7", "400", "2800", "33600"],
        ],
        "status": "verified",
        "notes": "已据页级OCR回源核录：workbench/ocr/paddle_ocr/下/part01/page_0204.txt，并参考 raw OCR：workbench/table_entries/下/raw/LYG-下-T023_2175.txt。表号为表46-7，单位为元；原JSON误列为化工产品产量统计表，本轮按源页纠正。",
    },
    "LYG-下-T024": {
        "title": "民国36年连云市政府员役俸给费表（续表）",
        "table_number": "表46-7",
        "page": 2176,
        "pages": [2176],
        "columns": SALARY_COLUMNS,
        "rows": [
            ["会计主任", "1", "400", "400", "4800"],
            ["人事主任", "1", "400", "400", "4800"],
            ["参事", "2", "400(1人); 380(1人)", "780", "9360"],
            ["专员", "3", "400(1人); 340(1人); 320(1人)", "1060", "12720"],
            ["技正", "4", "400(1人); 360(2人); 340(1人)", "1460", "17520"],
            ["视察", "4", "400(1人); 360(1人); 200(2人)", "1160", "13920"],
            ["督学", "2", "380(1人); 340(1人)", "720", "8640"],
            ["会计员", "3", "180(1人); 160(1人); 140(1人)", "480", "5760"],
            ["统计员", "1", "180", "180", "2160"],
            ["一级科员", "10", "180", "1800", "21600"],
            ["二级科员", "15", "160", "2400", "28800"],
            ["三级科员", "15", "140", "2100", "25200"],
            ["一级办事员", "10", "120", "1200", "14400"],
            ["二级办事员", "10", "80", "800", "9600"],
            ["技士", "6", "180", "1080", "12960"],
            ["技佐", "6", "140", "840", "10080"],
            ["一级雇员", "10", "80", "800", "9600"],
            ["二级雇员", "10", "40", "400", "4800"],
            ["公役", "70", "30(2人); 20(20人); 8(48人)", "844", "10128"],
            ["总计", "196", "9258", "24504", "294048"],
        ],
        "status": "verified",
        "notes": "已据页级OCR回源核录：workbench/ocr/paddle_ocr/下/part01/page_0205.txt，并参考 raw OCR：workbench/table_entries/下/raw/LYG-下-T024_2176.txt。本页为表46-7续上表，单位为元。多行每人月支数按源页合并为分号分隔。二级雇员全年合计数 raw/page OCR 漏识末位0，按页图复核及 40×10×12 算术关系核为4800。",
    },
}

for patch in PATCHES.values():
    patch["row_count"] = len(patch["rows"])
    patch["col_count"] = len(patch["columns"])


def patch_entry(entry: dict) -> bool:
    patch = PATCHES.get(entry.get("table_id"))
    if not patch:
        return False
    changed = False
    for key, value in patch.items():
        if entry.get(key) != value:
            entry[key] = value
            changed = True
    return changed


def patch_json() -> int:
    changed = 0
    for table_id in PATCHES:
        path = DATA_DIR / f"{table_id}.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        if patch_entry(data):
            path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            changed += 1
    return changed


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
