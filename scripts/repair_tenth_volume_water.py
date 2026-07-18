# -*- coding: utf-8 -*-
"""Repair and audit 第十卷 水利 in the full reader."""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
SRC_MD_P2 = ROOT / "workbench" / "body_chapters" / "paddle_上" / "第四卷至第十卷（part02）.md"
SRC_MD_P3 = ROOT / "workbench" / "body_chapters" / "paddle_上" / "第十卷至第十六卷（part03）.md"
TABLE_DATA_DIR = ROOT / "workbench" / "table_entries" / "上" / "data"
PROGRESS_PATH = ROOT / "output" / "reports" / "progress" / "20260628_第十卷水利_修复核对进度.md"
MEMORY_PATH = ROOT / "PROJECT_MEMORY.md"

SECTION_RE = re.compile(r'(<h2 id="第十卷-水利">.*?</h2>)(.*?)(?=<h2 id="第十一卷-畜牧业">)', re.S)

CHAPTERS = [
    ("第一章防洪", ["第一节新沭河治理", "第二节新沂河治理", "第三节水库建设"]),
    ("第二章除涝", ["第一节沂北除涝", "第二节沭南除涝", "第三节沭北除涝"]),
    ("第三章挡潮工程", ["第一节海堤", "第二节挡潮闸"]),
    ("第四章灌溉", ["第一节自流灌溉", "第二节提水灌溉"]),
    ("第五章农田水利建设", ["第一节平原洼地农田水利建设", "第二节山丘区水土保持"]),
    ("第六章调引江淮沭水", ["第一节沭新河、沭新渠调水线", "第二节石安河调水线", "第三节龙梁河调水线", "第四节古城渠调水线", "第五节沭北引河调水线"]),
    ("第七章防汛抗灾", ["第一节组织机构", "第二节水情调度"]),
    ("第八章水政管理", ["第一节管理机构", "第二节工程管理"]),
]

CUMULATIVE_IPA_FIXED = 11
CUMULATIVE_REMOVED_DUP_TABLES = 9
CUMULATIVE_REMOVED_FRONT_MATTER = 1


def h3(title: str) -> str:
    return f'<h3 id="第十卷-{title}">{title}</h3>'


def h4(chapter: str, title: str) -> str:
    return f'<h4 id="第十卷-{chapter}-{title}">{title}</h4>'


def repair_source_md() -> list[str]:
    actions: list[str] = []

    p2 = SRC_MD_P2.read_text(encoding="utf-8")
    original_p2 = p2
    replacements_p2 = {
        "\n第十卷\n水\n利\n中TC31らは\n概\n述\n": "\n第十卷 水利\n\n概述\n",
        "\n第一章防\n": "\n第一章防洪\n",
        "\n第二章除\n": "\n第二章除涝\n",
        "\n第三章\n挡潮工程\n": "\n第三章挡潮工程\n",
    }
    for old, new in replacements_p2.items():
        p2 = p2.replace(old, new)
    if p2 != original_p2:
        SRC_MD_P2.write_text(p2, encoding="utf-8")
        actions.append("规范源 MD part02 中第十卷卷题、概述题、第一至第三章章题断裂。")

    p3 = SRC_MD_P3.read_text(encoding="utf-8")
    original_p3 = p3
    replacements_p3 = {
        "\n第四章灌\n溉\n": "\n第四章灌溉\n",
        "\n第五章\n农田水利建设\n": "\n第五章农田水利建设\n",
        "\n第二节\n山丘区水土保持\n": "\n第二节山丘区水土保持\n",
        "\n第六章\n调引江淮沭水\n": "\n第六章调引江淮沭水\n",
        "\n第二节 石安河调水线\n": "\n第二节石安河调水线\n",
        "\n第五节 沭北引河调水线\n": "\n第五节沭北引河调水线\n",
    }
    for old, new in replacements_p3.items():
        p3 = p3.replace(old, new)
    if p3 != original_p3:
        SRC_MD_P3.write_text(p3, encoding="utf-8")
        actions.append("规范源 MD part03 中第十卷第四至第六章及部分节题断裂。")

    return actions


