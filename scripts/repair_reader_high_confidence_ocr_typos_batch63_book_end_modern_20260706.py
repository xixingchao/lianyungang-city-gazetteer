# -*- coding: utf-8 -*-
"""Batch 63: verified book-end modern text short fixes."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT = ROOT / "output" / "reports" / "progress" / "20260706_高置信OCR错字补修第六十三批_书末现代短片段.md"

REPLACEMENTS = [
    (
        "表现出极大的热枕",
        "表现出极大的热忱",
        "`workbench/ocr/tesseract_check/book_end_20260706/page_0476_tess.txt` 作 `表现出极大的热忱`；raw 同页为 `热枕` 残留",
    ),
    (
        "第四阶段（1999.8~2000.5）重新总，出版印刷",
        "第四阶段（1999.8~2000.5）重新总繁，出版印刷",
        "`workbench/ocr/tesseract_check/book_end_20260706/page_0478_tess.txt` 作 `重新总繁,出版印刷`；raw 同页漏 `繁`",
    ),
    (
        "连云港市志编寨委员会综合汇报《连云港市志）书稿修改完成情况",
        "连云港市志编纂委员会综合汇报《连云港市志》书稿修改完成情况",
        "同页上下文多处作 `编纂委员会`，Tesseract 同行可辨为书名号闭合；raw 为 `编寨委员会/《连云港市志）` 残留",
    ),
    (
        "调整篇自、充实内容、修改定稿",
        "调整篇目、充实内容、修改定稿",
        "`workbench/ocr/tesseract_check/book_end_20260706/page_0478_tess.txt` 作 `调整篇目`；raw 同页为 `篇自` 残留",
    ),
    (
        "《连云港市志》的编繁出版",
        "《连云港市志》的编纂出版",
        "`workbench/ocr/tesseract_check/book_end_20260706/page_0478_tess.txt` 作 `《连云港市志》的编纂出版`；raw 同页为 `编繁出版` 残留",
    ),
    (
        "表现出极大的热忧",
        "表现出极大的热忱",
        "`workbench/ocr/tesseract_check/book_end_20260706/page_0478_tess.txt` 作 `表现出极大的热忱`；raw 同页为 `热忧` 残留",
    ),
]


def main() -> None:
    html = HTML.read_text(encoding="utf-8")
    changed = []
    for old, new, evidence in REPLACEMENTS:
        count = html.count(old)
        if count != 1:
            raise RuntimeError(f"expected 1 hit, found {count}: {old}")
        html = html.replace(old, new)
        changed.append((old, new, evidence))

    HTML.write_text(html, encoding="utf-8")

    lines = [
        "# 高置信 OCR 错字补修第六十三批：书末现代短片段",
        "",
        f"> 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "## 修复项",
        "",
    ]
    for old, new, evidence in changed:
        lines.append(f"- `{old}` -> `{new}`（命中 1 处）")
        lines.append(f"  - 证据：{evidence}")
    lines.extend(
        [
            "",
            "## 边界",
            "",
            "- 只修主阅读版，不改 OCR 原文。",
            "- `避选`、`于秋大业`、`上尽，然长逝` 仍缺稳定文本证据，本批不猜改。",
            "- `总繁/分繁` 作为书末反复出现的术语样字暂不全局改，只补标题中明显漏字的 `重新总繁`。",
            "- 未展示、未嵌入页图。",
        ]
    )
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"changed={len(changed)}")
    print(f"progress={REPORT}")


if __name__ == "__main__":
    main()
