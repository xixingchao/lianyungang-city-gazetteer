# -*- coding: utf-8 -*-
"""Verify LYG-中-T095 grain and oil purchase storage continuation table."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
DATA = ROOT / "workbench" / "table_entries" / "中" / "data" / "LYG-中-T095.json"

COLUMNS = [
    "年份",
    "合计-粮食(吨)",
    "合计-油脂(吨)",
    "市区-粮食(吨)",
    "市区-油脂(吨)",
    "赣榆县-粮食(吨)",
    "赣榆县-油脂(吨)",
    "东海县-粮食(吨)",
    "东海县-油脂(吨)",
    "灌云县-粮食(吨)",
    "灌云县-油脂(吨)",
]

ROWS = [
    ["1964", "141035", "2510", "4275", "10", "40900", "875", "41515", "1460", "54345", "165"],
    ["1965", "148515", "2520", "6170", "10", "47470", "935", "44160", "1410", "50715", "165"],
    ["1966", "147761", "3465", "8645", "30", "47260", "1375", "35791", "1975", "56065", "85"],
    ["1967", "142450", "5640", "6470", "120", "40950", "2260", "34180", "3090", "60850", "170"],
    ["1968", "162791", "6830", "9570", "15", "48896", "2715", "44100", "3920", "60225", "180"],
    ["1969", "133797", "2885", "7310", "10", "32372", "1640", "40000", "975", "54115", "260"],
    ["1970", "124475", "3930", "6485", "15", "32250", "2090", "33650", "1790", "52090", "35"],
    ["1971", "121460", "3550", "6545", "20", "35720", "1575", "40095", "1935", "39100", "20"],
    ["1972", "140415", "6205", "12875", "5", "38005", "2895", "49360", "3295", "40175", "10"],
    ["1973", "200305", "7435", "14075", "10", "59215", "3420", "69025", "3980", "57990", "25"],
    ["1974", "148355", "5585", "12720", "", "37495", "2325", "49920", "3225", "48220", "35"],
    ["1975", "198750", "6845", "12725", "40", "54510", "3145", "72105", "3650", "59410", "10"],
    ["1976", "181675", "2315", "12010", "", "46890", "765", "63765", "1485", "59010", "65"],
    ["1977", "190225", "3850", "11690", "5", "52030", "1100", "77350", "2620", "49155", "125"],
    ["1978", "223685", "8050", "13840", "", "70405", "3090", "100660", "4885", "38780", "75"],
    ["1979", "339330", "7630", "21005", "", "110540", "3295", "145550", "4230", "62235", "105"],
    ["1980", "384035", "10525", "20655", "5", "112160", "3870", "194425", "6405", "56795", "245"],
    ["1981", "400220", "13125", "17660", "10", "112675", "5700", "207050", "7085", "62835", "330"],
    ["1982", "452024", "14045", "18170", "", "129370", "6730", "243310", "6965", "61174", "350"],
    ["1983", "556425", "12550", "25695", "105", "159705", "5095", "286455", "7205", "84570", "145"],
    ["1984", "646615", "14235", "34285", "340", "152410", "4935", "360625", "8545", "99295", "415"],
]

PATCH = {
    "title": "1953~1984年连云港市粮油征购入库统计表续表",
    "table_number": "表36-3",
    "page": 1637,
    "pages": [1637],
    "part": "part02",
    "vol": "中",
    "volume": "中",
    "columns": COLUMNS,
    "rows": ROWS,
    "row_count": len(ROWS),
    "col_count": len(COLUMNS),
    "status": "verified",
    "notes": "已据页级OCR核录续页：workbench/ocr/paddle_ocr/中/part02/page_0217.txt；表题、表号、单位和复合表头承接前页 workbench/ocr/paddle_ocr/中/part02/page_0216.txt。并参考 raw 坐标OCR workbench/ocr/raw/中/part02/page_0217.json 与 raw 文本 workbench/table_entries/中/raw/LYG-中-T095_1637.txt。仅录入 page_0217 可见的1964-1984年续表记录；源页未见数值处保留空值；1984年市区粮食 raw 坐标OCR尾随句点，按页级OCR记为34285。",
}


def patch_entry(entry: dict) -> bool:
    if entry.get("table_id") != "LYG-中-T095":
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
