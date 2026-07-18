# -*- coding: utf-8 -*-
"""Repair verified climate tables in 第一卷 自然环境."""

from __future__ import annotations

import html
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
PROGRESS_PATH = ROOT / "output" / "reports" / "progress" / "20260629_第一卷自然环境_表格专项阶段二_气候要素.md"
MEMORY_PATH = ROOT / "PROJECT_MEMORY.md"

SECTION_RE = re.compile(
    r'(<h2 id="第一卷-自然环境">第一卷自然环境</h2>)(.*?)(?=<h2 id="第二卷-建置区划">)',
    re.S,
)
PLACEHOLDER = '<p class="table-placeholder">【表格页-待结构化录入】</p>\n'


def table_html(caption: str, columns: list[str], rows: list[list[str]], note: str | None = None) -> str:
    ths = ''.join(f"<th>{html.escape(col)}</th>" for col in columns)
    trs = []
    for row in rows:
        tds = ''.join(f"<td>{html.escape(cell)}</td>" for cell in row)
        trs.append(f"<tr>{tds}</tr>")
    table = f'<table class="structured-table"><caption>{html.escape(caption)}</caption><thead><tr>{ths}</tr></thead><tbody>{"".join(trs)}</tbody></table>'
    if note:
        table += f"\n<p>{html.escape(note)}</p>"
    return table


def audit_section(section: str) -> dict[str, int]:
    return {
        "placeholders": section.count('class="table-placeholder"'),
        "structured_tables": section.count('<table class="structured-table"'),
        "table_1_4": section.count('<caption>表1-4 连云港市各月太阳总辐射量表</caption>'),
        "table_1_6": section.count('<caption>表1-6 连云港市各月平均气压和极端最高、最低气压表</caption>'),
        "raw_1_4": section.count('连云港市各月太阳总辐射量表表1-4单位：千卡/平方厘米月份全年总辐射'),
        "raw_1_6": section.count('连云港市各月平均气压和极端最高、最低气压表表1-6单位：百帕'),
    }


