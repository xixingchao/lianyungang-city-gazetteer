# -*- coding: utf-8 -*-
"""Verify LYG-下-T008 production reformatory intake table."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
DATA = ROOT / "workbench" / "table_entries" / "下" / "data" / "LYG-下-T008.json"

COLUMNS = [
    "收容总数合计(人)",
    "收容总数男(人)",
    "收容总数女(人)",
    "人员类型合计(人)",
    "人员类型乞丐(人)",
    "人员类型小偷(人)",
    "人员类型烟民(人)",
    "人员类型游民(人)",
    "人员类型土娼旧官兵(人)",
    "人员类型贫民(人)",
    "其中道会门反革命骨干分子(人)",
    "处理情况回乡(人)",
    "处理情况所留(人)",
    "处理情况生产改造(人)",
    "处理情况逃跑(人)",
    "处理情况死亡(人)",
    "处理情况法办(人)",
]
ROWS = [[
    "231", "161", "70", "109", "17", "2", "12", "2", "10", "2", "2", "75", "26", "125", "6", "73", "1"
]]

PATCH = {
    "title": "1951年新海连市生产教养院收容人员情况表",
    "table_number": "表43-13",
    "page": 2021,
    "pages": [2021],
    "part": "part01",
    "vol": "下",
    "volume": "下",
    "columns": COLUMNS,
    "rows": ROWS,
    "row_count": len(ROWS),
    "col_count": len(COLUMNS),
    "status": "verified",
    "notes": "已据页级OCR核录：workbench/ocr/paddle_ocr/下/part01/page_0050.txt，并参考 raw OCR：workbench/table_entries/下/raw/LYG-下-T008_2021.txt。原表为单行多级表头，结构化为展开列；表头中的土娼旧官兵按源页合并列保留。",
}


def patch_entry(entry: dict) -> bool:
    if entry.get("table_id") != "LYG-下-T008":
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
