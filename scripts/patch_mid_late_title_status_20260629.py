# -*- coding: utf-8 -*-
"""Patch mid/lower volume OCR-title mistakes while keeping tables pending source check."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
DATA_DIRS = {
    "中": ROOT / "workbench" / "table_entries" / "中" / "data",
    "下": ROOT / "workbench" / "table_entries" / "下" / "data",
}

PATCHES = {
    "LYG-中-T006": {"volume": "中", "title": "(续表，表题待确认)"},
    "LYG-中-T007": {"volume": "中", "title": "(续表，表题待确认)"},
    "LYG-中-T008": {"volume": "中", "title": "(续表，表题待确认)"},
    "LYG-中-T009": {"volume": "中", "title": "(续表，表题待确认)"},
    "LYG-中-T010": {"volume": "中", "title": "(续表，表题待确认)"},
    "LYG-中-T031": {"volume": "中", "title": "(续表，表题待确认)"},
    "LYG-中-T048": {"volume": "中", "title": "(续表，表题待确认)"},
    "LYG-中-T050": {
        "volume": "中",
        "title": "1984~1990年中国银行连云港分行企业外币存款余额统计表",
        "table_number": "表29-17",
    },
    "LYG-中-T074": {
        "volume": "中",
        "title": "1949~1990年部分年份连云港市市区国营商业主要商品零售量统计表（一）",
        "table_number": "表33-6",
    },
    "LYG-中-T095": {"volume": "中", "title": "(续表，表题待确认)"},
    "LYG-下-T074": {
        "volume": "下",
        "title": "1978年连云港市获省科技大会奖项目表",
        "table_number": "表51-9",
    },
}

COMMON = {
    "status": "pending-source-check",
    "notes": "表题已据raw OCR片段纠偏或标为续表；当前仍为单列骨架/待录入，待回源核录；不得作为主交付入口",
}


def patch_entry(entry: dict) -> bool:
    patch = PATCHES.get(entry.get("table_id"))
    if not patch:
        return False
    changed = False
    updates = {k: v for k, v in patch.items() if k != "volume"}
    updates.update(COMMON)
    for key, value in updates.items():
        if entry.get(key) != value:
            entry[key] = value
            changed = True
    return changed


def patch_json_files() -> int:
    changed = 0
    for table_id, patch in PATCHES.items():
        path = DATA_DIRS[patch["volume"]] / f"{table_id}.json"
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
    print(f"json_files_changed={patch_json_files()}")
    print(f"site_entries_changed={patch_site()}")


if __name__ == "__main__":
    main()
