# -*- coding: utf-8 -*-
"""Repair Shilianghe reservoir water level table in 第一卷 自然环境."""

from __future__ import annotations

import html
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
PROGRESS_PATH = ROOT / "output" / "reports" / "progress" / "20260629_第一卷自然环境_表格专项阶段七_石梁河水库.md"
MEMORY_PATH = ROOT / "PROJECT_MEMORY.md"

SECTION_RE = re.compile(
    r'(<h2 id="第一卷-自然环境">第一卷自然环境</h2>)(.*?)(?=<h2 id="第二卷-建置区划">)',
    re.S,
)
PLACEHOLDER = '<p class="table-placeholder">【表格页-待结构化录入】</p>'


def table_html() -> str:
    columns = ["年份", "最高水位(米)", "相应蓄水量(万立方米)", "最高发生日期(月·日)", "最低水位(米)", "相应蓄水量(万立方米)", "最低发生日期(月·日)"]
    values = [
        ["21.03", "12200", "7.7", "18.06", "", "4.23"],
        ["21.93", "15400", "7.15", "15.92", "", "5.31"],
        ["22.07", "15920", "7.21", "19.00", "", "1.1"],
        ["21.85", "15060", "10.6", "19.86", "", "8.15"],
        ["22.26", "16670", "7.28", "15.24", "", "7.9"],
        ["22.54", "17860", "7.26", "15.42", "", "10.27"],
        ["22.10", "16100", "9.9", "15.34", "", "6.18"],
        ["22.22", "16510", "8.24", "17.30", "", "7.7"],
        ["22.71", "18680", "9.29", "17.53", "", "7.20"],
        ["24.70", "30510", "10.27", "18.83", "", "6.28"],
        ["25.42", "35970", "8.29", "22.38", "17150", "6.3"],
        ["25.14", "33800", "8.27", "20.94", "11700", "7.2"],
        ["24.83", "31400", "7.31", "19.30", "", "7.2"],
        ["26.82", "43000", "8.15", "16.49", "", "7.8"],
        ["25.67", "34400", "5.2", "20.54", "", "7.9"],
        ["25.19", "31000", "1.1", "19.17", "", "7.11"],
        ["22.17", "14400", "2.21", "15.95", "", "10.24"],
        ["22.83", "17400", "8.24", "15.31", "", "7.1"],
        ["22.10", "14100", "8.5", "19.24", "", "7.2"],
        ["22.25", "14700", "6.19", "19.58", "", "10.5"],
        ["20.90", "", "3.5", "15.36", "", "9.23"],
        ["24.92", "29175", "8.22", "17.23", "", "7.4"],
        ["23.68", "21800", "3.18", "18.07", "", "9.8"],
        ["23.82", "22500", "7.26", "17.83", "", "7.8"],
        ["23.26", "19500", "5.23", "19.94", "", "7.6"],
        ["23.37", "20100", "2.21", "19.33", "", "7.13"],
        ["23.48", "20700", "12.25", "19.06", "", "7.7"],
        ["23.49", "20800", "1.17", "18.35", "", "7.12"],
        ["22.62", "16400", "6.14", "18.31", "", "11.2"],
        ["23.40", "20300", "8.4", "20.20", "", "1.1"],
    ]
    rows = []
    for year, row in zip(range(1961, 1991), values):
        rows.append([str(year), *row])
    ths = ''.join(f"<th>{html.escape(col)}</th>" for col in columns)
    trs = []
    for row in rows:
        tds = ''.join(f"<td>{html.escape(cell)}</td>" for cell in row)
        trs.append(f"<tr>{tds}</tr>")
    table = f'<table class="structured-table"><caption>表1-22 1961～1990年连云港市石梁河水库水位、蓄水量统计表</caption><thead><tr>{ths}</tr></thead><tbody>{"".join(trs)}</tbody></table>'
    table += "\n<p>注：年份按表题1961～1990年顺序补入；源 OCR 多数最低相应蓄水量缺读，空项待对照原图补录。</p>"
    return table


