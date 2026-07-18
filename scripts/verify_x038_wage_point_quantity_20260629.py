# -*- coding: utf-8 -*-
"""Verify LYG-下-T038 national wage point quantity table from raw OCR."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
DATA = ROOT / "workbench" / "table_entries" / "下" / "data" / "LYG-下-T038.json"

COLUMNS = ["品名", "单位", "每分含量", "实物牌号质量、价格计算说明"]
ROWS = [
    ["粮食", "市斤", "", "实物牌号质量、价格计算一律依照国营企业调整工资办法执行。"],
    ["双龙细布", "市尺", "", ""],
    ["生油", "市斤", "0.03125", ""],
    ["食盐", "市斤", "0.03125", ""],
    ["原煤", "市斤", "", ""],
]

PATCH = {
    "title": "全国工资分定量表",
    "table_number": "表47-6",
    "page": 2230,
    "pages": [2230],
    "columns": COLUMNS,
    "rows": ROWS,
    "row_count": len(ROWS),
    "col_count": len(COLUMNS),
    "status": "verified",
    "notes": "已据raw OCR回源核录：workbench/table_entries/下/raw/LYG-下-T038_2230.txt；原JSON为单列待录入骨架。OCR中粮食、双龙细布、原煤的每分含量未清晰读出，保留空值，未据正文换算补填。",
}


def patch_entry(entry: dict) -> bool:
    if entry.get("table_id") != "LYG-下-T038":
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
