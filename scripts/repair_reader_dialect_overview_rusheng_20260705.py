# -*- coding: utf-8 -*-
"""Source-backed fix for a dialect overview OCR slip."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_dialect_overview_rusheng_20260705.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_dialect_overview_rusheng_20260705.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260705_第五十九卷方言概述入声错识修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SOURCE = "workbench/ocr/paddle_ocr/下/part02/page_0295.txt"
SCOPE_START = '<h3 id="第五十九卷-概述">概述</h3>'
SCOPE_END = '<h3 id="第五十九卷-第一章方言差别">第一章方言差别</h3>'
OLD = "越往北的村庄人声字越少"
NEW = "越往北的村庄入声字越少"


def append_once(path: Path, marker: str, content: str) -> None:
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker not in old:
        path.write_text(old.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")


def main() -> None:
    html = HTML.read_text(encoding="utf-8")
    start = html.index(SCOPE_START)
    end = html.index(SCOPE_END, start)
    segment = html[start:end]
    count = segment.count(OLD)
    if count != 1:
        raise RuntimeError(f"expected one occurrence, got {count}: {OLD}")
    segment = segment.replace(OLD, NEW, 1)
    HTML.write_text(html[:start] + segment + html[end:], encoding="utf-8")

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "第五十九卷方言 / 概述",
        "source": SOURCE,
        "changes": [{"old": OLD, "new": NEW}],
        "principle": "仅修复 PaddleOCR page_0295 明确支持的一处入声错识，不处理音标表。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    md = f"""# 第五十九卷方言概述入声错识修复

- 时间：{now}
- 范围：第五十九卷方言 / 概述。
- 源文依据：`{SOURCE}`。

## 修复

- `{OLD}` -> `{NEW}`。

## 原则

只修复 page_0295 PaddleOCR 明确支持的一处错识；不处理后续声韵调音标表中的不确定符号。
"""
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")

    marker = "## 2026-07-05 第五十九卷方言概述入声错识修复"
    append_once(
        MEMORY,
        marker,
        f"""
{marker}
- 依据 `{SOURCE}` 修复第五十九卷方言概述一处 `人声字` -> `入声字`。
- 未处理声韵调音标表内证据不足的符号错识。
- 报告：`output/reports/reader_dialect_overview_rusheng_20260705.md`。
""",
    )

    print("dialect_overview_rusheng_repaired")
    print("changes=1")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()
