# -*- coding: utf-8 -*-
"""Verify construction-industry continuation tables."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
DATA_DIR = ROOT / "workbench" / "table_entries" / "中" / "data"

QUALITY_COLUMNS = ["工程名称", "建筑面积(平方米)", "结构", "层次", "施工单位", "年份"]
UNIT_COLUMNS = [
    "单位名称",
    "成立年月",
    "单位性质",
    "资质等级",
    "隶属关系",
    "职工人数总数(人)",
    "职工人数技术人员(人)",
    "固定资产原值(万元)",
    "技术装备率(元/人)",
    "年生产能力",
]

PATCHES = {
    "LYG-中-T033": {
        "title": "1981~1990年连云港市获省级优质工程一览表（续表）",
        "table_number": "表24-4",
        "page": 1220,
        "pages": [1220],
        "part": "part01",
        "vol": "中",
        "volume": "中",
        "columns": QUALITY_COLUMNS,
        "rows": [
            ["市海监局A型住宅楼", "2525", "混合", "5", "连云区院前建筑公司", "1990"],
            ["市海监局B型住宅楼", "1663", "混合", "5", "连云区院前建筑公司", "1990"],
            ["海州邮电楼", "1878", "框架", "3", "市第一建筑工程公司", "1990"],
            ["市房屋修缮公司二号楼", "1800", "混合", "7", "云台区二建公司", "1990"],
            ["市车辆厂住宅楼", "3300", "混合", "6", "海州区建安装璜公司", "1990"],
            ["市计生委办公楼", "2093", "混合", "4", "赣榆县一建二处(欢墩)", "1990"],
            ["赣榆县中国人民银行营业楼", "1700", "框架", "4", "赣榆县一建四处(金山)", "1990"],
            ["市人大微机楼", "1700", "混合", "4", "赣榆县一建五处(沙河)", "1990"],
            ["市海监局办公楼", "4062", "框架", "5", "赣榆县一建三处(大岭)", "1990"],
            ["赣榆县福利院综合楼", "1267", "混合", "4", "赣榆县青口镇建筑公司", "1990"],
            ["东海县酿造综合楼", "1017", "混合", "3", "东海县二建二处", "1990"],
        ],
        "status": "verified",
        "notes": "已据页级OCR回源核录：workbench/ocr/paddle_ocr/中/part01/page_0317.txt，并参考 raw OCR：workbench/table_entries/中/raw/LYG-中-T033_1220.txt。表题、表号和列组据前页 workbench/ocr/paddle_ocr/中/part01/page_0316.txt 补定。原JSON误列为主要勘察设计单位一览表；本页为表24-4续上表。",
    },
    "LYG-中-T034": {
        "title": "1990年连云港市建筑业主要单位基本情况表（续表）",
        "table_number": "表24-5",
        "page": 1232,
        "pages": [1232],
        "part": "part01",
        "vol": "中",
        "volume": "中",
        "columns": UNIT_COLUMNS,
        "rows": [
            ["交通部第三航务工程局第五工程公司", "1976.12", "全民", "一级", "部属", "2410", "247", "7670.50", "21423", "6000"],
            ["连云港市建筑设计院", "1978.12", "全民", "乙级", "市属", "147", "107", "240.00", "", "40万平方米工程设计；3万米工程勘探进尺"],
            ["连云港市建筑工程公司", "1959.10", "全民", "一级", "市属", "5500", "450", "2200.00", "1489", "11000"],
            ["其中：连云港市第一建筑工程公司", "1949", "全民", "二级", "市属", "2250", "152", "795.40", "1524", "4500"],
            ["连云港市第二建筑工程公司", "1976", "全民", "二级", "市属", "1014", "103", "809.00", "1587", "3000"],
            ["连云港市第三建筑工程公司", "1983.7", "集体", "二级", "市属", "918", "79", "629.00", "1371", "2500"],
            ["连云港市建设开发公司", "1984", "全民", "一级", "市属", "393", "214", "3765.00", "", "25000"],
            ["江苏省盐业建筑公司", "1981", "全民", "二级", "省属", "1643", "144", "817.80", "1537", "2500"],
            ["连云港市工业设备安装公司", "1958.7", "全民", "二级", "市属", "415", "42", "333.46", "1700", "1200"],
            ["锦屏磷矿机电设备安装公司", "1967.10", "全民", "二级", "矿属", "535", "55", "712.80", "8657", "1000"],
            ["连云港市机械化施工公司", "1973.3", "全民", "二级", "市属", "345", "30", "378.60", "5223", "700"],
            ["赣榆县第一建筑安装工程公司", "1978", "集体", "二级", "县属", "3696", "268", "1079.00", "4514", "9000"],
            ["赣榆县建筑安装工程公司", "1950", "集体", "二级", "县属", "1914", "236", "557.60", "450", "4000"],
            ["东海县第二建筑安装工程公司", "1977", "集体", "二级", "县属", "3305", "239", "811.50", "1300", "6000"],
            ["中国化学工程总公司连云港分公司", "1984.9", "全民", "一级", "部属", "189", "138", "460.00", "9115", "15000"],
            ["连云港市建筑工程承包公司", "1989.2", "全民", "一级", "市属", "82", "77", "26.60", "5097", "12200"],
        ],
        "status": "verified",
        "notes": "已据页级OCR回源核录：workbench/ocr/paddle_ocr/中/part01/page_0329.txt，并参考 raw OCR：workbench/table_entries/中/raw/LYG-中-T034_1232.txt。表题、表号和列组据前页 workbench/ocr/paddle_ocr/中/part01/page_0328.txt 补定。原JSON误列为主要勘察设计单位一览表；本页为表24-5续上表。跨行单位名称和年生产能力已归并；源页未见数值的单元格保留空值。",
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
