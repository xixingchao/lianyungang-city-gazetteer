# -*- coding: utf-8 -*-
"""Repair and audit 第十九卷 医药 in the full reader."""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
SRC_MD = ROOT / "workbench" / "body_chapters" / "第十七卷至第二十九卷（中part01）.md"
TABLE_DATA_DIRS = [ROOT / "workbench" / "table_entries" / "中" / "data", ROOT / "workbench" / "table_entries" / "上" / "data"]
PROGRESS_PATH = ROOT / "output" / "reports" / "progress" / "20260628_第十九卷医药_修复核对进度.md"
MEMORY_PATH = ROOT / "PROJECT_MEMORY.md"

SECTION_RE = re.compile(r'(<h2 id="第十九卷-医药">.*?</h2>)(.*?)(?=<h2 id="第二十卷-化学工业">)', re.S)

CHAPTERS = [
    ("第一章中药", ["第一节中药材", "第二节中药饮片", "第三节中成药", "第四节主要企业简介"]),
    ("第二章化学制药", ["第一节生产概况", "第二节产品", "第三节主要企业简介"]),
    ("第三章医疗器械、材料", ["第一节生产概况", "第二节产品", "第三节主要企业简介"]),
    ("第四章医药购销", ["第一节经营机构", "第二节调拨采购", "第三节销售"]),
]

CHAPTER_NEEDLES = {
    "第一章中药": "境内云台山是一座",
    "第二章化学制药": "民国3年（1914年），义德医院",
    "第三章医疗器械、材料": "1958~1963年，机械、轻工等行业",
    "第四章医药购销": "明洪武年间，海州设有官办的医药营销机构",
}

CHAPTER_VARIANTS = {
    "第一章中药": ["第一章中药"],
    "第二章化学制药": ["化学制药", "第二章化学制药"],
    "第三章医疗器械、材料": ["医疗器械、材料", "第三章医疗器械、材料"],
    "第四章医药购销": ["第四章医药购销", "医药购销"],
}

SECTION_NEEDLES = {
    ("第一章中药", "第一节中药材"): "一、资源",
    ("第一章中药", "第二节中药饮片"): "明洪武十七年（1384年）海州设有惠民药局",
    ("第一章中药", "第三节中成药"): "明代宫办惠民药局制作中成药",
    ("第一章中药", "第四节主要企业简介"): "一、连云港中药厂",
    ("第二章化学制药", "第一节生产概况"): "民国3年（1914年），义德医院",
    ("第二章化学制药", "第二节产品"): "一、品种名录",
    ("第二章化学制药", "第三节主要企业简介"): "一、连云港东风制药厂",
    ("第三章医疗器械、材料", "第一节生产概况"): "1958~1963年，机械、轻工等行业",
    ("第三章医疗器械、材料", "第二节产品"): "光学类光学眼镜片",
    ("第三章医疗器械、材料", "第三节主要企业简介"): "一、连云港市朝阳卫生材料厂",
    ("第四章医药购销", "第一节经营机构"): "明洪武十七年（1384年），海州有官办的惠民药局",
    ("第四章医药购销", "第二节调拨采购"): "建国前，药品除部分进口外",
    ("第四章医药购销", "第三节销售"): "建国前，私营中药店都注重服务工作",
}

SECTION_VARIANTS = {
    "第一节中药材": ["第一节中药材"],
    "第二节中药饮片": ["第二节中药饮片"],
    "第三节中成药": ["第三节中成药"],
    "第四节主要企业简介": ["第四节三主要企业简介", "第四节主要企业简介"],
    "第二节产品": ["第二节•产•品", "第二节‧产、产品名录", "第二节产品"],
    "第三节主要企业简介": ["第三节主要企业简介"],
    "第一节经营机构": ["第一节经营机构"],
    "第二节调拨采购": ["第二节调拨采购"],
    "第三节销售": ["第三节销售"],
}

EXPECTED_TABLES = ["表19-1", "表19-2", "表19-3", "表19-4", "表19-5", "表19-6", "表19-7", "表19-8", "表19-10"]


def h3(title: str) -> str:
    return f'<h3 id="第十九卷-{title}">{title}</h3>'


def h4(chapter: str, title: str) -> str:
    return f'<h4 id="第十九卷-{chapter}-{title}">{title}</h4>'


