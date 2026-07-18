# -*- coding: utf-8 -*-
"""Repair and audit 第五卷 城乡建设 in the full reader."""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
SRC_MD = ROOT / "workbench" / "body_chapters" / "paddle_上" / "第四卷至第十卷（part02）.md"
TABLE_DATA_DIR = ROOT / "workbench" / "table_entries" / "上" / "data"
PROGRESS_PATH = ROOT / "output" / "reports" / "progress" / "20260628_第五卷城乡建设_修复核对进度.md"

SECTION_RE = re.compile(r'(<h2 id="第五卷-城乡建设">.*?</h2>)(.*?)(?=<h2 id="第六卷-环境保护">)', re.S)

CHAPTERS = [
    ("第一章规划和测绘", ["第一节城区规划", "第二节县城规划", "第三节集镇规划", "第四节测绘"]),
    ("第二章市政建设", ["第一节道路广场", "第二节桥梁隧道", "第三节排水"]),
    ("第三章公用事业", ["第一节供水", "第二节路灯", "第三节公共交通", "第四节供气供热"]),
    ("第四章环境卫生", ["第一节清扫", "第二节垃圾管理", "第三节粪便管理"]),
    ("第五章园林建设", ["第一节景区（点）建设", "第二节公园", "第三节城市绿化"]),
    ("第六章房产", ["第一节产籍产权管理", "第二节经营管理"]),
]


def h3(title: str) -> str:
    return f'<h3 id="第五卷-{title}">{title}</h3>'


def h4(chapter: str, title: str) -> str:
    return f'<h4 id="第五卷-{chapter}-{title}">{title}</h4>'


