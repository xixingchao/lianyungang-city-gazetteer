# -*- coding: utf-8 -*-
"""Verify LYG-下-T036 labor population continuation page."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
DATA = ROOT / "workbench" / "table_entries" / "下" / "data" / "LYG-下-T036.json"

COLUMNS = [
    "年份",
    "年末社会劳动者(万人)",
    "城镇职工合计(万人)",
    "全民职工(万人)",
    "集体职工(万人)",
    "其他职工(万人)",
    "城镇个体劳动者(万人)",
    "农村劳动者(万人)",
    "年末城镇待业人数(万人)",
]

ROWS = [
    ["1979", "119.01", "26.83", "18.24", "8.59", "0.02", "", "92.16", "1.12"],
    ["1980", "122.18", "28.29", "19.03", "9.26", "0.09", "", "93.80", "0.93"],
    ["1981", "124.17", "29.51", "20.30", "9.21", "0.16", "", "94.50", "1.07"],
    ["1982", "132.57", "30.79", "21.26", "9.53", "0.19", "", "101.59", "0.42"],
    ["1983", "133.30", "30.94", "21.31", "9.63", "0.37", "", "102.23", "0.63"],
    ["1984", "139.07", "32.02", "21.41", "10.61", "0.42", "", "106.63", "0.68"],
    ["1985", "149.62", "33.52", "22.44", "11.04", "0.04", "0.47", "115.63", "0.67"],
    ["1986", "151.64", "34.90", "23.57", "11.29", "0.04", "0.52", "116.22", "0.72"],
    ["1987", "158.20", "36.43", "25.05", "11.24", "0.14", "0.69", "121.08", "0.69"],
    ["1988", "161.63", "37.12", "26.12", "10.82", "0.18", "0.83", "123.68", "0.86"],
    ["1989", "164.79", "37.74", "26.35", "11.04", "0.35", "0.95", "126.10", "1.97"],
    ["1990", "170.70", "38.57", "26.77", "11.42", "0.38", "1.00", "131.13", "1.90"],
]

PATCH = {
    "title": "1949~1990年部分年份连云港市劳动力人口情况统计表（续表）",
    "table_number": "表47-1",
    "page": 2207,
    "pages": [2207],
    "part": "part01",
    "vol": "下",
    "volume": "下",
    "columns": COLUMNS,
    "rows": ROWS,
    "row_count": len(ROWS),
    "col_count": len(COLUMNS),
    "status": "verified",
    "notes": "已据页级OCR核录：workbench/ocr/paddle_ocr/下/part01/page_0236.txt；表题、表号和单位依据前页 workbench/ocr/paddle_ocr/下/part01/page_0235.txt；并参考 raw 文本 workbench/table_entries/下/raw/LYG-下-T036_2207.txt。原JSON题名串章为供电线损率统计表；此条仅录入表47-1续页 1979-1990 年记录，单位为万人。",
}


def patch_entry(entry: dict) -> bool:
    if entry.get("table_id") != "LYG-下-T036":
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
