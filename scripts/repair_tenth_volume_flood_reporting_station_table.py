# -*- coding: utf-8 -*-
"""Repair flood reporting station table in 第十卷 水利."""

from __future__ import annotations

import html
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
PROGRESS_PATH = ROOT / "output" / "reports" / "progress" / "20260629_第十卷水利_表格专项阶段二_报汛站网.md"
MEMORY_PATH = ROOT / "PROJECT_MEMORY.md"

SECTION_RE = re.compile(
    r'(<h2 id="第十卷-水利">第十卷水利</h2>)(.*?)(?=<h2 id="第十一卷-畜牧业">)',
    re.S,
)
PLACEHOLDER = '<p class="table-placeholder">【表格页-待结构化录入】</p>'
TITLE = "1990年连云港市报汛站网基本情况表"

STATION_ROWS = [
    ("石梁河水库", 9), ("小塔山水库", 9), ("安峰山水库", 8), ("八条路水库", 7), ("西双湖水库", 7),
    ("贺庄水库", 7), ("横沟水库", 7), ("昌梨水库", 7), ("房山水库", 7), ("大石埠水库", 7), ("羽山水库", 7),
    ("大村水库", 3), ("灌云", 4), ("燕尾港", 4), ("青口", 3), ("岳庄", 4), ("临洪闸", 5), ("善后闸", 6),
    ("太平庄闸", 5), ("黑林", 5), ("临洪西站", 6), ("大兴镇", 5), ("临洪", 5), ("小许庄", 5),
    ("汪子头", 5), ("蔷北地涵", 5), ("沭新退水闸", 5), ("房山翻水站", 4), ("芝麻翻水站", 2),
    ("石梁河翻水站", 2), ("盐河北套闸", 2), ("古城翻水站", 3), ("龙门翻水站", 3), ("夹谷山", 2),
    ("东风", 2), ("阴平", 2), ("石门", 2), ("石桥", 2), ("朱汪", 2), ("洙边", 2), ("石家崖", 2), ("蛟龙", 2),
    ("临沭", 2), ("叮当河涵洞", 4), ("板浦", 2), ("杨集", 2), ("张湾", 2), ("包庄", 2), ("华沂★", 2),
    ("新安★", 4), ("嶂山闸★", 5), ("沭阳★", 4), ("桐槐树★", 4), ("青峰岭★", 6), ("小仕阳★", 6),
    ("莒县★", 4), ("徒山★", 6), ("石拉渊★", 4), ("石泉湖★", 6), ("大官庄★", 5), ("临沂★", 4),
    ("刘家道口★", 4),
]


def table_html() -> str:
    columns = ["站名", "源 OCR 勾选数", "是否境外站", "备注"]
    rows = []
    for name, count in STATION_ROWS:
        rows.append([name, str(count), "是" if "★" in name else "", "勾选列顺序待原图校正"])
    ths = "".join(f"<th>{html.escape(col)}</th>" for col in columns)
    trs = []
    for row in rows:
        tds = "".join(f"<td>{html.escape(cell)}</td>" for cell in row)
        trs.append(f"<tr>{tds}</tr>")
    table = f'<table class="structured-table"><caption>表10-23 {TITLE}</caption><thead><tr>{ths}</tr></thead><tbody>{"".join(trs)}</tbody></table>'
    table += "\n<p>注：源 OCR 可稳定识别站名和勾选数量，但列位被分页串行打散；本轮先结构化为核对型表，完整拍报项目/收报单位列位待对照原图补录。带“★”者为境外向连云港市拍报水情的站点。</p>"
    return table


def audit_section(section: str) -> dict[str, int]:
    return {
        "placeholders": section.count('class="table-placeholder"'),
        "structured_tables": section.count('<table class="structured-table"'),
        "table_10_23": section.count(f'<caption>表10-23 {TITLE}</caption>'),
        "raw_10_23": section.count(f'{TITLE}表10-23'),
        "broken_water_word": section.count('水位</p>\n<p class="table-placeholder">【表格页-待结构化录入】</p>\n<p>站。1951年春'),
    }


