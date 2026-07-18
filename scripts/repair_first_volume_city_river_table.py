# -*- coding: utf-8 -*-
"""Repair verified city river table in 第一卷 自然环境."""

from __future__ import annotations

import html
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
PROGRESS_PATH = ROOT / "output" / "reports" / "progress" / "20260629_第一卷自然环境_表格专项阶段五_市区河流.md"
MEMORY_PATH = ROOT / "PROJECT_MEMORY.md"

SECTION_RE = re.compile(
    r'(<h2 id="第一卷-自然环境">第一卷自然环境</h2>)(.*?)(?=<h2 id="第二卷-建置区划">)',
    re.S,
)
PLACEHOLDER = '<p class="table-placeholder">【表格页-待结构化录入】</p>'


def table_html() -> str:
    columns = [
        "河流名称",
        "市区内长度(公里)",
        "流向",
        "底高程(米)",
        "口宽/底宽(米)",
        "坡比",
        "常水位(米)",
        "高水位(米)",
        "控制闸",
        "备注",
    ]
    rows = [
        ["蔷薇河", "15.5", "北", "-1", "70～90", "1:3", "1.8", "5.95", "临洪闸", ""],
        ["临洪河", "12.5", "北", "-1～2", "1100～2200", "", "", "5.95", "", "潮水河；流域面积市境内240平方公里"],
        ["西盐河", "16.0", "南北", "-1", "", "1:3", "1.6", "3.50", "善后闸", ""],
        ["龙尾河", "5.4", "南北", "±0", "15～30", "1:2～3", "1.6", "3.50", "", "盐河南"],
        ["大浦河", "7.5", "北", "-1", "", "1:3", "1.0～1.6", "3.40", "大浦闸；电厂闸", "流域面积市境127平方公里"],
        ["玉带河", "8.0", "东", "-1", "", "1:3", "1.7", "3.40", "玉带河闸", ""],
        ["东盐河", "11.0", "北", "-1", "", "1:3", "1.6", "3.40", "猴嘴闸", ""],
        ["排淡河", "21.0", "北东", "-1～2.5", "10～30", "1:3", "1.5", "3.00", "大板桥闸", ""],
        ["泊阳河（卓王河）", "14.0", "东", "-1", "", "", "1.7", "3.40", "善后闸", ""],
        ["烧香河", "26.0", "东", "", "", "", "", "", "烧香河闸", ""],
    ]
    ths = ''.join(f"<th>{html.escape(col)}</th>" for col in columns)
    trs = []
    for row in rows:
        tds = ''.join(f"<td>{html.escape(cell)}</td>" for cell in row)
        trs.append(f"<tr>{tds}</tr>")
    table = f'<table class="structured-table"><caption>表1-17 连云港市市区主要河流情况表</caption><thead><tr>{ths}</tr></thead><tbody>{"".join(trs)}</tbody></table>'
    table += "\n<p>注：根据源 MD 可读 OCR 项阶段性结构化；设计流量、实际最大流量等缺读项待对照原图补录。</p>"
    return table


def audit_section(section: str) -> dict[str, int]:
    return {
        "placeholders": section.count('class="table-placeholder"'),
        "structured_tables": section.count('<table class="structured-table"'),
        "table_1_17": section.count('<caption>表1-17 连云港市市区主要河流情况表</caption>'),
    }


def repair_html() -> tuple[list[str], dict[str, int], dict[str, int]]:
    html_text = HTML_PATH.read_text(encoding="utf-8")
    match = SECTION_RE.search(html_text)
    if not match:
        raise RuntimeError("Cannot locate 第一卷 自然环境 section")

    heading, section = match.groups()
    before = audit_section(section)
    actions: list[str] = []

    target = '<p>连云港市市区主要河流情况表</p>\n' + PLACEHOLDER
    if target in section:
        section = section.replace(target, table_html(), 1)
        actions.append("结构化表1-17《连云港市市区主要河流情况表》，替换一处表格占位；缺读列留空并标注待核图。")

    fixed = html_text[: match.start()] + heading + section + html_text[match.end() :]
    if fixed != html_text:
        HTML_PATH.write_text(fixed, encoding="utf-8")

    after_match = SECTION_RE.search(fixed)
    if not after_match:
        raise RuntimeError("Cannot locate 第一卷 after repair")
    after = audit_section(after_match.group(2))
    return actions, before, after


