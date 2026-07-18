# -*- coding: utf-8 -*-
"""Repair verified ground temperature tables in 第一卷 自然环境."""

from __future__ import annotations

import html
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
PROGRESS_PATH = ROOT / "output" / "reports" / "progress" / "20260629_第一卷自然环境_表格专项阶段三_地温.md"
MEMORY_PATH = ROOT / "PROJECT_MEMORY.md"

SECTION_RE = re.compile(
    r'(<h2 id="第一卷-自然环境">第一卷自然环境</h2>)(.*?)(?=<h2 id="第二卷-建置区划">)',
    re.S,
)
PLACEHOLDER = '<p class="table-placeholder">【表格页-待结构化录入】</p>'


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


def ground_temperature_tables() -> str:
    months = [f"{i}月" for i in range(1, 13)]
    table_1_14 = table_html(
        "表1-14 连云港市各月平均温差表",
        ["项目", *months],
        [["温差(℃)", "0.5", "1.4", "2.5", "3.4", "4.6", "4.6", "3.1", "3.3", "2.7", "1.7", "0.2", "-0.1"]],
        "注：资料年份1951～1990年。",
    )
    table_1_15 = table_html(
        "表1-15 连云港市各月平均最高、最低地面温度表",
        ["项目", *months],
        [
            ["平均最高(℃)", "13.4", "17.3", "26.2", "34.1", "42.4", "45.8", "44.1", "44.9", "39.2", "32.5", "22.1", "14.8"],
            ["平均最低(℃)", "-6.8", "-4.9", "-0.2", "6.5", "12.3", "18.1", "22.9", "22.4", "16.3", "8.7", "1.3", "-5.1"],
        ],
        "注：资料年份1951～1990年。",
    )
    table_1_16 = table_html(
        "表1-16 连云港市5、10、15、20、40、80、160、320厘米各月平均地面温度表",
        ["项目", *months],
        [
            ["5厘米(℃)", "1.1", "3.1", "8.2", "14.9", "21.4", "26.0", "28.2", "28.7", "23.6", "17.3", "9.6", "3.1"],
            ["10厘米(℃)", "1.7", "3.3", "8.1", "14.4", "20.4", "25.2", "27.6", "28.3", "23.7", "17.7", "10.4", "3.9"],
            ["15厘米(℃)", "2.4", "3.6", "7.8", "14.2", "20.1", "24.6", "27.2", "28.0", "23.8", "18.1", "11.1", "4.7"],
            ["20厘米(℃)", "2.7", "3.8", "8.0", "14.0", "19.6", "24.1", "26.7", "27.7", "23.9", "18.4", "11.7", "5.2"],
            ["40厘米(℃)", "4.6", "4.7", "7.9", "13.1", "18.2", "22.2", "25.1", "26.2", "23.7", "19.1", "13.4", "7.3"],
            ["80厘米(℃)", "7.4", "6.4", "8.1", "11.7", "15.9", "19.6", "22.6", "24.4", "23.3", "20.1", "15.7", "10.6"],
            ["160厘米(℃)", "11.6", "9.8", "9.6", "11.0", "13.5", "16.3", "18.9", "21.0", "21.5", "20.4", "18.0", "14.7"],
            ["320厘米(℃)", "16.1", "14.8", "13.7", "13.1", "13.2", "13.9", "15.0", "16.2", "17.3", "17.9", "17.9", "17.3"],
        ],
        "注：资料年份1951～1990年。",
    )
    return "\n".join([table_1_14, table_1_15, table_1_16])


def audit_section(section: str) -> dict[str, int]:
    return {
        "placeholders": section.count('class="table-placeholder"'),
        "structured_tables": section.count('<table class="structured-table"'),
        "table_1_14": section.count('<caption>表1-14 连云港市各月平均温差表</caption>'),
        "table_1_15": section.count('<caption>表1-15 连云港市各月平均最高、最低地面温度表</caption>'),
        "table_1_16": section.count('<caption>表1-16 连云港市5、10、15、20、40、80、160、320厘米各月平均地面温度表</caption>'),
        "raw_1_16_tail": section.count('续上表月份项目40厘米4.64.77.913.118.222.225.126.223.719.113.47.3'),
    }


