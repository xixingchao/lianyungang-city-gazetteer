# -*- coding: utf-8 -*-
"""Repair placeholders in 第十五卷 纺织工业."""

from __future__ import annotations

import html
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
PROGRESS_PATH = ROOT / "output" / "reports" / "progress" / "20260629_第十五卷纺织工业_表格专项阶段一.md"
MEMORY_PATH = ROOT / "PROJECT_MEMORY.md"
SECTION_RE = re.compile(r'(<h2 id="第十五卷-纺织工业">第十五卷纺织工业</h2>)(.*?)(?=<h2 id="第十六卷-皮塑工业">)', re.S)
PLACEHOLDER = '<p class="table-placeholder">【表格页-待结构化录入】</p>'


def make_table(caption: str, rows: list[list[str]], note: str) -> str:
    cols = ["项目", "源 OCR 可读序列", "备注"]
    ths = ''.join(f"<th>{html.escape(c)}</th>" for c in cols)
    trs = ['<tr>' + ''.join(f"<td>{html.escape(v)}</td>" for v in row) + '</tr>' for row in rows]
    return f'<table class="structured-table"><caption>{html.escape(caption)}</caption><thead><tr>{ths}</tr></thead><tbody>{"".join(trs)}</tbody></table>\n<p>{html.escape(note)}</p>'


def table_15_4() -> str:
    return make_table(
        "表15-4 1970～1990年部分年份连云港市针织、复制业主要产品产量统计表",
        [["指标序列", "份0.02；0.37", "针织、复制业多产品宽表，现存 OCR 仅保留开头可读序列，待原图补录"]],
        "注：源 OCR 表头可读但正文残缺，本轮保留可读序列，待对照原图补录。",
    )


def table_15_5() -> str:
    return make_table(
        "表15-5 1959～1990年部分年份连云港市麻纺织业生产经营情况统计表",
        [["指标序列", "20.40；66.95；7.29；57.84；136.87；39.60；2.99；15.61；3.90；185.91；334.64；85.10；212.00；381.40；82.34；220.79；397.83；49.88；565.44；945.99；150.10；11439686.00；1002.78；167.58；11395746.50；1290.00；213.00；11311550.00；1155.15；192.04；860.00；1627.30；263.30；1036.10；2196.20；327.57；115411048.80；119.94；219.84；184.12；11595945.60；226.76；610.97；2174.00；110.00；11860888.80；393.89；461.56；2332.13；186.05；10519900.10；412.27；297.15；2382.66；304.00；10552754.00；382.01；266.14；2237.17；103.23；646.00；371.31；44.54；2290.34；-180.29；894.00；263.04；8.56；2973.00；-312.64；10330", "年份、产量、产值、利润、全员劳动生产率等列位待校正"]],
        "注：源 OCR 为多列宽表串行，本轮保留可读序列，待原图校正。",
    )


def table_15_6() -> str:
    return make_table(
        "表15-6 1981～1990年连云港市毛纺丝织业主要产品产量统计表",
        [["指标序列", "0.07；0.59；2.57；2.58；3.35；0.10；7.42；1.69；16.80；127.54；8.03；1.77；13.20；260.16；7.39；1.61；5.95；93.54；9.11；0.79；5.00；110.60；8.19；0.13；0.34", "毛线、毛毯、呢绒、丝织品等列位待校正"]],
        "注：源 OCR 为宽表串行，本轮保留可读序列，待原图补录。",
    )


def table_15_7() -> str:
    return make_table(
        "表15-7 1980～1990年部分年份连云港市服装鞋帽骨干企业生产经营情况表",
        [["指标序列", "6.90；0.64", "表头可读，正文 OCR 残缺，列位待原图补录"]],
        "注：源 OCR 残缺，本轮先承接可读序列，未臆造数据。",
    )


def table_15_8() -> str:
    return make_table(
        "表15-8 1980～1990年部分年份连云港市服装鞋帽重点企业生产经营情况表",
        [["指标序列", "利-11；-14；-3；利0.3；润0.2；-24；-26；-20", "重点企业多项目宽表，列位待校正"]],
        "注：源 OCR 多列表格串行错位，本轮保留可读序列，待原图校正。",
    )


def table_15_9() -> str:
    return make_table(
        "表15-9 1975～1990年连云港市纺织企业工业总产值统计表",
        [["指标序列", "111991654713970165621393818549159692684623792280362449139664350123683830988425193657347203406244937241465", "企业数、工业产值及系统内外分类列位待校正；后续企业基本情况表已保留原结构化表"]],
        "注：源 OCR 为宽表串行，本轮保留可读序列，待对照原图补录。",
    )


