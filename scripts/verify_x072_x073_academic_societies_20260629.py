# -*- coding: utf-8 -*-
"""Verify LYG-下-T072/T073 academic societies table from raw OCR."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
DATA_FILES = {
    "LYG-下-T072": ROOT / "workbench" / "table_entries" / "下" / "data" / "LYG-下-T072.json",
    "LYG-下-T073": ROOT / "workbench" / "table_entries" / "下" / "data" / "LYG-下-T073.json",
}

COLUMNS = ["名称", "成立年月", "挂靠单位", "会员数(人)"]
PATCHES = {
    "LYG-下-T072": {
        "title": "1990年连云港市市级学会、协会、研究会一览表",
        "table_number": "表51-5",
        "page": 2396,
        "pages": [2396],
        "columns": COLUMNS,
        "rows": [
            ["畜牧兽医学会", "1958.4", "市多管局", "158"],
            ["农学会", "1959.10", "市农业局", "372"],
            ["机械工程学会", "1964", "市机械工业公司", "387"],
            ["土木建筑学会", "1966.4", "市建委", "575"],
            ["医学会", "1958.9", "市卫生局", "843"],
            ["电机工程学会", "1977.3", "市供电局", "305"],
            ["数学会", "1978", "市教育学院", "230"],
            ["纺织工程学会", "1979.9", "市纺织工业公司", "223"],
            ["林学会", "1979.9", "市多管局", "133"],
            ["水产学会", "1979.10", "连云港水产学校", "134"],
            ["电子学会", "1979.11", "市电子工业公司", "370"],
            ["护理学会", "1980.1", "市卫生局", "560"],
            ["轻工学会", "1980.4", "市轻工公司", "198"],
            ["中医学会", "1980.5", "市卫生局", "427"],
            ["制冷学会", "1980.7", "市建筑设计院", "58"],
            ["珠算学会", "1980.7", "市财政局", "174"],
            ["图书馆学会", "1980.9", "市图书馆", "242"],
            ["科技情报学会", "1980.9", "市科技情报所", "293"],
            ["地震学会", "1980.11", "市地震办", "85"],
            ["化学化工学会", "1980.11", "市化学化工公司", "355"],
            ["标准化协会", "1980.12", "市标准计量局", "314"],
            ["质量管理协会", "1980", "市计经委", "306"],
            ["烹饪协会", "1981.3", "市饮食中心", "405"],
            ["工艺美术学会", "1981.3", "市工美工业公司", "09"],
            ["太阳能利用研究会", "1981", "市建科所", "77"],
        ],
        "status": "verified",
        "notes": "已据raw OCR回源核录：workbench/table_entries/下/raw/LYG-下-T072_2396.txt；原JSON为单列待录入骨架。本页为表51-5首页，续表见LYG-下-T073；工艺美术学会会员数OCR为“09”，保留原读数，未猜补百位。",
    },
    "LYG-下-T073": {
        "title": "1990年连云港市市级学会、协会、研究会一览表（续表）",
        "table_number": "表51-5",
        "page": 2397,
        "pages": [2397],
        "columns": COLUMNS,
        "rows": [
            ["物理学会", "1981", "市教育局", "128"],
            ["气象学会", "1981.11", "市气象局", "133"],
            ["包装技术协会", "1982.2", "市计经委", "300"],
            ["青少年科技辅导员协会", "1982.3", "市科协", "210"],
            ["科普创作协会", "1982.4", "《科技汇报》社", "84"],
            ["中西医结合研究会", "1982.4", "市卫生局", "114"],
            ["金融学会", "1982.5", "人民银行连云港分行", "446"],
            ["人才学会", "1982.6", "市科委", "156"],
            ["药学会", "1982.11", "市卫生局", "227"],
            ["统计学会", "1983.11", "市统计局", "420"],
            ["计量测试学会", "1984.2", "市标准计量局", "109"],
            ["水利学会", "1984.4", "市水利局", "153"],
            ["商业经济学会", "1984.6", "市商业局", "406"],
            ["环境科学学会", "1984.8", "市环保局", "128"],
            ["农业机械学会", "1984.9", "市农业局", "154"],
            ["计划生育协会", "1984.11", "市计生委", "49"],
            ["档案学会", "1984.12", "市档案局", "310"],
            ["财政学会", "1985.2", "市财政局", "55"],
            ["会计学会", "1985.2", "市财政局", "177"],
            ["微电脑应用学会", "1985.5", "市电子计算机办公室", "369"],
            ["港口协会", "1985.8", "连云港港务局", "350"],
            ["农业区划学会", "1985.9", "市农业区划办公室", "152"],
            ["海洋湖沼学会", "1986.11", "连云港水产学校", "151"],
            ["针灸蜂针研究会", "1987.5", "市蜂疗研究所", "48"],
            ["公路学会", "1987.6", "市交通局", "123"],
            ["气功科学研究会", "1986.3", "市政协", "546"],
            ["翻译工作者协会", "1989.2", "市科协", "100"],
            ["预防医学会", "1989.2", "市卫生局", "286"],
            ["测绘学会", "1989.5", "市规划局", "154"],
            ["审计学会", "1989.6", "市审计局", "86"],
            ["科技致富能手协会", "1989.3", "市科协", "181"],
            ["“科技兴市”研究会", "1989.8", "市科委", "58"],
            ["离退休科技工作者协会", "1989.12", "市委老干局", "115"],
            ["计算机学会", "1990.4", "市电子计算机办公室", "157"],
        ],
        "status": "verified",
        "notes": "已据raw OCR回源核录：workbench/table_entries/下/raw/LYG-下-T073_2397.txt；原JSON为单列待录入骨架。本页为表51-5续表，首页见LYG-下-T072；“针灸蜂针研究会”按语境规范OCR“针炙”为“针灸”。",
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
    for path in DATA_FILES.values():
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
