# -*- coding: utf-8 -*-
"""Append Batch 63 note to PROJECT_MEMORY.md once."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MEMORY = ROOT / "PROJECT_MEMORY.md"

NOTE = """
## 2026-07-06 高置信 OCR 错字补修第六十三批：书末现代短片段
- 新增并运行 `scripts/repair_reader_high_confidence_ocr_typos_batch63_book_end_modern_20260706.py`，据本地 Tesseract OCR 与 raw OCR 对照修复主阅读版 6 个书末现代文字短片段。
- 主要修复：`表现出极大的热枕/热忧` -> `表现出极大的热忱`，`重新总，出版印刷` -> `重新总繁，出版印刷`，`编寨委员会/《连云港市志）` -> `编纂委员会/《连云港市志》`，`调整篇自` -> `调整篇目`，`《连云港市志》的编繁出版` -> `《连云港市志》的编纂出版`。
- 证据文本：`workbench/ocr/tesseract_check/book_end_20260706/page_0476_tess.txt`、`workbench/ocr/tesseract_check/book_end_20260706/page_0478_tess.txt`；对照 raw：`workbench/ocr/raw/下/part02/page_0476.txt`、`workbench/ocr/raw/下/part02/page_0478.txt`。
- 边界：`避选`、`于秋大业`、`上尽，然长逝` 仍缺稳定文本证据，本批不猜改；`总繁/分繁` 作为书末反复出现的术语样字暂不全局改。报告：`output/reports/progress/20260706_高置信OCR错字补修第六十三批_书末现代短片段.md`。
""".strip()


def main() -> None:
    text = MEMORY.read_text(encoding="utf-8")
    marker = "## 2026-07-06 高置信 OCR 错字补修第六十三批：书末现代短片段"
    if marker in text:
        print("already_present=1")
        return
    sep = "" if text.endswith("\n") else "\n"
    MEMORY.write_text(text + sep + "\n" + NOTE + "\n", encoding="utf-8")
    print("appended=1")


if __name__ == "__main__":
    main()
