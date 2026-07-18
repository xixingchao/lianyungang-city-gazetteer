# -*- coding: utf-8 -*-
"""Verify LYG-中-T027 chemical industry award products continuation table."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
DATA = ROOT / "workbench" / "table_entries" / "中" / "data" / "LYG-中-T027.json"

COLUMNS = ["年份", "产品名称", "获奖级别", "生产厂家"]
ROWS = [
    ["1984", "工业黄磷", "国家银质", "市锦屏化工厂"],
    ["1984", "甘露醇", "部优", "市制碘厂"],
    ["1984", "甘露醇", "省优", "市制碘厂"],
    ["1984", "氯化苄", "省优", "市化工厂"],
    ["1984", "二甲基甲酰胺", "省优", "市曙光化工厂"],
    ["1984", "磷酸二氢钾", "省优", "市海滨化工厂"],
    ["1984", "柠檬酸", "省优", "市发酵厂"],
    ["1984", "海藻酸钠", "省优", "赣榆县七二化工厂"],
    ["1985", "工业赤磷", "国家银质", "市锦屏磷矿"],
    ["1985", "牙膏级磷酸氢钙", "部优", "市红旗化工厂"],
    ["1985", "食品级磷酸氢钙", "省优", "市红旗化工厂"],
    ["1985", "甲酰胺", "省优", "市曙光化工厂"],
    ["1985", "海藻酸钠", "省优", "市制碘厂"],
    ["1985", "磷化铝(片剂)", "部优", "市化工厂"],
    ["1986", "工业级溴甲烷", "部优", "市海水化工一厂"],
    ["1986", "工业级溴甲烷", "省优", "市海水化工一厂"],
    ["1986", "工业无水焦磷酸钠", "省优", "市红旗化工厂"],
    ["1986", "氯化钾", "省优", "江苏省盐业公司黄海化工厂"],
    ["1987", "工业磷酸", "部优", "市锦屏化工厂"],
    ["1987", "甘露醇", "部优", "市制碘厂"],
    ["1987", "药用级磷酸氢钙", "省优", "市红旗化工厂"],
    ["1987", "田菁胶粉", "省优", "灌云县化工厂"],
    ["1987", "氯化镁", "省优", "江苏省盐业公司灌西化工厂"],
    ["1988", "柠檬酸", "省优", "市发酵厂"],
    ["1988", "柠檬酸", "部优", "市发酵厂"],
    ["1988", "工业甲酸", "省优", "市锦屏化工厂"],
    ["1988", "丙烯酸树脂", "省优", "市制碘厂"],
    ["1989", "工业黄磷(复评)", "国家银质", "市锦屏化工厂"],
    ["1989", "工业磷酸", "国家银质", "市锦屏化工厂"],
    ["1989", "氯化苄(复评)", "省优", "市化工厂"],
    ["1989", "磷酸二氢钾(复评)", "省优", "市海滨化工厂"],
    ["1989", "二甲基甲酰胺(复评)", "省优", "市曙光化工厂"],
    ["1989", "焦亚硫酸钠", "省优", "市化肥厂"],
    ["1989", "钙镁磷钾肥", "省优", "东海县磷肥厂"],
    ["1989", "碘(复评)", "省优", "赣榆县七二化工厂"],
]

PATCH = {
    "title": "1980~1990年连云港市化学工业获奖产品一览表（续表）",
    "table_number": "表20-16",
    "page": 1093,
    "pages": [1093],
    "columns": COLUMNS,
    "rows": ROWS,
    "row_count": len(ROWS),
    "col_count": len(COLUMNS),
    "status": "verified",
    "notes": "已据页级OCR回源核录：workbench/ocr/paddle_ocr/中/part01/page_0190.txt；主表题和表号见page_0189.txt。原JSON误串为胶粘剂产量表，本轮修正为表20-16续表；表注：省优、部优分别为省优质产品、部优质产品。",
}


def patch_entry(entry: dict) -> bool:
    if entry.get("table_id") != "LYG-中-T027":
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
