# -*- coding: utf-8 -*-
"""Verify LYG-中-T079 large catering/accommodation outlets table from raw OCR."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
DATA = ROOT / "workbench" / "table_entries" / "中" / "data" / "LYG-中-T079.json"

COLUMNS = ["企业名称", "营业地址", "隶属系统", "企业性质", "开办年份", "床位张数", "餐厅接待人数"]
ROWS = [
    ["神州宾馆", "海棠路", "市经联公司", "合资", "1987", "171", "220"],
    ["天然居宾馆", "海连中路", "市经联公司", "全民", "1987", "207", "130"],
    ["云台宾馆", "云台路", "市政府接待处", "全民", "1983", "210", "300"],
    ["云华宾馆", "海连东路", "市旅游局", "合资", "1986", "96", "250"],
    ["远洋宾馆", "连云陶庵", "远洋公司", "全民", "1973", "398", "500"],
    ["海州湾宾馆", "中山路", "市商业局", "全民", "1988", "180", "220"],
    ["海棠宾馆", "海棠路", "乡镇企业局", "集体", "1986", "200", "198"],
    ["陇海饭店", "海连中路", "市商业局", "全民", "1978", "400", "920"],
    ["连云饭店", "中山路", "市商业局", "全民", "1977", "210", "211"],
    ["上海饭店", "通灌路", "市白集煤矿", "集体", "1987", "208", "48"],
    ["物华饭店", "通灌路", "市物资局", "全民", "1987", "84", "160"],
    ["东方大酒店", "解放中路", "市供销社", "集体", "1986", "120", "200"],
    ["明珠大酒店", "海连中路", "市商业局", "全民", "1989", "300", "150"],
    ["海云贸易大厦", "海连中路", "新浦区", "全民", "1989", "300", "248"],
    ["振兴大厦", "海连东路", "新浦农场", "全民", "1988", "250", "100"],
    ["第一招待所", "通灌路", "市政府", "全民", "1952", "326", "500"],
]

PATCH = {
    "title": "1990年连云港市市区大型饮服网点一览表",
    "table_number": "表33-15",
    "page": 1577,
    "pages": [1577],
    "columns": COLUMNS,
    "rows": ROWS,
    "row_count": len(ROWS),
    "col_count": len(COLUMNS),
    "status": "verified",
    "notes": "已据raw OCR回源核录：workbench/table_entries/中/raw/LYG-中-T079_1577.txt；页级OCR分卷页码未能稳定定位，本表以raw OCR完整表头和行值为据。",
}


def patch_entry(entry: dict) -> bool:
    if entry.get("table_id") != "LYG-中-T079":
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
