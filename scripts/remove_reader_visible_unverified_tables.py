# -*- coding: utf-8 -*-
"""Remove reader-visible unverified/workbench structured tables from final reader."""

from __future__ import annotations

import json
import re
from collections import Counter
from datetime import datetime
from html import unescape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_MD = ROOT / "output" / "reports" / "reader_visible_unverified_tables_removed.md"
REPORT_JSON = ROOT / "output" / "reports" / "reader_visible_unverified_tables_removed.json"
PROGRESS_PATH = ROOT / "output" / "reports" / "progress" / "20260629_第二批_全书未核表撤出主阅读版.md"
MEMORY_PATH = ROOT / "PROJECT_MEMORY.md"

H2_RE = re.compile(r'<h2 id="[^"]+">(.*?)</h2>', re.S)
TABLE_RE = re.compile(r'<table class="structured-table".*?</table>', re.S)
BAD_MARKERS = [
    "待对照原图录入",
    "待对照原图补录",
    "待原图",
    "待校正",
    "待补录",
    "源 OCR",
    "源OCR",
    "核对状态",
]


def strip_tags(value: str) -> str:
    value = re.sub(r"<[^>]+>", " ", value)
    return re.sub(r"\s+", " ", unescape(value)).strip()


def h2_ranges(text: str) -> list[tuple[int, int, str]]:
    heads = [(m.start(), strip_tags(m.group(1))) for m in H2_RE.finditer(text)]
    ranges = []
    for idx, (start, title) in enumerate(heads):
        end = heads[idx + 1][0] if idx + 1 < len(heads) else len(text)
        ranges.append((start, end, title))
    return ranges


def locate_title(ranges: list[tuple[int, int, str]], pos: int) -> str:
    for start, end, title in ranges:
        if start <= pos < end:
            return title
    return "未定位章节"


def is_bad_table(table_html: str) -> tuple[bool, list[str]]:
    plain = strip_tags(table_html)
    hits = [marker for marker in BAD_MARKERS if marker in plain]
    if hits:
        return True, hits
    return False, []


def audit(text: str) -> dict[str, int]:
    tables = TABLE_RE.findall(text)
    bad_tables = 0
    for table in tables:
        bad, _ = is_bad_table(table)
        if bad:
            bad_tables += 1
    return {
        "structured_tables": len(tables),
        "unverified_tables": bad_tables,
        "待对照原图录入": text.count("待对照原图录入"),
        "待对照原图补录": text.count("待对照原图补录"),
        "待校正": text.count("待校正"),
        "源_OCR": text.count("源 OCR") + text.count("源OCR"),
    }


def remove_tables(text: str) -> tuple[str, list[dict[str, object]]]:
    ranges = h2_ranges(text)
    removed: list[dict[str, object]] = []
    parts: list[str] = []
    cursor = 0
    for match in TABLE_RE.finditer(text):
        table_html = match.group(0)
        bad, hits = is_bad_table(table_html)
        if not bad:
            continue
        parts.append(text[cursor:match.start()])
        title = locate_title(ranges, match.start())
        plain = strip_tags(table_html)
        removed.append({
            "section": title,
            "markers": hits,
            "excerpt": plain[:900],
        })
        cursor = match.end()
    parts.append(text[cursor:])
    return "".join(parts), removed


def write_reports(removed: list[dict[str, object]], before: dict[str, int], after: dict[str, int]) -> None:
    by_section = Counter(str(item["section"]) for item in removed)
    payload = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "principle": "主阅读版撤出含待核、待录入、源OCR、核对状态等工作台标记的结构化表；未核表不得伪装为成品表。",
        "before": before,
        "after": after,
        "removed_count": len(removed),
        "by_section": dict(by_section),
        "removed": removed,
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    section_rows = "\n".join(f"| {section} | {count} |" for section, count in by_section.most_common()) or "| - | - |"
    rows = []
    for idx, item in enumerate(removed, 1):
        markers = "、".join(item["markers"]) if isinstance(item["markers"], list) else str(item["markers"])
        excerpt = str(item["excerpt"]).replace("|", "｜")
        rows.append(f"| {idx} | {item['section']} | {markers} | {excerpt} |")
    rows_text = "\n".join(rows) or "| - | - | - | - |"

    REPORT_MD.write_text(f"""# 全书未核结构化表撤出主阅读版报告

生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}

## 原则

东辛农场志交付口径要求主阅读版只展示已核结构化表。凡含 `待对照原图录入`、`待对照原图补录`、`待校正`、`源 OCR`、`核对状态` 等工作台标记的结构化表，本批从主阅读版撤出，登记为后续回源核录任务。

## 统计

| 指标 | 撤出前 | 撤出后 |
| --- | ---: | ---: |
| 主阅读版结构化表 | {before['structured_tables']} | {after['structured_tables']} |
| 含未核/工作台标记表 | {before['unverified_tables']} | {after['unverified_tables']} |
| `待对照原图录入` | {before['待对照原图录入']} | {after['待对照原图录入']} |
| `待对照原图补录` | {before['待对照原图补录']} | {after['待对照原图补录']} |
| `待校正` | {before['待校正']} | {after['待校正']} |
| `源 OCR` | {before['源_OCR']} | {after['源_OCR']} |
| 撤出表格 | {len(removed)} | - |

## 章节分布

| 章节 | 撤出表数 |
| --- | ---: |
{section_rows}

## 撤出清单

| 序号 | 章节 | 命中标记 | 表格摘录 |
| ---: | --- | --- | --- |
{rows_text}
""", encoding="utf-8")


