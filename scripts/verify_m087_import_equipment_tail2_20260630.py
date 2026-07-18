# -*- coding: utf-8 -*-
"""Verify final import equipment/product continuation page."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
DATA_DIR = ROOT / "workbench" / "table_entries" / "中" / "data"

PATCHES = {
    "LYG-中-T087": {
        "title": "1984~1990年连云港市进口设备和产品情况表（续表）",
        "table_number": "表35-5",
        "page": 1617,
        "pages": [1617],
        "part": "part02",
        "vol": "中",
        "volume": "中",
        "columns": ["单位", "项目(单机)名称", "金额(万美元)"],
        "rows": [
            ["市电子系统", "彩电晶体生产线", "39.85"],
            ["市电子系统", "磁带计数器安装配线", "4.95"],
            ["市电子系统", "彩电接插件生产线", "102.94"],
            ["市电子系统", "端子五金冲模", "3.90"],
            ["市电子系统", "接插件检测设备", "4.15"],
            ["市电子系统", "商标印刷机", "4.30"],
            ["市电子系统", "收录机CKD", "19.59"],
            ["市电子系统", "收录机CKD", "17.08"],
            ["市电子系统", "二级管后道加工设备", "10.48"],
            ["市电子系统", "设备仪表", "10.00"],
            ["市电子系统", "中外合作生产彩色软包装", "50.00"],
            ["市电子系统", "意大利彩色印刷机", "22.80"],
            ["市电子系统", "打印机和显示器", "12.94"],
            ["市电子系统", "微波炉SKD", "12.40"],
            ["市电子系统", "微波炉SKD", "6.25"],
            ["市电子系统", "微波炉SKD", "8.80"],
            ["市电子系统", "微波炉SKD", "0.03"],
        ],
        "status": "verified",
        "notes": "已据页级OCR回源核录：workbench/ocr/paddle_ocr/中/part02/page_0197.txt，并参考 raw OCR：workbench/table_entries/中/raw/LYG-中-T087_1617.txt。表题、表号和列组依据前页表35-5。本页为进口设备和产品情况表末段续表；页后进入第四章正文。",
    }
}

for patch in PATCHES.values():
    patch["row_count"] = len(patch["rows"])
    patch["col_count"] = len(patch["columns"])


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
