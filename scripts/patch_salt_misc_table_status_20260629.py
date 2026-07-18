# -*- coding: utf-8 -*-
"""Correct salt/misc continuation-table metadata without over-verifying data."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
DATA_DIR = ROOT / "workbench" / "table_entries" / "上" / "data"

PATCHES = {
    "LYG-上-T034": {
        "title": "(续表，表题待确认)",
        "status": "pending-source-check",
        "notes": "仅见续表页，表题需回源前页确认；不得作为主交付入口",
    },
    "LYG-上-T035": {
        "title": "民国13~36年（1924~1947年）部分年份连云港市境内各盐场年产量统计表",
        "table_number": "表13-7",
        "status": "pending-source-check",
        "notes": "表题/表号已据OCR文本补正；现有结构表与源表列序/缺值需回源核录；不得作为主交付入口",
    },
    "LYG-上-T036": {
        "title": "(续表，表题待确认)",
        "status": "pending-source-check",
        "notes": "当前页为盐场年产量续表，前页表题未在现有raw片段中定位；待回源核录；不得作为主交付入口",
    },
    "LYG-上-T040": {
        "title": "(续表，表题待确认)",
        "status": "pending-source-check",
        "notes": "仅见日用五金与工具续表页，表题需回源前页确认；不得作为主交付入口",
    },
}


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
