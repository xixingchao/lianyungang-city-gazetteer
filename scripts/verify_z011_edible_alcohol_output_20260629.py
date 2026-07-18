# -*- coding: utf-8 -*-
"""Verify LYG-中-T011 edible alcohol output table."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
DATA = ROOT / "workbench" / "table_entries" / "中" / "data" / "LYG-中-T011.json"

COLUMNS = ["年份", "市葡萄酒厂(吨)", "市酿酒厂(吨)", "赣榆县酒厂(吨)", "东海县酒厂(吨)", "灌云县酒厂(吨)"]
ROWS = [
    ["1976", "274", "", "", "", ""],
    ["1977", "408", "24", "", "", ""],
    ["1978", "458", "310", "", "", ""],
    ["1979", "870", "200", "", "", ""],
    ["1980", "883", "118", "", "", ""],
    ["1981", "1198", "6", "394", "", ""],
    ["1982", "1400", "20", "1061", "", "1061"],
    ["1983", "1676", "10", "2897", "250", "1300"],
    ["1984", "1645", "2", "2801", "200", "1312"],
    ["1985", "1877", "1469", "5448", "1890", "1528"],
    ["1986", "1303", "2987", "4242", "1898", "1893"],
    ["1987", "1983", "2924", "5017", "2433", "1626"],
    ["1988", "3720", "3704", "4951", "2404", "1736"],
    ["1989", "3892", "3621", "3652", "1556", "1592"],
    ["1990", "4284", "5242", "3482", "2702", "2121"],
]

PATCH = {
    "title": "1976~1990年连云港市食用酒精产量统计表",
    "table_number": "表18-5",
    "page": 992,
    "pages": [992],
    "columns": COLUMNS,
    "rows": ROWS,
    "row_count": len(ROWS),
    "col_count": len(COLUMNS),
    "status": "verified",
    "notes": "已据页级OCR回源核录：workbench/ocr/paddle_ocr/中/part01/page_0089.txt；原JSON为单列待录入骨架。页首含上一表续段，本轮仅录入表18-5；OCR未列数值的早期厂别单元格保留空值，未猜补。",
}


def patch_entry(entry: dict) -> bool:
    if entry.get("table_id") != "LYG-中-T011":
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
