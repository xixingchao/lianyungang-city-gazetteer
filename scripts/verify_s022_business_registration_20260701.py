# -*- coding: utf-8 -*-
"""Verify LYG-上-T022 business registration table."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
DATA = ROOT / "workbench" / "table_entries" / "上" / "data" / "LYG-上-T022.json"

COLUMNS = ["行业", "1982", "1983", "1984", "1985", "1986", "1987", "1988", "1989", "1990"]

ROWS = [
    ["合计", "6873", "7470", "9270", "12183", "12742", "14317", "15602", "15216", "13329"],
    ["农、牧、渔、水利业", "", "", "", "45", "50", "32", "125", "133", "126"],
    ["工业", "1570", "1731", "2196", "3352", "3630", "4066", "4351", "4336", "3852"],
    ["建筑业", "143", "160", "202", "277", "307", "298", "304", "305", "298"],
    ["交通运输邮电通讯业", "201", "223", "260", "323", "336", "395", "420", "417", "397"],
    ["商业、公共饮食业、物资供销和仓储业", "4227", "4505", "5759", "7214", "7304", "8162", "8892", "8474", "7271"],
    ["公用事业、房地产管理", "732", "851", "853", "853", "876", "983", "1055", "1055", "903"],
    ["居民服务和咨询服务业", "", "", "", "", "", "", "", "", ""],
    ["卫生、体育和社会福利事业", "", "", "", "3", "3", "6", "6", "7", "4"],
    ["教育、文化艺术和广播电视事业", "", "", "", "86", "84", "97", "113", "109", "101"],
    ["科学研究和综合技术服务事业", "", "", "", "3", "6", "9", "11", "18", "22"],
    ["金融保险业", "", "", "", "6", "142", "253", "279", "310", "303"],
    ["其它行业", "", "", "", "21", "4", "16", "46", "52", "52"],
]

PATCH = {
    "title": "1982~1990年连云港市工商企业登记基本情况统计表",
    "table_number": "表8-12",
    "page": 493,
    "pages": [493],
    "part": "part02",
    "vol": "上",
    "volume": "上",
    "columns": COLUMNS,
    "rows": ROWS,
    "row_count": len(ROWS),
    "col_count": len(COLUMNS),
    "status": "verified",
    "notes": "已据页级OCR核录：workbench/ocr/paddle_ocr/上/part02/page_0193.txt；并参考 raw 坐标 OCR：workbench/ocr/raw/上/part02/page_0193.json 与 raw 文本 workbench/table_entries/上/raw/LYG-上-T022_493.txt。表8-12实际位于 page_0193，本条仅录入该表，后续表8-13未并入；多行行业名按同列位置合并，源页未见数值处保留空值。",
}


def patch_entry(entry: dict) -> bool:
    if entry.get("table_id") != "LYG-上-T022":
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
