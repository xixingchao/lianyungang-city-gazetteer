# -*- coding: utf-8 -*-
"""Split flattened collection-management subheadings in volume 39."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_tax_collection_management_subheads_20260702.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_tax_collection_management_subheads_20260702.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260702_第三十九卷征收管理标题粘连修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SOURCE_NOTE = (
    "workbench/body_chapters/连云港市志_全书_正文汇总.md:80288-80594; "
    "workbench/ocr/paddle_ocr/中/part02/page_0328.txt; "
    "workbench/ocr/paddle_ocr/中/part02/page_0329.txt; "
    "workbench/ocr/paddle_ocr/中/part02/page_0330.txt; "
    "workbench/ocr/paddle_ocr/中/part02/page_0331.txt; "
    "workbench/ocr/paddle_ocr/中/part02/page_0332.txt; "
    "workbench/ocr/paddle_ocr/中/part02/page_0335.txt; "
    "workbench/ocr/paddle_ocr/中/part02/page_0336.txt"
)
SCOPE_START = '<h4 id="第三十九卷-第三章稽征管理-第一节征收管理">第一节征收管理</h4>'
SCOPE_END = '<h4 id="第三十九卷-第三章稽征管理-第二节减税免税">第二节减税免税</h4>'

REPLACEMENTS: list[tuple[str, str, str, int]] = [
    (
        "一、明清时期 / 丁银征收管理",
        "<p>一、明清时期丁银征收管理明时丁银为均，",
        "<p><strong>一、明清时期</strong></p>\n<p><strong>丁银征收管理</strong></p>\n<p>明时丁银为均，",
        2,
    ),
    (
        "田赋征收管理（明清）",
        "<p>田赋征收管理明时田赋称田粮，",
        "<p><strong>田赋征收管理</strong></p>\n<p>明时田赋称田粮，",
        1,
    ),
    (
        "盐课征收管理",
        "<p>盐课征收管理明时海州境内四个盐场",
        "<p><strong>盐课征收管理</strong></p>\n<p>明时海州境内四个盐场",
        1,
    ),
    (
        "二、民国时期 / 田赋征收管理",
        "<p>二、民国时期田赋征收管理民国时期田赋每年皆有征收定额，",
        "<p><strong>二、民国时期</strong></p>\n<p><strong>田赋征收管理</strong></p>\n<p>民国时期田赋每年皆有征收定额，",
        2,
    ),
    (
        "公粮征收管理",
        "<p>公粮征收管理抗战期间，",
        "<p><strong>公粮征收管理</strong></p>\n<p>抗战期间，",
        1,
    ),
    (
        "盐税征收管理（民国）",
        "<p>盐税征收管理民国初盐税税率紊乱，",
        "<p><strong>盐税征收管理</strong></p>\n<p>民国初盐税税率紊乱，",
        1,
    ),
    (
        "工商税捐征收管理",
        "<p>工商税捐征收管理民国初，",
        "<p><strong>工商税捐征收管理</strong></p>\n<p>民国初，",
        1,
    ),
    (
        "三、建国后 / 工商税收征收管理",
        "<p>三、建国后工商税收征收管理1950年，",
        "<p><strong>三、建国后</strong></p>\n<p><strong>工商税收征收管理</strong></p>\n<p>1950年，",
        2,
    ),
    (
        "盐税征收管理（建国后）",
        "<p>盐税征收管理1950年全国统盐政，",
        "<p><strong>盐税征收管理</strong></p>\n<p>1950年全国统盐政，",
        1,
    ),
    (
        "农业税征收管理",
        "<p>农业税征收管理建国后，",
        "<p><strong>农业税征收管理</strong></p>\n<p>建国后，",
        1,
    ),
]

RESIDUALS = [needle.removeprefix("<p>") for _, needle, _, _ in REPLACEMENTS]


def split_headings(segment: str) -> tuple[str, int, int, dict[str, int]]:
    changed = 0
    headings_exposed = 0
    counts: dict[str, int] = {}
    for label, needle, replacement, exposed in REPLACEMENTS:
        count = segment.count(needle)
        if count:
            segment = segment.replace(needle, replacement)
            counts[label] = count
            changed += count
            headings_exposed += count * exposed

    remaining = [marker for marker in RESIDUALS if marker in segment]
    if remaining:
        raise RuntimeError(f"collection-management heading residue remains: {remaining}")
    return segment, changed, headings_exposed, counts


def patch_reader() -> tuple[int, int, dict[str, int]]:
    text = HTML.read_text(encoding="utf-8")
    start = text.index(SCOPE_START)
    end = text.index(SCOPE_END, start)
    segment = text[start:end]
    new_segment, changed, headings_exposed, counts = split_headings(segment)
    if new_segment != segment:
        text = text[:start] + new_segment + text[end:]
        HTML.write_text(text, encoding="utf-8")
    return changed, headings_exposed, counts


def write_reports(changed: int, headings_exposed: int, counts: dict[str, int]) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "第三十九卷税务 / 第三章稽征管理 / 第一节征收管理",
        "source": SOURCE_NOTE,
        "reader_path": str(HTML),
        "paragraph_boundaries_split_this_run": changed,
        "headings_exposed_this_run": headings_exposed,
        "target_paragraph_boundaries": len(REPLACEMENTS),
        "target_headings": sum(item[3] for item in REPLACEMENTS),
        "counts": counts,
        "principle": "依据正文汇总和 PaddleOCR 页级文本中的独立标题行，仅拆分标题边界，不改写征收管理正文和数值。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    md = f"""# 第三十九卷征收管理标题粘连修复

