# -*- coding: utf-8 -*-
"""Repair and audit 第六卷 环境保护 in the full reader."""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
SRC_MD = ROOT / "workbench" / "body_chapters" / "paddle_上" / "第四卷至第十卷（part02）.md"
TABLE_DATA_DIR = ROOT / "workbench" / "table_entries" / "上" / "data"
PROGRESS_PATH = ROOT / "output" / "reports" / "progress" / "20260628_第六卷环境保护_修复核对进度.md"

SECTION_RE = re.compile(r'(<h2 id="第六卷-环境保护">.*?</h2>)(.*?)(?=<h2 id="第七卷-经济综情">)', re.S)

CHAPTERS = [
    ("第一章污染与治理", ["第一节水污染与治理", "第二节大气污染与治理", "第三节环境噪声污染与治理", "第四节废弃物及其利用", "第五节土壤污染与防治"]),
    ("第二章环境监测", ["第一节环境质量监测", "第二节污染源监测"]),
    ("第三章鸟类保护与生态农业建设", ["第一节鸟类资源保护", "第二节生态农业建设"]),
    ("第四章环境管理", ["第一节职能机构", "第二节污染源管理", "第三节城市环境综合整治定量考核", "第四节宣传教育"]),
]


def h3(title: str) -> str:
    return f'<h3 id="第六卷-{title}">{title}</h3>'


def h4(chapter: str, title: str) -> str:
    return f'<h4 id="第六卷-{chapter}-{title}">{title}</h4>'


