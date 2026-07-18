# -*- coding: utf-8 -*-
"""Append Batch 52 note to PROJECT_MEMORY.md once."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MEMORY = ROOT / "PROJECT_MEMORY.md"

NOTE = """

## 2026-07-06 高置信 OCR 错字补修第五十二批：人物水利短片段
- 新增并运行 `scripts/repair_reader_high_confidence_ocr_typos_batch52_people_water_short_20260706.py`，据 PaddleOCR/raw OCR 对照修复主阅读版 4 个人物与水利短片段。
- 主要修复：`灌云县农机广` -> `灌云县农机厂`，`减轻谣役` -> `减轻徭役`，`编繁县志` -> `编纂县志`，武同举水利著述段 `编繁/水惠` -> `编纂/水患`。
- 证据页：`workbench/ocr/paddle_ocr/下/part02/page_0399.txt`、`workbench/ocr/raw/下/part02/page_0399.txt`、`workbench/ocr/paddle_ocr/下/part02/page_0382.txt`、`workbench/ocr/raw/下/part02/page_0382.txt`、`workbench/ocr/paddle_ocr/下/part01/page_0436.txt`、`workbench/ocr/raw/下/part01/page_0436.txt`。
- 边界：书末编纂始末页暂无 PaddleOCR 页文本支撑的疑点，本批不猜改；未展示、未嵌入页图。报告：`output/reports/progress/20260706_高置信OCR错字补修第五十二批_人物水利短片段.md`。
""".strip()


def main() -> None:
    text = MEMORY.read_text(encoding="utf-8")
    marker = "## 2026-07-06 高置信 OCR 错字补修第五十二批：人物水利短片段"
    if marker in text:
        print("already_present=1")
        return
    sep = "" if text.endswith("\n") else "\n"
    MEMORY.write_text(text + sep + "\n" + NOTE + "\n", encoding="utf-8")
    print("appended=1")


if __name__ == "__main__":
    main()
