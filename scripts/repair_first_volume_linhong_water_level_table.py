# -*- coding: utf-8 -*-
"""Repair Linhong station water level table in 第一卷 自然环境."""

from __future__ import annotations

import html
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
PROGRESS_PATH = ROOT / "output" / "reports" / "progress" / "20260629_第一卷自然环境_表格专项阶段八_临洪站水位.md"
MEMORY_PATH = ROOT / "PROJECT_MEMORY.md"

SECTION_RE = re.compile(
    r'(<h2 id="第一卷-自然环境">第一卷自然环境</h2>)(.*?)(?=<h2 id="第二卷-建置区划">)',
    re.S,
)
TITLE = "1961～1990年连云港市临洪站水位统计表"
NEXT_TITLE = "连云港市部分灾害年降雨、水位情况表"
PLACEHOLDER = '<p class="table-placeholder">【表格页-待结构化录入】</p>'


def table_html() -> str:
    columns = ["年份", "年最高水位(米)", "最高日期(月·日)", "年最低水位(米)", "最低日期(月·日)", "年平均水位(米)"]
    rows = [
        ["1961", "3.57", "7.7", "1.08", "6.15", ""],
        ["1962", "3.89", "7.21", "0.70", "11.27", "1.63"],
        ["1963", "3.23", "8.8", "1.06", "5.8", "1.41"],
        ["1964", "4.16", "8.5", "0.56", "4.17", "1.56"],
        ["1965", "3.45", "7.26", "0.93", "2.21", "1.88"],
        ["1966", "3.09", "8.17", "0.18", "6.17", "1.93"],
        ["1967", "4.05", "7.17", "1.26", "11.11", ""],
        ["1968", "4.34", "10.1", "1.57", "4.15", ""],
        ["1969", "5.09", "7.24", "河干", "11.22", ""],
        ["1970", "4.84", "8.30", "1.40", "11.28", "2.35"],
        ["1971", "3.65", "7.6", "0.90", "4.23", "2.06"],
        ["1972", "3.57", "7.30", "1.02", "11.29", "2.19"],
        ["1973", "5.93", "8.14", "1.03", "1.16", "2.21"],
        ["1974", "5.19", "8.15", "1.24", "7.17", "2.16"],
        ["1975", "3.61", "7.16", "1.39", "12.20", "2.20"],
        ["1976", "3.53", "7.12", "1.48", "4.10", "1.90"],
        ["1977", "3.43", "8.12", "0.46", "7.1", "2.32"],
        ["1978", "4.08", "9.17", "1.61", "6.18", "2.24"],
        ["1979", "3.56", "7.29", "1.31", "12.21", "2.13"],
        ["1980", "3.33", "9.25", "1.33", "11.28", "2.20"],
        ["1981", "4.08", "7.11", "1.45", "5.28", "2.33"],
        ["1982", "4.23", "7.25", "1.37", "4.16", "2.33"],
        ["1983", "3.98", "9.10", "1.35", "12.19", ""],
        ["1984", "3.33", "5.4", "1.37", "8.7", "2.32"],
        ["1985", "3.31", "7.27", "1.70", "8.8", "2.31"],
        ["1986", "3.43", "10.16", "1.34", "7.24", "2.12"],
        ["1987", "3.41", "7.26", "1.40", "5.15", "2.30"],
        ["1988", "3.52", "6.8", "1.38", "7.19", "2.34"],
        ["1989", "5.02", "8.5", "1.41", "3.13", ""],
        ["1990", "", "", "", "", ""],
    ]
    ths = "".join(f"<th>{html.escape(col)}</th>" for col in columns)
    trs = []
    for row in rows:
        tds = "".join(f"<td>{html.escape(cell)}</td>" for cell in row)
        trs.append(f"<tr>{tds}</tr>")
    table = f'<table class="structured-table"><caption>表1-19 {TITLE}</caption><thead><tr>{ths}</tr></thead><tbody>{"".join(trs)}</tbody></table>'
    table += "\n<p>注：年份按表题1961～1990年顺序补入；1990年及部分年平均水位源 OCR 缺读，空项待对照原图补录。</p>"
    return table


def audit_section(section: str) -> dict[str, int]:
    return {
        "placeholders": section.count('class="table-placeholder"'),
        "structured_tables": section.count('<table class="structured-table"'),
        "table_1_19": section.count(f'<caption>表1-19 {TITLE}</caption>'),
        "title_1_19": section.count(f"<p>{TITLE}</p>"),
        "table_1_20": section.count("连云港市部分灾害年降雨、水位情况表"),
    }


