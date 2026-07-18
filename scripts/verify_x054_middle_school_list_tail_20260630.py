# -*- coding: utf-8 -*-
"""Verify LYG-下-T054 ordinary middle school list continuation page."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
DATA_DIR = ROOT / "workbench" / "table_entries" / "下" / "data"

COLUMNS = [
    "隶属",
    "校名",
    "创办年份",
    "班数(个)",
    "学生数(人)",
    "教职工数小计(人)",
    "专任教师(人)",
]

PATCHES = {
    "LYG-下-T054": {
        "title": "1990年连云港市普通中学一览表（续表一）",
        "table_number": "表50-11",
        "page": 2350,
        "pages": [2350],
        "part": "part01",
        "vol": "下",
        "volume": "下",
        "columns": COLUMNS,
        "rows": [
            ["新浦区", "新浦中学", "1957", "38", "2197", "178", "128"],
            ["新浦区", "陇东中学", "1964", "19", "975", "147", "111"],
            ["新浦区", "延安中学", "1971", "29", "1450", "140", "112"],
            ["新浦区", "浦东中学", "1973", "14", "724", "66", "51"],
            ["新浦区", "临洪中学", "1982", "24", "1080", "98", "80"],
            ["新浦区", "海宁中学", "1987", "12", "588", "39", "33"],
            ["海州区", "锦屏中学", "1958", "13", "602", "84", "59"],
            ["海州区", "新坝中学", "1958", "25", "1105", "82", "58"],
            ["海州区", "幸福路中学", "1974", "9", "433", "65", "38"],
            ["海州区", "蔷薇中学", "1975", "31", "1503", "125", "90"],
            ["海州区", "朐山中学", "1976", "10", "603", "41", "33"],
            ["海州区", "朝阳中学", "1956", "17", "964", "68", "53"],
            ["云台区", "南城中学", "1958", "11", "534", "44", "29"],
            ["云台区", "猴嘴中学", "1958", "27", "1262", "106", "71"],
            ["云台区", "云台中学", "1970", "19", "900", "54", "38"],
            ["云台区", "花果山中学", "1972", "14", "781", "48", "40"],
            ["云台区", "中云中学", "1975", "14", "680", "43", "36"],
            ["云台区", "板桥中学", "1964", "7", "356", "27", "21"],
            ["连云区", "墟沟中学", "1956", "39", "2194", "169", "95"],
            ["连云区", "连云中学", "1958", "23", "1130", "102", "68"],
            ["连云区", "云山中学", "1965", "7", "351", "26", "21"],
            ["连云区", "海滨中学", "1975", "28", "1600", "107", "100"],
            ["连云区", "宿城中学", "1985", "6", "257", "18", "16"],
            ["连云区", "连岛初中", "1985", "5", "207", "16", "15"],
            ["连云区", "高公岛学校", "1969", "3", "112", "12", "12"],
            ["连云区", "东港中学", "1989", "8", "400", "32", "27"],
            ["赣榆县", "赣榆县中学", "1923", "30", "1751", "170", "112"],
            ["赣榆县", "青口一中", "1976", "18", "1111", "73", "59"],
            ["赣榆县", "青口二中", "1977", "17", "1074", "72", "53"],
            ["赣榆县", "赣马中学", "1958", "12", "849", "71", "49"],
            ["赣榆县", "海头中学", "1957", "14", "751", "62", "55"],
            ["赣榆县", "城头中学", "1956", "20", "1210", "95", "68"],
            ["赣榆县", "沙河中学", "1957", "19", "1154", "72", "56"],
            ["赣榆县", "城南中学", "1971", "9", "790", "53", "44"],
            ["赣榆县", "厉庄中学", "1956", "19", "1189", "90", "69"],
            ["赣榆县", "石桥中学", "1958", "12", "642", "52", "37"],
            ["赣榆县", "班庄中学", "1972", "13", "730", "38", "38"],
        ],
        "status": "verified",
        "notes": "已据页级OCR核录：workbench/ocr/paddle_ocr/下/part01/page_0379.txt；表题、表号和表头依据前页 workbench/ocr/paddle_ocr/下/part01/page_0378.txt；并参考 raw 文本 workbench/table_entries/下/raw/LYG-下-T054_2350.txt。原条目题名串章为船舶检验统计表，本次更正为教育章表50-11续页；跨行隶属按源页向下展开。",
    }
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
