# -*- coding: utf-8 -*-
"""Repair one source-backed pre-Qing war subhead boundary in volume 45."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_volume45_military_pre_qing_war_subhead_20260705.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_volume45_military_pre_qing_war_subhead_20260705.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260705_第四十五卷军事清以前战事标题边界补修.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"
SOURCE = "workbench/body_chapters/第四十三卷至第五十一卷（下part01）.md:8817"

OLD = "<p>一、清以前战事齐莒纪彰之战鲁昭公十九年（前523年），"
NEW = "<h5>一、清以前战事</h5>\n<p>齐莒纪彰之战鲁昭公十九年（前523年），"


def append_once(path: Path, marker: str, content: str) -> None:
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker not in old:
        path.write_text(old.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")


def main() -> None:
    text = HTML.read_text(encoding="utf-8")
    count = text.count(OLD)
    if count != 1:
        raise RuntimeError(f"expected one match for 一、清以前战事, got {count}")
    HTML.write_text(text.replace(OLD, NEW, 1), encoding="utf-8")

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "第四十五卷军事：第二节战事",
        "html_boundaries_fixed": 1,
        "fixed": [{"heading": "一、清以前战事", "source": SOURCE}],
        "notes": ["仅拆分源文独立编号子目标题；不拆分正文内战役名。"],
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    md = f"""# 第四十五卷军事清以前战事标题边界补修

- 时间：{now}
- 范围：第四十五卷军事，第一章第二节战事。
- 本次修复边界：1 处。

## 修复

- `一、清以前战事`（依据 `{SOURCE}`）

## 说明

- 仅拆出源文独立编号子目标题。
- `齐莒纪彰之战` 等战役名保留为正文内条目，不扩大改动范围。
"""
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")

    marker = "## 2026-07-05 第四十五卷军事清以前战事标题边界补修"
    append_once(
        MEMORY,
        marker,
        f"""
{marker}
- 修复第四十五卷军事第一章第二节战事 1 处编号子目标题边界：`一、清以前战事`。
- 依据 `{SOURCE}` 源文独立标题行；不拆分正文内战役名。
- 报告：`output/reports/reader_readability_volume45_military_pre_qing_war_subhead_20260705.md`。
""",
    )
    print("html_boundaries_fixed=1")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()
