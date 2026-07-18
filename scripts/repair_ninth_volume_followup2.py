# -*- coding: utf-8 -*-
"""Second follow-up repairs for 第九卷 农林业 mid-volume boundaries."""

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


def section_block(html: str) -> tuple[re.Match[str], str]:
    m = SECTION_RE.search(html)
    if not m:
        raise RuntimeError("Cannot locate 第九卷 section")
    return m, m.group(1)


def repair_html() -> dict[str, int]:
    html = HTML_PATH.read_text(encoding="utf-8")
    m, block = section_block(html)
    fixed_block = block

    # Move 第三章品种 from the later crop-cultivation boundary back to its real preface.
    late = '<h3 id="第九卷-第三章品种">第三章品种</h3>\n<h4 id="第九卷-第三章品种-第一节水稻">第一节水稻</h4>\n<p>栽培一、种植规模'
    fixed_block = fixed_block.replace(late, '<p>栽培一、种植规模', 1)
    if '<h3 id="第九卷-第三章品种">第三章品种</h3>' not in fixed_block:
        fixed_block = fixed_block.replace(
            '<p>种建国前，农作物用种',
            '<h3 id="第九卷-第三章品种">第三章品种</h3>\n<p>建国前，农作物用种',
            1,
        )
    fixed_block = fixed_block.replace(
        '<p>第一节水一、品种演变',
        '<h4 id="第九卷-第三章品种-第一节水稻">第一节水稻</h4>\n<p>一、品种演变',
        1,
    )
    fixed_block = fixed_block.replace(
        '<p>第六节甘薯建国前，',
        '<h4 id="第九卷-第三章品种-第六节甘薯">第六节甘薯</h4>\n<p>建国前，',
        1,
    )
    fixed_block = fixed_block.replace(
        '<p>第七节棉花建国前，',
        '<h4 id="第九卷-第三章品种-第七节棉花">第七节棉花</h4>\n<p>建国前，',
        1,
    )

    # Restore 第四章作物栽培 section boundaries. OCR left only 栽培... at the first section.
    fixed_block = fixed_block.replace(
        '<h3 id="第九卷-第四章作物栽培">第四章作物栽培</h3>\n<h4 id="第九卷-第四章作物栽培-第六节棉花栽培">第六节棉花栽培</h4>\n<p>一、种植规模1949年，境内棉花',
        '<h3 id="第九卷-第四章作物栽培">第四章作物栽培</h3>\n<h4 id="第九卷-第四章作物栽培-第六节棉花栽培">第六节棉花栽培</h4>\n<p>一、种植规模1949年，境内棉花',
        1,
    )
    fixed_block = fixed_block.replace(
        '<p>栽培一、种植规模民国时期，',
        '<h3 id="第九卷-第四章作物栽培">第四章作物栽培</h3>\n<h4 id="第九卷-第四章作物栽培-第一节水稻栽培">第一节水稻栽培</h4>\n<p>一、种植规模民国时期，',
        1,
    )
    chapter4_repls = {
        '<p>第二节三麦栽培一、种植规模': '<h4 id="第九卷-第四章作物栽培-第二节三麦栽培">第二节三麦栽培</h4>\n<p>一、种植规模',
        '<p>第三节玉米栽培一、种植规模': '<h4 id="第九卷-第四章作物栽培-第三节玉米栽培">第三节玉米栽培</h4>\n<p>一、种植规模',
        '<p>第四节大豆栽培一、种植规模': '<h4 id="第九卷-第四章作物栽培-第四节大豆栽培">第四节大豆栽培</h4>\n<p>一、种植规模',
        '<p>第五节花生栽培一、种植规模': '<h4 id="第九卷-第四章作物栽培-第五节花生栽培">第五节花生栽培</h4>\n<p>一、种植规模',
    }
    for old, new in chapter4_repls.items():
        fixed_block = fixed_block.replace(old, new, 1)

    # If 第四章 was already present at the old late location, keep only the first occurrence.
    marker = '<h3 id="第九卷-第四章作物栽培">第四章作物栽培</h3>'
    first = fixed_block.find(marker)
    if first >= 0:
        second = fixed_block.find(marker, first + len(marker))
        if second >= 0:
            fixed_block = fixed_block[:second] + fixed_block[second + len(marker) + 1 :]

    fixed = html[: m.start()] + fixed_block + html[m.end() :]
    if fixed != html:
        HTML_PATH.write_text(fixed, encoding="utf-8")
    return audit(fixed)


def update_progress(stats: dict[str, int]) -> None:
    text = PROGRESS_PATH.read_text(encoding="utf-8")
    text = re.sub(r"- 第九卷 HTML 字节数：.*。", f"- 第九卷 HTML 字节数：{stats['bytes']:,}。", text)
    text = re.sub(r"- 第九卷范围内 H2 数：.*。", f"- 第九卷范围内 H2 数：{stats['h2_count']}；H3 数：{stats['h3_count']}；H4 数：{stats['h4_count']}。", text)
    note = "- 追加修复第三章品种与第四章作物栽培章内边界，并补齐甘薯、棉花及作物栽培前五节：7 处。"
    if note not in text:
        text = text.replace("- 追加修复第九章、第十章旧 `anchor` 包裹，并补齐第三、四、六、八章 H3 边界：6 处。", "- 追加修复第九章、第十章旧 `anchor` 包裹，并补齐第三、四、六、八章 H3 边界：6 处。\n" + note)
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
