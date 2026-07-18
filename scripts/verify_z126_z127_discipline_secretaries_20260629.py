# -*- coding: utf-8 -*-
"""Verify LYG-中-T126/T127 discipline inspection secretaries table from raw OCR."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
DATA_FILES = {
    "LYG-中-T126": ROOT / "workbench" / "table_entries" / "中" / "data" / "LYG-中-T126.json",
    "LYG-中-T127": ROOT / "workbench" / "table_entries" / "中" / "data" / "LYG-中-T127.json",
}

COLUMNS = ["组织名称", "职务", "姓名", "任职时间"]
PATCHES = {
    "LYG-中-T126": {
        "title": "1950~1990年中共连云港市监察委员会、纪律检查委员会历任书记表",
        "table_number": "表41-14",
        "page": 1868,
        "pages": [1868],
        "columns": COLUMNS,
        "rows": [
            ["中共新海县纪律检查委员会", "书记", "刘建民", "1950.9~1951.1"],
            ["中共新海连市纪律检查委员会", "书记", "刘建民", "1951.1~1952.4"],
            ["中共新海连市委监察委员会", "书记", "许光", "1952.7~1953.2"],
            ["中共连云港市委监察委员会", "书记", "余晋康（兼）", "1960~1961.4"],
            ["中共连云港市委监察委员会", "书记", "郑鹤（兼）", "1963.1~1966.5"],
            ["中共连云港市委纪律检查委员会", "书记", "邱效周（兼）", "1979.4~1980.8"],
            ["中共连云港市委纪律检查委员会", "书记", "王遐松（兼）", "1980.8~1983.2"],
            ["中共连云港市委纪律检查委员会", "书记", "周召", "1980.8~1983.2"],
        ],
        "status": "verified",
        "notes": "已据raw OCR回源核录：workbench/table_entries/中/raw/LYG-中-T126_1868.txt；原JSON为单列待录入骨架。本页为表41-14首页，续表见LYG-中-T127。",
    },
    "LYG-中-T127": {
        "title": "1950~1990年中共连云港市监察委员会、纪律检查委员会历任书记表（续表）",
        "table_number": "表41-14",
        "page": 1869,
        "pages": [1869],
        "columns": COLUMNS,
        "rows": [
            ["中共连云港市纪律检查委员会", "书记", "李彬", "1984.10~1985.10"],
            ["中共连云港市纪律检查委员会", "书记", "郑申雄（兼）", "1985.10~1987.12"],
            ["中共连云港市纪律检查委员会", "书记", "俞素娥", "1988.1~"],
        ],
        "status": "verified",
        "notes": "已据raw OCR回源核录：workbench/table_entries/中/raw/LYG-中-T127_1869.txt；原JSON为单列待录入骨架。本页为表41-14续表，首页见LYG-中-T126。",
    },
}

for patch in PATCHES.values():
    patch["row_count"] = len(patch["rows"])
    patch["col_count"] = len(patch["columns"])


def patch_entry(entry: dict) -> bool:
    patch = PATCHES.get(entry.get("table_id"))
    if not patch:
        return False
    changed = False
    for key, value in patch.items():
        if entry.get(key) != value:
            entry[key] = value
            changed = True
    return changed


def patch_json() -> int:
    changed = 0
    for table_id, path in DATA_FILES.items():
        data = json.loads(path.read_text(encoding="utf-8"))
        if patch_entry(data):
            path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            changed += 1
    return changed


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
