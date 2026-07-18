# -*- coding: utf-8 -*-
"""Verify LYG-下-T018 lawyer business statistics continuation."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
DATA = ROOT / "workbench" / "table_entries" / "下" / "data" / "LYG-下-T018.json"

COLUMNS = ["项目", "1980", "1981", "1982", "1983", "1984", "1985", "1986", "1987", "1988", "1989", "1990", "合计"]

ROWS = [
    ["法律顾问单位(个)", "", "", "", "27", "64", "71", "163", "244", "254", "254", "210", "1041"],
    ["办理法律事务", "", "", "", "2", "194", "254", "709", "632", "742", "", "408", "2951"],
    ["索赔和避免经济损失合计(万元)", "", "", "", "12.17", "56.20", "969.40", "1928.20", "2721.40", "3130.39", "1902.20", "1972.51", "12692.47"],
    ["索赔和避免经济损失-民事代理", "", "", "", "8.67", "55.70", "236.80", "483.90", "946.70", "2163.29", "1684.00", "1712.91", "7291.97"],
    ["索赔和避免经济损失-非诉讼事务", "", "", "", "3.50", "0.50", "532.60", "554.30", "589.70", "947.10", "218.20", "230.60", "3076.50"],
    ["索赔和避免经济损失-涉外法律事务", "", "", "", "", "", "192", "200", "890", "", "20", "29", "1331"],
    ["索赔和避免经济损失-法律顾问", "", "", "", "", "", "", "", "1185", "", "", "", "1192"],
    ["解答法律咨询(人次)", "860", "816", "2049", "1323", "2148", "3576", "2650", "4365", "4605", "", "4513", "26905"],
    ["代写法律文书(份)", "108", "95", "252", "160", "459", "655", "874", "699", "791", "", "470", "4563"],
    ["业务收支-收入(万元)", "0.19", "0.27", "0.60", "1.23", "12.40", "27.26", "40.07", "52.80", "71.36", "", "77.75", "283.94"],
    ["业务收支-支出(万元)", "", "0.02", "0.06", "0.04", "5.74", "13.71", "17.12", "23.69", "43.91", "", "40.36", "144.65"],
]

PATCH = {
    "title": "1980~1990年连云港市律师业务综合统计表续表",
    "table_number": "表44-37",
    "page": 2116,
    "pages": [2116],
    "part": "part01",
    "vol": "下",
    "volume": "下",
    "columns": COLUMNS,
    "rows": ROWS,
    "row_count": len(ROWS),
    "col_count": len(COLUMNS),
    "status": "verified",
    "notes": "已据页级OCR核录：workbench/ocr/paddle_ocr/下/part01/page_0145.txt；表题、表号和年份表头承接前页 workbench/ocr/paddle_ocr/下/part01/page_0144.txt。并参考 raw 坐标OCR workbench/ocr/raw/下/part01/page_0145.json 与 raw 文本 workbench/table_entries/下/raw/LYG-下-T018_2116.txt。本条原题名串章为医药系统获奖产品一览表，实际为表44-37续页；仅录入 page_0145 可见续表项目，源页未见数值处保留空值。",
}


def patch_entry(entry: dict) -> bool:
    if entry.get("table_id") != "LYG-下-T018":
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
