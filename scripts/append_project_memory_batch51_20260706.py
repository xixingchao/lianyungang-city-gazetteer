# -*- coding: utf-8 -*-
"""Append Batch 51 note to PROJECT_MEMORY.md once."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MEMORY = ROOT / "PROJECT_MEMORY.md"

NOTE = """

## 2026-07-06 高置信 OCR 错字补修第五十一批：食品工业短片段
- 新增并运行 `scripts/repair_reader_high_confidence_ocr_typos_batch51_food_industry_short_20260706.py`，据 PaddleOCR/raw OCR 对照修复主阅读版 3 个食品工业短片段。
- 主要修复：`连云港市酶制剂广` -> `连云港市酶制剂厂`，`19821989年` -> `1982~1989年`，`部分外销本、香港` -> `部分外销日本、香港`。
- 证据页：`workbench/ocr/paddle_ocr/中/part01/page_0103.txt`、`workbench/ocr/raw/中/part01/page_0103.txt`、`workbench/ocr/paddle_ocr/中/part01/page_0107.txt`、`workbench/ocr/raw/中/part01/page_0107.txt`。
- 边界：同页 raw 的其它错字若当前主阅读版已不存在，本批不重复处理；未展示、未嵌入页图。报告：`output/reports/progress/20260706_高置信OCR错字补修第五十一批_食品工业短片段.md`。
""".strip()


def main() -> None:
    text = MEMORY.read_text(encoding="utf-8")
    marker = "## 2026-07-06 高置信 OCR 错字补修第五十一批：食品工业短片段"
    if marker in text:
        print("already_present=1")
        return
    sep = "" if text.endswith("\n") else "\n"
    MEMORY.write_text(text + sep + "\n" + NOTE + "\n", encoding="utf-8")
    print("appended=1")


if __name__ == "__main__":
    main()
