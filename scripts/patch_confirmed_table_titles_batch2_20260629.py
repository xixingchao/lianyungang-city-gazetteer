# -*- coding: utf-8 -*-
"""Patch a second source-confirmed batch of table title metadata."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
DATA_DIR = ROOT / "workbench" / "table_entries" / "上" / "data"

PATCHES = {
    "LYG-上-T039": {
        "title": "1964年连云港市主要杂件印刷企业基本情况表",
        "table_number": "表14-2",
    },
    "LYG-上-T041": {
        "title": "1970~1990年连云港市化纤业生产经营情况统计表",
        "table_number": "表15-1",
        "status": "pending-source-check",
        "notes": "表题/表号已据OCR文本补正；现有结构表缺少源表部分字段，待回源核录；不得作为主交付入口",
    },
    "LYG-上-T043": {
        "title": "1990年连云港市纺织工业企业基本情况表",
        "table_number": "表15-10",
        "status": "pending-source-check",
        "notes": "表题/表号已据OCR文本补正；现有结构表多列未录入，待回源核录；不得作为主交付入口",
    },
    "LYG-上-T044": {
        "title": "1990年连云港市塑料工业企业基本情况表",
        "table_number": "表16-3",
        "status": "pending-source-check",
        "notes": "表题/表号已据OCR文本补正；源表含主管单位等字段，现有结构表需回源复核；不得作为主交付入口",
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
