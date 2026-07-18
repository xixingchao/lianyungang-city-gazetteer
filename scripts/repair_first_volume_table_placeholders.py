# -*- coding: utf-8 -*-
"""Clean verified 第一卷 table placeholders in the full reader."""

from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
PROGRESS_PATH = ROOT / "output" / "reports" / "progress" / "20260629_第一卷自然环境_表格专项进度.md"
MEMORY_PATH = ROOT / "PROJECT_MEMORY.md"

SECTION_RE = re.compile(
    r'(<h2 id="第一卷-自然环境">第一卷自然环境</h2>)(.*?)(?=<h2 id="第二卷-建置区划">)',
    re.S,
)
PLACEHOLDER = '<p class="table-placeholder">【表格页-待结构化录入】</p>\n'


def audit_section(section: str) -> dict[str, int]:
    return {
        "placeholders": section.count('class="table-placeholder"'),
        "structured_tables": section.count('<table class="structured-table"'),
        "table_1_13": section.count('<caption>表1-13 连云港市各月平均蒸发量表</caption>'),
        "table_1_24": section.count('<caption>表1-24 连云港市沿海潮位站最高最低潮位统计表</caption>'),
        "raw_1_24": section.count('连云港市沿海潮位站最高最低潮位统计表表1-24单位：米站名'),
    }


def repair_html() -> tuple[list[str], dict[str, int], dict[str, int]]:
    html = HTML_PATH.read_text(encoding="utf-8")
    match = SECTION_RE.search(html)
    if not match:
        raise RuntimeError("Cannot locate 第一卷 自然环境 section")

    heading, section = match.groups()
    before_stats = audit_section(section)
    actions: list[str] = []

    table_1_13 = '<table class="structured-table"><caption>表1-13 连云港市各月平均蒸发量表</caption>'
    old = PLACEHOLDER + table_1_13
    if old in section:
        section = section.replace(old, table_1_13, 1)
        actions.append("撤除表1-13《连云港市各月平均蒸发量表》前的遗留占位符；结构化表已存在且来源为 LYG-上-T003。")

    table_1_24 = '<table class="structured-table"><caption>表1-24 连云港市沿海潮位站最高最低潮位统计表</caption>'
    raw_1_24 = re.compile(
        re.escape(PLACEHOLDER)
        + r'<p>连云港市沿海潮位站最高最低潮位统计表表1-24单位：米站名.*?注：此表基面未统一，用时请换算。</p>\n'
        + re.escape(table_1_24),
        re.S,
    )
    section, removed_raw = raw_1_24.subn(table_1_24, section, count=1)
    if removed_raw:
        actions.append("撤除表1-24《连云港市沿海潮位站最高最低潮位统计表》前的占位符和乱序 OCR 表格纯文本；保留已核验结构化表 LYG-上-T005。")
    elif PLACEHOLDER + table_1_24 in section:
        section = section.replace(PLACEHOLDER + table_1_24, table_1_24, 1)
        actions.append("撤除表1-24《连云港市沿海潮位站最高最低潮位统计表》前的遗留占位符；结构化表已存在且来源为 LYG-上-T005。")

    fixed = html[: match.start()] + heading + section + html[match.end() :]
    if fixed != html:
        HTML_PATH.write_text(fixed, encoding="utf-8")

    after_match = SECTION_RE.search(fixed)
    if not after_match:
        raise RuntimeError("Cannot locate 第一卷 after repair")
    after_stats = audit_section(after_match.group(2))
    return actions, before_stats, after_stats


def write_progress(actions: list[str], before: dict[str, int], after: dict[str, int]) -> None:
    action_lines = "\n".join(f"- {action}" for action in actions) or "- 本次复跑未产生新改动，脚本保持幂等。"
    content = f"""# 第一卷自然环境 表格专项进度

更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}

## 本轮范围
- 章节：第一卷 自然环境。
- 目标：优先清理已有可靠结构化表格前残留的占位符和乱序 OCR 表格文本。
- 输入：`output/final_reader/连云港市志_全书.html`、`workbench/table_entries/上/data/LYG-上-T003.json`、`workbench/table_entries/上/data/LYG-上-T005.json`。

## 已完成
{action_lines}

## 统计变化
| 指标 | 修复前 | 修复后 |
| --- | ---: | ---: |
| 第一卷正文表格占位符 | {before['placeholders']} | {after['placeholders']} |
| 第一卷结构化表格 | {before['structured_tables']} | {after['structured_tables']} |
| 表1-13结构化表 | {before['table_1_13']} | {after['table_1_13']} |
| 表1-24结构化表 | {before['table_1_24']} | {after['table_1_24']} |
| 表1-24乱序OCR纯文本残留 | {before['raw_1_24']} | {after['raw_1_24']} |

## 当场验收
- 表1-13、表1-24均保留结构化 HTML 表格，没有新增手工臆造数据。
- 本脚本可重复运行；再次运行不会重复删除或破坏结构化表。
- 全书表格占位符清单、全书阅读器审计和 TypeScript 类型检查作为本轮最终验收项。

## 遇到的问题
- 第一卷还有多张气候、水文、灾害宽表只有 OCR 串行文本或跨页碎片，暂不能在没有逐页核图的情况下结构化。
- `LYG-上-T004.json` 虽有表格资产，但标题、页码和内容说明存在矛盾，暂不用于替换表1-20等灾害水位表。

## 下一步计划
- 继续第一卷表格专项：优先核对表1-4、表1-6、风速湿度、主要河流、水位/降雨灾害、石梁河水库和水面蒸发量等剩余占位。
- 若已有 OCR 不能可靠还原列行，转入 PDF 页面逐表核对后再结构化。
"""
    PROGRESS_PATH.write_text(content, encoding="utf-8")


def update_memory(before: dict[str, int], after: dict[str, int]) -> None:
    entry = f"""
## 2026-06-29 第一卷自然环境表格专项阶段一完成

已完成第一卷表格专项第一阶段：

- 新增脚本：`scripts/repair_first_volume_table_placeholders.py`。
- 清理表1-13《连云港市各月平均蒸发量表》前的遗留占位符，保留结构化表 `LYG-上-T003`。
- 清理表1-24《连云港市沿海潮位站最高最低潮位统计表》前的遗留占位符和乱序 OCR 表格纯文本，保留结构化表 `LYG-上-T005`。
- 第一卷正文表格占位符：{before['placeholders']} -> {after['placeholders']}。
- 第一卷结构化表格保持：{after['structured_tables']} 处。
- 已写入进度文档：`output/reports/progress/20260629_第一卷自然环境_表格专项进度.md`。

下一步：继续第一卷剩余表格占位符，重点核对宽表和跨页水文表。
"""
    memory = MEMORY_PATH.read_text(encoding="utf-8") if MEMORY_PATH.exists() else ""
    marker = "## 2026-06-29 第一卷自然环境表格专项阶段一完成"
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
