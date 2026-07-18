# -*- coding: utf-8 -*-
"""Remove linearized unit residue for volume 9 table 9-1 after completing T024."""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
TABLE_JSON = ROOT / "workbench" / "table_entries" / "上" / "data" / "LYG-上-T024.json"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_grain_cotton_oil_table9_1_residue_20260702.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_grain_cotton_oil_table9_1_residue_20260702.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260702_第九卷表9-1粮棉油表首页补录与残行清理.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SOURCE_NOTE = "workbench/ocr/paddle_ocr/上/part02/page_0232.txt、page_0233.txt、page_0234.txt"
SCOPE_START = '<h4 id="第九卷-第四章作物栽培-第六节棉花栽培">第六节棉花栽培</h4>'
SCOPE_END = '<h3 id="第九卷-第五章土壤改良与肥料施用">第五章土壤改良与肥料施用</h3>'
CAPTION = "表9-1 1949~1990年连云港市粮、棉、油生产情况统计表"
OLD_CAPTION = "表9-1 1949~1990年连云港市粮、棉、油生产情况统计表续表"
EXPECTED_UNIT_PARAGRAPHS = 24
UNIT_PARAGRAPH_RE = re.compile(r"\n?<p>（(?:万亩|公斤|吨)）</p>\n?", re.M)


def validate_table_json() -> dict[str, object]:
    table = json.loads(TABLE_JSON.read_text(encoding="utf-8"))
    rows = table.get("rows") or []
    years = [str(row[0]) for row in rows if row]
    expected = {"1949", "1950", "1951", "1952", "1953", "1990"}
    missing = sorted(expected.difference(years))
    if table.get("title") != "1949~1990年连云港市粮、棉、油生产情况统计表":
        raise RuntimeError(f"unexpected T024 title: {table.get('title')}")
    if missing:
        raise RuntimeError(f"T024 still misses years: {missing}")
    if len(rows) != 42:
        raise RuntimeError(f"unexpected T024 row_count: {len(rows)}")
    return {
        "table_id": table.get("table_id"),
        "title": table.get("title"),
        "pages": table.get("pages"),
        "row_count": len(rows),
        "first_year": years[0] if years else None,
        "last_year": years[-1] if years else None,
    }


def patch_reader() -> dict[str, object]:
    table_state = validate_table_json()
    text = HTML.read_text(encoding="utf-8")
    if CAPTION not in text:
        raise RuntimeError(f"completed table caption not embedded in reader: {CAPTION}")
    if OLD_CAPTION in text:
        raise RuntimeError(f"old continuation caption remains in reader: {OLD_CAPTION}")

    start = text.index(SCOPE_START)
    end = text.index(SCOPE_END, start)
    segment = text[start:end]
    before_units = UNIT_PARAGRAPH_RE.findall(segment)
    new_segment, removed = UNIT_PARAGRAPH_RE.subn("\n", segment)
    new_segment = re.sub(r"\n{3,}", "\n\n", new_segment)
    if removed:
        text = text[:start] + new_segment + text[end:]
        HTML.write_text(text, encoding="utf-8")

    after = HTML.read_text(encoding="utf-8")
    adjusted_end = end - (len(segment) - len(new_segment))
    after_segment = after[start:adjusted_end]
    remaining_units = UNIT_PARAGRAPH_RE.findall(after_segment)
    if remaining_units:
        raise RuntimeError(f"standalone table 9-1 unit residue remains: {len(remaining_units)}")

    return {
        "table_state": table_state,
        "unit_paragraphs_before_this_run": len(before_units),
        "unit_paragraphs_removed_this_run": removed,
        "unit_paragraphs_cleared_in_scope": EXPECTED_UNIT_PARAGRAPHS,
        "caption_count_after": after.count(CAPTION),
    }


def write_reports(result: dict[str, object]) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "第九卷农林业 / 第四章作物栽培 / 表9-1粮棉油表",
        "source": SOURCE_NOTE,
        "reader_path": str(HTML),
        "table_json": str(TABLE_JSON),
        "principle": "先补齐结构化表9-1首页数据，再删除正文中重复的表头单位线性化残行；不删除正文叙述。",
        "result": result,
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    table_state = result["table_state"]
    md = f"""# 第九卷表9-1粮棉油表首页补录与残行清理

- 时间：{now}
- 范围：`第九卷农林业 / 第四章作物栽培 / 表9-1粮棉油表`
- 源文依据：`{SOURCE_NOTE}`

## 修复动作

- 将 `LYG-上-T024` 从续表状态补齐为完整 `表9-1 1949~1990年连云港市粮、棉、油生产情况统计表`。
- 首页 1949-1953 年数据来自 `page_0232.txt`，续页 1954-1990 年数据保留原核录结果。
- 复跑全量嵌表后，阅读版卷末已核结构化表格中 `LYG-上-T024` 显示完整 1949-1990 年 42 行。
- 删除正文原位置残留的孤立单位段落 `（万亩）/（公斤）/（吨）`，不触碰棉花栽培正文和第五章正文。

## 结果

- 表格：`{table_state['table_id']}`
- 源页：`{table_state['pages']}`
- 行数：{table_state['row_count']}
- 年份范围：{table_state['first_year']} - {table_state['last_year']}
- 累计清理孤立单位段：{result['unit_paragraphs_cleared_in_scope']}
- 本次复跑新增删除：{result['unit_paragraphs_removed_this_run']}
- 阅读版完整表题计数：{result['caption_count_after']}
"""
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")


def update_memory(result: dict[str, object]) -> None:
    marker = "## 2026-07-02 第九卷表9-1粮棉油表首页补录与残行清理"
    memory = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker in memory:
        return
    table_state = result["table_state"]
    entry = f"""
{marker}

- 对第九卷农林业第四章作物栽培末尾 `表9-1 1949~1990年连云港市粮、棉、油生产情况统计表` 做小闭环修复。
- 源文依据：`{SOURCE_NOTE}`；`LYG-上-T024` 已由续表补齐为完整表，覆盖 {table_state['first_year']} - {table_state['last_year']} 共 {table_state['row_count']} 行。
- 已复跑 `scripts/embed_verified_tables_into_reader.py` 同步主阅读版卷末已核结构化表格；正文原位置累计清理 `（万亩）/（公斤）/（吨）` 孤立单位残段 {result['unit_paragraphs_cleared_in_scope']} 个。
- 报告：`output/reports/reader_readability_grain_cotton_oil_table9_1_residue_20260702.md`。
"""
    MEMORY.write_text(memory.rstrip() + "\n\n" + entry.lstrip(), encoding="utf-8")


def main() -> None:
    result = patch_reader()
    write_reports(result)
    update_memory(result)
    print("table 9-1 residue repaired")
    print(f"unit_paragraphs_removed_this_run={result['unit_paragraphs_removed_this_run']}")
    print(f"unit_paragraphs_cleared_in_scope={result['unit_paragraphs_cleared_in_scope']}")
    print(f"caption_count_after={result['caption_count_after']}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()
