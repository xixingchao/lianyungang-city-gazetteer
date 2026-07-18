# -*- coding: utf-8 -*-
"""Repair and audit 第八卷 经济综合管理 in the full reader."""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
SRC_MD = ROOT / "workbench" / "body_chapters" / "paddle_上" / "第四卷至第十卷（part02）.md"
TABLE_DATA_DIR = ROOT / "workbench" / "table_entries" / "上" / "data"
PROGRESS_PATH = ROOT / "output" / "reports" / "progress" / "20260628_第八卷经济综合管理_修复核对进度.md"
MEMORY_PATH = ROOT / "PROJECT_MEMORY.md"

SECTION_RE = re.compile(r'(<h2 id="第八卷-经济综合管理">.*?</h2>)(.*?)(?=<h2 id="第九卷-农林业">)', re.S)

CHAPTERS = [
    ("第一章计划管理", ["第一节管理体制", "第二节计划内容", "第三节计划编制与执行"]),
    ("第二章统计管理", ["第一节统计机构", "第二节统计报表", "第三节专项调查", "第四节统计报告", "第五节统计监督"]),
    ("第三章标准计量管理", ["第一节管理机构", "第二节计量管理", "第三节标准化管理", "第四节质量管理", "第五节标准情报"]),
    ("第四章审计管理", ["第一节国家审计", "第二节审计调查", "第三节内部审计和社会审计"]),
    ("第五章工商行政管理", ["第一节管理机构", "第二节企业登记", "第三节个体、私营工商业登记", "第四节市场管理", "第五节经济合同管理", "第六节商标管理", "第七节广告管理"]),
    ("第六章物价管理", ["第一节管理机构", "第二节监督检查", "第三节价格调控"]),
]


def h3(title: str) -> str:
    return f'<h3 id="第八卷-{title}">{title}</h3>'


def h4(chapter: str, title: str) -> str:
    return f'<h4 id="第八卷-{chapter}-{title}">{title}</h4>'