- 时间：{now}
- 范围：`第三十九卷税务 / 第三章稽征管理 / 第一节征收管理`
- 源文依据：`{SOURCE_NOTE}`

## 修复动作

- 拆分 `一、明清时期`、`二、民国时期`、`三、建国后` 3 个时期标题。
- 拆分 `丁银征收管理`、`田赋征收管理`、`盐课征收管理`、`公粮征收管理`、`盐税征收管理`、`工商税捐征收管理`、`工商税收征收管理`、`农业税征收管理` 等分项标题。
- 本轮覆盖 {len(REPLACEMENTS)} 处标题正文粘连，可显露 {sum(item[3] for item in REPLACEMENTS)} 个独立标题；本次复跑新增拆分：{changed} 处，新增显露标题：{headings_exposed} 个。
- 本轮只处理标题边界，不补改正文内 OCR 错字、不调整税收数值。

## 核对说明

- 正文汇总 80288-80594 行显示 `第一节征收管理` 下有 `一、明清时期`、`二、民国时期`、`三、建国后` 三个层级标题。
- PaddleOCR `page_0328` 至 `page_0336` 确认 `丁银征收管理`、`田赋征收管理`、`盐课征收管理`、`公粮征收管理`、`盐税征收管理`、`工商税捐征收管理`、`工商税收征收管理`、`农业税征收管理` 均为独立分项起点。
- 读者版原来将这些标题压成 `一、明清时期丁银征收管理...`、`二、民国时期田赋征收管理...`、`三、建国后工商税收征收管理...` 等连续正文，本轮已按源文层级拆开。
"""
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")


def update_memory(changed: int, headings_exposed: int) -> None:
    marker = "## 2026-07-02 第三十九卷征收管理标题粘连修复"
    memory = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker in memory:
        return
    entry = f"""
{marker}

- 对第三十九卷税务第三章第一节 `征收管理` 的标题压平问题进行修复。
- 源文依据：`{SOURCE_NOTE}`，确认明清、民国、建国后三个时期标题及征收管理分项为独立标题起点。
- 阅读版仅拆分标题边界，不改写征收管理正文和数值；本轮拆分 {changed} 处，显露 {headings_exposed} 个标题。
- 报告：`output/reports/reader_readability_tax_collection_management_subheads_20260702.md`。
"""
    MEMORY.write_text(memory.rstrip() + "\n\n" + entry.lstrip(), encoding="utf-8")


def main() -> None:
    changed, headings_exposed, counts = patch_reader()
    write_reports(changed, headings_exposed, counts)
    update_memory(changed, headings_exposed)
    print("collection-management subheadings repaired")
    print(f"paragraph_boundaries_split={changed}")
    print(f"headings_exposed={headings_exposed}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()
