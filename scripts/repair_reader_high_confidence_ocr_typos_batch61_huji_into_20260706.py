# -*- coding: utf-8 -*-
"""Batch 61: verified 户籍科并入 short fix."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT = ROOT / "output" / "reports" / "progress" / "20260706_高置信OCR错字补修第六十一批_户籍科并入.md"

OLD = "1965年，户籍科并人治安科"
NEW = "1965年，户籍科并入治安科"


def main() -> None:
    html = HTML.read_text(encoding="utf-8")
    count = html.count(OLD)
    if count != 1:
        raise RuntimeError(f"expected 1 hit, found {count}: {OLD}")
    HTML.write_text(html.replace(OLD, NEW), encoding="utf-8")
    text = f"""# 高置信 OCR 错字补修第六十一批：户籍科并入

> 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}

## 修复项

- 市公安局机构沿革段：`{OLD}` -> `{NEW}`（命中 1 处）
  - 证据：`workbench/ocr/paddle_ocr/下/part01/page_0063.txt:32` 作 `户籍科并入治安科`
  - 证据：`workbench/ocr/raw/下/part01/page_0063.txt:30` 为 `户籍科并人治安科` 残留

## 边界

- 只修主阅读版，不改 OCR 原文。
- `检察机关并人公安机关` 本轮未找到同页强证据，继续不猜改。
- 未展示、未嵌入页图。
"""
    REPORT.write_text(text, encoding="utf-8")
    print("changed=1")
    print(f"progress={REPORT}")


if __name__ == "__main__":
    main()
