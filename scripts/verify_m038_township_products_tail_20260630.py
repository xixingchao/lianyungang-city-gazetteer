# -*- coding: utf-8 -*-
"""Verify township enterprise main products continuation table T038."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
DATA = ROOT / "workbench" / "table_entries" / "中" / "data" / "LYG-中-T038.json"

COLUMNS = ["类别", "产品名称", "计算单位", "合计", "乡办", "村办"]

ROWS = [
    ["", "氮肥(折100%)", "吨", "6663", "6663", ""],
    ["", "磷肥(折100%)", "吨", "10491", "7932", "2559"],
    ["", "钾肥(折100%)", "吨", "192", "192", ""],
    ["", "乳胶手套", "万双", "17", "17", ""],
    ["", "塑料制品", "吨", "4251", "3325", "926"],
    ["", "水泥", "万吨", "19", "19", ""],
    ["", "砖(实物量)", "万块", "146760", "78028", "68732"],
    ["", "瓦(实物量)", "万片", "2428", "1032", "1396"],
    ["", "石灰", "吨", "15871", "8871", "7000"],
    ["", "水泥瓦", "万片", "1032", "1032", ""],
    ["", "水泥预制件", "万立方米", "24", "15", "9"],
    ["工业", "花岗石", "立方米", "985173", "843489", "141684"],
    ["", "大理石", "立方米", "9585", "9585", ""],
    ["", "大理石板材", "平方米", "21730", "19730", "2000"],
    ["", "石膏板", "平方米", "3939", "3939", ""],
    ["", "暖气片", "万片", "5.5", "5.5", ""],
    ["", "铜材", "吨", "2", "2", ""],
    ["", "泵", "台", "4859", "4859", ""],
    ["", "其中：农业用泵", "台", "4859", "4859", ""],
    ["", "手扶拖拉机配套农具", "台", "80", "80", ""],
    ["", "机动脱粒机", "台", "609", "589", "20"],
    ["", "中、小农具", "万件", "153", "130", "23"],
    ["", "其中：铁制小农具", "万件", "139", "119", "20"],
    ["", "木制农具", "万件", "13", "10", "3"],
    ["", "半机械化农具", "部", "1578", "1552", "26"],
    ["", "脱粒机", "部", "1578", "1552", "26"],
    ["", "自行车配件", "万元", "5", "5", ""],
    ["", "工矿配件", "吨", "110", "110", ""],
    ["", "农机具配件", "万件", "10", "10", ""],
    ["", "电线", "万千米", "3", "3", ""],
    ["", "灯具", "万只", "3", "3", ""],
    ["", "电视机", "部", "3516", "3516", ""],
    ["建筑业", "房屋建筑竣工面积", "万平方米", "321", "264", "57"],
    ["交通运输业", "运输量", "万吨", "763", "426", "337"],
    ["农业", "粮食", "吨", "655", "145", "510"],
    ["", "茶叶", "吨", "12", "6", "6"],
    ["", "水果", "吨", "4006", "158", "3848"],
    ["", "牲畜出栏头数", "头", "315", "315", ""],
    ["", "水产品", "吨", "7163", "3454", "3709"],
]

PATCH = {
    "table_id": "LYG-中-T038",
    "title": "1990年连云港市乡镇企业主要产品产量统计表（续表）",
    "table_number": "表27-8",
    "page": 1309,
    "pages": [1309],
    "part": "part01",
    "vol": "中",
    "volume": "中",
    "columns": COLUMNS,
    "rows": ROWS,
    "row_count": len(ROWS),
    "col_count": len(COLUMNS),
    "status": "verified",
    "notes": "已据页级OCR回源核录：表题、表号和表头见 workbench/ocr/paddle_ocr/中/part01/page_0405.txt；续表内容见 workbench/ocr/paddle_ocr/中/part01/page_0406.txt，并参考 raw OCR workbench/table_entries/中/raw/LYG-中-T038_1309.txt。原JSON为单列骨架且标题误列为乡镇企业水泥瓦产量统计表；源页未见数值的单元格保留空值。",
}


def patch_entry(entry: dict) -> bool:
    if entry.get("table_id") != PATCH["table_id"]:
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
    changed = sum(1 for table in tables if patch_entry(table))
    if changed:
        text = text[: match.start(1)] + json.dumps(tables, ensure_ascii=False) + text[match.end(1) :]
        SITE.write_text(text, encoding="utf-8")
    return changed


def main() -> None:
    print(f"json_files_changed={patch_json()}")
    print(f"site_entries_changed={patch_site()}")


if __name__ == "__main__":
    main()
