# -*- coding: utf-8 -*-
"""Normalize continuation-table pending title markers to avoid OCR-glue false positives."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
DATA_ROOT = ROOT / "workbench" / "table_entries"
OLD = "(续表，表题待确认)"
NEW = "续表（表题待确认）"


def patch_entry(entry: dict) -> bool:
    if entry.get("title") == OLD:
        entry["title"] = NEW
        return True
    return False


def patch_json_files() -> int:
    changed = 0
    for path in DATA_ROOT.glob("*/data/LYG-*-T*.json"):
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