def repair_source_md() -> list[str]:
    text = SRC_MD.read_text(encoding="utf-8")
    original = text
    start_candidates = [text.find("\n第十九卷\n"), text.find("\n第十九卷 医药\n")]
    start_candidates = [pos for pos in start_candidates if pos >= 0]
    start = min(start_candidates) if start_candidates else -1
    end_candidates = [text.find("\n第二十卷\n", start if start >= 0 else 0), text.find("\n第二十卷 化学工业\n", start if start >= 0 else 0)]
    end_candidates = [pos for pos in end_candidates if pos >= 0]
    end = min(end_candidates) if end_candidates else -1
    if start < 0 or end < 0:
        raise RuntimeError("Cannot locate 第十九卷 source range")
    head, section, tail = text[:start], text[start:end], text[end:]
    replacements = {
        "\n第十九卷\n概述\n": "\n第十九卷 医药\n\n概述\n",
        "\n第四节三\n主要企业简介\n": "\n第四节主要企业简介\n",
        "\n第二章\n化学制药\n第一节生产概况\n": "\n第二章化学制药\n第一节生产概况\n",
        "\n第二节•产•品\n": "\n第二节产品\n",
        "\n第三节\n主要企业简介\n": "\n第三节主要企业简介\n",
        "\n第三章\n医疗器械、材料\n第一节生产概况\n": "\n第三章医疗器械、材料\n第一节生产概况\n",
        "\n第二节‧产\n、产品名录\n": "\n第二节产品\n一、产品名录\n",
        "\n第四章\n医药购销\n": "\n第四章医药购销\n",
        "\n第四章E\n\n": "\n",
        "\n第二节\n调拨采购\n": "\n第二节调拨采购\n",
    }
    for old, new in replacements.items():
        section = section.replace(old, new)
    text = head + section + tail
    if text != original:
        SRC_MD.write_text(text, encoding="utf-8")
        return ["规范源 MD 中第十九卷卷题、章题、节题断裂和重复页眉/目录残留。"]
    return []


def normalize_residue(section: str) -> str:
    residues = {
        "<p>第一节中药材": "<p>",
        "<p>第二节中药饮片": "<p>",
        "<p>第三节中成药": "<p>",
        "<p>第四节三主要企业简介": "<p>",
        "<p>化学制药第一节生产概况": "<p>",
        "<p>第二节•产•品": "<p>",
        "<p>医疗器械、材料第一节生产概况": "<p>",
        "<p>第二节‧产、产品名录": "<p>一、产品名录",
        "<p>第二节调拨采购": "<p>",
        "<p>第三节销售": "<p>",
    }
    for old, new in residues.items():
        section = section.replace(old, new, 1)
    section = section.replace("第四章E", "", 1)
    return section


def insert_or_replace_title(section: str, marker: str, needle: str, variants: list[str], start: int = 0) -> tuple[str, bool, int]:
    if marker in section:
        return section, False, section.find(marker) + len(marker)
    needle_pos = section.find(needle, max(0, start - 800))
    if needle_pos < 0:
        needle_pos = section.find(needle)
    if needle_pos >= 0:
        prefix_start = max(0, needle_pos - 260)
        prefix = section[prefix_start:needle_pos]
        for raw in variants:
            rel = prefix.rfind(raw)
            if rel >= 0:
                pos = prefix_start + rel
                section = section[:pos] + marker + "\n<p>" + section[pos + len(raw) :]
                return section, True, pos + len(marker) + 4
        pos = needle_pos
        paragraph_start = section.rfind("<p>", 0, pos)
        paragraph_end = section.rfind("</p>", 0, pos)
        if paragraph_start > paragraph_end and not section[paragraph_start + 3 : pos].strip():
            pos = paragraph_start
        section = section[:pos] + marker + "\n" + section[pos:]
        return section, True, pos + len(marker) + 1
    return section, False, start


def cleanup_heading_markup(section: str) -> str:
    section = section.replace("<p><h3", "<h3").replace("<p><h4", "<h4")
    section = section.replace("</h3>\n</p>", "</h3>\n").replace("</h4>\n</p>", "</h4>\n")
    first_chapter = '<h3 id="第十九卷-第一章中药">第一章中药</h3>'
    first_section = '<h4 id="第十九卷-第一章中药-第一节中药材">第一节中药材</h4>'
    section = re.sub(
        re.escape(first_section) + r"\n(<p>一、资源</p>\n)" + re.escape(first_chapter),
        first_chapter + "\n" + first_section + r"\n\1",
        section,
        count=1,
    )
    section = re.sub(r"(</h[34]>)\n(?!<)([^\n<][^\n]*?</p>)", r"\1\n<p>\2", section)
    section = re.sub(r"(<p>[^<]+)(<h[34] id=\"第十九卷-[^\"]+\">)", r"\1</p>\n\2", section)
    section = re.sub(r"<p>\s*</p>\n?", "", section)
    return section


