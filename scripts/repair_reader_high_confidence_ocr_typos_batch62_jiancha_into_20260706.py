# -*- coding: utf-8 -*-
"""Batch 62: verified 检察机关并入 short fix."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT = ROOT / "output" / "reports" / "progress" / "20260706_高置信OCR错字补修第六十二批_检察机关并入.md"

OLD = "19581961年，检察机关并人公安机关"
NEW = "1958~1961年，检察机关并入公安机关"


def main() -> None:
    html = HTML.read_text(encoding="utf-8")
    count = html.count(OLD)
    if count != 1:
        raise RuntimeError(f"expected 1 hit, found {count}: {OLD}")
    HTML.write_text(html.replace(OLD, NEW), encoding="utf-8")
    text = f"""# 高置信 OCR 错字补修第六十二批：检察机关并入

> 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}

## 修复项

- 经济检察沿革段：`{OLD}` -> `{NEW}`（命中 1 处）
  - 证据：`workbench/ocr/paddle_ocr/下/part01/page_0107.txt:15-16` 作 `1958~1961年，检察机关并入公安机关，经济检察随之停止`
  - 证据：`workbench/ocr/raw/下/part01/page_0107.txt:15-16` 为 `19581961年，检察机关并人公安机关` 残留

## 边界

- 只修主阅读版，不改 OCR 原文。
- `劳改队撤销，并人徐州第四监狱` 双源仍作 `并人`，继续不猜改。
- 未展示、未嵌入页图。
"""
    REPORT.write_text(text, encoding="utf-8")
    print("changed=1")
    print(f"progress={REPORT}")


if __name__ == "__main__":
    main()
