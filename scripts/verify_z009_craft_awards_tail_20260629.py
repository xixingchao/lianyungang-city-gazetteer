# -*- coding: utf-8 -*-
"""Verify LYG-中-T009 craft art award products tail table."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
DATA = ROOT / "workbench" / "table_entries" / "中" / "data" / "LYG-中-T009.json"

COLUMNS = ["获奖年月", "获奖产品", "获奖名称", "生产企业"]
ROWS = [
    ["1989.12", "“葵花”牌桐木制品", "江苏省工艺美术“百花”奖", "连云港市工艺桐木制品厂"],
    ["1990.1", "斗牛图、小放牛", "人选江苏省首届民间美术博览会", "东海县白塔骁云阁工艺美术厂"],
    ["1990.2", "京彩式地毯图案", "江苏省地毯图案创新特别奖", "连云港市地毯厂"],
    ["1990.2", "金银线嵌贝画", "江苏省优秀新产品“金牛”奖", "连云港贝雕总厂"],
    ["1990.9", "镶嵌板画、贝雕柳编", "江苏省优秀新产品“金牛”奖", "赣榆县工艺美术公司"],
    ["1990.11", "869-5A1型多功能折叠式豪华童车", "江苏省优秀新产品“金牛”奖", "灌云县工艺美术工业公司"],
    ["1990.11", "多用摇篮床车", "江苏省先进适用科技成果新产品展览会金奖", "灌云县工艺美术工业公司"],
    ["1990.11", "浮雕八骏马", "江苏省先进适用科技成果新产品展览会金奖", "赣榆县工艺美术厂"],
    ["1990.11", "仕女贝瓷画“四季屏”(春艳、夏翠、秋实、冬秀)", "江苏省先进适用科技成果新产品展览会金奖", "赣榆县工艺美术厂"],
]

PATCH = {
    "title": "1963~1990年连云港市工艺美术工业获奖产品一览表（续表）",
    "table_number": "表17-16",
    "page": 963,
    "pages": [963],
    "columns": COLUMNS,
    "rows": ROWS,
    "row_count": len(ROWS),
    "col_count": len(COLUMNS),
    "status": "verified",
    "notes": "已据页级OCR回源核录：workbench/ocr/paddle_ocr/中/part01/page_0060.txt；主表题和表号见raw OCR workbench/table_entries/中/raw/LYG-中-T006_960.txt。本页为表17-16尾段续表。",
}


def patch_entry(entry: dict) -> bool:
    if entry.get("table_id") != "LYG-中-T009":
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
