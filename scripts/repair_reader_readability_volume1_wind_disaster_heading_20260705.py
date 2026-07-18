# -*- coding: utf-8 -*-
"""Repair the remaining source-backed wind-disaster section heading."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_volume1_wind_disaster_heading_20260705.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_volume1_wind_disaster_heading_20260705.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260705_第一卷风灾节标题边界补修.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

OLD = "<p>第三节风灾市境年平均风速为3米/秒。"
NEW = "<h4>第三节 风灾</h4>\n<p>市境年平均风速为3米/秒。"
SOURCE_LINES = [
    "workbench/body_chapters/paddle_上/第一卷_自然环境.md:6157-6159",
    "workbench/indexes/连云港市志_全书_章节骨架.md:66",
]


def append_once(path: Path, marker: str, content: str) -> None:
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker not in old:
        path.write_text(old.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")


def main() -> None:
    text = HTML.read_text(encoding="utf-8")
    count = text.count(OLD)
    if count != 1:
        raise RuntimeError(f"expected one wind disaster match, got {count}")
    HTML.write_text(text.replace(OLD, NEW, 1), encoding="utf-8")

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "第一卷自然灾害第三节风灾标题边界",
        "section_boundaries_fixed": 1,
        "source_evidence": SOURCE_LINES,
        "notes": ["仅恢复 `第三节 风灾` 标题边界，不改正文文字。"],
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    md = f"""# 第一卷风灾节标题边界补修

- 时间：{now}
- 范围：第一卷自然环境，第八章自然灾害第三节。
- 本次恢复节标题边界：1 处。

## 修复

- 将 `第三节风灾` 从段首粘连中恢复为独立 `第三节 风灾` 标题。
- 仅恢复标题边界，不改正文文字。

## 依据

"""
    md += "".join(f"- `{line}`\n" for line in SOURCE_LINES)
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")

    marker = "## 2026-07-05 第一卷风灾节标题边界补修"
    append_once(
        MEMORY,
        marker,
        f"""
{marker}
- 修复第一卷自然环境第八章自然灾害 `第三节 风灾` 标题粘正文问题。
- 依据 `workbench/body_chapters/paddle_上/第一卷_自然环境.md:6157-6159` 与章节骨架确认标题。
- 报告：`output/reports/reader_readability_volume1_wind_disaster_heading_20260705.md`。
""",
    )
    print("section_boundaries_fixed=1")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()
