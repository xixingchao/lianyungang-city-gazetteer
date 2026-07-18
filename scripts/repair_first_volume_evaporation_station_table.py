# -*- coding: utf-8 -*-
"""Repair verified station water-surface evaporation table in 第一卷 自然环境."""

from __future__ import annotations

import html
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
PROGRESS_PATH = ROOT / "output" / "reports" / "progress" / "20260629_第一卷自然环境_表格专项阶段六_水面蒸发.md"
MEMORY_PATH = ROOT / "PROJECT_MEMORY.md"

SECTION_RE = re.compile(
    r'(<h2 id="第一卷-自然环境">第一卷自然环境</h2>)(.*?)(?=<h2 id="第二卷-建置区划">)',
    re.S,
)
PLACEHOLDER = '<p class="table-placeholder">【表格页-待结构化录入】</p>'


def table_html() -> str:
    columns = ["站名", "资料年份", "蒸发器形式", "特征值", "1月", "2月", "3月", "4月", "5月", "6月", "7月", "8月", "9月", "10月", "11月", "12月", "年总量"]
    rows = [
        ["石梁河", "", "E601", "平均", "27.8", "3.9", "71.2", "96.8", "132.3", "132.7", "112.6", "117.5", "99.6", "81.2", "55.2", "34.6", "995.4"],
        ["石梁河", "", "E601", "月分配(%)", "2.8", "3.4", "7.2", "9.7", "13.3", "13.3", "11.3", "11.8", "11.0", "8.2", "5.5", "3.5", ""],
        ["石梁河", "", "E601", "最大", "73.5", "60.5", "106.3", "172.2", "88.2", "201.7", "223.9", "181.9", "152.9", "168.9", "80.2", "99.5", ""],
        ["石梁河", "", "E601", "最小", "15.0", "16.8", "58.4", "84.5", "101.8", "73.6", "76.4", "89.7", "74.7", "58.3", "43.7", "20.0", ""],
        ["青口", "", "E601", "平均", "29.7", "42.3", "78.0", "137.6", "158.3", "169.4", "146.5", "145.9", "119.2", "99.9", "59.2", "35.2", "1221.2"],
        ["青口", "", "E601", "月分配(%)", "2.4", "3.5", "6.4", "11.3", "13.0", "13.8", "12.0", "11.9", "9.8", "8.2", "4.8", "2.9", ""],
        ["东海", "", "E601", "平均", "23.2", "32.5", "62.0", "102.1", "116.7", "121.0", "108.5", "104.6", "90.4", "82.9", "51.3", "30.8", "925.5"],
        ["东海", "", "E601", "月分配(%)", "2.5", "3.5", "6.7", "11.0", "12.6", "13.0", "11.7", "11.3", "9.8", "9.0", "5.8", "3.3", ""],
    ]
    ths = ''.join(f"<th>{html.escape(col)}</th>" for col in columns)
    trs = []
    for row in rows:
        tds = ''.join(f"<td>{html.escape(cell)}</td>" for cell in row)
        trs.append(f"<tr>{tds}</tr>")
    table = f'<table class="structured-table"><caption>表1-23 连云港市主要站水面蒸发量特征值表</caption><thead><tr>{ths}</tr></thead><tbody>{"".join(trs)}</tbody></table>'
    table += "\n<p>注：单位为毫米；资料年份及最大、最小发生年份在源 OCR 中缺读，待对照原图补录。</p>"
    return table


