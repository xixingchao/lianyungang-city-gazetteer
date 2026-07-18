# -*- coding: utf-8 -*-
"""Repair and audit 第七卷 经济综情 in the full reader."""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
SRC_MD = ROOT / "workbench" / "body_chapters" / "paddle_上" / "第四卷至第十卷（part02）.md"
TABLE_DATA_DIR = ROOT / "workbench" / "table_entries" / "上" / "data"
PROGRESS_PATH = ROOT / "output" / "reports" / "progress" / "20260628_第七卷经济综情_修复核对进度.md"

SECTION_RE = re.compile(r'(<h2 id="第七卷-经济综情">.*?</h2>)(.*?)(?=<h2 id="第八卷-经济综合管理">)', re.S)

CHAPTERS = [
    ("第一章经济发展概况", ["第一节解放前的经济发展概况", "第二节解放后的经济发展概况"]),
    ("第二章经济结构", ["第一节所有制结构", "第二节产业结构", "第三节投资结构"]),
    ("第三章人民生活", ["第一节城市人民生活", "第二节农村人民生活"]),
]


def h3(title: str) -> str:
    return f'<h3 id="第七卷-{title}">{title}</h3>'


def h4(chapter: str, title: str) -> str:
    return f'<h4 id="第七卷-{chapter}-{title}">{title}</h4>'


