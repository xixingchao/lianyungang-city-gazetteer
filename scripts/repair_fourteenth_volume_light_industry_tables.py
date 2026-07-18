# -*- coding: utf-8 -*-
"""Repair placeholders in 第十四卷 轻（手）工业."""

from __future__ import annotations

import html
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
PROGRESS_PATH = ROOT / "output" / "reports" / "progress" / "20260629_第十四卷轻手工业_表格专项阶段一.md"
MEMORY_PATH = ROOT / "PROJECT_MEMORY.md"
SECTION_RE = re.compile(r'(<h2 id="第十四卷-轻-手-工业">第十四卷轻（手）工业</h2>)(.*?)(?=<h2 id="第十五卷-纺织工业">)', re.S)
PLACEHOLDER = '<p class="table-placeholder">【表格页-待结构化录入】</p>'


def make_table(caption: str, rows: list[list[str]], note: str) -> str:
    cols = ["项目", "源 OCR 可读序列", "备注"]
    ths = ''.join(f"<th>{html.escape(c)}</th>" for c in cols)
    trs = ['<tr>' + ''.join(f"<td>{html.escape(v)}</td>" for v in row) + '</tr>' for row in rows]
    return f'<table class="structured-table"><caption>{html.escape(caption)}</caption><thead><tr>{ths}</tr></thead><tbody>{"".join(trs)}</tbody></table>\n<p>{html.escape(note)}</p>'


def table_14_3() -> str:
    return make_table(
        "表14-3 1980～1990年陇东火柴厂主要指标统计表",
        [["指标序列", "19.14；277.53；20.80；10.45；183.17；25.93；375.99；89.35；10.39；184.01；31.60；435.20；119.40；10.24；235.10；32.85；476.30；129.05；10.57；290.20；35.40；513.30；115.72；11.41；290.20；34.37；498.37；143.76；14.86；453.55；28.43；412.20；6.71；17.25；465.17；23.68；356.80；-26.85；19.36；477.60；25.14；375.40；92.80；23.27；515.40；30.35；444.50；151.87；30.25；422.00；32.04；464.58；118.81；31.32；468.00", "年份、职工、产量、产值、利润、成本、固定资产原值列位待校正"]],
        "注：源 OCR 为多列宽表串行，本轮保留可读序列，具体列位待原图补录。",
    )


def table_14_4() -> str:
    return make_table(
        "表14-4 1978～1988年连云港市衡器业主要指标统计表",
        [["指标序列", "12.20；10.30；1.20；6.40；11.30；9.70；1.70；0.40；15.00；16.40；1.80；0.70；9.40；9.40；0.60；0.40；12.40；11.70；1.20；0.50；19.00；24.60；5.40；1.10；11.10；16.20；0.70；0.60；14.40；27.30；2.20；0.80；22.80；51.40；-2.40；1.40；15.50；40.30；4.10；1.50；21.50；27.90；4.70；1.50", "年份、产量、产值、销售收入、利润、税金列位待校正"]],
        "注：源 OCR 为宽表串行，本轮先保留可读序列，待原图校正。",
    )


def table_14_5() -> str:
    return make_table(
        "表14-5 1969～1988年部分年份连云港市制锅业主要指标统计表",
        [["前段指标序列", "8.64；11.70；35.50；47.36；37.50；59.32；38.73；51.00；40.39；63.62；36.20；52.44；36.10；52.10；24.80；35.41；13.48；27.51；8.13；36.98；20.68；42.20；26.70；54.91；30.14；62.20", "1969～1982年前段列位待校正；下方既有结构化续表保留"]],
        "注：源 OCR 前段缺年份列位，本轮保留可读序列，待原图补录。",
    )


def table_14_7() -> str:
    return make_table(
        "表14-7 1990年连云港市主要家具企业基本情况表",
        [
            ["市家具一厂", "市/集体；22000；11000；8.50；192.8", "列位待校正"],
            ["市家具二厂", "市/集体；2.20；37.6", "列位待校正"],
            ["市钢木家具厂", "区/联营；33300；4.50；11040", "列位待校正"],
            ["赣榆县木器厂", "县/集体；17500；5.00；10000", "列位待校正"],
            ["赣榆县罗阳轻河家具厂", "乡/联营；30600；4.50；20000", "列位待校正"],
            ["东海县家具厂", "县/集体；12500；3.40；111.20", "列位待校正"],
            ["灌云县家具厂", "镇/集体；11000；2.20", "列位待校正"],
        ],
        "注：源 OCR 表头完整但数据列串行，本轮按企业保留可读序列，面积、职工、固定资产、产值等列待原图校正。",
    )


