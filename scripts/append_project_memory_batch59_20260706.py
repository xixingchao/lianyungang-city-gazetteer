# -*- coding: utf-8 -*-
"""Append Batch 59 note to PROJECT_MEMORY.md once."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MEMORY = ROOT / "PROJECT_MEMORY.md"

NOTE = """

## 2026-07-06 高置信 OCR 错字补修第五十九批：工厂短片段
- 新增并运行 `scripts/repair_reader_high_confidence_ocr_typos_batch59_factory_short_20260706.py`，据 PaddleOCR/raw OCR 对照修复主阅读版 3 个 `工广/工厂` 短片段。
- 主要修复：`东海县横沟乡日用化工广` -> `东海县横沟乡日用化工厂`，`监所附设工广或作坊` -> `监所附设工厂或作坊`，`街头、工广、街道建立黑板报` -> `街头、工厂、街道建立黑板报`。
- 证据页：`workbench/ocr/paddle_ocr/中/part01/page_0403.txt`、`workbench/ocr/raw/中/part01/page_0403.txt`、`workbench/ocr/paddle_ocr/下/part01/page_0151.txt`、`workbench/ocr/raw/下/part01/page_0151.txt`、`workbench/ocr/paddle_ocr/下/part02/page_0050.txt`、`workbench/ocr/raw/下/part02/page_0050.txt`。
- 边界：`施工广泛使用`、`农村体育经济交流会` 不属 `工广` OCR 错字；`劳改队撤销，并人徐州第四监狱` 双源仍作 `并人`，继续不猜改；未展示、未嵌入页图。报告：`output/reports/progress/20260706_高置信OCR错字补修第五十九批_工厂短片段.md`。
""".strip()


def main() -> None:
    text = MEMORY.read_text(encoding="utf-8")
    marker = "## 2026-07-06 高置信 OCR 错字补修第五十九批：工厂短片段"
    if marker in text:
        print("already_present=1")
        return
    sep = "" if text.endswith("\n") else "\n"
    MEMORY.write_text(text + sep + "\n" + NOTE + "\n", encoding="utf-8")
    print("appended=1")


if __name__ == "__main__":
    main()
