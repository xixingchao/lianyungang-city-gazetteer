# -*- coding: utf-8 -*-
"""Append Batch 49 note to PROJECT_MEMORY.md once."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MEMORY = ROOT / "PROJECT_MEMORY.md"

NOTE = """

## 2026-07-06 高置信 OCR 错字补修第四十九批：人大视察短片段
- 新增并运行 `scripts/repair_reader_high_confidence_ocr_typos_batch49_people_congress_short_20260706.py`，据本地 Tesseract OCR 文本修复主阅读版 3 个人大视察短片段。
- 本地 OCR 输入页图为 `workbench/conversion/page_images/中/part02/page_0516_180dpi.jpg`，文本输出为 `workbench/ocr/tesseract_check/zhong_part02_page_0516.txt`；未展示、未嵌入页图。
- 主要修复：补回 `1985年4月15~22日，组织市区人大代表对全市贯彻《水污染防治法》实施情况视察。`，修复 `薇河` -> `蔷薇河`，`新海发电广` -> `新海发电厂`。
- 边界：`考究评议`、`实地考究` 两套 OCR 仍同样识别，本批不猜改；检察段 `于部违法乱纪`、医学段 `麦粘肿/B2一微蛋白/LISR` 仍缺更强更正证据。报告：`output/reports/progress/20260706_高置信OCR错字补修第四十九批_人大视察短片段.md`。
""".strip()


def main() -> None:
    text = MEMORY.read_text(encoding="utf-8")
    marker = "## 2026-07-06 高置信 OCR 错字补修第四十九批：人大视察短片段"
    if marker in text:
        print("already_present=1")
        return
    sep = "" if text.endswith("\n") else "\n"
    MEMORY.write_text(text + sep + "\n" + NOTE + "\n", encoding="utf-8")
    print("appended=1")


if __name__ == "__main__":
    main()
