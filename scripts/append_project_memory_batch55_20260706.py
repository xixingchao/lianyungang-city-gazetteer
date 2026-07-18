# -*- coding: utf-8 -*-
"""Append Batch 55 note to PROJECT_MEMORY.md once."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MEMORY = ROOT / "PROJECT_MEMORY.md"

NOTE = """

## 2026-07-06 高置信 OCR 错字补修第五十五批：入字短片段
- 新增并运行 `scripts/repair_reader_high_confidence_ocr_typos_batch55_ru_into_short_20260706.py`，据 PaddleOCR/raw OCR 对照修复主阅读版 9 个 `人/入` 短片段。
- 主要修复：供销社段 `人股` -> `入股` 4 处，财政四项费用段 `并人` -> `并入` 2 处，金融/政党/政务行政沿革段 `并人` -> `并入` 3 处。
- 证据页：`workbench/ocr/paddle_ocr/中/part02/page_0159.txt`、`workbench/ocr/raw/中/part02/page_0159.txt`、`workbench/ocr/paddle_ocr/中/part02/page_0161.txt`、`workbench/ocr/raw/中/part02/page_0161.txt`、`workbench/ocr/paddle_ocr/中/part02/page_0302.txt`、`workbench/ocr/raw/中/part02/page_0302.txt`、`workbench/ocr/paddle_ocr/中/part02/page_0346.txt`、`workbench/ocr/raw/中/part02/page_0346.txt`、`workbench/ocr/paddle_ocr/中/part02/page_0404.txt`、`workbench/ocr/paddle_ocr/中/part02/page_0480.txt`。
- 边界：公安、法院、教育等其他 `并人` 残留若缺少同页 PaddleOCR 直接支撑，本批不处理；未展示、未嵌入页图。报告：`output/reports/progress/20260706_高置信OCR错字补修第五十五批_入字短片段.md`。
""".strip()


def main() -> None:
    text = MEMORY.read_text(encoding="utf-8")
    marker = "## 2026-07-06 高置信 OCR 错字补修第五十五批：入字短片段"
    if marker in text:
        print("already_present=1")
        return
    sep = "" if text.endswith("\n") else "\n"
    MEMORY.write_text(text + sep + "\n" + NOTE + "\n", encoding="utf-8")
    print("appended=1")


if __name__ == "__main__":
    main()