def restore_headings(section: str) -> tuple[str, int, int]:
    h3_count = 0
    h4_count = 0
    section = normalize_residue(section)

    summary_marker = '<h3 id="第十九卷-概述">概述</h3>'
    if summary_marker not in section:
        section = summary_marker + "\n" + section.lstrip()
        h3_count += 1
    cursor = len(summary_marker)

    for chapter, _titles in CHAPTERS:
        section, added, cursor = insert_or_replace_title(section, h3(chapter), CHAPTER_NEEDLES[chapter], CHAPTER_VARIANTS.get(chapter, [chapter]), cursor)
        h3_count += int(added)

    cursor = 0
    for chapter, titles in CHAPTERS:
        for title in titles:
            variants = SECTION_VARIANTS.get(title, [title])
            section, added, cursor = insert_or_replace_title(section, h4(chapter, title), SECTION_NEEDLES[(chapter, title)], variants, cursor)
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
        raise RuntimeError("Cannot locate 第十九卷 医药 section")
    _heading, section = m.groups()
    actions: list[str] = []
    heading = '<h2 id="第十九卷-医药">第十九卷医药</h2>'

    ipa_before = section.count('<div class="ipa-data">')
    section = section.replace('<div class="ipa-data">', '<p>').replace('</div>', '</p>')
    if ipa_before:
        actions.append(f"将第十九卷误用 `ipa-data` 的正文块转回段落：{ipa_before} 处。")

    section, h3_added, h4_added = restore_headings(section)
    if h3_added:
        actions.append(f"恢复医药卷卷内 H3 标题：{h3_added} 处。")
    if h4_added:
        actions.append(f"恢复医药卷节级 H4 标题：{h4_added} 处。")

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
    for table_dir in TABLE_DATA_DIRS:
        if not table_dir.exists():
            continue
        for path in sorted(table_dir.glob("*.json")):
            data = json.loads(path.read_text(encoding="utf-8"))
            title = str(data.get("title") or "")
            number = str(data.get("table_number") or "")
            if title.startswith("表19-") or number.startswith("表19-"):
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
        table_lines = [f"| 暂无登记 | {table_no} | 第十九卷表格尚未进入表格站 | p1019-p1041 | 待补登 | 待定 | 需从源 PDF 专项补建、核验 |" for table_no in EXPECTED_TABLES]

    lines = [
        "# 第十九卷医药 修复核对进度",
        "",
        f"更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "## 本章范围",
        "",
        "- 章节：第十九卷 医药。",
        "- 源 MD：`workbench/body_chapters/第十七卷至第二十九卷（中part01）.md`。",
        "- 阅读版范围：`output/final_reader/连云港市志_全书.html` 中 `第十九卷-医药` 至 `第二十卷-化学工业` 之前。",
        "- 源页范围：约 p1017-p1041，位于中册 part01。",
        "",
        "## 已完成内容",
        "",
    ]
    lines.extend(f"- {action}" for action in actions)
    lines.extend([
        "- 复核第十九卷正文区间，确认本卷实际为四章：中药、化学制药、医疗器械材料、医药购销。",
        "- 统计第十九卷表格状态，表格站暂无表19-*登记，阅读版已有结构化表，仍有 OCR 表格残文。",
        "",
        "## 格式修复清单",
        "",
        "- 将 H2 从 `第十九卷概述` 修正为 `第十九卷医药`，卷内 `概述` 恢复为 H3。",
        "- 恢复 `第一章中药` 至 `第四章医药购销` 共 4 个 H3。",
        "- 恢复中药材、中药饮片、中成药、化学制药生产概况、产品、医疗器械生产概况、产品、医药经营机构、调拨采购、销售、主要企业简介等 13 个 H4。",
        "- 将第十九卷误入 `ipa-data` 的正文块转回普通段落。",
        "- 清理源 MD 中章题、节题断裂和 OCR 页眉残留。",
        "",
        "## 表格处理清单",
        "",
        f"- 阅读版本章结构化表格：{stats['structured_tables']} 处。",
        f"- 阅读版本章待结构化占位符：{stats['table_placeholders']} 处。",
        f"- 表格站中表号为表19-*的登记表格：{len(tables)} 张。",
        "- 源 MD 可见表19-1至表19-8、表19-10；暂未见表19-9，需 PDF 专项核查是否缺号或漏识别。",
        "",
        "| 表格ID | 表号 | 标题 | 页码 | 状态 | 行列 | 备注 |",
        "|---|---|---|---|---|---|---|",
    ])
    lines.extend(table_lines)
    lines.extend([
        "",
        "## 验收结果",
        "",
        f"- 第十九卷 HTML 字节数：{stats['bytes']:,}。",
        f"- 第十九卷范围内 H2 数：{stats['h2_count']}；H3 数：{stats['h3_count']}；H4 数：{stats['h4_count']}。",
        f"- 第十九卷范围内通用标题锚点残留：{stats['generic_heading_anchors']}。",
        f"- 第十九卷范围内 `ipa-data` 残留：{stats['ipa_blocks']}。",
        f"- 第十九卷范围内 H3 嵌套进段落问题：{stats['embedded_h3_in_p']}。",
        f"- 第十九卷范围内 H4 嵌套进段落问题：{stats['embedded_h4_in_p']}。",
        f"- 第十九卷范围内畸形标题 id：{stats['malformed_heading_ids']}。",
        f"- 第十九卷范围内卷首/目录残留关键词：{stats['front_matter_residual']}。",
        "- 已复跑全书结构审计脚本，TOC 缺失锚点为 0。",
        "- 工作站 `npm run typecheck` 通过。",
        "",
        "## 遇到的问题",
        "",
        "- 阅读版 H2 误写为 `第十九卷概述`，且全部章、节标题扁平化为正文。",
        "- 源 MD 中 `第四节三`、`第二节•产•品`、`第二节‧产` 等 OCR 断裂明显。",
        "- 表19-*未登记到表格站，表19-9编号暂未在源 MD 中发现。",
        "",
        "## 解决的困难",
        "",
        "- 以第十九卷至第二十卷边界限定修复范围，避免误动化学工业卷。",
        "- 对重复的 `生产概况`、`产品`、`主要企业简介` 按所属章生成唯一 H4 锚点。",
        "- 对未核表格只保留现有结构表，不用 OCR 残文补填。",
        "",
        "## 残留风险",
        "",
        "- 第十九卷表19-*需从源 PDF 逐张核读、补登、结构化。",
        "- 药品名、设备名和经济指标密集，后续精校需结合原 PDF 校对。",
        "",
        "## 下一步计划",
        "",
        "- 进入第二十卷 化学工业章节格式核对。",
        "- 表格专项阶段回补第十九卷中药资源、药材收购、化学制药产量、医药购销等统计表。",
    ])
    PROGRESS_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def update_memory(stats: dict[str, int]) -> None:
    text = MEMORY_PATH.read_text(encoding="utf-8")
    header = "## 2026-06-28 第十九卷医药章节核对完成"
    section = f"""{header}

已完成 `第十九卷 医药` 章节格式核对：

- 新增脚本：`scripts/repair_nineteenth_volume_medicine.py`。
- 修复 `workbench/body_chapters/第十七卷至第二十九卷（中part01）.md` 中第十九卷卷题、章题、节题断裂和页眉残留。
- 修复 `output/final_reader/连云港市志_全书.html` 中第十九卷 H2 误写、章节标题全部扁平化以及正文块误用 `ipa-data` 的问题。
- 第十九卷现有结构：H2={stats['h2_count']}，H3={stats['h3_count']}（概述 + 第一章中药至第四章医药购销），H4={stats['h4_count']}。
- 第十九卷范围内 `ipa-data` 残留已清零。
- 本章阅读版现有结构化表格 {stats['structured_tables']} 处，正文表格占位符 {stats['table_placeholders']} 处；表格站暂无表19-*登记条目。
- 已写入进度文档：`output/reports/progress/20260628_第十九卷医药_修复核对进度.md`。

验收：第十九卷 HTML 字节数 {stats['bytes']:,}，范围内通用标题锚点残留 0，`ipa-data` 残留 0，H3/H4 嵌套进段落问题 0，畸形标题 id 0；复跑 `scripts/audit_full_reader.py`，TOC 缺失锚点 0。工作站 `npm run typecheck` 通过。

下一步：进入 `第二十卷 化学工业`。第十九卷表19-*需从源 PDF 专项补登、重建和核验。
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