def audit_section(section: str) -> dict[str, int]:
    return {
        "placeholders": section.count('class="table-placeholder"'),
        "structured_tables": section.count('<table class="structured-table"'),
        "table_1_22": section.count('<caption>表1-22 1961～1990年连云港市石梁河水库水位、蓄水量统计表</caption>'),
        "raw_1_22": section.count('1961～1990年连云港市石梁河水库水位、蓄水量统计表表1-22'),
        "table_1_23": section.count('<caption>表1-23 连云港市主要站水面蒸发量特征值表</caption>'),
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
        re.escape(PLACEHOLDER)
        + r'\n<p>1961～1990年连云港市石梁河水库水位、蓄水量统计表表1-22最高（最大）</p>\n'
        r'<p>最低（最小）</p>\n'
        r'<p>年份水位相应蓄水量发生日期水位相应蓄水量发生日期（米）</p>\n'
        r'<p>（万立方米）</p>\n'
        r'<p>（月·日）</p>\n'
        r'<p>（米）</p>\n'
        r'<p>（万立方米）</p>\n'
        r'<p>（月·日）</p>\n'
        r'<p>21\.03122007\.718\.064\.2321\.93154007\.1515\.925\.3122\.07159207\.2119\.001\.121\.851506010\.619\.868\.1522\.26166707\.2815\.247\.922\.54178607\.2615\.4210\.2722\.10161009\.915\.346\.1822\.22165108\.2417\.307\.722\.71186809\.2917\.537\.2024\.703051010\.2718\.836\.2825\.42359708\.2922\.38171506\.325\.14338008\.2720\.94117007\.224\.83314007\.3119\.307\.226\.82430008\.1516\.497\.825\.67344005\.220\.547\.925\.19310001\.119\.177\.1122\.17144002\.2115\.9510\.2422\.83174008\.2415\.317\.122\.10141008\.519\.247\.222\.25147006\.1919\.5810\.520\.903\.515\.369\.2324\.92291758\.2217\.237\.423\.68218003\.1818\.079\.823\.82225007\.2617\.837\.823\.26195005\.2319\.947\.623\.37201002\.2119\.337\.1323\.482070012\.2519\.067\.723\.49208001\.1718\.357\.1222\.62164006\.1418\.3111\.223\.40203008\.420\.201\.1</p>',
        re.S,
    )
    section, count = pattern.subn(table_html(), section, count=1)
    if count:
        actions.append("结构化表1-22《1961～1990年连云港市石梁河水库水位、蓄水量统计表》，替换占位符和串行 OCR 残留；最低蓄水量缺读项留空待核图。")

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
    content = f"""# 第一卷自然环境 表格专项阶段七：石梁河水库水位蓄水量表

更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}

## 本轮范围
- 章节：第一卷 自然环境，第五章水系水文。
- 目标：结构化表1-22石梁河水库水位、蓄水量统计表，清理一处跨页水文占位。
- 输入：`workbench/body_chapters/paddle_上/第一卷_自然环境.md` 中表1-22 OCR 段。

## 已完成
{action_lines}

## 统计变化
| 指标 | 修复前 | 修复后 |
| --- | ---: | ---: |
| 第一卷正文表格占位符 | {before['placeholders']} | {after['placeholders']} |
| 第一卷结构化表格 | {before['structured_tables']} | {after['structured_tables']} |
| 表1-22结构化表 | {before['table_1_22']} | {after['table_1_22']} |
| 表1-22串行OCR残留 | {before['raw_1_22']} | {after['raw_1_22']} |
| 表1-23结构化表 | {before['table_1_23']} | {after['table_1_23']} |

## 当场验收
- 表1-22最高水位、最高相应蓄水量、最高发生日期、最低水位、最低发生日期均来自源 MD 可读 OCR。
- 年份按表题 `1961～1990年` 顺序补入；多数最低相应蓄水量源 OCR 缺读，未臆造，留空并标注待原图补录。
- 保留既有表1-23结构化表，未重复改动。
- 本脚本可重复运行；再次运行不会重复插入表格。

## 遇到的问题
- 源 OCR 未显式读出年份列，需根据表题连续年份补入。
- 源 OCR 对最低相应蓄水量列缺读严重，后续 PDF 原图核验时需重点补齐。

## 下一步计划
- 继续第一卷水文表1-18、表1-19和表1-20灾害年降雨水位表核图。
- 气候表1-7、1-10、1-11仍需回到 PDF 原图补全缺行。
"""
    PROGRESS_PATH.write_text(content, encoding="utf-8")


def update_memory(before: dict[str, int], after: dict[str, int]) -> None:
    entry = f"""
## 2026-06-29 第一卷自然环境表格专项阶段七完成

已完成第一卷石梁河水库水位蓄水量表专项第七阶段：

- 新增脚本：`scripts/repair_first_volume_shilianghe_reservoir_table.py`。
- 结构化表1-22《1961～1990年连云港市石梁河水库水位、蓄水量统计表》，缺读最低蓄水量留空并标注待原图补录。
- 第一卷正文表格占位符：{before['placeholders']} -> {after['placeholders']}。
- 第一卷结构化表格：{before['structured_tables']} -> {after['structured_tables']}。
- 已写入进度文档：`output/reports/progress/20260629_第一卷自然环境_表格专项阶段七_石梁河水库.md`。

下一步：继续第一卷表1-18、表1-19和表1-20灾害年降雨水位表核图。
"""
    memory = MEMORY_PATH.read_text(encoding="utf-8") if MEMORY_PATH.exists() else ""
    marker = "## 2026-06-29 第一卷自然环境表格专项阶段七完成"
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
