# -*- coding: utf-8 -*-
"""Verify LYG-下-T057 labor technology course table from raw OCR."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
DATA = ROOT / "workbench" / "table_entries" / "下" / "data" / "LYG-下-T057.json"

COLUMNS = ["校名", "开设年份", "开设专业", "开设年级"]
ROWS = [
    ["新海中学", "1983", "工艺美术、书法、园艺、微机、英文打字、制图、缝纫、家电维修", "初一至高三"],
    ["海州中学", "1986", "摄影、缝纫、电子技术基础、微机、打字、工艺、园艺", "初一、初二；高一至高三"],
    ["连云港教育学院附中", "1986", "工艺美术、篆刻、理发、花卉栽培、动植物标本制作、机织、电器制作、烹饪、摄影、缝纫", "初一至初三"],
    ["新浦中学", "1987", "剪纸及书法、摄影、泥塑技术、照明电路及家电维修", "初一、初二；高一、高二"],
    ["浦东中学", "1988", "花卉栽培、摄影、工艺制作、裁剪缝纫、家用电器维修、电子技术基础", "初一至初三"],
    ["陇东中学", "1988", "纸工、布工、家政", "初一、初二"],
    ["延安中学", "1988", "手工、书法、裁剪缝纫", "初一、初二"],
    ["临洪中学", "1984", "植物标本制作、篆刻、工艺制作、裁剪缝纫、家用电器", "初一至初三；初一、初二"],
    ["蔷薇中学", "1986", "电子技术基础、花卉栽培、工艺美术制作", "高一至高三；初一至初三"],
    ["新坝中学", "1987", "手工制作、植物栽培、动物饲养", "初一至初三"],
    ["南城中学", "1988", "植物栽培、制图、家用电器", "初一、初二；高一、高二"],
    ["花果山中学", "1988", "工艺制作、家用电器、裁剪缝纫", "初一至初三"],
]

PATCH = {
    "title": "1990年连云港市市区普通中学劳动技术课开设情况表",
    "table_number": "表50-12",
    "page": 2353,
    "pages": [2353],
    "columns": COLUMNS,
    "rows": ROWS,
    "row_count": len(ROWS),
    "col_count": len(COLUMNS),
    "status": "verified",
    "notes": "已据raw OCR回源核录：workbench/table_entries/下/raw/LYG-下-T057_2353.txt；原JSON为单列待录入骨架。页首含上一表续表残段，本轮仅录入表50-12；跨行专业设置已合并至对应学校；OCR中的“裁培/裁栽培”按语境规范为“栽培”。",
}


def patch_entry(entry: dict) -> bool:
    if entry.get("table_id") != "LYG-下-T057":
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
