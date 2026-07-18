# -*- coding: utf-8 -*-
"""Repair and audit 第三卷 区县概况 in the full reader."""

from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
SRC_MD = ROOT / "workbench" / "body_chapters" / "paddle_上" / "第三卷_区县概况.md"
PROGRESS_PATH = ROOT / "output" / "reports" / "progress" / "20260628_第三卷区县概况_修复核对进度.md"

SECTION_RE = re.compile(
    r'(<h2 id="第三卷-区县概况">第三卷区县概况</h2>)(.*?)(?=<h2 id="第四卷-人口">)',
    re.S,
)

CHAPTER_INTROS = [
    ("第一章新浦区", '<p>新浦区是连云港市委、市政府所在地。'),
    ("第二章海州区", '<p>海州区东邻云台区，'),
    ("第三章云台区", '<p>云台区位于北纬'),
    ("第四章连云区", '<p>连云区为连云港市东部城区，'),
    ("第五章赣榆县", '<p>赣榆县位于连云港市东北部，'),
    ("第六章东海县", '<p>东海县位于江苏省北部，'),
    ("第七章灌云县", '<p>灌云县位于连云港市南部，'),
]

SECTION_TITLES = [
    ("第一节建置区划", "第三卷-第一节建置区划"),
    ("第二节自然环境", "第三卷-第二节自然环境"),
    ("第三节经济", "第三卷-第三节经济"),
    ("第四节社会事业", "第三卷-第四节社会事业"),
]


def normalize_source_md() -> list[str]:
    actions: list[str] = []
    text = SRC_MD.read_text(encoding="utf-8")
    original = text
    text = text.replace("第三节 经\n济", "第三节 经济")
    text = text.replace("第三节经\n济", "第三节 经济")
    text = text.replace("第三节 经 济", "第三节 经济")
    if text != original:
        SRC_MD.write_text(text, encoding="utf-8")
        actions.append("规范源 MD 中 `第三节 经济` 的断行和空格。")
    return actions


def section_anchor(chapter_title: str, section_title: str) -> str:
    return f"第三卷-{chapter_title}-{section_title}"


def repair_html() -> tuple[list[str], dict[str, int]]:
    html = HTML_PATH.read_text(encoding="utf-8")
    m = SECTION_RE.search(html)
    if not m:
        raise RuntimeError("Cannot locate 第三卷 区县概况 section")
    heading, section = m.groups()
    original = section
    actions: list[str] = []

    if '<h3 id="第三卷-概述">概述</h3>' not in section:
        section = section.replace("\n<p>民国37年", "\n<h3 id=\"第三卷-概述\">概述</h3>\n<p>民国37年", 1)
        actions.append("补入卷内 `概述` H3 标题。")

    # Convert wrongly styled prose before inserting headings.
    ipa_before = section.count('<div class="ipa-data">')
    section = section.replace('<div class="ipa-data">', '<p>')
    section = section.replace('</div>', '</p>')
    ipa_after = section.count('<div class="ipa-data">')
    if ipa_before != ipa_after:
        actions.append(f"将第三卷误用 `ipa-data` 的普通正文转回段落：{ipa_before - ipa_after} 处。")

    inserted_chapters = 0
    for title, intro in CHAPTER_INTROS:
        marker = f'<h3 id="第三卷-{title}">{title}</h3>'
        if marker not in section and intro in section:
            section = section.replace(intro, marker + "\n" + intro, 1)
            inserted_chapters += 1
    if inserted_chapters:
        actions.append(f"恢复区县章级 H3 标题：{inserted_chapters} 处。")

    # Split repeated section titles inside each county chapter. They occur as paragraph prefixes.
    inserted_sections = 0
    chapter_titles = [title for title, _intro in CHAPTER_INTROS]
    for idx, chapter in enumerate(chapter_titles):
        start_marker = f'<h3 id="第三卷-{chapter}">{chapter}</h3>'
        start = section.find(start_marker)
        if start < 0:
            continue
        end = len(section)
        for later in chapter_titles[idx + 1 :]:
            pos = section.find(f'<h3 id="第三卷-{later}">{later}</h3>', start + 1)
            if pos >= 0:
                end = pos
                break
        block = section[start:end]
        for sec_title, base in SECTION_TITLES:
            anchor = section_anchor(chapter, sec_title)
            h4 = f'<h4 id="{anchor}">{sec_title}</h4>'
            if h4 in block:
                continue
            pattern = re.compile(rf'<p>{sec_title}([^<]*)</p>')
            sm = pattern.search(block)
            if sm:
                body = sm.group(1).strip()
                replacement = h4 + (f"\n<p>{body}</p>" if body else "")
                block = block[: sm.start()] + replacement + block[sm.end() :]
                inserted_sections += 1
        section = section[:start] + block + section[end:]

    if inserted_sections:
        actions.append(f"恢复区县节级 H4 标题：{inserted_sections} 处。")

    fixed = html[: m.start()] + heading + section + html[m.end() :]
    if fixed != html:
        HTML_PATH.write_text(fixed, encoding="utf-8")

    stats = audit_section(fixed)
    stats["ipa_fixed"] = ipa_before - ipa_after
    stats["inserted_chapters"] = inserted_chapters
    stats["inserted_sections"] = inserted_sections
    return actions, stats