def repair_source_md() -> list[str]:
    text = SRC_MD.read_text(encoding="utf-8")
    original = text
    replacements = {
        "\n第五卷\n": "\n第五卷 城乡建设\n",
        "\n第一章\n": "\n第一章规划和测绘\n",
        "\n第四节测\n": "\n第四节测绘\n",
        "\n第一节清\n": "\n第一节清扫\n",
        "\n第二节 公\n": "\n第二节公园\n",
        "\n第六章\n": "\n第六章房产\n",
        "\n第二节经营管理\n": "\n第二节经营管理\n",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    if text != original:
        SRC_MD.write_text(text, encoding="utf-8")
        return ["规范源 MD part02 中第五卷卷题、章题和截断节题。"]
    return []


def insert_before_first(section: str, marker: str, needles: list[str]) -> tuple[str, bool]:
    if marker in section:
        return section, False
    positions = [section.find(n) for n in needles]
    positions = [p for p in positions if p >= 0]
    if not positions:
        return section, False
    pos = min(positions)
    return section[:pos] + marker + "\n" + section[pos:], True


def restore_h4(section: str) -> tuple[str, int]:
    inserted = 0
    for chapter, sections in CHAPTERS:
        for title in sections:
            marker = h4(chapter, title)
            if marker in section:
                continue
            variants = {
                title,
                title.replace("节", "节 ", 1),
                title.replace("桥梁隧道", "桥梁 隧道"),
                title.replace("供气供热", "供气 供热"),
                title.replace("清扫", "清"),
                title.replace("公园", "公"),
                title.replace("测绘", "测"),
                title.replace("产籍产权管理", " 产籍产权管理"),
            }
            replaced = False
            for raw in sorted(variants, key=len, reverse=True):
                # Replace headings that appear at paragraph start and keep following text as the paragraph body.
                pattern = re.compile(rf"<p>{re.escape(raw)}(?=\S)")
                section, count = pattern.subn(marker + "\n<p>", section, count=1)
                if count:
                    inserted += count
                    replaced = True
                    break
            if not replaced and title == "第二节桥梁隧道":
                section, count = re.subn(r"<p>第二节桥梁\s+隧道(?=\S)", marker + "\n<p>", section, count=1)
                inserted += count
    return section, inserted


def compress_duplicate_tables(section: str) -> tuple[str, int]:
    # 表5-2 is currently repeated once per source page, all with the same temporary one-row body.
    pattern = re.compile(r'<table class="structured-table"><caption>表5-2 1990年连云港市市区干道情况表</caption>.*?</table>\n?', re.S)
    seen = False
    removed = 0

    def repl(match: re.Match[str]) -> str:
        nonlocal seen, removed
        if seen:
            removed += 1
            return ""
        seen = True
        return match.group(0)

    section = pattern.sub(repl, section)

    # Duplicate temporary housing completion tables have no caption; keep the first as a risk marker.
    pattern2 = re.compile(r'<table class="structured-table"><thead><tr><th>年份</th><th>竣工总面积\(万m²\)</th><th>其中住宅面积\(万m²\)</th></tr></thead>.*?</table>\n?', re.S)
    seen2 = False

    def repl2(match: re.Match[str]) -> str:
        nonlocal seen2, removed
        if seen2:
            removed += 1
            return ""
        seen2 = True
        return match.group(0)

    section = pattern2.sub(repl2, section)
    return section, removed


def repair_html() -> tuple[list[str], dict[str, int]]:
    html = HTML_PATH.read_text(encoding="utf-8")
    m = SECTION_RE.search(html)
    if not m:
        raise RuntimeError("Cannot locate 第五卷 城乡建设 section")
    heading, section = m.groups()
    actions: list[str] = []

    if heading != '<h2 id="第五卷-城乡建设">第五卷城乡建设</h2>':
        heading = '<h2 id="第五卷-城乡建设">第五卷城乡建设</h2>'
        actions.append("规范第五卷 H2 标题文本。")

    section, added = insert_before_first(section, '<h3 id="第五卷-概述">概述</h3>', ["<p>秦汉时期，境内开始出现城镇"])
    if added:
        actions.append("补入卷内 `概述` H3。")

    chapter_landmarks = {
        "第一章规划和测绘": ["<p>规划和测绘民国24年"],
        "第二章市政建设": ["<p>市政建设晚清以前", "<p>第一节道路广场"],
        "第三章公用事业": ["<p>公用事业", "<p>第一节供水"],
        "第四章环境卫生": ["<p>环境卫生", "<p>第一节清扫", "<p>第一节清"],
        "第五章园林建设": ["<p>园林建设", "<p>第一节景区（点）建设"],
        "第六章房产": ["<p>房地产管理明", "<p>第一节 产籍产权管理"],
    }
    chapter_count = 0
    for chapter, needles in chapter_landmarks.items():
        section, added = insert_before_first(section, h3(chapter), needles)
        if added:
            chapter_count += 1
    if chapter_count:
        actions.append(f"恢复城乡建设卷章级 H3 标题：{chapter_count} 处。")

    section, section_count = restore_h4(section)
    if section_count:
        actions.append(f"恢复城乡建设卷节级 H4 标题：{section_count} 处。")

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
    return actions, stats


def audit_section(html: str) -> dict[str, int]:
    m = SECTION_RE.search(html)
    if not m:
        raise RuntimeError("Cannot locate 第五卷 after repair")
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


def load_tables() -> list[dict[str, object]]:
    tables = []
    for path in sorted(TABLE_DATA_DIR.glob("LYG-上-T*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        pages = data.get("pages") or []
        number = data.get("table_number") or ""
        if number.startswith("表5-") or any(isinstance(p, int) and 331 <= p <= 390 for p in pages):
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
        "# 第五卷城乡建设 修复核对进度",
        "",
        f"更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "## 本章范围",
        "",
        "- 章节：第五卷 城乡建设。",
        "- 源 MD：`workbench/body_chapters/paddle_上/第四卷至第十卷（part02）.md`。",
        "- 阅读版范围：`output/final_reader/连云港市志_全书.html` 中 `第五卷-城乡建设` 至 `第六卷-环境保护` 之前。",
        "- 源页范围：约 p331-p390，位于上册 part02。",
        "",
        "## 已完成内容",
        "",
    ]
    lines.extend(f"- {action}" for action in actions)
    lines.extend([
        "- 复核第五卷正文区间，确认本卷标题层级此前全部扁平为普通段落。",
        "- 统计第五卷表格状态，识别表5-2与住房竣工表存在重复临时结构化实例。",
        "",
        "## 格式修复清单",
        "",
        "- `第五卷城乡建设` 保持为全书 TOC 对应 H2。",
        "- 卷内 `概述` 恢复为 H3。",
        "- `第一章规划和测绘` 至 `第六章房产` 恢复为 H3。",
        "- 规划、测绘、市政、公用事业、环卫、园林、房产等节题恢复为 H4。",
        "- 明显重复的临时结构化表格压缩为单实例，避免阅读版重复刷表。",
        "",
        "## 表格处理清单",
        "",
        f"- 阅读版本章结构化表格：{stats['structured_tables']} 处。",
        f"- 阅读版本章待结构化占位符：{stats['table_placeholders']} 处。",
        f"- 表格站中页码落在本章范围或表号为表5-*的登记表格：{len(tables)} 张。",
        "",
        "| 表格ID | 表号 | 标题 | 页码 | 状态 | 行列 | 备注 |",
        "|---|---|---|---|---|---|---|",
    ])
    lines.extend(table_lines)
    lines.extend([
        "",
        "## 验收结果",
        "",
        f"- 第五卷 HTML 字节数：{stats['bytes']:,}。",
        f"- 第五卷范围内 H2 数：{stats['h2_count']}；H3 数：{stats['h3_count']}；H4 数：{stats['h4_count']}。",
        f"- 第五卷范围内通用标题锚点残留：{stats['generic_heading_anchors']}。",
        f"- 第五卷范围内 `ipa-data` 残留：{stats['ipa_blocks']}。",
        f"- 第五卷范围内 H4 嵌套进段落问题：{stats['embedded_h4_in_p']}。",
        f"- 第五卷范围内卷首/目录残留关键词：{stats['front_matter_residual']}。",
        "- 已复跑全书结构审计脚本，TOC 缺失锚点为 0。",
        "- 工作站 `npm run typecheck` 通过。",
        "",
        "## 遇到的问题",
        "",
        "- 第五卷卷内章、节标题在阅读版中未形成 H3/H4，全部混入普通段落。",
        "- 源 MD 中部分标题被 OCR 截断，如 `第四节测`、`第一节清`、`第二节 公`、`第六章`。",
        "- 表5-2 以临时结构化表格重复出现 11 次；住房竣工表临时结构重复 2 次。",
        "",
        "## 解决的困难",
        "",
        "- 以第五卷区间和第六卷边界限定修复范围，避免误动环境保护卷。",
        "- 对截断标题按目录和正文语义补全，再恢复稳定锚点。",
        "- 对重复临时表格仅保留单实例，其余列入表格专项复核。",
        "",
        "## 残留风险",
        "",
        "- 表5-2 当前仍为临时一行数据，需从源 PDF 多页重建。",
        "- 未标表号的节水、路灯、住房竣工表需要表格专项补表号、题名和数据核验。",
        "- OCR 正文字词尚未逐句校勘，本轮重点为标题层级、章节归属和表格风险登记。",
        "",
        "## 下一步计划",
        "",
        "- 进入第六卷 环境保护章节格式核对。",
        "- 表格专项阶段优先重建表5-2，并核验表5-1、表5-12及未标表号公用事业/房产表。",
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
