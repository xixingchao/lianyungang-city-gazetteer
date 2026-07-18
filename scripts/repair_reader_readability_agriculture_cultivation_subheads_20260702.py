# -*- coding: utf-8 -*-
"""Split flattened crop-cultivation subheadings in volume 9 reader text."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_agriculture_cultivation_subheads_20260702.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_agriculture_cultivation_subheads_20260702.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260702_第九卷作物栽培小标题粘连修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SOURCE_NOTE = "workbench/body_chapters/paddle_上/第四卷至第十卷（part02）.md:13881-14068"
SCOPE_START = '<h3 id="第九卷-第四章作物栽培">第四章作物栽培</h3>'
SCOPE_END = '<h3 id="第九卷-第五章土壤改良与肥料施用">第五章土壤改良与肥料施用</h3>'

# The body_start values are the first source text immediately after headings
# that are independent lines in the PaddleOCR chapter text.
HEADINGS: list[tuple[str, str]] = [
    ("一、种植规模", "民国时期"),
    ("二、栽培技术", "育秧"),
    ("一、种植规模", "境内是"),
    ("二、栽培技术", "少（免）耕"),
    ("三、田间管理", "20世纪70年代"),
    ("一、种植规模", "1949年"),
    ("二、栽培管理", "20世纪70年代"),
    ("一、种植规模", "民国19年"),
    ("二、栽培管理", "20世纪50年代"),
    ("一、种植规模", "民国初"),
    ("二、栽培技术", "20世纪60年代"),
    ("二、栽培技术", "20世纪50年代"),
]


def split_headings_in_scope(text: str) -> tuple[str, int, dict[str, int]]:
    start = text.index(SCOPE_START)
    end = text.index(SCOPE_END, start)
    segment = text[start:end]
    changed = 0
    split_counts: dict[str, int] = {}

    for heading, body_start in HEADINGS:
        needle = f"<p>{heading}{body_start}"
        replacement = f"<p><strong>{heading}</strong></p>\n<p>{body_start}"
        count = segment.count(needle)
        if count:
            segment = segment.replace(needle, replacement)
            split_counts[f"{heading}{body_start}"] = count
            changed += count

    remaining = [
        f"{heading}{body_start}"
        for heading, body_start in HEADINGS
        if f"<p>{heading}{body_start}" in segment
    ]
    if remaining:
        raise RuntimeError(f"crop cultivation heading residue remains: {remaining}")

    return text[:start] + segment + text[end:], changed, split_counts


def patch_reader() -> tuple[int, dict[str, int]]:
    text = HTML.read_text(encoding="utf-8")
    new_text, changed, split_counts = split_headings_in_scope(text)
    HTML.write_text(new_text, encoding="utf-8")
    return changed, split_counts


def write_reports(changed: int, split_counts: dict[str, int]) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    expected_boundaries = 13
    payload = {
        "time": now,
        "scope": "第九卷农林业 / 第四章作物栽培 / 第一节水稻栽培至第六节棉花栽培",
        "source": SOURCE_NOTE,
        "reader_path": str(HTML),
        "headings_split_this_run": changed,
        "headings_in_scope": expected_boundaries,
        "split_counts": split_counts,
        "principle": "依据 PaddleOCR 正文汇总中的独立标题行，仅拆分阅读版标题粘连，不改写正文内容和数值。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    md = f"""# 第九卷作物栽培小标题粘连修复

- 时间：{now}
- 范围：`第九卷农林业 / 第四章作物栽培 / 第一节水稻栽培至第六节棉花栽培`
- 源文依据：`{SOURCE_NOTE}`

## 修复动作

- 将阅读版中 `一、种植规模民国时期...`、`二、栽培技术育秧...` 等小标题粘连拆为独立标题段。
- 覆盖水稻、三麦、玉米、大豆、花生、棉花 6 节，共 {expected_boundaries} 处源文独立小标题边界。
- 本次复跑新增拆分：{changed} 处。
- 仅调整段落结构，不改写正文文字、统计数值或行内技术小题。

## 核对说明

- `workbench/body_chapters/paddle_上/第四卷至第十卷（part02）.md` 中 13881-14068 行显示这些标题为独立行。
- `育秧 1956年以前`、`水浆管理20世纪...`、`少（免）耕配套技术20世纪...` 等仍按源文保留为正文行内小题。
"""
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")


def update_memory(changed: int) -> None:
    marker = "## 2026-07-02 第九卷作物栽培小标题粘连修复"
    memory = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker in memory:
        return
    entry = f"""
{marker}

- 对正文可读性审计命中的第九卷农林业第四章作物栽培小标题压平进行修复。
- 源文依据：`{SOURCE_NOTE}`，确认水稻、三麦、玉米、大豆、花生、棉花 6 节中 `一、种植规模`、`二、栽培技术/管理`、`三、田间管理` 等为独立标题行。
- 阅读版仅拆分标题边界，不重录正文文字和数值；本轮拆分 {changed} 处，范围覆盖 13 处标题粘连。
- 报告：`output/reports/reader_readability_agriculture_cultivation_subheads_20260702.md`。
"""
    MEMORY.write_text(memory.rstrip() + "\n\n" + entry.lstrip(), encoding="utf-8")


def main() -> None:
    changed, split_counts = patch_reader()
    write_reports(changed, split_counts)
    update_memory(changed)
    print("agriculture cultivation subheadings repaired")
    print(f"headings_split={changed}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()
