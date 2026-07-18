# -*- coding: utf-8 -*-
"""Patch remaining party/CPPCC section OCR-title mistakes."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
DATA_DIR = ROOT / "workbench" / "table_entries" / "中" / "data"

PATCHES = {
    "LYG-中-T115": {
        "title": "历任特委、市（县）委书记表",
        "table_number": "表41-8",
    },
    "LYG-中-T117": {"title": "续表（表题待确认）"},
    "LYG-中-T118": {"title": "续表（表题待确认）"},
    "LYG-中-T119": {"title": "续表（表题待确认）"},
    "LYG-中-T120": {"title": "续表（表题待确认）"},
    "LYG-中-T121": {"title": "续表（表题待确认）"},
    "LYG-中-T122": {"title": "续表（表题待确认）"},
    "LYG-中-T126": {
        "title": "1950~1990年中共连云港市监察委员会、纪律检查委员会历任书记表",
        "table_number": "表41-14",
    },
    "LYG-中-T127": {"title": "续表（表题待确认）"},
    "LYG-中-T128": {
        "title": "连云港市历届人民代表大会党外人士安排情况表",
        "table_number": "表41-16",
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
    updates = dict(patch)
    updates.update(COMMON)
    for key, value in updates.items():
        if entry.get(key) != value:
            entry[key] = value
            changed = True
    return changed


def patch_json_files() -> int:
    changed = 0
    for table_id in PATCHES:
        path = DATA_DIR / f"{table_id}.json"
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
