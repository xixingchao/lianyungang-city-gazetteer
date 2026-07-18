# -*- coding: utf-8 -*-
"""Verify main adhesive product output table T025."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
DATA = ROOT / "workbench" / "table_entries" / "中" / "data" / "LYG-中-T025.json"

COLUMNS = [
    "年份",
    "工业明胶(吨)",
    "田菁胶粉(吨)",
    "聚醋酸乙烯乳液(吨)",
    "聚乙烯醇缩丁醛(吨)",
    "EVA热熔胶(吨)",
    "EVAL粉末(吨)",
    "305树脂胶(吨)",
    "人造毛皮防风胶(吨)",
    "强化合成胶(吨)",
]

ROWS = [
    ["1972", "46", "", "", "", "", "", "", "", ""],
    ["1973", "128", "", "", "", "", "", "", "", ""],
    ["1974", "41", "50", "", "", "", "", "", "", ""],
    ["1975", "106", "50", "", "", "", "", "", "", ""],
    ["1976", "103", "100", "", "", "", "", "", "", ""],
    ["1977", "973", "100", "", "", "", "", "", "", ""],
    ["1978", "815", "100", "", "", "", "", "", "", ""],
    ["1979", "536", "48", "100", "", "", "", "", "", ""],
    ["1980", "976", "24", "100", "202", "", "", "", "", ""],
    ["1981", "1531", "33", "21", "100", "", "", "", "", "150"],
    ["1982", "2650", "62", "30", "14", "", "", "100", "", "246"],
    ["1983", "2758", "31", "89", "2", "22", "", "100", "100", "270"],
    ["1984", "2552", "52", "111", "54", "38", "27", "100", "120", "338"],
    ["1985", "2862", "19", "127", "399", "190", "28", "100", "150", "360"],
    ["1986", "2326", "146", "46", "148", "66", "50", "250", "", "514"],
    ["1987", "1835", "230", "82", "187", "54", "50", "500", "", "592"],
    ["1988", "1717", "45", "496", "114", "249", "11", "870", "", "451"],
    ["1989", "984", "58", "650", "232", "211", "301", "580", "", "416"],
    ["1990", "1927", "17", "372", "121", "248", "446", "50", "450", "412"],
]

PATCH = {
    "table_id": "LYG-中-T025",
    "title": "1972~1990年连云港市主要胶粘剂产量统计表",
    "table_number": "表20-12",
    "page": 1083,
    "pages": [1083],
    "part": "part01",
    "vol": "中",
    "volume": "中",
    "columns": COLUMNS,
    "rows": ROWS,
    "row_count": len(ROWS),
    "col_count": len(COLUMNS),
    "status": "verified",
    "notes": "已据页级OCR回源核录：workbench/ocr/paddle_ocr/中/part01/page_0180.txt，并参考 raw OCR workbench/table_entries/中/raw/LYG-中-T025_1083.txt。原JSON为单列骨架；源页未见数值的单元格保留空值，未补作0。",
}


def patch_entry(entry: dict) -> bool:
    if entry.get("table_id") != PATCH["table_id"]:
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
    changed = sum(1 for table in tables if patch_entry(table))
    if changed:
        text = text[: match.start(1)] + json.dumps(tables, ensure_ascii=False) + text[match.end(1) :]
        SITE.write_text(text, encoding="utf-8")
    return changed


def main() -> None:
    print(f"json_files_changed={patch_json()}")
    print(f"site_entries_changed={patch_site()}")


if __name__ == "__main__":
    main()
