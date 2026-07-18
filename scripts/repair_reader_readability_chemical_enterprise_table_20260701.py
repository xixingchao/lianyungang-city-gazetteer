# -*- coding: utf-8 -*-
"""Repair the reader residue for table 20-15 and add its verified table data."""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
DATA = ROOT / "workbench" / "table_entries" / "中" / "data" / "LYG-中-T130.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_chemical_enterprise_table_20260701.md"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_chemical_enterprise_table_20260701.json"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260701_第二十卷化工企业基本情况表残文修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

COLUMNS = [
    "单位名称",
    "性质",
    "建厂年份",
    "职工(人)",
    "固定资产原值(万元)",
    "主要产品",
    "产值(万元)",
    "利税(万元)",
]

ROWS = [
    ["市锦屏化工厂", "全民", "1958", "1804", "2068", "黄磷、赤磷、磷酸、甲酸、钙镁磷肥", "3876", "844"],
    ["市海水化工一厂", "全民", "1958", "286", "398", "溴甲烷、溴乙烷、八溴醚", "327", "40"],
    ["江苏省盐务局黄海化工厂", "全民", "1958", "600", "800", "氯化钾、氯化镁、氯化钠、溴素", "524", "130"],
    ["市曙光化工厂", "市集", "1958", "357", "366", "二甲基甲酰胺、甲酰胺", "1143", "200"],
    ["市第一橡胶厂", "市集", "1958", "161", "200", "轮胎翻新、橡胶杂件、塑料包装桶", "140", "72"],
    ["赣榆县盐化厂", "全民", "1958", "359", "305", "烧碱、盐酸、漂液", "436", "292"],
    ["市化工厂", "全民", "1965", "1406", "1324", "烧碱、盐酸、磷化铝、氯化苄、苯甲醛", "2710", "528"],
    ["灌云县磷肥厂", "全民", "1965", "434", "290", "普通过磷酸钙、硫酸", "400", "47"],
    ["市盐化厂", "市集", "1966", "158", "100", "氧化镁、氢氧化镁、工业级磷酸二氢钾", "126", "23"],
    ["市红光化工厂", "市集", "1958", "120", "130", "聚醋酸乙烯乳胶、人造毛皮防风胶", "158", "15"],
    ["灌云县化工厂", "全民", "1969", "280", "107", "SG植物胶", "206", ""],
    ["市有机化工厂", "市集", "1970", "431", "332", "聚醋酸乙烯乳胶、乙烯、醋酸乙烯粉末", "639", "44"],
    ["赣榆县磷肥厂", "全民", "1971", "563", "392", "钙镁磷肥、普通过磷酸钙、硫酸", "446", "53"],
    ["东海县化工厂", "县集", "1972", "176", "208", "甲胺磷", "241", "40"],
    ["东海县金刚砂厂", "县集", "1977", "130", "106", "碳化硅", "304", "42"],
    ["飞天润滑油调合厂", "全民", "1986", "61", "250", "汽油机油、柴油机油、压缩机油", "379", "99"],
    ["市热熔粘合剂厂", "市集", "1988", "87", "406", "EVA系列热熔胶、热熔胶带", "386", "103"],
]

ENTRY = {
    "table_id": "LYG-中-T130",
    "title": "1990年连云港市化工企业基本情况表",
    "table_number": "表20-15",
    "page": 1092,
    "pages": [1092],
    "part": "part01",
    "vol": "中",
    "columns": COLUMNS,
    "rows": ROWS,
    "row_count": len(ROWS),
    "col_count": len(COLUMNS),
    "status": "verified",
    "notes": "已据 raw OCR 回源核录：workbench/ocr/raw/中/part01/page_0189.txt 与 page_0189.json；表题、表号和表注均在同页。表注：市集、县集分别指市属集体企业、县属集体企业；简介企业不列入此表。灌云县化工厂利税栏源页未见数值，保留空值。",
    "volume": "中",
}

RESIDUE_RE = re.compile(
    r"\n?<p>\(万元（万元）</p>\s*"
    r"<p>（万元）</p>\s*"
    r"<p>全民市锦屏化工厂195818042068844.*?2\.简介企业不列入此表。</p>\s*",
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
        raise SystemExit("TABLES payload not found")
    tables = json.loads(match.group(1))
    updated = False
    for idx, table in enumerate(tables):
        if table.get("table_id") == ENTRY["table_id"]:
            if table != ENTRY:
                tables[idx] = ENTRY
                updated = True
            break
    else:
        tables.append(ENTRY)
        updated = True
    if updated:
        tables.sort(key=lambda t: (str(t.get("vol") or t.get("volume") or ""), int((t.get("pages") or [t.get("page") or 999999])[0]), str(t.get("table_id") or "")))
        text = text[: match.start(1)] + json.dumps(tables, ensure_ascii=False) + text[match.end(1) :]
        SITE.write_text(text, encoding="utf-8")
        return 1
    return 0


def remove_reader_residue() -> int:
    text = HTML.read_text(encoding="utf-8")
    new, count = RESIDUE_RE.subn("\n", text)
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
        "source_raw_text": "workbench/ocr/raw/中/part01/page_0189.txt",
        "source_raw_json": "workbench/ocr/raw/中/part01/page_0189.json",
        "json_changed": json_changed,
        "site_changed": site_changed,
        "reader_residue_blocks_removed": removed,
        "rows": len(ROWS),
        "columns": len(COLUMNS),
    }
    REPORT_JSON.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    md = f"""# 第二十卷化工企业基本情况表残文修复

- 时间：{now}
- 表ID：`{ENTRY['table_id']}`
- 表题：{ENTRY['table_number']} {ENTRY['title']}
- 源页：`workbench/ocr/raw/中/part01/page_0189.txt`、`workbench/ocr/raw/中/part01/page_0189.json`

## 修复动作

- 新增/更新结构化表 JSON：`workbench/table_entries/中/data/LYG-中-T130.json`。
- 表格按 raw OCR 坐标核列，录入 {len(ROWS)} 行、{len(COLUMNS)} 列。
- 从最终阅读版撤出被压成正文的表头单位残片和企业串行段落：{removed} 组。
- 同步结构化表格站 TABLES 数据：{site_changed}。

## 核对说明

- 表题、表号和表注均见 raw OCR 同页。
- 列序按源页横向坐标整理为：单位名称、性质、建厂年份、职工、固定资产原值、主要产品、产值、利税。
- 灌云县化工厂利税栏源页未见数值，保留空值。
"""
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")


def update_memory(removed: int) -> None:
    marker = "## 2026-07-01 第二十卷化工企业基本情况表残文修复"
    entry = f"""
{marker}

- 针对可读性审计命中的第二十卷化学工业表格线性化残文，回源 `workbench/ocr/raw/中/part01/page_0189.txt` 与 `.json` 核对。
- 新增 verified 结构化表：`workbench/table_entries/中/data/LYG-中-T130.json`，表20-15《1990年连云港市化工企业基本情况表》，17 行 8 列。
- 从 `output/final_reader/连云港市志_全书.html` 撤出表头单位残片和企业串行正文残文 {removed} 组，后续由全量嵌回脚本以结构化表展示。
- 报告：`output/reports/reader_readability_chemical_enterprise_table_20260701.md`。
"""
    memory = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker not in memory:
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
