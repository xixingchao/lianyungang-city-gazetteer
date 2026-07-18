# -*- coding: utf-8 -*-
"""Append Batch 61 note to PROJECT_MEMORY.md once."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MEMORY = ROOT / "PROJECT_MEMORY.md"

NOTE = """

## 2026-07-06 高置信 OCR 错字补修第六十一批：户籍科并入
- 新增并运行 `scripts/repair_reader_high_confidence_ocr_typos_batch61_huji_into_20260706.py`，据 PaddleOCR/raw OCR 对照修复主阅读版 1 个短片段：`1965年，户籍科并人治安科` -> `1965年，户籍科并入治安科`。
- 证据页：`workbench/ocr/paddle_ocr/下/part01/page_0063.txt` 作 `户籍科并入治安科`；`workbench/ocr/raw/下/part01/page_0063.txt` 为 `并人` 残留。
- 边界：`检察机关并人公安机关` 本轮未找到同页强证据，继续不猜改；未展示、未嵌入页图。报告：`output/reports/progress/20260706_高置信OCR错字补修第六十一批_户籍科并入.md`。
""".strip()


def main() -> None:
    text = MEMORY.read_text(encoding="utf-8")
    marker = "## 2026-07-06 高置信 OCR 错字补修第六十一批：户籍科并入"
    if marker in text:
        print("already_present=1")
        return
    sep = "" if text.endswith("\n") else "\n"
    MEMORY.write_text(text + sep + "\n" + NOTE + "\n", encoding="utf-8")
    print("appended=1")


if __name__ == "__main__":
    main()
