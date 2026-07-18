# -*- coding: utf-8 -*-
"""Third follow-up repairs for 第九卷 农林业 section labels."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
PROGRESS_PATH = ROOT / "output" / "reports" / "progress" / "20260628_第九卷农林业_修复核对进度.md"
MEMORY_PATH = ROOT / "PROJECT_MEMORY.md"
SECTION_RE = re.compile(r'(<h2 id="第九卷-农林业">.*?)(?=<h2 id="第十卷-水利">)', re.S)


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


def main() -> None:
    html = HTML_PATH.read_text(encoding="utf-8")
    fixed = html

    # Restore 第三章品种 section headings in the variety chapter.
    variety_repls = {
        '<p>第二节三麦20世纪50年代初期前，': '<h4 id="第九卷-第三章品种-第二节三麦">第二节三麦</h4>\n<p>20世纪50年代初期前，',
        '<p>第三节玉米建国前，': '<h4 id="第九卷-第三章品种-第三节玉米">第三节玉米</h4>\n<p>建国前，',
        '<p>第四节大豆建国前及50年代初期，': '<h4 id="第九卷-第三章品种-第四节大豆">第四节大豆</h4>\n<p>建国前及50年代初期，',
        '<p>第五节花生清雍正年间': '<h4 id="第九卷-第三章品种-第五节花生">第五节花生</h4>\n<p>清雍正年间',
    }
    for old, new in variety_repls.items():
        fixed = fixed.replace(old, new, 1)

    # Correct the cultivation chapter labels that were attached to 第三章 during first pass.
    cultivation_repls = {
        '<h4 id="第九卷-第三章品种-第二节三麦">第二节三麦</h4>\n<p>栽培一、种植规模': '<h4 id="第九卷-第四章作物栽培-第二节三麦栽培">第二节三麦栽培</h4>\n<p>一、种植规模',
        '<h4 id="第九卷-第三章品种-第三节玉米">第三节玉米</h4>\n<p>栽培一、种植规模': '<h4 id="第九卷-第四章作物栽培-第三节玉米栽培">第三节玉米栽培</h4>\n<p>一、种植规模',
        '<h4 id="第九卷-第三章品种-第四节大豆">第四节大豆</h4>\n<p>栽培一、种植规模': '<h4 id="第九卷-第四章作物栽培-第四节大豆栽培">第四节大豆栽培</h4>\n<p>一、种植规模',
        '<h4 id="第九卷-第三章品种-第五节花生">第五节花生</h4>\n<p>栽培一、种植规模': '<h4 id="第九卷-第四章作物栽培-第五节花生栽培">第五节花生栽培</h4>\n<p>一、种植规模',
    }
    for old, new in cultivation_repls.items():
        fixed = fixed.replace(old, new, 1)

    if fixed != html:
        HTML_PATH.write_text(fixed, encoding="utf-8")
    stats = audit(fixed)

    text = PROGRESS_PATH.read_text(encoding="utf-8")
    text = re.sub(r"- 第九卷 HTML 字节数：.*。", f"- 第九卷 HTML 字节数：{stats['bytes']:,}。", text)
    text = re.sub(r"- 第九卷范围内 H2 数：.*。", f"- 第九卷范围内 H2 数：{stats['h2_count']}；H3 数：{stats['h3_count']}；H4 数：{stats['h4_count']}。", text)
    note = "- 追加修复第三章品种第二至第五节与第四章作物栽培第二至第五节标签归属：8 处。"
    if note not in text:
        text = text.replace("- 追加修复第三章品种与第四章作物栽培章内边界，并补齐甘薯、棉花及作物栽培前五节：7 处。", "- 追加修复第三章品种与第四章作物栽培章内边界，并补齐甘薯、棉花及作物栽培前五节：7 处。\n" + note)
    PROGRESS_PATH.write_text(text, encoding="utf-8")

    mem = MEMORY_PATH.read_text(encoding="utf-8")
    mem = re.sub(r"第九卷现有结构：H2=\d+，H3=\d+（概述 \+ 第一章农业生产关系变革至第十章农机具），H4=\d+。", f"第九卷现有结构：H2={stats['h2_count']}，H3={stats['h3_count']}（概述 + 第一章农业生产关系变革至第十章农机具），H4={stats['h4_count']}。", mem)
    mem = re.sub(r"验收：第九卷 HTML 字节数 [\d,]+，", f"验收：第九卷 HTML 字节数 {stats['bytes']:,}，", mem)
    MEMORY_PATH.write_text(mem, encoding="utf-8")

    print(f"stats={stats}")


if __name__ == "__main__":
    main()
