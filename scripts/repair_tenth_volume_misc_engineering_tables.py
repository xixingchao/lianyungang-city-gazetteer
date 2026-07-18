# -*- coding: utf-8 -*-
"""Repair miscellaneous engineering table placeholders in 第十卷 水利."""

from __future__ import annotations

import html
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
PROGRESS_PATH = ROOT / "output" / "reports" / "progress" / "20260629_第十卷水利_表格专项阶段四_工程表误占位.md"
MEMORY_PATH = ROOT / "PROJECT_MEMORY.md"
SECTION_RE = re.compile(r'(<h2 id="第十卷-水利">第十卷水利</h2>)(.*?)(?=<h2 id="第十一卷-畜牧业">)', re.S)
PLACEHOLDER = '<p class="table-placeholder">【表格页-待结构化录入】</p>'


def make_table(caption: str, columns: list[str], rows: list[list[str]], note: str) -> str:
    ths = ''.join(f"<th>{html.escape(c)}</th>" for c in columns)
    trs = []
    for row in rows:
        trs.append('<tr>' + ''.join(f"<td>{html.escape(v)}</td>" for v in row) + '</tr>')
    return f'<table class="structured-table"><caption>{html.escape(caption)}</caption><thead><tr>{ths}</tr></thead><tbody>{"".join(trs)}</tbody></table>\n<p>{html.escape(note)}</p>'


def table_10_2_html() -> str:
    return make_table(
        "表10-2 1990年新沭河连云港市境内桥、闸基本情况表",
        ["名称", "建成年月", "源 OCR 可读序列", "备注"],
        [
            ["蒋庄漫水闸", "1957.5", "3.70；10.8；7.1；10.5；5.0；12.63；12.33；4.2", "列位待原图校正"],
            ["墩尚公路桥", "1974.6", "12.1；11.5；9.7；9.5", "列位待原图校正"],
            ["朱圈漫水桥", "1976.3", "6.9；5.3；0.0；8.40", "列位待原图校正"],
            ["太平庄闸", "1977.7", "5.0；5.20；10.5；2.0；10.09；6.57；4.7；31", "列位待原图校正"],
        ],
        "注：源 OCR 可识别名称、建成年月和数值序列，但桥闸宽表列位错位；本轮先替代表页占位，具体列位待对照原图补录。",
    )


def table_10_11_html() -> str:
    return make_table(
        "表10-11 1990年连云港市沭南引排干支河基本情况表",
        ["河名", "境内起迄位置", "源 OCR 可读序列", "备注"],
        [
            ["蔷薇河", "友谊河口一临洪闸", "50～80；-0.5～-2.5；1:2～1:3；6～8；9.45～8", "流量、河底、堤顶等列位待校正"],
            ["民主河", "沭新渠小丘庄—马汪村", "1.5～0.7；1:2；3～6.5；8.8～7.0；1:2～1:2.5", "列位待校正"],
            ["马河", "沭新渠马河闸一顾庄", "10～30；1.5～0；1:2；8～7.5；1:2～1:3", "列位待校正"],
            ["鲁兰河", "驼峰乡上湾村～富安村", "30～60；6～1；1:3；11～9；1:2～1:3", "列位待校正"],
            ["乌龙河", "青湖镇—乌龙河调度闸", "10～20；4～-1；1:2～1:3；4～6；8.5～7.0；1:2", "列位待校正"],
            ["磨山河", "青湖闸—黄圈村", "9.7；9.7～7.0；1:2；8～10；15.7～13.6；1:2～1:3", "列位待校正"],
            ["大浦河", "新浦市区一大浦闸", "6.5；-1.0；1:3.5；1:3", "列位待校正"],
        ],
        "注：源 OCR 表头与字段串行打散，本轮按河名保留可读序列，完整字段待对照原图补录。",
    )


def audit(section: str) -> dict[str, int]:
    return {
        "placeholders": section.count('class="table-placeholder"'),
        "structured_tables": section.count('<table class="structured-table"'),
        "table_10_2": section.count('表10-2 1990年新沭河连云港市境内桥、闸基本情况表'),
        "table_10_11": section.count('表10-11 1990年连云港市沭南引排干支河基本情况表'),
        "broken_2_m": section.count('堤顶超高2</p>\n<p class="table-placeholder">【表格页-待结构化录入】</p>\n<p>米'),
    }


