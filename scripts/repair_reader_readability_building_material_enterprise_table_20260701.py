# -*- coding: utf-8 -*-
"""Repair reader residue for table 23-4 and add verified table data."""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
DATA = ROOT / "workbench" / "table_entries" / "中" / "data" / "LYG-中-T132.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_building_material_enterprise_table_20260701.md"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_building_material_enterprise_table_20260701.json"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260701_第二十三卷建材工业主要企业表残文修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

COLUMNS = [
    "名称",
    "地址",
    "性质",
    "建厂年份",
    "职工人数(人)",
    "固定资产原值(万元)",
    "工业总产值(万元)",
    "主要产品",
]

ROWS = [
    ["东海县第一砖瓦厂", "东海县牛山乡西双湖", "全民", "1958", "202", "177", "83", "粘土砖、粘土平瓦"],
    ["东海县水泥厂", "东海县牛山镇幸福南路58号", "全民", "1958", "850", "1521", "1287", "水泥"],
    ["东海县蛭石厂", "东海县牛山镇茅墩西路54路", "集体", "1958", "118", "65", "09", "蛭石粉、珍珠岩粉"],
    ["东海县浦南乡第一砖瓦厂", "东海县浦南乡", "集体", "1958", "158", "92", "820", "粘土砖、粘土平瓦"],
    ["市墟沟石灰厂", "市连云区墟沟镇平山西首", "集体", "1963", "100", "77", "156", "石灰、消石灰粉"],
    ["赣榆县水泥制品厂", "赣榆县青口镇黄海路62号", "集体", "1966", "117", "58", "102", "环形预应力电杆、大型屋面板、槽板"],
    ["灌云县伊山镇采石厂", "灌云县伊山镇街尖路", "集体", "1966", "298", "6", "330", "石料、石子"],
    ["赣榆县石桥石粉厂", "赣榆县石桥镇", "集体", "1969", "125", "89", "167", "石英砂、钾长石粉、白云石"],
    ["赣榆县水泥厂", "赣榆县班庄乡泉坡村", "集体", "1970", "920", "792", "1511", "水泥"],
    ["灌云县水泥厂", "灌云县板浦镇南马路", "集体", "1970", "530", "652", "265", "水泥"],
    ["市石灰厂", "市海州火车站北首", "集体", "1970", "64", "86", "37", "石灰、石灰膏"],
    ["云台区第二建筑安装公司混凝土构件厂", "市云台区朝阳乡沙河口", "集体", "1973", "85", "85", "120", "115厚圆孔板、180厚中孔板、预制桩、圆型板、双“T”板、大型屋面板"],
    ["东海县石湖石粉厂", "东海县石湖乡", "集体", "1974", "165", "85", "175", "石英砂、高级玻璃砂"],
    ["东海县白塔埠镇砖瓦厂", "东海县白塔埠镇军屯村东首", "集体", "1976", "265", "61", "108", "粘土砖"],
    ["东海县水泥制品厂", "东海县牛山镇幸福南路", "集体", "1976", "147", "81", "132", "大、中、小圆孔板、平板、桁条"],
    ["东海县第二水泥厂", "东海县白塔埠镇火车站南首", "集体", "1976", "365", "556", "410", "水泥"],
    ["赣榆县厉庄乡石子厂", "赣榆县厉庄乡", "集体", "1978", "110", "11", "140", "石料、石子"],
    ["市海州制砖厂", "连云港市海州海孔南路", "集体", "1980", "290", "122", "197", "粘土砖"],
    ["市粉煤灰烧结砖厂", "连云港市海州区洪门乡铁路北", "集体", "1980", "325", "206", "200", "粉煤灰烧结砖"],
    ["赣榆县第二水泥厂", "赣榆县欢墩镇", "集体", "1980", "350", "450", "596", "水泥"],
    ["市朝阳西山砖厂", "连云港市云台区朝阳乡西庄村", "集体", "1981", "190", "66", "120", "空心砖、免烧砖、粘土砖"],
    ["市云台采石厂", "连云港市云台区云台乡大岛山", "集体", "1981", "350", "70", "145", "石料、石子"],
    ["东海县混凝土构件二厂", "东海县牛山镇城东路6号", "集体", "1983", "160", "120", "170", "大、中、小型空心板、排水管"],
    ["市锦屏采石厂", "连云港市海州锦屏山西侧", "集体", "1984", "270", "43", "117", "石料、石子"],
    ["市大理石厂", "连云港市新浦区新孔路1号", "集体", "1984", "227", "291", "349", "大理石、花岗石板材"],
]

ENTRY = {
    "table_id": "LYG-中-T132",
    "title": "1990年连云港市建材工业主要企业基本情况表",
    "table_number": "表23-4",
    "page": 1196,
    "pages": [1196, 1197],
    "part": "part01",
    "vol": "中",
    "columns": COLUMNS,
    "rows": ROWS,
    "row_count": len(ROWS),
    "col_count": len(COLUMNS),
    "status": "verified",
    "notes": "已据页级OCR核录：workbench/ocr/paddle_ocr/中/part01/page_0294.txt、page_0295.txt；并参考 raw OCR：workbench/ocr/raw/中/part01/page_0294.txt/json、page_0295.txt/json。表23-4首页与续上表跨两页，page_0295在注释“简介企业不列入本表”后进入表23-5。本表列序按源页复合表头整理为名称、地址、性质、建厂年份、职工人数、固定资产原值、工业总产值、主要产品。赣榆县厉庄乡石子厂固定资产原值栏 OCR 为 I1，按同列坐标核为 11；灌云县伊山镇采石厂固定资产原值栏为 6。",
    "volume": "中",
}

