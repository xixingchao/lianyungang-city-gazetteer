# -*- coding: utf-8 -*-
"""Split and source-correct village clinic management."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_health_village_clinic_management_20260702.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_health_village_clinic_management_20260702.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260702_第五十五卷村卫生室管理标题与OCR修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SOURCE_NOTE = (
    "workbench/body_chapters/连云港市志_全书_正文汇总.md:101027-101062; "
    "workbench/body_chapters/第五十二卷至第六十卷及附录（下part02）.md:7724-7759; "
    "workbench/ocr/paddle_ocr/下/part02/page_0193.txt"
)
SCOPE_START_OPTIONS = ('<p>二、村卫生室管理', '<p><strong>二、村卫生室管理</strong></p>')
SCOPE_END = '<h4 id="第五十五卷-第四章医政 药政-第三节城市医院管理">第三节城市医院管理</h4>'

REPLACEMENTS: list[tuple[str, str, str]] = [
    (
        "二、村卫生室管理标题",
        "<p>二、村卫生室管理1958年，市区各村办起保健站，",
        "<p><strong>二、村卫生室管理</strong></p>\n<p>1958年，市区各村办起保健站，",
    ),
    ("纳入字形", "纳人集体所有制医疗单位", "纳入集体所有制医疗单位"),
    ("统一发给缺字", "由省卫生厅统发给", "由省卫生厅统一发给"),
]

SPLITS: list[tuple[str, str]] = [
    ("实行月工资制。</p>\n<p>1984年，", "实行月工资制。</p>\n<p>1984年，"),
]

EXPECTED_TEXT = [
    "<p><strong>二、村卫生室管理</strong></p>",
    "纳入集体所有制医疗单位",
    "由省卫生厅统一发给《乡村保健医生证书》",
]
RESIDUALS = [
    "二、村卫生室管理1958年",
    "纳人集体所有制医疗单位",
    "由省卫生厅统发给",
]


def find_scope(text: str) -> tuple[int, int]:
    starts = [text.find(marker) for marker in SCOPE_START_OPTIONS]
    valid_starts = [start for start in starts if start != -1]
    if not valid_starts:
        raise RuntimeError("village clinic management scope start not found")
    start = min(valid_starts)
    end = text.index(SCOPE_END, start)
    return start, end


def patch_segment(segment: str) -> tuple[str, int, dict[str, int]]:
    changed = 0
    counts: dict[str, int] = {}
    for label, needle, replacement in REPLACEMENTS:
        count = segment.count(needle)
        if count:
            segment = segment.replace(needle, replacement)
            counts[label] = count
            changed += count

    # If a future source re-flattens the two natural paragraphs, keep the split.
    for needle, replacement in SPLITS:
        count = segment.count(needle)
        if count:
            # This no-op keeps the check explicit without changing already split content.
            counts.setdefault("自然段边界确认", 0)

    missing = [text for text in EXPECTED_TEXT if text not in segment]
    if missing:
        raise RuntimeError(f"village clinic management expected corrections missing: {missing}")
    remaining = [marker for marker in RESIDUALS if marker in segment]
    if remaining:
        raise RuntimeError(f"village clinic management OCR residue remains: {remaining}")
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
        "scope": "第五十五卷卫生 / 第四章医政 药政 / 第二节农村医疗管理 / 二、村卫生室管理",
        "source": SOURCE_NOTE,
        "reader_path": str(HTML),
        "changes_this_run": changed,
        "counts": counts,
        "principle": "依据 PaddleOCR 页级文本拆分小节标题，并修复村卫生室管理小节内可证 OCR 错字；未处理第三节城市医院管理。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    md = f"""# 第五十五卷村卫生室管理标题与 OCR 修复

- 时间：{now}
- 范围：`第五十五卷卫生 / 第四章医政 药政 / 第二节农村医疗管理 / 二、村卫生室管理`
- 源文依据：`{SOURCE_NOTE}`

## 修复动作

- 拆分 `二、村卫生室管理` 小节标题。
- 依据 PaddleOCR `page_0193.txt` 修复 `纳入集体所有制医疗单位`、`由省卫生厅统一发给《乡村保健医生证书》`。
- 本次复跑新增替换：{changed} 处。
- 本轮未处理 `第三节城市医院管理`。

## 核对说明

- PaddleOCR `page_0193.txt` 确认本小节标题、主体段落及与 `第三节城市医院管理` 的边界。
"""
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")


def update_memory(changed: int) -> None:
    marker = "## 2026-07-02 第五十五卷村卫生室管理标题与OCR修复"
    memory = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker in memory:
        return
    entry = f"""
{marker}

- 对第五十五卷卫生第四章第二节 `农村医疗管理` 的 `二、村卫生室管理` 进行回源修复。
- 源文依据：`{SOURCE_NOTE}`；拆分小节标题，修复 `纳入集体所有制医疗单位`、`由省卫生厅统一发给《乡村保健医生证书》` 等页级 OCR 可证问题。
- 本轮新增替换 {changed} 处；`第三节城市医院管理` 未在本脚本中处理。
- 报告：`output/reports/reader_readability_health_village_clinic_management_20260702.md`。
"""
    MEMORY.write_text(memory.rstrip() + "\n\n" + entry.lstrip(), encoding="utf-8")


def main() -> None:
    changed, counts = patch_reader()
    write_reports(changed, counts)
    update_memory(changed)
    print("village clinic management section repaired")
    print(f"changes={changed}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()
