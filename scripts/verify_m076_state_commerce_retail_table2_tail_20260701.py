# -*- coding: utf-8 -*-
"""Verify LYG-中-T076 state commerce retail table (II) continuation."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
DATA = ROOT / "workbench" / "table_entries" / "中" / "data" / "LYG-中-T076.json"

COLUMNS = [
    "年份",
    "绸缎(万米)",
    "汗背心(百件)",
    "棉毛衫(百件)",
    "棉毛裤(百件)",
    "毛线(百公斤)",
    "胶鞋(百双)",
    "皮鞋(百双)",
    "毛巾(百条)",
    "火柴(百件)",
    "肥皂(百箱)",
    "洗衣粉(吨)",
    "暖水瓶(百只)",
]

ROWS = [
    ["1971", "16", "1741", "911", "626", "184", "1890", "", "2323", "", "206", "33", "572"],
    ["1972", "10", "2128", "754", "563", "115", "2118", "", "2804", "68", "261", "", "470"],
    ["1973", "20", "2504", "645", "571", "198", "2656", "", "4029", "82", "279", "37", "433"],
    ["1974", "23", "2691", "1144", "1448", "278", "3084", "141", "4023", "96", "265", "48", "407"],
    ["1975", "26", "3016", "1146", "918", "289", "2885", "188", "4919", "102", "318", "11", "551"],
    ["1976", "21", "2606", "1329", "878", "338", "3291", "427", "4520", "112", "304", "", "423"],
    ["1977", "29", "2832", "1322", "904", "296", "2878", "711", "5574", "87", "288", "", "738"],
    ["1978", "27", "3317", "2116", "842", "357", "2607", "565", "5874", "96", "250", "", "925"],
    ["1979", "37", "3093", "2769", "748", "492", "2731", "794", "5751", "91", "296", "77", "666"],
    ["1980", "32", "3505", "3245", "953", "717", "2801", "1629", "6319", "109", "355", "73", "706"],
    ["1981", "25", "3463", "3401", "917", "729", "2915", "1678", "6390", "161", "494", "70", "1041"],
    ["1982", "22", "4233", "3208", "824", "820", "8458", "1757", "9158", "133", "465", "180", "696"],
    ["1983", "48", "4053", "2916", "792", "1137", "8558", "3556", "8128", "283", "758", "318", "1312"],
    ["1984", "49", "4568", "3648", "856", "1261", "10999", "2844", "12316", "250", "732", "376", "1450"],
    ["1985", "48", "5392", "5181", "856", "1303", "6922", "2185", "9643", "209", "537", "280", "1483"],
    ["1986", "48", "4972", "5060", "1174", "1446", "6166", "3277", "14302", "159", "569", "455", "1431"],
    ["1987", "47", "4946", "5410", "754", "2181", "7091", "3379", "21091", "119", "537", "652", "1396"],
    ["1988", "39", "4482", "12990", "546", "2764", "4890", "5074", "20136", "317", "587", "1609", "1354"],
    ["1989", "38", "4400", "4899", "416", "2776", "7188", "4133", "14809", "357", "402", "838", "1223"],
    ["1990", "50", "4130", "4501", "553", "2621", "7041", "3983", "7407", "142", "551", "1599", "964"],
]

PATCH = {
    "title": "1949~1990年部分年份连云港市市区国营商业主要商品零售量统计表（二）续表",
    "table_number": "表33-7",
    "page": 1557,
    "pages": [1557],
    "part": "part02",
    "vol": "中",
    "volume": "中",
    "columns": COLUMNS,
    "rows": ROWS,
    "row_count": len(ROWS),
    "col_count": len(COLUMNS),
    "status": "verified",
    "notes": "已据页级OCR核录续页：workbench/ocr/paddle_ocr/中/part02/page_0137.txt；表题、表号和复合表头承接前页 workbench/ocr/paddle_ocr/中/part02/page_0136.txt。并参考 raw 坐标OCR workbench/ocr/raw/中/part02/page_0137.json 与 raw 文本 workbench/table_entries/中/raw/LYG-中-T076_1557.txt。仅录入 page_0137 可见的1971-1990年续表记录；源页未见数值处保留空值；1977年棉毛裤 raw 坐标OCR近形误识为 t06，按页级OCR更正为904。",
}


def patch_entry(entry: dict) -> bool:
    if entry.get("table_id") != "LYG-中-T076":
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
