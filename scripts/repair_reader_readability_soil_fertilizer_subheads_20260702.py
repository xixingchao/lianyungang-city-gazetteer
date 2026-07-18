# -*- coding: utf-8 -*-
"""Split flattened soil-improvement and fertilizer subheadings in volume 9."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_soil_fertilizer_subheads_20260702.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_soil_fertilizer_subheads_20260702.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260702_第九卷土壤肥料小标题粘连修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SOURCE_NOTE = "workbench/body_chapters/paddle_上/第四卷至第十卷（part02）.md:14483-14562"
SCOPE_START = '<h3 id="第九卷-第五章土壤改良与肥料施用">第五章土壤改良与肥料施用</h3>'
SCOPE_END = '<h3 id="第九卷-第六章植物保护">第六章植物保护</h3>'

HEADINGS: list[tuple[str, str]] = [
    ("一、盐土改良", "境内盐土"),
    ("二、砂礓黑土改良", "境内砂礓黑土"),
    ("三、白浆土改良", "境内白浆土"),
    ("一、有机肥料施用", "建国前及50年代"),
    ("二、化学肥料施用", "1956年"),
    ("三、施肥技术", "水稻施肥技术"),
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
        raise RuntimeError(f"soil/fertilizer heading residue remains: {remaining}")

    return text[:start] + segment + text[end:], changed, split_counts


def patch_reader() -> tuple[int, dict[str, int]]:
    text = HTML.read_text(encoding="utf-8")
    new_text, changed, split_counts = split_headings_in_scope(text)
    HTML.write_text(new_text, encoding="utf-8")
    return changed, split_counts


def write_reports(changed: int, split_counts: dict[str, int]) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    total = len(HEADINGS)
    payload = {
        "time": now,
        "scope": "第九卷农林业 / 第五章土壤改良与肥料施用",
        "source": SOURCE_NOTE,
        "reader_path": str(HTML),
        "headings_split_this_run": changed,
        "headings_in_scope": total,
        "split_counts": split_counts,
        "principle": "依据 PaddleOCR 正文汇总中的独立标题行，仅拆分阅读版标题粘连，不改写正文内容和数值。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    md = f"""# 第九卷土壤肥料小标题粘连修复

- 时间：{now}
- 范围：`第九卷农林业 / 第五章土壤改良与肥料施用`
- 源文依据：`{SOURCE_NOTE}`

## 修复动作

- 拆分 `一、盐土改良境内盐土...`、`二、砂礓黑土改良境内砂礓黑土...`、`三、白浆土改良境内白浆土...`。
- 拆分 `一、有机肥料施用建国前...`、`二、化学肥料施用1956年...`、`三、施肥技术水稻施肥技术...`。
- 本脚本覆盖标题边界：{total} 处；本次复跑新增拆分：{changed} 处。
- 仅调整段落结构，不改写正文文字、统计数值或行内技术小题。

## 核对说明

- 源文中 14483-14562 行显示上述 6 个标题为独立行。
- `水稻施肥技术20世纪...`、`三麦施肥技术20世纪...` 为源文正文行内小题，本轮保留行内形式。
"""
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")


def update_memory(changed: int) -> None:
    marker = "## 2026-07-02 第九卷土壤肥料小标题粘连修复"
    memory = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker in memory:
        return
    total = len(HEADINGS)
    entry = f"""
{marker}

- 对第九卷农林业第五章土壤改良与肥料施用的小标题压平进行修复。
- 源文依据：`{SOURCE_NOTE}`，确认土壤改良 3 个小题和肥料施用 3 个小题为独立标题行。
- 阅读版仅拆分标题边界，不重录正文文字和数值；本轮拆分 {changed} 处，范围覆盖 {total} 处标题粘连。
- 报告：`output/reports/reader_readability_soil_fertilizer_subheads_20260702.md`。
"""
    MEMORY.write_text(memory.rstrip() + "\n\n" + entry.lstrip(), encoding="utf-8")


def main() -> None:
    changed, split_counts = patch_reader()
    write_reports(changed, split_counts)
    update_memory(changed)
    print("soil and fertilizer subheadings repaired")
    print(f"headings_split={changed}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()