def repair_html() -> tuple[list[str], dict[str, int], dict[str, int]]:
    html_text = HTML_PATH.read_text(encoding="utf-8")
    match = SECTION_RE.search(html_text)
    if not match:
        raise RuntimeError("Cannot locate 第十卷 水利 section")
    heading, section = match.groups()
    before = audit(section)
    actions: list[str] = []

    marker_10_2 = '1990年新沭河连云港市境内桥、闸基本情况表表10-2工程规模设计水位防洪水位校核流量建成名称年月'
    if '<caption>表10-2 1990年新沭河连云港市境内桥、闸基本情况表</caption>' not in section and marker_10_2 in section:
        section = section.replace(PLACEHOLDER + '\n<p>1990年新沭河连云港市境内穿堤建筑物情况表', table_10_2_html() + '\n<p>1990年新沭河连云港市境内穿堤建筑物情况表', 1)
        actions.append("结构化表10-2为核对型表格，清理桥闸基本情况表后一处占位。")

    broken = '堤顶超高2</p>\n<p class="table-placeholder">【表格页-待结构化录入】</p>\n<p>米'
    if broken in section:
        section = section.replace(broken, '堤顶超高2米', 1)
        actions.append("清理新沂河治理正文中由分页造成的误占位，将“2/米”断句合并。")

    if '<caption>表10-11 1990年连云港市沭南引排干支河基本情况表</caption>' not in section:
        pattern = re.compile(
            r'<p>1990年连云港市沭南引排干支河基本情况表表10-11.*?注：蔷薇河上游黄泥河发源于新沂县马陵山区，有淋头河、后镇河、虞姬沟等汇入，长24公里，其中连云港市境内长17公里。</p>\n'
            + re.escape(PLACEHOLDER),
            re.S,
        )
        section, count = pattern.subn(table_10_11_html(), section, count=1)
        if count:
            actions.append("结构化表10-11为核对型表格，清理沭南引排干支河表占位。")

    fixed = html_text[: match.start()] + heading + section + html_text[match.end():]
    if fixed != html_text:
        HTML_PATH.write_text(fixed, encoding="utf-8")
    after = audit(SECTION_RE.search(fixed).group(2))  # type: ignore[union-attr]
    return actions, before, after


def write_progress(actions: list[str], before: dict[str, int], after: dict[str, int]) -> None:
    action_lines = '\n'.join(f"- {a}" for a in actions) or "- 本次复跑未产生新改动，脚本保持幂等。"
    content = f"""# 第十卷水利 表格专项阶段四：工程表与误占位

更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}

## 本轮范围
- 章节：第十卷 水利，第一章防洪、第二章除涝。
- 目标：处理表10-2、表10-11，并清理一处正文分页误占位。

## 已完成
{action_lines}

## 统计变化
| 指标 | 修复前 | 修复后 |
| --- | ---: | ---: |
| 第十卷正文表格占位符 | {before['placeholders']} | {after['placeholders']} |
| 第十卷结构化表格 | {before['structured_tables']} | {after['structured_tables']} |
| 表10-2出现次数 | {before['table_10_2']} | {after['table_10_2']} |
| 表10-11出现次数 | {before['table_10_11']} | {after['table_10_11']} |
| 正文误占位残留 | {before['broken_2_m']} | {after['broken_2_m']} |

## 当场验收
- 表10-2、表10-11均以核对型结构化表保留源 OCR 可读序列。
- 宽表列位未臆造，待后续对照原图补录。
- 本脚本可重复运行；再次运行不会重复插入表格。

## 下一步计划
- 第十卷已降出 P0 后，继续逐卷清理 P1：第十三卷盐业、第十二卷水产、第一卷自然环境等。
"""
    PROGRESS_PATH.write_text(content, encoding="utf-8")


def update_memory(before: dict[str, int], after: dict[str, int]) -> None:
    entry = f"""
## 2026-06-29 第十卷水利表格专项阶段四完成

已完成第十卷工程表与误占位专项第四阶段：

- 新增脚本：`scripts/repair_tenth_volume_misc_engineering_tables.py`。
- 结构化表10-2、表10-11为核对型表格，保留源 OCR 可读序列。
- 清理新沂河治理正文中一处由分页造成的误占位。
- 第十卷正文表格占位符：{before['placeholders']} -> {after['placeholders']}。
- 第十卷结构化表格：{before['structured_tables']} -> {after['structured_tables']}。
- 已写入进度文档：`output/reports/progress/20260629_第十卷水利_表格专项阶段四_工程表误占位.md`。

下一步：第十卷已降出 P0，继续逐卷清理 P1 表格占位符。
"""
    memory = MEMORY_PATH.read_text(encoding="utf-8") if MEMORY_PATH.exists() else ""
    marker = "## 2026-06-29 第十卷水利表格专项阶段四完成"
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
