# -*- coding: utf-8 -*-
"""Append Batch 65 note to PROJECT_MEMORY.md once."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MEMORY = ROOT / "PROJECT_MEMORY.md"

NOTE = """
## 2026-07-06 高置信 OCR 错字补修第六十五批：牺牲、业务短片段
- 新增并运行 `scripts/repair_reader_high_confidence_ocr_typos_batch65_sacrifice_business_20260706.py`，据本地 Tesseract OCR、raw OCR 与同句/同段上下文修复主阅读版 5 个短片段。
- 主要修复：4 处 `栖牲` -> `牺牲`（吕祥璧烈士纪念亭、朱环烈士、烈士表华川战斗、书末跋文 `不怕牺牲`），以及 `修志理论与业.务知识` -> `修志理论与业务知识`。
- 证据文本：`workbench/ocr/tesseract_check/book_end_20260706/page_0475_tess.txt` 作 `不怕牺牲`；`workbench/ocr/raw/下/part02/page_0476.txt` 断行为 `业/.务知识` 且同句后文作 `业务问题`；同句碑文作 `吕祥璧烈士牺牲处`。
- 边界：`避选`、`上尽，然长逝`、`票高献身精神` 等仍缺稳定文本证据，本批不猜改。报告：`output/reports/progress/20260706_高置信OCR错字补修第六十五批_牺牲业务短片段.md`。
""".strip()


def main() -> None:
    text = MEMORY.read_text(encoding="utf-8")
    marker = "## 2026-07-06 高置信 OCR 错字补修第六十五批：牺牲、业务短片段"
    if marker in text:
        print("already_present=1")
        return
    sep = "" if text.endswith("\n") else "\n"
    MEMORY.write_text(text + sep + "\n" + NOTE + "\n", encoding="utf-8")
    print("appended=1")


if __name__ == "__main__":
    main()
