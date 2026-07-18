# -*- coding: utf-8 -*-
"""Verify LYG-下-T005 social welfare enterprise table from OCR."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
DATA = ROOT / "workbench" / "table_entries" / "下" / "data" / "LYG-下-T005.json"

COLUMNS = [
    "项目",
    "层级",
    "新浦区",
    "海州区",
    "云台区",
    "连云区",
    "赣榆县",
    "东海县",
    "灌云县",
]

ROWS = [
    ["社会办福利厂企业数(个)", "小计", "34", "22", "9", "10", "43", "23", "38"],
    ["社会办福利厂企业数(个)", "市办", "31", "5", "", "", "", "", ""],
    ["社会办福利厂企业数(个)", "镇办", "", "4", "4", "9", "6", "3", "6"],
    ["社会办福利厂企业数(个)", "乡办", "3", "13", "5", "1", "37", "20", "32"],
    ["社会办福利厂职工总人数(人)", "小计", "703", "407", "125", "80", "1548", "534", "625"],
    ["社会办福利厂其中残废职工人数(人)", "小计", "382", "222", "60", "33", "433", "209", "307"],
    ["社会办福利厂职工人数(人)", "市办", "640", "155", "", "", "", "", ""],
    ["社会办福利厂职工人数(人)", "镇办", "", "76", "36", "62", "144", "60", "115"],
    ["社会办福利厂职工人数(人)", "乡办", "63", "176", "89", "18", "1404", "474", "510"],
    ["社会办福利厂年总产值(万元)", "小计", "3040", "489", "100", "105", "1440", "380", "920"],
    ["社会办福利厂年总产值(万元)", "市办", "2497", "250", "", "", "", "", ""],
    ["社会办福利厂年总产值(万元)", "镇办", "", "112", "55", "89", "127", "37", "185"],
    ["社会办福利厂年总产值(万元)", "乡办", "543", "127", "45", "16", "1313", "343", "735"],
    ["社会办福利厂年利润额(万元)", "小计", "150", "10", "6", "3", "108", "18", "31"],
    ["社会办福利厂年利润额(万元)", "市办", "106", "4", "", "", "", "", ""],
    ["社会办福利厂年利润额(万元)", "镇办", "", "2", "4", "1", "37", "2", "3"],
    ["社会办福利厂年利润额(万元)", "乡办", "44", "4", "2", "2", "71", "16", "28"],
    ["社会办福利商业服务业单位数(个)", "", "7", "4", "", "4", "10", "", ""],
    ["社会办福利商业服务业职工总人数(人)", "", "25", "13", "45", "35", "", "", ""],
    ["社会办福利商业服务业其中残废职工人数(人)", "", "9", "5", "17", "22", "", "", ""],
    ["社会办福利商业服务业年总收入(万元)", "", "156", "99", "3", "60", "25", "", ""],
    ["社会办福利商业服务业年利润额(万元)", "", "", "3", "4", "4", "", "", ""],
    ["街道分散安置“四残”人员数(人)", "", "15", "36", "", "", "", "", ""],
]

PATCH = {
    "title": "1990年连云港市社会举办福利企业情况表",
    "table_number": "表43-9",
    "page": 2014,
    "pages": [2014],
    "part": "part01",
    "vol": "下",
    "volume": "下",
    "columns": COLUMNS,
    "rows": ROWS,
    "row_count": len(ROWS),
    "col_count": len(COLUMNS),
    "status": "verified",
    "notes": "已据页级OCR核录：workbench/ocr/paddle_ocr/下/part01/page_0043.txt，并参考 raw OCR：workbench/table_entries/下/raw/LYG-下-T005_2014.txt。单位按源页为人；社会办福利厂分项按小计与市办、镇办、乡办加总关系校验，源页未见数值处保留空值；页底福利商业服务业和街道分散安置行按OCR可辨列位录入。",
}


def patch_entry(entry: dict) -> bool:
    if entry.get("table_id") != "LYG-下-T005":
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
