# -*- coding: utf-8 -*-
"""Repair flow feature table in 第一卷 自然环境."""

from __future__ import annotations

import html
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
PROGRESS_PATH = ROOT / "output" / "reports" / "progress" / "20260629_第一卷自然环境_表格专项阶段九_主要河流流量.md"
MEMORY_PATH = ROOT / "PROJECT_MEMORY.md"

SECTION_RE = re.compile(
    r'(<h2 id="第一卷-自然环境">第一卷自然环境</h2>)(.*?)(?=<h2 id="第二卷-建置区划">)',
    re.S,
)
TITLE = "连云港市主要河流年、月平均流量特征值表"
NEXT_TITLE = "1961～1990年连云港市临洪站水位统计表"
PLACEHOLDER = '<p class="table-placeholder">【表格页-待结构化录入】</p>'


def table_html() -> str:
    columns = ["河名", "站名", "特征值", "源 OCR 可读序列", "参加平均年份", "核对状态"]
    rows = [
        ["新沂河", "嶂山闸", "平均", "23.9；1.34；0.53；0.019；0.018；0.11；0.65；0.93；7.87；77.59", "1961～1991", "月序待原图校正"],
        ["新沂河", "嶂山闸", "最大", "0.60；0.58；1.97；17.7；18.6；34.7；12.0；423.12", "", "源 OCR 缺列，待原图补齐"],
        ["新沂河", "嶂山闸", "最大年份", "1984；1969；1984；1963；1966；1971；1974；1964；1966；1963；1975；1985；1971", "", "按 OCR 序列暂存"],
        ["新沂河", "嶂山闸", "最小年份", "1967；1962；1962；1962；1981；1961；1961；1961；1961；1962；1967；1967；1961", "", "最小流量值缺读"],
        ["蔷薇河", "临洪站", "平均", "14.97；3.76；10.44；5.03；10.2；25.42；81.45；46.22；32.48；11.04；1.59；0.33；20.24", "1981～1994", "月序待原图校正"],
        ["蔷薇河", "临洪站", "最大", "299；304；312；365；517；619；238；629；156；387；423；293；378.5", "", "源 OCR 小数点疑有缺读"],
        ["蔷薇河", "临洪站", "最大年份", "1990；1661；1989；1991；1990；1989；1994；1991；1988；1991；1994", "", "含 OCR 误读年份，待原图校正"],
        ["蔷薇河", "临洪站", "最小年份", "1988；1988；1988；1981；1981；1981；1981；1981；1988；1988；1988；1981", "", "最小流量值缺读"],
        ["新沭河", "石梁河站", "平均", "-1.62；-0.99；0.07；2.83；4.38；35.98；24.88；44.21；15.23；2.97；1.49；0.54；10.47", "1981～1994", "月序待原图校正"],
        ["新沭河", "石梁河站", "最大", "12.0；56.6；87.6；40.8；32.7；73.6；446.03", "", "源 OCR 缺列，待原图补齐"],
        ["新沭河", "石梁河站", "最大年份", "1991；1991；1991；1990；1994；1981；1986；1988；1988；1994；1986", "", "按 OCR 序列暂存"],
        ["新沭河", "石梁河站", "最小", "-13.5；-14.9；-12.3；-13.0；-10.5；-12.6；-12.1；-5.92；-11.0；-11.6；-15.0；-15.6", "", "按 OCR 序列暂存"],
        ["新沭河", "石梁河站", "最小年份", "1981；1984；1984；1983；1986；1984；1981；1983；1982；1986；1984；1984", "", "按 OCR 序列暂存"],
    ]
    ths = "".join(f"<th>{html.escape(col)}</th>" for col in columns)
    trs = []
    for row in rows:
        tds = "".join(f"<td>{html.escape(cell)}</td>" for cell in row)
        trs.append(f"<tr>{tds}</tr>")
    table = f'<table class="structured-table"><caption>表1-18 {TITLE}</caption><thead><tr>{ths}</tr></thead><tbody>{"".join(trs)}</tbody></table>'
    table += "\n<p>注：单位为立方米/秒。源 OCR 将 1～12 月、全年、年份列串行打散，本表先保留可读数值序列以替代正文占位；月序、缺列和疑似小数点误读项待对照原图补录。</p>"
    return table


def audit_section(section: str) -> dict[str, int]:
    return {
        "placeholders": section.count('class="table-placeholder"'),
        "structured_tables": section.count('<table class="structured-table"'),
        "table_1_18": section.count(f'<caption>表1-18 {TITLE}</caption>'),
        "title_1_18": section.count(f"<p>{TITLE}</p>"),
        "table_1_19": section.count("表1-19 1961～1990年连云港市临洪站水位统计表"),
    }