def audit_section(section: str) -> dict[str, int]:
    return {
        "placeholders": section.count('class="table-placeholder"'),
        "structured_tables": section.count('<table class="structured-table"'),
        "table_1_23": section.count('<caption>表1-23 连云港市主要站水面蒸发量特征值表</caption>'),
        "raw_1_23": section.count('连云港市主要站水面蒸发量特征值表表1-23单位：毫米'),
        "table_1_24": section.count('<caption>表1-24 连云港市沿海潮位站最高最低潮位统计表</caption>'),
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
        + r'\n<p>连云港市主要站水面蒸发量特征值表表1-23单位：毫米站资料蒸发器月份年总量名年份形式特征值平均'
        r'27\.83\.971\.296\.8132\.3132\.7112\.6117\.599\.681\.255\.234\.6995\.4月分配（%）</p>\n'
        r'<p>2\.83\.47\.29\.713\.313\.311\.311\.811\.08\.25\.53\.5石最大73\.560\.5106\.3172\.288\.2201\.7223\.9181\.9152\.9168\.980\.299\.5E601梁～年份河最小15\.016\.858\.484\.5101\.873\.676\.489\.774\.758\.343\.720\.0年份平均29\.742\.378\.0137\.6158\.3169\.4146\.5145\.9119\.299\.959\.235\.21221\.2E601青口月分配（%）</p>\n'
        r'<p>2\.43\.56\.411\.313\.013\.812\.011\.99\.88\.24\.82\.9平均23\.232\.562\.0102\.1116\.7121\.0108\.5104\.690\.482\.951\.330\.8925\.5E601东海月分配（%）</p>\n'
        r'<p>2\.53\.56\.711\.012\.613\.011\.711\.39\.89\.05\.83\.3</p>',
        re.S,
    )
    section, count = pattern.subn(table_html(), section, count=1)
    if count:
        actions.append("结构化表1-23《连云港市主要站水面蒸发量特征值表》，替换占位符和串行 OCR 表格文本；缺读年份标注待核图。")

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
    content = f"""# 第一卷自然环境 表格专项阶段六：水面蒸发量特征值表

更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}

## 本轮范围
- 章节：第一卷 自然环境，第五章水系水文，水文相关表。
- 目标：结构化表1-23主要站水面蒸发量特征值表，清理跨页水文段一处占位。
- 输入：`workbench/body_chapters/paddle_上/第一卷_自然环境.md` 中表1-23 OCR 段。

## 已完成
{action_lines}

## 统计变化
| 指标 | 修复前 | 修复后 |
| --- | ---: | ---: |
| 第一卷正文表格占位符 | {before['placeholders']} | {after['placeholders']} |
| 第一卷结构化表格 | {before['structured_tables']} | {after['structured_tables']} |
| 表1-23结构化表 | {before['table_1_23']} | {after['table_1_23']} |
| 表1-23串行OCR残留 | {before['raw_1_23']} | {after['raw_1_23']} |
| 表1-24结构化表 | {before['table_1_24']} | {after['table_1_24']} |

## 当场验收
- 表1-23的月均值、月分配、石梁河最大/最小可读值均来自源 MD。
- 资料年份及最大/最小发生年份缺读，未臆造，已在表下注明待原图补录。
- 保留既有表1-24结构化潮位表，未重复改动。
- 本脚本可重复运行；再次运行不会重复插入表格。

## 遇到的问题
- 表1-23源 OCR 对“站名/资料年份/蒸发器形式”有明显穿插，当前仅保留可确认站名和 E601 形式。
- 表1-18、表1-19、表1-22仍有年份或多列缺读，需要继续核图。

## 下一步计划
- 继续第一卷水系水文：优先建立表1-18、1-19、1-22缺读核图清单，能分批结构化的再处理。
- 气候表1-7、1-10、1-11也需回到 PDF 原图核验后再补齐。
"""
    PROGRESS_PATH.write_text(content, encoding="utf-8")


def update_memory(before: dict[str, int], after: dict[str, int]) -> None:
    entry = f"""
## 2026-06-29 第一卷自然环境表格专项阶段六完成

已完成第一卷水面蒸发量特征值表专项第六阶段：

- 新增脚本：`scripts/repair_first_volume_evaporation_station_table.py`。
- 结构化表1-23《连云港市主要站水面蒸发量特征值表》，缺读年份标注待原图补录。
- 第一卷正文表格占位符：{before['placeholders']} -> {after['placeholders']}。
- 第一卷结构化表格：{before['structured_tables']} -> {after['structured_tables']}。
- 已写入进度文档：`output/reports/progress/20260629_第一卷自然环境_表格专项阶段六_水面蒸发.md`。

下一步：继续第一卷水文宽表缺读核图与分批结构化。
"""
    memory = MEMORY_PATH.read_text(encoding="utf-8") if MEMORY_PATH.exists() else ""
    marker = "## 2026-06-29 第一卷自然环境表格专项阶段六完成"
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
