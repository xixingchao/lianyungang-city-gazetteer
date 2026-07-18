# -*- coding: utf-8 -*-
"""Verify LYG-下-T077 social science technical staff table from raw OCR."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
DATA = ROOT / "workbench" / "table_entries" / "下" / "data" / "LYG-下-T077.json"

COLUMNS = ["类别", "总计(人)", "高级技术人员(人)", "中级技术人员(人)", "初级技术人员(人)"]
ROWS = [
    ["总计", "10652", "47", "1336", "9269"],
    ["会计人员", "3138", "7", "366", "2765"],
    ["统计人员", "742", "7", "79", "656"],
    ["经济人员", "5786", "24", "656", "5106"],
    ["翻译人员", "76", "", "51", "25"],
    ["体育人员", "143", "21", "41", "81"],
    ["编辑人员", "", "", "62", "73"],
    ["图书档案人员", "575", "4", "112", "459"],
    ["工艺美术人员", "104", "", "20", "29"],
    ["律师、公证人员", "110", "", "", ""],
    ["播音人员", "", "12", "", ""],
]

PATCH = {
    "title": "1990年连云港市社会科学技术人员情况表",
    "table_number": "表51-14",
    "page": 2431,
    "pages": [2431],
    "columns": COLUMNS,
    "rows": ROWS,
    "row_count": len(ROWS),
    "col_count": len(COLUMNS),
    "status": "verified",
    "notes": "已据raw OCR回源核录：workbench/table_entries/下/raw/LYG-下-T077_2431.txt；原JSON为单列待录入骨架。表前含上一表续表残段，本轮仅录入表51-14。编辑人员、工艺美术人员、律师/公证人员、播音人员部分栏位OCR未清晰读出，保留空值，未猜补。",
}


def patch_entry(entry: dict) -> bool:
    if entry.get("table_id") != "LYG-下-T077":
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
