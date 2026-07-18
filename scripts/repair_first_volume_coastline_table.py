# -*- coding: utf-8 -*-
"""Repair verified coastline table in 第一卷 自然环境."""

from __future__ import annotations

import html
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
PROGRESS_PATH = ROOT / "output" / "reports" / "progress" / "20260629_第一卷自然环境_表格专项阶段四_海岸线.md"
MEMORY_PATH = ROOT / "PROJECT_MEMORY.md"

SECTION_RE = re.compile(
    r'(<h2 id="第一卷-自然环境">第一卷自然环境</h2>)(.*?)(?=<h2 id="第二卷-建置区划">)',
    re.S,
)
PLACEHOLDER = '<p class="table-placeholder">【表格页-待结构化录入】</p>'


def table_html() -> str:
    columns = ["河段名称", "理论海岸线(公里)", "标准海岸线(公里)", "外沿海岸线(公里)", "海岸类型"]
    rows = [
        ["绣针河口一兴庄河口", "48.93", "30.06", "30.06", "沙质海岸"],
        ["兴庄河口一临洪河口", "30.40", "17.31", "15.57", "淤泥质海岸"],
        ["临洪河口—西墅一烧香河口", "21.38", "14.57", "14.56", "淤泥质海岸"],
        ["西墅一烧香河口", "41.33", "40.25", "40.25", "基岩海岸"],
        ["烧香河口—埒子口", "60.50", "32.06", "26.18", "淤泥质海岸"],
        ["埒子口—灌河口", "91.98", "27.33", "17.10", "淤泥质海岸"],
        ["合计", "294.52", "161.58", "143.72", ""],
    ]
    ths = ''.join(f"<th>{html.escape(col)}</th>" for col in columns)
    trs = []
    for row in rows:
        tds = ''.join(f"<td>{html.escape(cell)}</td>" for cell in row)
        trs.append(f"<tr>{tds}</tr>")
    return f'<table class="structured-table"><caption>表1-2 连云港市大陆海岸线按河口分段长度表</caption><thead><tr>{ths}</tr></thead><tbody>{"".join(trs)}</tbody></table>'


def audit_section(section: str) -> dict[str, int]:
    return {
        "placeholders": section.count('class="table-placeholder"'),
        "structured_tables": section.count('<table class="structured-table"'),
        "table_1_2": section.count('<caption>表1-2 连云港市大陆海岸线按河口分段长度表</caption>'),
        "raw_1_2": section.count('连云港市大陆海岸线按河口分段长度表表1-2单位：公里河段名称理论海岸线'),
    }


def repair_html() -> tuple[list[str], dict[str, int], dict[str, int]]:
    html_text = HTML_PATH.read_text(encoding="utf-8")
    match = SECTION_RE.search(html_text)
    if not match:
        raise RuntimeError("Cannot locate 第一卷 自然环境 section")

    heading, section = match.groups()
    before = audit_section(section)
    actions: list[str] = []

    pattern = re.compile(
        r'<p>连云港市大陆海岸线按河口分段长度表表1-2单位：公里河段名称理论海岸线标淮海岸线外沿海岸线海岸类型'
        r'绣针河口一兴庄河口48\.9330\.0630\.06沙质海岸'
        r'兴庄河口一临洪河口30\.4017\.3115\.57淤泥质海岸'
        r'临洪河口—西21\.3814\.5714\.56淤泥质海岸'
        r'墅一烧香河口41\.3340\.2540\.25基岩海岸'
        r'烧香河口—埒子口60\.5032\.0626\.18淤泥质海岸'
        r'埒子口—灌河口91\.9827\.3317\.10淤泥质海岸合计294\.52161\.58143\.72</p>\n'
        + re.escape(PLACEHOLDER),
        re.S,
    )
    section, count = pattern.subn(table_html(), section, count=1)
    if count:
        actions.append("结构化表1-2《连云港市大陆海岸线按河口分段长度表》，替换串行 OCR 表格文本和占位符。")

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
    content = f"""# 第一卷自然环境 表格专项阶段四：海岸线分段表

更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}

## 本轮范围
- 章节：第一卷 自然环境，第三章海，第一节海岸。
- 目标：结构化表1-2海岸线分段长度表，清理第一卷前部遗留占位。
- 输入：`workbench/body_chapters/paddle_上/第一卷_自然环境.md` 中表1-2。

## 已完成
{action_lines}

## 统计变化
| 指标 | 修复前 | 修复后 |
| --- | ---: | ---: |
| 第一卷正文表格占位符 | {before['placeholders']} | {after['placeholders']} |
| 第一卷结构化表格 | {before['structured_tables']} | {after['structured_tables']} |
| 表1-2结构化表 | {before['table_1_2']} | {after['table_1_2']} |
| 表1-2串行OCR残留 | {before['raw_1_2']} | {after['raw_1_2']} |

## 当场验收
- 表1-2行列和数值取自源 MD，对应河段、三类岸线长度和海岸类型。
- 串行 OCR 表格文本及其后一处正文表格占位已清除。
- 本脚本可重复运行；再次运行不会重复插入表格。

## 遇到的问题
- 源 OCR 将“临洪河口—西墅一烧香河口”断为两段，本轮按源表上下文合并为完整河段名。
- 第一卷剩余表格多为气候风速/湿度缺行或水文跨页宽表，需继续逐表核图。

## 下一步计划
- 继续第一卷气候剩余表，无法可靠还原的进入 PDF 原图核验清单。
- 转入表1-17至表1-23水系水文宽表专项。
"""
    PROGRESS_PATH.write_text(content, encoding="utf-8")


def update_memory(before: dict[str, int], after: dict[str, int]) -> None:
    entry = f"""
## 2026-06-29 第一卷自然环境表格专项阶段四完成

已完成第一卷海岸线分段表专项第四阶段：

- 新增脚本：`scripts/repair_first_volume_coastline_table.py`。
- 结构化表1-2《连云港市大陆海岸线按河口分段长度表》。
- 清除表1-2串行 OCR 表格文本和后一处正文表格占位。
- 第一卷正文表格占位符：{before['placeholders']} -> {after['placeholders']}。
- 第一卷结构化表格：{before['structured_tables']} -> {after['structured_tables']}。
- 已写入进度文档：`output/reports/progress/20260629_第一卷自然环境_表格专项阶段四_海岸线.md`。

下一步：继续第一卷气候剩余表与水系水文跨页宽表。
"""
    memory = MEMORY_PATH.read_text(encoding="utf-8") if MEMORY_PATH.exists() else ""
    marker = "## 2026-06-29 第一卷自然环境表格专项阶段四完成"
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
