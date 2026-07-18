# -*- coding: utf-8 -*-
"""Verify table 46-12 welfare income and expense continuation page."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
DATA_DIR = ROOT / "workbench" / "table_entries" / "下" / "data"

COLUMNS = [
    "项目",
    "1984年国家机关、党派团体",
    "1984年全民所有制事业单位",
    "1985年国家机关、党派团体",
    "1985年全民所有制事业单位",
]

PATCHES = {
    "LYG-下-T027": {
        "title": "1984年、1985年连云港市(含三县)国家机关、党派、团体、全民事业单位福利费收支情况统计表（续表）",
        "table_number": "表46-12",
        "page": 2183,
        "pages": [2183],
        "columns": COLUMNS,
        "rows": [
            ["合计", "253049.56", "1029770.75", "239975", "671704"],
            ["补助人数(人)", "5589", "14440", "5811", "13651"],
            ["支出-个人部分-款数", "114592.87", "273705.86", "120543", "280633"],
            ["支出-集体福利补贴-小计", "138456.69", "756064.89", "109432", "391071"],
            ["支出-集体福利补贴-补助集体福利事业的部分", "44012.30", "199411.15", "41678", "164568"],
            ["支出-集体福利补贴-家属统筹医疗补贴", "13846.66", "115140.32", "16861", "78256"],
            ["支出-集体福利补贴-慰问病号补贴", "10326.58", "23481.03", "11737", "21230"],
            ["支出-集体福利补贴-集体福利设施补贴", "10679.27", "194123.3", "8541", "20909"],
            ["支出-集体福利补贴-计划生育补贴", "34442.95", "51332.57", "12348", "47639"],
            ["支出-集体福利补贴-其它补贴", "25148.93", "172546.49", "18267", "58469"],
        ],
        "status": "verified",
        "notes": "已据页级OCR回源核录：workbench/ocr/paddle_ocr/下/part01/page_0212.txt，并参考 raw OCR：workbench/table_entries/下/raw/LYG-下-T027_2183.txt。表题、表号和列组依据前页 workbench/ocr/paddle_ocr/下/part01/page_0211.txt；本页为表46-12续上表。四个数值列按 raw OCR 坐标核定为 1984年国家机关、党派团体，1984年全民所有制事业单位，1985年国家机关、党派团体，1985年全民所有制事业单位。注释见源页：1984年度福利费按每人每月1.6元提取，1985年按工资总额2.5%提取；1984年国家机关、党派团体超支22391.8元，全民所有制事业单位超支166938.32元；1985年国家机关、党派团体超支13264元，全民所有制事业单位超支18326元。",
    }
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
