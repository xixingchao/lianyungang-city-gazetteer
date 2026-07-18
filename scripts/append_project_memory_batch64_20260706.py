# -*- coding: utf-8 -*-
"""Append Batch 64 note to PROJECT_MEMORY.md once."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MEMORY = ROOT / "PROJECT_MEMORY.md"

NOTE = """
## 2026-07-06 高置信 OCR 错字补修第六十四批：书末编纂短片段
- 新增并运行 `scripts/repair_reader_high_confidence_ocr_typos_batch64_book_end_more_20260706.py`，据本地 Tesseract OCR、raw OCR、当前章节标题体系与同书序言上下文修复主阅读版 4 个书末现代文字短片段。
- 主要修复：`《连云港市志》的编繁工作始于1986年8月` -> `《连云港市志》的编纂工作始于1986年8月`，`编篆始末` -> `编纂始末`，`《连云港市志》的编篆出版` -> `《连云港市志》的编纂出版`，`然“于秋大业”得以告成` -> `然“千秋大业”得以告成`。
- 证据文本：`workbench/ocr/tesseract_check/book_end_20260706/page_0475_tess.txt`、`workbench/ocr/raw/下/part02/page_0475.txt`、`workbench/ocr/tesseract_check/book_end_20260706/page_0476_tess.txt`、`workbench/ocr/raw/下/part02/page_0476.txt`；同书序言主阅读版已有 `有益后世的千秋大业`。
- 边界：`避选`、`上尽，然长逝` 仍缺稳定文本证据，本批不猜改；`市志编繁委员会`、`省志编繁委员` 等机构名残留虽可疑，但本页 OCR 未闭合，本批不处理。报告：`output/reports/progress/20260706_高置信OCR错字补修第六十四批_书末编纂短片段.md`。
""".strip()


def main() -> None:
    text = MEMORY.read_text(encoding="utf-8")
    marker = "## 2026-07-06 高置信 OCR 错字补修第六十四批：书末编纂短片段"
    if marker in text:
        print("already_present=1")
        return
    sep = "" if text.endswith("\n") else "\n"
    MEMORY.write_text(text + sep + "\n" + NOTE + "\n", encoding="utf-8")
    print("appended=1")


if __name__ == "__main__":
    main()
