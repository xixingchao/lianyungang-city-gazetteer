# -*- coding: utf-8 -*-
"""Verify LYG-上-T028 medium reservoir structure table."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
DATA = ROOT / "workbench" / "table_entries" / "上" / "data" / "LYG-上-T028.json"

COLUMNS = [
    "水库名称",
    "大坝名称",
    "坝顶长度(米)",
    "坝顶高程(米)",
    "坝顶宽度(米)",
    "最大坝高(米)",
    "泄洪设施名称",
    "孔数(个)",
    "每孔净宽(米)",
    "每孔净高(米)",
    "洞底高程或堰顶高程(米)",
    "设计最大流量(立方米/秒)",
]

ROWS = [
    ["八条路", "大坝", "920", "34.7", "6", "13.4", "北溢洪闸", "7", "4.0", "", "30.0", "250"],
    ["八条路", "", "", "", "", "", "内溢洪闸", "3", "4.0", "", "30.0", "112"],
    ["横沟", "大坝", "1950", "30.5", "5", "12.5", "溢洪闸", "4", "2.5", "", "25.9", "50"],
    ["横沟", "", "", "", "", "", "泄洪涵洞", "5", "2.0", "2.6", "22.5", "106"],
    ["房山", "主坝", "1700", "13.0", "7", "8.2", "溢洪闸", "7", "2.0", "", "9.15", "58"],
    ["房山", "副坝", "1800", "12.5", "7", "4.0", "泄洪涵洞", "5", "2.0", "2.0", "4.5", "110"],
    ["贺庄", "大坝", "3600", "42.0", "6", "8.0", "泄洪涵洞", "5", "2.0", "2.0", "32.5", "132"],
    ["贺庄", "", "", "", "", "", "尤塘泄洪闸", "2", "3.5", "3.0", "34.0", "112"],
    ["西双湖", "东坝", "2250", "34.5", "8", "11.5", "东坝泄洪闸", "2", "2.8", "2.35", "29.15", "99"],
    ["西双湖", "南坝", "2500", "34.5", "8", "4.5", "南坝泄洪闸", "3", "2.5", "3.45", "30.15", "61"],
    ["西双湖", "北坝", "2500", "34.5", "8", "9.5", "", "", "", "", "", ""],
    ["西双湖", "西坝", "2250", "34.5", "6", "4.5", "", "", "", "", "", ""],
    ["西双湖", "湖心堤", "2500", "34.5", "8", "5.0", "", "", "", "", "", ""],
    ["昌梨", "主坝", "1800", "52.0", "6", "15.0", "溢洪闸", "3", "3.0", "4.0", "46.0", "123"],
    ["昌梨", "副坝", "650", "52.0", "3", "4.4", "", "", "", "", "", ""],
    ["大石埠", "大坝", "881", "54.0", "6", "11.7", "溢洪闸", "10", "6.0", "", "47.0", "910"],
    ["大石埠", "", "", "", "", "", "泄洪涵洞", "5", "2.0", "2.0", "43.0", "147"],
    ["羽山", "大坝", "2700", "52.0", "8", "15.0", "泄洪涵洞", "2", "2.0", "2.0", "41.0", "48"],
]

PATCH = {
    "title": "1990年连云港市中型水库主要建筑物情况表",
    "table_number": "表10-6",
    "page": 581,
    "pages": [581, 582],
    "part": "part02",
    "vol": "上",
    "volume": "上",
    "columns": COLUMNS,
    "rows": ROWS,
    "row_count": len(ROWS),
    "col_count": len(COLUMNS),
    "status": "verified",
    "notes": "已据页级OCR核录：workbench/ocr/paddle_ocr/上/part02/page_0281.txt、workbench/ocr/paddle_ocr/上/part02/page_0282.txt；并参考 raw 坐标 OCR：workbench/ocr/raw/上/part02/page_0281.json、workbench/ocr/raw/上/part02/page_0282.json 与 raw 文本 workbench/table_entries/上/raw/LYG-上-T028_581.txt。表10-6实际止于 page_0282 注释前，本条仅录入中型水库主要建筑物情况表；同页后续表10-7未并入。源页左右复合表头已展开为大坝与泄洪设施字段；一个水库对应多项泄洪设施时按源页分行保留。",
}


def patch_entry(entry: dict) -> bool:
    if entry.get("table_id") != "LYG-上-T028":
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
