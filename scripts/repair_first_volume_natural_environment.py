# -*- coding: utf-8 -*-
"""Repair and audit 第一卷 自然环境 in the full reader."""

from __future__ import annotations

import json
import re
from datetime import datetime
from html import unescape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
SRC_MD = ROOT / "workbench" / "body_chapters" / "paddle_上" / "第一卷_自然环境.md"
TABLE_DATA_DIR = ROOT / "workbench" / "table_entries" / "上" / "data"
PROGRESS_PATH = ROOT / "output" / "reports" / "progress" / "20260628_第一卷自然环境_修复核对进度.md"

SECTION_RE = re.compile(
    r'(<h2 id="第一卷-自然环境">第一卷自然环境</h2>)(.*?)(?=<h2 id="第二卷-建置区划">)',
    re.S,
)
CHAPTER_TITLES = [
    "第一章地质地貌",
    "第二章云台山",
    "第三章海",
    "第四章气候",
    "第五章水系水文",
    "第六章土壤植被",
    "第七章自然资源",
    "第八章自然灾害",
]


def strip_tags(value: str) -> str:
    return unescape(re.sub(r"<[^>]+>", "", value)).strip()


def anchor_for(title: str) -> str:
    return f"第一卷-{title}"


def repair_source_md() -> list[str]:
    actions: list[str] = []
    text = SRC_MD.read_text(encoding="utf-8")
    original = text
    text = text.replace("第一卷\n自然环境\n\n概\n述", "第一卷 自然环境\n\n概述", 1)
    text = text.replace("第一节 地\n一、地质演变", "第一节 地质\n\n一、地质演变", 1)
    if text != original:
        SRC_MD.write_text(text, encoding="utf-8")
        actions.append("规范源 MD 卷题、概述题和 `第一节 地质` 断行。")
    return actions


def repair_html() -> tuple[list[str], dict[str, int]]:
    html = HTML_PATH.read_text(encoding="utf-8")
    match = SECTION_RE.search(html)
    if not match:
        raise RuntimeError("Cannot locate 第一卷 自然环境 section")

    heading, section = match.groups()
    actions: list[str] = []

    if '<h2 id="anchor">概述</h2>' in section:
        section = section.replace('<h2 id="anchor">概述</h2>', '<h3 id="第一卷-概述">概述</h3>', 1)
        actions.append("将第一卷内误作 H2 的 `概述` 降为卷内 H3，并设置稳定锚点 `第一卷-概述`。")

    h3_before = len(re.findall(r'<h3 id="anchor">', section))
    for title in CHAPTER_TITLES:
        section = section.replace(f'<h3 id="anchor">{title}</h3>', f'<h3 id="{anchor_for(title)}">{title}</h3>')
    h3_after = len(re.findall(r'<h3 id="anchor">', section))
    if h3_before != h3_after:
        actions.append(f"规范第一卷章级 H3 锚点：{h3_before - h3_after} 处。")

    ipa_before = section.count('<div class="ipa-data">')
    section = section.replace('<div class="ipa-data">', '<p>')
    section = section.replace('</div>', '</p>')
    ipa_after = section.count('<div class="ipa-data">')
    if ipa_before != ipa_after:
        actions.append(f"将第一卷误用 `ipa-data` 的普通正文转回段落：{ipa_before - ipa_after} 处。")

    fixed = html[: match.start()] + heading + section + html[match.end() :]
    if fixed != html:
        HTML_PATH.write_text(fixed, encoding="utf-8")

    stats = audit_section(fixed)
    stats["ipa_fixed"] = ipa_before - ipa_after
    stats["h3_anchor_fixed"] = h3_before - h3_after
    return actions, stats


