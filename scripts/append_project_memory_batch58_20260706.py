# -*- coding: utf-8 -*-
"""Append Batch 58 note to PROJECT_MEMORY.md once."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MEMORY = ROOT / "PROJECT_MEMORY.md"

NOTE = """

## 2026-07-06 高置信 OCR 错字补修第五十八批：工厂、干警、入短片段
- 新增并运行 `scripts/repair_reader_high_confidence_ocr_typos_batch58_factory_short_20260706.py`，据 PaddleOCR/raw OCR 对照修复主阅读版 6 个短片段。
- 主要修复：`工广变成一片废墟` -> `工厂变成一片废墟`，`鱼品加工广后` -> `鱼品加工厂后`，`涂料生产工广有8家` -> `涂料生产工厂有8家`，`工广化养鱼` -> `工厂化养鱼`，`公安于警学校` -> `公安干警学校`，`陶瓷人海州` -> `陶瓷入海州`。
- 证据页：`workbench/ocr/paddle_ocr/中/part01/page_0049.txt`、`workbench/ocr/raw/中/part01/page_0049.txt`、`workbench/ocr/paddle_ocr/中/part01/page_0078.txt`、`workbench/ocr/raw/中/part01/page_0078.txt`、`workbench/ocr/paddle_ocr/中/part01/page_0291.txt`、`workbench/ocr/raw/中/part01/page_0291.txt`、`workbench/ocr/paddle_ocr/下/part01/page_0438.txt`、`workbench/ocr/paddle_ocr/下/part01/page_0064.txt`、`workbench/ocr/paddle_ocr/中/part01/page_0456.txt`。
- 边界：`日用化工广` 暂只见 raw 同页残留，未纳入本批；未展示、未嵌入页图。报告：`output/reports/progress/20260706_高置信OCR错字补修第五十八批_工厂干警入短片段.md`。
""".strip()


def main() -> None:
    text = MEMORY.read_text(encoding="utf-8")
    marker = "## 2026-07-06 高置信 OCR 错字补修第五十八批：工厂、干警、入短片段"
    if marker in text:
        print("already_present=1")
        return
    sep = "" if text.endswith("\n") else "\n"
    MEMORY.write_text(text + sep + "\n" + NOTE + "\n", encoding="utf-8")
    print("appended=1")


if __name__ == "__main__":
    main()
