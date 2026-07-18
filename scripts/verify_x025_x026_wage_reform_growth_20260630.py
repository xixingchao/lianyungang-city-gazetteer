# -*- coding: utf-8 -*-
"""Verify table 46-9 wage reform growth pages from page OCR."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
DATA_DIR = ROOT / "workbench" / "table_entries" / "下" / "data"
COLUMNS = [
    "职别",
    "总人数(人)",
    "升级人数(人)",
    "其中升二级人数(人)",
    "升级人数占总人数(%)",
    "工资改革前工资总数(元)",
    "工资改革前平均工资(元)",
    "工资改革后工资总数(元)",
    "工资改革后平均工资(元)",
    "月增长工资数(元)",
    "月增长(%)",
]

PATCHES = {
    "LYG-下-T025": {
        "title": "1956年底新海连市国家机关工资改革后各类人员工资增长情况表",
        "table_number": "表46-9",
        "page": 2178,
        "pages": [2178],
        "columns": COLUMNS,
        "rows": [
            ["合计", "1063", "656", "31", "61.71", "49049.38", "46.14", "57458.00", "54.05", "8408.62", "17.14"],
            ["书记市长", "10", "9", "", "90.00", "1076.96", "107.75", "1324.50", "132.45", "247.54", "22.99"],
            ["部长", "26", "18", "", "69.23", "2107.28", "81.05", "2543.00", "97.81", "435.72", "20.68"],
            ["科局长", "82", "54", "3", "65.85", "5722.94", "69.79", "6831.50", "83.31", "108.56", "19.37"],
            ["局下科长", "111", "79", "3", "71.17", "6409.82", "57.75", "7574.00", "68.23", "1164.18", "18.16"],
        ],
        "status": "verified",
        "notes": "已据页级OCR回源核录：workbench/ocr/paddle_ocr/下/part01/page_0207.txt，并参考 raw OCR：workbench/table_entries/下/raw/LYG-下-T025_2178.txt。原JSON标题误列为胶粘剂产量表；本页实际为表46-9首页，单位为元。书记市长、部长行的其中升二级人数源页未见数字，保留空值，未猜补。",
    },
    "LYG-下-T026": {
        "title": "1956年底新海连市国家机关工资改革后各类人员工资增长情况表（续表）",
        "table_number": "表46-9",
        "page": 2179,
        "pages": [2179],
        "columns": COLUMNS,
        "rows": [
            ["股长科员", "260", "151", "6", "58.08", "11969.52", "46.04", "13804.50", "53.09", "1834.98", "15.33"],
            ["一般干部", "279", "179", "8", "64.16", "10305.32", "36.94", "12132.00", "43.48", "1826.68", "17.73"],
            ["勤杂人员", "26", "18", "1", "69.23", "697.48", "26.83", "825.00", "31.73", "127.52", "18.28"],
            ["汽车司机", "3", "2", "", "66.67", "151.58", "50.53", "182.50", "60.83", "30.92", "20.40"],
            ["炊事员", "34", "21", "", "61.76", "1047.28", "30.80", "1230.00", "36.18", "182.72", "17.45"],
            ["人民警察", "232", "125", "10", "53.88", "9561.20", "41.21", "11011.00", "47.46", "1449.80", "15.16"],
        ],
        "status": "verified",
        "notes": "已据页级OCR回源核录：workbench/ocr/paddle_ocr/下/part01/page_0208.txt，并参考 raw OCR：workbench/table_entries/下/raw/LYG-下-T026_2179.txt。表题和表号依据前页 workbench/ocr/paddle_ocr/下/part01/page_0207.txt；本页为表46-9续上表，单位为元。汽车司机、炊事员行的其中升二级人数源页未见数字，保留空值，未猜补。",
    },
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
