# -*- coding: utf-8 -*-
"""Verify LYG-下-T094/T095 Catholic clergy jurisdiction continuation pages."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
DATA_DIR = ROOT / "workbench" / "table_entries" / "下" / "data"

COLUMNS = ["年份", "神父", "职务", "管辖范围", "备注"]

PATCHES = {
    "LYG-下-T094": {
        "title": "1907~1953年连云港市天主教教职人员及其管辖范围表（续表二）",
        "table_number": "表57-1",
        "page": 2701,
        "pages": [2701],
        "part": "part02",
        "vol": "下",
        "volume": "下",
        "columns": COLUMNS,
        "rows": [
            ["1937", "双国英", "总本堂、中心校长", "", "此时天主教会成立中心小学"],
            ["1937", "雷类斯", "副本堂、副校长", "墟沟", ""],
            ["1937", "利亚诺", "", "城头", ""],
            ["1937", "葛路德维各", "", "高流", ""],
            ["1937", "蒙雷那德", "", "沙河", ""],
            ["1937", "赖若汗(DELALANGREREJOANNES)", "", "", ""],
            ["1938", "双国英", "总本堂、校长", "", ""],
            ["1938", "雷类斯", "", "", ""],
            ["1938", "利亚诺", "副本堂、副校长", "墟沟", ""],
            ["1938", "葛路德维各", "", "城头", ""],
            ["1938", "蒙雷那德", "", "高流", ""],
            ["1938", "赖若汗", "", "沙河", ""],
            ["1939~1941", "洛毛利", "总本堂、校长", "", ""],
            ["1939~1941", "雷类斯", "", "新浦", ""],
            ["1939~1941", "利亚诺", "副本堂、副校长", "墟沟", ""],
            ["1939~1941", "华青克(FALEYMARCUSA)", "", "竹墩", ""],
            ["1939~1941", "葛路德维各", "", "阿湖、城头", ""],
            ["1939~1941", "沈安芳", "", "沙河", ""],
            ["1942", "洛毛利", "总本堂、校长", "", ""],
            ["1942", "伏恩德望(CESBRONLAVANSTEPHANUS)", "", "新浦", ""],
            ["1942", "利亚诺", "副本堂、副校长", "墟沟", ""],
            ["1942", "华玛尔各", "", "竹墩", ""],
            ["1942", "蒙蕾那德", "", "城头", ""],
            ["1942", "沈安芳", "", "沙河", ""],
            ["1943", "赖若翰(DELALARGEREJOANNES)", "总本堂、校长", "", ""],
            ["1943", "陈天宝(ZENLUCAS)", "", "新浦、东海", ""],
            ["1943", "吴应枫(ONALOISIUS)", "", "", ""],
            ["1943", "利亚诺", "副本堂、副校长", "墟沟", ""],
            ["1943", "华玛尔各", "", "竹墩", ""],
            ["1943", "龚若瑟(GONCALVESJOS)", "", "马厂(沭阳)", ""],
            ["1943", "蒙雷那德", "", "高流", ""],
            ["1943", "沈安芳", "", "沙河", ""],
            ["1943", "张孝松(TSAMAJOSEPHUS)", "", "城头", ""],
            ["1944", "蒙雷那德", "总本堂、校长", "新浦", ""],
            ["1944", "班伯多禄(PELLIARDPETRUS)", "", "沭阳", ""],
            ["1944", "吴应枫", "副本堂、副校长", "墟沟", ""],
            ["1944", "陆起龙(LOHMATTHOEUS)", "", "", ""],
            ["1944", "贝河勿略(PERREZFR-XAVERIUS)", "", "竹墩", ""],
            ["1944", "张登俨(TSANGBERCHMANS)", "", "高流", ""],
            ["1944", "沈安芳", "", "沙河", ""],
            ["1944", "张孝松", "", "城头", ""],
        ],
        "status": "verified",
        "notes": "已据页级OCR核录：workbench/ocr/paddle_ocr/下/part02/page_0269.txt；表题和表号依据 workbench/ocr/paddle_ocr/下/part02/page_0267.txt；并参考 raw 坐标 OCR：workbench/ocr/raw/下/part02/page_0269.json 与 raw 文本 workbench/table_entries/下/raw/LYG-下-T094_2701.txt。此页仅录入表57-1续页可见记录，同年多名神父的年份向下展开，源页未见单元格内容处保留空值。",
    },
    "LYG-下-T095": {
        "title": "1907~1953年连云港市天主教教职人员及其管辖范围表（续表三）",
        "table_number": "表57-1",
        "page": 2702,
        "pages": [2702],
        "part": "part02",
        "vol": "下",
        "volume": "下",
        "columns": COLUMNS,
        "rows": [
            ["1945~1946", "和基利斯当(CHRISTIANUSHOMO)", "总本堂、校长", "", ""],
            ["1945~1946", "陆起龙", "", "", ""],
            ["1945~1946", "丁斐(TINGPHILIPPNS)", "副本堂、副校长", "新浦", ""],
            ["1945~1946", "唐西满(DANGSIMON)", "修士事务主任", "", ""],
            ["1945~1946", "蒙雷那德", "", "墟沟", ""],
            ["1945~1946", "班伯多禄", "", "沭阳", ""],
            ["1945~1946", "贝沙勿略", "", "竹墩", ""],
            ["1945~1946", "沈安芳", "", "沙河", ""],
            ["1945~1946", "张登俨", "", "高流", ""],
            ["1945~1946", "张孝松", "", "阿湖、城头", ""],
            ["1947", "和基利斯当", "总本堂、校长", "", ""],
            ["1947", "贝沙勿略", "副校长", "东海", ""],
            ["1947", "丁斐", "", "新浦、墟沟", ""],
            ["1947", "徐依纳爵(ZILGNATIUS)", "中心校主任、语文教师", "东海", ""],
            ["1947", "张登俨", "", "沭阳", ""],
            ["1947", "沈安芳", "", "沙河", ""],
            ["1947", "禄沙勿略(ROBERTXAVERIUS)", "", "高流", ""],
            ["1947", "张孝松", "", "城头、竹墩", ""],
            ["1947", "张景超", "", "城头", ""],
            ["1948", "傅雅各(JACOBUSDELEFFE)", "总本堂校长", "", ""],
            ["1948", "马怀仁(MARXJOSEPHUS)", "", "墟沟、连云港", ""],
            ["1948", "贝沙勿略", "副校长", "东海、赣榆", ""],
            ["1948", "丁斐", "", "新浦", "自冷修会主任"],
            ["1948", "毕沙勿略(BUREKLERFR-XAVER)", "副本堂", "沭阳", ""],
            ["1948", "史多明我(STEINERDOMINICUS)", "副本堂、英文教师", "", ""],
            ["1948", "司路加(STOFFELLNCAS)", "副本堂", "", ""],
            ["1948", "李保禄(LIPANLUS)", "学生监督、语文教师", "", ""],
            ["1948", "徐依纳爵", "教师", "", ""],
            ["1949", "傅雅各", "总本堂、校长", "新浦、城头、竹墩", ""],
            ["1949", "", "", "高流", ""],
            ["1949", "马怀仁", "", "墟沟、连云港", ""],
            ["1949", "贝锦章", "", "海州", ""],
            ["1950~1952", "黄道生", "总本堂、校长", "", ""],
            ["1950~1952", "李新生", "", "海州", ""],
            ["1950~1952", "阎维道", "", "墟沟", ""],
            ["1950~1952", "陈惟本", "", "新浦", ""],
            ["1953", "阎维道", "", "新浦", ""],
        ],
        "status": "verified",
        "notes": "已据页级OCR核录：workbench/ocr/paddle_ocr/下/part02/page_0270.txt；表题和表号依据 workbench/ocr/paddle_ocr/下/part02/page_0267.txt；并参考 raw 坐标 OCR：workbench/ocr/raw/下/part02/page_0270.json 与 raw 文本 workbench/table_entries/下/raw/LYG-下-T095_2702.txt。此页仅录入表57-1续页可见记录，同年多名神父的年份向下展开，源页未见单元格内容处保留空值。",
    },
}

for patch in PATCHES.values():
    patch["row_count"] = len(patch["rows"])
    patch["col_count"] = len(COLUMNS)


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
        data_path = DATA_DIR / f"{table_id}.json"
        data = json.loads(data_path.read_text(encoding="utf-8"))
        if patch_entry(data):
            data_path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
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
