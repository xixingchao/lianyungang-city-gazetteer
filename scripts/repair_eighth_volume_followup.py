# -*- coding: utf-8 -*-
"""Follow-up repairs for 第八卷 经济综合管理 heading boundaries."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
PROGRESS_PATH = ROOT / "output" / "reports" / "progress" / "20260628_第八卷经济综合管理_修复核对进度.md"
MEMORY_PATH = ROOT / "PROJECT_MEMORY.md"
SECTION_RE = re.compile(r'(<h2 id="第八卷-经济综合管理">.*?)(?=<h2 id="第九卷-农林业">)', re.S)


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
        "front_matter_residual": len(re.findall(r"CIP|责任编辑|编纂委员会|方志出版社", block)),
        "malformed_heading_ids": len(re.findall(r'<h[34] id="[^"]*<h[34]', block)),
    }


def repair_html() -> dict[str, int]:
    html = HTML_PATH.read_text(encoding="utf-8")
    fixed = html

    fixed = fixed.replace(
        '<h3 id="第八卷-第三章标准计量管理">第三章标准计量管理</h3>\n第三章标准计量管理第一节管理机构民国21年',
        '<h3 id="第八卷-第三章标准计量管理">第三章标准计量管理</h3>\n'
        '<h4 id="第八卷-第三章标准计量管理-第一节管理机构">第一节管理机构</h4>\n<p>民国21年',
        1,
    )
    fixed = fixed.replace(
        '市东风制药厂第四节质量管理20世纪50～60年代',
        '市东风制药厂</p>\n<h4 id="第八卷-第三章标准计量管理-第四节质量管理">第四节质量管理</h4>\n<p>20世纪50～60年代',
        1,
    )
    fixed = fixed.replace(
        '<h3 id="第八卷-第四章审计管理">第四章审计管理</h3>\n第四章审计管理第一节国家审计一、财务收支审计1984年',
        '<h3 id="第八卷-第四章审计管理">第四章审计管理</h3>\n'
        '<h4 id="第八卷-第四章审计管理-第一节国家审计">第一节国家审计</h4>\n<p>一、财务收支审计1984年',
        1,
    )
    malformed = (
        '<h4 id="第八卷-第三章标准计量管理-<h4 id="第八卷-第五章工商行政管理-<h4 id="第八卷-第六章物价管理-第一节管理机构">第一节管理机构</h4>\n'
        '<p>">第一节管理机构</h4>\n<p>">第一节管理机构</h4>\n'
    )
    fixed = fixed.replace(
        malformed,
        '<h4 id="第八卷-第五章工商行政管理-第一节管理机构">第一节管理机构</h4>\n',
        1,
    )
    fixed = fixed.replace(
        '<h3 id="第八卷-第六章物价管理">第六章物价管理</h3>\n<p>第一节管理机构建国前',
        '<h3 id="第八卷-第六章物价管理">第六章物价管理</h3>\n'
        '<h4 id="第八卷-第六章物价管理-第一节管理机构">第一节管理机构</h4>\n<p>建国前',
        1,
    )

    if fixed != html:
        HTML_PATH.write_text(fixed, encoding="utf-8")
    return audit(fixed)


def update_progress(stats: dict[str, int]) -> None:
    text = PROGRESS_PATH.read_text(encoding="utf-8")
    text = re.sub(r"- 第八卷 HTML 字节数：.*。", f"- 第八卷 HTML 字节数：{stats['bytes']:,}。", text)
    text = re.sub(r"- 第八卷范围内 H2 数：.*。", f"- 第八卷范围内 H2 数：{stats['h2_count']}；H3 数：{stats['h3_count']}；H4 数：{stats['h4_count']}。", text)
    text = re.sub(r"- 第八卷范围内 H3 嵌套进段落问题：.*。", f"- 第八卷范围内 H3 嵌套进段落问题：{stats['embedded_h3_in_p']}。", text)
    text = re.sub(r"- 第八卷范围内 H4 嵌套进段落问题：.*。", f"- 第八卷范围内 H4 嵌套进段落问题：{stats['embedded_h4_in_p']}。", text)
    note = "- 追加修复同名 `第一节管理机构` 的章内归属边界，并补齐第三章第四节质量管理：4 处。"
    if note not in text:
        text = text.replace("- 明显重复的临时结构化表格压缩为单实例。", "- 明显重复的临时结构化表格压缩为单实例。\n" + note)
    PROGRESS_PATH.write_text(text, encoding="utf-8")


def update_memory(stats: dict[str, int]) -> None:
    text = MEMORY_PATH.read_text(encoding="utf-8")
    text = re.sub(r"第八卷现有结构：H2=\d+，H3=\d+（概述 \+ 第一章计划管理至第六章物价管理），H4=\d+。", f"第八卷现有结构：H2={stats['h2_count']}，H3={stats['h3_count']}（概述 + 第一章计划管理至第六章物价管理），H4={stats['h4_count']}。", text)
    text = re.sub(r"验收：第八卷 HTML 字节数 [\d,]+，", f"验收：第八卷 HTML 字节数 {stats['bytes']:,}，", text)
    MEMORY_PATH.write_text(text, encoding="utf-8")


def main() -> None:
    stats = repair_html()
    update_progress(stats)
    update_memory(stats)
    print(f"stats={stats}")


if __name__ == "__main__":
    main()
