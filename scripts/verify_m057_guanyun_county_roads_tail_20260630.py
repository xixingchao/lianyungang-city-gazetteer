# -*- coding: utf-8 -*-
"""Verify Guanyun county road overview continuation table T057."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
DATA = ROOT / "workbench" / "table_entries" / "中" / "data" / "LYG-中-T057.json"

COLUMNS = [
    "类别",
    "起讫站点",
    "经过集镇",
    "里程(公里)",
    "路面宽度(米)",
    "修筑年份",
    "备注",
]

ROWS = [
    ["南陡线", "南岗一小潘庄", "后皂、潘场", "5.5", "3.5", "", "1966年筑成土面公路，1984年铺为沙石路"],
    ["董仲线", "董集一仲集", "小西庄、盐西", "5.5", "3.5", "", "1966年筑成土面公路，1988年铺为沙石路面"],
    ["穆高线", "穆圩一高墟", "", "5.4", "3.5", "", "1985年筑成土面公路，次年铺为沙石路面"],
    ["柴东线", "柴门一东陬山", "洋桥", "16.9", "4", "", "盐务专用；1952年筑成海堤道路，1965年淮北盐务局铺为沙石路"],
    ["穆平线", "穆圩一平明", "吴南、张湾", "5.2", "4", "", "县内里程；1988年筑成土面公路，1990年铺为沙石路"],
    ["陡西线", "陡沟一西圩", "", "5.0", "4", "", "1988年筑成土面公路，1990年铺为沙石路"],
]

PATCH = {
    "table_id": "LYG-中-T057",
    "title": "1990年灌云县县级公路概况表（续表）",
    "table_number": "表30-4",
    "page": 1446,
    "pages": [1446],
    "part": "part02",
    "vol": "中",
    "volume": "中",
    "columns": COLUMNS,
    "rows": ROWS,
    "row_count": len(ROWS),
    "col_count": len(COLUMNS),
    "status": "verified",
    "notes": "已据页级OCR回源核录：表题、表号和表头见 workbench/ocr/paddle_ocr/中/part02/page_0025.txt；续表内容见 workbench/ocr/paddle_ocr/中/part02/page_0026.txt，并参考 raw OCR workbench/table_entries/中/raw/LYG-中-T057_1446.txt。原JSON为单列骨架；本次仅录入续页可见的 6 条公路记录，长备注中的筑路年份保留在备注列，未拆入修筑年份列。",
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
