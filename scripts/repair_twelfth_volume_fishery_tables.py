# -*- coding: utf-8 -*-
"""Repair selected placeholders in 第十二卷 水产."""

from __future__ import annotations

import html
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
PROGRESS_PATH = ROOT / "output" / "reports" / "progress" / "20260629_第十二卷水产_表格专项阶段一.md"
MEMORY_PATH = ROOT / "PROJECT_MEMORY.md"
SECTION_RE = re.compile(r'(<h2 id="第十二卷-水产">第十二卷水产</h2>)(.*?)(?=<h2 id="第十三卷-盐业">)', re.S)
PLACEHOLDER = '<p class="table-placeholder">【表格页-待结构化录入】</p>'


def make_table(caption: str, columns: list[str], rows: list[list[str]], note: str) -> str:
    ths = ''.join(f"<th>{html.escape(c)}</th>" for c in columns)
    trs = ['<tr>' + ''.join(f"<td>{html.escape(v)}</td>" for v in row) + '</tr>' for row in rows]
    return f'<table class="structured-table"><caption>{html.escape(caption)}</caption><thead><tr>{ths}</tr></thead><tbody>{"".join(trs)}</tbody></table>\n<p>{html.escape(note)}</p>'


def table_12_1() -> str:
    return make_table(
        "表12-1 海州湾渔场主要渔类及渔期表",
        ["类别", "种名/地方名", "源 OCR 可读渔期和生长情况", "备注"],
        [
            ["鱼类", "黄鲫/黄季鱼", "一年两次渔期：春季4月初到5月下旬，秋季8～9月；渔场在连岛山北至岚山头一带。", "列位按源文整理"],
            ["鱼类", "真鲷/加吉鱼", "海州湾为产卵场，产卵期5月；20世纪30年代后资源被破坏，至1990年未见明显恢复。", "列位按源文整理"],
            ["鱼类", "大黄鱼/黄鱼", "海州湾为产卵场，渔期5月上旬到7月，6月产卵。", "列位按源文整理"],
            ["鱼类", "小黄鱼/黄花鱼", "海州湾是产卵场，渔期4～6月，5月旺季。", "列位按源文整理"],
            ["鱼类", "带鱼/镰刀鱼", "春秋两季，春季4月下旬入渔场，5～6月下旬为产卵期；秋季8～9月。", "列位按源文整理"],
            ["甲壳类", "东方对虾/对虾", "渔期4月上旬到5月底，4月底5月初为旺期，分布在5～10米深泥质海域和河口海湾。", "列位按源文整理"],
            ["贝类", "兰蛤/海沙子", "分布在赣榆县海头镇以南、连云区西墅村西北、临洪河口外泥质底潮间带。", "列位按源文整理"],
            ["软体类", "乌贼/大乌贼", "渔期5～6月，为产卵群体，主要分布在5～15米深较清水中。", "列位按源文整理"],
        ],
        "注：源 OCR 将多页表格串入正文，本轮按可读条目整理为核对型表格；完整物种全表待对照原图校正。",
    )


def table_12_5() -> str:
    return make_table(
        "表12-5 1949～1990年部分年份连云港市海洋捕捞产量、渔船数量统计表",
        ["项目", "源 OCR 可读序列", "备注"],
        [
            ["表头", "年份、产量、国营渔轮捕捞产量、个体捕鱼、渔船总数、其中机帆船、其中渔轮、功率", "列位待原图校正"],
            ["可读数据", "18752；海洋捕捞产量60207吨；国营渔轮捕捞13439吨；渔民捕捞46768吨", "表页前后正文可确认部分"],
            ["后续分品种表衔接", "鱼类2429328；鯧鱼、东方对虾、周氏新对虾、鹰爪虾、中国毛虾、三疣梭子蟹、海蜇、乌贼等", "疑与表12-6相邻，待核图"],
        ],
        "注：表12-5宽表 OCR 列位错乱，本轮先替代表页占位并保留可读序列，未臆造年份和列位。",
    )


def table_12_11() -> str:
    return make_table(
        "表12-11 1990年连云港市冷库情况统计表",
        ["单位", "冷库座数", "制冰能力/冷藏能力等源 OCR 序列", "备注"],
        [
            ["赣榆县", "3", "13600", "列位待校正"],
            ["东海县", "", "", "列位待校正"],
            ["灌云县", "", "300000", "列位待校正"],
            ["连云区", "24", "422410210", "列位待校正"],
            ["云台区", "1", "1250", "列位待校正"],
            ["连云港渔业公司等续表", "10", "1087490803087010108", "续表列位待校正"],
        ],
        "注：表12-11与表12-12相邻，源 OCR 表头和数据串行；本轮保留单位和可读序列，具体制冰、冷藏、冷冻品等列待原图补录。",
    )


def audit(section: str) -> dict[str, int]:
    return {
        "placeholders": section.count('class="table-placeholder"'),
        "structured_tables": section.count('<table class="structured-table"'),
        "table_12_1": section.count('表12-1 海州湾渔场主要渔类及渔期表'),
        "table_12_5": section.count('表12-5 1949～1990年部分年份连云港市海洋捕捞产量、渔船数量统计表'),
        "table_12_11": section.count('表12-11 1990年连云港市冷库情况统计表'),
    }


