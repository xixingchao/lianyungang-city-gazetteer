# -*- coding: utf-8 -*-
"""Verify LYG-上-T043 against page-level OCR and mark it deliverable."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
DATA = ROOT / "workbench" / "table_entries" / "上" / "data" / "LYG-上-T043.json"

COLUMNS = ["企业名称", "工业总产值(万元)", "销售收入(万元)", "利税(万元)", "固定资产原值(万元)", "职工人数(人)"]
ROWS = [
    ["连云港涤纶厂", "15041", "10621", "2150", "6882", "1082"],
    ["连云港市纺织厂", "7417", "6512", "536", "2405", "2596"],
    ["连云港市麻纺厂", "2176", "2627", "-245", "1768", "2226"],
    ["连云港市毛巾厂", "3920", "2742", "-65", "2258", "1800"],
    ["连云港色织一厂", "2740", "1372", "-415", "2063", "1283"],
    ["连云港市床单厂", "220", "356", "-190", "476", "526"],
    ["连云港市针织内衣厂", "543", "349", "-227", "1200", "568"],
    ["连云港市经纬编一厂", "1108", "463", "-246", "965", "436"],
    ["连云港市针织一厂", "629", "465", "-90", "567", "610"],
    ["连云港市纺机厂", "82", "131", "-36", "219", "332"],
    ["连云港市针织二厂", "921", "879", "-154", "655", "706"],
    ["连云港市第三毛纺厂", "1560", "1100", "140", "1000", "600"],
    ["连云港市丝织厂", "265", "276", "-108", "1229", "318"],
    ["连云港市鞋帽厂", "133", "123", "-3", "136", "252"],
    ["赣榆县织布厂", "565", "410", "57.4", "62", "349"],
    ["赣榆县针织厂", "200", "265", "-22", "88", "345"],
    ["赣榆县经编厂", "259", "264", "-30", "386", "140"],
    ["赣榆县印染厂", "686", "122", "-27", "569", "144"],
    ["赣榆县丝织厂", "143", "248", "17", "92", "159"],
    ["东海县染织厂", "175", "119", "-35", "178", "199"],
    ["灌云县织布厂", "269", "468", "40", "162", "275"],
]

PATCH = {
    "title": "1990年连云港市纺织工业企业基本情况表",
    "table_number": "表15-10",
    "pages": [875, 876],
    "columns": COLUMNS,
    "rows": ROWS,
    "row_count": len(ROWS),
    "col_count": len(COLUMNS),
    "status": "verified",
    "notes": "已据页级OCR回源核录：上册part03/page_0270-page_0271。注：简介企业不列入此表。",
}


def patch_entry(entry: dict) -> bool:
    if entry.get("table_id") != "LYG-上-T043":
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
