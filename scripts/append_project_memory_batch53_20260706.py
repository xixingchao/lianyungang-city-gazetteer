# -*- coding: utf-8 -*-
"""Append Batch 53 note to PROJECT_MEMORY.md once."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MEMORY = ROOT / "PROJECT_MEMORY.md"

NOTE = """

## 2026-07-06 高置信 OCR 错字补修第五十三批：工会统战短片段
- 新增并运行 `scripts/repair_reader_high_confidence_ocr_typos_batch53_labor_united_front_short_20260706.py`，据 PaddleOCR/raw OCR 对照修复主阅读版 4 个工会与统战短片段。
- 主要修复：两处 `人股集资` -> `入股集资`，`并人国营商店` -> `并入国营商店`，`各负盈号` -> `各负盈亏`。
- 证据页：`workbench/ocr/paddle_ocr/下/part01/page_0318.txt`、`workbench/ocr/raw/下/part01/page_0318.txt`、`workbench/ocr/paddle_ocr/下/part02/page_0042.txt`、`workbench/ocr/raw/下/part02/page_0042.txt`、`workbench/ocr/paddle_ocr/中/part02/page_0452.txt`、`workbench/ocr/raw/中/part02/page_0452.txt`。
- 边界：`并人沭阳县` 目前缺少同页 PaddleOCR 直接支撑，本批不猜改；未展示、未嵌入页图。报告：`output/reports/progress/20260706_高置信OCR错字补修第五十三批_工会统战短片段.md`。
""".strip()


def main() -> None:
    text = MEMORY.read_text(encoding="utf-8")
    marker = "## 2026-07-06 高置信 OCR 错字补修第五十三批：工会统战短片段"
    if marker in text:
        print("already_present=1")
        return
    sep = "" if text.endswith("\n") else "\n"
    MEMORY.write_text(text + sep + "\n" + NOTE + "\n", encoding="utf-8")
    print("appended=1")


if __name__ == "__main__":
    main()
