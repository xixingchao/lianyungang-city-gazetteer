# -*- coding: utf-8 -*-
"""Verify table 47-5 wage-point conversion table from page OCR."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
DATA_DIR = ROOT / "workbench" / "table_entries" / "下" / "data"

PATCHES = {
    "LYG-下-T037": {
        "title": "新海连市工资分与实物折价对照计算表",
        "table_number": "表47-5",
        "page": 2229,
        "pages": [2229],
        "columns": [
            "品名",
            "市价(旧人民币元)",
            "每分含量-实物数量",
            "每分含量-折合人民币(旧人民币元)",
            "备注",
        ],
        "rows": [
            ["小麦", "2500", "1市斤", "2500", "此表按民国38年6月28日市场牌价，每一工资分按14448.5元(旧人民币)计算。"],
            ["小米", "2903", "2市斤", "5806", ""],
            ["土布", "2400", "1市尺", "3400", ""],
            ["豆油", "22500", "5钱", "703.125", ""],
            ["盐", "1260", "5钱", "39.375", ""],
            ["煤", "1000", "2市斤", "2000", ""],
            ["合计", "", "", "14448.5", ""],
        ],
        "status": "verified",
        "notes": "已据页级OCR回源核录：workbench/ocr/paddle_ocr/下/part01/page_0258.txt，并参考 raw OCR：workbench/table_entries/下/raw/LYG-下-T037_2229.txt。原JSON标题误列为乡镇企业水泥瓦产量统计表；本页实际为表47-5，新海连市工资分与实物折价对照计算表，民国38年7月8日制。备注为跨行竖排文字，本轮合并为完整句。",
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
