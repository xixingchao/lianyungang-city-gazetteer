# -*- coding: utf-8 -*-
"""Verify LYG-下-T002 grassroots governance and mass organizations table."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
DATA = ROOT / "workbench" / "table_entries" / "下" / "data" / "LYG-下-T002.json"

COLUMNS = [
    "区县",
    "镇数(个)",
    "乡数(个)",
    "街道办事处(个)",
    "居民委员会数(个)",
    "居民委员会委员人数(人)",
    "村民委员会数(个)",
    "村民委员会委员人数(人)",
]
ROWS = [
    ["新浦区", "", "", "5", "83", "651", "2", "14"],
    ["海州区", "1", "3", "2", "22", "43", "", "194"],
    ["云台区", "4", "4", "", "17", "44", "50", "41"],
    ["连云区", "2", "4", "2", "37", "224", "24", "160"],
    ["赣榆县", "10", "19", "", "8", "40", "760", "4906"],
    ["东海县", "6", "18", "", "5", "36", "479", "2460"],
    ["灌云县", "7", "18", "", "20", "82", "427", "2530"],
    ["合计", "30", "66", "9", "192", "1143", "1785", "10305"],
]

PATCH = {
    "title": "1990年基层政权及群众自治组织情况表",
    "table_number": "表43-3",
    "page": 1991,
    "pages": [1991],
    "part": "part01",
    "vol": "下",
    "volume": "下",
    "columns": COLUMNS,
    "rows": ROWS,
    "row_count": len(ROWS),
    "col_count": len(COLUMNS),
    "status": "verified",
    "notes": "已据页级OCR核录：workbench/ocr/paddle_ocr/下/part01/page_0020.txt，并参考 raw OCR：workbench/table_entries/下/raw/LYG-下-T002_1991.txt。源页未见数值的单元格保留空值；列组按基层政权机构、基层群众自治组织展开。",
}


def patch_entry(entry: dict) -> bool:
    if entry.get("table_id") != "LYG-下-T002":
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
