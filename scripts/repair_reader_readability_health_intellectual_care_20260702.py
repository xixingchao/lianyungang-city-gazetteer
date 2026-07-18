# -*- coding: utf-8 -*-
"""Fix intellectual healthcare OCR typo from page OCR."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_health_intellectual_care_20260702.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_health_intellectual_care_20260702.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260702_第五十五卷知识分子保健错字修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SOURCE_NOTE = (
    "workbench/ocr/paddle_ocr/下/part02/page_0205.txt:29-36; "
    "workbench/body_chapters/连云港市志_全书_正文汇总.md:101489-101497; "
    "workbench/body_chapters/第五十二卷至第六十卷及附录（下part02）.md:8184-8192"
)
SCOPE_START = '<h4 id="第五十五卷-第五章保健疗养-第四节知识分子保健">第四节知识分子保健</h4>'
SCOPE_END = '<h4 id="第五十五卷-第五章保健疗养-第五节疗养">第五节疗养</h4>'
BAD = "眼球届光不正"
GOOD = "眼球屈光不正"


def find_scope(text: str) -> tuple[int, int]:
    start = text.index(SCOPE_START) + len(SCOPE_START)
    end = text.index(SCOPE_END, start)
    return start, end


def patch_reader() -> tuple[int, dict[str, int]]:
    text = HTML.read_text(encoding="utf-8")
    start, end = find_scope(text)
    segment = text[start:end]
    changed = int(BAD in segment)
    if changed:
        segment = segment.replace(BAD, GOOD)
        HTML.write_text(text[:start] + segment + text[end:], encoding="utf-8")

    text = HTML.read_text(encoding="utf-8")
    start, end = find_scope(text)
    segment = text[start:end]
    if GOOD not in segment:
        raise RuntimeError("intellectual care expected text missing")
    if BAD in segment:
        raise RuntimeError("intellectual care residue remains")
    return changed, {"typo_replacements": changed}


def write_reports(changed: int, counts: dict[str, int]) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "第五十五卷卫生 / 第五章保健疗养 / 第四节知识分子保健",
        "source": SOURCE_NOTE,
        "reader_path": str(HTML),
        "changes_this_run": changed,
        "counts": counts,
        "principle": "依据 PaddleOCR 页级文本修正单处 OCR 错字；未处理第五节疗养。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    md = f"""# 第五十五卷知识分子保健错字修复

- 时间：{now}
- 范围：`第五十五卷卫生 / 第五章保健疗养 / 第四节知识分子保健`
- 源文依据：`{SOURCE_NOTE}`

## 修复动作

- 修正 `眼球届光不正` 为 `眼球屈光不正`。
- 本次复跑新增替换：{changed} 处。
- 本轮未处理 `第五节疗养`。

## 核对说明

- PaddleOCR `page_0205.txt` 确认原文为 `眼球屈光不正`。
"""
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")


def update_memory(changed: int) -> None:
    marker = "## 2026-07-02 第五十五卷知识分子保健错字修复"
    memory = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker in memory:
        return
    entry = f"""
{marker}

- 对第五十五卷卫生第五章第四节 `知识分子保健` 进行单点回源修复。
- 源文依据：`{SOURCE_NOTE}`；修正 `眼球届光不正` 为 `眼球屈光不正`。
- 本轮新增替换 {changed} 处；`第五节疗养` 未在本脚本中处理。
- 报告：`output/reports/reader_readability_health_intellectual_care_20260702.md`。
"""
    MEMORY.write_text(memory.rstrip() + "\n\n" + entry.lstrip(), encoding="utf-8")


def main() -> None:
    changed, counts = patch_reader()
    write_reports(changed, counts)
    update_memory(changed)
    print("intellectual care section repaired")
    print(f"changes={changed}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()