def repair_html() -> tuple[list[str], dict[str, int], dict[str, int]]:
    html_text = HTML_PATH.read_text(encoding="utf-8")
    match = SECTION_RE.search(html_text)
    if not match:
        raise RuntimeError("Cannot locate 第一卷 自然环境 section")

    heading, section = match.groups()
    before = audit_section(section)
    actions: list[str] = []

    if f'<caption>表1-18 {TITLE}</caption>' not in section:
        pattern = re.compile(rf'<p>{re.escape(TITLE)}</p>\n{re.escape(PLACEHOLDER)}\n(?=<p>{re.escape(NEXT_TITLE)}</p>)', re.S)
        replacement = f"<p>{TITLE}</p>\n{table_html()}\n"
        section, count = pattern.subn(replacement, section, count=1)
        if count != 1:
            raise RuntimeError("Cannot locate 表1-18 placeholder before 表1-19")
        actions.append("结构化表1-18《连云港市主要河流年、月平均流量特征值表》为核对型表格，清理表题后的正文占位符；月序和缺读项标注待原图补录。")

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
    content = f"""# 第一卷自然环境 表格专项阶段九：主要河流流量特征值表

更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}

## 本轮范围
- 章节：第一卷 自然环境，第五章水系水文。
- 目标：处理表1-18主要河流年、月平均流量特征值表，清理水文段一处占位。
- 输入：`workbench/body_chapters/上/第一卷_自然环境.md` 与 `workbench/body_chapters/paddle_上/第一卷_自然环境.md` 中表1-18 OCR 段。

## 已完成
{action_lines}

## 统计变化
| 指标 | 修复前 | 修复后 |
| --- | ---: | ---: |
| 第一卷正文表格占位符 | {before['placeholders']} | {after['placeholders']} |
| 第一卷结构化表格 | {before['structured_tables']} | {after['structured_tables']} |
| 表1-18结构化表 | {before['table_1_18']} | {after['table_1_18']} |
| 表1-18正文表题 | {before['title_1_18']} | {after['title_1_18']} |
| 表1-19结构化表 | {before['table_1_19']} | {after['table_1_19']} |

## 当场验收
- 表1-18可读数据来自源 MD 的普通 OCR 与 PaddleOCR 对照。
- OCR 将月列、全年列、年份列串行打散，未能稳定还原完整二维表；本轮以核对型结构化表保存可读序列，不臆造月序。
- 对缺列、小数点疑误读、年份疑误读项均保留待原图补录说明。
- 本脚本可重复运行；再次运行不会重复插入表格。

## 遇到的问题
- 表1-18为宽表，源 OCR 对表头和月份列顺序破坏严重。
- `蔷薇河-临洪站-最大年份` 中出现 `1661` 等明显 OCR 误读，需 PDF 原图校正。
- 表1-20灾害年降雨、水位表跨多页，仍需独立核图处理。

## 下一步计划
- 第一卷继续处理表1-20灾害年降雨、水位情况表；若无法直接还原，先转换为分站核对型结构化表并保留原图补录提示。
- 复跑表格占位符清单，确认第一卷剩余占位数。
"""
    PROGRESS_PATH.write_text(content, encoding="utf-8")


def update_memory(before: dict[str, int], after: dict[str, int]) -> None:
    entry = f"""
## 2026-06-29 第一卷自然环境表格专项阶段九完成

已完成第一卷主要河流流量特征值表专项第九阶段：

- 新增脚本：`scripts/repair_first_volume_flow_feature_table.py`。
- 结构化表1-18《连云港市主要河流年、月平均流量特征值表》为核对型表格，保留源 OCR 可读序列。
- 第一卷正文表格占位符：{before['placeholders']} -> {after['placeholders']}。
- 第一卷结构化表格：{before['structured_tables']} -> {after['structured_tables']}。
- 已写入进度文档：`output/reports/progress/20260629_第一卷自然环境_表格专项阶段九_主要河流流量.md`。

下一步：继续第一卷表1-20灾害年降雨、水位情况表；该表跨多页，需独立核图或转换为分站核对型结构化表。
"""
    memory = MEMORY_PATH.read_text(encoding="utf-8") if MEMORY_PATH.exists() else ""
    marker = "## 2026-06-29 第一卷自然环境表格专项阶段九完成"
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
