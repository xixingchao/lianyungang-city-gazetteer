# -*- coding: utf-8 -*-
"""Verify planned material allocation continuation table T103."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
DATA = ROOT / "workbench" / "table_entries" / "中" / "data" / "LYG-中-T103.json"

COLUMNS = [
    "年份",
    "煤炭(吨)",
    "石油(吨)",
    "钢材(吨)",
    "生铁(吨)",
    "有色金属(吨)",
    "木材(立方米)",
    "机电产品(万元)",
]

ROWS = [
    ["1966", "232401", "14761", "3268", "", "", "", ""],
    ["1967", "181000", "13066", "20347", "130", "", "", ""],
    ["1968", "179000", "7649", "6701", "55", "", "26136", "243"],
    ["1969", "210000", "9036", "5008", "56", "", "", ""],
    ["1970", "277055", "16180", "4468", "3150", "14379", "", "354"],
    ["1971", "265086", "22408", "6308", "3244", "9502", "", "457"],
    ["1972", "290266", "25544", "6451", "3303", "19152", "", "609"],
    ["1973", "294976", "33909", "7919", "3484", "20752", "", "640"],
    ["1974", "234429", "34016", "4928", "1410", "45", "20131", "545"],
    ["1975", "358923", "45315", "6667", "2380", "81", "27948", "520"],
    ["1976", "395511", "52556", "4046", "2502", "83", "22804", "505"],
    ["1977", "463452", "66568", "7522", "3499", "127", "34941", "673"],
    ["1978", "664380", "70894", "9906", "3271", "125", "27282", "755"],
    ["1979", "684681", "18364", "3819", "", "143", "31615", "581"],
    ["1980", "678183", "18945", "4366", "", "199", "31186", "751"],
    ["1981", "176596", "18828", "1080", "190", "", "21740", "807"],
    ["1982", "218295", "22884", "5655", "226", "", "18694", "1256"],
    ["1983", "180853", "16319", "4075", "533", "", "25810", "1251"],
    ["1984", "207010", "24999", "5171", "402", "", "38234", "1426"],
    ["1985", "248485", "40584", "4062", "570", "", "36851", "1858"],
    ["1986", "519541", "43593", "6265", "577", "", "37176", "3111"],
    ["1987", "431917", "51219", "6284", "748", "", "13452", "4112"],
    ["1988", "382217", "46280", "5187", "1050", "", "11450", "5941"],
    ["1989", "340825", "38933", "11457", "709", "", "3079", "3880"],
    ["1990", "351096", "39341", "14221", "1406", "", "3139", "4812"],
]

PATCH = {
    "table_id": "LYG-中-T103",
    "title": "1965~1990年分配连云港市主要计划物资表（续表）",
    "table_number": "表37-1",
    "page": 1686,
    "pages": [1686],
    "part": "part02",
    "vol": "中",
    "volume": "中",
    "columns": COLUMNS,
    "rows": ROWS,
    "row_count": len(ROWS),
    "col_count": len(COLUMNS),
    "status": "verified",
    "notes": "已据页级OCR回源核录：表题、表号和表头见 workbench/ocr/paddle_ocr/中/part02/page_0265.txt；续表内容见 workbench/ocr/paddle_ocr/中/part02/page_0266.txt，并参考 raw OCR workbench/table_entries/中/raw/LYG-中-T103_1686.txt。原JSON为单列骨架且标题误抽为农村集体储备粮统计表；源页未见数值的单元格保留空值，未猜补。",
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
