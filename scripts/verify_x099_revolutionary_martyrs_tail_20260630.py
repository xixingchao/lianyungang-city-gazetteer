# -*- coding: utf-8 -*-
"""Verify LYG-下-T099 revolutionary martyrs continuation page."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
DATA = ROOT / "workbench" / "table_entries" / "下" / "data" / "LYG-下-T099.json"

COLUMNS = [
    "姓名", "性别", "出生年月", "籍贯", "参加革命年月", "入党团年月",
    "牺牲时所在军队及其职务", "牺牲时间、地点、原因", "何时何单位授何奖励", "备注",
]

ROWS = [
    ["黄安龙", "男", "1919", "海州区锦屏新海大队袁庄", "1942.8", "", "志愿军三十八军一一三师三三八团五连", "1950年11月朝鲜战场牺牲", "", ""],
    ["程振起", "男", "1925.8", "海州区文化街", "1949", "", "志愿军三十军八十八师三营八连班长", "1950年12月朝鲜下碣隅里战斗牺牲", "1949年立三等功二次", ""],
    ["姚长利", "男", "1921.5", "海州区洪门乡", "1949.5", "", "志愿军二十七军七十九师二三五团三营战士", "1951年1月朝鲜战场失踪", "1962年5月追认", ""],
    ["赵秀锦", "男", "1923.1", "海州区新海街", "1948.12", "团员", "志愿军二十军五十九师文工队员", "1951年在朝鲜战场牺牲", "", ""],
    ["邹松年", "男", "1929", "海州区西门乡", "1948.8", "1949年7月入党", "志愿军三十军八十八师三营八连班长", "1951年朝鲜平津淮战斗牺牲", "1949年5月立三等功、二等功各一次，1950年4月立三等功一次", ""],
    ["李祥元", "男", "1928", "海州区西门乡", "1948.8", "", "志愿军二十军五十九师一七五团战士", "1951年4月在朝鲜战场牺牲", "", ""],
    ["滕士甫", "男", "1926", "海州区锦屏许庄", "1948", "", "志愿军二十六军七十六师炮兵团战士", "1951年4月朝鲜战场牺牲", "", ""],
    ["张厚余", "男", "1922.11", "海州区双龙街", "1949.5", "1949年12月入党", "志愿军十一师炮兵营见习参谋", "1951年5月在朝鲜战场牺牲", "立二等功一次", ""],
    ["汪玉德", "男", "1918.10", "海州区砚池街", "1948.9", "", "志愿军二十六军七十七师二二七团三营战士", "1951年5月抗美援朝战争牺牲在朝鲜", "", ""],
    ["孙庆来", "男", "1930.12", "海州区双池街", "1950.7", "", "志愿军六十军一八零师五三九团油印员", "1951年6月朝鲜洪川江战斗牺牲", "", ""],
    ["陈茂香", "男", "1927.7", "海州区南门乡", "1948.11", "党团", "志愿军二十六军七十七师二二九团战士", "1951年7月朝鲜平津淮战斗牺牲", "", ""],
    ["周臣江", "男", "1928.1", "海州区南门乡", "1948.7", "1952年入党", "志愿军二十六军七十七师二二九团副排长", "1951年9月朝鲜平津淮战斗牺牲", "", ""],
    ["相开山", "男", "1926.8", "海州区双龙街", "1948.9", "", "志愿军二十六军特务团二营六连班长", "1952年9月朝鲜五圣山战斗牺牲", "", ""],
    ["顾立敏", "男", "1927.6", "海州区南门乡", "1947.9", "", "志愿军二十四军七十二师二一四团战士", "1952年10月在朝鲜战场牺牲", "", ""],
]

PATCH = {
    "title": "连云港市市区革命烈士简况表（续表）",
    "table_number": "",
    "page": 2835,
    "pages": [2835],
    "part": "part02",
    "vol": "下",
    "volume": "下",
    "columns": COLUMNS,
    "rows": ROWS,
    "row_count": len(ROWS),
    "col_count": len(COLUMNS),
    "status": "verified",
    "notes": "已据页级OCR核录：workbench/ocr/paddle_ocr/下/part02/page_0403.txt；表题依据本表首页 workbench/ocr/paddle_ocr/下/part02/page_0401.txt；并参考 raw 坐标 OCR：workbench/ocr/raw/下/part02/page_0403.json 与 raw 文本 workbench/table_entries/下/raw/LYG-下-T099_2835.txt。此条仅录入 page_0403 可见的连云港市市区革命烈士简况表续页记录。",
}


def patch_entry(entry: dict) -> bool:
    if entry.get("table_id") != "LYG-下-T099":
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
