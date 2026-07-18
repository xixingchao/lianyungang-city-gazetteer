# -*- coding: utf-8 -*-
"""Follow-up repairs for 第五卷 inline section headings."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
PROGRESS_PATH = ROOT / "output" / "reports" / "progress" / "20260628_第五卷城乡建设_修复核对进度.md"
SECTION_RE = re.compile(r'(<h2 id="第五卷-城乡建设">.*?)(?=<h2 id="第六卷-环境保护">)', re.S)


def h4(chapter: str, title: str) -> str:
    return f'<h4 id="第五卷-{chapter}-{title}">{title}</h4>'


def split_inline(text: str, chapter: str, title: str, variants: list[str]) -> tuple[str, int]:
    marker = h4(chapter, title)
    if marker in text:
        return text, 0
    total = 0
    for raw in variants:
        pattern = re.compile(rf"{re.escape(raw)}(?=\S)")
        text, count = pattern.subn(marker + "\n<p>", text, count=1)
        total += count
        if count:
            break
    return text, total


def fix_boundaries(text: str) -> str:
    text = text.replace("<p><h4", "<h4")
    return re.sub(r"(<p>[^<]+)(<h4 id=\"第五卷-[^\"]+\">)", r"\1</p>\n\2", text)


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
        "embedded_h4_in_p": len(re.findall(r'<p[^>]*>[^<]*<h4', block)),
    }


def update_progress(stats: dict[str, int], fixed: int) -> None:
    text = PROGRESS_PATH.read_text(encoding="utf-8")
    text = re.sub(r"- 第五卷 HTML 字节数：.*。", f"- 第五卷 HTML 字节数：{stats['bytes']:,}。", text)
    text = re.sub(r"- 第五卷范围内 H2 数：.*。", f"- 第五卷范围内 H2 数：{stats['h2_count']}；H3 数：{stats['h3_count']}；H4 数：{stats['h4_count']}。", text)
    text = re.sub(r"- 第五卷范围内 H4 嵌套进段落问题：.*。", f"- 第五卷范围内 H4 嵌套进段落问题：{stats['embedded_h4_in_p']}。", text)
    note = f"- 追加修复粘连在表格残文中的节题边界：{fixed} 处。"
    if note not in text:
        text = text.replace("- 规划、测绘、市政、公用事业、环卫、园林、房产等节题恢复为 H4。", "- 规划、测绘、市政、公用事业、环卫、园林、房产等节题恢复为 H4。\n" + note)
    PROGRESS_PATH.write_text(text, encoding="utf-8")


def main() -> None:
    html = HTML_PATH.read_text(encoding="utf-8")
    fixed = html
    total = 0
    fixed, count = split_inline(fixed, "第二章市政建设", "第二节桥梁隧道", ["第二节桥梁 隧道", "第二节桥梁隧道"])
    total += count
    fixed, count = split_inline(fixed, "第三章公用事业", "第三节公共交通", ["第三节公共交通", "第三节 公共交通"])
    total += count
    fixed = fix_boundaries(fixed)
    if fixed != html:
        HTML_PATH.write_text(fixed, encoding="utf-8")
    stats = audit(fixed)
    update_progress(stats, total)
    print(f"fixed_inline_headings={total}")
    print(f"stats={stats}")


if __name__ == "__main__":
    main()
