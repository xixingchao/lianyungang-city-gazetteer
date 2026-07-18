# -*- coding: utf-8 -*-
"""Fix invalid paragraph boundaries around 第四卷 inline H4 headings."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
PROGRESS_PATH = ROOT / "output" / "reports" / "progress" / "20260628_第四卷人口_修复核对进度.md"
SECTION_RE = re.compile(r'(<h2 id="第四卷-人口">.*?)(?=<h2 id="第五卷-城乡建设">)', re.S)


def audit(html: str) -> dict[str, int]:
    block = SECTION_RE.search(html).group(1)
    return {
        "h2_count": len(re.findall(r"<h2 ", block)),
        "h3_count": len(re.findall(r"<h3 ", block)),
        "h4_count": len(re.findall(r"<h4 ", block)),
        "embedded_h4_in_p": len(re.findall(r'<p[^>]*>[^<]*<h4', block)),
        "empty_p_h4": len(re.findall(r'<p>\s*<h4', block)),
    }


def main() -> None:
    html = HTML_PATH.read_text(encoding="utf-8")
    fixed = html
    fixed = fixed.replace("<p><h4", "<h4")
    fixed = re.sub(r"(<p>[^<]+)(<h4 id=\"第四卷-[^\"]+\">)", r"\1</p>\n\2", fixed)
    if fixed != html:
        HTML_PATH.write_text(fixed, encoding="utf-8")
    stats = audit(fixed)
    progress = PROGRESS_PATH.read_text(encoding="utf-8")
    progress = re.sub(
        r"- 第四卷范围内 H4 嵌套进段落问题：.*。",
        f"- 第四卷范围内 H4 嵌套进段落问题：{stats['embedded_h4_in_p']}。",
        progress,
    )
    note = "- 追加清理 H4 与段落标签交叉嵌套，保证标题标签独立成块。"
    if note not in progress:
        progress = progress.replace("- 追加修复粘连在段落/表格残文中的节题边界：5 处。", "- 追加修复粘连在段落/表格残文中的节题边界：5 处。\n" + note)
    PROGRESS_PATH.write_text(progress, encoding="utf-8")
    print(f"stats={stats}")


if __name__ == "__main__":
    main()
