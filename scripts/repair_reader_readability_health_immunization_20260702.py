# -*- coding: utf-8 -*-
"""Source-correct the immunization section in volume 55."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_health_immunization_20260702.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_health_immunization_20260702.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260702_第五十五卷计划免疫OCR修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SOURCE_NOTE = (
    "workbench/body_chapters/连云港市志_全书_正文汇总.md:100578-100606; "
    "workbench/body_chapters/第五十二卷至第六十卷及附录（下part02）.md:7278-7306; "
    "workbench/ocr/paddle_ocr/下/part02/page_0181.txt; "
    "workbench/ocr/paddle_ocr/下/part02/page_0182.txt"
)
SCOPE_START = '<h4 id="第五十五卷-第二章常见病防治-第四节计划免疫">第四节计划免疫</h4>'
SCOPE_END = '<h3 id="第五十五卷-第三章医疗">第三章医疗</h3>'

REPLACEMENTS: list[tuple[str, str, str]] = [
    ("冷藏库缺字", "建10平方米冷藏库座", "建10平方米冷藏库一座"),
    ("编码引号", '编码"07”', "编码“07”"),
    ("第一个计划免疫宣传日", "规定的第个计划免疫宣传日", "规定的第一个计划免疫宣传日"),
    ("第一个85%目标", "达到第个85%目标", "达到第一个85%目标"),
]

RESIDUALS = ["冷藏库座", '编码"07”', "第个计划免疫宣传日", "第个85%目标"]


def patch_segment(segment: str) -> tuple[str, int, dict[str, int]]:
    changed = 0
    counts: dict[str, int] = {}
    for label, needle, replacement in REPLACEMENTS:
        count = segment.count(needle)
        if count:
            segment = segment.replace(needle, replacement)
            counts[label] = count
            changed += count

    remaining = [marker for marker in RESIDUALS if marker in segment]
    if remaining:
        raise RuntimeError(f"immunization OCR residue remains: {remaining}")
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
        "scope": "第五十五卷卫生 / 第二章常见病防治 / 第四节计划免疫",
        "source": SOURCE_NOTE,
        "reader_path": str(HTML),
        "changes_this_run": changed,
        "counts": counts,
        "principle": "依据 PaddleOCR 页级文本，仅修复第四节计划免疫中可证的缺字和标点；未处理第三章医疗。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    md = f"""# 第五十五卷计划免疫 OCR 修复

- 时间：{now}
- 范围：`第五十五卷卫生 / 第二章常见病防治 / 第四节计划免疫`
- 源文依据：`{SOURCE_NOTE}`

## 修复动作

- 依据 PaddleOCR `page_0181.txt`，修复 `建10平方米冷藏库座` 为 `建10平方米冷藏库一座`。
- 依据 PaddleOCR `page_0182.txt`，修复 `第个计划免疫宣传日` 为 `第一个计划免疫宣传日`。
- 依据 PaddleOCR `page_0182.txt`，修复 `第个85%目标` 为 `第一个85%目标`。
- 同步修复 `编码\"07”` 的中西引号错配为 `编码“07”`。
- 本次复跑新增替换：{changed} 处。
- 本轮未处理第三章 `医疗`。

## 核对说明

- PaddleOCR `page_0181.txt` 跨页进入第四节，确认 `冷藏库一座`。
- PaddleOCR `page_0182.txt` 确认 `第一个计划免疫宣传日` 与 `第一个85%目标`。
"""
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")


def update_memory(changed: int) -> None:
    marker = "## 2026-07-02 第五十五卷计划免疫OCR修复"
    memory = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker in memory:
        return
    entry = f"""
{marker}

- 对第五十五卷卫生第二章第四节 `计划免疫` 进行回源修复。
- 源文依据：`{SOURCE_NOTE}`；确认 `冷藏库一座`、`第一个计划免疫宣传日`、`第一个85%目标` 等字词。
- 阅读版修复 4 处可证 OCR/标点问题；第三章 `医疗` 未在本脚本中处理。
- 报告：`output/reports/reader_readability_health_immunization_20260702.md`。
"""
    MEMORY.write_text(memory.rstrip() + "\n\n" + entry.lstrip(), encoding="utf-8")


def main() -> None:
    changed, counts = patch_reader()
    write_reports(changed, counts)
    update_memory(changed)
    print("immunization section repaired")
    print(f"changes={changed}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()
