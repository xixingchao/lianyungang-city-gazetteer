# -*- coding: utf-8 -*-
"""Append book-end pending hard-point note to PROJECT_MEMORY.md once."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MEMORY = ROOT / "PROJECT_MEMORY.md"

NOTE = """
## 2026-07-06 书末剩余硬点待核记录
- 新增 `output/reports/progress/20260706_书末剩余硬点待核记录.md`，记录书末现代页仍未修正文的两个硬点：`避选` 与 `上尽，然长逝`。
- `避选`：raw 作 `避选`，Tesseract `--psm 6` 作 `遂选`，`--psm 11` 作 `迟选`，语义疑似 `遴选` 但证据未闭合，暂不改。
- `上尽，然长逝`：raw 断行为 `征途/上尽，然长逝`，Tesseract 该行乱码，暂不改。
- 页图仅记录本地路径供后续人工核对：`workbench/conversion/page_images/下/part02/page_0476_180dpi.jpg`、`workbench/conversion/page_images/下/part02/page_0478_180dpi.jpg`；未展示、未嵌入图片。
""".strip()


def main() -> None:
    text = MEMORY.read_text(encoding="utf-8")
    marker = "## 2026-07-06 书末剩余硬点待核记录"
    if marker in text:
        print("already_present=1")
        return
    sep = "" if text.endswith("\n") else "\n"
    MEMORY.write_text(text + sep + "\n" + NOTE + "\n", encoding="utf-8")
    print("appended=1")


if __name__ == "__main__":
    main()
