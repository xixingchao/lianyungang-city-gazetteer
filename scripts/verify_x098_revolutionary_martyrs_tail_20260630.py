# -*- coding: utf-8 -*-
"""Verify LYG-下-T098 revolutionary martyrs continuation page."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
DATA = ROOT / "workbench" / "table_entries" / "下" / "data" / "LYG-下-T098.json"

COLUMNS = [
    "姓名", "性别", "出生年月", "籍贯", "参加革命年月", "入党团年月",
    "牺牲时所在军队及其职务", "牺牲时间、地点、原因", "何时何单位授何奖励", "备注",
]

ROWS = [
    ["刘吉文", "男", "1931", "新浦区临洪乡", "", "", "志愿军二十六军特务团侦察员", "1952年朝鲜平津淮战斗牺牲", "", ""],
    ["卜秉寿", "男", "", "新浦区市民街", "1945.8", "1950年5月入团", "志愿军一六二部队二支队炮兵团排长", "1952年4月朝鲜战场牺牲", "", ""],
    ["赵昌台", "男", "1923", "新浦区", "1949.10", "", "志愿军十五军四十四师团警卫连副班长", "1953年7月朝鲜战场牺牲", "", ""],
    ["黄榘门", "男", "1915", "海州区鼓楼街", "1938", "党员", "新四军苏浙军区三纵队科长", "1945年战斗牺牲", "", ""],
    ["蔡加福", "男", "1920.2", "海州区新建街", "1943.12", "", "东北野战军一纵二师战士", "1946年4月兴隆岭战斗牺牲", "", ""],
    ["王长根", "男", "1922", "海州区", "1945.6", "", "华中野战军六纵四十八团三营战士", "1946年9月涟水战斗牺牲", "", ""],
    ["李学腻", "男", "", "海州区", "1945", "", "华中野战军六纵五十二团一营炊事员", "1946年9月涟水战斗中牺牲", "", ""],
    ["石青堂", "男", "1918", "海州区", "1944.7", "1945年入党", "华中野战军六纵四十八团二营排长", "1946年9月涟水战斗中牺牲", "", ""],
    ["宋子授", "男", "1912", "海州区", "1944", "1945年入党", "华中野战军六纵四十六团炮兵副连长", "1946年9月涟水战斗中牺牲", "", ""],
    ["赵叔叶", "男", "1903", "海州区", "1946.8", "", "华东野战军六纵四十八团三营战士", "1946年9月涟水战斗中牺牲", "", ""],
    ["江希余", "男", "1914.4", "海州区", "", "党员", "华东野战军四纵二旅连长", "1946年解放战争牺牲", "", ""],
    ["唐学山", "男", "1921", "海州区西门乡", "1941.1", "", "东北野战军一纵二师连长", "1947年6月四平战斗牺牲", "", ""],
    ["舒明炎", "男", "1921.3", "海州区南中街", "1942", "", "东海城工部地下情报员", "1948年1月在新浦被捕牺牲", "", ""],
    ["舒炳杰", "男", "1896.8", "海州区南中街", "1939", "1940年入党", "东海城工部地下情报员", "1948年1月在新浦被捕牺牲", "", ""],
    ["李文广", "男", "1931", "海州区文化街", "1948", "", "十九军五十五师一六三团通讯员", "1950年11月陕西镇巴县因公牺牲", "", ""],
    ["刘立德", "男", "1926", "海州区车站大队", "1948", "", "志愿军二十军五十八师一七二团三营战士", "1950年朝鲜战场失踪", "1961年追认", ""],
]

PATCH = {
    "title": "连云港市市区革命烈士简况表（续表）",
    "table_number": "",
    "page": 2834,
    "pages": [2834],
    "part": "part02",
    "vol": "下",
    "volume": "下",
    "columns": COLUMNS,
    "rows": ROWS,
    "row_count": len(ROWS),
    "col_count": len(COLUMNS),
    "status": "verified",
    "notes": "已据页级OCR核录：workbench/ocr/paddle_ocr/下/part02/page_0402.txt；表题依据本表首页 workbench/ocr/paddle_ocr/下/part02/page_0401.txt；并参考 raw 坐标 OCR：workbench/ocr/raw/下/part02/page_0402.json 与 raw 文本 workbench/table_entries/下/raw/LYG-下-T098_2834.txt。此条仅录入 page_0402 可见的连云港市市区革命烈士简况表续页记录。",
}


def patch_entry(entry: dict) -> bool:
    if entry.get("table_id") != "LYG-下-T098":
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