def repair_html() -> tuple[list[str], dict[str, int], dict[str, int]]:
    html_text = HTML_PATH.read_text(encoding="utf-8")
    match = SECTION_RE.search(html_text)
    if not match:
        raise RuntimeError("Cannot locate 第一卷 自然环境 section")

    heading, section = match.groups()
    before = audit_section(section)
    actions: list[str] = []

    months = [f"{i}月" for i in range(1, 13)]
    table_1_4 = table_html(
        "表1-4 连云港市各月太阳总辐射量表",
        ["项目", *months, "全年"],
        [["总辐射(千卡/平方厘米)", "6.7", "7.7", "10.7", "11.6", "14.0", "13.7", "12.3", "12.7", "10.5", "5.4", "6.9", "6.2", "122.2"]],
    )
    raw_1_4 = re.compile(
        r'<p>连云港市各月太阳总辐射量表表1-4单位：千卡/平方厘米月份全年总辐射'
        r'6\.77\.710\.711\.614\.013\.712\.312\.710\.55\.46\.96\.2122\.2</p>\n'
        + re.escape(PLACEHOLDER),
        re.S,
    )
    section, count_1_4 = raw_1_4.subn(table_1_4 + "\n", section, count=1)
    if count_1_4:
        actions.append("结构化表1-4《连云港市各月太阳总辐射量表》，替换串行 OCR 表格文本和占位符。")

    table_1_6 = table_html(
        "表1-6 连云港市各月平均气压和极端最高、最低气压表",
        ["项目", *months],
        [
            ["平均气压(百帕)", "1027.3", "1025.5", "1021.4", "1015.5", "1010.7", "1005.9", "1003.6", "1006.2", "1013.6", "1020.5", "1024.8", "1027.1"],
            ["极端最高气压(百帕)", "1045.8", "1042.4", "1038.7", "1034.8", "1024.6", "1018.0", "1013.4", "1017.4", "1025.8", "1033.5", "1044.5", "1046.0"],
            ["极端最低气压(百帕)", "1006.3", "1000.0", "997.5", "994.5", "994.7", "992.2", "988.9", "989.2", "997.7", "1005.1", "1009.7", "1008.3"],
        ],
        "注：资料年份为1951～1990年；原表年份行 OCR 缺值，待对照原图补录。",
    )
    raw_1_6 = re.compile(
        re.escape(PLACEHOLDER)
        + r'<p>连云港市各月平均气压和极端最高、最低气压表表1-6单位：百帕月份气项目压平均'
        r'1027\.31025\.51021\.41015\.51010\.71005\.91003\.61006\.21013\.61020\.51024\.81027\.1'
        r'极端最高1045\.81042\.41038\.71034\.81024\.61018\.01013\.41017\.41025\.81033\.51044\.51046\.0'
        r'年份极端最低1006\.31000\.0997\.5994\.5994\.7992\.2988\.9989\.2997\.71005\.11009\.71008\.3年份注：资料年份为1951～1990年。</p>',
        re.S,
    )
    section, count_1_6 = raw_1_6.subn(table_1_6, section, count=1)
    if count_1_6:
        actions.append("结构化表1-6《连云港市各月平均气压和极端最高、最低气压表》，替换占位符和串行 OCR 表格文本；年份行标记待核图。")

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
    content = f"""# 第一卷自然环境 表格专项阶段二：气候要素

更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}

## 本轮范围
- 章节：第一卷 自然环境，第四章气候，第二节气候要素。
- 目标：优先结构化 OCR 数值完整、行列关系明确的气候要素小表。
- 输入：`workbench/body_chapters/paddle_上/第一卷_自然环境.md` 与最终阅读版相同段落。

## 已完成
{action_lines}

## 统计变化
| 指标 | 修复前 | 修复后 |
| --- | ---: | ---: |
| 第一卷正文表格占位符 | {before['placeholders']} | {after['placeholders']} |
| 第一卷结构化表格 | {before['structured_tables']} | {after['structured_tables']} |
| 表1-4结构化表 | {before['table_1_4']} | {after['table_1_4']} |
| 表1-6结构化表 | {before['table_1_6']} | {after['table_1_6']} |
| 表1-4串行OCR残留 | {before['raw_1_4']} | {after['raw_1_4']} |
| 表1-6串行OCR残留 | {before['raw_1_6']} | {after['raw_1_6']} |

## 当场验收
- 表1-4的 1～12 月及全年总辐射数值来自源 MD，行列关系明确。
- 表1-6的平均、极端最高、极端最低三行数值来自源 MD；原表年份行 OCR 缺值，未臆造补齐，已在表下注明待核图。
- 本脚本可重复运行；再次运行不会重复插入表格。

## 遇到的问题
- 表1-6疑有年份行，但当前 OCR 只保留“年份”字样，没有对应月份年份值，需 PDF 原图补录。
- 同一气候章节中表1-7、风速湿度、地温温差等表仍有串行 OCR 或跨页碎片，需要继续逐表处理。

## 下一步计划
- 继续第一卷气候表格：优先核对表1-7气温、风速/湿度、表1-14地温温差等剩余占位。
- 对跨页水文和灾害宽表转入 PDF 页图专项核对。
"""
    PROGRESS_PATH.write_text(content, encoding="utf-8")


def update_memory(before: dict[str, int], after: dict[str, int]) -> None:
    entry = f"""
## 2026-06-29 第一卷自然环境表格专项阶段二完成

已完成第一卷气候要素表格专项第二阶段：

- 新增脚本：`scripts/repair_first_volume_climate_tables.py`。
- 结构化表1-4《连云港市各月太阳总辐射量表》。
- 结构化表1-6《连云港市各月平均气压和极端最高、最低气压表》；年份行 OCR 缺值，已标记待对照原图补录。
- 第一卷正文表格占位符：{before['placeholders']} -> {after['placeholders']}。
- 第一卷结构化表格：{before['structured_tables']} -> {after['structured_tables']}。
- 已写入进度文档：`output/reports/progress/20260629_第一卷自然环境_表格专项阶段二_气候要素.md`。

下一步：继续第一卷气候章节剩余表格和水文跨页表核对。
"""
    memory = MEMORY_PATH.read_text(encoding="utf-8") if MEMORY_PATH.exists() else ""
    marker = "## 2026-06-29 第一卷自然环境表格专项阶段二完成"
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