def repair_html() -> tuple[list[str], dict[str, int], dict[str, int]]:
    html_text = HTML_PATH.read_text(encoding="utf-8")
    match = SECTION_RE.search(html_text)
    if not match:
        raise RuntimeError("Cannot locate 第一卷 自然环境 section")

    heading, section = match.groups()
    before = audit_section(section)
    actions: list[str] = []

    replacement = ground_temperature_tables()
    pattern = re.compile(
        r'<p>连云港市各月平均温差表</p>\n'
        + re.escape(PLACEHOLDER)
        + r'\n'
        + re.escape(PLACEHOLDER)
        + r'\n<p>续上表月份项目40厘米4\.64\.77\.913\.118\.222\.225\.126\.223\.719\.113\.47\.3'
        r'80厘米7\.46\.48\.111\.715\.919\.622\.624\.423\.320\.115\.710\.6'
        r'160厘米11\.69\.89\.611\.013\.516\.318\.921\.021\.520\.418\.014\.7'
        r'320厘米16\.114\.813\.713\.113\.213\.915\.016\.217\.317\.917\.917\.3注：资料年份1951～1990年。</p>',
        re.S,
    )
    section, count = pattern.subn(replacement, section, count=1)
    if count:
        actions.append("结构化表1-14、表1-15、表1-16地温相关三表，替换两个连续占位符和表1-16续表串行 OCR 残留。")

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
    content = f"""# 第一卷自然环境 表格专项阶段三：地温表

更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}

## 本轮范围
- 章节：第一卷 自然环境，第四章气候，第三节地温和冻土。
- 目标：结构化 OCR 数值完整的地温相关表格，清除连续占位和续表串行文本。
- 输入：`workbench/body_chapters/paddle_上/第一卷_自然环境.md` 中表1-14、表1-15、表1-16。

## 已完成
{action_lines}

## 统计变化
| 指标 | 修复前 | 修复后 |
| --- | ---: | ---: |
| 第一卷正文表格占位符 | {before['placeholders']} | {after['placeholders']} |
| 第一卷结构化表格 | {before['structured_tables']} | {after['structured_tables']} |
| 表1-14结构化表 | {before['table_1_14']} | {after['table_1_14']} |
| 表1-15结构化表 | {before['table_1_15']} | {after['table_1_15']} |
| 表1-16结构化表 | {before['table_1_16']} | {after['table_1_16']} |
| 表1-16续表OCR残留 | {before['raw_1_16_tail']} | {after['raw_1_16_tail']} |

## 当场验收
- 表1-14、表1-15、表1-16数值均取自源 MD 对应表格段落。
- 两个连续正文占位符已替换为结构化表；表1-16跨页续表串行 OCR 残留已清除。
- 本脚本可重复运行；再次运行不会重复插入表格。

## 遇到的问题
- 表1-14/15 的最终阅读器原始串行数据已被前文段落吞并，无法仅从 HTML 中完整还原；本轮以源 MD 为准重建。
- 同章剩余表1-7气温、表1-10风速、表1-11湿度等仍存在缺行或交错 OCR，需要继续核图或逐段拆分。

## 下一步计划
- 继续第一卷气候章节剩余表格，优先处理可完整核验的表；无法确认的表进入 PDF 原图核验清单。
- 第一卷气候收尾后转入第五章水系水文跨页宽表专项。
"""
    PROGRESS_PATH.write_text(content, encoding="utf-8")


def update_memory(before: dict[str, int], after: dict[str, int]) -> None:
    entry = f"""
## 2026-06-29 第一卷自然环境表格专项阶段三完成

已完成第一卷地温表格专项第三阶段：

- 新增脚本：`scripts/repair_first_volume_ground_temperature_tables.py`。
- 结构化表1-14《连云港市各月平均温差表》、表1-15《连云港市各月平均最高、最低地面温度表》、表1-16《连云港市5、10、15、20、40、80、160、320厘米各月平均地面温度表》。
- 清除两个连续正文表格占位符和表1-16续表串行 OCR 残留。
- 第一卷正文表格占位符：{before['placeholders']} -> {after['placeholders']}。
- 第一卷结构化表格：{before['structured_tables']} -> {after['structured_tables']}。
- 已写入进度文档：`output/reports/progress/20260629_第一卷自然环境_表格专项阶段三_地温.md`。

下一步：继续第一卷气候章节剩余表格，随后转入水系水文跨页宽表。
"""
    memory = MEMORY_PATH.read_text(encoding="utf-8") if MEMORY_PATH.exists() else ""
    marker = "## 2026-06-29 第一卷自然环境表格专项阶段三完成"
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
