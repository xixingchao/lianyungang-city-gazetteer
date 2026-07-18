# -*- coding: utf-8 -*-
"""Repair flood control organization table in 第十卷 水利."""

from __future__ import annotations

import html
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
PROGRESS_PATH = ROOT / "output" / "reports" / "progress" / "20260629_第十卷水利_表格专项阶段一_防汛抗旱机构.md"
MEMORY_PATH = ROOT / "PROJECT_MEMORY.md"

SECTION_RE = re.compile(
    r'(<h2 id="第十卷-水利">第十卷水利</h2>)(.*?)(?=<h2 id="第十一卷-畜牧业">)',
    re.S,
)
PLACEHOLDER = '<p class="table-placeholder">【表格页-待结构化录入】</p>'
TITLE = "1950～1990年连云港市防汛抗旱指挥机构情况表"


def table_html() -> str:
    columns = ["机构名称", "指挥（总队长）姓名", "任职时间", "备注"]
    rows = [
        ["新海县人民政府防汛总队部", "周子虹", "", "源 OCR 重复出现姓名，任职时间缺读"],
        ["新海连市人民政府防汛总队部", "许耀林", "1952～1953", ""],
        ["新海连市人民委员会防汛防旱总队部", "许耀林", "", "续表首行，任职时间缺读"],
        ["新海连市人民委员会防汛防旱总队部", "张书伦", "", "任职时间缺读"],
        ["新海连市人民委员会防汛防旱总队部", "周思德", "1956～1957", ""],
        ["新海连市人民委员会防汛防旱总队部", "季士杰", "1958～1961", ""],
        ["新海连市人民委员会防汛防旱指挥部", "季士杰", "", "任职时间缺读"],
        ["新海连市人民委员会防汛防旱指挥部", "陈心文", "1963～1966", ""],
        ["连云港市人民委员会防汛防旱指挥部", "陈心文", "1970～1973", ""],
        ["连云港市人民委员会防汛防旱指挥部", "徐河均", "1974～1979", ""],
        ["连云港市革命委员会防汛抗旱指挥部", "徐河均", "1980～1982", ""],
        ["连云港市人民政府防汛抗旱指挥部", "李登先", "1983～1984", ""],
        ["连云港市人民政府防汛抗旱指挥部", "唐贯淮", "", "任职时间缺读"],
        ["连云港市人民政府防汛抗旱指挥部", "周国林", "1986～1988", ""],
        ["连云港市人民政府防汛抗旱指挥部", "刘步生", "1989～", ""],
    ]
    ths = "".join(f"<th>{html.escape(col)}</th>" for col in columns)
    trs = []
    for row in rows:
        tds = "".join(f"<td>{html.escape(cell)}</td>" for cell in row)
        trs.append(f"<tr>{tds}</tr>")
    table = f'<table class="structured-table"><caption>表10-22 {TITLE}</caption><thead><tr>{ths}</tr></thead><tbody>{"".join(trs)}</tbody></table>'
    table += "\n<p>注：据源 OCR 分页文字整理；个别任职时间源 OCR 缺读，未臆补，留空并在备注中标明。</p>"
    return table


def audit_section(section: str) -> dict[str, int]:
    return {
        "placeholders": section.count('class="table-placeholder"'),
        "structured_tables": section.count('<table class="structured-table"'),
        "table_10_22": section.count(f'<caption>表10-22 {TITLE}</caption>'),
        "raw_10_22": section.count(f'{TITLE}表10-22'),
        "table_10_23": section.count('表10-23 1990年连云港市报汛站网基本情况表'),
    }


