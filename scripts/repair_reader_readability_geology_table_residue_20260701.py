# -*- coding: utf-8 -*-
"""Remove duplicated OCR-linearized residue for 表1-1 in the final reader.

The verified structured table LYG-上-T001 is already embedded. The reader may
also contain OCR-linearized paragraphs from the table pages, which make the same
table appear as broken prose. This script removes those exact paragraphs and is
safe to rerun after the residue has already been removed.
"""

from __future__ import annotations

import json
import re
from datetime import datetime
from html import unescape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_geology_table_residue_20260701.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_geology_table_residue_20260701.md"
PROGRESS_PATH = ROOT / "output" / "reports" / "progress" / "20260701_第一卷地层系统表线性化残文修复.md"
MEMORY_PATH = ROOT / "PROJECT_MEMORY.md"

P_RE = re.compile(r"<p>.*?</p>", re.S)
BAD_PARAGRAPH_MARKERS = [
    "上部；以白云斜长片麻岩为主",
    "朐山组",
    "沙河组",
    "阿湖组",
    "班庄组",
    "长混合片麻岩",
]

REQUIRED_STRUCTURED_MARKERS = [
    'id="table-LYG-上-T001"',
    "表1-1 连云港市地层系统表",
    "朐山组",
    "沙河组",
    "阿湖组",
    "班庄组",
    "夹山组",
]


def strip_tags(html: str) -> str:
    text = re.sub(r"<[^>]+>", " ", html)
    return re.sub(r"\s+", " ", unescape(text)).strip()


def find_bad_paragraphs(html: str) -> list[str]:
    return [
        match.group(0)
        for match in P_RE.finditer(html)
        if all(marker in strip_tags(match.group(0)) for marker in BAD_PARAGRAPH_MARKERS)
    ]


def write_report(removed: list[str], before_count: int, after_count: int) -> None:
    payload = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "scope": "第一卷自然环境 表1-1 连云港市地层系统表",
        "html_path": str(HTML_PATH),
        "principle": "删除已由 verified 结构化表承载的 OCR 线性化重复残文，不改结构化表数据。",
        "before_bad_paragraphs": before_count,
        "after_bad_paragraphs": after_count,
        "removed": [strip_tags(item) for item in removed],
        "verified_table_markers": REQUIRED_STRUCTURED_MARKERS,
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    removed_rows = []
    for idx, item in enumerate(payload["removed"], 1):
        removed_rows.append(f"| {idx} | {item[:1000].replace('|', '｜')} |")
    rows = "\n".join(removed_rows) or "| - | - |"
    REPORT_MD.write_text(
        f"""# 第一卷地层系统表线性化残文修复报告

生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}

## 修复原则

`LYG-上-T001` 已作为 verified 结构化表嵌入最终阅读版。最终 HTML 中可能另有由续页 OCR 线性化形成的正文残文，内容对应朐山组、沙河组、阿湖组、班庄组等表格行。本次只删除重复残文，保留结构化表。

## 结果

| 项目 | 数量 |
| --- | ---: |
| 修复前命中残文段落 | {before_count} |
| 修复后命中残文段落 | {after_count} |
| 删除段落 | {len(removed)} |

## 删除摘录

| 序号 | 摘录 |
| ---: | --- |
{rows}

## 保留证据

最终阅读版仍包含 `id="table-LYG-上-T001"` 和 `表1-1 连云港市地层系统表`，表内保留朐山组、沙河组、阿湖组、班庄组、夹山组等行。
""",
        encoding="utf-8",
    )


def write_progress(before_count: int, after_count: int, removed_count: int) -> None:
    PROGRESS_PATH.write_text(
        f"""# 第一卷地层系统表线性化残文修复

更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}

## 已完成

- 修复对象：最终阅读版 `output/final_reader/连云港市志_全书.html` 中第一卷自然环境 `表1-1 连云港市地层系统表` 的 OCR 线性化重复残文。
- 源证据：`workbench/ocr/paddle_ocr/上/part01/page_0130.txt`、`workbench/ocr/paddle_ocr/上/part01/page_0131.txt`；结构化表源为 `workbench/table_entries/上/data/LYG-上-T001.json`。
- 处理方式：删除已由 verified 结构化表承载的重复正文段落，不改表格数据。

## 验收

| 项目 | 修复前 | 修复后 |
| --- | ---: | ---: |
| 线性化残文命中 | {before_count} | {after_count} |
| 删除段落 | {removed_count} | - |
""",
        encoding="utf-8",
    )


def update_memory(before_count: int, after_count: int, removed_count: int) -> None:
    marker = "## 2026-07-01 第一卷地层系统表线性化残文修复"
    memory = MEMORY_PATH.read_text(encoding="utf-8") if MEMORY_PATH.exists() else ""
    if marker in memory:
        return
    entry = f"""
{marker}

- 新增脚本：`scripts/repair_reader_readability_geology_table_residue_20260701.py`。
- 修复最终阅读版第一卷自然环境中 `表1-1 连云港市地层系统表` 的 OCR 线性化重复残文：命中 {before_count} -> {after_count}，删除段落 {removed_count} 段。
- 保留 verified 结构化表 `LYG-上-T001`，不改表格数据；源证据为 `workbench/ocr/paddle_ocr/上/part01/page_0130.txt`、`page_0131.txt` 与 `workbench/table_entries/上/data/LYG-上-T001.json`。
- 报告：`output/reports/reader_readability_geology_table_residue_20260701.md`。
- 经验：最终阅读版嵌回 verified 表后，还必须删除同页 OCR 线性化正文残文，否则读者会看到重复且破碎的表格内容。
"""
    MEMORY_PATH.write_text(memory.rstrip() + "\n\n" + entry.lstrip(), encoding="utf-8")


def main() -> None:
    html = HTML_PATH.read_text(encoding="utf-8")
    for marker in REQUIRED_STRUCTURED_MARKERS:
        if marker not in html:
            raise RuntimeError(f"verified structured table marker missing before edit: {marker}")

    matches = find_bad_paragraphs(html)
    before_count = len(matches)
    fixed = html
    for match in matches:
        fixed = fixed.replace(match, "", 1)
    after_count = len(find_bad_paragraphs(fixed))

    for marker in REQUIRED_STRUCTURED_MARKERS:
        if marker not in fixed:
            raise RuntimeError(f"verified structured table marker missing after edit: {marker}")

    if fixed != html:
        HTML_PATH.write_text(fixed, encoding="utf-8")

    write_report(matches, before_count, after_count)
    write_progress(before_count, after_count, len(matches))
    update_memory(before_count, after_count, len(matches))
    if matches:
        print("geology table OCR-linearized residue repaired")
    else:
        print("geology table OCR-linearized residue already absent")
    print(f"before={before_count}")
    print(f"after={after_count}")
    print(f"removed={len(matches)}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()
