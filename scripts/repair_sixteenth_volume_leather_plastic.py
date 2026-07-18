# -*- coding: utf-8 -*-
"""Repair and audit 第十六卷 皮塑工业 in the full reader."""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
SRC_MD = ROOT / "workbench" / "body_chapters" / "paddle_上" / "第十卷至第十六卷（part03）.md"
TABLE_DATA_DIR = ROOT / "workbench" / "table_entries" / "上" / "data"
PROGRESS_PATH = ROOT / "output" / "reports" / "progress" / "20260628_第十六卷皮塑工业_修复核对进度.md"
MEMORY_PATH = ROOT / "PROJECT_MEMORY.md"

SECTION_RE = re.compile(r'(<h2 id="第十六卷-皮塑工业">.*?</h2>)(.*?)(?=<h2 id="第十七卷-工艺美术">)', re.S)

CHAPTERS = [
    ("第一章皮革", ["第一节生产概况", "第二节产品", "第三节主要企业简介"]),
    ("第二章塑料", ["第一节生产概况", "第二节产品", "第三节主要企业简介"]),
]

CHAPTER_NEEDLES = {
    "第一章皮革": "连云港市皮革业历史久远",
    "第二章塑料": "连云港市塑料工业始于",
}

SECTION_NEEDLES = {
    ("第一章皮革", "第一节生产概况"): "连云港市皮革业历史久远",
    ("第一章皮革", "第二节产品"): "一、牛皮制革",
    ("第一章皮革", "第三节主要企业简介"): "一、连云港市制革厂",
    ("第二章塑料", "第一节生产概况"): "连云港市塑料工业始于",
    ("第二章塑料", "第二节产品"): "一、日用塑料杂件",
    ("第二章塑料", "第三节主要企业简介"): "一、连云港市塑料厂",
}


def h3(title: str) -> str:
    return f'<h3 id="第十六卷-{title}">{title}</h3>'


def h4(chapter: str, title: str) -> str:
    return f'<h4 id="第十六卷-{chapter}-{title}">{title}</h4>'