def repair_html() -> tuple[list[str], dict[str, int], dict[str, int]]:
    html_text = HTML_PATH.read_text(encoding="utf-8")
    match = SECTION_RE.search(html_text)
    if not match:
        raise RuntimeError("Cannot locate 第十卷 水利 section")

    heading, section = match.groups()
    before = audit_section(section)
    actions: list[str] = []

    if f'<caption>表10-22 {TITLE}</caption>' not in section:
        raw = (
            f"<p>{TITLE}表10-22机构名称指挥（总队长）姓名任职时间新海县人民政府防汛总队部周子虹周子虹新海连市人民政府防汛总队部许耀林1952～1953</p>\n"
            f"{PLACEHOLDER}\n"
            f"{PLACEHOLDER}\n"
            "<p>续上表机构名称指挥（总队长）姓名任职时间许耀林新海连市人民委员会张书伦防汛防旱总队部周思德1956～1957季士杰1958～1961新海连市人民委员会防汛防旱指挥部季士杰陈心文1963～1966连云港市人民委员会防汛防旱指挥部陈心文1970～1973徐河均1974～1979连云港市革命委员会防汛抗旱指挥部徐河均1980～1982李登先1983～1984连云港市人民政府唐贯淮防汛抗旱指挥部周国林1986～1988刘步生1989～</p>"
        )
        replacement = f"<p>{TITLE}</p>\n{table_html()}"
        if raw not in section:
            raise RuntimeError("Cannot locate 表10-22 raw block")
        section = section.replace(raw, replacement, 1)
        actions.append("结构化表10-22《1950～1990年连云港市防汛抗旱指挥机构情况表》，清理两处表页占位和续表串行 OCR。")

    fixed = html_text[: match.start()] + heading + section + html_text[match.end() :]
    if fixed != html_text:
        HTML_PATH.write_text(fixed, encoding="utf-8")

    after_match = SECTION_RE.search(fixed)
    if not after_match:
        raise RuntimeError("Cannot locate 第十卷 after repair")
    after = audit_section(after_match.group(2))
    return actions, before, after


def write_progress(actions: list[str], before: dict[str, int], after: dict[str, int]) -> None:
    action_lines = "\n".join(f"- {action}" for action in actions) or "- 本次复跑未产生新改动，脚本保持幂等。"
    content = f"""# 第十卷水利 表格专项阶段一：防汛抗旱指挥机构表

更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}

## 本轮范围
- 章节：第十卷 水利，第七章防汛抗灾。
- 目标：结构化表10-22防汛抗旱指挥机构情况表，清理连续表格页占位。
- 输入：`workbench/body_chapters/paddle_上/第十卷至第十六卷（part03）.md` 中表10-22 OCR 段。

## 已完成
{action_lines}

## 统计变化
| 指标 | 修复前 | 修复后 |
| --- | ---: | ---: |
| 第十卷正文表格占位符 | {before['placeholders']} | {after['placeholders']} |
| 第十卷结构化表格 | {before['structured_tables']} | {after['structured_tables']} |
| 表10-22结构化表 | {before['table_10_22']} | {after['table_10_22']} |
| 表10-22串行OCR残留 | {before['raw_10_22']} | {after['raw_10_22']} |
| 表10-23结构化表 | {before['table_10_23']} | {after['table_10_23']} |

## 当场验收
- 表10-22机构名称、指挥姓名、任职时间均来自源 OCR 分页文字。
- 个别源 OCR 缺读的任职时间留空，不做推断。
- 清理表10-22前后两处连续正文表格占位符。
- 本脚本可重复运行；再次运行不会重复插入表格。

## 下一步计划
- 继续第十卷表10-23报汛站网基本情况表，该表含多页续表和复选标记。
- 再转入表10-21农田基本建设工程效益表。
"""
    PROGRESS_PATH.write_text(content, encoding="utf-8")


def update_memory(before: dict[str, int], after: dict[str, int]) -> None:
    entry = f"""
## 2026-06-29 第十卷水利表格专项阶段一完成

已完成第十卷防汛抗旱指挥机构表专项第一阶段：

- 新增脚本：`scripts/repair_tenth_volume_flood_control_org_table.py`。
- 结构化表10-22《1950～1990年连云港市防汛抗旱指挥机构情况表》，缺读任职时间留空并标注待原图补录。
- 第十卷正文表格占位符：{before['placeholders']} -> {after['placeholders']}。
- 第十卷结构化表格：{before['structured_tables']} -> {after['structured_tables']}。
- 已写入进度文档：`output/reports/progress/20260629_第十卷水利_表格专项阶段一_防汛抗旱机构.md`。

下一步：继续第十卷表10-23报汛站网基本情况表和表10-21农田基本建设工程效益表。
"""
    memory = MEMORY_PATH.read_text(encoding="utf-8") if MEMORY_PATH.exists() else ""
    marker = "## 2026-06-29 第十卷水利表格专项阶段一完成"
    if marker in memory:
        start = memory.find(marker)
        next_entry = memory.find("\n## ", start + len(marker))
        if next_entry == -1:
            memory = memory[:start].rstrip() + "\n" + entry.lstrip()
        else:
            memory = memory[:start].rstrip() + "\n" + entry.rstrip() + "\n" + memory[next_entry:].lstrip()
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