RESIDUE_RE = re.compile(
    r"\n?<p>主要产品地址性质年份\(人\)（万元）</p>\s*"
    r"<p>（万元）</p>\s*"
    r"<p>粘土砖、粘土东海县牛山乡西双全民195820283177东海县第一砖瓦厂.*?东海县第二水泥厂1976556水泥365410车站南首其它建筑材料</p>\s*",
    re.S,
)


def write_json() -> bool:
    old = DATA.read_text(encoding="utf-8") if DATA.exists() else ""
    new = json.dumps(ENTRY, ensure_ascii=False, indent=2) + "\n"
    if old != new:
        DATA.write_text(new, encoding="utf-8")
        return True
    return False


def patch_site() -> int:
    text = SITE.read_text(encoding="utf-8")
    match = re.search(r"const TABLES = (\[.*?\]);\s*\n\s*function escape", text, re.S)
    if not match:
        raise RuntimeError("TABLES payload not found")
    tables = json.loads(match.group(1))
    changed = False
    for idx, table in enumerate(tables):
        if table.get("table_id") == ENTRY["table_id"]:
            if table != ENTRY:
                tables[idx] = ENTRY
                changed = True
            break
    else:
        tables.append(ENTRY)
        changed = True
    if changed:
        tables.sort(key=lambda t: (str(t.get("vol") or t.get("volume") or ""), int((t.get("pages") or [t.get("page") or 999999])[0]), str(t.get("table_id") or "")))
        text = text[: match.start(1)] + json.dumps(tables, ensure_ascii=False) + text[match.end(1) :]
        SITE.write_text(text, encoding="utf-8")
        return 1
    return 0


def remove_reader_residue() -> int:
    text = HTML.read_text(encoding="utf-8")
    new, count = RESIDUE_RE.subn("\n", text, count=1)
    if count:
        HTML.write_text(new, encoding="utf-8")
    return count


def write_reports(json_changed: bool, site_changed: int, removed: int) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    result = {
        "time": now,
        "table_id": ENTRY["table_id"],
        "table_number": ENTRY["table_number"],
        "title": ENTRY["title"],
        "source_pages": ENTRY["pages"],
        "source_ocr": [
            "workbench/ocr/paddle_ocr/中/part01/page_0294.txt",
            "workbench/ocr/paddle_ocr/中/part01/page_0295.txt",
            "workbench/ocr/raw/中/part01/page_0294.txt",
            "workbench/ocr/raw/中/part01/page_0295.txt",
        ],
        "json_changed": json_changed,
        "site_changed": site_changed,
        "reader_residue_blocks_removed": removed,
        "rows": len(ROWS),
        "columns": len(COLUMNS),
    }
    REPORT_JSON.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    md = f"""# 第二十三卷建材工业主要企业表残文修复

- 时间：{now}
- 表ID：`{ENTRY['table_id']}`
- 表题：{ENTRY['table_number']} {ENTRY['title']}
- 源页：`workbench/ocr/paddle_ocr/中/part01/page_0294.txt`、`workbench/ocr/paddle_ocr/中/part01/page_0295.txt`

## 修复动作

- 新增/更新结构化表 JSON：`workbench/table_entries/中/data/LYG-中-T132.json`。
- 将跨页表23-4核录为 {len(ROWS)} 行、{len(COLUMNS)} 列，并同步到结构化表格站。
- 从最终阅读版撤出被压成正文的表头单位残片和首页企业串行段落：{removed} 组。

## 核对说明

- `page_0294` 为表23-4首页，`page_0295` 为“续上表”，到注释“简介企业不列入本表”结束。
- 列序按源页复合表头整理为：名称、地址、性质、建厂年份、职工人数、固定资产原值、工业总产值、主要产品。
- `赣榆县厉庄乡石子厂` 固定资产原值栏 OCR 为 `I1`，按同列坐标核为 `11`。
- `灌云县伊山镇采石厂` 固定资产原值栏为 `6`，未按常识外推修改。
"""
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")


def update_memory(removed: int) -> None:
    marker = "## 2026-07-01 第二十三卷建材工业主要企业表残文修复"
    memory = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker in memory:
        return
    entry = f"""
{marker}

- 针对正文可读性审计命中的第二十三卷建材工业表格线性化残文，回源 `workbench/ocr/paddle_ocr/中/part01/page_0294.txt`、`page_0295.txt` 及 raw OCR 坐标核对。
- 新增 verified 结构化表：`workbench/table_entries/中/data/LYG-中-T132.json`，表23-4《1990年连云港市建材工业主要企业基本情况表》，25 行 8 列。
- 从 `output/final_reader/连云港市志_全书.html` 撤出首页表头单位残片和企业串行正文残文 {removed} 组；续页未在主阅读版检出同类残文。
- 报告：`output/reports/reader_readability_building_material_enterprise_table_20260701.md`。
"""
    MEMORY.write_text(memory.rstrip() + "\n\n" + entry.lstrip(), encoding="utf-8")


def main() -> None:
    json_changed = write_json()
    site_changed = patch_site()
    removed = remove_reader_residue()
    write_reports(json_changed, site_changed, removed)
    update_memory(removed)
    print(f"json_changed={int(json_changed)}")
    print(f"site_changed={site_changed}")
    print(f"reader_residue_blocks_removed={removed}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()