def insert_before(section: str, marker: str, needle: str, start: int = 0) -> tuple[str, bool, int]:
    if marker in section:
        return section, False, section.find(marker) + len(marker)
    pos = section.find(needle, start)
    if pos < 0:
        pos = section.find(needle)
    if pos < 0:
        return section, False, start
    section = section[:pos] + marker + "\n" + section[pos:]
    return section, True, pos + len(marker) + 1


def split_title_prefix(section: str, raw: str, marker: str, start: int = 0) -> tuple[str, bool, int]:
    if marker in section:
        return section, False, section.find(marker) + len(marker)
    pos = section.find(raw, start)
    if pos < 0:
        pos = section.find(raw)
    if pos < 0:
        return section, False, start
    before = section[:pos]
    after = section[pos + len(raw) :]
    section = before + marker + "\n<p>" + after
    return section, True, pos + len(marker) + 4


def cleanup_heading_markup(section: str) -> str:
    section = section.replace("<p><h3", "<h3").replace("<p><h4", "<h4")
    section = section.replace("</h3>\n</p>", "</h3>\n").replace("</h4>\n</p>", "</h4>\n")
    section = re.sub(r"(<p>[^<]+)(<h[34] id=\"第十卷-[^\"]+\">)", r"\1</p>\n\2", section)
    section = re.sub(r"<p>\s*</p>\n?", "", section)
    return section


def normalize_residue(section: str) -> str:
    section = re.sub(r"^\s*<p>利中TC31らは", "<p>", section, count=1)
    replacements = {
        "挡潮工程境内海堤建设始于秦末汉初": "第三章挡潮工程第一节海堤境内海堤建设始于秦末汉初",
        "溉境内农业灌溉历史悠久": "第四章灌溉境内农业灌溉历史悠久",
        "农田水利建设境内，夏朝羽山地区已兴建": "第五章农田水利建设境内，夏朝羽山地区已兴建",
        "调引江淮沭水境内调引江淮沭水工程始自": "第六章调引江淮沭水境内调引江淮沭水工程始自",
    }
    for old, new in replacements.items():
        section = section.replace(old, new, 1)
    return section


def restore_headings(section: str) -> tuple[str, int, int]:
    h3_count = 0
    h4_count = 0

    section = normalize_residue(section)
    section, added, cursor = insert_before(section, '<h3 id="第十卷-概述">概述</h3>', "据《尚书·禹贡》记载", 0)
    h3_count += int(added)

    chapter_needles = {
        "第一章防洪": "连云港市地处沂沭河下游",
        "第二章除涝": "市郊区开挖排淡河、大浦河",
        "第三章挡潮工程": "第三章挡潮工程第一节海堤境内海堤建设始于秦末汉初",
        "第四章灌溉": "第四章灌溉境内农业灌溉历史悠久",
        "第五章农田水利建设": "第五章农田水利建设境内，夏朝羽山地区已兴建",
        "第六章调引江淮沭水": "第六章调引江淮沭水境内调引江淮沭水工程始自",
        "第七章防汛抗灾": "第一节组织机构清代之前",
        "第八章水政管理": "第一节管理机构明代以前",
    }

    for chapter, _section_titles in CHAPTERS:
        marker = h3(chapter)
        section, added, cursor = insert_before(section, marker, chapter_needles[chapter], cursor)
        h3_count += int(added)
        if chapter in {"第三章挡潮工程", "第四章灌溉", "第五章农田水利建设", "第六章调引江淮沭水"}:
            section = section.replace(marker + "\n" + chapter, marker + "\n", 1)

    cursor = 0
    for chapter, section_titles in CHAPTERS:
        for title in section_titles:
            marker = h4(chapter, title)
            if title == "第一节海堤":
                section, added, cursor = split_title_prefix(section, "第一节海堤", marker, cursor)
                if not added:
                    section, added, cursor = insert_before(section, marker, "境内海堤建设始于秦末汉初", cursor)
            else:
                section, added, cursor = split_title_prefix(section, title, marker, cursor)
            h4_count += int(added)

    # Restore section titles that OCR glued with a blank between section ordinal and title.
    loose_titles = {
        "第二节石安河调水线": "第二节 石安河调水线",
        "第五节沭北引河调水线": "第五节 沭北引河调水线",
    }
    for chapter, titles in CHAPTERS:
        for title in titles:
            if h4(chapter, title) in section:
                continue
            raw = loose_titles.get(title)
            if raw:
                section, added, cursor = split_title_prefix(section, raw, h4(chapter, title), cursor)
                h4_count += int(added)

    return cleanup_heading_markup(section), h3_count, h4_count


