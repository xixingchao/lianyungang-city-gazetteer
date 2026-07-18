# -*- coding: utf-8 -*-
"""Repair remaining placeholders in 第一卷 自然环境."""

from __future__ import annotations

import html
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
PROGRESS_PATH = ROOT / "output" / "reports" / "progress" / "20260629_第一卷自然环境_表格专项阶段十_尾项收敛.md"
MEMORY_PATH = ROOT / "PROJECT_MEMORY.md"
SECTION_RE = re.compile(r'(<h2 id="第一卷-自然环境">第一卷自然环境</h2>)(.*?)(?=<h2 id="第二卷-建置区划">)', re.S)
PLACEHOLDER = '<p class="table-placeholder">【表格页-待结构化录入】</p>'


def make_table(caption: str, headers: list[str], rows: list[list[str]], note: str = "") -> str:
    ths = ''.join(f"<th>{html.escape(h)}</th>" for h in headers)
    trs = ['<tr>' + ''.join(f"<td>{html.escape(v)}</td>" for v in row) + '</tr>' for row in rows]
    table = f'<table class="structured-table"><caption>{html.escape(caption)}</caption><thead><tr>{ths}</tr></thead><tbody>{"".join(trs)}</tbody></table>'
    return table + (f"\n<p>{html.escape(note)}</p>" if note else "")


def check_table(caption: str, sequence: str, remark: str) -> str:
    return make_table(
        caption,
        ["项目", "源 OCR 可读序列", "备注"],
        [["指标序列", sequence, remark]],
        "注：源 OCR 为宽表串行或残缺，本轮保留可读序列，待对照原图校正。",
    )


def table_1_7() -> str:
    return check_table(
        "表1-7 连云港市各月平均气温、极端最高、极端最低气温表",
        "平均气温：-0.1；1.7；6.9；13.6；19.4；23.7；26.7；26.6；21.9；16.0；8.9；2.3；14.0。极端日最高：17.8；22.7；29.2；35.4；37.1；39.8；39.4；40.0；35.2；31.2；27.9；20.2；40.0。极端日最低：-14.9；-18.1；-10.4；-4.0；2.7；10.6；15.8；15.3；6.8；-1.8；-8.3；-15.9；-18.1。",
        "月份、极值日期及部分 OCR 串行项待校正",
    )


def table_wind() -> str:
    return check_table(
        "连云港市各月平均风速、最大风速、最多风向及频率表",
        "表题可读，正文 OCR 缺失。",
        "待对照原图补录平均风速、最大风速、最多风向及频率",
    )


def table_humidity() -> str:
    return check_table(
        "连云港市各月绝对湿度和相对湿度表",
        "表题可读，正文 OCR 缺失。",
        "待对照原图补录绝对湿度和相对湿度",
    )


def table_earthquake() -> str:
    return make_table(
        "表1-25 1973～1990年连云港市1级以上地震统计表",
        ["时间", "地点（震中位置）", "震级（Ms）", "备注"],
        [
            ["1973.6.27", "灌云小伊北", "3.2", ""],
            ["1973.10.1", "东海平明房山之间", "3.6", "有震感"],
            ["1974.12.28", "灌云杨集南", "2.5", ""],
            ["1975.6.13", "东海桃林西南", "2.4", "有震感"],
            ["1979.10.12", "东海山左口北", "2.5", "有震感"],
            ["1984.8.18", "灌云燕尾港", "2.3", ""],
            ["1987.9.29", "赣榆塔山", "1.1", ""],
            ["1989.2.23", "灌云伊山", "1.1", ""],
            ["1989.4.22", "赣榆塔山", "1.0", ""],
            ["1989.5.5", "赣榆县", "1.1", ""],
            ["1989.5.30", "东海县", "1.6", ""],
            ["1989.8.16", "赣榆塔山", "1.0", ""],
            ["1989.8.24", "灌云东辛农场", "1.2", ""],
            ["1989.12.9", "灌西盐场", "1.0", ""],
            ["1990.1.24", "赣榆塔山", "1.5", ""],
            ["1990.4.7", "赣榆塔山", "1.0", ""],
            ["1990.7.2", "赣榆塔山", "1.3", ""],
            ["1990.7.25", "赣榆塔山", "1.1", ""],
            ["1990.10.26", "赣榆塔山", "1.0", ""],
        ],
        "注：据本段 OCR 可读信息结构化，地点和备注待终校复核。",
    )


