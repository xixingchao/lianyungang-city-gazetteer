# -*- coding: utf-8 -*-
"""Verify LYG-下-T093 Catholic clergy jurisdiction continuation page."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
DATA = ROOT / "workbench" / "table_entries" / "下" / "data" / "LYG-下-T093.json"

COLUMNS = ["年份", "神父", "职务", "管辖范围", "备注"]

ROWS = [
    ["1929", "双国英", "总本堂", "东海、赣榆、灌云", ""],
    ["1929", "利亚诺", "", "沭阳", ""],
    ["1929", "鲁亨利", "", "高流", ""],
    ["1929", "冯奥古斯丁(GAGNONAUGUSTUS)", "", "东海西部、城头", ""],
    ["1930", "双国英", "总本堂", "东海、赣榆、灌云", ""],
    ["1930", "徐保禄(SINJOS-PANLUS)", "副本堂", "东海西部", ""],
    ["1930", "利亚诺", "", "沭阳", ""],
    ["1930", "鲁亨利", "", "高流", ""],
    ["1931", "双国英", "总本堂", "", ""],
    ["1931", "利亚诺", "", "", ""],
    ["1931", "邱若瑟(COUTURIERJOSEPHUS)", "", "城头", ""],
    ["1931", "洛毛利(LANZON(DE)MANRITIUS)", "", "竹墩", ""],
    ["1931", "鲁亨利", "", "", ""],
    ["1932", "双国英", "总本堂", "沭阳", ""],
    ["1932", "利亚诺", "", "城头", ""],
    ["1932", "邱诺瑟", "", "高流", ""],
    ["1932", "蒙雷那德(HOMONRENATUS)", "本堂", "东海东部、赣榆", ""],
    ["1932", "雷类斯(LEBAYONALOISIUS)", "", "灌云", ""],
    ["1932", "蒋慕悌(TSIANGMATTHIAS)", "", "竹墩", ""],
    ["1933~1934", "双国英", "总本堂", "", ""],
    ["1933~1934", "洛毛利", "", "城头", ""],
    ["1933~1934", "雷类斯", "本堂", "", ""],
    ["1933~1934", "利亚诺", "", "沭阳", ""],
    ["1933~1934", "蒙雷那德", "", "高流", ""],
    ["1933~1934", "蒋慕悌", "", "竹墩、桃林、新安镇", ""],
    ["1935", "双国英", "总本堂", "", ""],
    ["1935", "雷类斯", "", "", ""],
    ["1935", "利亚诺", "", "墟沟", ""],
    ["1935", "葛路德维各(GAUCHETLUDOVICUS)", "", "阿湖、城头", ""],
    ["1935", "薛加禄(SIMONSCAROLUS)", "本堂", "沭阳", ""],
    ["1935", "蒋慕悌(蒙雷那德)", "", "竹墩、高流", ""],
    ["1936", "双国英", "总本堂", "", ""],
    ["1936", "雷类斯", "副本堂", "", ""],
    ["1936", "利亚诺", "", "墟沟", ""],
    ["1936", "蔷路注维各", "", "阿湖、城头", ""],
    ["1936", "蒙雷那德", "", "高流", ""],
    ["1936", "薛加禄", "", "沭阳", ""],
    ["1936", "徐宗敏(Z:MICHAEL)", "", "竹墩", ""],
]

PATCH = {
    "title": "1907~1953年连云港市天主教教职人员及其管辖范围表（续表一）",
    "table_number": "表57-1",
    "page": 2700,
    "pages": [2700],
    "part": "part02",
    "vol": "下",
    "volume": "下",
    "columns": COLUMNS,
    "rows": ROWS,
    "row_count": len(ROWS),
    "col_count": len(COLUMNS),
    "status": "verified",
    "notes": "已据页级OCR核录：workbench/ocr/paddle_ocr/下/part02/page_0268.txt；表题和表号依据前页 workbench/ocr/paddle_ocr/下/part02/page_0267.txt；并参考 raw OCR：workbench/table_entries/下/raw/LYG-下-T093_2700.txt。此页仅录入表57-1续页可见记录，同年多名神父的年份向下展开，源页未见职务、管辖范围或备注处保留空值。",
}


def patch_entry(entry: dict) -> bool:
    if entry.get("table_id") != "LYG-下-T093":
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
