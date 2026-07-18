# -*- coding: utf-8 -*-
"""Append Batch 50 note to PROJECT_MEMORY.md once."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MEMORY = ROOT / "PROJECT_MEMORY.md"

NOTE = """

## 2026-07-06 高置信 OCR 错字补修第五十批：学校与人物短片段
- 新增并运行 `scripts/repair_reader_high_confidence_ocr_typos_batch50_schools_people_20260706.py`，据 PaddleOCR 与同章结构化表证据修复主阅读版 4 个短片段。
- 主要修复：`蕃薇中学、陇东中学` -> `蔷薇中学、陇东中学`，`连云6港市蕃薇中学` -> `连云港市蔷薇中学`，`导淮入江人海之研究` -> `导淮入江入海之研究`，`泗、沂、述分治合治之研究` -> `泗、沂、沭分治合治之研究`。
- 证据页：`workbench/ocr/paddle_ocr/下/part01/page_0375.txt`，`workbench/ocr/paddle_ocr/下/part02/page_0229.txt`，`workbench/ocr/paddle_ocr/下/part02/page_0350.txt`；同章表格 `LYG-下-T054/T057` 亦作 `蔷薇中学`。
- 边界：`新浦据蓄薇河` 等附录古文段源证不足，本批不猜改；未展示、未嵌入页图。报告：`output/reports/progress/20260706_高置信OCR错字补修第五十批_学校与人物短片段.md`。
""".strip()


def main() -> None:
    text = MEMORY.read_text(encoding="utf-8")
    marker = "## 2026-07-06 高置信 OCR 错字补修第五十批：学校与人物短片段"
    if marker in text:
        print("already_present=1")
        return
    sep = "" if text.endswith("\n") else "\n"
    MEMORY.write_text(text + sep + "\n" + NOTE + "\n", encoding="utf-8")
    print("appended=1")


if __name__ == "__main__":
    main()