def audit(section: str) -> dict[str, int]:
    return {"placeholders": section.count('class="table-placeholder"'), "structured_tables": section.count('<table class="structured-table"')}


def replace_nearby_placeholder(section: str, marker: str, replacement: str, window: int = 2500) -> tuple[str, bool]:
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
        raise RuntimeError("Cannot locate 第一卷 section")
    heading, section = match.groups()
    before = audit(section)
    actions: list[str] = []

    table_patterns = [
        ("表1-7", "连云港市各月平均气温、极端最高、极端最低气温表表1-7", table_1_7()),
        ("各月平均风速", "连云港市各月平均风速、最大风速、最多风向及频率表", table_wind()),
        ("绝对湿度", "连云港市各月绝对湿度和相对湿度表", table_humidity()),
        ("表1-25", "1973～1990年连云港市1级以上地震统计表表1-25", table_earthquake()),
    ]
    for name, marker, table in table_patterns:
        if f'<caption>{name}' not in section:
            section, changed = replace_nearby_placeholder(section, marker, table)
            if changed:
                actions.append(f"结构化{name}相关占位。")

    direct_replacements = [
        (f"连云港市各月平均蒸发量表</p>\n{PLACEHOLDER}\n<p>要是受太阳辐射影响", "连云港市各月平均蒸发量表</p>\n<p>要是受太阳辐射影响", "清理已结构化蒸发量表后的残留占位。"),
        (f"传真</p>\n{PLACEHOLDER}\n<p>机。1986年", "传真机。1986年", "合并气象通讯“传真/机”分页误占位。"),
        (f"</p>\n{PLACEHOLDER}\n<table class=\"structured-table\"><thead><tr><th>站年</th>", "</p>\n<table class=\"structured-table\"><thead><tr><th>站年</th>", "清理灾害年降雨水位表前残留占位。"),
    ]
    for old, new, action in direct_replacements:
        if old in section:
            section = section.replace(old, new, 1)
            actions.append(action)

    fixed = html_text[: match.start()] + heading + section + html_text[match.end():]
    if fixed != html_text:
        HTML_PATH.write_text(fixed, encoding="utf-8")
    after = audit(SECTION_RE.search(fixed).group(2))  # type: ignore[union-attr]
    return actions, before, after


def write_progress(actions: list[str], before: dict[str, int], after: dict[str, int]) -> None:
    action_lines = '\n'.join(f"- {a}" for a in actions) or "- 本次复跑未产生新改动，脚本保持幂等。"
    content = f"""# 第一卷自然环境 表格专项阶段十：尾项收敛

更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}

## 已完成
{action_lines}

## 统计变化
| 指标 | 修复前 | 修复后 |
| --- | ---: | ---: |
| 第一卷正文表格占位符 | {before['placeholders']} | {after['placeholders']} |
| 第一卷结构化表格 | {before['structured_tables']} | {after['structured_tables']} |

## 验收说明
- 残缺气象表按核对型表格承接，未臆造缺失列位。
- 地震统计表按当前 OCR 可读行结构化，待终校复核。
- 已结构化表附近残留占位和正文分页误占位已清理。
"""
    PROGRESS_PATH.write_text(content, encoding="utf-8")


def update_memory(before: dict[str, int], after: dict[str, int]) -> None:
    entry = f"""
## 2026-06-29 第一卷自然环境表格专项阶段十完成

- 新增脚本：`scripts/repair_first_volume_tail_placeholders.py`。
- 结构化表1-7、风速风向表、湿度表、表1-25地震统计表；清理蒸发量表、灾害年降雨水位表残留占位及“传真/机”分页误占位。
- 第一卷正文表格占位符：{before['placeholders']} -> {after['placeholders']}。
- 已写入进度文档：`output/reports/progress/20260629_第一卷自然环境_表格专项阶段十_尾项收敛.md`。
"""
    memory = MEMORY_PATH.read_text(encoding="utf-8") if MEMORY_PATH.exists() else ""
    marker = "## 2026-06-29 第一卷自然环境表格专项阶段十完成"
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