def write_progress(actions: list[str], before: dict[str, int], after: dict[str, int]) -> None:
    action_lines = "\n".join(f"- {action}" for action in actions) or "- 本次复跑未产生新改动，脚本保持幂等。"
    content = f"""# 第一卷自然环境 表格专项阶段五：市区主要河流表

更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}

## 本轮范围
- 章节：第一卷 自然环境，第五章水系水文，第一节水系。
- 目标：将表1-17从纯占位提升为可读结构化表，保留缺读字段待原图补录。
- 输入：`workbench/body_chapters/paddle_上/第一卷_自然环境.md` 中表1-17 OCR 段。

## 已完成
{action_lines}

## 统计变化
| 指标 | 修复前 | 修复后 |
| --- | ---: | ---: |
| 第一卷正文表格占位符 | {before['placeholders']} | {after['placeholders']} |
| 第一卷结构化表格 | {before['structured_tables']} | {after['structured_tables']} |
| 表1-17结构化表 | {before['table_1_17']} | {after['table_1_17']} |

## 当场验收
- 表1-17河流名称、长度、流向、底高程、口宽/底宽、水位和控制闸等字段取自源 MD 可读 OCR。
- 设计流量、实际最大流量等缺读字段未臆造，保留为空并在表下注明待对照原图补录。
- 本脚本可重复运行；再次运行不会重复插入表格。

## 遇到的问题
- 源 OCR 表头和多列数据错位明显，不足以一次性达到完整表格终稿。
- 表1-18至表1-23多为跨页水文宽表，仍需 PDF 原图核图或更细的 OCR 表格抽取。

## 下一步计划
- 继续第一卷水系水文表：优先检查表1-18、表1-19、表1-22、表1-23是否可分批结构化。
- 将缺读字段和需核图表格纳入后续 PDF 专项清单。
"""
    PROGRESS_PATH.write_text(content, encoding="utf-8")


def update_memory(before: dict[str, int], after: dict[str, int]) -> None:
    entry = f"""
## 2026-06-29 第一卷自然环境表格专项阶段五完成

已完成第一卷市区主要河流表专项第五阶段：

- 新增脚本：`scripts/repair_first_volume_city_river_table.py`。
- 结构化表1-17《连云港市市区主要河流情况表》，缺读列留空并标注待原图补录。
- 第一卷正文表格占位符：{before['placeholders']} -> {after['placeholders']}。
- 第一卷结构化表格：{before['structured_tables']} -> {after['structured_tables']}。
- 已写入进度文档：`output/reports/progress/20260629_第一卷自然环境_表格专项阶段五_市区河流.md`。

下一步：继续第一卷水系水文跨页宽表专项。
"""
    memory = MEMORY_PATH.read_text(encoding="utf-8") if MEMORY_PATH.exists() else ""
    marker = "## 2026-06-29 第一卷自然环境表格专项阶段五完成"
    if marker in memory:
        memory = memory[: memory.find(marker)].rstrip() + "\n" + entry
    else:
        memory = memory.rstrip() + "\n" + entry
    MEMORY_PATH.write_text(memory, encoding="utf-8")


def main() -> None:
    actions, before, after = repair_html()
    if actions or not PROGRESS_PATH.exists():
        write_progress(actions, before, after)
    if actions:
        update_memory(before, after)
    print("Repair complete")
    for action in actions:
        print(f"- {action}")
    if not actions:
        print("- no html changes; idempotent rerun")
    print(f"before={before}")
    print(f"after={after}")
    print(f"progress={PROGRESS_PATH}")


if __name__ == "__main__":
    main()
