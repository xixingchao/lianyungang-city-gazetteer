# -*- coding: utf-8 -*-
"""Append Batch 66 note to PROJECT_MEMORY.md once."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MEMORY = ROOT / "PROJECT_MEMORY.md"

NOTE = """
## 2026-07-06 高置信 OCR 错字补修第六十六批：字间点残留短片段
- 新增并运行 `scripts/repair_reader_high_confidence_ocr_typos_batch66_dot_residue_20260706.py`，据 raw/Paddle OCR 与同段术语修复主阅读版 7 个唯一命中的短片段。
- 主要修复：`市罐头食品广` -> `市罐头食品厂`、`时产时.停` -> `时产时停`、`基础.上` -> `基础上`、`企业8家.生产` -> `企业8家，生产`、`建筑.石材` -> `建筑石材`、`协作.产品` -> `协作产品`、`市交警.大队` -> `市交警大队`。
- 证据文本：`workbench/ocr/paddle_ocr/中/part01/page_0076.txt`、`workbench/ocr/paddle_ocr/中/part01/page_0238.txt`、`workbench/ocr/raw/中/part01/page_0290.txt`、`workbench/ocr/paddle_ocr/中/part02/page_0336.txt`、`workbench/ocr/paddle_ocr/下/part01/page_0088.txt`。
- 边界：`票高献身精神`、`用破万人心`、`避选`、`上尽，然长逝` 仍缺稳定文本证据，本批不猜改。报告：`output/reports/progress/20260706_高置信OCR错字补修第六十六批_字间点残留短片段.md`。
""".strip()


def main() -> None:
    text = MEMORY.read_text(encoding="utf-8")
    marker = "## 2026-07-06 高置信 OCR 错字补修第六十六批：字间点残留短片段"
    if marker in text:
        print("already_present=1")
        return
    sep = "" if text.endswith("\n") else "\n"
    MEMORY.write_text(text + sep + "\n" + NOTE + "\n", encoding="utf-8")
    print("appended=1")


if __name__ == "__main__":
    main()