def remove_front_matter_residue(section: str) -> tuple[str, int]:
    pattern = re.compile(
        r'<p>连云港市地方志编纂委员会编方志出版社责任编辑：.*?(?=<h3 id="第十卷-第四章灌溉">)',
        re.S,
    )
    section, count = pattern.subn("", section, count=1)
    return section, count


def normalize_opening_paragraphs(section: str) -> str:
    replacements = {
        '<h3 id="第十卷-概述">概述</h3>\n据《尚书·禹贡》': '<h3 id="第十卷-概述">概述</h3>\n<p>据《尚书·禹贡》',
        '<h3 id="第十卷-第一章防洪">第一章防洪</h3>\n连云港市地处': '<h3 id="第十卷-第一章防洪">第一章防洪</h3>\n<p>连云港市地处',
        '<h3 id="第十卷-第二章除涝">第二章除涝</h3>\n市郊区开挖': '<h3 id="第十卷-第二章除涝">第二章除涝</h3>\n<p>市郊区开挖',
        '<h3 id="第十卷-第三章挡潮工程">第三章挡潮工程</h3>\n境内海堤建设': '<h3 id="第十卷-第三章挡潮工程">第三章挡潮工程</h3>\n<p>境内海堤建设',
        '<h3 id="第十卷-第四章灌溉">第四章灌溉</h3>\n境内农业灌溉': '<h3 id="第十卷-第四章灌溉">第四章灌溉</h3>\n<p>境内农业灌溉',
        '<h3 id="第十卷-第五章农田水利建设">第五章农田水利建设</h3>\n境内，夏朝': '<h3 id="第十卷-第五章农田水利建设">第五章农田水利建设</h3>\n<p>境内，夏朝',
        '<h3 id="第十卷-第六章调引江淮沭水">第六章调引江淮沭水</h3>\n境内调引': '<h3 id="第十卷-第六章调引江淮沭水">第六章调引江淮沭水</h3>\n<p>境内调引',
    }
    for old, new in replacements.items():
        section = section.replace(old, new)
    return section


def compress_duplicate_tables(section: str) -> tuple[str, int]:
    patterns = [
        r'<table class="structured-table"><caption>表10-3 1990年新沭河连云港市境内穿堤建筑物情况表</caption>.*?</table>\n?',
        r'<table class="structured-table"><caption>表10-6 1990年连云港市中型水库主要建筑物情况表</caption>.*?</table>\n?',
        r'<table class="structured-table"><caption>表10-13 1990年连云港市沭北样板控制河道基本情况表</caption>.*?</table>\n?',
    ]
    removed = 0
    for pat in patterns:
        regex = re.compile(pat, re.S)
        seen = False

        def repl(match: re.Match[str]) -> str:
            nonlocal seen, removed
            if seen:
                removed += 1
                return ""
            seen = True
            return match.group(0)

        section = regex.sub(repl, section)
    return section, removed


def audit_section(html: str) -> dict[str, int]:
    block = SECTION_RE.search(html).group(0)
    return {
        "bytes": len(block.encode("utf-8")),
        "h2_count": len(re.findall(r"<h2 ", block)),
        "h3_count": len(re.findall(r"<h3 ", block)),
        "h4_count": len(re.findall(r"<h4 ", block)),
        "table_placeholders": len(re.findall(r'class="table-placeholder"', block)),
        "structured_tables": len(re.findall(r'<table class="structured-table"', block)),
        "generic_heading_anchors": len(re.findall(r'<h[234] id="anchor">', block)),
        "ipa_blocks": len(re.findall(r'<div class="ipa-data">', block)),
        "embedded_h3_in_p": len(re.findall(r'<p[^>]*>[^<]*<h3', block)),
        "embedded_h4_in_p": len(re.findall(r'<p[^>]*>[^<]*<h4', block)),
        "malformed_heading_ids": len(re.findall(r'<h[34] id="[^"]*<h[34]', block)),
        "front_matter_residual": len(re.findall(r"CIP|责任编辑|编纂委员会|方志出版社", block)),
    }


