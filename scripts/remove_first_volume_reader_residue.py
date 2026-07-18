# -*- coding: utf-8 -*-
"""Remove reader-facing residue from 第一卷 自然环境.

The first volume still contains OCR table text and workbench notes left after
unverified tables were removed. This script removes only paragraph-level reader
residue; structured tables and ordinary narrative paragraphs are left untouched.
"""

from __future__ import annotations

import json
import re
from datetime import datetime
from html import unescape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_MD = ROOT / "output" / "reports" / "first_volume_reader_residue_removed.md"
REPORT_JSON = ROOT / "output" / "reports" / "first_volume_reader_residue_removed.json"
PROGRESS_PATH = ROOT / "output" / "reports" / "progress" / "20260629_第二批_第一卷自然环境残文撤出主阅读版.md"
MEMORY_PATH = ROOT / "PROJECT_MEMORY.md"

SECTION_RE = re.compile(r'(<h2 id="第一卷-自然环境">.*?</h2>)(.*?)(?=<h2 id="第二卷-建置区划">)', re.S)
P_RE = re.compile(r"<p>(.*?)</p>", re.S)
TABLE_RE = re.compile(r'<table class="structured-table".*?</table>', re.S)
TABLE1_RE = re.compile(r"表\s*1\s*[-－— ]*\s*\d+|表1-\d+")
LONG_NUM_RE = re.compile(r"[0-9][0-9.]{25,}")
BAD_NOTE_RE = re.compile(r"源\s*OCR|待对照原图|待校正|待补录|补录|缺读|核对型")


def strip_tags(value: str) -> str:
    value = re.sub(r"<[^>]+>", " ", value)
    return re.sub(r"\s+", " ", unescape(value)).strip()


def audit(section: str) -> dict[str, int]:
    plain = strip_tags(TABLE_RE.sub(" ", section))
    return {
        "structured_tables": section.count('<table class="structured-table"'),
        "long_numeric_runs": len(LONG_NUM_RE.findall(plain)),
        "table1_serial_titles": len(TABLE1_RE.findall(plain)),
        "bad_notes": len(BAD_NOTE_RE.findall(plain)),
    }


def residue_reason(plain: str) -> str | None:
    if BAD_NOTE_RE.search(plain):
        return "读者可见源OCR/待补录/缺读等处理说明"
    if LONG_NUM_RE.search(plain):
        return "第一卷表格被OCR串行为正文长数字段"
    if TABLE1_RE.search(plain):
        return "第一卷裸表题/表格残文未达到主阅读版交付标准"
    return None


def remove_residue(section: str) -> tuple[str, list[dict[str, str]]]:
    removed: list[dict[str, str]] = []

    def repl(match: re.Match[str]) -> str:
        inner = match.group(1)
        plain = strip_tags(inner)
        reason = residue_reason(plain)
        if not reason:
            return match.group(0)
        removed.append({
            "reason": reason,
            "excerpt": plain[:1200],
        })
        return ""

    return P_RE.sub(repl, section), removed


def write_reports(removed: list[dict[str, str]], before: dict[str, int], after: dict[str, int]) -> None:
    payload = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "scope": "第一卷 自然环境",
        "principle": "撤出读者可见表格OCR残文和工作台处理说明；不把未核OCR串行文本伪装为成品表。",
        "before": before,
        "after": after,
        "removed": removed,
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    rows = []
    for idx, item in enumerate(removed, 1):
        excerpt = item["excerpt"].replace("|", "｜")
        rows.append(f"| {idx} | {item['reason']} | {excerpt} |")
    rows_text = "\n".join(rows) or "| - | - | - |"
    REPORT_MD.write_text(f"""# 第一卷自然环境残文撤出主阅读版报告

生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}

## 原则

按东辛农场志交付口径，主阅读版不得显示裸表题、串行 OCR 数字块、`源 OCR`、`待对照原图补录`、`缺读`、`待校正` 等工作台内容。本批仅撤出第一卷自然环境中段落级残文，正式结构化表和普通正文不改。

## 统计

| 指标 | 撤出前 | 撤出后 |
| --- | ---: | ---: |
| 第一卷结构化表 | {before['structured_tables']} | {after['structured_tables']} |
| 正文长数字串 | {before['long_numeric_runs']} | {after['long_numeric_runs']} |
| 表1-*裸表题/串行表题 | {before['table1_serial_titles']} | {after['table1_serial_titles']} |
| 处理说明/待补录标记 | {before['bad_notes']} | {after['bad_notes']} |
| 撤出段落 | {len(removed)} | - |

## 撤出清单

| 序号 | 原因 | 摘录 |
| ---: | --- | --- |
{rows_text}
""", encoding="utf-8")


