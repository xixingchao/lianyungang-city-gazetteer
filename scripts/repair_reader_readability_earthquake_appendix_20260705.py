# -*- coding: utf-8 -*-
"""Restore volume 1 earthquake section heading and appendix list."""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_earthquake_appendix_20260705.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_earthquake_appendix_20260705.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260705_第一卷地震附录列表版式修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SECTION_PREFIX = "<p>第八节地震市域位于华北地震区的南缘，"
SECTION_REPLACEMENT = "<h4>第八节 地震</h4>\n<p>市域位于华北地震区的南缘，"
TITLE = "<h4>附1-12：连云港市境西汉至民国时期主要地震</h4>"
END = "<table class=\"structured-table\"><caption>表1-25 1973～1990年连云港市1级以上地震统计表</caption>"
RESIDUALS = [SECTION_PREFIX]


def append_once(path: Path, marker: str, content: str) -> None:
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker not in old:
        path.write_text(old.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")


def restore_list(text: str) -> tuple[str, int]:
    start = text.index(TITLE) + len(TITLE)
    end = text.index(END, start)
    block = text[start:end]
    items = re.findall(r"<p>(.*?)</p>", block, flags=re.S)
    if len(items) < 20:
        raise RuntimeError(f"expected earthquake list items, got {len(items)}")
    rendered = "\n<ul class=\"reader-restored-list\">\n" + "\n".join(f"<li>{item}</li>" for item in items) + "\n</ul>\n"
    return text[:start] + rendered + text[end:], len(items)


def patch_html() -> tuple[int, int]:
    text = HTML.read_text(encoding="utf-8")
    count = text.count(SECTION_PREFIX)
    if count != 1:
        raise RuntimeError(f"expected one section heading match, got {count}")
    text = text.replace(SECTION_PREFIX, SECTION_REPLACEMENT, 1)
    text, items = restore_list(text)
    for residue in RESIDUALS:
        if residue in text:
            raise RuntimeError(f"earthquake residue remains: {residue}")
    HTML.write_text(text, encoding="utf-8")
    return 1, items


def main() -> None:
    headings, items = patch_html()
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "第一卷自然环境：第八节地震、附1-12主要地震",
        "section_headings_split": headings,
        "earthquake_items_restored": items,
        "source_evidence": ["workbench/body_chapters/paddle_上/第一卷_自然环境.md:6253-6319"],
        "notes": ["保留最终阅读版现有条目文字，仅按源行/条目边界恢复标题和列表版式。"],
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    md = f"""# 第一卷地震附录列表版式修复

- 时间：{now}
- 范围：第一卷自然环境，第八节地震与附1-12。
- 拆分小节标题：{headings} 处。
- 恢复地震条目：{items} 条。

## 修复

- 将 `第八节地震` 从正文段首拆为独立小节标题。
- 将 `附1-12：连云港市境西汉至民国时期主要地震` 下的逐条地震记录恢复为 `reader-restored-list`。
- 保留最终阅读版现有条目文字，不猜修 OCR 字词。

## 依据

- `workbench/body_chapters/paddle_上/第一卷_自然环境.md:6253-6319`
"""
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")
    marker = "## 2026-07-05 第一卷地震附录列表版式修复"
    append_once(
        MEMORY,
        marker,
        f"""
{marker}
- 修复第一卷自然环境 `第八节地震` 小节标题粘正文问题，并将 `附1-12` 主要地震条目恢复为列表。
- 本批保留最终阅读版现有条目文字，只按源文边界恢复版式，不猜修 OCR 字词。
- 报告：`output/reports/reader_readability_earthquake_appendix_20260705.md`。
""",
    )
    print(f"section_headings_split={headings}")
    print(f"earthquake_items_restored={items}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()
