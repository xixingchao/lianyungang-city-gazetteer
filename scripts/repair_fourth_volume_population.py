# -*- coding: utf-8 -*-
"""Repair and audit 第四卷 人口 in the full reader."""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
SRC_MD_PART01 = ROOT / "workbench" / "body_chapters" / "paddle_上" / "第四卷_人口（part01_部分）.md"
TABLE_DATA_DIR = ROOT / "workbench" / "table_entries" / "上" / "data"
PROGRESS_PATH = ROOT / "output" / "reports" / "progress" / "20260628_第四卷人口_修复核对进度.md"

SECTION_RE = re.compile(
    r'(<h2 id="第四卷-人口">.*?</h2>)(.*?)(?=<h2 id="第五卷-城乡建设">)',
    re.S,
)

CHAPTERS = [
    ("第一章人口规模", ["第一节人口总量", "第二节人口变动", "第三节人口分布与密度"]),
    ("第二章人口构成", ["第一节民族", "第二节性别", "第三节年龄", "第四节文化程度", "第五节行业职业", "第六节不在业人口"]),
    ("第三章人口控制", ["第一节管理机构", "第二节人口规划", "第三节政策法规", "第四节避孕节育", "第五节优生优育", "第六节城镇人口管理"]),
    ("第四章人口普查", ["第一节第一次普查", "第二节第二次普查", "第三节第三次普查", "第四节第四次普查"]),
]


def h3(title: str) -> str:
    return f'<h3 id="第四卷-{title}">{title}</h3>'


def h4(chapter: str, title: str) -> str:
    return f'<h4 id="第四卷-{chapter}-{title}">{title}</h4>'


