# -*- coding: utf-8 -*-
"""Verify two port-service single-page tables from page OCR."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
DATA_DIR = ROOT / "workbench" / "table_entries" / "中" / "data"

PATCHES = {
    "LYG-中-T053": {
        "title": "1985~1990年外轮服务公司供水、回收垃圾情况表",
        "table_number": "表29-25",
        "page": 1390,
        "pages": [1390],
        "columns": ["年份", "船舶供水(吨)", "生产用水(吨)", "船次", "袋数", "约合吨数", "备注"],
        "rows": [
            ["1985", "475293", "529460", "2413", "59185", "889", "本表数字均为国际航线船舶，每袋以15公斤计算"],
            ["1986", "414119", "468626", "2458", "58840", "883", "本表数字均为国际航线船舶，每袋以15公斤计算"],
            ["1987", "459496", "530724", "2353", "43217", "648", "本表数字均为国际航线船舶，每袋以15公斤计算"],
            ["1988", "497806", "583415", "3043", "30977", "465", "本表数字均为国际航线船舶，每袋以15公斤计算"],
            ["1989", "646207", "474808", "3030", "18410", "267", "本表数字均为国际航线船舶，每袋以15公斤计算"],
            ["1990", "611170", "696516", "2807", "25115", "377", "本表数字均为国际航线船舶，每袋以15公斤计算"],
        ],
        "notes": "已据页级OCR回源核录：workbench/ocr/paddle_ocr/中/part01/page_0487.txt。",
    },
    "LYG-中-T054": {
        "title": "1974~1989年中国旗船舶检验统计表",
        "table_number": "表29-28",
        "page": 1419,
        "pages": [1419],
        "columns": ["年份", "检验艘次"],
        "rows": [
            ["1974", "3"],
            ["1975", "6"],
            ["1976", "5"],
            ["1977", "16"],
            ["1978", "22"],
            ["1979", "32"],
            ["1980", "64"],
            ["1981", "60"],
            ["1982", "99"],
            ["1983", "96"],
            ["1984", "127"],
            ["1985", "121"],
            ["1986", "116"],
            ["1987", "146"],
            ["1988", "158"],
            ["1989", "165"],
        ],
        "notes": "已据页级OCR回源核录：workbench/ocr/paddle_ocr/中/part01/page_0516.txt。",
    },
}


def patch_entry(entry: dict) -> bool:
    patch = PATCHES.get(entry.get("table_id"))
    if not patch:
        return False
    updates = dict(patch)
    updates["row_count"] = len(patch["rows"])
    updates["col_count"] = len(patch["columns"])
    updates["status"] = "verified"
    changed = False
    for key, value in updates.items():
        if entry.get(key) != value:
            entry[key] = value
            changed = True
    return changed


def patch_json_files() -> int:
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
    print(f"json_files_changed={patch_json_files()}")
    print(f"site_entries_changed={patch_site()}")


if __name__ == "__main__":
    main()
