# -*- coding: utf-8 -*-
"""Append Batch 56 note to PROJECT_MEMORY.md once."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MEMORY = ROOT / "PROJECT_MEMORY.md"

NOTE = """

## 2026-07-06 高置信 OCR 错字补修第五十六批：文化司法短片段
- 新增并运行 `scripts/repair_reader_high_confidence_ocr_typos_batch56_culture_justice_short_20260706.py`，据 PaddleOCR/raw OCR 对照修复主阅读版 6 个文化与司法短片段。
- 主要修复：`编繁《连云港市志》` -> `编纂《连云港市志》`，`组织史资料》的编繁工作` -> `编纂工作`，民间文学段 `诊语卷/姜威编繁/玄辩学` -> `谚语卷/姜威编纂/玄奘辩学`，两处 `淮北盐特区司法科并人市法院` -> `并入市法院`。
- 证据页：`workbench/ocr/paddle_ocr/下/part01/page_0458.txt`、`workbench/ocr/raw/下/part01/page_0458.txt`、`workbench/ocr/paddle_ocr/下/part02/page_0054.txt`、`workbench/ocr/raw/下/part02/page_0054.txt`、`workbench/ocr/paddle_ocr/下/part02/page_0020.txt`、`workbench/ocr/raw/下/part02/page_0020.txt`、`workbench/ocr/paddle_ocr/下/part01/page_0114.txt`、`workbench/ocr/raw/下/part01/page_0114.txt`、`workbench/ocr/paddle_ocr/下/part01/page_0142.txt`、`workbench/ocr/raw/下/part01/page_0142.txt`。
- 边界：书末编纂始末页仍缺更强页级证据，本批不处理；未展示、未嵌入页图。报告：`output/reports/progress/20260706_高置信OCR错字补修第五十六批_文化司法短片段.md`。
""".strip()


def main() -> None:
    text = MEMORY.read_text(encoding="utf-8")
    marker = "## 2026-07-06 高置信 OCR 错字补修第五十六批：文化司法短片段"
    if marker in text:
        print("already_present=1")
        return
    sep = "" if text.endswith("\n") else "\n"
    MEMORY.write_text(text + sep + "\n" + NOTE + "\n", encoding="utf-8")
    print("appended=1")


if __name__ == "__main__":
    main()
