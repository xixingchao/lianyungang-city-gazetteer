# -*- coding: utf-8 -*-
"""Verify LYG-中-T058 auto passenger units table from raw OCR."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
DATA = ROOT / "workbench" / "table_entries" / "中" / "data" / "LYG-中-T058.json"

COLUMNS = ["单位名称", "地址", "经理人", "开业时间", "拥有车辆", "行驶路线及主要站点", "里程(公里)", "备注"]
ROWS = [
    ["孙东记汽车公司", "青口", "孙东文", "民国14年", "4辆", "马厂至新浦；后经营青口至海头、青口至欢墩埠两线客运", "", "民国28年后经营青口至海头、青口至欢墩埠两线客运"],
    ["普益汽车公司", "新浦", "陈旦元、朱连贵", "民国17年2月", "大客车3辆；小客车4辆；货车1辆", "起新浦，经南城、板浦、小伊山、仙桥、大伊山、夹山口，至伊山镇西门", "52", "民国24年并入东华汽车公司"],
    ["新大汽车公司", "新浦", "", "民国17年9月", "4辆", "新浦至大浦", "", ""],
    ["三益汽车公司", "沭城", "谢仲舫", "民国22年", "大客车4辆；小客车5辆；货车1辆", "起准阴，经五里庄、钱集、沭阳、五集、龙直至新浦", "179", "民国24年客线遭水毁，改道板浦，经同兴、龙王口、杨集至东坎"],
    ["连云汽车公司", "板浦", "孙笃生", "民国22年", "大客车6辆；小客车8辆", "起板浦，经彭渡、沙行、徐跳、顺兴、杨集、响水口至东坎", "", ""],
    ["淮北盐务稽核分所", "板浦", "", "民国24年", "", "板浦至柘汪；板浦至堆沟；陈港至响水口", "", ""],
]

PATCH = {
    "title": "民国13~28年（1924~1939年）连云港市汽车客运单位基本情况表",
    "table_number": "表30-5",
    "page": 1449,
    "pages": [1449],
    "columns": COLUMNS,
    "rows": ROWS,
    "row_count": len(ROWS),
    "col_count": len(COLUMNS),
    "status": "verified",
    "notes": "已据raw OCR回源核录：workbench/table_entries/中/raw/LYG-中-T058_1449.txt；原JSON为单列待录入骨架。部分单位地址、经理人、里程、车辆数OCR未清晰读出，保留空值，未猜补。",
}


def patch_entry(entry: dict) -> bool:
    if entry.get("table_id") != "LYG-中-T058":
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
