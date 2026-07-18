# -*- coding: utf-8 -*-
"""Verify LYG-上-T019 social retail total table."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
DATA = ROOT / "workbench" / "table_entries" / "上" / "data" / "LYG-上-T019.json"

COLUMNS = ["类别", "全市(万元)", "市区(万元)", "赣榆县(万元)", "东海县(万元)", "灌云县(万元)"]

ROWS = [
    ["社会商品零售总额", "243239", "100498", "47214", "52150", "43377"],
    ["社会商品零售额", "222831", "86697", "44663", "51097", "40374"],
    ["一、按销售对象分：", "", "", "", "", ""],
    ["对居民的消费品", "158434", "83407", "33900", "30516", "31019"],
    ["对社会集团的消费品", "20134", "11524", "3089", "2251", "3270"],
    ["对农民的生产资料", "44263", "5567", "10225", "19383", "9088"],
    ["二、按行业分：", "", "", "", "", ""],
    ["商业零售额", "175993", "73663", "35958", "36510", "29862"],
    ["饮食业零售额", "8698", "3761", "1766", "1498", "1673"],
    ["工业零售额", "29360", "5647", "5957", "10148", "7608"],
    ["其它行业零售额", "8780", "3626", "982", "2941", "1231"],
    ["三、农民对非农居民零售", "20408", "13801", "2551", "1053", "3003"],
]

PATCH = {
    "title": "1990年连云港市社会商品零售总额统计表",
    "table_number": "表7-7",
    "page": 439,
    "pages": [439],
    "part": "part02",
    "vol": "上",
    "volume": "上",
    "columns": COLUMNS,
    "rows": ROWS,
    "row_count": len(ROWS),
    "col_count": len(COLUMNS),
    "status": "verified",
    "notes": "已据页级OCR核录：workbench/ocr/paddle_ocr/上/part02/page_0140.txt；并参考 raw 坐标 OCR：workbench/ocr/raw/上/part02/page_0140.json 与 raw 文本 workbench/table_entries/上/raw/LYG-上-T019_439.txt。表7-7实际位于 page_0140，本条仅录入社会商品零售总额统计表；同页后续表7-8未并入。源页表头为地区/类别复合表头，列名已展开为各地区金额。",
}


def patch_entry(entry: dict) -> bool:
    if entry.get("table_id") != "LYG-上-T019":
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