def write_progress(removed: list[dict[str, object]], before: dict[str, int], after: dict[str, int]) -> None:
    by_section = Counter(str(item["section"]) for item in removed)
    top = "；".join(f"{section} {count}" for section, count in by_section.most_common(8))
    PROGRESS_PATH.write_text(f"""# 第二批：全书未核结构化表撤出主阅读版

更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}

## 已完成

- 从主阅读版撤出含未核/工作台标记的结构化表 {len(removed)} 张。
- 撤出对象包括 `待对照原图录入`、`待对照原图补录`、`待校正`、`源 OCR`、`核对状态` 等读者可见非交付内容。
- 主要分布：{top or '无'}。
- 证据报告：`output/reports/reader_visible_unverified_tables_removed.md`。

## 验收数据

| 指标 | 撤出前 | 撤出后 |
| --- | ---: | ---: |
| 主阅读版结构化表 | {before['structured_tables']} | {after['structured_tables']} |
| 含未核/工作台标记表 | {before['unverified_tables']} | {after['unverified_tables']} |
| `待对照原图录入` | {before['待对照原图录入']} | {after['待对照原图录入']} |
| `待对照原图补录` | {before['待对照原图补录']} | {after['待对照原图补录']} |
| `待校正` | {before['待校正']} | {after['待校正']} |
| `源 OCR` | {before['源_OCR']} | {after['源_OCR']} |

## 经验

- “核对型结构表”对工作台有价值，但不等于交付表；主阅读版显示 `源 OCR`、`备注`、`待校正` 会直接破坏交付观感。
- 下一步回补表格时必须先核源图/PDF，达到已核结构化表标准后再嵌回正文。

## 下一步计划

- 复跑交付质量门禁和结构审计，确认 `待对照原图录入`、空表、可见处理说明是否显著下降。
- 根据新门禁排序继续处理剩余非表格 OCR 串行残文，优先第五十卷教育、第四十六卷人事、第二十九卷口岸等高发章节。
""", encoding="utf-8")


def update_memory(removed: list[dict[str, object]], before: dict[str, int], after: dict[str, int]) -> None:
    entry = f"""
## 2026-06-29 第二批全书未核结构化表撤出

- 新增脚本：`scripts/remove_reader_visible_unverified_tables.py`。
- 从主阅读版撤出含 `待对照原图录入`、`待对照原图补录`、`待校正`、`源 OCR`、`核对状态` 等工作台/未核标记的结构化表 {len(removed)} 张。
- 主阅读版结构化表：{before['structured_tables']} -> {after['structured_tables']}；含未核标记表：{before['unverified_tables']} -> {after['unverified_tables']}。
- `待对照原图录入`：{before['待对照原图录入']} -> {after['待对照原图录入']}；`源 OCR`：{before['源_OCR']} -> {after['源_OCR']}。
- 证据报告：`output/reports/reader_visible_unverified_tables_removed.md`。
- 经验：核对型表只能留在工作台/报告中，不能作为主阅读版交付内容；后续嵌回必须回源核录。
- 下一步：按新门禁排序继续清理非结构化正文中的长数字串/OCR 表格残文，并逐批验收。
"""
    memory = MEMORY_PATH.read_text(encoding="utf-8") if MEMORY_PATH.exists() else ""
    marker = "## 2026-06-29 第二批全书未核结构化表撤出"
    if marker not in memory:
        MEMORY_PATH.write_text(memory.rstrip() + "\n\n" + entry.lstrip(), encoding="utf-8")


def main() -> None:
    text = HTML_PATH.read_text(encoding="utf-8")
    before = audit(text)
    fixed, removed = remove_tables(text)
    if fixed != text:
        HTML_PATH.write_text(fixed, encoding="utf-8")
    after = audit(fixed)
    write_reports(removed, before, after)
    write_progress(removed, before, after)
    update_memory(removed, before, after)
    print("reader-visible unverified tables removed")
    print(f"removed={len(removed)}")
    print(f"before={before}")
    print(f"after={after}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()
