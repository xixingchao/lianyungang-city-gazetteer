# -*- coding: utf-8 -*-
"""Verify LYG-中-T109 savings types table from raw OCR."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
DATA = ROOT / "workbench" / "table_entries" / "中" / "data" / "LYG-中-T109.json"

COLUMNS = ["序号", "条目类型", "名称", "起讫时间"]
ROWS = [
    ["1", "储蓄种类或账户类型", "折实储蓄", "1949.10.17~1950.12"],
    ["2", "类别提示", "保值性储蓄", ""],
    ["3", "储蓄种类或账户类型", "定期储蓄", "1950.7~1952.6"],
    ["4", "储蓄种类或账户类型", "定期定额有奖储蓄", "1951.7~1952.6"],
    ["5", "储蓄种类或账户类型", "保本保值储蓄", ""],
    ["6", "储蓄种类或账户类型", "定额储蓄", "1950~1952.6"],
    ["7", "储蓄种类或账户类型", "保值定期储蓄", "1988.9.10~"],
    ["8", "储蓄种类或账户类型", "定期储蓄", "1949~"],
    ["9", "储蓄种类或账户类型", "华侨（人民币）定期储蓄", "1955.10.1~"],
    ["10", "储蓄种类或账户类型", "定期定额有奖有息储蓄", "1985、1986、1987、1988"],
    ["11", "类别提示", "定整", ""],
    ["12", "储蓄种类或账户类型", "大面额（优息）储蓄存单", "1988.1~1989.10"],
    ["13", "储蓄种类或账户类型", "个人大面额可转让定期储蓄", "1990.1~"],
    ["14", "储蓄种类或账户类型", "零存整取有奖贴花储蓄", "1951.12~1958.12；1959.7~1961.1"],
    ["15", "类别提示", "个人户", ""],
    ["16", "储蓄种类或账户类型", "零存整取贴花储蓄", "1959.1~1959.6；1961.1~1965.6"],
    ["17", "类别提示", "储存", ""],
    ["18", "储蓄种类或账户类型", "零存整取小额（记帐）储蓄", "1965.7.1~"],
    ["19", "类别提示", "集体户", ""],
    ["20", "储蓄种类或账户类型", "零存整取集体（记帐）储蓄", "1979~"],
    ["21", "储蓄种类或账户类型", "零存整取集体有奖有息（记帐）储蓄", "1983~"],
    ["22", "储蓄种类或账户类型", "存本取息", "1953.1~1965.5；1980.4~"],
    ["23", "储蓄种类或账户类型", "江苏省地方工业建设储蓄", "1959.6~12；1961.3~10"],
    ["24", "储蓄种类或账户类型", "支票户", "1949~1963.3"],
    ["25", "储蓄种类或账户类型", "存折户", "1949~"],
    ["26", "储蓄种类或账户类型", "定额有息户", "1951.12~1955.2；1957.6~1959.6"],
    ["27", "类别提示", "存单", ""],
    ["28", "储蓄种类或账户类型", "有奖有息户", "1958.6~12"],
    ["29", "储蓄种类或账户类型", "定活两便储蓄", "1950.7~12；1986.1~"],
    ["30", "储蓄种类或账户类型", "活期存单", "1981.1~"],
]

PATCH = {
    "title": "1949~1990年连云港市储蓄种类表",
    "table_number": "表40-3",
    "page": 1777,
    "pages": [1777],
    "columns": COLUMNS,
    "rows": ROWS,
    "row_count": len(ROWS),
    "col_count": len(COLUMNS),
    "status": "verified",
    "notes": "已据raw OCR回源核录：workbench/table_entries/中/raw/LYG-中-T109_1777.txt；本表为储蓄种类/账户类型清单，按OCR行序保守整理，未强行重建版面层级；OCR中的“保值性储蕾”按上下文规范为“保值性储蓄”。",
}


def patch_entry(entry: dict) -> bool:
    if entry.get("table_id") != "LYG-中-T109":
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