def write_progress(removed: list[dict[str, str]], before: dict[str, int], after: dict[str, int]) -> None:
    PROGRESS_PATH.write_text(f"""# 第二批：第一卷自然环境残文撤出主阅读版

更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}

## 已完成

- 从第一卷自然环境主阅读版撤出裸表题、串行 OCR 数字块和处理说明段落 {len(removed)} 段。
- 本批不补造表格数据；撤出的表格线索进入证据报告，后续需回源 PDF/页图核录后再嵌回正式结构化表。
- 证据报告：`output/reports/first_volume_reader_residue_removed.md`。

## 验收数据

| 指标 | 撤出前 | 撤出后 |
| --- | ---: | ---: |
| 第一卷结构化表 | {before['structured_tables']} | {after['structured_tables']} |
| 正文长数字串 | {before['long_numeric_runs']} | {after['long_numeric_runs']} |
| 表1-*裸表题/串行表题 | {before['table1_serial_titles']} | {after['table1_serial_titles']} |
| 处理说明/待补录标记 | {before['bad_notes']} | {after['bad_notes']} |

## 经验

- 第一卷之前的“核对型表”撤出后，仍会留下表题、注释和长数字段，必须做段落级残文收敛。
- 主阅读版宁可暂缺未核表，也不能展示 `源 OCR`、`待补录` 或无行列关系的数字串。

## 下一步计划

- 复跑 `scripts/audit_delivery_quality.py` 和 `scripts/audit_full_reader.py`。
- 若第一卷退出门禁前列，转入第六卷环境保护或第三十六卷粮油购销的表格 OCR 残文专项。
""", encoding="utf-8")


def update_memory(removed: list[dict[str, str]], before: dict[str, int], after: dict[str, int]) -> None:
    entry = f"""
## 2026-06-29 第二批第一卷自然环境残文撤出

- 新增脚本：`scripts/remove_first_volume_reader_residue.py`。
- 从第一卷自然环境主阅读版撤出裸表题、串行 OCR 数字块和处理说明段落 {len(removed)} 段。
- 第一卷正文长数字串：{before['long_numeric_runs']} -> {after['long_numeric_runs']}；表1-*裸表题/串行表题：{before['table1_serial_titles']} -> {after['table1_serial_titles']}；处理说明/待补录标记：{before['bad_notes']} -> {after['bad_notes']}。
- 证据报告：`output/reports/first_volume_reader_residue_removed.md`。
- 经验：撤出未核结构化表后，还要清理遗留在正文中的裸表题和说明文字；主阅读版不得显示 `源 OCR`、`待补录` 或无行列关系数字串。
- 下一步：复跑交付门禁后，转入第六卷环境保护或第三十六卷粮油购销的表格残文专项。
"""
    memory = MEMORY_PATH.read_text(encoding="utf-8") if MEMORY_PATH.exists() else ""
    marker = "## 2026-06-29 第二批第一卷自然环境残文撤出"
    if marker not in memory:
        MEMORY_PATH.write_text(memory.rstrip() + "\n\n" + entry.lstrip(), encoding="utf-8")


def main() -> None:
    text = HTML_PATH.read_text(encoding="utf-8")
    match = SECTION_RE.search(text)
    if not match:
        raise RuntimeError("Cannot locate 第一卷 section")
    heading, section = match.groups()
    before = audit(section)
    new_section, removed = remove_residue(section)
    fixed = text[:match.start()] + heading + new_section + text[match.end():]
    if fixed != text:
        HTML_PATH.write_text(fixed, encoding="utf-8")
    after = audit(new_section)
    write_reports(removed, before, after)
    write_progress(removed, before, after)
    update_memory(removed, before, after)
    print("first volume reader residue removed")
    print(f"removed={len(removed)}")
    print(f"before={before}")
    print(f"after={after}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()
