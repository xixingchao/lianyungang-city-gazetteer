# -*- coding: utf-8 -*-
"""Split selected flattened tax subheadings in volume 39."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_tax_subheads_20260702.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_tax_subheads_20260702.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260702_第三十九卷税务小标题粘连修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SOURCE_NOTE = "workbench/body_chapters/连云港市志_全书_正文汇总.md:80173-80220,80597-80674"

SCOPES: list[tuple[str, str, list[tuple[str, str]]]] = [
    (
        '<h4 id="第三十九卷-第二章税种税率-第二节工商各税">第二节工商各税</h4>',
        '<h4 id="第三十九卷-第二章税种税率-第三节盐税">第三节盐税</h4>',
        [
            ("二十六、建筑税", "1983年10月起"),
            ("二十七、奖金税", "1985年"),
            ("二十八、城市维护建设税", "1988年起"),
        ],
    ),
    (
        '<h4 id="第三十九卷-第三章稽征管理-第二节减税免税">第二节减税免税</h4>',
        '<h4 id="第三十九卷-第三章稽征管理-第三节税务稽查">第三节税务稽查</h4>',
        [
            ("一、工商税减免", "建国初"),
            ("二、盐税减免", "建国后"),
            ("三、农业税减免", "古时海州"),
        ],
    ),
]


def split_headings_in_scope(segment: str, headings: list[tuple[str, str]]) -> tuple[str, int, dict[str, int]]:
    changed = 0
    split_counts: dict[str, int] = {}
    for heading, body_start in headings:
        needle = f"<p>{heading}{body_start}"
        replacement = f"<p><strong>{heading}</strong></p>\n<p>{body_start}"
        count = segment.count(needle)
        if count:
            segment = segment.replace(needle, replacement)
            split_counts[f"{heading}{body_start}"] = count
            changed += count

    remaining = [
        f"{heading}{body_start}"
        for heading, body_start in headings
        if f"<p>{heading}{body_start}" in segment
    ]
    if remaining:
        raise RuntimeError(f"tax heading residue remains: {remaining}")
    return segment, changed, split_counts


def patch_reader() -> tuple[int, dict[str, int]]:
    text = HTML.read_text(encoding="utf-8")
    offset = 0
    total_changed = 0
    all_counts: dict[str, int] = {}

    for scope_start, scope_end, headings in SCOPES:
        start = text.index(scope_start, offset)
        end = text.index(scope_end, start)
        segment = text[start:end]
        new_segment, changed, split_counts = split_headings_in_scope(segment, headings)
        text = text[:start] + new_segment + text[end:]
        offset = start + len(new_segment)
        total_changed += changed
        all_counts.update(split_counts)

    HTML.write_text(text, encoding="utf-8")
    return total_changed, all_counts


def write_reports(changed: int, split_counts: dict[str, int]) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    total = sum(len(scope[2]) for scope in SCOPES)
    payload = {
        "time": now,
        "scope": "第三十九卷税务 / 第二章税种税率末段、第三章稽征管理第二节减税免税",
        "source": SOURCE_NOTE,
        "reader_path": str(HTML),
        "headings_split_this_run": changed,
        "headings_in_scope": total,
        "split_counts": split_counts,
        "principle": "依据正文汇总中的独立标题行，仅拆分阅读版标题粘连，不改写正文内容和数值。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    md = f"""# 第三十九卷税务小标题粘连修复

- 时间：{now}
- 范围：`第三十九卷税务 / 第二章税种税率末段、第三章稽征管理第二节减税免税`
- 源文依据：`{SOURCE_NOTE}`

## 修复动作

- 拆分第二章第二节工商各税末尾 3 个税种小题：`二十六、建筑税`、`二十七、奖金税`、`二十八、城市维护建设税`。
- 拆分第三章第二节减税免税 3 个小题：`一、工商税减免`、`二、盐税减免`、`三、农业税减免`。
- 本脚本覆盖标题边界：{total} 处；本次复跑新增拆分：{changed} 处。
- 仅调整段落结构，不改写正文文字、统计数值或税制内容。

## 核对说明

- 源文中 80173-80220、80597-80674 行显示上述 6 个小题为独立行。
- 本轮不处理第一节征收管理内 `盐税征收管理`、`农业税征收管理` 等行内条目，避免扩大改动范围。
"""
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")


def update_memory(changed: int) -> None:
    marker = "## 2026-07-02 第三十九卷税务小标题粘连修复"
    memory = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker in memory:
        return
    total = sum(len(scope[2]) for scope in SCOPES)
    entry = f"""
{marker}

- 对第三十九卷税务中两处边界清楚的小标题压平进行修复。
- 源文依据：`{SOURCE_NOTE}`，确认第二章工商各税末尾 3 个税种小题和第三章减税免税 3 个小题为独立标题行。
- 阅读版仅拆分标题边界，不重录正文文字和数值；本轮拆分 {changed} 处，范围覆盖 {total} 处标题粘连。
- 征收管理节中 `盐税征收管理`、`农业税征收管理` 等行内条目未改，留待后续按源文单独核对。
- 报告：`output/reports/reader_readability_tax_subheads_20260702.md`。
"""
    MEMORY.write_text(memory.rstrip() + "\n\n" + entry.lstrip(), encoding="utf-8")


def main() -> None:
    changed, split_counts = patch_reader()
    write_reports(changed, split_counts)
    update_memory(changed)
    print("tax subheadings repaired")
    print(f"headings_split={changed}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()
