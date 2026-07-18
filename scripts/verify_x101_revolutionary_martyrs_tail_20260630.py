# -*- coding: utf-8 -*-
"""Verify LYG-下-T101 revolutionary martyrs continuation page."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
DATA = ROOT / "workbench" / "table_entries" / "下" / "data" / "LYG-下-T101.json"

COLUMNS = [
    "姓名", "性别", "出生年月", "籍贯", "参加革命年月", "入党团年月",
    "牺牲时所在军队及其职务", "牺牲时间、地点、原因", "何时何单位授何奖励", "备注",
]

ROWS = [
    ["孙绪会", "男", "1912", "云台区云台乡梧桐沟", "1930", "", "", "1930年大村暴动牺牲", "", ""],
    ["徐登楼", "男", "1913", "云台区云台乡薄巷", "1930", "", "", "1930年大村暴动牺牲", "", ""],
    ["姜国元", "男", "1888", "云台区云台乡薄巷", "1927", "", "", "1930年大村暴动牺牲", "", ""],
    ["徐殿喜", "男", "1894", "云台区云台乡薄巷", "1929", "", "", "1930年大村暴动牺牲", "", ""],
    ["武同儒", "男", "1903.2", "云台区大村", "1928", "1928年入党", "中共沭阳县城区区委书记", "1931年在沭阳十字桥牺牲", "", "有传"],
    ["唐雨生", "男", "1906.4", "云台区朝阳乡新县村", "1928", "1928年入党", "盐城尚庄区大队副大队长", "1941年1月黄石乡战斗牺牲", "", "有传"],
    ["张昌干", "男", "1924", "云台区徐圩镇", "1940", "1940年入团", "三师司号员", "1945年在战争中牺牲", "", ""],
    ["刘汉生", "男", "1913", "云台区朝阳乡刘巷", "1941", "", "大队长", "1945年伏龙镇战斗牺牲", "", ""],
    ["钱光三", "男", "1926.10", "云台区猴嘴镇", "1944", "", "东海县曹埠民兵队长", "1946年曹埠战斗牺牲", "", ""],
    ["张步胜", "男", "1926", "云台区新滩乡", "1944", "", "中原野战军某部司号长", "1947年黄山战斗牺牲", "", ""],
    ["方国家", "男", "1918.4", "云台区云台乡大村", "1942", "", "教导二旅四团司务长", "1948年6月东海县七里沟村被捕牺牲", "", ""],
    ["刘振生", "男", "1928.9", "云台区云台乡西山村", "1946", "", "三十八军一一三师三三七团炮兵连班长", "1948年因战牺牲", "", ""],
    ["胡正兴", "男", "1929.3", "云台区中云乡东巷村", "1947.9", "", "灌云县区中队战士", "1948年在灌云县参战牺牲", "", ""],
    ["薛飞", "男", "1924.5", "云台区中云乡牛王庙", "1942.2", "党员", "某部班长", "1948年9月响水县战斗牺牲", "", ""],
    ["杨立安", "男", "1925.3", "云台区猴嘴镇", "1948", "", "淮海独立旅三团三营战士", "1948年12月涟水战斗牺牲", "", ""],
]

PATCH = {
    "title": "连云港市市区革命烈士简况表（续表）",
    "table_number": "",
    "page": 2837,
    "pages": [2837],
    "part": "part02",
    "vol": "下",
    "volume": "下",
    "columns": COLUMNS,
    "rows": ROWS,
    "row_count": len(ROWS),
    "col_count": len(COLUMNS),
    "status": "verified",
    "notes": "已据页级OCR核录：workbench/ocr/paddle_ocr/下/part02/page_0405.txt；表题依据本表首页 workbench/ocr/paddle_ocr/下/part02/page_0401.txt；并参考 raw 坐标 OCR：workbench/ocr/raw/下/part02/page_0405.json 与 raw 文本 workbench/table_entries/下/raw/LYG-下-T101_2837.txt。此条仅录入 page_0405 可见的连云港市市区革命烈士简况表续页记录。",
}


def patch_entry(entry: dict) -> bool:
    if entry.get("table_id") != "LYG-下-T101":
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
