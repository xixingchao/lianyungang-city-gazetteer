# -*- coding: utf-8 -*-
"""Append Batch 60 note to PROJECT_MEMORY.md once."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MEMORY = ROOT / "PROJECT_MEMORY.md"

NOTE = """

## 2026-07-06 高置信 OCR 错字补修第六十批：ISBN 与并入短片段
- 新增并运行 `scripts/repair_reader_high_confidence_ocr_typos_batch60_isbn_into_short_20260706.py`，据同书版权页 PaddleOCR 与正文 OCR 对照修复主阅读版 3 个短片段。
- 主要修复：卷末 `80124ISBN...（上中，下三明精装）` 归正为 `ISBN...（上、中、下三册精装）`；书末 `编繁委员会/TSBN/$71` 归正为 `编纂委员会/ISBN/571`；线性表残留 `夹山并人东华汽` 改为 `夹山并入东华汽`。
- 证据页：`workbench/ocr/paddle_ocr/上/part01/page_0003.txt`、`workbench/ocr/paddle_ocr/上/part02/page_0002.txt`、`workbench/ocr/paddle_ocr/上/part03/page_0002.txt`、`workbench/ocr/raw/上/part02/page_0071.txt`、`workbench/ocr/paddle_ocr/merged/连云港市志_上_part02_PaddleOCR汇总.md`。
- 边界：书末版权信息只归正字符误识别，不重排版式；`避选` 等书末词双源证据仍弱，本批不猜改；未展示、未嵌入页图。报告：`output/reports/progress/20260706_高置信OCR错字补修第六十批_ISBN并入短片段.md`。
""".strip()


def main() -> None:
    text = MEMORY.read_text(encoding="utf-8")
    marker = "## 2026-07-06 高置信 OCR 错字补修第六十批：ISBN 与并入短片段"
    if marker in text:
        print("already_present=1")
        return
    sep = "" if text.endswith("\n") else "\n"
    MEMORY.write_text(text + sep + "\n" + NOTE + "\n", encoding="utf-8")
    print("appended=1")


if __name__ == "__main__":
    main()
