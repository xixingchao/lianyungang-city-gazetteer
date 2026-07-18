# -*- coding: utf-8 -*-
"""Verify LYG-上-T027 Xinshu river bank-crossing structures table."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
DATA = ROOT / "workbench" / "table_entries" / "上" / "data" / "LYG-上-T027.json"

COLUMNS = [
    "建筑物名称",
    "堤别",
    "地点",
    "建成年份",
    "长度(米)",
    "孔数(个)",
    "孔宽(米)",
    "孔高(米)",
    "顶高程(米)",
    "底高程(米)",
    "设计流量(立方米/秒)",
    "工程规模说明",
]

ROWS = [
    ["李曹埠电排涵", "左堤", "大岭乡", "1976", "36", "3", "1.0", "1.5", "16.5", "15.0", "1.58", ""],
    ["西赤金电排涵", "左堤", "大岭乡", "1976", "36", "2", "1.0", "1.5", "16.0", "14.5", "1", ""],
    ["前赤金电排涵", "左堤", "大岭乡", "1976", "36", "1", "2.0", "1.5", "15.5", "14.0", "0.83", ""],
    ["张庄电排涵", "左堤", "大岭乡", "1976", "36", "3", "1.0", "1.5", "14.5", "13.0", "1", ""],
    ["蒋庄军垦涵洞", "左堤", "沙河镇", "1966", "40", "1", "1.2", "1.8", "8.6", "7.0", "8", ""],
    ["沭北放水涵洞", "左堤", "沙河镇", "1966", "40", "2", "1.2", "1.8", "8.6", "7.0", "8", ""],
    ["沭北通航闸", "左堤", "沙河镇", "1978", "10", "1", "10.0", "6.0", "9.9", "-1.0", "90", ""],
    ["排碱涵洞", "左堤", "罗阳乡", "1977", "110", "2", "1.5", "1.8", "2.2", "0.0", "", ""],
    ["范河闸", "左堤", "罗阳乡", "1958", "28.9", "3", "2×5.5；1×8.0", "8.5", "6.0", "-2.0", "267", ""],
    ["海浮涵洞", "左堤", "罗阳乡", "1988", "110", "2", "2.5", "2.0", "1.0", "-1.0", "12", ""],
    ["石梁河退水闸", "左堤", "石梁河乡", "1962", "6.5", "2", "2.5", "4.0", "20.0", "16.0", "20", ""],
    ["磨山河桥闸", "左堤", "黄川乡", "1984", "81.7", "5", "4.7", "5.0", "12.0", "7.0", "660", ""],
    ["沭南灌溉涵洞", "右堤", "浦南乡", "1957", "40.0", "2", "1.5", "1.5", "8.7", "7.0", "10", ""],
    ["沭南通航闸", "右堤", "浦南乡", "1977", "10.0", "1", "10.0", "8.0", "9.9", "-1.0", "90", ""],
    ["太平庄排碱涵洞", "右堤", "浦南乡", "1977", "55.0", "1", "1.5", "2.25", "6.3", "0.5", "10", ""],
    ["临洪西站", "右堤", "浦南乡", "1978", "", "", "", "", "", "", "90", "装机3台套，9000瓦，设计流量90米/秒"],
    ["乌龙河自排闸", "右堤", "浦南乡", "1978", "10.0", "1", "10.0", "8.0", "9.9", "-1.0", "90", ""],
    ["临洪闸", "右堤", "市郊", "1959", "167.5", "26", "5.0", "6.2", "7.5", "-3.0", "1380", ""],
    ["临洪东站", "右堤", "市郊", "1980", "", "", "", "", "", "", "360", "设计装机12套36000千瓦，设计流量360米/秒；停建"],
    ["大浦站", "右堤", "市郊", "1980", "", "", "", "", "", "", "45", "设计装机6台套4800千瓦，设计流量45米/秒；停建"],
    ["大浦闸", "右堤", "市郊", "1955", "11.2", "3", "2×2.5；1×5.0", "2×3.5；1×6.5", "5.6", "-1.0", "98", ""],
    ["公兴闸", "右堤", "市郊", "1961", "7.8", "2", "3.5", "3.0", "8.4", "0.0", "", ""],
    ["元宝港闸", "右堤", "市郊", "1961", "12.8", "3", "2×2.5；1×6.5", "2×3.8；1×7.5", "7.3", "-1.0", "", ""],
]

PATCH = {
    "title": "1990年新沭河连云港市境内穿堤建筑物情况表",
    "table_number": "表10-3",
    "page": 571,
    "pages": [571],
    "part": "part02",
    "vol": "上",
    "volume": "上",
    "columns": COLUMNS,
    "rows": ROWS,
    "row_count": len(ROWS),
    "col_count": len(COLUMNS),
    "status": "verified",
    "notes": "已据页级OCR核录：workbench/ocr/paddle_ocr/上/part02/page_0271.txt；并参考 raw 坐标 OCR：workbench/ocr/raw/上/part02/page_0271.json 与 raw 文本 workbench/table_entries/上/raw/LYG-上-T027_571.txt。表10-3实际位于 page_0271，本条仅录入新沭河穿堤建筑物情况表；工程规模复合表头已展开，泵站类文字规模写入工程规模说明。raw OCR 将新沭河、沭北、沭南误作近形字，按页级OCR与章节语境更正。",
}


def patch_entry(entry: dict) -> bool:
    if entry.get("table_id") != "LYG-上-T027":
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
