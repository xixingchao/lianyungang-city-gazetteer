# -*- coding: utf-8 -*-
"""Repair farmland construction tables in 第十卷 水利."""

from __future__ import annotations

import html
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
PROGRESS_PATH = ROOT / "output" / "reports" / "progress" / "20260629_第十卷水利_表格专项阶段三_农田基本建设.md"
MEMORY_PATH = ROOT / "PROJECT_MEMORY.md"

SECTION_RE = re.compile(r'(<h2 id="第十卷-水利">第十卷水利</h2>)(.*?)(?=<h2 id="第十一卷-畜牧业">)', re.S)
PLACEHOLDER = '<p class="table-placeholder">【表格页-待结构化录入】</p>'


def make_table(caption: str, columns: list[str], rows: list[list[str]], note: str) -> str:
    ths = ''.join(f"<th>{html.escape(col)}</th>" for col in columns)
    trs = []
    for row in rows:
        tds = ''.join(f"<td>{html.escape(cell)}</td>" for cell in row)
        trs.append(f"<tr>{tds}</tr>")
    return f'<table class="structured-table"><caption>{html.escape(caption)}</caption><thead><tr>{ths}</tr></thead><tbody>{"".join(trs)}</tbody></table>\n<p>{html.escape(note)}</p>'


def table_10_20_html() -> str:
    rows = [
        ["1983", "165.5", "111/9982", "4007", "13729", "171.1", "113/10732", "7554", "14838", "176.9"],
        ["1984", "120/12962", "3274", "10619", "185.9", "121/14462", "3918", "10711", "188.2"],
        ["1985", "122/1465", "26756", "11549", "190.3", "125/1690", "30123", "13547", "192.5"],
        ["1986", "127/1712", "29170", "13263", "190.0", "129/1757", "29680", "14314", ""],
    ]
    return make_table(
        "表10-20 1983～1990年连云港市平原、圩区农田基本建设情况表",
        ["序列年份", "源OCR字段1", "源OCR字段2", "源OCR字段3", "源OCR字段4", "源OCR字段5", "源OCR字段6", "源OCR字段7", "源OCR字段8", "源OCR字段9"],
        rows,
        "注：源 OCR 表头和年度字段串行错位，本轮先保留可读数值序列，六条标准分项列位待对照原图补录。",
    )


def table_10_21_html() -> str:
    rows = [
        ["1983", "21052", "2.5", "22.8", "0.8", "50.3", "", "", "", ""],
        ["1984", "20629", "13066", "8.9", "30.6", "2.6", "62.1", "", "", ""],
        ["1985", "18017", "16.9", "31.8", "2.6", "40.1", "", "", "", ""],
        ["1986", "20643", "2.8", "32.8", "0.5", "32.4", "", "", "", ""],
        ["1987", "28592", "10.0", "35.9", "5.2", "36.6", "", "", "", ""],
        ["1988", "30679", "12550", "10.3", "41.6", "7.3", "43.5", "", "", ""],
        ["1989", "33913", "27038", "8.5", "34.2", "1.3", "37.2", "", "", ""],
        ["1990", "", "", "4.7", "34.1", "0.2", "20.8", "", "", ""],
    ]
    return make_table(
        "表10-21 1983～1990年连云港市农田基本建设工程效益表",
        ["年份", "建设总投工/源OCR", "土方/源OCR", "木材/源OCR", "水泥/源OCR", "钢材/源OCR", "工程效益/源OCR", "灌溉新增", "灌溉改善", "除涝新增/改善"],
        rows,
        "注：源 OCR 将三大材、完成工程量和工程效益列串行打散；本轮按年份保留可读序列，具体列位待对照原图补录。",
    )


def audit(section: str) -> dict[str, int]:
    return {
        "placeholders": section.count('class="table-placeholder"'),
        "structured_tables": section.count('<table class="structured-table"'),
        "table_10_20": section.count('表10-20 1983～1990年连云港市平原、圩区农田基本建设情况表'),
        "table_10_21": section.count('表10-21 1983～1990年连云港市农田基本建设工程效益表'),
        "raw_10_21": section.count('1983～1990年连云港市农田基本建设工程效益表表 10-21'),
    }


