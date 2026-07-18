# -*- coding: utf-8 -*-
"""Follow-up repairs for 第七卷 经济综情 chapter heading boundaries."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
PROGRESS_PATH = ROOT / "output" / "reports" / "progress" / "20260628_第七卷经济综情_修复核对进度.md"
SECTION_RE = re.compile(r'(<h2 id="第七卷-经济综情">.*?)(?=<h2 id="第八卷-经济综合管理">)', re.S)
H3_SECOND = '<h3 id="第七卷-第二章经济结构">第二章经济结构</h3>'
H4_FIRST = '<h4 id="第七卷-第二章经济结构-第一节所有制结构">第一节所有制结构</h4>'


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
        "front_matter_residual": len(re.findall(r"CIP|责任编辑|编纂委员会|方志出版社", block)),
    }


def update_progress(stats: dict[str, int]) -> None:
    text = PROGRESS_PATH.read_text(encoding="utf-8")
    text = re.sub(r"- 第七卷 HTML 字节数：.*。", f"- 第七卷 HTML 字节数：{stats['bytes']:,}。", text)
    text = re.sub(r"- 第七卷范围内 H2 数：.*。", f"- 第七卷范围内 H2 数：{stats['h2_count']}；H3 数：{stats['h3_count']}；H4 数：{stats['h4_count']}。", text)
    text = re.sub(r"- 第七卷范围内 H4 嵌套进段落问题：.*。", f"- 第七卷范围内 H4 嵌套进段落问题：{stats['embedded_h4_in_p']}。", text)
    note = "- 追加修复第二章经济结构章题边界：1 处。"
    if note not in text:
        text = text.replace("- `第一章经济发展概况` 至 `第三章人民生活` 恢复为 H3。", "- `第一章经济发展概况` 至 `第三章人民生活` 恢复为 H3。\n" + note)
    PROGRESS_PATH.write_text(text, encoding="utf-8")


def main() -> None:
    html = HTML_PATH.read_text(encoding="utf-8")
    fixed = html
    if H3_SECOND not in fixed and H4_FIRST in fixed:
        fixed = fixed.replace(H4_FIRST, H3_SECOND + "\n" + H4_FIRST, 1)
    fixed = fixed.replace("合营个体有证经济结构</p>\n" + H3_SECOND, "合营个体有证</p>\n" + H3_SECOND, 1)
    if fixed != html:
        HTML_PATH.write_text(fixed, encoding="utf-8")
    stats = audit(fixed)
    update_progress(stats)
    print(f"stats={stats}")


if __name__ == "__main__":
    main()
