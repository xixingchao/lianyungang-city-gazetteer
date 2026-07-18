# -*- coding: utf-8 -*-
"""Verify LYG-下-T059 secondary specialized schools table from raw OCR."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
DATA = ROOT / "workbench" / "table_entries" / "下" / "data" / "LYG-下-T059.json"

COLUMNS = ["学校名称", "校址", "创办年份", "学生数(人)", "专业设置"]
ROWS = [
    ["江苏省连云港水产学校", "墟沟", "1934", "482", "水产养殖；水产捕捞；轮机管理；加工、制冷"],
    ["江苏省连云港中药学校", "新浦海连东路", "1958", "886", "中药剂士；护士"],
    ["江苏盐业学校", "猴嘴", "1960", "786", "盐化管理；轻工机械装备；工业企业管理"],
    ["江苏省连云港财经学校", "新浦通赣路", "1964", "662", "财务会计；财政；税务；企业财务"],
    ["连云港艺术学校", "新浦海连西路", "1977", "53", "舞蹈"],
    ["连云港市体育运动学校", "新浦菜市街", "1986", "111", "体育运动"],
]

PATCH = {
    "title": "1990年连云港市中等专业学校一览表",
    "table_number": "表50-15",
    "page": 2357,
    "pages": [2357],
    "columns": COLUMNS,
    "rows": ROWS,
    "row_count": len(ROWS),
    "col_count": len(COLUMNS),
    "status": "verified",
    "notes": "已据raw OCR回源核录：workbench/table_entries/下/raw/LYG-下-T059_2357.txt；专业设置多行合并到对应学校；财经学校专业中“税物”按语境规范为“税务”。",
}


def patch_entry(entry: dict) -> bool:
    if entry.get("table_id") != "LYG-下-T059":
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