def repair_html() -> tuple[list[str], dict[str, int], dict[str, int]]:
    html_text = HTML_PATH.read_text(encoding="utf-8")
    match = SECTION_RE.search(html_text)
    if not match:
        raise RuntimeError("Cannot locate 第一卷 自然环境 section")

    heading, section = match.groups()
    before = audit_section(section)
    actions: list[str] = []

    if f'<caption>表1-19 {TITLE}</caption>' not in section:
        pattern = re.compile(rf'<p>{re.escape(TITLE)}</p>\n{re.escape(PLACEHOLDER)}\n(?=<p>{re.escape(NEXT_TITLE)})', re.S)
        replacement = f"<p>{TITLE}</p>\n{table_html()}\n"
        section, count = pattern.subn(replacement, section, count=1)
        if count != 1:
            raise RuntimeError("Cannot locate 表1-19 placeholder before 表1-20")
        actions.append("结构化表1-19《1961～1990年连云港市临洪站水位统计表》，替换表题后的占位符；缺读项留空待核图。")

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
    content = f"""# 第一卷自然环境 表格专项阶段八：临洪站水位统计表

更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}

## 本轮范围
- 章节：第一卷 自然环境，第五章水系水文。
- 目标：结构化表1-19临洪站水位统计表，清理水文段一处占位。
- 输入：`workbench/body_chapters/paddle_上/第一卷_自然环境.md` 中表1-19 OCR 段。

## 已完成
{action_lines}

## 统计变化
| 指标 | 修复前 | 修复后 |
| --- | ---: | ---: |
| 第一卷正文表格占位符 | {before['placeholders']} | {after['placeholders']} |
| 第一卷结构化表格 | {before['structured_tables']} | {after['structured_tables']} |
| 表1-19结构化表 | {before['table_1_19']} | {after['table_1_19']} |
| 表1-19正文表题 | {before['title_1_19']} | {after['title_1_19']} |

## 当场验收
- 表1-19水位、日期、年平均水位值来自源 MD 可读 OCR。
- 年份按表题 `1961～1990年` 顺序补入；1990年及部分年平均水位缺读，未臆造，留空并标注待原图补录。
- 未触碰表1-20灾害年降雨、水位情况表的大段 OCR，留待独立核图处理。
- 本脚本可重复运行；再次运行不会重复插入表格。

## 遇到的问题
- 源 OCR 表头存在列顺序断裂，正文数字按表头语义重排为可读表格。
- 源 OCR 未显式读出年份列，需依据表题连续年份补入。
- 1990年行未读出数值，需后续对照 PDF 原图补录。

## 下一步计划
- 继续第一卷表1-18主要河流年、月平均流量特征值表，若 OCR 无法可靠拆列则先建立核图清单。
- 表1-20灾害年降雨水位表为跨页大表，需单独分站处理。
"""
    PROGRESS_PATH.write_text(content, encoding="utf-8")


def update_memory(before: dict[str, int], after: dict[str, int]) -> None:
    entry = f"""
## 2026-06-29 第一卷自然环境表格专项阶段八完成

已完成第一卷临洪站水位统计表专项第八阶段：

- 新增脚本：`scripts/repair_first_volume_linhong_water_level_table.py`。
- 结构化表1-19《1961～1990年连云港市临洪站水位统计表》，缺读项留空并标注待原图补录。
- 第一卷正文表格占位符：{before['placeholders']} -> {after['placeholders']}。
- 第一卷结构化表格：{before['structured_tables']} -> {after['structured_tables']}。
- 已写入进度文档：`output/reports/progress/20260629_第一卷自然环境_表格专项阶段八_临洪站水位.md`。

下一步：继续第一卷表1-18主要河流年、月平均流量特征值表；表1-20灾害年降雨水位表需独立核图。
"""
    memory = MEMORY_PATH.read_text(encoding="utf-8") if MEMORY_PATH.exists() else ""
    marker = "## 2026-06-29 第一卷自然环境表格专项阶段八完成"
    if marker in memory:
        memory = memory[: memory.find(marker)].rstrip() + "\n" + entry.lstrip()
    else:
        memory = memory.rstrip() + "\n\n" + entry.lstrip()
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