def repair_html() -> tuple[list[str], dict[str, int], dict[str, int]]:
    html_text = HTML_PATH.read_text(encoding="utf-8")
    match = SECTION_RE.search(html_text)
    if not match:
        raise RuntimeError("Cannot locate 第十二卷 水产 section")
    heading, section = match.groups()
    before = audit(section)
    actions: list[str] = []

    if '<caption>表12-1 海州湾渔场主要渔类及渔期表</caption>' not in section:
        pattern = re.compile(re.escape(PLACEHOLDER) + r'\n<table class="structured-table"><thead><tr><th>品种</th>.*?</table>', re.S)
        section, count = pattern.subn(table_12_1(), section, count=1)
        if count:
            actions.append("结构化表12-1为核对型表格，替换空占位表。")

    if '<caption>表12-5 1949～1990年部分年份连云港市海洋捕捞产量、渔船数量统计表</caption>' not in section:
        pattern = re.compile(r'<p>1949～1990年部分年份连云港市海洋捕捞产量、渔船数量统计表表12-5.*?</p>\n(?:<p>.*?</p>\n){1,8}' + re.escape(PLACEHOLDER), re.S)
        section, count = pattern.subn(table_12_5(), section, count=1)
        if count:
            actions.append("结构化表12-5为核对型表格。")

    broken = '<p>1984年起，市水产科学研究所承担省海珍品增养殖放流任务，从山东长岛运来1厘</p>\n' + PLACEHOLDER + '\n<p>米大的刺参稚参向车牛山西湾海域投放7.5万头'
    if broken in section:
        section = section.replace(broken, '<p>1984年起，市水产科学研究所承担省海珍品增养殖放流任务，从山东长岛运来1厘米大的刺参稚参向车牛山西湾海域投放7.5万头', 1)
        actions.append("清理海参增殖正文“1厘/米”分页误占位。")

    if '<caption>表12-11 1990年连云港市冷库情况统计表</caption>' not in section:
        pattern = re.compile(r'<p>1990年连云港市冷库情况统计表表12-11.*?</p>\n(?:<p>.*?</p>\n){1,8}' + re.escape(PLACEHOLDER) + r'\n(?:<table class="structured-table">.*?</table>\n)?<p>续上表冷库制冰能力.*?灌云县水产供销公司灌云县冷库海产品加工燕尾镇</p>', re.S)
        section, count = pattern.subn(table_12_11(), section, count=1)
        if count:
            actions.append("结构化表12-11为核对型表格，并清理相邻误插表。")

    broken2 = '<p>水库养殖20世纪50年代末，东海、赣榆县每年在水库投放鱼种，增殖鱼类资源，水库由单纯天然捕捞转向人放天养与捕捞结合。东海县有大小水库96座，素有“百库之县”</p>\n' + PLACEHOLDER + '\n<p>之称。'
    if broken2 in section:
        section = section.replace(broken2, '<p>水库养殖20世纪50年代末，东海、赣榆县每年在水库投放鱼种，增殖鱼类资源，水库由单纯天然捕捞转向人放天养与捕捞结合。东海县有大小水库96座，素有“百库之县”之称。', 1)
        actions.append("清理水库养殖正文“百库之县/之称”分页误占位。")

    fixed = html_text[: match.start()] + heading + section + html_text[match.end():]
    if fixed != html_text:
        HTML_PATH.write_text(fixed, encoding="utf-8")
    after = audit(SECTION_RE.search(fixed).group(2))  # type: ignore[union-attr]
    return actions, before, after


def write_progress(actions: list[str], before: dict[str, int], after: dict[str, int]) -> None:
    action_lines = '\n'.join(f"- {a}" for a in actions) or "- 本次复跑未产生新改动，脚本保持幂等。"
    content = f"""# 第十二卷水产 表格专项阶段一

更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}

## 本轮范围
- 章节：第十二卷 水产。
- 目标：处理表12-1、表12-5、表12-11，并清理正文分页误占位。

## 已完成
{action_lines}

## 统计变化
| 指标 | 修复前 | 修复后 |
| --- | ---: | ---: |
| 第十二卷正文表格占位符 | {before['placeholders']} | {after['placeholders']} |
| 第十二卷结构化表格 | {before['structured_tables']} | {after['structured_tables']} |
| 表12-1出现次数 | {before['table_12_1']} | {after['table_12_1']} |
| 表12-5出现次数 | {before['table_12_5']} | {after['table_12_5']} |
| 表12-11出现次数 | {before['table_12_11']} | {after['table_12_11']} |

## 当场验收
- 对列位清楚度不足的宽表使用核对型结构化表，未臆造缺失列位。
- 正文误占位直接合并断句。
"""
    PROGRESS_PATH.write_text(content, encoding="utf-8")


def update_memory(before: dict[str, int], after: dict[str, int]) -> None:
    entry = f"""
## 2026-06-29 第十二卷水产表格专项阶段一完成

已完成第十二卷水产表格专项第一阶段：

- 新增脚本：`scripts/repair_twelfth_volume_fishery_tables.py`。
- 结构化表12-1、表12-5、表12-11为核对型表格。
- 清理海参增殖、水库养殖两处正文分页误占位。
- 第十二卷正文表格占位符：{before['placeholders']} -> {after['placeholders']}。
- 第十二卷结构化表格：{before['structured_tables']} -> {after['structured_tables']}。
- 已写入进度文档：`output/reports/progress/20260629_第十二卷水产_表格专项阶段一.md`。
"""
    memory = MEMORY_PATH.read_text(encoding="utf-8") if MEMORY_PATH.exists() else ""
    marker = "## 2026-06-29 第十二卷水产表格专项阶段一完成"
    if marker not in memory:
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
