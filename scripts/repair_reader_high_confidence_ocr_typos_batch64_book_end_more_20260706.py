# -*- coding: utf-8 -*-
"""Batch 64: more verified book-end modern text short fixes."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT = ROOT / "output" / "reports" / "progress" / "20260706_高置信OCR错字补修第六十四批_书末编纂短片段.md"

REPLACEMENTS = [
    (
        "《连云港市志》的编繁工作始于1986年8月",
        "《连云港市志》的编纂工作始于1986年8月",
        "`workbench/ocr/tesseract_check/book_end_20260706/page_0475_tess.txt` 作 `《连云港市志》编纂工作始于 1986 年`；当前 reader 为 `编繁工作` 残留",
    ),
    (
        "《连云港市志》全书400余万字，由序、凡例、总述、大事记、60分卷、附录、编篆始末和跋组成",
        "《连云港市志》全书400余万字，由序、凡例、总述、大事记、60分卷、附录、编纂始末和跋组成",
        "当前 reader 章节标题体系作 `编纂始末`，同页 Tesseract 可见 `编繁始末` 为形近残留；`编篆始末` 与章节名不合",
    ),
    (
        "《连云港市志》的编篆出版",
        "《连云港市志》的编纂出版",
        "同书书末 `workbench/ocr/tesseract_check/book_end_20260706/page_0478_tess.txt` 作 `《连云港市志》的编纂出版`；当前跋页为 `编篆出版` 形近残留",
    ),
    (
        "然“于秋大业”得以告成",
        "然“千秋大业”得以告成",
        "同书序言主阅读版作 `有益后世的千秋大业`；本页 raw 为断行后的 `于/秋大业`，Tesseract 亦仅识出 `秋大业`，语义和引号内成语支撑补 `千`",
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
        "# 高置信 OCR 错字补修第六十四批：书末编纂短片段",
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
            "- `避选`、`上尽，然长逝` 仍缺稳定文本证据，本批不猜改。",
            "- `市志编繁委员会`、`省志编繁委员` 等机构名残留虽可疑，但本页 OCR 未闭合，本批不处理。",
            "- 未展示、未嵌入页图。",
        ]
    )
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"changed={len(changed)}")
    print(f"progress={REPORT}")


if __name__ == "__main__":
    main()