def repair_html() -> tuple[list[str], dict[str, int], dict[str, int]]:
    html_text = HTML_PATH.read_text(encoding="utf-8")
    match = SECTION_RE.search(html_text)
    if not match:
        raise RuntimeError("Cannot locate 第十卷 水利 section")
    heading, section = match.groups()
    before = audit(section)
    actions: list[str] = []

    if '<caption>表10-20 1983～1990年连云港市平原、圩区农田基本建设情况表</caption>' not in section:
        pattern20 = re.compile(
            r'<p>1983～1990年连云港市平原、圩区农田基本建设情况表表10-20农田基本建设六条标准分项达到面积（万亩）</p>\n'
            r'<p>旱涝保收年圩堤排涝抗旱防渍配套平整深翻高产稳产田累计数累计建筑物（座）</p>\n'
            r'<p>累计累计达标标准大于大于30 至大于0\.5至至达到平整份深翻（万亩）</p>\n'
            r'<p>面积小沟级中沟级面积面积（万亩/公里）</p>\n'
            r'<p>毫米100天100天1\.0米1\.0米毫米（万亩）</p>\n'
            r'<p>以上（万亩）</p>\n'
            r'<p>（万亩）</p>\n'
            r'<p>165\.5111/9982400713729171\.1113/10732755414838176\.9120/12962327410619185\.9121/14462391810711188\.2122/14652675611549190\.3125/16903012313547192\.5127/17122917013263190\.0129/17572968014314</p>\n'
            + re.escape(PLACEHOLDER),
            re.S,
        )
        section, count = pattern20.subn(table_10_20_html(), section, count=1)
        if count:
            actions.append("结构化表10-20为核对型表格，清理一处农田基本建设表占位。")

    if '<caption>表10-21 1983～1990年连云港市农田基本建设工程效益表</caption>' not in section:
        pattern21 = re.compile(
            r'<p>1983～1990年连云港市农田基本建设工程效益表表 10-21实用三大材完成工程量工程效益（万亩）</p>\n'
            r'<p>农田基本木材水泥钢材水利石方混凝土灌溉除涝建设年份建设总投工土方（万立（万立新增改善新增改善（万工日）</p>\n'
            r'<p>（立方米）</p>\n<p>（吨）</p>\n<p>（吨）</p>\n<p>方米）</p>\n<p>方米）</p>\n<p>（立方米）</p>\n'
            r'<p>210522\.522\.80\.850\.320629130668\.930\.62\.662\.11801716\.931\.82\.640\.1206432\.832\.80\.532\.42859210\.035\.95\.236\.6306791255010\.341\.67\.343\.533913270388\.534\.21\.337\.24\.734\.10\.220\.8</p>',
            re.S,
        )
        section, count = pattern21.subn(table_10_21_html(), section, count=1)
        if count:
            actions.append("结构化表10-21为核对型表格，清理串行 OCR 残留。")

    fixed = html_text[: match.start()] + heading + section + html_text[match.end() :]
    if fixed != html_text:
        HTML_PATH.write_text(fixed, encoding="utf-8")
    after = audit(SECTION_RE.search(fixed).group(2))  # type: ignore[union-attr]
    return actions, before, after


def write_progress(actions: list[str], before: dict[str, int], after: dict[str, int]) -> None:
    action_lines = "\n".join(f"- {a}" for a in actions) or "- 本次复跑未产生新改动，脚本保持幂等。"
    content = f"""# 第十卷水利 表格专项阶段三：农田基本建设表

更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}

## 本轮范围
- 章节：第十卷 水利，第五章农田水利建设。
- 目标：处理表10-20、表10-21农田基本建设相关表格。

## 已完成
{action_lines}

## 统计变化
| 指标 | 修复前 | 修复后 |
| --- | ---: | ---: |
| 第十卷正文表格占位符 | {before['placeholders']} | {after['placeholders']} |
| 第十卷结构化表格 | {before['structured_tables']} | {after['structured_tables']} |
| 表10-20出现次数 | {before['table_10_20']} | {after['table_10_20']} |
| 表10-21出现次数 | {before['table_10_21']} | {after['table_10_21']} |
| 表10-21串行OCR残留 | {before['raw_10_21']} | {after['raw_10_21']} |

## 当场验收
- 表10-20、表10-21均以核对型结构化表保留源 OCR 可读序列。
- 因源 OCR 宽表列位严重错位，未臆造具体列名归属。
- 本脚本可重复运行；再次运行不会重复插入表格。

## 下一步计划
- 继续第十卷前段表10-3、表10-10等工程宽表。
"""
    PROGRESS_PATH.write_text(content, encoding="utf-8")


def update_memory(before: dict[str, int], after: dict[str, int]) -> None:
    entry = f"""
## 2026-06-29 第十卷水利表格专项阶段三完成

已完成第十卷农田基本建设表专项第三阶段：

- 新增脚本：`scripts/repair_tenth_volume_farmland_construction_tables.py`。
- 结构化表10-20、表10-21为核对型表格，保留源 OCR 可读序列。
- 第十卷正文表格占位符：{before['placeholders']} -> {after['placeholders']}。
- 第十卷结构化表格：{before['structured_tables']} -> {after['structured_tables']}。
- 已写入进度文档：`output/reports/progress/20260629_第十卷水利_表格专项阶段三_农田基本建设.md`。

下一步：继续第十卷前段表10-3、表10-10等工程宽表。
"""
    memory = MEMORY_PATH.read_text(encoding="utf-8") if MEMORY_PATH.exists() else ""
    marker = "## 2026-06-29 第十卷水利表格专项阶段三完成"
    if marker in memory:
        start = memory.find(marker)
        next_entry = memory.find("\n## ", start + len(marker))
        memory = memory[:start].rstrip() + "\n" + entry.rstrip() + ("\n" + memory[next_entry:].lstrip() if next_entry != -1 else "")
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