def table_14_8() -> str:
    return make_table(
        "表14-8 1979～1988年连云港市碘钨灯生产主要指标统计表",
        [["指标序列", "17.13；140.93；26.17；229.72；17.51；144.12；27.08；214.38；42.28；439.00；46.51；512.08；64.36；679.09；57.56；519.16；57.03；702.12；76.91；770.70；10541", "年份、职工、产量、产值、劳动生产率列位待校正"]],
        "注：源 OCR 宽表串行，本轮先保留可读序列，待对照原图补录。",
    )


def table_14_9() -> str:
    return make_table(
        "表14-9 1987～1990年连云港市精密仪器厂主要指标统计表",
        [["指标序列", "85.87；2.45；51.48；6.76；3.63；76.69；0.46；6.20；122.89；3.44；6.56；184.9；10330", "年份、职工、固定资产原值、产量、产值、劳动生产率列位待校正"]],
        "注：源 OCR 缺列位，本轮保留可读序列，待原图校正。",
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
        raise RuntimeError("Cannot locate 第十四卷 section")
    heading, section = match.groups()
    before = audit(section)
    actions: list[str] = []

    replacements = [
        ('试</p>\n' + PLACEHOLDER + '\n<p>产任务后', '试产任务后', "清理文化用纸正文“试/产”分页误占位。"),
        ('停产。</p>\n' + PLACEHOLDER + '\n<p>下半年关闭。', '停产。下半年关闭。', "清理肥皂正文“停产/下半年”分页误占位。"),
        ('设备，</p>\n' + PLACEHOLDER + '\n<p>利用市玻璃二厂厂房等设施试产', '设备，利用市玻璃二厂厂房等设施试产', "清理日光灯管正文分页误占位。"),
        ('“金牛”</p>\n' + PLACEHOLDER + '\n<p>奖。</p>', '“金牛”奖。</p>', "清理特种灯泡厂正文分页误占位。"),
    ]
    for old, new, action in replacements:
        if old in section:
            section = section.replace(old, new, 1)
            actions.append(action)

    table_patterns = [
        ("表14-3", "1980～1990年陇东火柴厂主要指标统计表表14-3", table_14_3()),
        ("表14-4", "1978～1988年连云港市衡器业主要指标统计表表14-4", table_14_4()),
        ("表14-5", "1969～1988年部分年份连云港市制锅业主要指标统计表表14-5", table_14_5()),
        ("表14-7", "1990年连云港市主要家具企业基本情况表表14-7", table_14_7()),
        ("表14-8", "1979～1988年连云港市碘钨灯生产主要指标统计表表14-8", table_14_8()),
        ("表14-9", "1987～1990年连云港市精密仪器厂主要指标统计表表14-9", table_14_9()),
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
    content = f"""# 第十四卷轻（手）工业 表格专项阶段一

更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}

## 已完成
{action_lines}

## 统计变化
| 指标 | 修复前 | 修复后 |
| --- | ---: | ---: |
| 第十四卷正文表格占位符 | {before['placeholders']} | {after['placeholders']} |
| 第十四卷结构化表格 | {before['structured_tables']} | {after['structured_tables']} |

## 验收说明
- 正文分页误占位已合并。
- 指标宽表按核对型表格保留源 OCR 可读序列，未臆造列位。
"""
    PROGRESS_PATH.write_text(content, encoding="utf-8")


def update_memory(before: dict[str, int], after: dict[str, int]) -> None:
    entry = f"""
## 2026-06-29 第十四卷轻手工业表格专项阶段一完成

- 新增脚本：`scripts/repair_fourteenth_volume_light_industry_tables.py`。
- 清理第十四卷文化用纸、肥皂、日光灯管、特种灯泡厂等正文分页误占位。
- 结构化表14-3、表14-4、表14-5、表14-7、表14-8、表14-9为核对型表格。
- 第十四卷正文表格占位符：{before['placeholders']} -> {after['placeholders']}。
- 已写入进度文档：`output/reports/progress/20260629_第十四卷轻手工业_表格专项阶段一.md`。
"""
    memory = MEMORY_PATH.read_text(encoding="utf-8") if MEMORY_PATH.exists() else ""
    marker = "## 2026-06-29 第十四卷轻手工业表格专项阶段一完成"
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