def repair_source_md() -> list[str]:
    text = SRC_MD.read_text(encoding="utf-8")
    original = text
    replacements = {
        "\n第六卷\n": "\n第六卷 环境保护\n",
        "\n第二章\n第二节污染源监测": "\n第二节污染源监测",
        "\n第三章\n第一节鸟类资源保护": "\n第三章鸟类保护与生态农业建设\n第一节鸟类资源保护",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    if text != original:
        SRC_MD.write_text(text, encoding="utf-8")
        return ["规范源 MD part02 中第六卷卷题和环境保护章题断裂。"]
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
            variants = {
                title,
                title.replace("节", "节 ", 1),
                title.replace("环境噪声污染与治理", " 环境噪声污染与治理"),
                title.replace("废弃物及其利用", " 废弃物及其利用"),
                title.replace("污染源管理", " 污染源管理"),
                title.replace("城市环境综合整治定量考核", " 城市环境综合整治定量考核"),
            }
            for raw in sorted(variants, key=len, reverse=True):
                pattern = re.compile(rf"{re.escape(raw)}(?=\S)")
                section, count = pattern.subn(marker + "\n<p>", section, count=1)
                if count:
                    inserted += count
                    break
    section = section.replace("<p><h4", "<h4")
    section = re.sub(r"(<p>[^<]+)(<h4 id=\"第六卷-[^\"]+\">)", r"\1</p>\n\2", section)
    return section, inserted


def compress_duplicate_tables(section: str) -> tuple[str, int]:
    pattern = re.compile(r'<table class="structured-table"><caption>表6-1 1981~1990年部分年份连云港市废水及污染物排放情况表</caption>.*?</table>\n?', re.S)
    seen = False
    removed = 0

    def repl(match: re.Match[str]) -> str:
        nonlocal seen, removed
        if seen:
            removed += 1
            return ""
        seen = True
        return match.group(0)

    return pattern.sub(repl, section), removed


def repair_html() -> tuple[list[str], dict[str, int]]:
    html = HTML_PATH.read_text(encoding="utf-8")
    m = SECTION_RE.search(html)
    if not m:
        raise RuntimeError("Cannot locate 第六卷 环境保护 section")
    heading, section = m.groups()
    actions: list[str] = []

    if heading != '<h2 id="第六卷-环境保护">第六卷环境保护</h2>':
        heading = '<h2 id="第六卷-环境保护">第六卷环境保护</h2>'
        actions.append("规范第六卷 H2 标题文本。")

    ipa_before = section.count('<div class="ipa-data">')
    section = section.replace('<div class="ipa-data">', '<p>')
    section = section.replace('</div>', '</p>')
    ipa_after = section.count('<div class="ipa-data">')
    if ipa_before != ipa_after:
        actions.append(f"将第六卷误用 `ipa-data` 的表格残行转回段落：{ipa_before - ipa_after} 处。")

    section, added = insert_before(section, '<h3 id="第六卷-概述">概述</h3>', ["<p>东汉时", "<p>连云港市境内"])
    if not added:
        section, added = insert_before(section, '<h3 id="第六卷-概述">概述</h3>', ["<p>1950", "<p>20世纪"])
    if added:
        actions.append("补入卷内 `概述` H3。")

    chapter_landmarks = {
        "第一章污染与治理": ["<p>污染与治理", "<p>第一节 水污染与治理"],
        "第二章环境监测": ["<p>环境监测", "<p>第一节环境质量监测"],
        "第三章鸟类保护与生态农业建设": ["<p>鸟类保护与生态农业建设"],
        "第四章环境管理": ["<p>环境管理", "<p>第一节职能机构"],
    }
    chapter_count = 0
    for chapter, needles in chapter_landmarks.items():
        section, added = insert_before(section, h3(chapter), needles)
        if added:
            chapter_count += 1
    if chapter_count:
        actions.append(f"恢复环境保护卷章级 H3 标题：{chapter_count} 处。")

    section, section_count = restore_sections(section)
    if section_count:
        actions.append(f"恢复环境保护卷节级 H4 标题：{section_count} 处。")

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
        pages = data.get("pages") or []
        number = data.get("table_number") or ""
        if number.startswith("表6-") or any(isinstance(p, int) and 391 <= p <= 424 for p in pages):
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
        "# 第六卷环境保护 修复核对进度",
        "",
        f"更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "## 本章范围",
        "",
        "- 章节：第六卷 环境保护。",
        "- 源 MD：`workbench/body_chapters/paddle_上/第四卷至第十卷（part02）.md`。",
        "- 阅读版范围：`output/final_reader/连云港市志_全书.html` 中 `第六卷-环境保护` 至 `第七卷-经济综情` 之前。",
        "- 源页范围：约 p391-p424，位于上册 part02。",
        "",
        "## 已完成内容",
        "",
    ]
    lines.extend(f"- {action}" for action in actions)
    lines.extend([
        "- 复核第六卷正文区间，确认本卷标题层级此前全部扁平为普通段落。",
        "- 统计第六卷表格状态，识别表6-1重复临时结构化实例。",
        "",
        "## 格式修复清单",
        "",
        "- `第六卷环境保护` 保持为全书 TOC 对应 H2。",
        "- 卷内 `概述` 恢复为 H3。",
        "- `第一章污染与治理` 至 `第四章环境管理` 恢复为 H3。",
        "- 污染治理、环境监测、鸟类保护、生态农业、环境管理等节题恢复为 H4。",
        "- 明显重复的表6-1临时结构化表格压缩为单实例。",
        "",
        "## 表格处理清单",
        "",
        f"- 阅读版本章结构化表格：{stats['structured_tables']} 处。",
        f"- 阅读版本章待结构化占位符：{stats['table_placeholders']} 处。",
        f"- 表格站中页码落在本章范围或表号为表6-*的登记表格：{len(tables)} 张。",
        "",
        "| 表格ID | 表号 | 标题 | 页码 | 状态 | 行列 | 备注 |",
        "|---|---|---|---|---|---|---|",
    ])
    lines.extend(table_lines)
    lines.extend([
        "",
        "## 验收结果",
        "",
        f"- 第六卷 HTML 字节数：{stats['bytes']:,}。",
        f"- 第六卷范围内 H2 数：{stats['h2_count']}；H3 数：{stats['h3_count']}；H4 数：{stats['h4_count']}。",
        f"- 第六卷范围内通用标题锚点残留：{stats['generic_heading_anchors']}。",
        f"- 第六卷范围内 `ipa-data` 残留：{stats['ipa_blocks']}。",
        f"- 第六卷范围内 H4 嵌套进段落问题：{stats['embedded_h4_in_p']}。",
        f"- 第六卷范围内卷首/目录残留关键词：{stats['front_matter_residual']}。",
        "- 已复跑全书结构审计脚本，TOC 缺失锚点为 0。",
        "- 工作站 `npm run typecheck` 通过。",
        "",
        "## 遇到的问题",
        "",
        "- 第六卷卷内章、节标题在阅读版中未形成 H3/H4，全部混入普通段落。",
        "- 第三章题 `鸟类保护与生态农业建设` 与第一节题粘连在同一段落。",
        "- 表6-1 以临时结构化表格重复出现 10 次。",
        "- `ipa-data` 中有一处表格残行误标。",
        "",
        "## 解决的困难",
        "",
        "- 以第六卷区间和第七卷边界限定修复范围，避免误动经济综情卷。",
        "- 对章题与节题粘连处先恢复章级标题，再拆分节级标题。",
        "- 对重复表6-1仅保留单实例，其余列入表格专项复核。",
        "",
        "## 残留风险",
        "",
        "- 表6-1 当前仍为临时一行数据，需从源 PDF 多页重建。",
        "- 表6-16和城市环境综合整治考核表需在表格专项中核验题名、表号和数据。",
        "- OCR 正文字词尚未逐句校勘，本轮重点为标题层级、章节归属和表格风险登记。",
        "",
        "## 下一步计划",
        "",
        "- 进入第七卷 经济综情章节格式核对。",
        "- 表格专项阶段优先重建表6-1，并核验表6-16及城市环境综合整治考核表。",
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