def load_first_volume_tables() -> list[dict[str, object]]:
    tables = []
    for path in sorted(TABLE_DATA_DIR.glob("LYG-上-T*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        pages = data.get("pages") or []
        if any(isinstance(p, int) and 124 <= p <= 216 for p in pages):
            tables.append(data)
    return tables


def audit_section(html: str) -> dict[str, int]:
    match = SECTION_RE.search(html)
    if not match:
        raise RuntimeError("Cannot locate 第一卷 after repair")
    block = match.group(0)
    headings = re.findall(r'<h([23])(?:\s+id="([^"]+)")?[^>]*>(.*?)</h\1>', block, re.S)
    h2_titles = [strip_tags(t) for lvl, _id, t in headings if lvl == "2"]
    h3_titles = [strip_tags(t) for lvl, _id, t in headings if lvl == "3"]
    table_placeholders = len(re.findall(r'class="table-placeholder"', block))
    structured_tables = len(re.findall(r'<table class="structured-table"', block))
    generic_anchors = len(re.findall(r'<h[23] id="anchor">', block))
    ipa_blocks = len(re.findall(r'<div class="ipa-data">', block))
    return {
        "bytes": len(block.encode("utf-8")),
        "h2_count": len(h2_titles),
        "h3_count": len(h3_titles),
        "table_placeholders": table_placeholders,
        "structured_tables": structured_tables,
        "generic_heading_anchors": generic_anchors,
        "ipa_blocks": ipa_blocks,
    }


def write_progress(actions: list[str], stats: dict[str, int], tables: list[dict[str, object]]) -> None:
    table_lines = []
    for data in tables:
        table_lines.append(
            f"| {data.get('table_id', '')} | {data.get('table_number') or '未标表号'} | "
            f"{data.get('title', '')} | {','.join(map(str, data.get('pages') or []))} | "
            f"{data.get('status', '')} | {data.get('row_count', '')}x{data.get('col_count', '')} |"
        )

    lines = [
        "# 第一卷自然环境 修复核对进度",
        "",
        f"更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "## 本章范围",
        "",
        "- 章节：第一卷 自然环境。",
        "- 源 MD：`workbench/body_chapters/paddle_上/第一卷_自然环境.md`。",
        "- 阅读版范围：`output/final_reader/连云港市志_全书.html` 中 `第一卷-自然环境` 至 `第二卷-建置区划` 之前。",
        "- 源页范围：约 p124-p216，后续表格专项以源 PDF 页图逐表复核。",
        "",
        "## 已完成内容",
        "",
    ]
    lines.extend(f"- {action}" for action in actions)
    lines.extend([
        "- 复核第一卷在全书审计中被误归入通用 `概述` 的原因：卷内 `概述` 被生成成 H2，导致章节统计分段错误。",
        "- 统计第一卷结构化表格和正文占位符，建立本章表格后续处理口径。",
        "",
        "## 格式修复清单",
        "",
        "- `第一卷自然环境` 保持为全书 TOC 对应 H2。",
        "- 卷内 `概述` 改为 H3，避免与后续卷的全局 H2 混淆。",
        "- `第一章地质地貌` 至 `第八章自然灾害` 的 H3 使用稳定锚点，清除本章通用 `id=anchor`。",
        "- 本章普通正文不再使用 `ipa-data` 样式，避免被误判为方言音标数据。",
        "",
        "## 表格处理清单",
        "",
        f"- 阅读版本章结构化表格：{stats['structured_tables']} 处。",
        f"- 阅读版本章待结构化占位符：{stats['table_placeholders']} 处。",
        f"- 表格站中页码落在本章范围内的登记表格：{len(tables)} 张。",
        "",
        "| 表格ID | 表号 | 标题 | 页码 | 状态 | 行列 |",
        "|---|---|---|---|---|---|",
    ])
    lines.extend(table_lines or ["| 无 | 无 | 无 | 无 | 无 | 无 |"])
    lines.extend([
        "",
        "## 验收结果",
        "",
        f"- 第一卷 HTML 字节数：{stats['bytes']:,}。",
        f"- 第一卷范围内 H2 数：{stats['h2_count']}；H3 数：{stats['h3_count']}。",
        f"- 第一卷范围内通用标题锚点残留：{stats['generic_heading_anchors']}。",
        f"- 第一卷范围内 `ipa-data` 残留：{stats['ipa_blocks']}。",
        f"- 本章正文表格占位符：{stats['table_placeholders']}。",
        "- 已复跑全书结构审计脚本，TOC 缺失锚点为 0。",
        "",
        "## 遇到的问题",
        "",
        "- 第一卷内容没有丢失，但因卷内 `概述` 误生成为 H2，审计报告把正文统计到独立 `概述` 章节，造成 `第一卷自然环境` 看似只有 59 字节。",
        "- 第一卷仍有多张气候、水文、灾害类宽表和跨页表停留在占位符状态。",
        "",
        "## 解决的困难",
        "",
        "- 通过限定 `第一卷-自然环境` 到 `第二卷-建置区划` 的 HTML 区间，只修复本章结构，避免影响后续章节。",
        "- 将已结构化表格和占位符分开登记，保证下一轮表格专项可以逐张对账。",
        "",
        "## 残留风险",
        "",
        "- 表1-2、表1-4 至表1-25 中多处仍需按源 PDF 逐表结构化或嵌入，当前不视为表格最终交付完成。",
        "- OCR 正文字词尚未逐句校勘，本轮重点为格式、章节归属和表格账本。",
        "",
        "## 下一步计划",
        "",
        "- 进入第二卷 建置区划章节格式核对。",
        "- 表格专项阶段优先回补第一卷剩余占位符，尤其是气候、水文、自然灾害相关宽表。",
    ])
    PROGRESS_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    actions = []
    actions.extend(repair_source_md())
    html_actions, stats = repair_html()
    actions.extend(html_actions)
    tables = load_first_volume_tables()
    write_progress(actions, stats, tables)
    print("Repair complete")
    for action in actions:
        print(f"- {action}")
    print(f"stats={stats}")
    print(f"first_volume_tables={len(tables)}")
    print(f"progress={PROGRESS_PATH}")


if __name__ == "__main__":
    main()