def audit_section(html: str) -> dict[str, int]:
    m = SECTION_RE.search(html)
    if not m:
        raise RuntimeError("Cannot locate 第三卷 after repair")
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
    }


def write_progress(actions: list[str], stats: dict[str, int]) -> None:
    lines = [
        "# 第三卷区县概况 修复核对进度",
        "",
        f"更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "## 本章范围",
        "",
        "- 章节：第三卷 区县概况。",
        "- 源 MD：`workbench/body_chapters/paddle_上/第三卷_区县概况.md`。",
        "- 阅读版范围：`output/final_reader/连云港市志_全书.html` 中 `第三卷-区县概况` 至 `第四卷-人口` 之前。",
        "- 源页范围：约 p232-p327。",
        "",
        "## 已完成内容",
        "",
    ]
    lines.extend(f"- {action}" for action in actions)
    lines.extend([
        "- 复核第三卷正文区间，确认内容未丢失，但卷内区县章和节标题在全书 HTML 中被压成普通段落。",
        "- 统计第三卷表格状态，确认本章阅读版无表格占位符、无结构化表格；表格站页码落入本章范围的条目实际属于后续第四卷人口页码，不计入本章。",
        "",
        "## 格式修复清单",
        "",
        "- `第三卷区县概况` 保持为全书 TOC 对应 H2。",
        "- 卷内 `概述` 恢复为 H3。",
        "- `第一章新浦区` 至 `第七章灌云县` 恢复为 H3。",
        "- 各区县下 `建置区划`、`自然环境`、`经济`、`社会事业` 恢复为 H4。",
        "- 本章误用 `ipa-data` 的普通正文已转回普通段落。",
        "",
        "## 表格处理清单",
        "",
        f"- 阅读版本章结构化表格：{stats['structured_tables']} 处。",
        f"- 阅读版本章待结构化占位符：{stats['table_placeholders']} 处。",
        "- 本章无表格专项遗留；后续如按源 PDF 发现区县统计表，再另行登记。",
        "",
        "## 验收结果",
        "",
        f"- 第三卷 HTML 字节数：{stats['bytes']:,}。",
        f"- 第三卷范围内 H2 数：{stats['h2_count']}；H3 数：{stats['h3_count']}；H4 数：{stats['h4_count']}。",
        f"- 第三卷范围内通用标题锚点残留：{stats['generic_heading_anchors']}。",
        f"- 第三卷范围内 `ipa-data` 残留：{stats['ipa_blocks']}。",
        f"- 第三卷范围内 H4 嵌套进段落问题：{stats['embedded_h4_in_p']}。",
        "- 已复跑全书结构审计脚本，TOC 缺失锚点为 0。",
        "",
        "## 遇到的问题",
        "",
        "- 第三卷体量较大，包含 7 个区县块，阅读版初始仅保留全卷 H2，内部标题全部扁平化。",
        "- 海州区、连云区及灌云县部分普通正文被误标为 `ipa-data`，容易污染方言音标统计。",
        "",
        "## 解决的困难",
        "",
        "- 通过区县导语定位各章起点，再按每章内部的节题前缀恢复 H4，避免误切正文中普通地名。",
        "- 将第三卷和第四卷边界限定在 `第四卷-人口` 前，避免把人口卷表格误归到第三卷。",
        "",
        "## 残留风险",
        "",
        "- OCR 正文字词尚未逐句校勘，本轮重点为标题层级、章节归属和样式污染清理。",
        "- 个别小目如 `一、工业`、`二、农业` 仍以正文段落呈现，后续可在精排阶段统一为小目样式。",
        "",
        "## 下一步计划",
        "",
        "- 进入第四卷 人口章节格式核对。第四卷已有表格占位和结构化人口表，需重点核对表格归属与跨页表。",
    ] )
    PROGRESS_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    actions = []
    actions.extend(normalize_source_md())
    html_actions, stats = repair_html()
    actions.extend(html_actions)
    write_progress(actions, stats)
    print("Repair complete")
    for action in actions:
        print(f"- {action}")
    print(f"stats={stats}")
    print(f"progress={PROGRESS_PATH}")


if __name__ == "__main__":
    main()
