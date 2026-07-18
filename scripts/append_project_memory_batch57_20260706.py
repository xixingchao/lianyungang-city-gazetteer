# -*- coding: utf-8 -*-
"""Append Batch 57 note to PROJECT_MEMORY.md once."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MEMORY = ROOT / "PROJECT_MEMORY.md"

NOTE = """

## 2026-07-06 高置信 OCR 错字补修第五十七批：并入短片段
- 新增并运行 `scripts/repair_reader_high_confidence_ocr_typos_batch57_more_into_short_20260706.py`，据 PaddleOCR/raw OCR 对照修复主阅读版 5 个 `并人/并入` 短片段。
- 主要修复：`盐务局公安科并人盐区公安分局`、`并人成人中专/成人高校`、`江苏省立第八师范学校并人江苏省立十中学`、`并人灌云师范学校`、`并人赣榆县师范学校` 均改为 `并入`。
- 证据页：`workbench/ocr/paddle_ocr/下/part01/page_0064.txt`、`workbench/ocr/raw/下/part01/page_0064.txt`、`workbench/ocr/paddle_ocr/下/part01/page_0397.txt`、`workbench/ocr/raw/下/part01/page_0397.txt`、`workbench/ocr/paddle_ocr/下/part01/page_0387.txt`、`workbench/ocr/raw/下/part01/page_0387.txt`、`workbench/ocr/paddle_ocr/下/part01/page_0401.txt`、`workbench/ocr/raw/下/part01/page_0401.txt`。
- 边界：劳改队撤销并入徐州第四监狱一处 PaddleOCR 仍作 `并人`，本批不猜改；未展示、未嵌入页图。报告：`output/reports/progress/20260706_高置信OCR错字补修第五十七批_并入短片段.md`。
""".strip()


def main() -> None:
    text = MEMORY.read_text(encoding="utf-8")
    marker = "## 2026-07-06 高置信 OCR 错字补修第五十七批：并入短片段"
    if marker in text:
        print("already_present=1")
        return
    sep = "" if text.endswith("\n") else "\n"
    MEMORY.write_text(text + sep + "\n" + NOTE + "\n", encoding="utf-8")
    print("appended=1")


if __name__ == "__main__":
    main()
