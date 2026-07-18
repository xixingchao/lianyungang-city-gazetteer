# -*- coding: utf-8 -*-
"""Verify import equipment/product continuation page."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
DATA_DIR = ROOT / "workbench" / "table_entries" / "中" / "data"

PATCHES = {
    "LYG-中-T086": {
        "title": "1984~1990年连云港市进口设备和产品情况表（续表）",
        "table_number": "表35-5",
        "page": 1616,
        "pages": [1616],
        "part": "part02",
        "vol": "中",
        "volume": "中",
        "columns": ["单位", "项目(单机)名称", "金额(万美元)"],
        "rows": [
            ["市工艺美术公司系统", "项链配件", "1.42"],
            ["市工艺美术公司系统", "家具生产线", "39.68"],
            ["市工艺美术公司系统", "铝塑、塑塑复合线", "136.20"],
            ["市工艺美术公司系统", "画框条生产设备", "39.60"],
            ["市工艺美术公司系统", "全自动拆景机", "3.4"],
            ["市工艺美术公司系统", "缝纫单机", "0.84"],
            ["新海发电厂", "汽轮机保护仪表", "18.00"],
            ["市卫生局系统", "单机11", "44.88"],
            ["市卫生局系统", "B超声线扫仪", "2.54"],
            ["市卫生局系统", "血气分析仪", "2.60"],
            ["市卫生局系统", "纤维支气管镜", "0.46"],
            ["市卫生局系统", "医疗器械", "4.26"],
            ["市卫生局系统", "B超超声线扫仪", "2.54"],
            ["市卫生局系统", "纤维支气管镜", "0.46"],
            ["市卫生局系统", "医疗器械", "4.26"],
            ["市卫生局系统", "超声诊断仪", "0.62"],
            ["市卫生局系统", "医疗器械", "1.45"],
            ["市卫生局系统", "气相色谱仪", "1.10"],
            ["市卫生局系统", "X线机", "24.59"],
            ["市农业局系统", "蔬菜生产线", "134.30"],
            ["市计经委", "样机", "4.41"],
            ["市经协委", "汽车", "31.09"],
            ["市电子系统", "项目12 单机10", "1407.25"],
            ["市电子系统", "共用电视天线生产线", "766.00"],
            ["市电子系统", "彩电CKD", "193.80"],
            ["市电子系统", "彩色监视器", "89.21"],
            ["市电子系统", "小公差晶体关键生产设备", "4.88"],
            ["市电子系统", "通讯晶体生产设备", "22.90"],
        ],
        "status": "verified",
        "notes": "已据页级OCR回源核录：workbench/ocr/paddle_ocr/中/part02/page_0196.txt，并参考 raw OCR：workbench/table_entries/中/raw/LYG-中-T086_1616.txt。表题、表号和列组依据前页表35-5。本页为进口设备和产品情况表续表；仅录入本页可见项目，后续电子系统条目另页处理。",
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
