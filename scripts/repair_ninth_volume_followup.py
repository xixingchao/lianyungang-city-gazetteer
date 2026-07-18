# -*- coding: utf-8 -*-
"""Follow-up repairs for 第九卷 农林业 chapter heading boundaries."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
PROGRESS_PATH = ROOT / "output" / "reports" / "progress" / "20260628_第九卷农林业_修复核对进度.md"
MEMORY_PATH = ROOT / "PROJECT_MEMORY.md"
SECTION_RE = re.compile(r'(<h2 id="第九卷-农林业">.*?)(?=<h2 id="第十卷-水利">)', re.S)

MISSING_CHAPTERS = [
    ("第三章品种", "第一节水稻"),
    ("第四章作物栽培", "第六节棉花栽培"),
    ("第六章植物保护", "第一节病虫害防治"),
    ("第八章蔬菜生产", "第一节蔬菜品种"),
]


def h3(title: str) -> str:
    return f'<h3 id="第九卷-{title}">{title}</h3>'


def h4_prefix(chapter: str, title: str) -> str:
    return f'<h4 id="第九卷-{chapter}-{title}">{title}</h4>'


def audit(html: str) -> dict[str, int]:
    block = SECTION_RE.search(html).group(1)
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


def repair_html() -> dict[str, int]:
    html = HTML_PATH.read_text(encoding="utf-8")
    fixed = html

    fixed = fixed.replace(
        '<h3 id="anchor"><h3 id="第九卷-第九章林果桑茶">第九章林果桑茶</h3></h3>',
        '<h3 id="第九卷-第九章林果桑茶">第九章林果桑茶</h3>',
    )
    fixed = fixed.replace(
        '<h3 id="anchor"><h3 id="第九卷-第十章农机具">第十章农机具</h3></h3>',
        '<h3 id="第九卷-第十章农机具">第十章农机具</h3>',
    )

    for chapter, first_section in MISSING_CHAPTERS:
        marker = h3(chapter)
        if marker in fixed:
            continue
        target = h4_prefix(chapter, first_section)
        fixed = fixed.replace(target, marker + "\n" + target, 1)

    if fixed != html:
        HTML_PATH.write_text(fixed, encoding="utf-8")
    return audit(fixed)


def update_progress(stats: dict[str, int]) -> None:
    text = PROGRESS_PATH.read_text(encoding="utf-8")
    text = re.sub(r"- 第九卷 HTML 字节数：.*。", f"- 第九卷 HTML 字节数：{stats['bytes']:,}。", text)
    text = re.sub(r"- 第九卷范围内 H2 数：.*。", f"- 第九卷范围内 H2 数：{stats['h2_count']}；H3 数：{stats['h3_count']}；H4 数：{stats['h4_count']}。", text)
    text = re.sub(r"- 第九卷范围内通用标题锚点残留：.*。", f"- 第九卷范围内通用标题锚点残留：{stats['generic_heading_anchors']}。", text)
    text = re.sub(r"- 第九卷范围内畸形标题 id：.*。", f"- 第九卷范围内畸形标题 id：{stats['malformed_heading_ids']}。", text)
    note = "- 追加修复第九章、第十章旧 `anchor` 包裹，并补齐第三、四、六、八章 H3 边界：6 处。"
    if note not in text:
        text = text.replace("- 明显重复的临时结构化表格压缩为单实例。", "- 明显重复的临时结构化表格压缩为单实例。\n" + note)
    PROGRESS_PATH.write_text(text, encoding="utf-8")


def update_memory(stats: dict[str, int]) -> None:
    text = MEMORY_PATH.read_text(encoding="utf-8")
    text = re.sub(r"第九卷现有结构：H2=\d+，H3=\d+（概述 \+ 第一章农业生产关系变革至第十章农机具），H4=\d+。", f"第九卷现有结构：H2={stats['h2_count']}，H3={stats['h3_count']}（概述 + 第一章农业生产关系变革至第十章农机具），H4={stats['h4_count']}。", text)
    text = re.sub(r"验收：第九卷 HTML 字节数 [\d,]+，", f"验收：第九卷 HTML 字节数 {stats['bytes']:,}，", text)
    MEMORY_PATH.write_text(text, encoding="utf-8")


def main() -> None:
    stats = repair_html()
    update_progress(stats)
    update_memory(stats)
    print(f"stats={stats}")


if __name__ == "__main__":
    main()
