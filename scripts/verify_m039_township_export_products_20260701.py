# -*- coding: utf-8 -*-
"""Verify LYG-中-T039 township enterprise export products table."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
DATA = ROOT / "workbench" / "table_entries" / "中" / "data" / "LYG-中-T039.json"

COLUMNS = [
    "数量概况",
    "年份",
    "合计",
    "化工",
    "机电",
    "矿产品",
    "轻工业品",
    "食品",
    "土产品",
    "畜产品",
    "纺织品",
    "丝织品",
    "服装",
    "工艺美术品",
    "其它",
]

ROWS = [
    ["企业单位数(个)", "1988", "106", "4", "2", "1", "5", "25", "3", "18", "2", "1", "3", "18", "24"],
    ["企业单位数(个)", "1990", "104", "2", "7", "5", "5", "24", "3", "6", "5", "1", "6", "20", "20"],
    ["企业人数(人)", "1988", "9079", "187", "198", "20", "2247", "1040", "85", "614", "303", "37", "352", "2268", "1728"],
    ["企业人数(人)", "1990", "8927", "167", "597", "242", "1932", "1059", "78", "238", "995", "12", "1437", "1110", "1060"],
    ["出口产品生产总值(按当年价计算)(万元)", "1988", "9334", "176", "94", "65", "682", "4509", "491", "128", "155", "12", "153", "420", "2449"],
    ["出口产品生产总值(按当年价计算)(万元)", "1990", "13015", "92", "550", "891", "2685", "4024", "382", "101", "313", "12", "1995", "611", "1359"],
    ["出口产品金额(万元)", "1988", "7966", "174", "94", "45", "347", "4459", "491", "94", "146", "93", "456", "1567", ""],
    ["出口产品金额(万元)", "1990", "11135", "92", "553", "891", "1570", "3575", "297", "101", "265", "1989", "587", "1215", ""],
    ["其中：直接出口", "1988", "5014", "150", "64", "45", "235", "2602", "358", "32", "146", "41", "339", "1002", ""],
    ["其中：直接出口", "1990", "9873", "92", "414", "891", "1466", "2747", "297", "76", "226", "1949", "508", "1207", ""],
    ["其中：间接出口", "1988", "2952", "24", "30", "", "112", "1857", "133", "62", "", "52", "117", "565", ""],
    ["其中：间接出口", "1990", "1262", "", "139", "", "104", "828", "", "25", "39", "", "40", "79", ""],
]

PATCH = {
    "title": "1988年、1990年连云港市乡镇企业及出口产品情况表",
    "table_number": "表27-10",
    "page": 1311,
    "pages": [1311],
    "part": "part01",
    "vol": "中",
    "volume": "中",
    "columns": COLUMNS,
    "rows": ROWS,
    "row_count": len(ROWS),
    "col_count": len(COLUMNS),
    "status": "verified",
    "notes": "已据页级OCR核录：workbench/ocr/paddle_ocr/中/part01/page_0408.txt；并参考 raw 坐标 OCR：workbench/ocr/raw/中/part01/page_0408.json 与 raw 文本 workbench/table_entries/中/raw/LYG-中-T039_1311.txt。表27-10按源页横向品类列展开；raw 坐标 OCR 中 1988 年出口产品生产总值机电列 `t6`、1988 年直接出口机电列 `t9` 分别按页级 OCR 与行内合计校验更正为 `94`、`64`。源页未见数值处保留空值。",
}


def patch_entry(entry: dict) -> bool:
    if entry.get("table_id") != "LYG-中-T039":
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
