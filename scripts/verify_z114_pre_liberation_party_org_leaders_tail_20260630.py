# -*- coding: utf-8 -*-
"""Verify table 41-1 continuation from page OCR."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
DATA_DIR = ROOT / "workbench" / "table_entries" / "中" / "data"

PATCHES = {
    "LYG-中-T114": {
        "title": "解放前中共海属地区地方组织负责人表（续表）",
        "table_number": "表41-1",
        "page": 1823,
        "pages": [1823],
        "columns": ["组织名称", "职务", "姓名", "籍贯", "任职时间"],
        "rows": [
            ["中共海州市委", "书记", "华诚一", "河北赞皇", "民国34年8~10月"],
            ["中共新海(新浦)工委", "书记", "吕剑光", "山东泰安", "民国34年10月~民国35年3月"],
            ["中共海州市委", "书记", "于化琪", "江苏灌云", "民国35年3月~民国37年3月"],
            ["中共新海工委", "书记", "李玉山", "山东沂水", "民国37年3~4月"],
            ["中共新海工委", "书记", "许耀林", "山东日照", "民国37年4~9月"],
            ["中共新海工委", "书记", "梁如仁", "江苏东海", "民国37年10~11月"],
            ["中共淮北盐场特区委", "书记", "杜李", "河南济源", "民国35年11月~民国36年12月"],
            ["中共两淮盐场特区委", "书记", "杜李", "河南济源", "民国36年12月~民国37年10月"],
            ["中共淮北盐场特区委", "书记", "杜李", "河南济源", "民国37年10~11月"],
        ],
        "status": "verified",
        "notes": "已据页级OCR回源核录：workbench/ocr/paddle_ocr/中/part02/page_0403.txt，并参考 raw OCR：workbench/table_entries/中/raw/LYG-中-T114_1823.txt。表题和表号依据前页 workbench/ocr/paddle_ocr/中/part02/page_0402.txt；本页为表41-1续上表。raw OCR存在列序漂移，本轮按页级OCR的表头顺序归并为组织名称、职务、姓名、籍贯、任职时间。",
    }
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
    print(f"json_files_changed={patch_json()}")
    print(f"site_entries_changed={patch_site()}")


if __name__ == "__main__":
    main()
