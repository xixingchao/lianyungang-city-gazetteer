# -*- coding: utf-8 -*-
"""Verify LYG-中-T115 party secretaries table from raw OCR."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
DATA = ROOT / "workbench" / "table_entries" / "中" / "data" / "LYG-中-T115.json"

COLUMNS = ["组织名称", "职务", "姓名", "籍贯", "任职时间"]
ROWS = [
    ["新海连特委", "书记", "谷牧", "山东荣城", "1948.12~1949.3"],
    ["新海连特委", "书记", "苏羽", "河南沁阳", "1949.3~1949.10"],
    ["新海市委", "书记", "刁一民", "山东牟平", "1948.12~1949.10"],
    ["连云市委", "书记", "李奎元", "", "1948.12~1949.10"],
    ["云台工委", "书记", "梁如仁", "江苏东海", "1948.12~1949.8"],
    ["新海连市委", "书记", "苏羽", "河南沁阳", "1949.11~1950.5"],
    ["新海县委", "书记", "刁一民", "山东牟平", "1950.5~1950.12"],
    ["新海连市委", "代书记", "刁一民", "山东牟平", "1951.1~1952.2"],
    ["新海连市委", "兼书记", "梁如仁", "江苏东海", "1952.2~1953.1"],
    ["新海连市委", "代书记", "许耀林", "山东日照", "1953.1~1953.2"],
    ["新海连市委", "书记", "许耀林", "山东日照", "1953.2~1955.1"],
    ["新海连市委", "书记", "冯克玉", "山东曲阜", "1955.1~1956.5"],
    ["连云港市委", "第一书记", "许耀林", "山东日照", "1956.5~1959.2"],
    ["连云港市委", "第一书记", "许耀林", "山东日照", "1959.2~1960.12"],
    ["连云港市委", "第一书记", "田诚", "山东临沂", "1960.12~1961.10"],
    ["连云港市委", "第一书记", "田诚", "山东临沂", "1961.10~1962.11"],
    ["连云港市委", "书记", "张国安", "山东", "1962.11~1971.6"],
    ["连云港市委", "书记", "刘文龙", "江苏江都", "1971.6~1972.10"],
    ["连云港市委", "书记", "金逊", "浙江黄岩", "1974.2~1977.5"],
    ["连云港市委", "书记", "徐智", "浙江杭州", "1977.5~1980.1"],
    ["连云港市委", "书记", "叶志俊", "江苏沭阳", "1980.1~1984.7"],
    ["连云港市委", "书记", "季允石", "江苏海门", "1984.7~1989.9"],
    ["连云港市委", "书记", "秦兆祯", "上海市", "1989.9~"],
]

PATCH = {
    "title": "历任特委、市（县）委书记表",
    "table_number": "表41-8",
    "page": 1847,
    "pages": [1847],
    "columns": COLUMNS,
    "rows": ROWS,
    "row_count": len(ROWS),
    "col_count": len(COLUMNS),
    "status": "verified",
    "notes": "已据raw OCR回源核录：workbench/table_entries/中/raw/LYG-中-T115_1847.txt；原JSON为单列待录入骨架。连云市委书记李奎元籍贯OCR未清晰读出，保留空值；仅录入表41-8明确行，不将版面中的“辖：”另作层级推断。",
}


def patch_entry(entry: dict) -> bool:
    if entry.get("table_id") != "LYG-中-T115":
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
