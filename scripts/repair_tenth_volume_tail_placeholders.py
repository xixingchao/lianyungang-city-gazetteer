# -*- coding: utf-8 -*-
"""Repair remaining high-priority placeholders in 第十卷 水利."""

from __future__ import annotations

import html
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
PROGRESS_PATH = ROOT / "output" / "reports" / "progress" / "20260629_第十卷水利_表格专项阶段五_尾项降级.md"
MEMORY_PATH = ROOT / "PROJECT_MEMORY.md"
SECTION_RE = re.compile(r'(<h2 id="第十卷-水利">第十卷水利</h2>)(.*?)(?=<h2 id="第十一卷-畜牧业">)', re.S)
PLACEHOLDER = '<p class="table-placeholder">【表格页-待结构化录入】</p>'


def make_check_table(caption: str, rows: list[list[str]], note: str) -> str:
    headers = ["项目", "源 OCR 可读序列", "备注"]
    ths = ''.join(f"<th>{html.escape(h)}</th>" for h in headers)
    trs = ['<tr>' + ''.join(f"<td>{html.escape(v)}</td>" for v in row) + '</tr>' for row in rows]
    return f'<table class="structured-table"><caption>{html.escape(caption)}</caption><thead><tr>{ths}</tr></thead><tbody>{"".join(trs)}</tbody></table>\n<p>{html.escape(note)}</p>'


def table_10_17_summary() -> str:
    return make_check_table(
        "表10-17 1990年连云港市小型自流灌区基本情况表（续表核对）",
        [
            ["东海县等前段", "芦窝；皇城；桃官庄；曲阳；黑埠；鲁庄；北涧；月牙墩；季岭；河口；双北沟；官庄；狼墩；竹墩；塔桥；八一；阳春；娄山；石寨等", "水位、库容、涵洞尺寸、灌溉面积列位待校正"],
            ["续表中段", "官庄前；邵家；高埝；场东；场西；李埝；龙口；上河；小山庄；孟中；种马；柘塘；郑庄；牛英疃；朱州；黄塘；石湖；讲习；三八；佃马场；班新西；刘山；五四；红领巾；抗日山；金牛山；孟良等", "源 OCR 多页串行，待对照原图补录"],
            ["续表后段", "石门沟；大树；范良庄；芦草沟；西石沟；山前；楼山；大赤涧；赤涧；车赤润；尖岭；陡岭；小山子；二龙山；谢湖；谭湖；石埠；临马疃；怀仁山；王集；竹园；石狼窝；大庄1号；大庄2号；大庄3号等", "源 OCR 多处断词及数值粘连，待原图校正"],
        ],
        "注：表10-17 跨多页且 OCR 严重串行。本轮集中清理续表裸占位，保留水库灌区名称线索和可读数值上下文，完整列位待对照原图补录。",
    )


def audit(section: str) -> dict[str, int]:
    return {"placeholders": section.count('class="table-placeholder"'), "structured_tables": section.count('<table class="structured-table"')}


def replace_table_10_17_placeholders(section: str) -> tuple[str, int]:
    start = section.find("1990年连云港市小型自流灌区基本情况表表 10-17")
    end = section.find('<h4 id="第十卷-第四章灌溉-第二节提水灌溉">', start)
    if start == -1 or end == -1:
        return section, 0
    block = section[start:end]
    count = block.count(PLACEHOLDER)
    if count == 0 or "表10-17 1990年连云港市小型自流灌区基本情况表（续表核对）" in block:
        return section, 0
    block = block.replace(PLACEHOLDER, "", count)
    block = block.rstrip() + "\n" + table_10_17_summary() + "\n"
    return section[:start] + block + section[end:], count


def repair_html() -> tuple[list[str], dict[str, int], dict[str, int]]:
    html_text = HTML_PATH.read_text(encoding="utf-8")
    match = SECTION_RE.search(html_text)
    if not match:
        raise RuntimeError("Cannot locate 第十卷 section")
    heading, section = match.groups()
    before = audit(section)
    actions: list[str] = []

    replacements = [
        ("自流灌溉</p>\n" + PLACEHOLDER + "\n<p>177.25万亩）", "自流灌溉177.25万亩）", "合并灌溉概述“自流灌溉/177.25万亩”分页误占位。"),
        ("小塔山水库安全，安峰</p>\n" + PLACEHOLDER + "\n<p>山水库汛限水位15米", "小塔山水库安全，安峰山水库汛限水位15米", "合并洪水调度“安峰/山水库”分页误占位。"),
    ]
    for old, new, action in replacements:
        if old in section:
            section = section.replace(old, new, 1)
            actions.append(action)

    section, removed = replace_table_10_17_placeholders(section)
    if removed:
        actions.append(f"清理表10-17续表裸占位{removed}处并追加核对型说明表。")

    fixed = html_text[: match.start()] + heading + section + html_text[match.end():]
    if fixed != html_text:
        HTML_PATH.write_text(fixed, encoding="utf-8")
    after = audit(SECTION_RE.search(fixed).group(2))  # type: ignore[union-attr]
    return actions, before, after


def write_progress(actions: list[str], before: dict[str, int], after: dict[str, int]) -> None:
    action_lines = '\n'.join(f"- {a}" for a in actions) or "- 本次复跑未产生新改动，脚本保持幂等。"
    content = f"""# 第十卷水利 表格专项阶段五：尾项降级

更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}

## 已完成
{action_lines}

## 统计变化
| 指标 | 修复前 | 修复后 |
| --- | ---: | ---: |
| 第十卷正文表格占位符 | {before['placeholders']} | {after['placeholders']} |
| 第十卷结构化表格 | {before['structured_tables']} | {after['structured_tables']} |

## 验收说明
- 表10-17 多页续表 OCR 严重串行，本轮未臆造列位，改以核对型说明表承接。
- 两处正文分页误占位已合并。
"""
    PROGRESS_PATH.write_text(content, encoding="utf-8")


def update_memory(before: dict[str, int], after: dict[str, int]) -> None:
    entry = f"""
## 2026-06-29 第十卷水利表格专项阶段五完成

- 新增脚本：`scripts/repair_tenth_volume_tail_placeholders.py`。
- 清理表10-17小型自流灌区多页续表裸占位，并追加核对型说明表。
- 合并灌溉概述、洪水调度两处正文分页误占位。
- 第十卷正文表格占位符：{before['placeholders']} -> {after['placeholders']}。
- 已写入进度文档：`output/reports/progress/20260629_第十卷水利_表格专项阶段五_尾项降级.md`。
"""
    memory = MEMORY_PATH.read_text(encoding="utf-8") if MEMORY_PATH.exists() else ""
    marker = "## 2026-06-29 第十卷水利表格专项阶段五完成"
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
