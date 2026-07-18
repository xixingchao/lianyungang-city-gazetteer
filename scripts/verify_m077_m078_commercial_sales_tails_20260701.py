# -*- coding: utf-8 -*-
"""Verify LYG-中-T077/T078 commercial sales continuation tables."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"

PATCHES = {
    "LYG-中-T077": {
        "path": ROOT / "workbench" / "table_entries" / "中" / "data" / "LYG-中-T077.json",
        "patch": {
            "title": "1970~1990年部分年份连云港市五交化公司主要商品销量统计表续表",
            "table_number": "表33-8",
            "page": 1561,
            "pages": [1561],
            "part": "part02",
            "vol": "中",
            "volume": "中",
            "columns": [
                "年份",
                "元钉(吨)",
                "铁丝(吨)",
                "自行车(辆)",
                "花线(百米)",
                "日光灯管(万支)",
                "电视机(台)",
                "洗衣机(台)",
                "电冰箱(台)",
                "台扇(台)",
                "油漆(吨)",
            ],
            "rows": [
                ["1988", "205", "476", "13501", "5298", "8.80", "4358", "1931", "1314", "11031", "596"],
                ["1989", "233", "685", "12084", "2795", "", "4675", "441", "675", "5935", "582"],
                ["1990", "", "", "40904", "", "", "22110", "15218", "11971", "", ""],
            ],
            "status": "verified",
            "notes": "已据页级OCR核录续页：workbench/ocr/paddle_ocr/中/part02/page_0141.txt；表题、表号和复合表头承接前页 workbench/ocr/paddle_ocr/中/part02/page_0140.txt。并参考 raw 坐标OCR workbench/ocr/raw/中/part02/page_0141.json 与 raw 文本 workbench/table_entries/中/raw/LYG-中-T077_1561.txt。仅录入 page_0141 可见的1988-1990年续表记录；源页未见数值处保留空值。",
        },
    },
    "LYG-中-T078": {
        "path": ROOT / "workbench" / "table_entries" / "中" / "data" / "LYG-中-T078.json",
        "patch": {
            "title": "1980~1990年部分年份连云港市烟酒公司销售渠道表续表",
            "table_number": "表33-11",
            "page": 1567,
            "pages": [1567],
            "part": "part02",
            "vol": "中",
            "volume": "中",
            "columns": [
                "年份",
                "总销售(万元)",
                "国内纯销售(万元)",
                "调给省内供销(万元)",
                "调给省外(万元)",
                "调给省内市外(万元)",
                "调给市(县)内(万元)",
            ],
            "rows": [
                ["1985", "4743", "1131", "543", "940", "1732", "340"],
                ["1986", "6316", "1931", "736", "1337", "1245", "1015"],
                ["1987", "4071", "1306", "1145", "424", "239", "455"],
                ["1988", "4273", "2425", "1036", "203", "92", "515"],
                ["1989", "3946", "2232", "752", "267", "185", "509"],
                ["1990", "4739", "2635", "660", "260", "379", "753"],
            ],
            "status": "verified",
            "notes": "已据页级OCR核录续页：workbench/ocr/paddle_ocr/中/part02/page_0147.txt；表题、表号、单位和复合表头承接前页 workbench/ocr/paddle_ocr/中/part02/page_0146.txt。并参考 raw 坐标OCR workbench/ocr/raw/中/part02/page_0147.json 与 raw 文本 workbench/table_entries/中/raw/LYG-中-T078_1567.txt。仅录入 page_0147 可见的1985-1990年续表记录。",
        },
    },
}


def normalized_patch(table_id: str) -> dict:
    patch = dict(PATCHES[table_id]["patch"])
    rows = patch["rows"]
    columns = patch["columns"]
    patch["row_count"] = len(rows)
    patch["col_count"] = len(columns)
    return patch


def patch_entry(entry: dict) -> bool:
    table_id = entry.get("table_id")
    if table_id not in PATCHES:
        return False
    patch = normalized_patch(table_id)
    changed = False
    for key, value in patch.items():
        if entry.get(key) != value:
            entry[key] = value
            changed = True
    return changed


def patch_json_files() -> int:
    changed = 0
    for table_id, spec in PATCHES.items():
        data_path = spec["path"]
        data = json.loads(data_path.read_text(encoding="utf-8"))
        if patch_entry(data):
            data_path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
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
