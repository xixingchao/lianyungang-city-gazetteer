# -*- coding: utf-8 -*-
"""Verify township-enterprise staff and development-zone planning continuations."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
DATA_DIR = ROOT / "workbench" / "table_entries" / "中" / "data"

PATCHES = {
    "LYG-中-T040": {
        "title": "1988年、1990年连云港市乡(镇)、村企业职工素质情况表（续表）",
        "table_number": "表27-11",
        "page": 1314,
        "pages": [1314],
        "part": "part01",
        "vol": "中",
        "volume": "中",
        "columns": ["项目", "合计1988(人)", "合计1990(人)", "工业企业1988(人)", "工业企业1990(人)", "建筑企业1988(人)", "建筑企业1990(人)"],
        "rows": [
            ["工程技术人员", "4416", "3156", "1298", "1654", "2993", "1141"],
            ["其中：中级以上职称", "122", "162", "61", "102", "61", "56"],
            ["一般职称", "1654", "2798", "785", "1526", "826", "1070"],
            ["聘用人员", "1232", "1602", "461", "762", "699", "670"],
            ["其中：具有技术职称", "271", "253", "76", "159", "186", "45"],
            ["在总计中：技术工人", "898", "1335", "371", "589", "501", "619"],
            ["当年培训人员", "1062", "1183", "568", "750", "385", "291"],
            ["其中：业大、电大", "348", "315", "213", "236", "114", "77"],
            ["中专、技校", "529", "616", "287", "395", "208", "191"],
            ["户口在城镇人员", "6958", "9735", "5060", "7816", "781", "1013"],
        ],
        "status": "verified",
        "notes": "已据页级OCR回源核录：workbench/ocr/paddle_ocr/中/part01/page_0411.txt，并参考 raw OCR：workbench/table_entries/中/raw/LYG-中-T040_1314.txt。表题、表号、单位和列组据前页 workbench/ocr/paddle_ocr/中/part01/page_0410.txt 补定。原JSON误列为乡镇企业及出口产品情况表；本页为表27-11续上表。",
    },
    "LYG-中-T041": {
        "title": "连云港经济技术开发区规划用地平衡表（续表）",
        "table_number": "表28-1",
        "page": 1325,
        "pages": [1325],
        "part": "part01",
        "vol": "中",
        "volume": "中",
        "columns": ["项目", "首期用地(亩)", "首期占%", "近期用地(亩)", "近期占%", "远期用地(亩)", "远期占%"],
        "rows": [
            ["绿化", "146", "13.83", "124", "6.30", "491", "10.91"],
            ["其它", "97", "9.19", "", "", "", ""],
            ["合计", "1056", "100", "1968", "100", "4500", "100"],
        ],
        "status": "verified",
        "notes": "已据页级OCR回源核录：workbench/ocr/paddle_ocr/中/part01/page_0422.txt，并参考 raw OCR：workbench/table_entries/中/raw/LYG-中-T041_1325.txt。表题、表号、单位和列组据前页 workbench/ocr/paddle_ocr/中/part01/page_0421.txt 补定。原JSON误列为乡镇企业及出口产品情况表；本页为表28-1续上表。其它行近期、远期栏源页未见数值，保留空值。",
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
