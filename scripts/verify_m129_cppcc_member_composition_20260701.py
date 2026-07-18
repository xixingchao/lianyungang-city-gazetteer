# -*- coding: utf-8 -*-
"""Verify LYG-中-T129 CPPCC member composition table."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
DATA = ROOT / "workbench" / "table_entries" / "中" / "data" / "LYG-中-T129.json"

TERMS = ["第一届", "第二届", "第三届", "第四届", "第五届", "第六届", "第七届"]
COLUMNS = ["界别"] + [f"{term}{metric}" for term in TERMS for metric in ("人数(人)", "比例(%)")]


def row(name: str, vals: list[str]) -> list[str]:
    if len(vals) != 14:
        raise ValueError(f"{name} has {len(vals)} values")
    return [name] + vals


ROWS = [
    row("中共", ["", "6.6", "", "5.5", "", "5.7", "12", "7.5", "24", "10.5", "36", "11.5", "32", "8.6"]),
    row("源页界别未识别行1", ["", "", "", "", "", "", "", "", "", "", "", "", "10", "2.7"]),
    row("源页界别未识别行2", ["", "", "", "2.1", "", "1.9", "", "", "12", "5.3", "12", "3.8", "13", "3.5"]),
    row("源页界别未识别行3", ["", "", "", "", "", "", "", "", "", "", "", "", "19", "5.1"]),
    row("源页界别未识别行4", ["", "", "", "", "", "", "", "", "", "", "", "0.3", "13", "3.5"]),
    row("源页界别未识别行5", ["", "", "", "", "", "", "", "", "", "", "", "", "", "2.4"]),
    row("源页界别未识别行6", ["", "", "", "", "", "", "", "", "", "", "", "", "", "1.6"]),
    row("总工会", ["", "6.6", "", "5.5", "", "5.1", "", "4.4", "12", "5.3", "15", "4.8", "15", ""]),
    row("源页界别未识别行7", ["", "6.6", "", "4.9", "", "5.1", "", "5.1", "12", "5.3", "15", "4.8", "14", "3.8"]),
    row("共青团、青联", ["", "8.4", "", "4.2", "", "3.8", "", "3.1", "12", "5.3", "15", "4.8", "13", "3.5"]),
    row("工商联", ["17", "16.1", "18", "12.5", "18", "11.5", "18", "11.3", "", "", "", "2.6", "10", "2.7"]),
    row("农渔民", ["", "7.5", "", "6.3", "", "5.7", "10", "6.3", "10", "4.4", "15", "4.8", "16", "4.3"]),
    row("文学艺术", ["", "2.8", "10", "6.9", "", "5.7", "10", "6.3", "10", "4.4", "16", "5.1", "12", "3.2"]),
    row("科技", ["10", "9.4", "17", "11.1", "20", "12.8", "14", "8.8", "30", "13.1", "50", "15.9", "47", "12.6"]),
    row("教育", ["", "7.5", "14", "9.7", "17", "10.9", "20", "13", "20", "8.7", "40", "12.7", "35", "9.4"]),
    row("体育", ["", "", "", "", "", "", "", "", "", "0.9", "", "1.3", "", "1.3"]),
    row("医药卫生", ["", "7.5", "12", "8.3", "13", "8.3", "16", "10", "20", "8.7", "30", "9.6", "27", "7.2"]),
    row("新闻出版", ["", "", "", "", "", "", "", "", "", "1.3", "", "1.3", "", "1.3"]),
    row("社科", ["", "", "", "", "", "", "", "", "", "", "", "1.3", "", "1.1"]),
    row("归侨侨眷", ["", "", "", "", "", "", "", "", "", "0.9", "", "", "10", "2.7"]),
    row("台胞", ["", "", "", "", "", "", "", "", "", "0.5", "", "0.6", "", ""]),
    row("合作社", ["", "3.7", "", "2.8", "", "3.2", "", "3.1", "", "", "", "", "", ""]),
    row("少数民族", ["", "", "", "", "", "1.9", "", "", "", "0.9", "", "1.9", "", "1.6"]),
    row("宗教", ["", "3.7", "", "4.9", "", "3.8", "", "3.8", "", "1.8", "", "1.9", "", "1.9"]),
    row("对外友好", ["", "1.8", "", "1.4", "", "1.3", "", "1.3", "", "0.9", "", "0.6", "", "1.1"]),
    row("社会人士", ["", "", "10", "", "10", "6.4", "", "5.6", "", "", "", "", "", ""]),
    row("特邀", ["12", "11.3", "", "6.3", "10", "6.4", "12", "7.5", "", "22.3", "25", "7.9", "30", ""]),
    row("解放军", ["", "", "", "", "", "", "", "", "", "", "", "1.9", "", ""]),
    row("委员总数", ["106", "", "144", "", "156", "", "160", "", "229", "", "315", "", "373", ""]),
]

PATCH = {
    "title": "连云港市第一至七届历届政协委员会委员组成情况表",
    "table_number": "表42-3",
    "page": 1970,
    "pages": [1970],
    "part": "part02",
    "vol": "中",
    "volume": "中",
    "columns": COLUMNS,
    "rows": ROWS,
    "row_count": len(ROWS),
    "col_count": len(COLUMNS),
    "status": "verified",
    "notes": "已据 raw 坐标OCR核录：workbench/ocr/raw/中/part02/page_0550.json；并参考 raw 文本 workbench/table_entries/中/raw/LYG-中-T129_1970.txt。源页题名 OCR 漏识“第一至七届”中的“一”，本条按表意补正；表内各届人数、比例列密集，若源页未见界别名或数值则保留为空，未按委员总数或比例反推。",
}


def patch_entry(entry: dict) -> bool:
    if entry.get("table_id") != "LYG-中-T129":
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
