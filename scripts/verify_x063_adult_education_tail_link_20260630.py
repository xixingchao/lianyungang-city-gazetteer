# -*- coding: utf-8 -*-
"""Mark LYG-下-T063 as merged into the verified adult education cross-page table."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
DATA = ROOT / "workbench" / "table_entries" / "下" / "data" / "LYG-下-T063.json"

COLUMNS = ["主表ID", "主表题", "本页来源", "处理说明"]
ROWS = [[
    "LYG-下-T062",
    "1990年连云港市成人教育基本情况表",
    "workbench/ocr/paddle_ocr/下/part01/page_0400.txt；workbench/table_entries/下/raw/LYG-下-T063_2371.txt",
    "本页为表50-20的跨页续表内容，已在主表 LYG-下-T062 中按 5 列、23 行完整核录，本条保留交叉引用，不重复造表。",
]]

PATCH = {
    "title": "1990年连云港市成人教育基本情况表（跨页续表已并入LYG-下-T062）",
    "table_number": "表50-20",
    "page": 2371,
    "pages": [2371],
    "part": "part01",
    "vol": "下",
    "volume": "下",
    "columns": COLUMNS,
    "rows": ROWS,
    "row_count": len(ROWS),
    "col_count": len(COLUMNS),
    "status": "verified",
    "notes": "本页为跨页表50-20续表，已在 LYG-下-T062 中完整核录，证据见 scripts/verify_x062_adult_education_20260630.py、workbench/ocr/paddle_ocr/下/part01/page_0399.txt、page_0400.txt 及 raw OCR workbench/table_entries/下/raw/LYG-下-T063_2371.txt。原条目题名串章为筑路养护机械表，本次更正为成人教育表续页引用。",
}


def patch_entry(entry: dict) -> bool:
    if entry.get("table_id") != "LYG-下-T063":
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
