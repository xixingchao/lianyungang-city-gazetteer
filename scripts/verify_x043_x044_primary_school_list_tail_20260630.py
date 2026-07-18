# -*- coding: utf-8 -*-
"""Verify LYG-下-T043/T044 primary school list continuation pages."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
DATA_DIR = ROOT / "workbench" / "table_entries" / "下" / "data"

COLUMNS = ["隶属", "校名", "班数(个)", "学生数(人)", "教职工数(人)", "创办年份"]

PATCHES = {
    "LYG-下-T043": {
        "title": "1988年连云港市市区小学一览表（续表三）",
        "table_number": "表50-1",
        "page": 2331,
        "pages": [2331],
        "part": "part01",
        "vol": "下",
        "volume": "下",
        "columns": COLUMNS,
        "rows": [
            ["云台区", "张旐小学", "3", "59", "3", "1950"],
            ["云台区", "东山小学", "7", "180", "15", "1949"],
            ["云台区", "五圩小学", "6", "117", "", "1953"],
            ["云台区", "草地小学", "2", "61", "2", "1984"],
            ["云台区", "盐坨小学", "17", "848", "35", "1965"],
            ["云台区", "猴嘴小学", "13", "522", "30", "1944"],
            ["云台区", "路南小学", "6", "269", "12", "1973"],
            ["云台区", "新光小学", "6", "128", "7", "1935"],
            ["云台区", "大浦小学", "3", "28", "3", "1928"],
            ["云台区", "朱曹小学", "10", "393", "27", "1923"],
            ["云台区", "胜利小学", "8", "274", "10", "1946"],
            ["云台区", "焦庄小学", "6", "207", "", "不详"],
            ["云台区", "范庄小学", "11", "326", "", "不详"],
            ["云台区", "魏安小学", "4", "84", "3", "1952"],
            ["云台区", "金苏小学", "6", "155", "8", "1933"],
            ["云台区", "隔村小学", "12", "359", "16", "1953"],
            ["云台区", "黄东小学", "7", "256", "12", "1946"],
            ["云台区", "山后小学", "2", "23", "", "不详"],
            ["云台区", "江庄小学", "6", "158", "", "1936"],
            ["云台区", "云门小学", "6", "125", "15", "1931"],
            ["云台区", "大村小学", "17", "596", "37", "1921"],
            ["云台区", "新华小学", "8", "272", "12", "1949"],
            ["云台区", "当路小学", "8", "261", "12", "1946"],
            ["云台区", "前云小学", "8", "255", "14", "1928"],
            ["云台区", "小村小学", "7", "199", "10", "不详"],
            ["云台区", "新村小学", "4", "105", "10", "不详"],
            ["云台区", "花果山小学", "2", "25", "2", "不详"],
            ["云台区", "凤凰小学", "7", "223", "9", "不详"],
            ["云台区", "朱麻小学", "10", "398", "12", "不详"],
            ["云台区", "渔湾小学", "6", "176", "8", "不详"],
            ["云台区", "东磊小学", "8", "299", "7", "不详"],
        ],
        "status": "verified",
        "notes": "已据页级OCR核录：workbench/ocr/paddle_ocr/下/part01/page_0360.txt；表题、表号依据前页 workbench/ocr/paddle_ocr/下/part01/page_0357.txt；并参考 raw OCR：workbench/table_entries/下/raw/LYG-下-T043_2331.txt。原条目题名串章为货物吞吐量表，本次更正为教育章表50-1续页；源页未显示的教职工数保留空值。",
    },
    "LYG-下-T044": {
        "title": "1988年连云港市市区小学一览表（续表四）",
        "table_number": "表50-1",
        "page": 2332,
        "pages": [2332],
        "part": "part01",
        "vol": "下",
        "volume": "下",
        "columns": COLUMNS,
        "rows": [
            ["云台区", "山东小学", "11", "406", "11", "不详"],
            ["云台区", "凌州小学", "6", "181", "", "不详"],
            ["云台区", "后关小学", "11", "367", "12", "不详"],
            ["云台区", "虎窝小学", "2", "43", "2", "不详"],
            ["云台区", "关里小学", "12", "506", "34", "1930"],
            ["云台区", "东窑小学", "10", "309", "9", "不详"],
            ["云台区", "丹霞小学", "9", "306", "9", "不详"],
            ["云台区", "诸吾小学", "12", "460", "13", "1949"],
            ["云台区", "龙山小学", "3", "72", "4", "1971"],
            ["云台区", "机关小学", "4", "89", "7", "1983"],
            ["连云区", "墟沟小学", "29", "1860", "72", "1912"],
            ["连云区", "海头湾小学", "11", "544", "27", "1947"],
            ["连云区", "西墅小学", "7", "306", "13", "1930"],
            ["连云区", "院前小学", "6", "221", "13", "不详"],
            ["连云区", "大巷小学", "7", "290", "15", "不详"],
            ["连云区", "南巷学校", "9", "449", "24", "不详"],
            ["连云区", "陶庵学校", "11", "496", "27", "1946"],
            ["连云区", "庙岭小学", "22", "1164", "41", "1947"],
            ["连云区", "砚台小学", "6", "235", "12", "不详"],
            ["连云区", "临海路小学", "21", "1036", "55", "1932"],
            ["连云区", "洞山小学", "6", "198", "12", "不详"],
            ["连云区", "荷花街小学", "12", "505", "22", "1942"],
            ["连云区", "胜利街小学", "9", "362", "21", "1935"],
            ["连云区", "云台小学", "5", "130", "9", "不详"],
            ["连云区", "白果树小学", "6", "231", "13", "不详"],
            ["连云区", "平山小学", "6", "135", "9", "不详"],
            ["连云区", "云山小学", "6", "154", "9", "1949"],
            ["连云区", "李庄小学", "6", "200", "9", "不详"],
            ["连云区", "黄崖小学", "6", "119", "7", "不详"],
            ["连云区", "宿城小学", "12", "378", "22", "1929"],
            ["连云区", "东崖屋小学", "2", "48", "3", "不详"],
        ],
        "status": "verified",
        "notes": "已据页级OCR核录：workbench/ocr/paddle_ocr/下/part01/page_0361.txt；表题、表号依据前页 workbench/ocr/paddle_ocr/下/part01/page_0357.txt；并参考 raw OCR：workbench/table_entries/下/raw/LYG-下-T044_2332.txt。此页为教育章表50-1续页，跨行隶属按源页向下展开；源页未显示的教职工数保留空值。",
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
