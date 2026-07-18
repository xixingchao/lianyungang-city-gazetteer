# -*- coding: utf-8 -*-
"""Append Batch 54 note to PROJECT_MEMORY.md once."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MEMORY = ROOT / "PROJECT_MEMORY.md"

NOTE = """

## 2026-07-06 高置信 OCR 错字补修第五十四批：工业厂名短片段
- 新增并运行 `scripts/repair_reader_high_confidence_ocr_typos_batch54_industry_factory_short_20260706.py`，据 PaddleOCR/raw OCR 对照修复主阅读版 3 个工业厂名短片段。
- 主要修复：`新海电厂附属电机广` -> `新海电厂附属电机厂`，`海州电器广` -> `海州电器厂`，`东辛农场水泥预制广、新浦区水泥制品广` -> `东辛农场水泥预制厂、新浦区水泥制品厂`。
- 证据页：`workbench/ocr/paddle_ocr/中/part01/page_0218.txt`、`workbench/ocr/raw/中/part01/page_0218.txt`、`workbench/ocr/paddle_ocr/中/part01/page_0219.txt`、`workbench/ocr/raw/中/part01/page_0219.txt`、`workbench/ocr/paddle_ocr/中/part01/page_0282.txt`、`workbench/ocr/raw/中/part01/page_0282.txt`。
- 边界：其他 `广` 字样未取得同页证据闭合，本批不处理；未展示、未嵌入页图。报告：`output/reports/progress/20260706_高置信OCR错字补修第五十四批_工业厂名短片段.md`。
""".strip()


def main() -> None:
    text = MEMORY.read_text(encoding="utf-8")
    marker = "## 2026-07-06 高置信 OCR 错字补修第五十四批：工业厂名短片段"
    if marker in text:
        print("already_present=1")
        return
    sep = "" if text.endswith("\n") else "\n"
    MEMORY.write_text(text + sep + "\n" + NOTE + "\n", encoding="utf-8")
    print("appended=1")


if __name__ == "__main__":
    main()
