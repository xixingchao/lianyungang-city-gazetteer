# -*- coding: utf-8 -*-
"""Verify Guanyun county road overview head table T056."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
DATA = ROOT / "workbench" / "table_entries" / "中" / "data" / "LYG-中-T056.json"

COLUMNS = [
    "类别",
    "起讫站点",
    "经过集镇",
    "里程(公里)",
    "路面宽度(米)",
    "修筑年份",
    "备注",
]

ROWS = [
    ["云台线", "贾圩桥一猴嘴", "新滩、大村、小村", "12.8", "3.5~5.5", "1979", ""],
    ["新坝东线", "陶湾一孙庄桥", "狮树、小荡", "14.6", "3.5", "1980", ""],
    ["新坝西线", "吉庄一新坝", "", "8.4", "5.5", "1981", "原通至6072部队营房"],
    ["朱麻线", "大岛山", "隔村、朱麻", "7.7", "5.5", "1982", ""],
    ["东连岛线", "水岛一白沙", "东连岛、水岛", "11.4", "", "", ""],
    ["云台山东线", "连云港一大桅尖", "东山嘴、黄窝", "7.9", "", "", ""],
    ["云台山西线", "宿城一大枪尖", "小庄", "9.1", "", "", ""],
    ["孟陬线", "孟河一东陬山", "伊芦、同兴", "38.8", "3.5", "", "1957~1958年筑成土面公路。1971年孟河至圩丰，1988年圩丰到东陬山铺筑沙石路面"],
    ["伊新线", "伊山镇一新坝", "陡沟、龙苴、穆圩", "31.5", "3.5", "", "1956年、1958年、1963年、1979年分段筑成土面公路，1972年、1981年分段铺为沙石路面"],
    ["伊龙线", "伊山镇一龙苴", "董集、大圩桥", "25.0", "3.5", "", "1958年筑成土面公路，1966年、1972年、1978年分段铺为沙石路"],
    ["仲下线", "仲集一下车", "", "6.5", "", "", "1958年筑成土面公路，1972年铺为沙石路"],
    ["西东线", "西山一东辛农场", "东辛乡", "18.0", "3.5", "", "1958年筑成土面公路，1972年西山至东乡铺为沙石路"],
    ["伊王沂线", "伊山镇一沂北", "东王集", "21.0", "35", "", "1958年、1970年分段筑成土面公路，1973年、1986年分段铺为沙石路"],
    ["云张线", "云台农场一张圩坨", "东辛农场", "20.0", "3.5", "", "1956年筑成土面公路，1964年铺为沙石路"],
    ["八圩线", "八道沟一圩丰", "", "11.0", "3.5", "", "1966年筑成土面公路，1988年铺为沙石路"],
]

PATCH = {
    "table_id": "LYG-中-T056",
    "title": "1990年灌云县县级公路概况表",
    "table_number": "表30-4",
    "page": 1445,
    "pages": [1445],
    "part": "part02",
    "vol": "中",
    "volume": "中",
    "columns": COLUMNS,
    "rows": ROWS,
    "row_count": len(ROWS),
    "col_count": len(COLUMNS),
    "status": "verified",
    "notes": "已据页级OCR回源核录：表题、表号、表头和首页内容见 workbench/ocr/paddle_ocr/中/part02/page_0025.txt，并参考 raw OCR workbench/table_entries/中/raw/LYG-中-T056_1445.txt。原JSON为单列骨架；页顶东海县县级公路概况续行未并入本条。长备注中的筑路年份保留在备注列；伊王沂线路面宽度 OCR 读作 35，本次按 OCR 文本保留。",
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
