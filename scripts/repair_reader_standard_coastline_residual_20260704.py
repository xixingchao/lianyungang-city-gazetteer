# -*- coding: utf-8 -*-
"""Repair reader-only standard coastline OCR residual."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_standard_coastline_residual_20260704.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_standard_coastline_residual_20260704.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260704_标准海岸线错识残留回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

OLD = "标淮海岸线长"
NEW = "标准海岸线长"
EVIDENCE = [
    "workbench/body_chapters/连云港市志_全书_正文汇总.md:1580",
    "workbench/body_chapters/连云港市志_全书_正文汇总.md:5093",
    "workbench/ocr/paddle_ocr/merged/连云港市志_上册_PaddleOCR汇总.md:2380,6028",
]


def append_once(path: Path, marker: str, content: str) -> None:
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker not in old:
        path.write_text(old.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")


def main() -> None:
    text = HTML.read_text(encoding="utf-8")
    count = text.count(OLD)
    if count:
        text = text.replace(OLD, NEW)
        HTML.write_text(text, encoding="utf-8")
    verify = HTML.read_text(encoding="utf-8")
    if OLD in verify or NEW not in verify:
        raise RuntimeError("standard coastline replacement verification failed")

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "标准海岸线错识残留回源修复",
        "reader_path": str(HTML),
        "old": OLD,
        "new": NEW,
        "replacements": count,
        "evidence": EVIDENCE,
        "principle": "仅修复主阅读版中与正文源、PaddleOCR 汇总不一致的 `标淮海岸线` 残留。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    report = f"""# 标准海岸线错识残留回源修复

- 时间：{now}
- 阅读器：`{HTML}`
- 修复：`{OLD}` → `{NEW}`。
- 替换：{count} 处。
- 证据：{'；'.join(f'`{item}`' for item in EVIDENCE)}。
- 原则：仅修复主阅读版中与正文源、PaddleOCR 汇总不一致的残留。
"""
    REPORT_MD.write_text(report, encoding="utf-8")
    PROGRESS.write_text(report, encoding="utf-8")

    marker = "## 2026-07-04 标准海岸线错识残留回源修复"
    memory = f"""
{marker}
- 依据正文源和上册 PaddleOCR 汇总，修复主阅读版 `标淮海岸线长` 为 `标准海岸线长`，共 {count} 处。
- 正文源已为 `标准海岸线`，本批只改 `output/final_reader/连云港市志_全书.html`。
- 报告：`output/reports/reader_standard_coastline_residual_20260704.md`。
"""
    append_once(MEMORY, marker, memory)
    print(json.dumps({"replacements": count, "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
