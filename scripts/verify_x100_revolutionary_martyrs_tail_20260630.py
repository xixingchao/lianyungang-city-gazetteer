# -*- coding: utf-8 -*-
"""Verify LYG-下-T100 revolutionary martyrs continuation page."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
DATA = ROOT / "workbench" / "table_entries" / "下" / "data" / "LYG-下-T100.json"

COLUMNS = [
    "姓名", "性别", "出生年月", "籍贯", "参加革命年月", "入党团年月",
    "牺牲时所在军队及其职务", "牺牲时间、地点、原因", "何时何单位授何奖励", "备注",
]

ROWS = [
    ["孙凤采", "男", "1927", "海州区新建街", "1947", "", "志愿军战士", "1953年抗美援朝战争牺牲在朝鲜", "", ""],
    ["杨翔斋", "男", "1928.3", "海州区双龙街", "1949.10", "党员", "九七零零部队第一中队战士", "1952年10月福建南日岛战斗失踪", "1961年追认", ""],
    ["周秉肖", "男", "1935", "海州区文化街", "1949.9", "", "志愿军十三军三十七师一一零团三营卫生员", "1953年6月朝鲜战场牺牲", "", ""],
    ["陈广士", "男", "1934", "海州区新坝陈户", "1948.5", "", "志愿军战士", "1953年朝鲜战场牺牲", "", ""],
    ["陈广前", "男", "1932", "海州区新坝陈户", "1948.9", "", "志愿军战士", "1953年朝鲜战场牺牲", "", ""],
    ["杨福如", "男", "1941.2", "海州区新坝武圩", "1959.12", "团员", "零二二四部队教导队驾驶员", "1961年郯城近山因公牺牲", "", ""],
    ["陈少发", "男", "1950.9", "海州区园艺场", "1970.1", "1970年1月入团", "五三一零部队六十二分队战士", "1971年9月宁夏石嘴山市石灰井因公牺牲", "", ""],
    ["黄文生", "男", "1941.5", "海州区新坝新东", "1959", "党员", "新疆农六师班长", "1973年11月农六师农机厂因公牺牲", "", ""],
    ["陈守党", "男", "1957", "海州区新坝陈户", "1977.1", "团员", "五三零五一部队一炮连战士", "1979年2月靖西县边境战斗牺牲", "", ""],
    ["马富强", "男", "1958.10", "海州区锦屏", "1977.1", "", "五三零四六部队战士", "1979年2月对越自卫还击战204高地战斗牺牲", "追记二等功", ""],
    ["卢德礼", "男", "1898", "云台区詹巷", "1927", "", "1927年参加农民革命", "1930年大村暴动牺牲", "", ""],
    ["杨文才", "男", "1899", "云台区云台乡武村", "1930", "", "", "1930年大村暴动牺牲", "", ""],
    ["赵开如", "男", "1909", "云台区云台乡赵巷", "1930", "", "", "1930年大村暴动牺牲", "", ""],
    ["赵绍银", "男", "1908", "云台区云台乡赵巷", "1930", "", "", "1930年大村暴动牺牲", "", ""],
    ["王维林", "男", "1910", "云台区云台乡大村", "1930", "", "", "1930年大村暴动牺牲", "", ""],
]

PATCH = {
    "title": "连云港市市区革命烈士简况表（续表）",
    "table_number": "",
    "page": 2836,
    "pages": [2836],
    "part": "part02",
    "vol": "下",
    "volume": "下",
    "columns": COLUMNS,
    "rows": ROWS,
    "row_count": len(ROWS),
    "col_count": len(COLUMNS),
    "status": "verified",
    "notes": "已据页级OCR核录：workbench/ocr/paddle_ocr/下/part02/page_0404.txt；表题依据本表首页 workbench/ocr/paddle_ocr/下/part02/page_0401.txt；并参考 raw 坐标 OCR：workbench/ocr/raw/下/part02/page_0404.json 与 raw 文本 workbench/table_entries/下/raw/LYG-下-T100_2836.txt。此条仅录入 page_0404 可见的连云港市市区革命烈士简况表续页记录。",
}


def patch_entry(entry: dict) -> bool:
    if entry.get("table_id") != "LYG-下-T100":
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
