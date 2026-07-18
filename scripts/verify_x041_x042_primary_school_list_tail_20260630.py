# -*- coding: utf-8 -*-
"""Verify LYG-下-T041/T042 primary school list continuation pages."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
DATA_DIR = ROOT / "workbench" / "table_entries" / "下" / "data"

COLUMNS = ["隶属", "校名", "班数(个)", "学生数(人)", "教职工数(人)", "创办年份"]

PATCHES = {
    "LYG-下-T041": {
        "title": "1988年连云港市市区小学一览表（续表一）",
        "table_number": "表50-1",
        "page": 2329,
        "pages": [2329],
        "part": "part01",
        "vol": "下",
        "volume": "下",
        "columns": COLUMNS,
        "rows": [
            ["新浦区", "通灌路小学", "20", "1231", "60", "1946"],
            ["新浦区", "新生小学", "9", "343", "25", "1958"],
            ["新浦区", "海宁小学", "23", "1361", "57", "1984"],
            ["新浦区", "浦西小学", "11", "552", "29", "1959"],
            ["新浦区", "临洪小学", "11", "454", "32", "1935"],
            ["新浦区", "西筋小学", "8", "398", "25", "1958"],
            ["新浦区", "民主路小学", "13", "654", "35", "1946"],
            ["新浦区", "南极路小学", "13", "664", "41", "1954"],
            ["新浦区", "铁路小学", "6", "126", "16", "不详"],
            ["新浦区", "刘簏小学", "6", "108", "11", "不详"],
            ["新浦区", "浦东小学", "7", "273", "19", "不详"],
            ["新浦区", "幸福路小学", "25", "1410", "63", "1973"],
            ["新浦区", "中大街小学", "20", "1004", "61", "1926"],
            ["新浦区", "砚池小学", "10", "429", "30", "1931"],
            ["新浦区", "蔷薇小学", "10", "363", "28", "1939"],
            ["新浦区", "网疃小学", "10", "396", "28", "1951"],
            ["新浦区", "园林小学", "6", "155", "15", "1961"],
            ["新浦区", "双龙小学", "6", "129", "15", "1952"],
            ["新浦区", "孔望山小学", "6", "161", "12", "1970"],
            ["新浦区", "车站小学", "21", "871", "50", "1951"],
            ["新浦区", "洪门小学", "11", "476", "25", "1951"],
            ["海州区", "锦屏小学", "17", "770", "45", "1951"],
            ["海州区", "刘顶小学", "16", "664", "24", "1928"],
            ["海州区", "桃花小学", "8", "345", "12", "1979"],
            ["海州区", "李圩小学", "8", "314", "9", "1952"],
            ["海州区", "新海小学", "7", "260", "9", "1958"],
            ["海州区", "岗嘴小学", "8", "276", "10", "1951"],
            ["海州区", "狮树小学", "7", "281", "9", "1953"],
            ["海州区", "陶湾小学", "6", "193", "9", "1952"],
            ["海州区", "朐山小学", "7", "237", "9", "1952"],
            ["海州区", "许庄小学", "7", "265", "9", "1960"],
        ],
        "status": "verified",
        "notes": "已据页级OCR核录：workbench/ocr/paddle_ocr/下/part01/page_0358.txt；表题、表号依据前页 workbench/ocr/paddle_ocr/下/part01/page_0357.txt；并参考 raw OCR：workbench/table_entries/下/raw/LYG-下-T041_2329.txt。此页为表50-1续页，跨行隶属按源页向下展开。",
    },
    "LYG-下-T042": {
        "title": "1988年连云港市市区小学一览表（续表二）",
        "table_number": "表50-1",
        "page": 2330,
        "pages": [2330],
        "part": "part01",
        "vol": "下",
        "volume": "下",
        "columns": COLUMNS,
        "rows": [
            ["海州区", "范庄小学", "6", "209", "8", "1952"],
            ["海州区", "李凤小学", "1", "20", "2", "1964"],
            ["海州区", "小海小学", "1", "14", "1", "1955"],
            ["海州区", "酒店小学", "3", "64", "4", "1951"],
            ["海州区", "新坝小学", "18", "800", "40", "1935"],
            ["海州区", "大穆小学", "6", "187", "7", "1951"],
            ["海州区", "大屯小学", "4", "171", "5", "不详"],
            ["海州区", "魏口小学", "8", "229", "11", "1950"],
            ["海州区", "樊庄小学", "6", "171", "7", "1950"],
            ["海州区", "何庄小学", "2", "38", "2", "不详"],
            ["海州区", "四里小学", "6", "137", "9", "1949"],
            ["海州区", "大井小学", "8", "228", "10", "1949"],
            ["海州区", "普安小学", "7", "209", "9", "1949"],
            ["海州区", "朱圩小学", "4", "88", "4", "1957"],
            ["海州区", "小荡小学", "6", "166", "10", "1950"],
            ["海州区", "王傅小学", "4", "100", "5", "1954"],
            ["海州区", "沙杭小学", "7", "196", "11", "1953"],
            ["海州区", "墙框小学", "5", "120", "4", "1961"],
            ["海州区", "武圩小学", "8", "208", "7", "1950"],
            ["海州区", "陈户小学", "7", "183", "8", "1949"],
            ["海州区", "孙庄小学", "1", "23", "2", "1972"],
            ["海州区", "新建小学", "1", "13", "9", "1982"],
            ["云台区", "南城小学", "23", "1011", "53", "1912"],
            ["云台区", "新县小学", "21", "854", "50", "1909"],
            ["云台区", "西山小学", "8", "276", "11", "1944"],
            ["云台区", "朝阳小学", "7", "228", "10", "1945"],
            ["云台区", "韩李小学", "7", "251", "9", "1958"],
            ["云台区", "张庄小学", "6", "174", "9", "1949"],
            ["云台区", "沙集小学", "7", "205", "9", "1953"],
            ["云台区", "马山小学", "6", "96", "8", "1958"],
            ["云台区", "板桥小学", "10", "409", "23", "1948"],
        ],
        "status": "verified",
        "notes": "已据页级OCR核录：workbench/ocr/paddle_ocr/下/part01/page_0359.txt；表题、表号依据前页 workbench/ocr/paddle_ocr/下/part01/page_0357.txt；并参考 raw OCR：workbench/table_entries/下/raw/LYG-下-T042_2330.txt。原条目题名串章为铁路专线分布表，本次更正为教育章表50-1续页；跨行隶属按源页向下展开。",
    },
}

for patch in PATCHES.values():
    patch["row_count"] = len(patch["rows"])
    patch["col_count"] = len(patch["columns"])


def patch_entry(entry: dict) -> bool:
    table_id = entry.get("table_id")
    if table_id not in PATCHES:
        return False
    changed = False
    for key, value in PATCHES[table_id].items():
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