def repair_html() -> tuple[list[str], dict[str, int], dict[str, int]]:
    html_text = HTML_PATH.read_text(encoding="utf-8")
    match = SECTION_RE.search(html_text)
    if not match:
        raise RuntimeError("Cannot locate 第十卷 水利 section")

    heading, section = match.groups()
    before = audit_section(section)
    actions: list[str] = []

    broken = '水位</p>\n<p class="table-placeholder">【表格页-待结构化录入】</p>\n<p>站。1951年春'
    if broken in section:
        section = section.replace(broken, '水位站。1951年春', 1)
        actions.append("清理水情测报正文中由分页造成的误占位，将“水位/站”断句合并为正文。")

    if f'<caption>表10-23 {TITLE}</caption>' not in section:
        pattern = re.compile(
            rf'<p>{re.escape(TITLE)}表10-23.*?羽山水库√√√√√√√</p>\n'
            rf'{re.escape(PLACEHOLDER)}\n{re.escape(PLACEHOLDER)}\n{re.escape(PLACEHOLDER)}\n'
            r'<p>续上表拍报项目收报单位站名闸门雨量水位流量蓄水量沙量中央省市启闭临沭√√叮当河涵洞√√√√板浦√√杨集√√张湾√√包庄√√华沂★√√新安★√√√√嶂山闸★√√√√√沭阳★√√√√桐槐树★√√√√青峰岭★√√√√√√小仕阳★√√√√√√莒县★√√√√徒山★√√√√√√石拉渊★√√√√石泉湖★√√√√√√大官庄★√√√√√临沂★√√√√刘家道口★√√√√注：带“★”者，为境外向连云港市拍报水情的站点。</p>',
            re.S,
        )
        replacement = f"<p>{TITLE}</p>\n{table_html()}"
        section, count = pattern.subn(replacement, section, count=1)
        if count != 1:
            raise RuntimeError("Cannot locate 表10-23 raw block")
        actions.append("结构化表10-23《1990年连云港市报汛站网基本情况表》为核对型表格，清理三处连续表页占位和续表串行 OCR。")

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
    content = f"""# 第十卷水利 表格专项阶段二：报汛站网表

更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}

## 本轮范围
- 章节：第十卷 水利，第七章防汛抗灾。
- 目标：处理表10-23报汛站网基本情况表，清理连续表格页占位；同时清理一处正文分页误占位。
- 输入：`workbench/body_chapters/paddle_上/第十卷至第十六卷（part03）.md` 中表10-23 OCR 段。

## 已完成
{action_lines}

## 统计变化
| 指标 | 修复前 | 修复后 |
| --- | ---: | ---: |
| 第十卷正文表格占位符 | {before['placeholders']} | {after['placeholders']} |
| 第十卷结构化表格 | {before['structured_tables']} | {after['structured_tables']} |
| 表10-23结构化表 | {before['table_10_23']} | {after['table_10_23']} |
| 表10-23串行OCR残留 | {before['raw_10_23']} | {after['raw_10_23']} |
| 正文误占位残留 | {before['broken_water_word']} | {after['broken_water_word']} |

## 当场验收
- 表10-23站名和勾选数量来自源 OCR；共整理 {len(STATION_ROWS)} 个站点。
- 因源 OCR 将“闸门、雨量、水位、流量、蓄水量、沙量、中央、省、市、启闭”列位串行打散，本轮未臆造具体列位。
- 带“★”者保留为境外站标记。
- `水位/站` 被分页占位切断的问题已合并为正文“水位站”。
- 本脚本可重复运行；再次运行不会重复插入表格。

## 下一步计划
- 继续第十卷表10-21农田基本建设工程效益表。
- 再回到前段表10-3、表10-10等水利工程宽表。
"""
    PROGRESS_PATH.write_text(content, encoding="utf-8")


def update_memory(before: dict[str, int], after: dict[str, int]) -> None:
    entry = f"""
## 2026-06-29 第十卷水利表格专项阶段二完成

已完成第十卷报汛站网表专项第二阶段：

- 新增脚本：`scripts/repair_tenth_volume_flood_reporting_station_table.py`。
- 结构化表10-23《1990年连云港市报汛站网基本情况表》为核对型表格，保留站名、源 OCR 勾选数和境外站标记。
- 清理水情测报正文中一处由分页造成的误占位。
- 第十卷正文表格占位符：{before['placeholders']} -> {after['placeholders']}。
- 第十卷结构化表格：{before['structured_tables']} -> {after['structured_tables']}。
- 已写入进度文档：`output/reports/progress/20260629_第十卷水利_表格专项阶段二_报汛站网.md`。

下一步：继续第十卷表10-21农田基本建设工程效益表，再回到表10-3、表10-10等工程宽表。
"""
    memory = MEMORY_PATH.read_text(encoding="utf-8") if MEMORY_PATH.exists() else ""
    marker = "## 2026-06-29 第十卷水利表格专项阶段二完成"
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
