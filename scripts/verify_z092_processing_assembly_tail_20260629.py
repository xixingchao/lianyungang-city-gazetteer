# -*- coding: utf-8 -*-
"""Verify LYG-中-T092 processing assembly project continuation table from raw OCR."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
DATA = ROOT / "workbench" / "table_entries" / "中" / "data" / "LYG-中-T092.json"

COLUMNS = ["年份", "序号", "批准备案号", "项目内容", "承接单位", "外方单位", "加工费用总额(万元)", "单价", "数量"]
ROWS = [
    ["1989", "15", "89苏外经贸来（连）字第001号", "仪器仪表接插件", "连云港市无线电元件厂", "香港华茂实业公司", "1.00", "0.20元", "50000只"],
    ["1989", "16", "89苏外经贸来（连）字第002号", "废蓄电瓶加工", "连云港市裸铜线厂", "美国联合资源公司", "5.00", "565元/吨", "2600吨"],
    ["1989", "17", "89苏外经贸来（连）字第003号", "废杂电机加工", "连云港市裸铜线厂", "美国联合资源公司", "5.00", "680元/吨", "4800吨"],
    ["1990", "18", "90苏外经贸来（连）字第001号", "丝绢绸和服面料", "开发区苏锦绣品工艺公司", "日本丸荣贸易株式会社", "6.13", "245元/件", "250件"],
    ["1990", "19", "90苏外经贸来（连）字第002号", "白色相良绣", "开发区苏锦绣品工艺公司", "日本丸荣贸易株式会社", "0.83", "55元/件", "150件"],
    ["1990", "20", "90苏外经贸来（连）字第003号", "白色相良绣", "开发区苏锦绣品工艺公司", "日本丸荣贸易株式会社", "2.00", "67元/件", "300件"],
    ["1990", "21", "90苏外经贸来（连）字第004号", "白色相良绣", "开发区苏锦绣品工艺公司", "日本丸荣贸易株式会社", "1.65", "55元/件", "300件"],
    ["1990", "22", "90苏外经贸来（连）字第005号", "废蓄电瓶加工", "连云港市裸铜线厂", "美国联合资源公司", "3.00", "420元/吨", "3600吨"],
    ["1990", "23", "90苏外经贸来（连）字第006号", "系列服装加工", "连云港农垦公司", "美国联合资源公司", "3.92", "", ""],
]

PATCH = {
    "title": "1984~1990年连云港市批准来料加工装配项目表（续表）",
    "table_number": "表35-9",
    "page": 1623,
    "pages": [1623],
    "columns": COLUMNS,
    "rows": ROWS,
    "row_count": len(ROWS),
    "col_count": len(COLUMNS),
    "status": "verified",
    "notes": "已据raw OCR回源核录：workbench/table_entries/中/raw/LYG-中-T092_1623.txt；原JSON标题误抽为“仪器仪表接插件”。本页为表35-9续表；第23项单价、数量OCR未见，保留空值，未猜补。",
}


def patch_entry(entry: dict) -> bool:
    if entry.get("table_id") != "LYG-中-T092":
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
