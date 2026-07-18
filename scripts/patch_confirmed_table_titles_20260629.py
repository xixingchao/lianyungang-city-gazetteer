# -*- coding: utf-8 -*-
"""Patch source-confirmed table title metadata for a small reviewed batch."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
DATA_DIR = ROOT / "workbench" / "table_entries" / "上" / "data"

PATCHES = {
    "LYG-上-T026": {
        "title": "1949~1990年部分年份连云港市果树面积、产量统计表",
        "table_number": "表9-5",
        "status": "pending-source-check",
        "notes": "表题/表号已据OCR文本补正；数据行存在错位疑点，待回源核录；不得作为主交付入口",
    },
    "LYG-上-T032": {
        "title": "1990年连云港市海洋捕捞分品种产量统计表",
        "table_number": "表12-6",
    },
    "LYG-上-T033": {
        "title": "1990年连云港市部分水产冷冻加工企业基本情况表",
        "table_number": "表12-12",
    },
}


def patch_entry(entry: dict) -> bool:
    table_id = entry.get("table_id")
    patch = PATCHES.get(table_id)
    if not patch:
        return False
    changed = False
    for key, value in patch.items():
        if entry.get(key) != value:
            entry[key] = value
            changed = True
    return changed


def patch_json_files() -> int:
    count = 0
    for table_id in PATCHES:
        path = DATA_DIR / f"{table_id}.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        if patch_entry(data):
            path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            count += 1
    return count


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
        payload = json.dumps(tables, ensure_ascii=False)
        text = text[: match.start(1)] + payload + text[match.end(1) :]
        SITE.write_text(text, encoding="utf-8")
    return changed


def main() -> None:
    print(f"json_files_changed={patch_json_files()}")
    print(f"site_entries_changed={patch_site()}")


if __name__ == "__main__":
    main()
