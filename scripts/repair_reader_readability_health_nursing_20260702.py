# -*- coding: utf-8 -*-
"""Source-correct obvious OCR errors in the nursing section."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_health_nursing_20260702.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_health_nursing_20260702.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260702_第五十五卷护理OCR修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SOURCE_NOTE = (
    "workbench/body_chapters/连云港市志_全书_正文汇总.md:100934-100962; "
    "workbench/body_chapters/第五十二卷至第六十卷及附录（下part02）.md:7638-7662; "
    "workbench/ocr/paddle_ocr/下/part02/page_0191.txt"
)
SCOPE_START = '<h4 id="第五十五卷-第三章医疗-第四节护理">第四节护理</h4>'
SCOPE_END = '<h3 id="第五十五卷-第四章医政 药政">第四章医政 药政</h3>'

REPLACEMENTS: list[tuple[str, str, str]] = [
    ("护士长字形", "护土长", "护士长"),
]

RESIDUALS = ["护土长"]
EXPECTED_TEXT = "护士长"
DEFERRED_UNCERTAIN = ["交换班", "堂对"]


def patch_segment(segment: str) -> tuple[str, int, dict[str, int]]:
    changed = 0
    counts: dict[str, int] = {}
    for label, needle, replacement in REPLACEMENTS:
        count = segment.count(needle)
        if count:
            segment = segment.replace(needle, replacement)
            counts[label] = count
            changed += count

    if EXPECTED_TEXT not in segment:
        raise RuntimeError("nursing expected correction missing: 护士长")
    remaining = [marker for marker in RESIDUALS if marker in segment]
    if remaining:
        raise RuntimeError(f"nursing OCR residue remains: {remaining}")
    return segment, changed, counts


def patch_reader() -> tuple[int, dict[str, int]]:
    text = HTML.read_text(encoding="utf-8")
    start = text.index(SCOPE_START)
    end = text.index(SCOPE_END, start)
    segment = text[start:end]
    new_segment, changed, counts = patch_segment(segment)
    if new_segment != segment:
        HTML.write_text(text[:start] + new_segment + text[end:], encoding="utf-8")
    return changed, counts


def write_reports(changed: int, counts: dict[str, int]) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "第五十五卷卫生 / 第三章医疗 / 第四节护理",
        "source": SOURCE_NOTE,
        "reader_path": str(HTML),
        "changes_this_run": changed,
        "counts": counts,
        "deferred_uncertain_ocr": DEFERRED_UNCERTAIN,
        "principle": "依据 PaddleOCR 页级文本仅修复护理节内可证 OCR 字形错误；证据不足的疑似词暂缓。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    md = f"""# 第五十五卷护理 OCR 修复

- 时间：{now}
- 范围：`第五十五卷卫生 / 第三章医疗 / 第四节护理`
- 源文依据：`{SOURCE_NOTE}`

## 修复动作

- 依据 PaddleOCR `page_0191.txt`，将护理节内 3 处 `护土长` 修为 `护士长`。
- 本次复跑新增替换：{changed} 处。
- 暂缓未改：`交换班`、`堂对`，原因是当前 OCR 文本未给出足够可靠的替代正形。
- 本轮未处理 `第四章医政 药政`。

## 核对说明

- PaddleOCR `page_0191.txt` 明确给出 `护士长`，覆盖民国9年、1960年、1964年三处。
"""
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")


def update_memory(changed: int) -> None:
    marker = "## 2026-07-02 第五十五卷护理OCR修复"
    memory = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker in memory:
        return
    entry = f"""
{marker}

- 对第五十五卷卫生第三章第四节 `护理` 进行回源修复。
- 源文依据：`{SOURCE_NOTE}`；修复护理节内 3 处 `护土长` 为 `护士长`。
- 本轮新增替换 {changed} 处；`交换班`、`堂对` 因当前 OCR 未给出可靠正形暂缓。
- 报告：`output/reports/reader_readability_health_nursing_20260702.md`。
"""
    MEMORY.write_text(memory.rstrip() + "\n\n" + entry.lstrip(), encoding="utf-8")


def main() -> None:
    changed, counts = patch_reader()
    write_reports(changed, counts)
    update_memory(changed)
    print("nursing section repaired")
    print(f"changes={changed}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()