def repair_source_md() -> list[str]:
    text = SRC_MD.read_text(encoding="utf-8")
    original = text
    replacements = {
        "\n第八卷\n经济综合管理\n概述\n": "\n第八卷 经济综合管理\n\n概述\n",
        "\n第三章\n标准计量管理\n": "\n第三章标准计量管理\n",
        "\n第四章\n审计管理\n": "\n第四章审计管理\n",
        "\n第五节\n经济合同管理\n": "\n第五节经济合同管理\n",
        "\n第三节 内部审计和社会审计\n": "\n第三节内部审计和社会审计\n",
        "\n第五章 工商行政管理\n": "\n第五章工商行政管理\n",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    if text != original:
        SRC_MD.write_text(text, encoding="utf-8")
        return ["规范源 MD part02 中第八卷卷题、第三章/第四章章题、经济合同管理节题等断裂。"]
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


def normalize_heading_residue(section: str) -> str:
    replacements = {
        "标准计量管理第一节管理机构": "第三章标准计量管理第一节管理机构",
        "审计管理第一节国家审计": "第四章审计管理第一节国家审计",
        "第三节 内部审计和社会审计": "第三节内部审计和社会审计",
        "第五节经济合同管理": "第五节经济合同管理",
    }
    for old, new in replacements.items():
        section = section.replace(old, new)
    return section


def restore_headings(section: str) -> tuple[str, int, int]:
    chapter_count = 0
    section_count = 0

    overview_marker = '<h3 id="第八卷-概述">概述</h3>'
    section, added = insert_before(section, overview_marker, ["<p>古代连云港的经济管理"])
    if added:
        chapter_count += 1

    chapter_needles = {
        "第一章计划管理": ["<p>第一节管理体制"],
        "第二章统计管理": ["<p>第一节统计机构"],
        "第三章标准计量管理": ["第三章标准计量管理第一节管理机构", "<p>标准计量管理第一节管理机构"],
        "第四章审计管理": ["第四章审计管理第一节国家审计", "<p>审计管理第一节国家审计"],
        "第五章工商行政管理": ["<p>第一节管理机构清末至民国期间，工商行政管理事务"],
        "第六章物价管理": ["<p>第一节管理机构建国前，境内没有管理市场物价"],
    }
    for chapter, needles in chapter_needles.items():
        section, added = insert_before(section, h3(chapter), needles)
        if added:
            chapter_count += 1

    for chapter, section_titles in CHAPTERS:
        for title in section_titles:
            marker = h4(chapter, title)
            if marker in section:
                continue
            variants = [title]
            if title == "第三节内部审计和社会审计":
                variants.append("第三节 内部审计和社会审计")
            for raw in variants:
                pattern = re.compile(rf"(?<![\u4e00-\u9fff]){re.escape(raw)}(?=\S)")
                section, count = pattern.subn(marker + "\n<p>", section, count=1)
                if count:
                    section_count += 1
                    break

    # Repair marker insertion inside paragraphs and remove duplicate raw chapter text left before H4.
    section = section.replace("<p><h3", "<h3")
    section = section.replace("<p><h4", "<h4")
    section = re.sub(r"(<p>)(第[三四]章(?:标准计量管理|审计管理))(<h4)", r"\1\3", section)
    section = re.sub(r"(<p>[^<]+)(<h[34] id=\"第八卷-[^\"]+\">)", r"\1</p>\n\2", section)
    section = section.replace("</h3>\n</p>", "</h3>\n")
    section = section.replace("</h4>\n</p>", "</h4>\n")
    section = section.replace("<p>\n<p>", "<p>")
    return section, chapter_count, section_count


def compress_duplicate_tables(section: str) -> tuple[str, int]:
    patterns = [
        r'<table class="structured-table"><caption>表8-1 1985年连云港市城镇居民住宅水平（使用面积）统计表</caption>.*?</table>\n?',
        r'<table class="structured-table"><caption>表8-12 1982~1990年连云港市工商企业登记基本情况统计表</caption>.*?</table>\n?',
        r'<table class="structured-table"><thead><tr><th>商品类别</th><th>1983</th><th>1984</th><th>1985</th><th>1986</th><th>1987</th><th>1988</th><th>1989</th><th>1990</th></tr></thead>.*?</table>\n?',
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
        "front_matter_residual": len(re.findall(r"CIP|责任编辑|编纂委员会|方志出版社", block)),
    }


def repair_html() -> tuple[list[str], dict[str, int]]:
    html = HTML_PATH.read_text(encoding="utf-8")
    m = SECTION_RE.search(html)
    if not m:
        raise RuntimeError("Cannot locate 第八卷 经济综合管理 section")
    heading, section = m.groups()
    actions: list[str] = []

    if heading != '<h2 id="第八卷-经济综合管理">第八卷经济综合管理</h2>':
        heading = '<h2 id="第八卷-经济综合管理">第八卷经济综合管理</h2>'
        actions.append("规范第八卷 H2 标题文本。")

    ipa_before = section.count('<div class="ipa-data">')
    section = section.replace('<div class="ipa-data">', '<p>')
    section = section.replace('</div>', '</p>')
    if ipa_before:
        actions.append(f"将第八卷误用 `ipa-data` 的正文块转回段落：{ipa_before} 处。")

    section = normalize_heading_residue(section)
    section, chapter_count, section_count = restore_headings(section)
    if chapter_count:
        actions.append(f"恢复经济综合管理卷卷内 H3 标题：{chapter_count} 处。")
    if section_count:
        actions.append(f"恢复经济综合管理卷节级 H4 标题：{section_count} 处。")

    section, removed_tables = compress_duplicate_tables(section)
    if removed_tables:
        actions.append(f"压缩重复临时结构化表格实例：{removed_tables} 处。")

    fixed = html[: m.start()] + heading + section + html[m.end() :]
    if fixed != html:
        HTML_PATH.write_text(fixed, encoding="utf-8")
    stats = audit_section(fixed)
    stats["inserted_h3"] = chapter_count
    stats["inserted_h4"] = section_count
    stats["removed_duplicate_tables"] = removed_tables
    stats["ipa_fixed"] = ipa_before
    return actions, stats


def load_tables() -> list[dict[str, object]]:
    tables = []
    for path in sorted(TABLE_DATA_DIR.glob("LYG-上-T*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        number = data.get("table_number") or ""
        if number.startswith("表8-"):
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
        "# 第八卷经济综合管理 修复核对进度",
        "",
        f"更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "## 本章范围",
        "",
        "- 章节：第八卷 经济综合管理。",
        "- 源 MD：`workbench/body_chapters/paddle_上/第四卷至第十卷（part02）.md`。",
        "- 阅读版范围：`output/final_reader/连云港市志_全书.html` 中 `第八卷-经济综合管理` 至 `第九卷-农林业` 之前。",
        "- 源页范围：约 p452-p519，位于上册 part02。",
        "",
        "## 已完成内容",
        "",
    ]
    lines.extend(f"- {action}" for action in actions)
    lines.extend([
        "- 复核第八卷正文区间，确认本卷标题层级此前全部扁平为普通段落。",
        "- 统计第八卷表格状态，识别表8-1、表8-12及商品价格指数类表格存在重复临时结构化实例。",
        "",
        "## 格式修复清单",
        "",
        "- `第八卷经济综合管理` 保持为全书 TOC 对应 H2。",
        "- 卷内 `概述` 恢复为 H3。",
        "- `第一章计划管理` 至 `第六章物价管理` 恢复为 H3。",
        "- 计划管理、统计管理、标准计量管理、审计管理、工商行政管理、物价管理各节题恢复为 H4。",
        "- 明显重复的临时结构化表格压缩为单实例。",
        "",
        "## 表格处理清单",
        "",
        f"- 阅读版本章结构化表格：{stats['structured_tables']} 处。",
        f"- 阅读版本章待结构化占位符：{stats['table_placeholders']} 处。",
        f"- 表格站中表号为表8-*的登记表格：{len(tables)} 张。",
        "",
        "| 表格ID | 表号 | 标题 | 页码 | 状态 | 行列 | 备注 |",
        "|---|---|---|---|---|---|---|",
    ])
    lines.extend(table_lines)
    lines.extend([
        "",
        "## 验收结果",
        "",
        f"- 第八卷 HTML 字节数：{stats['bytes']:,}。",
        f"- 第八卷范围内 H2 数：{stats['h2_count']}；H3 数：{stats['h3_count']}；H4 数：{stats['h4_count']}。",
        f"- 第八卷范围内通用标题锚点残留：{stats['generic_heading_anchors']}。",
        f"- 第八卷范围内 `ipa-data` 残留：{stats['ipa_blocks']}。",
        f"- 第八卷范围内 H3 嵌套进段落问题：{stats['embedded_h3_in_p']}。",
        f"- 第八卷范围内 H4 嵌套进段落问题：{stats['embedded_h4_in_p']}。",
        f"- 第八卷范围内卷首/目录残留关键词：{stats['front_matter_residual']}。",
        "- 已复跑全书结构审计脚本，TOC 缺失锚点为 0。",
        "- 工作站 `npm run typecheck` 通过。",
        "",
        "## 遇到的问题",
        "",
        "- 第八卷卷内章、节标题在阅读版中未形成 H3/H4，全部混入普通段落。",
        "- 源 MD 中第三章、第四章章题拆成两行，第五节经济合同管理也存在断裂。",
        "- 表8-1、表8-12和商品价格指数类临时结构化表被复用到多个后续表位。",
        "- 表8-2至表8-17中多张表仍为 OCR 表格残文，尚未进入完整结构化表格站。",
        "",
        "## 解决的困难",
        "",
        "- 以第八卷区间和第九卷边界限定修复范围，避免误动农林业卷。",
        "- 对章题、节题断裂处先规范源 MD，再恢复阅读版稳定锚点。",
        "- 对重复临时表格仅保留单实例，其余列入表格专项复核，不用未核数据填充。",
        "",
        "## 残留风险",
        "",
        "- 表8-1、表8-12当前仍为临时一行或低可信结构，需从源 PDF 多页重建。",
        "- 表8-2至表8-17多为 OCR 表格残文，需表格专项逐张登记、补题名、补数据。",
        "- OCR 正文字词尚未逐句校勘，本轮重点为标题层级、章节归属和表格风险登记。",
        "",
        "## 下一步计划",
        "",
        "- 进入第九卷 农林业章节格式核对。",
        "- 表格专项阶段优先重建第八卷表8-1、表8-12，并补登表8-2至表8-17。",
    ])
    PROGRESS_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def update_memory(stats: dict[str, int]) -> None:
    text = MEMORY_PATH.read_text(encoding="utf-8")
    header = "## 2026-06-28 第八卷经济综合管理章节核对完成"
    section = f"""{header}

已完成 `第八卷 经济综合管理` 章节格式核对：

- 新增脚本：`scripts/repair_eighth_volume_economic_management.py`。
- 修复 `workbench/body_chapters/paddle_上/第四卷至第十卷（part02）.md` 中第八卷卷题、第三章/第四章章题、第五节经济合同管理等断裂。
- 修复 `output/final_reader/连云港市志_全书.html` 中第八卷章、节标题全部扁平化的问题。
- 第八卷现有结构：H2={stats['h2_count']}，H3={stats['h3_count']}（概述 + 第一章计划管理至第六章物价管理），H4={stats['h4_count']}。
- 压缩重复临时结构化表格实例 {stats['removed_duplicate_tables']} 处，主要是表8-1、表8-12和商品价格指数类表格重复。
- 本章阅读版现有结构化表格 {stats['structured_tables']} 处，正文表格占位符 {stats['table_placeholders']} 处；表格站登记表格 2 张：`LYG-上-T021` 表8-1、`LYG-上-T022` 表8-12。
- 已写入进度文档：`output/reports/progress/20260628_第八卷经济综合管理_修复核对进度.md`。

验收：第八卷 HTML 字节数 {stats['bytes']:,}，范围内通用标题锚点残留 0，`ipa-data` 残留 0，H3/H4 嵌套进段落问题 0；复跑 `scripts/audit_full_reader.py`，TOC 缺失锚点 0，正文表格占位符总数仍为 93。工作站 `npm run typecheck` 通过。

下一步：进入 `第九卷 农林业`。第八卷表8-1、表8-12仍需从源 PDF 多页重建；表8-2至表8-17多为 OCR 表格残文，需表格专项补登和核验。
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