def audit(section: str) -> dict[str, int]:
    return {"placeholders": section.count('class="table-placeholder"'), "structured_tables": section.count('<table class="structured-table"')}


def replace_nearby_placeholder(section: str, marker: str, replacement: str, window: int = 3000) -> tuple[str, bool]:
    start = section.find(marker)
    if start == -1:
        return section, False
    placeholder_start = section.find(PLACEHOLDER, start, start + window)
    if placeholder_start == -1:
        return section, False
    placeholder_end = placeholder_start + len(PLACEHOLDER)
    return section[:placeholder_start] + replacement + section[placeholder_end:], True


def repair_html() -> tuple[list[str], dict[str, int], dict[str, int]]:
    html_text = HTML_PATH.read_text(encoding="utf-8")
    match = SECTION_RE.search(html_text)
    if not match:
        raise RuntimeError("Cannot locate 第十五卷 section")
    heading, section = match.groups()
    before = audit(section)
    actions: list[str] = []

    false_page = '填补全市该类产品的空白。</p>\n' + PLACEHOLDER + '\n<p>当年，海州针织厂更名为连云港市针织二厂。'
    if false_page in section:
        section = section.replace(false_page, '填补全市该类产品的空白。当年，海州针织厂更名为连云港市针织二厂。', 1)
        actions.append("清理毛纺织正文分页误占位。")

    table_patterns = [
        ("表15-4", "1970～1990年部分年份连云港市针织、复制业主要产品产量统计表表15-4", table_15_4()),
        ("表15-5", "1959～1990年部分年份连云港市麻纺织业生产经营情况统计表表15-5", table_15_5()),
        ("表15-6", "1981～1990年连云港市毛纺丝织业主要产品产量统计表表15-6", table_15_6()),
        ("表15-7", "1980～1990年部分年份连云港市服装鞋帽骨干企业生产经营情况表表15-7", table_15_7()),
        ("表15-8", "1980～1990年部分年份连云港市服装鞋帽重点企业生产经营情况表表15-8", table_15_8()),
        ("表15-9", "1975～1990年连云港市纺织企业工业总产值统计表表15-9", table_15_9()),
    ]
    for name, marker, table in table_patterns:
        if f'<caption>{name}' not in section:
            section, changed = replace_nearby_placeholder(section, marker, table)
            if changed:
                actions.append(f"结构化{name}为核对型表格。")

    fixed = html_text[: match.start()] + heading + section + html_text[match.end():]
    if fixed != html_text:
        HTML_PATH.write_text(fixed, encoding="utf-8")
    after = audit(SECTION_RE.search(fixed).group(2))  # type: ignore[union-attr]
    return actions, before, after


def write_progress(actions: list[str], before: dict[str, int], after: dict[str, int]) -> None:
    action_lines = '\n'.join(f"- {a}" for a in actions) or "- 本次复跑未产生新改动，脚本保持幂等。"
    content = f"""# 第十五卷纺织工业 表格专项阶段一

更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}

## 已完成
{action_lines}

## 统计变化
| 指标 | 修复前 | 修复后 |
| --- | ---: | ---: |
| 第十五卷正文表格占位符 | {before['placeholders']} | {after['placeholders']} |
| 第十五卷结构化表格 | {before['structured_tables']} | {after['structured_tables']} |

## 验收说明
- 正文分页误占位已合并。
- 残缺宽表均按核对型表格保留源 OCR 可读序列，未臆造列位。
"""
    PROGRESS_PATH.write_text(content, encoding="utf-8")


def update_memory(before: dict[str, int], after: dict[str, int]) -> None:
    entry = f"""
## 2026-06-29 第十五卷纺织工业表格专项阶段一完成

- 新增脚本：`scripts/repair_fifteenth_volume_textile_tables.py`。
- 清理第十五卷毛纺织正文分页误占位。
- 结构化表15-4、表15-5、表15-6、表15-7、表15-8、表15-9为核对型表格。
- 第十五卷正文表格占位符：{before['placeholders']} -> {after['placeholders']}。
- 已写入进度文档：`output/reports/progress/20260629_第十五卷纺织工业_表格专项阶段一.md`。
"""
    memory = MEMORY_PATH.read_text(encoding="utf-8") if MEMORY_PATH.exists() else ""
    marker = "## 2026-06-29 第十五卷纺织工业表格专项阶段一完成"
    if marker not in memory:
        MEMORY_PATH.write_text(memory.rstrip() + "\n\n" + entry.lstrip(), encoding="utf-8")


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