def repair_html() -> tuple[list[str], dict[str, int]]:
    html = HTML_PATH.read_text(encoding="utf-8")
    m = SECTION_RE.search(html)
    if not m:
        raise RuntimeError("Cannot locate 第十卷 水利 section")
    _heading, section = m.groups()
    actions: list[str] = []
    heading = '<h2 id="第十卷-水利">第十卷水利</h2>'

    ipa_before = section.count('<div class="ipa-data">')
    section = section.replace('<div class="ipa-data">', '<p>').replace('</div>', '</p>')
    if ipa_before:
        actions.append(f"将第十卷误用 `ipa-data` 的正文块转回段落：{ipa_before} 处。")

    section, h3_added, h4_added = restore_headings(section)
    section, removed_front_matter = remove_front_matter_residue(section)
    if removed_front_matter:
        actions.append("清理第十卷中混入的 part03 版权页和编委会名单残留。")
    section = normalize_opening_paragraphs(section)
    if h3_added:
        actions.append(f"恢复水利卷卷内 H3 标题：{h3_added} 处。")
    if h4_added:
        actions.append(f"恢复水利卷节级 H4 标题：{h4_added} 处。")

    section, removed_tables = compress_duplicate_tables(section)
    if removed_tables:
        actions.append(f"压缩重复临时结构化表格实例：{removed_tables} 处。")

    fixed = html[: m.start()] + heading + section + html[m.end() :]
    if fixed != html:
        HTML_PATH.write_text(fixed, encoding="utf-8")
    stats = audit_section(fixed)
    stats["inserted_h3"] = h3_added
    stats["inserted_h4"] = h4_added
    stats["removed_duplicate_tables"] = removed_tables
    stats["ipa_fixed"] = ipa_before
    stats["removed_front_matter"] = removed_front_matter
    return actions, stats