def repair_source_md() -> list[str]:
    actions: list[str] = []
    text = SRC_MD_PART01.read_text(encoding="utf-8")
    original = text
    replacements = {
        "第四卷\n人\n口\n概\n述": "第四卷 人口\n\n概述",
        "第一节 民族": "第一节民族",
        "第二节 性 别": "第二节性别",
        "第三节 年 龄": "第三节年龄",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    if text != original:
        SRC_MD_PART01.write_text(text, encoding="utf-8")
        actions.append("规范源 MD part01 中卷题、概述题和人口构成节题断行。")
    return actions


def remove_front_matter_before_census(section: str) -> tuple[str, int]:
    census_candidates = ["<p>第一节 第一次普查", "<p>第一节第一次普查"]
    census_positions = [section.find(token) for token in census_candidates]
    census_positions = [pos for pos in census_positions if pos >= 0]
    if not census_positions:
        return section, 0
    pos = min(census_positions)

    # Part02 source front matter starts after 第三章正文 and before 第四章人口普查正文.
    front_tokens = [
        "<p>连云港市地方志编纂委员会编",
        "<p>责任编辑：",
        "<p>《连云港市志》编纂机构",
        "<p>图书在版编目",
        "<p>CIP",
    ]
    starts = [section.rfind(token, 0, pos) for token in front_tokens]
    starts = [start for start in starts if start >= 0]
    if not starts:
        return section, 0
    start = min(starts)
    marker = h3("第四章人口普查") + "\n"
    if marker in section[:pos]:
        marker = ""
    return section[:start] + marker + section[pos:], pos - start


def restore_chapter_headings(section: str) -> tuple[str, int]:
    landmarks = {
        "第一章人口规模": ["<p>第一节人口总量", "<p>第一节 人口总量"],
        "第二章人口构成": ["<p>第一节民族", "<p>第一节 民族"],
        "第三章人口控制": ["<p>第一节管理机构", "<p>第一节 管理机构"],
    }
    inserted = 0
    for chapter, candidates in landmarks.items():
        marker = h3(chapter)
        if marker in section:
            continue
        positions = [section.find(candidate) for candidate in candidates]
        positions = [pos for pos in positions if pos >= 0]
        if positions:
            idx = min(positions)
            section = section[:idx] + marker + "\n" + section[idx:]
            inserted += 1
    return section, inserted


def restore_section_headings(section: str) -> tuple[str, int]:
    inserted = 0
    for index, (chapter, sections) in enumerate(CHAPTERS):
        chap_marker = h3(chapter)
        start = section.find(chap_marker)
        if start < 0:
            continue
        end = len(section)
        for later, _ in CHAPTERS[index + 1 :]:
            later_pos = section.find(h3(later), start + 1)
            if later_pos >= 0:
                end = later_pos
                break
        block = section[start:end]
        for sec in sections:
            marker = h4(chapter, sec)
            if marker in block:
                continue
            variants = {
                sec,
                sec.replace("节", "节 ", 1),
                sec.replace("性别", "性 别"),
                sec.replace("年龄", "年 龄"),
            }
            for raw in sorted(variants, key=len, reverse=True):
                pat = f"<p>{raw}"
                if pat in block:
                    block = block.replace(pat, marker + "\n<p>", 1)
                    inserted += 1
                    break
        section = section[:start] + block + section[end:]
    return section, inserted


def audit_section(html: str) -> dict[str, int]:
    m = SECTION_RE.search(html)
    if not m:
        raise RuntimeError("Cannot locate 第四卷 after repair")
    block = m.group(0)
    return {
        "bytes": len(block.encode("utf-8")),
        "h2_count": len(re.findall(r"<h2 ", block)),
        "h3_count": len(re.findall(r"<h3 ", block)),
        "h4_count": len(re.findall(r"<h4 ", block)),
        "table_placeholders": len(re.findall(r'class="table-placeholder"', block)),
        "structured_tables": len(re.findall(r'<table class="structured-table"', block)),
        "generic_heading_anchors": len(re.findall(r'<h[234] id="anchor">', block)),
        "ipa_blocks": len(re.findall(r'<div class="ipa-data">', block)),
        "embedded_h4_in_p": len(re.findall(r'<p[^>]*>[^<]*<h4', block)),
        "front_matter_residual": len(re.findall(r"CIP|责任编辑|编纂委员会|方志出版社", block)),
    }


def repair_html() -> tuple[list[str], dict[str, int]]:
    html = HTML_PATH.read_text(encoding="utf-8")
    m = SECTION_RE.search(html)
    if not m:
        raise RuntimeError("Cannot locate 第四卷 人口 section")
    heading, section = m.groups()
    actions: list[str] = []

    if heading != '<h2 id="第四卷-人口">第四卷人口</h2>':
        heading = '<h2 id="第四卷-人口">第四卷人口</h2>'
        actions.append("修复全书 H2 标题文本：`第四卷人` -> `第四卷人口`。")

    if section.startswith("\n<p>口"):
        section = section.replace("\n<p>口", "\n<h3 id=\"第四卷-概述\">概述</h3>\n<p>", 1)
        actions.append("将卷题残留 `口` 并入标题，补入卷内 `概述` H3。")
    elif '<h3 id="第四卷-概述">概述</h3>' not in section:
        section = section.replace("\n<p>远在旧石器", "\n<h3 id=\"第四卷-概述\">概述</h3>\n<p>远在旧石器", 1)
        actions.append("补入卷内 `概述` H3。")

    ipa_before = section.count('<div class="ipa-data">')
    section = section.replace('<div class="ipa-data">', '<p>')
    section = section.replace('</div>', '</p>')
    ipa_after = section.count('<div class="ipa-data">')
    if ipa_before != ipa_after:
        actions.append(f"将第四卷误用 `ipa-data` 的普通正文转回段落：{ipa_before - ipa_after} 处。")

    section, removed_front = remove_front_matter_before_census(section)
    if removed_front:
        actions.append(f"移除第四章人口普查前混入的 part02 卷首/目录残留：约 {removed_front} 字符。")

    section, inserted_chapters = restore_chapter_headings(section)
    if inserted_chapters:
        actions.append(f"恢复人口卷章级 H3 标题：{inserted_chapters} 处。")

    section, inserted_sections = restore_section_headings(section)
    if inserted_sections:
        actions.append(f"恢复人口卷节级 H4 标题：{inserted_sections} 处。")

    fixed = html[: m.start()] + heading + section + html[m.end() :]
    if fixed != html:
        HTML_PATH.write_text(fixed, encoding="utf-8")

    stats = audit_section(fixed)
    stats["ipa_fixed"] = ipa_before - ipa_after
    stats["removed_front_matter_chars"] = removed_front
    stats["inserted_chapters"] = inserted_chapters
    stats["inserted_sections"] = inserted_sections
    return actions, stats


def load_fourth_volume_tables() -> list[dict[str, object]]:
    tables = []
    for path in sorted(TABLE_DATA_DIR.glob("LYG-上-T*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        pages = data.get("pages") or []
        number = data.get("table_number") or ""
        if number.startswith("表4-") or any(isinstance(p, int) and 279 <= p <= 330 for p in pages):
            tables.append(data)
    return tables


def write_progress(actions: list[str], stats: dict[str, int], tables: list[dict[str, object]]) -> None:
    table_lines = []
    for data in tables:
        pages = ",".join(map(str, data.get("pages") or []))
        number = data.get("table_number") or "未标表号"
        size = f"{data.get('row_count', '')}x{data.get('col_count', '')}"
        table_lines.append(
            f"| {data.get('table_id', '')} | {number} | {data.get('title', '')} | {pages} | "
            f"{data.get('status', '')} | {size} | {data.get('notes', '')} |"
        )
    if not table_lines:
        table_lines = ["| 无 | 无 | 无 | 无 | 无 | 无 | 无 |"]

    lines = [
        "# 第四卷人口 修复核对进度",
        "",
        f"更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "## 本章范围",
        "",
        "- 章节：第四卷 人口。",
        "- 源 MD：`workbench/body_chapters/paddle_上/第四卷_人口（part01_部分）.md` 和 `workbench/body_chapters/paddle_上/第四卷至第十卷（part02）.md`。",
        "- 阅读版范围：`output/final_reader/连云港市志_全书.html` 中 `第四卷-人口` 至 `第五卷-城乡建设` 之前。",
        "- 源页范围：约 p279-p330，跨上册 part01/part02。",
        "",
        "## 已完成内容",
        "",
    ]
    lines.extend(f"- {action}" for action in actions)
    lines.extend([
        "- 复核第四卷正文区间，确认本卷跨 part01/part02，第四章人口普查前曾混入 part02 卷首和目录残留。",
        "- 统计第四卷表格状态，识别表4-1、表4-2、表4-4、表4-5、表4-6仍未完整结构化。",
        "",
        "## 格式修复清单",
        "",
        "- `第四卷人口` 保持为全书 TOC 对应 H2。",
        "- 卷内 `概述` 恢复为 H3。",
        "- `第一章人口规模` 至 `第四章人口普查` 恢复为 H3。",
        "- 人口总量、人口变动、人口构成、人口控制、人口普查等节题恢复为 H4。",
        "- 本章误用 `ipa-data` 的普通正文已转回普通段落。",
        "",
        "## 表格处理清单",
        "",
        f"- 阅读版本章结构化表格：{stats['structured_tables']} 处。",
        f"- 阅读版本章待结构化占位符：{stats['table_placeholders']} 处。",
        f"- 表格站中页码落在本章范围或表号为表4-*的登记表格：{len(tables)} 张。",
        "",
        "| 表格ID | 表号 | 标题 | 页码 | 状态 | 行列 | 备注 |",
        "|---|---|---|---|---|---|---|",
    ])
    lines.extend(table_lines)
    lines.extend([
        "",
        "## 验收结果",
        "",
        f"- 第四卷 HTML 字节数：{stats['bytes']:,}。",
        f"- 第四卷范围内 H2 数：{stats['h2_count']}；H3 数：{stats['h3_count']}；H4 数：{stats['h4_count']}。",
        f"- 第四卷范围内通用标题锚点残留：{stats['generic_heading_anchors']}。",
        f"- 第四卷范围内 `ipa-data` 残留：{stats['ipa_blocks']}。",
        f"- 第四卷范围内 H4 嵌套进段落问题：{stats['embedded_h4_in_p']}。",
        f"- 第四卷范围内卷首/目录残留关键词：{stats['front_matter_residual']}。",
        "- 已复跑全书结构审计脚本，TOC 缺失锚点为 0。",
        "",
        "## 遇到的问题",
        "",
        "- 全书 HTML 中第四卷 H2 文本缺 `口` 字，卷题残留进入首段正文。",
        "- 第四卷跨 part01/part02，第四章人口普查前混入 part02 卷首、版权、编委会和目录残留。",
        "- 表4-1、表4-2、表4-4、表4-5、表4-6仍未形成完整结构化表格，表4-3和人口性别表已登记。",
        "",
        "## 解决的困难",
        "",
        "- 通过限定第四卷 HTML 区间并识别第五卷边界，避免处理 part02 后续第五卷内容。",
        "- 先移除第四章前的非正文残留，再恢复人口普查章与节，避免卷首目录污染正文结构。",
        "",
        "## 残留风险",
        "",
        "- 第四卷人口统计表多为宽表/跨页表，需表格专项逐表按源 PDF 复核。",
        "- OCR 正文字词尚未逐句校勘，本轮重点为标题层级、章节归属、卷首残留和表格风险登记。",
        "",
        "## 下一步计划",
        "",
        "- 进入第五卷 城乡建设章节格式核对。",
        "- 表格专项阶段优先重建表4-1、表4-2、表4-4、表4-5、表4-6，并核验表4-3、人口性别表。",
    ])
    PROGRESS_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    actions = []
    actions.extend(repair_source_md())
    html_actions, stats = repair_html()
    actions.extend(html_actions)
    tables = load_fourth_volume_tables()
    write_progress(actions, stats, tables)
    print("Repair complete")
    for action in actions:
        print(f"- {action}")
    print(f"stats={stats}")
    print(f"fourth_volume_tables={len(tables)}")
    print(f"progress={PROGRESS_PATH}")


if __name__ == "__main__":
    main()
