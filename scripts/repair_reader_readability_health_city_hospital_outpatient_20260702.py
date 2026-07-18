# -*- coding: utf-8 -*-
"""Split outpatient management headings in city hospital management."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_health_city_hospital_outpatient_20260702.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_health_city_hospital_outpatient_20260702.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260702_第五十五卷城市医院门诊管理标题修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SOURCE_NOTE = (
    "workbench/body_chapters/连云港市志_全书_正文汇总.md:101062-101088; "
    "workbench/body_chapters/第五十二卷至第六十卷及附录（下part02）.md:7759-7784; "
    "workbench/ocr/paddle_ocr/下/part02/page_0194.txt"
)
SCOPE_START = '<h4 id="第五十五卷-第四章医政 药政-第三节城市医院管理">第三节城市医院管理</h4>'
SCOPE_END_OPTIONS = ('<p>二、病区管理', '<p><strong>二、病区管理</strong></p>')

REPLACEMENTS: list[tuple[str, str, str]] = [
    (
        "一、门诊管理与管理体制标题",
        "<p>一、门诊管理管理体制民国期间，义德医院",
        "<p><strong>一、门诊管理</strong></p>\n<p><strong>管理体制</strong></p>\n<p>民国期间，义德医院",
    ),
    ("管理制度标题", "<p>管理制度民国期间，市内", "<p><strong>管理制度</strong></p>\n<p>民国期间，市内"),
]

EXPECTED_TEXT = [
    "<p><strong>一、门诊管理</strong></p>",
    "<p><strong>管理体制</strong></p>",
    "<p><strong>管理制度</strong></p>",
]
RESIDUALS = ["一、门诊管理管理体制", "<p>管理制度民国期间"]


def find_scope(text: str) -> tuple[int, int]:
    start = text.index(SCOPE_START)
    ends = [text.find(marker, start) for marker in SCOPE_END_OPTIONS]
    valid_ends = [end for end in ends if end != -1]
    if not valid_ends:
        raise RuntimeError("city hospital outpatient scope end not found")
    return start, min(valid_ends)


def patch_segment(segment: str) -> tuple[str, int, dict[str, int]]:
    changed = 0
    counts: dict[str, int] = {}
    for label, needle, replacement in REPLACEMENTS:
        count = segment.count(needle)
        if count:
            segment = segment.replace(needle, replacement)
            counts[label] = count
            changed += count

    missing = [text for text in EXPECTED_TEXT if text not in segment]
    if missing:
        raise RuntimeError(f"city hospital outpatient headings missing: {missing}")
    remaining = [marker for marker in RESIDUALS if marker in segment]
    if remaining:
        raise RuntimeError(f"city hospital outpatient residue remains: {remaining}")
    return segment, changed, counts


def patch_reader() -> tuple[int, dict[str, int]]:
    text = HTML.read_text(encoding="utf-8")
    start, end = find_scope(text)
    segment = text[start:end]
    new_segment, changed, counts = patch_segment(segment)
    if new_segment != segment:
        HTML.write_text(text[:start] + new_segment + text[end:], encoding="utf-8")
    return changed, counts


def write_reports(changed: int, counts: dict[str, int]) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "第五十五卷卫生 / 第四章医政 药政 / 第三节城市医院管理 / 一、门诊管理",
        "source": SOURCE_NOTE,
        "reader_path": str(HTML),
        "changes_this_run": changed,
        "counts": counts,
        "principle": "依据 PaddleOCR 页级文本拆分门诊管理小节及分项标题；未处理二、病区管理。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    md = f"""# 第五十五卷城市医院门诊管理标题修复

- 时间：{now}
- 范围：`第五十五卷卫生 / 第四章医政 药政 / 第三节城市医院管理 / 一、门诊管理`
- 源文依据：`{SOURCE_NOTE}`

## 修复动作

- 拆分 `一、门诊管理` 小节标题。
- 拆分 `管理体制`、`管理制度` 两个分项标题。
- 本次复跑新增替换：{changed} 处。
- 本轮未处理 `二、病区管理`。

## 核对说明

- PaddleOCR `page_0194.txt` 确认 `第三节城市医院管理`、`一、门诊管理`、`管理体制`、`管理制度` 及 `二、病区管理` 边界。
"""
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")


def update_memory(changed: int) -> None:
    marker = "## 2026-07-02 第五十五卷城市医院门诊管理标题修复"
    memory = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker in memory:
        return
    entry = f"""
{marker}

- 对第五十五卷卫生第四章第三节 `城市医院管理` 的 `一、门诊管理` 进行回源修复。
- 源文依据：`{SOURCE_NOTE}`；拆分 `一、门诊管理`、`管理体制`、`管理制度` 标题。
- 本轮新增替换 {changed} 处；`二、病区管理` 未在本脚本中处理。
- 报告：`output/reports/reader_readability_health_city_hospital_outpatient_20260702.md`。
"""
    MEMORY.write_text(memory.rstrip() + "\n\n" + entry.lstrip(), encoding="utf-8")


def main() -> None:
    changed, counts = patch_reader()
    write_reports(changed, counts)
    update_memory(changed)
    print("city hospital outpatient section repaired")
    print(f"changes={changed}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()
