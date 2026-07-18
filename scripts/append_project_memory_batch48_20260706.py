# -*- coding: utf-8 -*-
"""Append Batch 48 note to PROJECT_MEMORY.md once."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MEMORY = ROOT / "PROJECT_MEMORY.md"

NOTE = """

## 2026-07-06 高置信 OCR 错字补修第四十八批：石灰厂与医学短片段
- 新增并运行 `scripts/repair_reader_high_confidence_ocr_typos_batch48_lime_medical_short_20260706.py`，据页级 PaddleOCR 对照修复主阅读版 4 个石灰厂与医学短片段。
- 石灰厂段证据为中册 `workbench/ocr/paddle_ocr/中/part01/page_0278.txt`、`page_0279.txt`，修复 `市石灰广为扩大生产`、`烟简`、`沟石灰厂`、`市第建筑公司/进行商` 等残留。
- 医学检验段证据为下册 `workbench/ocr/paddle_ocr/下/part02/page_0188.txt`，修复 `丙酮酸嗨测定` -> `丙酮酸晦测定`。
- 边界：`于部违法乱纪`、`麦粘肿`、`B2一微蛋白`、`LISR` 等页级 OCR 仍未给出更正证据，本批不处理；未展示、未嵌入页图。报告：`output/reports/progress/20260706_高置信OCR错字补修第四十八批_石灰厂与医学短片段.md`。
""".strip()


def main() -> None:
    text = MEMORY.read_text(encoding="utf-8")
    marker = "## 2026-07-06 高置信 OCR 错字补修第四十八批：石灰厂与医学短片段"
    if marker in text:
        print("already_present=1")
        return
    sep = "" if text.endswith("\n") else "\n"
    MEMORY.write_text(text + sep + "\n" + NOTE + "\n", encoding="utf-8")
    print("appended=1")


if __name__ == "__main__":
    main()
