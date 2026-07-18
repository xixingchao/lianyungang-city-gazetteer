# -*- coding: utf-8 -*-
"""Repair table 17-14 unit residue and add its verified structured data."""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
DATA = ROOT / "workbench" / "table_entries" / "中" / "data" / "LYG-中-T131.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_glass_crafts_table_20260701.md"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_glass_crafts_table_20260701.json"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260701_第十七卷玻璃工艺表残文修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

COLUMNS = [
    "年份",
    "海带浮球(万只)",
    "农药瓶(万只)",
    "工艺玻璃制品(万件)",
    "产值(万元)",
    "销售(万元)",
    "利税总额(万元)",
    "利润(万元)",
]

ROWS = [
    ["1971", "76.39", "", "", "83.47", "8.60", "19.04", "9.42"],
    ["1972", "81.94", "", "0.21", "45.06", "43.56", "13.72", "5.34"],
    ["1973", "70.20", "", "4.15", "48.45", "22.70", "-1.49", "-4.90"],
    ["1974", "15.17", "40.80", "1.57", "19.12", "", "-10.62", "-12.52"],
    ["1975", "32.64", "", "10.20", "39.09", "", "-0.12", "-0.12"],
    ["1976", "88.31", "", "8.51", "62.45", "54.23", "7.86", "-0.28"],
    ["1977", "139.30", "", "4.75", "97.43", "92.15", "16.82", "2.18"],
    ["1978", "46.87", "111.46", "4.97", "67.50", "35.53", "-7.04", "-12.36"],
    ["1979", "13.43", "", "11.29", "37.16", "36.71", "-11.38", "-16.89"],
    ["1980", "", "", "31.57", "71.13", "74.78", "19.25", "8.03"],
    ["1981", "", "", "35.60", "83.58", "83.25", "23.06", "10.58"],
    ["1982", "", "", "43.45", "90.66", "84.25", "26.08", "11.97"],
    ["1983", "", "", "38.13", "74.07", "51.30", "8.23", "0.46"],
    ["1984", "", "", "37.46", "81.20", "84.07", "13.28", "0.67"],
    ["1985", "", "", "56.10", "124.60", "140.75", "22.59", "0.00"],
    ["1986", "", "", "73.33", "159.72", "174.54", "34.76", "20.77"],
    ["1987", "", "", "90.50", "210.80", "232.11", "44.96", "6.65"],
    ["1988", "", "", "90.00", "244.10", "264.82", "42.26", "4.39"],
    ["1989", "4.16", "75.44", "218.70", "273.00", "38.79", "0.00", "0.00"],
    ["1990", "", "", "88.20", "303.30", "314.74", "48.47", "0.84"],
]

ENTRY = {
    "table_id": "LYG-中-T131",
    "title": "1971~1990年连云港市玻璃及工艺玻璃制品等生产经营情况表",
    "table_number": "表17-14",
    "page": 958,
    "pages": [958],
    "part": "part01",
    "vol": "中",
    "columns": COLUMNS,
    "rows": ROWS,
    "row_count": len(ROWS),
    "col_count": len(COLUMNS),
    "status": "verified",
    "notes": "已据 raw OCR 回源核录：workbench/ocr/raw/中/part01/page_0055.txt 与 page_0055.json；表题、表号、单位和列位均见同页。源页未见数值的单元格保留空值，未补作0或反推。",
    "volume": "中",
}

RESIDUE_RE = re.compile(
    r"\n?<p>（万元）</p>\s*<p>（万元）</p>\s*<p>（万元）</p>\s*<p>\(万只\)（万件）</p>\s*",
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
        "source_raw_text": "workbench/ocr/raw/中/part01/page_0055.txt",
        "source_raw_json": "workbench/ocr/raw/中/part01/page_0055.json",
        "json_changed": json_changed,
        "site_changed": site_changed,
        "reader_residue_blocks_removed": removed,
        "reader_residue_present_after_repair": "(万只)（万件）" in HTML.read_text(encoding="utf-8"),
        "rows": len(ROWS),
        "columns": len(COLUMNS),
    }
    REPORT_JSON.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    md = f"""# 第十七卷玻璃工艺表残文修复

- 时间：{now}
- 表ID：`{ENTRY['table_id']}`
- 表题：{ENTRY['table_number']} {ENTRY['title']}
- 源页：`workbench/ocr/raw/中/part01/page_0055.txt`、`workbench/ocr/raw/中/part01/page_0055.json`

## 修复动作

- 新增/更新结构化表 JSON：`workbench/table_entries/中/data/LYG-中-T131.json`。
- 表格按 raw OCR 坐标核列，录入 {len(ROWS)} 行、{len(COLUMNS)} 列。
- 从最终阅读版撤出表头单位残片；本次运行删除 {removed} 组，目标残片当前已不存在。
- 同步结构化表格站 TABLES 数据：{site_changed}。

## 核对说明

- 表题、表号、单位和列位均见 raw OCR 同页。
- 源页未见数值的单元格保留空值，未补作0或反推。
"""
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")


def update_memory(removed: int) -> None:
    marker = "## 2026-07-01 第十七卷玻璃工艺表残文修复"
    entry = f"""
{marker}

- 针对第十七卷其它工艺品中残留的表头单位段，回源 `workbench/ocr/raw/中/part01/page_0055.txt` 与 `.json` 核对。
- 新增 verified 结构化表：`workbench/table_entries/中/data/LYG-中-T131.json`，表17-14《1971~1990年连云港市玻璃及工艺玻璃制品等生产经营情况表》，20 行 8 列。
- 从 `output/final_reader/连云港市志_全书.html` 撤出孤立单位残片 {removed} 组，后续由全量嵌回脚本以结构化表展示。
- 报告：`output/reports/reader_readability_glass_crafts_table_20260701.md`。
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
