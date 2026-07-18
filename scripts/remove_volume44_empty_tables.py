# -*- coding: utf-8 -*-
"""Remove clearly empty structured tables from volume 44 reader."""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_MD = ROOT / "output" / "reports" / "volume44_empty_tables_removed.md"
REPORT_JSON = ROOT / "output" / "reports" / "volume44_empty_tables_removed.json"
PROGRESS_PATH = ROOT / "output" / "reports" / "progress" / "20260629_第二批_第四十四卷空壳表撤出主阅读版.md"
MEMORY_PATH = ROOT / "PROJECT_MEMORY.md"
SECTION_RE = re.compile(r'(<h2 id="第四十四卷-治安司法">.*?</h2>)(.*?)(?=<h2 id="第四十五卷-军事">)', re.S)
TABLE_RE = re.compile(r'<table class="structured-table".*?</table>', re.S)


def strip_tags(value: str) -> str:
    value = re.sub(r"<[^>]+>", " ", value)
    return re.sub(r"\s+", " ", value).strip()


def audit(section: str) -> dict[str, int]:
    plain_without_tables = strip_tags(TABLE_RE.sub(" ", section))
    return {
        "structured_tables": section.count('<table class="structured-table"'),
        "empty_markers": section.count("待对照原图录入"),
        "long_numeric_runs": len(re.findall(r"[0-9][0-9.]{25,}", plain_without_tables)),
        "suspect_serial_tables": len(re.findall(r"表\s*44\s*-\s*\d+", plain_without_tables)),
    }


def is_empty_table(table_html: str) -> bool:
    plain = strip_tags(table_html)
    if "待对照原图录入" in plain:
        return True
    cells = [strip_tags(cell) for cell in re.findall(r"<td>(.*?)</td>", table_html, re.S)]
    filled = [cell for cell in cells if cell]
    return len(filled) <= 1 and (not filled or filled[0] in {"数值", "待对照原图录入"})


def context_for(section: str, start: int, end: int) -> str:
    before = strip_tags(section[max(0, start - 900):start])
    after = strip_tags(section[end:min(len(section), end + 300)])
    return (before[-260:] + " || " + after[:180]).strip()


def remove_empty_tables(section: str) -> tuple[str, list[dict[str, str]]]:
    removed: list[dict[str, str]] = []
    parts: list[str] = []
    cursor = 0
    for match in TABLE_RE.finditer(section):
        table_html = match.group(0)
        if not is_empty_table(table_html):
            continue
        parts.append(section[cursor:match.start()])
        removed.append({
            "reason": "结构化表为空壳，仅含数值/待对照原图录入，未达到主阅读版交付标准",
            "table_excerpt": strip_tags(table_html),
            "context": context_for(section, match.start(), match.end()),
        })
        cursor = match.end()
    parts.append(section[cursor:])
    return "".join(parts), removed


def write_reports(removed: list[dict[str, str]], before: dict[str, int], after: dict[str, int]) -> None:
    payload = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "scope": "第四十四卷 治安司法",
        "before": before,
        "after": after,
        "removed": removed,
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    rows = "\n".join(
        f"| {idx} | {item['table_excerpt']} | {item['context']} |"
        for idx, item in enumerate(removed, 1)
    ) or "| - | - | - |"
    REPORT_MD.write_text(f"""# 第四十四卷空壳表撤出主阅读版报告

生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}

## 原则

第四十四卷治安司法表格密集，当前主阅读版中存在仅含 `数值/待对照原图录入` 的结构化空壳表。此类表不符合东辛农场志主阅读版交付标准，本轮只撤出明确空壳表；正文中的表44-*串行 OCR 残文不在本批粗暴处理，后续逐表核录或撤出。

## 统计

| 指标 | 撤出前 | 撤出后 |
| --- | ---: | ---: |
| 第四十四卷结构化表格 | {before['structured_tables']} | {after['structured_tables']} |
| `待对照原图录入` 命中 | {before['empty_markers']} | {after['empty_markers']} |
| 正文长数字串 | {before['long_numeric_runs']} | {after['long_numeric_runs']} |
| 疑似表44串行表题 | {before['suspect_serial_tables']} | {after['suspect_serial_tables']} |
| 撤出空壳表 | {len(removed)} | - |

## 撤出清单

| 序号 | 空壳表摘录 | 邻近上下文 |
| ---: | --- | --- |
{rows}
""", encoding="utf-8")


def write_progress(removed: list[dict[str, str]], before: dict[str, int], after: dict[str, int]) -> None:
    PROGRESS_PATH.write_text(f"""# 第二批：第四十四卷空壳表撤出主阅读版

更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}

## 已完成

- 从第四十四卷主阅读版撤出明确空壳结构化表 {len(removed)} 张。
- 本批只处理 `数值/待对照原图录入` 空壳表，不碰正文中表44-*串行 OCR 残文。
- 证据报告：`output/reports/volume44_empty_tables_removed.md`。

## 验收数据

| 指标 | 撤出前 | 撤出后 |
| --- | ---: | ---: |
| 第四十四卷结构化表格 | {before['structured_tables']} | {after['structured_tables']} |
| `待对照原图录入` 命中 | {before['empty_markers']} | {after['empty_markers']} |
| 正文长数字串 | {before['long_numeric_runs']} | {after['long_numeric_runs']} |
| 疑似表44串行表题 | {before['suspect_serial_tables']} | {after['suspect_serial_tables']} |

## 下一步计划

- 复跑交付门禁和结构审计。
- 下一批逐表处理表44-1、表44-3、表44-4、表44-5等正文串行 OCR 残文，能回源核录的恢复正式表，不能确认的撤出并登记。
""", encoding="utf-8")


def update_memory(removed: list[dict[str, str]], before: dict[str, int], after: dict[str, int]) -> None:
    entry = f"""
## 2026-06-29 第二批第四十四卷空壳表撤出

- 新增脚本：`scripts/remove_volume44_empty_tables.py`。
- 从第四十四卷治安司法主阅读版撤出明确空壳结构化表 {len(removed)} 张，仅含 `数值/待对照原图录入`，不符合东辛交付标准。
- 第四十四卷结构化表格：{before['structured_tables']} -> {after['structured_tables']}；`待对照原图录入`：{before['empty_markers']} -> {after['empty_markers']}。
- 证据报告：`output/reports/volume44_empty_tables_removed.md`。
- 下一步：逐表处理表44-*正文串行 OCR 残文，优先表44-1、表44-3、表44-4、表44-5。
"""
    memory = MEMORY_PATH.read_text(encoding="utf-8") if MEMORY_PATH.exists() else ""
    marker = "## 2026-06-29 第二批第四十四卷空壳表撤出"
    if marker not in memory:
        MEMORY_PATH.write_text(memory.rstrip() + "\n\n" + entry.lstrip(), encoding="utf-8")


def main() -> None:
    text = HTML_PATH.read_text(encoding="utf-8")
    match = SECTION_RE.search(text)
    if not match:
        raise RuntimeError("Cannot locate 第四十四卷 section")
    heading, section = match.groups()
    before = audit(section)
    new_section, removed = remove_empty_tables(section)
    fixed = text[:match.start()] + heading + new_section + text[match.end():]
    if fixed != text:
        HTML_PATH.write_text(fixed, encoding="utf-8")
    after = audit(new_section)
    write_reports(removed, before, after)
    write_progress(removed, before, after)
    update_memory(removed, before, after)
    print("volume 44 empty tables removed")
    print(f"removed={len(removed)}")
    print(f"before={before}")
    print(f"after={after}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()
