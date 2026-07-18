# -*- coding: utf-8 -*-
"""Verify LYG-中-T006 craft art award products head table."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
DATA = ROOT / "workbench" / "table_entries" / "中" / "data" / "LYG-中-T006.json"

COLUMNS = ["获奖年月", "获奖产品", "获奖名称", "生产企业"]
ROWS = [
    ["1963.10", "4吩机拉洗90道京式地毯", "江苏省地毯行业质量评比第一名", "连云港市地毯厂"],
    ["1978.6", "3吩机抽洗90道美术地毯", "江苏省地毯行业质量评比优胜奖", "连云港市地毯厂"],
    ["1978.8", "“西游记”贝雕立体小件", "江苏省“四新”产品三等奖", "连云港贝雕总厂"],
    ["1980.7", "“花果山”京式地毯图案", "江苏省地毯图案评比一等奖", "连云港市地毯厂"],
    ["1980.12", "“牡丹”花瓶", "华东地区玻璃器皿质量评比第一名", "连云港市玻璃制品"],
    ["1981.5", "22头炬器堆花茶具", "江苏省轻工“四新”产品三等奖", "赣榆县瓷厂"],
    ["1981.5", "毫毛发晶鼻烟壶", "江苏省轻工“四新”产品三等奖", "连云港市雕塑工艺"],
    ["1982.5", "双面异色座屏-梅花腊嘴", "全国同行业创新产品一等奖，中国工艺美术“百花”奖、优秀创作设计二等奖", "连云港贝雕总厂"],
    ["1982.5", "四季博古屏", "中国工艺美术“百花”奖，优秀创作设计二等奖", "连云港贝雕总厂"],
    ["1982.5", "“天姿国色”等6件作品", "全国同行业总分第三名", "连云港贝雕总厂"],
]

PATCH = {
    "title": "1963~1990年连云港市工艺美术工业获奖产品一览表",
    "table_number": "表17-16",
    "page": 960,
    "pages": [960],
    "columns": COLUMNS,
    "rows": ROWS,
    "row_count": len(ROWS),
    "col_count": len(COLUMNS),
    "status": "verified",
    "notes": "已据页级OCR回源核录：workbench/ocr/paddle_ocr/中/part01/page_0057.txt；原JSON为单列待录入骨架。页首含上一表续段，本轮仅录入表17-16首页；续表见LYG-中-T007、T008、T009。",
}


def patch_entry(entry: dict) -> bool:
    if entry.get("table_id") != "LYG-中-T006":
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