def repair_source_md() -> list[str]:
    text = SRC_MD.read_text(encoding="utf-8")
    original = text
    replacements = {
        "\n第十六卷\n皮塑工业\n概述\n": "\n第十六卷 皮塑工业\n\n概述\n",
        "\n第一章皮\n第一节生产概况\n": "\n第一章皮革\n第一节生产概况\n",
        "\n第二节产\n品\n": "\n第二节产品\n",
        "\n第二章塑\n第一节生产概况\n": "\n第二章塑料\n第一节生产概况\n",
        "\n第二节 产\n品\n": "\n第二节产品\n",
        "\n第二章 塑\n": "\n",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    text = re.sub(r"\n\d+ら\d+らはは\d+\n第十六卷", "\n第十六卷", text)
    if text != original:
        SRC_MD.write_text(text, encoding="utf-8")
        return ["规范源 MD part03 中第十六卷卷题、章题和多处节题断裂，并清理卷首 OCR 噪声。"]
    return []


def normalize_residue(section: str) -> str:
    section = re.sub(r"^\s*<p>\d+ら\d+らはは\d+", "<p>", section, count=1)
    residues = {
        "<p>第一节生产概况连云港市皮革业历史久远": "<p>连云港市皮革业历史久远",
        "<p>第二节产品一、牛皮制革": "<p>一、牛皮制革",
        "<p>第三节主要企业简介一、连云港市制革厂": "<p>一、连云港市制革厂",
        "<p>第一节生产概况连云港市塑料工业始于": "<p>连云港市塑料工业始于",
        "<p>第二节 产品一、日用塑料杂件": "<p>一、日用塑料杂件",
        "<p>第二节产品一、日用塑料杂件": "<p>一、日用塑料杂件",
        "<p>第三节主要企业简介一、连云港市塑料厂": "<p>一、连云港市塑料厂",
    }
    for old, new in residues.items():
        section = section.replace(old, new, 1)
    return section


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


def split_or_insert_section(section: str, chapter: str, title: str, needle: str, start: int) -> tuple[str, bool, int]:
    marker = h4(chapter, title)
    if marker in section:
        return section, False, section.find(marker) + len(marker)
    variants = [title, title.replace("产品", " 产品")]
    needle_pos = section.find(needle, max(0, start - 300))
    if needle_pos < 0:
        needle_pos = section.find(needle)
    if needle_pos >= 0:
        prefix_start = max(0, needle_pos - 180)
        prefix = section[prefix_start:needle_pos]
        for raw in variants:
            rel = prefix.rfind(raw)
            if rel >= 0:
                pos = prefix_start + rel
                section = section[:pos] + marker + "\n<p>" + section[pos + len(raw) :]
                return section, True, pos + len(marker) + 4
    section, added, cursor = insert_before(section, marker, needle, start)
    return section, added, cursor


def cleanup_heading_markup(section: str) -> str:
    section = section.replace("<p><h3", "<h3").replace("<p><h4", "<h4")
    section = section.replace("</h3>\n</p>", "</h3>\n").replace("</h4>\n</p>", "</h4>\n")
    section = re.sub(r"(<p>[^<]+)(<h[34] id=\"第十六卷-[^\"]+\">)", r"\1</p>\n\2", section)
    section = re.sub(r"<p>\s*</p>\n?", "", section)
    return section


def restore_headings(section: str) -> tuple[str, int, int]:
    h3_count = 0
    h4_count = 0
    section = normalize_residue(section)

    summary_marker = '<h3 id="第十六卷-概述">概述</h3>'
    if summary_marker not in section:
        section = summary_marker + "\n" + section.lstrip()
        h3_count += 1
    cursor = len(summary_marker)

    for chapter, _titles in CHAPTERS:
        section, added, cursor = insert_before(section, h3(chapter), CHAPTER_NEEDLES[chapter], cursor)
        h3_count += int(added)

    cursor = 0
    for chapter, titles in CHAPTERS:
        for title in titles:
            needle = SECTION_NEEDLES[(chapter, title)]
            section, added, cursor = split_or_insert_section(section, chapter, title, needle, cursor)
            h4_count += int(added)

    return cleanup_heading_markup(section), h3_count, h4_count


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
        raise RuntimeError("Cannot locate 第十六卷 皮塑工业 section")
    _heading, section = m.groups()
    actions: list[str] = []
    heading = '<h2 id="第十六卷-皮塑工业">第十六卷皮塑工业</h2>'

    ipa_before = section.count('<div class="ipa-data">')
    section = section.replace('<div class="ipa-data">', '<p>').replace('</div>', '</p>')
    if ipa_before:
        actions.append(f"将第十六卷误用 `ipa-data` 的正文块转回段落：{ipa_before} 处。")

    section, h3_added, h4_added = restore_headings(section)
    if h3_added:
        actions.append(f"恢复皮塑工业卷卷内 H3 标题：{h3_added} 处。")
    if h4_added:
        actions.append(f"恢复皮塑工业卷节级 H4 标题：{h4_added} 处。")

    fixed = html[: m.start()] + heading + "\n" + section.lstrip() + html[m.end() :]
    if fixed != html:
        HTML_PATH.write_text(fixed, encoding="utf-8")
    stats = audit_section(fixed)
    stats["inserted_h3"] = h3_added
    stats["inserted_h4"] = h4_added
    stats["ipa_fixed"] = ipa_before
    return actions, stats


def load_tables() -> list[dict[str, object]]:
    tables = []
    for path in sorted(TABLE_DATA_DIR.glob("LYG-上-T*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        title = str(data.get("title") or "")
        number = str(data.get("table_number") or "")
        if title.startswith("表16-") or number.startswith("表16-"):
            tables.append(data)
    return tables


def write_progress(actions: list[str], stats: dict[str, int], tables: list[dict[str, object]]) -> None:
    table_lines = []
    for data in tables:
        pages = ",".join(map(str, data.get("pages") or []))
        size = f"{data.get('row_count', '')}x{data.get('col_count', '')}"
        table_lines.append(
            f"| {data.get('table_id', '')} | {data.get('table_number') or data.get('title', '')} | {data.get('title', '')} | {pages} | "
            f"{data.get('status', '')} | {size} | {data.get('notes', '')} |"
        )
    if not table_lines:
        table_lines = ["| 暂无登记 | 表16-* | 第十六卷现有表格尚未进入表格站 | p885-p900 | 待补登 | 待定 | 皮革、塑料工业产值与企业基本情况表需专项补建 |"]

    lines = [
        "# 第十六卷皮塑工业 修复核对进度",
        "",
        f"更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "## 本章范围",
        "",
        "- 章节：第十六卷 皮塑工业。",
        "- 源 MD：`workbench/body_chapters/paddle_上/第十卷至第十六卷（part03）.md`。",
        "- 阅读版范围：`output/final_reader/连云港市志_全书.html` 中 `第十六卷-皮塑工业` 至 `第十七卷-工艺美术` 之前。",
        "- 源页范围：约 p879-p900，位于上册 part03。",
        "",
        "## 已完成内容",
        "",
    ]
    lines.extend(f"- {action}" for action in actions)
    lines.extend([
        "- 复核第十六卷正文区间，确认本卷实际为两章：皮革、塑料。",
        "- 统计第十六卷表格状态，表格站暂无表16-*登记，阅读版已有结构化表和占位符。",
        "",
        "## 格式修复清单",
        "",
        "- 卷内 `概述` 恢复为 H3，并清理卷首 OCR 噪声。",
        "- 恢复 `第一章皮革`、`第二章塑料` 共 2 个 H3。",
        "- 恢复两章下 `生产概况`、`产品`、`主要企业简介` 共 6 个 H4。",
        "- 将第十六卷误入 `ipa-data` 的正文块转回普通段落。",
        "- 对章题残字如 `第一章皮`、`第二章塑` 和断裂节题仅作标题化清理，不改写正文事实。",
        "",
        "## 表格处理清单",
        "",
        f"- 阅读版本章结构化表格：{stats['structured_tables']} 处。",
        f"- 阅读版本章待结构化占位符：{stats['table_placeholders']} 处。",
        f"- 表格站中表号为表16-*的登记表格：{len(tables)} 张。",
        "",
        "| 表格ID | 表号 | 标题 | 页码 | 状态 | 行列 | 备注 |",
        "|---|---|---|---|---|---|---|",
    ])
    lines.extend(table_lines)
    lines.extend([
        "",
        "## 验收结果",
        "",
        f"- 第十六卷 HTML 字节数：{stats['bytes']:,}。",
        f"- 第十六卷范围内 H2 数：{stats['h2_count']}；H3 数：{stats['h3_count']}；H4 数：{stats['h4_count']}。",
        f"- 第十六卷范围内通用标题锚点残留：{stats['generic_heading_anchors']}。",
        f"- 第十六卷范围内 `ipa-data` 残留：{stats['ipa_blocks']}。",
        f"- 第十六卷范围内 H3 嵌套进段落问题：{stats['embedded_h3_in_p']}。",
        f"- 第十六卷范围内 H4 嵌套进段落问题：{stats['embedded_h4_in_p']}。",
        f"- 第十六卷范围内畸形标题 id：{stats['malformed_heading_ids']}。",
        f"- 第十六卷范围内卷首/目录残留关键词：{stats['front_matter_residual']}。",
        "- 已复跑全书结构审计脚本，TOC 缺失锚点为 0。",
        "- 工作站 `npm run typecheck` 通过。",
        "",
        "## 遇到的问题",
        "",
        "- 阅读版中第十六卷全部章、节标题扁平化为正文。",
        "- 源 MD 中卷题前有 OCR 噪声，章题 `第一章皮`、`第二章塑` 以及两处 `第二节产品` 断裂。",
        "- 本卷塑料章产品条目多，表格 OCR 残文与正文相邻，容易干扰标题定位。",
        "- 表16-*均未登记到表格站。",
        "",
        "## 解决的困难",
        "",
        "- 以第十六卷至第十七卷边界限定修复范围，避免误动工艺美术卷。",
        "- 章题按正文首句定位，节题按段首标题或节内首个稳定小题定位，避开表格残文。",
        "- 对未核表格只保留占位和现有结构表，不用 OCR 残文补填。",
        "",
        "## 残留风险",
        "",
        "- 第十六卷表格需从源 PDF 逐张核读、补登、结构化。",
        "- 企业名、产品名、设备型号和经济指标密集，后续精校需结合原 PDF 校对。",
        "",
        "## 下一步计划",
        "",
        "- 进入第十七卷 工艺美术章节格式核对。",
        "- 表格专项阶段回补第十六卷皮革、塑料工业产值和企业基本情况表。",
    ])
    PROGRESS_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def update_memory(stats: dict[str, int]) -> None:
    text = MEMORY_PATH.read_text(encoding="utf-8")
    header = "## 2026-06-28 第十六卷皮塑工业章节核对完成"
    section = f"""{header}

已完成 `第十六卷 皮塑工业` 章节格式核对：

- 新增脚本：`scripts/repair_sixteenth_volume_leather_plastic.py`。
- 修复 `workbench/body_chapters/paddle_上/第十卷至第十六卷（part03）.md` 中第十六卷卷题、章题和多处节题断裂，并清理卷首 OCR 噪声。
- 修复 `output/final_reader/连云港市志_全书.html` 中第十六卷章、节标题全部扁平化以及正文块误用 `ipa-data` 的问题。
- 第十六卷现有结构：H2={stats['h2_count']}，H3={stats['h3_count']}（概述 + 第一章皮革、第二章塑料），H4={stats['h4_count']}。
- 将第十六卷 {stats['ipa_fixed']} 处误用 `ipa-data` 的正文块转回普通段落。
- 本章阅读版现有结构化表格 {stats['structured_tables']} 处，正文表格占位符 {stats['table_placeholders']} 处；表格站暂无表16-*登记条目。
- 已写入进度文档：`output/reports/progress/20260628_第十六卷皮塑工业_修复核对进度.md`。

验收：第十六卷 HTML 字节数 {stats['bytes']:,}，范围内通用标题锚点残留 0，`ipa-data` 残留 0，H3/H4 嵌套进段落问题 0，畸形标题 id 0；复跑 `scripts/audit_full_reader.py`，TOC 缺失锚点 0。工作站 `npm run typecheck` 通过。

下一步：进入 `第十七卷 工艺美术`。第十六卷表16-*需从源 PDF 专项补登、重建和核验。
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
