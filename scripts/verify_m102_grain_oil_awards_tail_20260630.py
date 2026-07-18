# -*- coding: utf-8 -*-
"""Verify grain and oil industry awards continuation table."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
DATA_DIR = ROOT / "workbench" / "table_entries" / "中" / "data"

PATCHES = {
    "LYG-中-T102": {
        "title": "1986~1990年连云港市粮油工业产品获奖情况一览表（续表）",
        "table_number": "表36-22",
        "page": 1677,
        "pages": [1677],
        "part": "part02",
        "vol": "中",
        "volume": "中",
        "columns": ["获奖产品名称", "生产企业", "获奖年份", "获奖等级"],
        "rows": [
            ["“海陵”牌标准粉", "东海县双店油米厂", "1987", "市优"],
            ["“海陵”牌标准粉挂面", "东海县双店油米厂", "1987", "市优"],
            ["“双黄”牌蛋鸡料", "东海县饲料厂", "1987", "市优"],
            ["“福民”牌精炼棉籽油", "灌云县植物油厂", "1987", "市优"],
            ["“羽山”牌标一粳米", "东海县面粉厂", "1988", "部优"],
            ["“春燕”牌特副粉挂面", "灌云县制面厂", "1988", "部优"],
            ["“福民”牌精炼棉籽油", "灌云县植物油厂", "1988", "部优"],
            ["“海陵”牌特副粉", "东海县双店油米厂", "1988", "省优"],
            ["“玉珠”牌珠元精洁米", "东海县平明米厂", "1988", "省优"],
            ["“双黄”牌蛋鸡料", "东海县饲料厂", "1988", "省优"],
            ["“连海”牌标一粳米", "连云港市碾米厂", "1988", "市优"],
            ["“金龙”牌一级花生油", "连云港市新海植物油厂", "1988", "市优"],
            ["“金龙”牌一级大豆油", "连云港市新海植物油厂", "1988", "市优"],
            ["“云溪”牌特副粉", "赣榆县粮食加工厂", "1988", "市优"],
            ["“榆花”牌二级花生油", "赣榆县植物油厂", "1988", "市优"],
            ["“海陵”牌标一籼米", "东海县双店油米厂", "1988", "市优"],
            ["“银鸽”牌二级大豆油", "东海县植物油厂", "1988", "市优"],
            ["“银鸽”牌一级花生油", "东海县植物油厂", "1988", "市优"],
            ["“双黄”牌系列蛋鸡料", "东海县饲料厂", "1988", "市优"],
            ["“黄川”牌标一元米", "东海县黄川米厂", "1988", "市优"],
            ["“羽山”牌标一籼米", "东海县面粉厂", "1988", "市优"],
            ["“羽山”牌标准粉", "东海县面粉厂", "1988", "市优"],
            ["“东喜”牌标一籼米", "东海县白塔面粉厂", "1988", "市优"],
            ["“东喜”牌特二粳米", "东海县白塔面粉厂", "1988", "市优"],
            ["“榆花”牌二级花生油", "赣榆县植物油厂", "1989", "部优"],
            ["“平珠”牌特二晚粳", "东海县平明米厂", "1989", "部优"],
            ["“海陵”牌特二晚粳", "东海县白塔面粉厂", "1989", "部优"],
            ["“春燕”牌特粉挂面", "灌云县制面厂", "1989", "部优"],
            ["“福民”牌二级大豆油", "灌云县植物油厂", "1989", "部优"],
            ["“银鸽”牌二级花生油", "东海县植物油厂", "1989", "省优"],
            ["“榆花”牌二级花生油", "赣榆县植物油厂", "1989", "省优"],
            ["“云雀”牌标一元米", "赣榆县粮食加工厂", "1990", "部优"],
            ["“海陵”牌标一粳米", "东海县双店油米厂", "1990", "部优"],
            ["“云丰”牌特制一等粉", "灌云县杨集面粉厂", "1990", "部优"],
            ["“连海”牌标一粳米", "连云港市碾米厂", "1990", "省优"],
            ["“东蓬”牌蛋鸡饲料", "赣榆县配合饲料厂", "1990", "省优"],
            ["“港城”牌特副粉挂面", "连云港市康乐粮油食品厂", "1990", "市优"],
        ],
        "status": "verified",
        "notes": "已据页级OCR回源核录：workbench/ocr/paddle_ocr/中/part02/page_0257.txt，并参考 raw OCR：workbench/table_entries/中/raw/LYG-中-T102_1677.txt。表题、表号和列组依据前页 page_0256.txt。原JSON误沿用农村集体储备粮表题且为单列骨架；本页实际为表36-22续表。产品名中粳米、籼米按同表前页与语境规范。",
    }
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
