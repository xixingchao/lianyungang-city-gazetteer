# -*- coding: utf-8 -*-
"""Verify salt-field output tables 13-7 and 13-8 continuation."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
DATA_DIR = ROOT / "workbench" / "table_entries" / "上" / "data"

PRE1949_COLUMNS = ["年份(民国)", "涛青场(吨)", "板浦场(吨)", "中正场(吨)", "济南场(吨)", "合计(吨)"]
POST1949_COLUMNS = ["年份", "青口盐场(吨)", "台北盐场(吨)", "台南盐场(吨)", "徐圩盐场(吨)", "灌西盐场(吨)", "合计(吨)"]

PATCHES = {
    "LYG-上-T035": {
        "title": "民国13~36年(1924~1947年)部分年份连云港市境内各盐场年产量统计表",
        "table_number": "表13-7",
        "pages": [743, 745],
        "columns": PRE1949_COLUMNS,
        "rows": [
            ["13", "42906", "78600", "93500", "325650", "540656"],
            ["14", "32050", "81350", "65350", "246350", "425100"],
            ["15", "15950", "74350", "52450", "220400", "363150"],
            ["16", "14100", "89400", "46250", "199900", "349650"],
            ["17", "21000", "93450", "48400", "244250", "407100"],
            ["18", "20550", "105500", "51000", "348250", "525300"],
            ["19", "7650", "30400", "35000", "21450", "94500"],
            ["20", "24500", "47800", "53700", "86650", "212650"],
            ["21", "44250", "83300", "116850", "168650", "413050"],
            ["22", "33250", "67550", "84000", "90200", "275000"],
            ["23", "30800", "88500", "121300", "149400", "390000"],
            ["24", "44050", "127400", "200600", "306900", "678950"],
            ["25", "32100", "53250", "105200", "135400", "325950"],
            ["28", "8550", "12700", "13050", "12600", "46900"],
            ["29", "19050", "73950", "7050", "42950", "143000"],
            ["30", "9750", "92100", "62400", "80800", "245050"],
            ["31", "13450", "85950", "47050", "107500", "253950"],
            ["32", "12900", "64200", "45250", "80250", "202600"],
            ["33", "14900", "89600", "72700", "57800", "235000"],
            ["34", "8500", "70950", "104550", "2600", "186600"],
            ["35", "", "", "49736", "18344", ""],
            ["36", "127", "53859", "94789", "6640", "155542"],
        ],
        "status": "verified",
        "notes": "已据页级OCR回源核录：workbench/ocr/paddle_ocr/上/part03/page_0144.txt，并参考 raw OCR：workbench/table_entries/上/raw/LYG-上-T036_749.txt。原JSON列序误置为合计在前，本轮按源页列序重录为年份、涛青场、板浦场、中正场、济南场、合计，单位为吨。民国35年仅见中正场49736、济南场18344，其他栏及合计栏保留空值；民国36年各值按坐标OCR列位核定。",
    },
    "LYG-上-T036": {
        "title": "1949~1990年连云港市境内国营盐场产量统计表（续表）",
        "table_number": "表13-8",
        "pages": [749, 751, 754, 756],
        "columns": POST1949_COLUMNS,
        "rows": [
            ["1980", "77288", "251927", "191484", "202032", "205442", "928173"],
            ["1981", "92980", "287035", "186257", "197039", "205374", "968685"],
            ["1982", "98804", "258984", "182604", "195123", "191366", "926881"],
            ["1983", "86661", "277328", "186208", "183665", "193360", "927222"],
            ["1984", "91552", "252536", "192425", "181375", "195822", "913710"],
            ["1985", "76690", "254951", "193061", "190798", "190800", "906300"],
            ["1986", "79916", "275106", "211165", "226542", "205818", "998547"],
            ["1987", "83802", "275215", "233843", "245233", "206184", "1044277"],
            ["1988", "86290", "271393", "234603", "221825", "201930", "1016041"],
            ["1989", "92000", "339026", "268014", "279011", "258478", "1236529"],
            ["1990", "78974", "233000", "214000", "184762", "143276", "854012"],
        ],
        "status": "verified",
        "notes": "已据页级OCR回源核录：workbench/ocr/paddle_ocr/上/part03/page_0146.txt，并参考 raw OCR：workbench/table_entries/上/raw/LYG-上-T036_749.txt。表题、表号和单位依据前页 workbench/ocr/paddle_ocr/上/part03/page_0145.txt；本页为表13-8续上表，单位为吨。原JSON列序与源页不一致，本轮按源页列序重录为年份、青口盐场、台北盐场、台南盐场、徐圩盐场、灌西盐场、合计。",
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
