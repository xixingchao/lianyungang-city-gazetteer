# -*- coding: utf-8 -*-
"""Verify LYG-下-T060 secondary school basic statistics table."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
DATA = ROOT / "workbench" / "table_entries" / "下" / "data" / "LYG-下-T060.json"

COLUMNS = [
    "类别",
    "地区",
    "学校数(所)",
    "毕业生数初中(人)",
    "毕业生数高中(人)",
    "招生数初中(人)",
    "招生数高中(人)",
    "在校学生数初中(人)",
    "在校学生数高中(人)",
    "教职员工数合计(人)",
    "教职员工数其中专任教师(人)",
]

ROWS = [
    ["中学", "合计", "253", "35870", "7012", "45557", "6544", "126040", "19370", "10380", "8182"],
    ["中学", "市区", "29", "7005", "1696", "8056", "1772", "25157", "5126", "1890", "1890"],
    ["中学", "赣榆县", "90", "9864", "1582", "12380", "1518", "34884", "4717", "2952", "2249"],
    ["中学", "东海县", "70", "10468", "1914", "13354", "1989", "37281", "5515", "2743", "2137"],
    ["中学", "灌云县", "64", "8533", "1820", "11767", "1265", "28718", "4012", "2795", "1906"],
    ["农(职)业中学", "合计", "28", "106", "3005", "100", "3575", "291", "11139", "920", "648"],
    ["农(职)业中学", "市区", "7", "", "1364", "", "1257", "", "4060", "389", "251"],
    ["农(职)业中学", "赣榆县", "9", "", "828", "", "868", "", "2477", "176", "147"],
    ["农(职)业中学", "东海县", "7", "106", "505", "100", "754", "", "1861", "176", "133"],
    ["农(职)业中学", "灌云县", "5", "", "308", "", "696", "", "1634", "179", "117"],
    ["中技", "合计", "4", "", "401", "", "600", "", "1408", "306", "157"],
    ["中技", "市区", "4", "", "401", "", "600", "", "1408", "306", "157"],
    ["中专", "合计", "6", "", "1436", "", "1303", "", "4330", "417", ""],
    ["中专", "市区", "6", "", "1436", "", "1303", "", "4330", "417", ""],
    ["中师", "合计", "2", "", "558", "", "381", "", "1288", "", ""],
    ["中师", "市区", "2", "", "558", "", "381", "", "1288", "", ""],
]

PATCH = {
    "title": "1990年连云港市中等学校基本情况表",
    "table_number": "表50-16",
    "page": 2360,
    "pages": [2360],
    "part": "part01",
    "vol": "下",
    "volume": "下",
    "columns": COLUMNS,
    "rows": ROWS,
    "row_count": len(ROWS),
    "col_count": len(COLUMNS),
    "status": "verified",
    "notes": "已据页级OCR核录：workbench/ocr/paddle_ocr/下/part01/page_0389.txt，并参考 raw OCR：workbench/table_entries/下/raw/LYG-下-T060_2360.txt。原条目题名串章为汽车站表，本次回源更正为教育章表50-16；源页未见数值的初中/高中或专任教师单元格保留空值，不按合计反推。",
}


def patch_entry(entry: dict) -> bool:
    if entry.get("table_id") != "LYG-下-T060":
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
