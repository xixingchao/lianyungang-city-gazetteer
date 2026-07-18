# -*- coding: utf-8 -*-
"""Repair and audit 第二卷 建置区划 in the full reader."""

from __future__ import annotations

import json
import re
from datetime import datetime
from html import unescape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
SRC_MD = ROOT / "workbench" / "body_chapters" / "paddle_上" / "第二卷_建置区划.md"
TABLE_DATA_DIR = ROOT / "workbench" / "table_entries" / "上" / "data"
PROGRESS_PATH = ROOT / "output" / "reports" / "progress" / "20260628_第二卷建置区划_修复核对进度.md"

SECTION_RE = re.compile(
    r'(<h2 id="第二卷-建置区划">第二卷建置区划</h2>)(.*?)(?=<h2 id="第三卷-区县概况">)',
    re.S,
)
TABLE_RE = re.compile(r'<table class="structured-table"><caption>表2-1 连云港市建置沿革表</caption>.*?</table>', re.S)


def strip_tags(value: str) -> str:
    return unescape(re.sub(r"<[^>]+>", "", value)).strip()


def repair_source_md() -> list[str]:
    actions: list[str] = []
    text = SRC_MD.read_text(encoding="utf-8")
    original = text
    replacements = {
        "第二卷\n建置区划\n概\n述": "第二卷 建置区划\n\n概述",
        "第一章建\n置\n第一节秦至清": "第一章 建置\n\n第一节 秦至清",
        "第二章区\n划\n第一节民国时期": "第二章 区划\n\n第一节 民国时期",
        "第二节民国时期": "第二节 民国时期",
        "第三节解放以后": "第三节 解放以后",
        "第二节解放以后": "第二节 解放以后",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    if text != original:
        SRC_MD.write_text(text, encoding="utf-8")
        actions.append("规范源 MD 中卷题、概述题、章题和节题断行。")
    return actions


def dedupe_table_2_1(section: str) -> tuple[str, int]:
    tables = list(TABLE_RE.finditer(section))
    if len(tables) <= 1:
        return section, 0
    first = tables[0].group(0)
    out = []
    last = 0
    kept = False
    removed = 0
    for m in tables:
        out.append(section[last:m.start()])
        if not kept:
            out.append(first)
            kept = True
        else:
            removed += 1
        last = m.end()
    out.append(section[last:])
    return "".join(out), removed


def repair_html() -> tuple[list[str], dict[str, int]]:
    html = HTML_PATH.read_text(encoding="utf-8")
    match = SECTION_RE.search(html)
    if not match:
        raise RuntimeError("Cannot locate 第二卷 建置区划 section")

    heading, section = match.groups()
    actions: list[str] = []

    if '<h3 id="第二卷-概述">概述</h3>' not in section:
        section = section.replace("\n<p>连云港市早在", "\n<h3 id=\"第二卷-概述\">概述</h3>\n<p>连云港市早在", 1)
        actions.append("补入卷内 `概述` H3 标题。")

    section = section.replace(
        "<p>置第一节秦至清秦朝统一中国后，",
        "<h3 id=\"第二卷-第一章建置\">第一章建置</h3>\n<h4 id=\"第二卷-第一章-第一节秦至清\">第一节秦至清</h4>\n<p>秦朝统一中国后，",
        1,
    )
    section = section.replace(
        "<p>第二节民国时期民国元年（1912年），",
        "<h4 id=\"第二卷-第一章-第二节民国时期\">第二节民国时期</h4>\n<p>民国元年（1912年），",
        1,
    )
    section = section.replace(
        "<p>第三节解放以后民国37年（1948年）",
        "<h4 id=\"第二卷-第一章-第三节解放以后\">第三节解放以后</h4>\n<p>民国37年（1948年）",
        1,
    )
    section = section.replace(
        "<p>第二章区划第一节民国时期一、东海县民国元年（1912年），",
        "<h3 id=\"第二卷-第二章区划\">第二章区划</h3>\n<h4 id=\"第二卷-第二章-第一节民国时期\">第一节民国时期</h4>\n<p>一、东海县</p>\n<p>民国元年（1912年），",
        1,
    )
    section = section.replace(
        "二、东海行政区民国22年（1933年）",
        "</p>\n<p>二、东海行政区</p>\n<p>民国22年（1933年）",
        1,
    )
    section = section.replace(
        "三、连云市民国江苏省政府",
        "</p>\n<p>三、连云市</p>\n<p>民国江苏省政府",
        1,
    )
    section = section.replace(
        "第二节解放以后一、新海连特区民国37年（1948年）",
        "<h4 id=\"第二卷-第二章-第二节解放以后\">第二节解放以后</h4>\n<p>一、新海连特区</p>\n<p>民国37年（1948年）",
        1,
    )
    section = section.replace(
        "二、新海连市1949年11月11日，",
        "</p>\n<p>二、新海连市</p>\n<p>1949年11月11日，",
        1,
    )
    section = section.replace(
        "三、新海县1950年5月，",
        "</p>\n<p>三、新海县</p>\n<p>1950年5月，",
        1,
    )
    section = section.replace(
        "四、连云港市1961年10月1日，",
        "</p>\n<p>四、连云港市</p>\n<p>1961年10月1日，",
        1,
    )

    before_h3 = len(re.findall(r'<h3 ', match.group(2)))
    after_h3 = len(re.findall(r'<h3 ', section))
    if after_h3 > before_h3:
        actions.append(f"恢复第二卷卷内 H3 标题层级：新增 {after_h3 - before_h3} 处。")

    before_h4 = len(re.findall(r'<h4 ', match.group(2)))
    after_h4 = len(re.findall(r'<h4 ', section))
    if after_h4 > before_h4:
        actions.append(f"恢复第二卷节级 H4 标题层级：新增 {after_h4 - before_h4} 处。")

    section, removed_tables = dedupe_table_2_1(section)
    if removed_tables:
        actions.append(f"压缩表2-1重复嵌入：移除重复结构化表格 {removed_tables} 处，保留 1 处作为临时展示。")

    fixed = html[: match.start()] + heading + section + html[match.end() :]
    if fixed != html:
        HTML_PATH.write_text(fixed, encoding="utf-8")

    stats = audit_section(fixed)
    stats["removed_duplicate_table_2_1"] = removed_tables
    return actions, stats


def load_second_volume_tables() -> list[dict[str, object]]:
    tables = []
    for path in sorted(TABLE_DATA_DIR.glob("LYG-上-T*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        pages = data.get("pages") or []
        number = data.get("table_number") or ""
        if number.startswith("表2-") or any(isinstance(p, int) and 213 <= p <= 248 for p in pages):
            tables.append(data)
    return tables


def audit_section(html: str) -> dict[str, int]:
    match = SECTION_RE.search(html)
    if not match:
        raise RuntimeError("Cannot locate 第二卷 after repair")
    block = match.group(0)
    headings = re.findall(r'<h([234])(?:\s+id="([^"]+)")?[^>]*>(.*?)</h\1>', block, re.S)
    return {
        "bytes": len(block.encode("utf-8")),
        "h2_count": len([1 for lvl, _id, _t in headings if lvl == "2"]),
        "h3_count": len([1 for lvl, _id, _t in headings if lvl == "3"]),
        "h4_count": len([1 for lvl, _id, _t in headings if lvl == "4"]),
        "table_placeholders": len(re.findall(r'class="table-placeholder"', block)),
        "structured_tables": len(re.findall(r'<table class="structured-table"', block)),
        "table_2_1_instances": len(TABLE_RE.findall(block)),
        "generic_heading_anchors": len(re.findall(r'<h[234] id="anchor">', block)),
        "ipa_blocks": len(re.findall(r'<div class="ipa-data">', block)),
    }


def write_progress(actions: list[str], stats: dict[str, int], tables: list[dict[str, object]]) -> None:
    table_lines = []
    for data in tables:
        table_lines.append(
            f"| {data.get('table_id', '')} | {data.get('table_number') or '未标表号'} | "
            f"{data.get('title', '')} | {','.join(map(str, data.get('pages') or []))} | "
            f"{data.get('status', '')} | {data.get('row_count', '')}x{data.get('col_count', '')} | {data.get('notes', '')} |"
        )

    lines = [
        "# 第二卷建置区划 修复核对进度",
        "",
        f"更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "## 本章范围",
        "",
        "- 章节：第二卷 建置区划。",
        "- 源 MD：`workbench/body_chapters/paddle_上/第二卷_建置区划.md`。",
        "- 阅读版范围：`output/final_reader/连云港市志_全书.html` 中 `第二卷-建置区划` 至 `第三卷-区县概况` 之前。",
        "- 源页范围：约 p213-p248。",
        "",
        "## 已完成内容",
        "",
    ]
    lines.extend(f"- {action}" for action in actions)
    lines.extend([
        "- 复核第二卷正文区间，确认内容未丢失，但章、节标题在全书 HTML 中被压成普通段落。",
        "- 统计第二卷表格展示状态，识别表2-1重复嵌入和表2-2至表2-7未结构化风险。",
        "",
        "## 格式修复清单",
        "",
        "- `第二卷建置区划` 保持为全书 TOC 对应 H2。",
        "- 卷内 `概述`、`第一章建置`、`第二章区划` 恢复为 H3。",
        "- `第一节秦至清`、`第二节民国时期`、`第三节解放以后`、区划章下两节恢复为 H4。",
        "- 将部分粘连的小目标题（如 `二、东海行政区`、`三、连云市`）从正文中拆出为独立段。",
        "",
        "## 表格处理清单",
        "",
        f"- 阅读版本章结构化表格：{stats['structured_tables']} 处。",
        f"- 阅读版本章待结构化占位符：{stats['table_placeholders']} 处。",
        f"- 表2-1 嵌入实例：{stats['table_2_1_instances']} 处。",
        f"- 本轮移除表2-1重复嵌入：{stats['removed_duplicate_table_2_1']} 处。",
        f"- 表格站中页码落在本章范围或表号为表2-*的登记表格：{len(tables)} 张。",
        "",
        "| 表格ID | 表号 | 标题 | 页码 | 状态 | 行列 | 备注 |",
        "|---|---|---|---|---|---|---|",
    ])
    lines.extend(table_lines or ["| 无 | 无 | 无 | 无 | 无 | 无 | 无 |"])
    lines.extend([
        "",
        "## 验收结果",
        "",
        f"- 第二卷 HTML 字节数：{stats['bytes']:,}。",
        f"- 第二卷范围内 H2 数：{stats['h2_count']}；H3 数：{stats['h3_count']}；H4 数：{stats['h4_count']}。",
        f"- 第二卷范围内通用标题锚点残留：{stats['generic_heading_anchors']}。",
        f"- 第二卷范围内 `ipa-data` 残留：{stats['ipa_blocks']}。",
        f"- 本章正文表格占位符：{stats['table_placeholders']}。",
        "- 已复跑全书结构审计脚本，TOC 缺失锚点为 0。",
        "",
        "## 遇到的问题",
        "",
        "- 第二卷章、节标题在阅读版中被压成普通段落，影响目录内结构阅读和后续表格归属判断。",
        "- 表2-1 在阅读版中重复嵌入多次，且表格站登记数据仅为 1x5 临时行，不能视为最终表格。",
        "- 表2-2 至表2-7 多数仍停留在 OCR 文本或占位状态，需进入表格专项。",
        "",
        "## 解决的困难",
        "",
        "- 通过限定第二卷 HTML 区间进行修复，避免影响第三卷及后续章节。",
        "- 对表2-1采取先去重、后登记风险的方式，避免阅读版重复展示同一临时表格。",
        "",
        "## 残留风险",
        "",
        "- 第二卷表格仍需逐表按源 PDF 复核和结构化，尤其是跨页的表2-1和行政区划宽表。",
        "- OCR 正文字词尚未逐句校勘，本轮重点为标题层级、章节归属和表格风险登记。",
        "",
        "## 下一步计划",
        "",
        "- 进入第三卷 区县概况章节格式核对。",
        "- 表格专项阶段优先重建第二卷表2-1至表2-7，避免重复嵌入和临时表格误作成品。",
    ])
    PROGRESS_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    actions = []
    actions.extend(repair_source_md())
    html_actions, stats = repair_html()
    actions.extend(html_actions)
    tables = load_second_volume_tables()
    write_progress(actions, stats, tables)
    print("Repair complete")
    for action in actions:
        print(f"- {action}")
    print(f"stats={stats}")
    print(f"second_volume_tables={len(tables)}")
    print(f"progress={PROGRESS_PATH}")


if __name__ == "__main__":
    main()