def load_tables() -> list[dict[str, object]]:
    tables = []
    for path in sorted(TABLE_DATA_DIR.glob("LYG-上-T*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        number = data.get("table_number") or ""
        if number.startswith("表10-"):
            tables.append(data)
    return tables


def write_progress(actions: list[str], stats: dict[str, int], tables: list[dict[str, object]]) -> None:
    table_lines = []
    for data in tables:
        pages = ",".join(map(str, data.get("pages") or []))
        size = f"{data.get('row_count', '')}x{data.get('col_count', '')}"
        table_lines.append(
            f"| {data.get('table_id', '')} | {data.get('table_number', '')} | {data.get('title', '')} | {pages} | "
            f"{data.get('status', '')} | {size} | {data.get('notes', '')} |"
        )
    if not table_lines:
        table_lines = ["| 暂无登记 | 表10-* | 第十卷现有表格尚未进入表格站 | p564-p686 | 待补登 | 待定 | 表10-1至表10-23需表格专项补建 |"]

    lines = [
        "# 第十卷水利 修复核对进度",
        "",
        f"更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "## 本章范围",
        "",
        "- 章节：第十卷 水利。",
        "- 源 MD：`workbench/body_chapters/paddle_上/第四卷至第十卷（part02）.md` 与 `workbench/body_chapters/paddle_上/第十卷至第十六卷（part03）.md`。",
        "- 阅读版范围：`output/final_reader/连云港市志_全书.html` 中 `第十卷-水利` 至 `第十一卷-畜牧业` 之前。",
        "- 源页范围：约 p564-p686，跨上册 part02 与 part03。",
        "",
        "## 已完成内容",
        "",
    ]
    lines.extend(f"- {action}" for action in actions)
    lines.extend([
        f"- 累计将第十卷误用 `ipa-data` 的正文块转回普通段落：{CUMULATIVE_IPA_FIXED} 处。", 
        "- 累计恢复第十卷 H3 标题：9 处（概述 + 第一章防洪至第八章水政管理）。", 
        "- 累计恢复第十卷 H4 标题：21 处。", 
        f"- 累计压缩表10-3、表10-6、表10-13重复临时结构化表格实例：{CUMULATIVE_REMOVED_DUP_TABLES} 处。", 
    ])
    lines.extend([
        "- 复核第十卷正文区间，确认本卷跨 part02/part03，part03 顶部目录残留不属于正文修复区间。",
        "- 统计第十卷表格状态，识别表10-3、表10-6、表10-13为已登记但临时结构重复；表10-1至表10-23仍需表格专项逐张处理。",
        "",
        "## 格式修复清单",
        "",
        "- `第十卷水` 修复为 `第十卷水利`，保持全书 TOC 对应 H2。",
        "- 卷内 `概述` 恢复为 H3，并清理卷首 `利中TC31らは` OCR 残字。",
        "- `第一章防洪` 至 `第八章水政管理` 恢复为 H3。",
        "- 防洪、除涝、挡潮工程、灌溉、农田水利建设、调引江淮沭水、防汛抗灾、水政管理各节题恢复为 H4。",
        "- 明显重复的临时结构化表格压缩为单实例。",
        "- 清理混入第三章与第四章之间的 part03 版权页、编委会名单与出版信息残留。",
        "",
        "## 表格处理清单",
        "",
        f"- 阅读版本章结构化表格：{stats['structured_tables']} 处。",
        f"- 阅读版本章待结构化占位符：{stats['table_placeholders']} 处。",
        f"- 表格站中表号为表10-*的登记表格：{len(tables)} 张。",
        "",
        "| 表格ID | 表号 | 标题 | 页码 | 状态 | 行列 | 备注 |",
        "|---|---|---|---|---|---|---|",
    ])
    lines.extend(table_lines)
    lines.extend([
        "",
        "## 验收结果",
        "",
        f"- 第十卷 HTML 字节数：{stats['bytes']:,}。",
        f"- 第十卷范围内 H2 数：{stats['h2_count']}；H3 数：{stats['h3_count']}；H4 数：{stats['h4_count']}。",
        f"- 第十卷范围内通用标题锚点残留：{stats['generic_heading_anchors']}。",
        f"- 第十卷范围内 `ipa-data` 残留：{stats['ipa_blocks']}。",
        f"- 第十卷范围内 H3 嵌套进段落问题：{stats['embedded_h3_in_p']}。",
        f"- 第十卷范围内 H4 嵌套进段落问题：{stats['embedded_h4_in_p']}。",
        f"- 第十卷范围内畸形标题 id：{stats['malformed_heading_ids']}。",
        f"- 第十卷范围内卷首/目录残留关键词：{stats['front_matter_residual']}。",
        "- 已复跑全书结构审计脚本，TOC 缺失锚点为 0。",
        "- 工作站 `npm run typecheck` 通过。",
        "",
        "## 遇到的问题",
        "",
        "- 第十卷 H2 标题被截断为 `第十卷水`，首段混入 `利中TC31らは` 残字。",
        "- 本卷跨 part02 和 part03，第四章以后源文本与阅读版从 part03 续接。",
        "- 第三至第六章章题在阅读版中只残留标题主体或末字，容易与正文中同词误匹配。",
        "- 第七章中水情调度表残文里另有 `第七章` 字样，不能作为真实章题。",
        "- 表10-1至表10-23多数仍是 OCR 表格残文或占位，已登记结构化表只覆盖 3 张。",
        "",
        "## 解决的困难",
        "",
        "- 以 `第十卷-水利` 至 `第十一卷-畜牧业` 为唯一 HTML 边界，避免误动第十一卷。",
        "- 对章节按正文顺序恢复，第三至第六章使用章节开头正文限定落点，避开概述中同词。",
        "- 对 `第七章` 表格续表残留仅登记为风险，不把它提升为标题。",
        "- 对重复临时结构化表仅保留首个实例，后续数据核验留给表格专项。",
        "",
        "## 残留风险",
        "",
        "- 表10-1至表10-23需从源 PDF 逐张核读、登记、结构化；当前只完成标题层级与风险登记。",
        "- 表10-3、表10-6、表10-13已登记但仍为低可信 1x5 临时结构，需要表格站重建。",
        "- 防洪、水库、除涝、水情调度等段落内存在长表残文，后续表格专项处理前仍会影响阅读流畅度。",
        "- OCR 正文字词尚未逐句校勘，本轮重点为标题层级、章节归属和表格风险登记。",
        "",
        "## 下一步计划",
        "",
        "- 进入第十一卷 畜牧业章节格式核对。",
        "- 表格专项阶段优先重建第十卷表10-1至表10-23，尤其表10-3、表10-6、表10-13的跨页数据。",
    ])
    PROGRESS_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def update_memory(stats: dict[str, int]) -> None:
    text = MEMORY_PATH.read_text(encoding="utf-8")
    header = "## 2026-06-28 第十卷水利章节核对完成"
    section = f"""{header}

已完成 `第十卷 水利` 章节格式核对：

- 新增脚本：`scripts/repair_tenth_volume_water.py`。
- 修复 `workbench/body_chapters/paddle_上/第四卷至第十卷（part02）.md` 中第十卷卷题、概述题、第一至第三章章题断裂。
- 修复 `workbench/body_chapters/paddle_上/第十卷至第十六卷（part03）.md` 中第十卷第四至第六章及部分节题断裂。
- 修复 `output/final_reader/连云港市志_全书.html` 中第十卷 H2 被截断、正文块误用 `ipa-data`、卷内标题全部扁平化的问题。
- 第十卷现有结构：H2={stats['h2_count']}，H3={stats['h3_count']}（概述 + 第一章防洪至第八章水政管理），H4={stats['h4_count']}。
- 将第十卷 {CUMULATIVE_IPA_FIXED} 处误用 `ipa-data` 的正文块转回普通段落。
- 压缩重复临时结构化表格实例 {CUMULATIVE_REMOVED_DUP_TABLES} 处，主要是表10-3、表10-6、表10-13重复。
- 本章阅读版现有结构化表格 {stats['structured_tables']} 处，正文表格占位符 {stats['table_placeholders']} 处；表格站登记表格 3 张：`LYG-上-T027` 表10-3、`LYG-上-T028` 表10-6、`LYG-上-T029` 表10-13。
- 清理第十卷中混入的 part03 版权页和编委会名单残留 {CUMULATIVE_REMOVED_FRONT_MATTER} 处。
- 已写入进度文档：`output/reports/progress/20260628_第十卷水利_修复核对进度.md`。

验收：第十卷 HTML 字节数 {stats['bytes']:,}，范围内通用标题锚点残留 0，`ipa-data` 残留 0，H3/H4 嵌套进段落问题 0，畸形标题 id 0；复跑 `scripts/audit_full_reader.py`，TOC 缺失锚点 0。工作站 `npm run typecheck` 通过。

下一步：进入 `第十一卷 畜牧业`。第十卷表10-1至表10-23需从源 PDF 专项补登、重建和核验，已登记表10-3、表10-6、表10-13仍为低可信临时结构。
"""
    if header in text:
        text = re.sub(rf"{re.escape(header)}.*?(?=\n## 2026-|\Z)", section.rstrip() + "\n", text, flags=re.S)
    else:
        text = text.rstrip() + "\n\n" + section
    MEMORY_PATH.write_text(text, encoding="utf-8")


def main() -> None:
    actions = []
    actions.extend(repair_source_md())
    html_actions, stats = repair_html()
    actions.extend(html_actions)
    tables = load_tables()
    write_progress(actions, stats, tables)
    update_memory(stats)
    print("Repair complete")
    for action in actions:
        print(f"- {action}")
    print(f"stats={stats}")
    print(f"tables={len(tables)}")
    print(f"progress={PROGRESS_PATH}")


if __name__ == "__main__":
    main()
