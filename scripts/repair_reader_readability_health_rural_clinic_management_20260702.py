# -*- coding: utf-8 -*-
"""Split and source-correct township health center management."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_health_rural_clinic_management_20260702.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_health_rural_clinic_management_20260702.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260702_第五十五卷乡镇卫生院管理标题与OCR修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SOURCE_NOTE = (
    "workbench/body_chapters/连云港市志_全书_正文汇总.md:100988-101027; "
    "workbench/body_chapters/第五十二卷至第六十卷及附录（下part02）.md:7686-7724; "
    "workbench/ocr/paddle_ocr/下/part02/page_0192.txt; "
    "workbench/ocr/paddle_ocr/下/part02/page_0193.txt"
)
SCOPE_START = '<h4 id="第五十五卷-第四章医政 药政-第二节农村医疗管理">第二节农村医疗管理</h4>'
SCOPE_END_OPTIONS = ('<p>二、村卫生室管理', '<p><strong>二、村卫生室管理</strong></p>')

REPLACEMENTS: list[tuple[str, str, str]] = [
    (
        "一、乡镇卫生院管理标题",
        "<p>一、乡镇卫生院管理市内乡镇卫生院是人民公社卫生院形成的。",
        "<p><strong>一、乡镇卫生院管理</strong></p>\n<p>市内乡镇卫生院是人民公社卫生院形成的。",
    ),
    ("乡镇名字形", "朝阳、新项、中云", "朝阳、新坝、中云"),
    ("统一管理缺字", "逐步实行统管理、独立核算", "逐步实行统一管理、独立核算"),
    (
        "1983年改革试点缺文",
        "1983试点，公社卫生院更名为乡（镇）卫生院。",
        "1983年，开始进行卫生院内部管理体制改革，在部分卫生院中进行浮动工资制和单科室承包制试点，公社卫生院更名为乡（镇）卫生院。",
    ),
    ("一批字形", "一一批懂业务、会管理", "一批懂业务、会管理"),
]

EXPECTED_TEXT = [
    "<p><strong>一、乡镇卫生院管理</strong></p>",
    "朝阳、新坝、中云",
    "逐步实行统一管理、独立核算",
    "1983年，开始进行卫生院内部管理体制改革，在部分卫生院中进行浮动工资制和单科室承包制试点",
    "一批懂业务、会管理",
]
RESIDUALS = [
    "一、乡镇卫生院管理市内乡镇卫生院",
    "朝阳、新项、中云",
    "逐步实行统管理",
    "1983试点",
    "一一批懂业务、会管理",
]


def find_scope(text: str) -> tuple[int, int]:
    start = text.index(SCOPE_START)
    ends = [text.find(marker, start) for marker in SCOPE_END_OPTIONS]
    valid_ends = [end for end in ends if end != -1]
    if not valid_ends:
        raise RuntimeError("rural clinic management scope end not found")
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
        raise RuntimeError(f"rural clinic management expected corrections missing: {missing}")
    remaining = [marker for marker in RESIDUALS if marker in segment]
    if remaining:
        raise RuntimeError(f"rural clinic management OCR residue remains: {remaining}")
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
        "scope": "第五十五卷卫生 / 第四章医政 药政 / 第二节农村医疗管理 / 一、乡镇卫生院管理",
        "source": SOURCE_NOTE,
        "reader_path": str(HTML),
        "changes_this_run": changed,
        "counts": counts,
        "principle": "依据 PaddleOCR 页级文本拆分小节标题，并修复乡镇卫生院管理小节内可证 OCR 错字和漏文；未处理二、村卫生室管理。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    md = f"""# 第五十五卷乡镇卫生院管理标题与 OCR 修复

- 时间：{now}
- 范围：`第五十五卷卫生 / 第四章医政 药政 / 第二节农村医疗管理 / 一、乡镇卫生院管理`
- 源文依据：`{SOURCE_NOTE}`

## 修复动作

- 拆分 `一、乡镇卫生院管理` 小节标题。
- 依据 PaddleOCR `page_0192.txt` 修复 `朝阳、新坝、中云`、`统一管理`，并补回 1983 年卫生院内部管理体制改革试点完整表述。
- 依据 PaddleOCR `page_0192.txt` 至 `page_0193.txt` 修复 `一批懂业务、会管理`。
- 本次复跑新增替换：{changed} 处。
- 本轮未处理 `二、村卫生室管理`。

## 核对说明

- PaddleOCR `page_0192.txt` 确认 `第二节农村医疗管理`、`一、乡镇卫生院管理` 起点及 1983 年改革试点缺文。
- PaddleOCR `page_0193.txt` 确认本小节尾句与 `二、村卫生室管理` 边界。
"""
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")


def update_memory(changed: int) -> None:
    marker = "## 2026-07-02 第五十五卷乡镇卫生院管理标题与OCR修复"
    memory = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker in memory:
        return
    entry = f"""
{marker}

- 对第五十五卷卫生第四章第二节 `农村医疗管理` 的 `一、乡镇卫生院管理` 进行回源修复。
- 源文依据：`{SOURCE_NOTE}`；拆分小节标题，修复 `朝阳、新坝、中云`、`统一管理`、1983 年卫生院内部管理体制改革试点漏文、`一批懂业务、会管理` 等页级 OCR 可证问题。
- 本轮新增替换 {changed} 处；`二、村卫生室管理` 未在本脚本中处理。
- 报告：`output/reports/reader_readability_health_rural_clinic_management_20260702.md`。
"""
    MEMORY.write_text(memory.rstrip() + "\n\n" + entry.lstrip(), encoding="utf-8")


def main() -> None:
    changed, counts = patch_reader()
    write_reports(changed, counts)
    update_memory(changed)
    print("rural clinic management section repaired")
    print(f"changes={changed}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()