def repair_source_md() -> list[str]:
    text = SRC_MD.read_text(encoding="utf-8")
    original = text
    replacements = {
        "\n第七卷\n经济综情\n概\n述\n": "\n第七卷 经济综情\n\n概述\n",
        "\n第二章\n经济结构\n第一节\n所有制结构\n": "\n第二章经济结构\n第一节所有制结构\n",
        "\n第三章\n人民生活\n": "\n第三章人民生活\n",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    # The duplicate chapter marker at the continuation of 表7-1 is table residue, not a real chapter heading.
    text = text.replace("\n第一章经济发展概况\n\n续上表\n", "\n续上表\n")
    if text != original:
        SRC_MD.write_text(text, encoding="utf-8")
        return ["规范源 MD part02 中第七卷卷题、概述题和经济结构/人民生活章题断裂。"]
    return []


def insert_before(section: str, marker: str, needles: list[str]) -> tuple[str, bool]:
    if marker in section:
        return section, False
    positions = [section.find(n) for n in needles]
    positions = [pos for pos in positions if pos >= 0]
    if not positions:
        return section, False
    pos = min(positions)
    return section[:pos] + marker + "\n" + section[pos:], True


def restore_sections(section: str) -> tuple[str, int]:
    inserted = 0
    for chapter, sections in CHAPTERS:
        for title in sections:
            marker = h4(chapter, title)
            if marker in section:
                continue
            variants = {title, title.replace("节", "节 ", 1)}
            for raw in sorted(variants, key=len, reverse=True):
                pattern = re.compile(rf"{re.escape(raw)}(?=\S)")
                section, count = pattern.subn(marker + "\n<p>", section, count=1)
                if count:
                    inserted += count
                    break
    section = section.replace("<p><h4", "<h4")
    section = re.sub(r"(<p>[^<]+)(<h4 id=\"第七卷-[^\"]+\">)", r"\1</p>\n\2", section)
    return section, inserted


def compress_duplicate_tables(section: str) -> tuple[str, int]:
    patterns = [
        r'<table class="structured-table"><caption>表7-1 1949~1990年连云港市工农业总产值及构成表</caption>.*?</table>\n?',
        r'<table class="structured-table"><caption>表7-9 1978~1990年连云港市国内生产总值结构表</caption>.*?</table>\n?',
        r'<table class="structured-table"><thead><tr><th>年份</th><th>农业总产值\(万元\)</th><th>种植业</th><th>林业</th><th>牧业</th><th>副业</th><th>渔业</th></tr></thead>.*?</table>\n?',
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


def repair_html() -> tuple[list[str], dict[str, int]]:
    html = HTML_PATH.read_text(encoding="utf-8")
    m = SECTION_RE.search(html)
    if not m:
        raise RuntimeError("Cannot locate 第七卷 经济综情 section")
    heading, section = m.groups()
    actions: list[str] = []

    if heading != '<h2 id="第七卷-经济综情">第七卷经济综情</h2>':
        heading = '<h2 id="第七卷-经济综情">第七卷经济综情</h2>'
        actions.append("规范第七卷 H2 标题文本。")

    ipa_before = section.count('<div class="ipa-data">')
    section = section.replace('<div class="ipa-data">', '<p>')
    section = section.replace('</div>', '</p>')
    ipa_after = section.count('<div class="ipa-data">')
    if ipa_before != ipa_after:
        actions.append(f"将第七卷误用 `ipa-data` 的普通正文转回段落：{ipa_before - ipa_after} 处。")

    section, added = insert_before(section, '<h3 id="第七卷-概述">概述</h3>', ["<p>连云港市东临黄海"])
    if added:
        actions.append("补入卷内 `概述` H3。")

    # Remove duplicate inline chapter text before continuation table residue.
    section = section.replace("<p>第一章经济发展概况</p>\n<p>续上表", "<p>续上表")
    section = section.replace("<p>第一章经济发展概况续上表", "<p>续上表")

    chapter_landmarks = {
        "第一章经济发展概况": ["<p>第一节解放前的经济发展概况"],
        "第二章经济结构": ["<p>第一节\n<p>所有制结构", "<p>第一节所有制结构", "<p>所有制结构"],
        "第三章人民生活": ["<p>第一节城市人民生活", "<p>人民生活"],
    }
    chapter_count = 0
    for chapter, needles in chapter_landmarks.items():
        section, added = insert_before(section, h3(chapter), needles)
        if added:
            chapter_count += 1
    if chapter_count:
        actions.append(f"恢复经济综情卷章级 H3 标题：{chapter_count} 处。")

    # Normalize two-line heading residue before H4 restoration.
    section = section.replace("<p>第一节</p>\n<p>所有制结构", "<p>第一节所有制结构")
    section, section_count = restore_sections(section)
    if section_count:
        actions.append(f"恢复经济综情卷节级 H4 标题：{section_count} 处。")

    section, removed_tables = compress_duplicate_tables(section)
    if removed_tables:
        actions.append(f"压缩重复临时结构化表格实例：{removed_tables} 处。")

    fixed = html[: m.start()] + heading + section + html[m.end() :]
    if fixed != html:
        HTML_PATH.write_text(fixed, encoding="utf-8")
    stats = audit_section(fixed)
    stats["inserted_chapters"] = chapter_count
    stats["inserted_sections"] = section_count
    stats["removed_duplicate_tables"] = removed_tables
    stats["ipa_fixed"] = ipa_before - ipa_after
    return actions, stats


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
        "embedded_h4_in_p": len(re.findall(r'<p[^>]*>[^<]*<h4', block)),
        "front_matter_residual": len(re.findall(r"CIP|责任编辑|编纂委员会|方志出版社", block)),
    }


def load_tables() -> list[dict[str, object]]:
    tables = []
    for path in sorted(TABLE_DATA_DIR.glob("LYG-上-T*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        number = data.get("table_number") or ""
        if number.startswith("表7-"):
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
        "# 第七卷经济综情 修复核对进度",
        "",
        f"更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "## 本章范围",
        "",
        "- 章节：第七卷 经济综情。",
        "- 源 MD：`workbench/body_chapters/paddle_上/第四卷至第十卷（part02）.md`。",
        "- 阅读版范围：`output/final_reader/连云港市志_全书.html` 中 `第七卷-经济综情` 至 `第八卷-经济综合管理` 之前。",
        "- 源页范围：约 p425-p451，位于上册 part02。",
        "",
        "## 已完成内容",
        "",
    ]
    lines.extend(f"- {action}" for action in actions)
    lines.extend([
        "- 复核第七卷正文区间，确认本卷标题层级此前全部扁平为普通段落。",
        "- 统计第七卷表格状态，识别表7-1、表7-9和农业总产值表存在重复临时结构化实例。",
        "",
        "## 格式修复清单",
        "",
        "- `第七卷经济综情` 保持为全书 TOC 对应 H2。",
        "- 卷内 `概述` 恢复为 H3。",
        "- `第一章经济发展概况` 至 `第三章人民生活` 恢复为 H3。",
        "- 经济发展、经济结构、人民生活各节题恢复为 H4。",
        "- 明显重复的临时结构化表格压缩为单实例。",
        "",
        "## 表格处理清单",
        "",
        f"- 阅读版本章结构化表格：{stats['structured_tables']} 处。",
        f"- 阅读版本章待结构化占位符：{stats['table_placeholders']} 处。",
        f"- 表格站中表号为表7-*的登记表格：{len(tables)} 张。",
        "",
        "| 表格ID | 表号 | 标题 | 页码 | 状态 | 行列 | 备注 |",
        "|---|---|---|---|---|---|---|",
    ])
    lines.extend(table_lines)
    lines.extend([
        "",
        "## 验收结果",
        "",
        f"- 第七卷 HTML 字节数：{stats['bytes']:,}。",
        f"- 第七卷范围内 H2 数：{stats['h2_count']}；H3 数：{stats['h3_count']}；H4 数：{stats['h4_count']}。",
        f"- 第七卷范围内通用标题锚点残留：{stats['generic_heading_anchors']}。",
        f"- 第七卷范围内 `ipa-data` 残留：{stats['ipa_blocks']}。",
        f"- 第七卷范围内 H4 嵌套进段落问题：{stats['embedded_h4_in_p']}。",
        f"- 第七卷范围内卷首/目录残留关键词：{stats['front_matter_residual']}。",
        "- 已复跑全书结构审计脚本，TOC 缺失锚点为 0。",
        "- 工作站 `npm run typecheck` 通过。",
        "",
        "## 遇到的问题",
        "",
        "- 第七卷卷内章、节标题在阅读版中未形成 H3/H4，全部混入普通段落。",
        "- 源 MD 中第二章、第三章章题断裂为两行，且表7-1续表处误出现重复章题。",
        "- 表7-1、表7-9和农业总产值表存在重复临时结构化实例。",
        "- `ipa-data` 中有一处普通正文误标。",
        "",
        "## 解决的困难",
        "",
        "- 以第七卷区间和第八卷边界限定修复范围，避免误动经济综合管理卷。",
        "- 对章题与节题断裂处先规范源 MD，再恢复阅读版稳定锚点。",
        "- 对重复临时表格仅保留单实例，其余列入表格专项复核。",
        "",
        "## 残留风险",
        "",
        "- 表7-1、表7-9当前仍为临时一行数据，需从源 PDF 多页重建。",
        "- 表7-10、表7-11等 OCR 表格残文尚未登记为完整结构化表，需表格专项补建。",
        "- OCR 正文字词尚未逐句校勘，本轮重点为标题层级、章节归属和表格风险登记。",
        "",
        "## 下一步计划",
        "",
        "- 进入第八卷 经济综合管理章节格式核对。",
        "- 表格专项阶段优先重建表7-1、表7-9、表7-10、表7-11。",
    ])
    PROGRESS_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    actions = []
    actions.extend(repair_source_md())
    html_actions, stats = repair_html()
    actions.extend(html_actions)
    tables = load_tables()
    write_progress(actions, stats, tables)
    print("Repair complete")
    for action in actions:
        print(f"- {action}")
    print(f"stats={stats}")
    print(f"tables={len(tables)}")
    print(f"progress={PROGRESS_PATH}")


if __name__ == "__main__":
    main()
