# -*- coding: utf-8 -*-
"""Verify LYG-中-T030 electronics award products continuation table."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
DATA = ROOT / "workbench" / "table_entries" / "中" / "data" / "LYG-中-T030.json"

COLUMNS = ["产品型号名称", "生产企业", "获奖级别", "获奖年份"]
ROWS = [
    ["“连晶”牌2CZ85C型硅整流二极管", "连云港市晶体管厂", "省优", "1989"],
    ["“超晶”牌DHG400目、600目活性硅微粉", "东海县硅微粉厂", "省优", "1989"],
    ["“超晶”牌DHC400目、600目活性硅微粉", "东海县硅微粉厂", "部优", "1990"],
    ["“玺瑶”牌BOC-200×10人造石英晶体材料", "东海县水晶厂", "省优", "1990"],
    ["“超晶”牌DHG400目、600目活性硅微粉", "东海县硅微粉厂", "省优秀新产品“金牛”奖", "1990"],
    ["“飞帆”牌TJC、TJC3型彩电连接器", "连云港市无线电元件四厂", "省优秀新产品“金牛”奖", "1990"],
]

PATCH = {
    "title": "连云港市电子工业获奖产品一览表（续表）",
    "table_number": "表22-8",
    "page": 1171,
    "pages": [1171],
    "columns": COLUMNS,
    "rows": ROWS,
    "row_count": len(ROWS),
    "col_count": len(COLUMNS),
    "status": "verified",
    "notes": "已据页级OCR回源核录：workbench/ocr/paddle_ocr/中/part01/page_0268.txt；主表题和表号见page_0267.txt。",
}


def patch_entry(entry: dict) -> bool:
    if entry.get("table_id") != "LYG-中-T030":
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
