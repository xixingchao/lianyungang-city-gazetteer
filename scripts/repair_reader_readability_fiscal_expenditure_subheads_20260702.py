# -*- coding: utf-8 -*-
"""Split flattened fiscal-expenditure subheadings in volume 38."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_fiscal_expenditure_subheads_20260702.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_fiscal_expenditure_subheads_20260702.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260702_第三十八卷财政支出小标题粘连修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SOURCE_NOTE = "workbench/body_chapters/连云港市志_全书_正文汇总.md:78804-78974"
SCOPE_START = '<h3 id="第三十八卷-第三章财政支出">第三章财政支出</h3>'
SCOPE_END = '<h3 id="第三十八卷-第四章财政管理">第四章财政管理</h3>'

HEADINGS: list[tuple[str, str]] = [
    ("一、基本建设支出", "1952年"),
    ("二、企业挖潜改造资金", "1976年"),
    ("三、科技三项费用支出", "1963年"),
    ("四、流动资金支出", "1951年"),
    ("五、工交商事业费和简易建筑费支出", "1952~1980年"),
    ("六、农林水利事业费和支援农业支出", "1982年前"),
    ("一、价格补贴支出", "1985年前"),
    ("二、专项支出", "1985年开始"),
]

DUPLICATE_CHAPTER_PREFIX = ("<p>财政支出财政支出，", "<p>财政支出，")


def split_headings_in_scope(text: str) -> tuple[str, int, int, dict[str, int]]:
    start = text.index(SCOPE_START)
    end = text.index(SCOPE_END, start)
    segment = text[start:end]
    changed = 0
    duplicate_fixed = 0
    split_counts: dict[str, int] = {}

    old_prefix, new_prefix = DUPLICATE_CHAPTER_PREFIX
    duplicate_fixed = segment.count(old_prefix)
    if duplicate_fixed:
        segment = segment.replace(old_prefix, new_prefix)

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
        raise RuntimeError(f"fiscal expenditure heading residue remains: {remaining}")

    if old_prefix in segment:
        raise RuntimeError("duplicate fiscal chapter prefix remains")

    return text[:start] + segment + text[end:], changed, duplicate_fixed, split_counts


def patch_reader() -> tuple[int, int, dict[str, int]]:
    text = HTML.read_text(encoding="utf-8")
    new_text, changed, duplicate_fixed, split_counts = split_headings_in_scope(text)
    HTML.write_text(new_text, encoding="utf-8")
    return changed, duplicate_fixed, split_counts


def write_reports(changed: int, duplicate_fixed: int, split_counts: dict[str, int]) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    total = len(HEADINGS)
    payload = {
        "time": now,
        "scope": "第三十八卷财政 / 第三章财政支出",
        "source": SOURCE_NOTE,
        "reader_path": str(HTML),
        "headings_split_this_run": changed,
        "headings_in_scope": total,
        "duplicate_chapter_prefix_fixed_this_run": duplicate_fixed,
        "split_counts": split_counts,
        "principle": "依据正文汇总中的独立标题行，仅拆分阅读版标题粘连和章题重复，不改写正文内容和数值。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    md = f"""# 第三十八卷财政支出小标题粘连修复

- 时间：{now}
- 范围：`第三十八卷财政 / 第三章财政支出`
- 源文依据：`{SOURCE_NOTE}`

## 修复动作

- 拆分第一节经济建设支出下 6 个小题：`一、基本建设支出` 至 `六、农林水利事业费和支援农业支出`。
- 拆分第六节其它支出下 2 个小题：`一、价格补贴支出`、`二、专项支出`。
- 修正同章开头 `财政支出财政支出，古称...` 的章题重复粘连。
- 本脚本覆盖标题边界：{total} 处；本次复跑新增拆分：{changed} 处；本次复跑新增章题重复修正：{duplicate_fixed} 处。
- 仅调整段落结构，不改写正文文字、统计数值或表格数据。

## 核对说明

- 源文中 78804-78974 行显示上述小题为独立行。
- 本轮不处理第四章财政管理中更复杂的多层小题，留待后续按源文单独核对。
"""
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")


def update_memory(changed: int, duplicate_fixed: int) -> None:
    marker = "## 2026-07-02 第三十八卷财政支出小标题粘连修复"
    memory = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker in memory:
        return
    total = len(HEADINGS)
    entry = f"""
{marker}

- 对第三十八卷财政第三章财政支出的小标题压平进行修复。
- 源文依据：`{SOURCE_NOTE}`，确认经济建设支出 6 个小题和其它支出 2 个小题为独立标题行。
- 阅读版仅拆分标题边界，并修正同章开头章题重复；本轮拆分 {changed} 处，修正章题重复 {duplicate_fixed} 处，范围覆盖 {total} 处标题粘连。
- 第四章财政管理的小题层级更复杂，本轮未改，留待后续单独回源核对。
- 报告：`output/reports/reader_readability_fiscal_expenditure_subheads_20260702.md`。
"""
    MEMORY.write_text(memory.rstrip() + "\n\n" + entry.lstrip(), encoding="utf-8")


def main() -> None:
    changed, duplicate_fixed, split_counts = patch_reader()
    write_reports(changed, duplicate_fixed, split_counts)
    update_memory(changed, duplicate_fixed)
    print("fiscal expenditure subheadings repaired")
    print(f"headings_split={changed}")
    print(f"duplicate_prefix_fixed={duplicate_fixed}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()
