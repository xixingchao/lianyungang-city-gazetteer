# -*- coding: utf-8 -*-
"""Move unverified workbench-style tables out of volume 15 reader."""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_MD = ROOT / "output" / "reports" / "volume15_workbench_tables_removed.md"
REPORT_JSON = ROOT / "output" / "reports" / "volume15_workbench_tables_removed.json"
PROGRESS_PATH = ROOT / "output" / "reports" / "progress" / "20260629_第二批_第十五卷核对表撤出主阅读版.md"
MEMORY_PATH = ROOT / "PROJECT_MEMORY.md"

SECTION_RE = re.compile(r'(<h2 id="第十五卷-纺织工业">.*?</h2>)(.*?)(?=<h2 id="第十六卷-皮塑工业">)', re.S)
TABLE_RE = re.compile(r'<table class="structured-table".*?</table>(?:\s*<p>注：(?:源 OCR|.*?待(?:原图|对照原图|校正|补录)).*?</p>)?', re.S)
BAD_MARKERS = ("源 OCR", "待对照原图", "待原图", "待校正", "待补录", "待核对", "备注")


def strip_tags(value: str) -> str:
    value = re.sub(r"<[^>]+>", "", value)
    return re.sub(r"\s+", " ", value).strip()


def audit(section: str) -> dict[str, int]:
    plain = strip_tags(section)
    return {
        "structured_tables": section.count('<table class="structured-table"'),
        "workbench_markers": sum(plain.count(marker) for marker in BAD_MARKERS),
        "long_numeric_runs": len(re.findall(r"[0-9][0-9.]{25,}", plain)),
    }


def remove_tables(section: str) -> tuple[str, list[dict[str, str]]]:
    removed: list[dict[str, str]] = []

    def repl(match: re.Match[str]) -> str:
        html = match.group(0)
        plain = strip_tags(html)
        if not any(marker in plain for marker in BAD_MARKERS):
            return html
        caption_match = re.search(r"<caption>(.*?)</caption>", html, re.S)
        caption = strip_tags(caption_match.group(1)) if caption_match else "无 caption"
        removed.append({
            "caption": caption,
            "reason": "含源 OCR/待校正/待补录/备注等工作台字段，未达到主阅读版交付标准",
            "excerpt": plain[:240],
        })
        return ""

    return TABLE_RE.sub(repl, section), removed


def write_reports(removed: list[dict[str, str]], before: dict[str, int], after: dict[str, int]) -> None:
    payload = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "scope": "第十五卷 纺织工业",
        "before": before,
        "after": after,
        "removed": removed,
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    rows = "\n".join(
        f"| {idx} | {item['caption']} | {item['reason']} | {item['excerpt']} |"
        for idx, item in enumerate(removed, 1)
    ) or "| - | - | - | - |"
    REPORT_MD.write_text(f"""# 第十五卷核对型表格撤出主阅读版报告

生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}

## 原则

含 `源 OCR`、`待校正`、`待补录`、`备注` 等工作台字段的核对型表格，不符合东辛农场志主阅读版交付标准。本轮从主阅读版撤出，保留在报告中，待源 PDF 核录后再恢复为正式结构化表。

## 统计

| 指标 | 撤出前 | 撤出后 |
| --- | ---: | ---: |
| 第十五卷结构化表格 | {before['structured_tables']} | {after['structured_tables']} |
| 工作台字段命中 | {before['workbench_markers']} | {after['workbench_markers']} |
| 长数字串 | {before['long_numeric_runs']} | {after['long_numeric_runs']} |
| 撤出表格 | {len(removed)} | - |

## 撤出清单

| 序号 | 表题 | 原因 | 摘录 |
| ---: | --- | --- | --- |
{rows}
""", encoding="utf-8")


def write_progress(removed: list[dict[str, str]], before: dict[str, int], after: dict[str, int]) -> None:
    items = "\n".join(f"- {item['caption']}" for item in removed) or "- 本次复跑未撤出新表格，脚本保持幂等。"
    PROGRESS_PATH.write_text(f"""# 第二批：第十五卷核对型表格撤出主阅读版

更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}

## 已完成
{items}

## 验收数据

| 指标 | 撤出前 | 撤出后 |
| --- | ---: | ---: |
| 第十五卷结构化表格 | {before['structured_tables']} | {after['structured_tables']} |
| 工作台字段命中 | {before['workbench_markers']} | {after['workbench_markers']} |
| 长数字串 | {before['long_numeric_runs']} | {after['long_numeric_runs']} |

## 下一步计划

- 复跑交付质量门禁与结构审计。
- 第十五卷剩余表格逐个判断是否为正式表；撤出项待对照源 PDF 重建后再回主阅读版。
""", encoding="utf-8")


def update_memory(removed: list[dict[str, str]], before: dict[str, int], after: dict[str, int]) -> None:
    entry = f"""
## 2026-06-29 第二批第十五卷核对表撤出

- 新增脚本：`scripts/remove_volume15_workbench_tables.py`。
- 按东辛交付标准，从第十五卷主阅读版撤出含 `源 OCR`、`待校正`、`待补录`、`备注` 等工作台字段的核对型表格。
- 撤出表格：{len(removed)}；第十五卷结构化表格：{before['structured_tables']} -> {after['structured_tables']}；工作台字段命中：{before['workbench_markers']} -> {after['workbench_markers']}。
- 证据报告：`output/reports/volume15_workbench_tables_removed.md`。
- 进度文档：`output/reports/progress/20260629_第二批_第十五卷核对表撤出主阅读版.md`。
"""
    memory = MEMORY_PATH.read_text(encoding="utf-8") if MEMORY_PATH.exists() else ""
    marker = "## 2026-06-29 第二批第十五卷核对表撤出"
    if marker not in memory:
        MEMORY_PATH.write_text(memory.rstrip() + "\n\n" + entry.lstrip(), encoding="utf-8")


def main() -> None:
    text = HTML_PATH.read_text(encoding="utf-8")
    match = SECTION_RE.search(text)
    if not match:
        raise RuntimeError("Cannot locate 第十五卷 section")
    heading, section = match.groups()
    before = audit(section)
    new_section, removed = remove_tables(section)
    fixed = text[:match.start()] + heading + new_section + text[match.end():]
    if fixed != text:
        HTML_PATH.write_text(fixed, encoding="utf-8")
    after = audit(new_section)
    write_reports(removed, before, after)
    write_progress(removed, before, after)
    update_memory(removed, before, after)
    print("volume 15 workbench tables removed")
    print(f"removed={len(removed)}")
    print(f"before={before}")
    print(f"after={after}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()
