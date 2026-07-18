# -*- coding: utf-8 -*-
"""Follow-up repairs for 第四卷 人口 heading boundaries."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
PROGRESS_PATH = ROOT / "output" / "reports" / "progress" / "20260628_第四卷人口_修复核对进度.md"
SECTION_RE = re.compile(r'(<h2 id="第四卷-人口">.*?)(?=<h2 id="第五卷-城乡建设">)', re.S)


def h4(chapter: str, title: str) -> str:
    return f'<h4 id="第四卷-{chapter}-{title}">{title}</h4>'


def split_inline_heading(text: str, chapter: str, title: str, variants: list[str]) -> tuple[str, int]:
    marker = h4(chapter, title)
    if marker in text:
        return text, 0
    for raw in variants:
        pattern = re.compile(rf"{re.escape(raw)}(?=\S)")
        next_text, count = pattern.subn(marker + "\n<p>", text, count=1)
        if count:
            return next_text, count
    return text, 0


def audit_fourth(html: str) -> dict[str, int]:
    m = SECTION_RE.search(html)
    if not m:
        raise RuntimeError("Cannot locate 第四卷")
    block = m.group(1)
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


def update_progress(stats: dict[str, int], fixed_count: int) -> None:
    text = PROGRESS_PATH.read_text(encoding="utf-8")
    text = re.sub(
        r"- 第四卷范围内 H2 数：.*。",
        f"- 第四卷范围内 H2 数：{stats['h2_count']}；H3 数：{stats['h3_count']}；H4 数：{stats['h4_count']}。",
        text,
    )
    text = re.sub(
        r"- 第四卷范围内 H4 嵌套进段落问题：.*。",
        f"- 第四卷范围内 H4 嵌套进段落问题：{stats['embedded_h4_in_p']}。",
        text,
    )
    marker = "- 人口总量、人口变动、人口构成、人口控制、人口普查等节题恢复为 H4。"
    addition = f"- 追加修复粘连在段落/表格残文中的节题边界：{fixed_count} 处。"
    if addition not in text:
        text = text.replace(marker, marker + "\n" + addition)
    risk = "- 第二章人口构成中表4-4、表4-5残文仍需表格专项从源 PDF 重建，当前只恢复阅读版节题边界。"
    if risk not in text:
        text = text.replace(
            "- 第四卷人口统计表多为宽表/跨页表，需表格专项逐表按源 PDF 复核。",
            "- 第四卷人口统计表多为宽表/跨页表，需表格专项逐表按源 PDF 复核。\n" + risk,
        )
    PROGRESS_PATH.write_text(text, encoding="utf-8")


def main() -> None:
    html = HTML_PATH.read_text(encoding="utf-8")
    fixed = html
    replacements = [
        ("第一章人口规模", "第二节人口变动", ["第二节人口变动"]),
        ("第二章人口构成", "第二节性别", ["第二节 性 别", "第二节性别"]),
        ("第二章人口构成", "第三节年龄", ["第三节 年 龄", "第三节年龄"]),
        ("第二章人口构成", "第四节文化程度", ["第四节文化程度"]),
        ("第二章人口构成", "第五节行业职业", ["第五节行业职业"]),
    ]
    total = 0
    for chapter, title, variants in replacements:
        fixed, count = split_inline_heading(fixed, chapter, title, variants)
        total += count
    if fixed != html:
        HTML_PATH.write_text(fixed, encoding="utf-8")
    stats = audit_fourth(fixed)
    update_progress(stats, total)
    print(f"fixed_inline_headings={total}")
    print(f"stats={stats}")


if __name__ == "__main__":
    main()
