# -*- coding: utf-8 -*-
"""Remove remaining reader-facing OCR/table residue from paragraph text.

This is a delivery cleanup pass. It operates only on normal <p> paragraphs and
leaves headings and structured tables untouched. Removed text is reported by
section for later source-image reconstruction.
"""

from __future__ import annotations

import json
import re
from collections import Counter
from datetime import datetime
from html import unescape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_MD = ROOT / "output" / "reports" / "remaining_reader_residue_removed.md"
REPORT_JSON = ROOT / "output" / "reports" / "remaining_reader_residue_removed.json"
PROGRESS_PATH = ROOT / "output" / "reports" / "progress" / "20260629_第二批_全书尾项残文撤出.md"
MEMORY_PATH = ROOT / "PROJECT_MEMORY.md"

MAIN_RE = re.compile(r"(<main>)(.*?)(</main>)", re.S)
H2_RE = re.compile(r'<h2 id="[^"]+">(.*?)</h2>', re.S)
P_RE = re.compile(r"<p>(.*?)</p>", re.S)
TABLE_RE = re.compile(r'<table class="structured-table".*?</table>', re.S)
LONG_NUM_RE = re.compile(r"[0-9][0-9.]{25,}")
TABLE_TITLE_RE = re.compile(r"表\s*\d+\s*[-－— ]*\s*\d+|表\d+-\d+|续上表")
BAD_NOTE_RE = re.compile(r"源\s*OCR|待对照原图|待校正|待补录|核对型|原阅读版裸占位")
ENGLISH_STICKY_RE = re.compile(r"[A-Za-z]{18,}|[A-Za-z]+\d{2,}[A-Za-z]+")

# Try to preserve narrative that was glued after a table residue block.
TAIL_RE = re.compile(
    r"(第[一二三四五六七八九十百]+节[^，。；：]{0,30}|[一二三四五六七八九十]+、[^，。；：]{2,30}|主要企业简介|主要厂家|主要产品|建设烟尘控制区|销售历史上|食油\d{4}年|海水污染|三、设施|二、治理|三、排污许可证|七、自然科学技术人员普查|十二、农村住户调查)"
)


def strip_tags(value: str) -> str:
    value = re.sub(r"<[^>]+>", " ", value)
    return re.sub(r"\s+", " ", unescape(value)).strip()


def h2_ranges(text: str) -> list[tuple[int, int, str]]:
    heads = [(m.start(), strip_tags(m.group(1))) for m in H2_RE.finditer(text)]
    out = []
    for idx, (start, title) in enumerate(heads):
        end = heads[idx + 1][0] if idx + 1 < len(heads) else len(text)
        out.append((start, end, title))
    return out


def locate_section(ranges: list[tuple[int, int, str]], pos: int) -> str:
    for start, end, title in ranges:
        if start <= pos < end:
            return title
    return "未定位章节"


def text_without_tables(text: str) -> str:
    return TABLE_RE.sub(" ", text)


def audit(text: str) -> dict[str, int]:
    plain = strip_tags(text_without_tables(text))
    return {
        "long_numeric_runs": len(LONG_NUM_RE.findall(plain)),
        "serial_titles": len(TABLE_TITLE_RE.findall(plain)),
        "bad_notes": len(BAD_NOTE_RE.findall(plain)),
        "english_sticky": len(ENGLISH_STICKY_RE.findall(plain)),
    }


def reason_for(plain: str) -> str | None:
    if BAD_NOTE_RE.search(plain):
        return "读者可见处理说明/待补录说明"
    if TABLE_TITLE_RE.search(plain):
        return "裸表题/续表/OCR表格残文"
    if LONG_NUM_RE.search(plain):
        return "长数字串/OCR表格残文"
    if ENGLISH_STICKY_RE.search(plain):
        return "英文粘连/页码残留"
    return None


def split_tail(plain: str) -> tuple[str, str | None]:
    # Only preserve a tail if the marker appears after a meaningful residue prefix.
    matches = [(m.start(), m.group(1)) for m in TAIL_RE.finditer(plain) if m.start() > 20]
    if not matches:
        return plain, None
    pos, _ = min(matches)
    return plain[:pos].strip(), plain[pos:].strip()


def remove_residue(text: str) -> tuple[str, list[dict[str, str]]]:
    ranges = h2_ranges(text)
    removed: list[dict[str, str]] = []
    parts: list[str] = []
    cursor = 0
    for m in P_RE.finditer(text):
        inner = m.group(1)
        if "<table" in inner:
            continue
        plain = strip_tags(inner)
        reason = reason_for(plain)
        if not reason:
            continue
        parts.append(text[cursor:m.start()])
        section = locate_section(ranges, m.start())
        removed_text, tail = split_tail(plain)
        removed.append({
            "section": section,
            "reason": reason,
            "removed_excerpt": removed_text[:1200],
            "preserved_tail": tail or "",
        })
        if tail:
            parts.append(f"<p>{tail}</p>")
        cursor = m.end()
    parts.append(text[cursor:])
    return "".join(parts), removed


def write_reports(removed: list[dict[str, str]], before: dict[str, int], after: dict[str, int]) -> None:
    by_section = Counter(item["section"] for item in removed)
    payload = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "principle": "撤出普通段落中剩余 OCR 表格残文、处理说明和英文粘连；正式结构化表和标题结构不动。",
        "before": before,
        "after": after,
        "by_section": dict(by_section),
        "removed_count": len(removed),
        "removed": removed,
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    section_rows = "\n".join(f"| {k} | {v} |" for k, v in by_section.most_common()) or "| - | - |"
    rows = []
    for idx, item in enumerate(removed, 1):
        excerpt = item["removed_excerpt"].replace("|", "｜")
        tail = (item["preserved_tail"] or "-").replace("|", "｜")
        rows.append(f"| {idx} | {item['section']} | {item['reason']} | {excerpt} | {tail} |")
    REPORT_MD.write_text(f"""# 全书尾项残文撤出报告

生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}

## 原则

本批只处理普通段落中的尾项残文：长数字串、裸表题/续表、`源 OCR`/`待补录` 等处理说明，以及英文粘连/页码残留。正式结构化表、标题、目录和锚点不改。撤出的表格线索进入待回源核录清单。

## 统计

| 指标 | 撤出前 | 撤出后 |
| --- | ---: | ---: |
| 长数字串/OCR表格残文 | {before['long_numeric_runs']} | {after['long_numeric_runs']} |
| 裸表题/续表 | {before['serial_titles']} | {after['serial_titles']} |
| 处理说明/待补录 | {before['bad_notes']} | {after['bad_notes']} |
| 英文粘连/页码残留 | {before['english_sticky']} | {after['english_sticky']} |
| 撤出段落 | {len(removed)} | - |

## 章节分布

| 章节 | 撤出段落 |
| --- | ---: |
{section_rows}

## 撤出清单

| 序号 | 章节 | 原因 | 撤出摘录 | 保留正文尾段 |
| ---: | --- | --- | --- | --- |
{chr(10).join(rows) or '| - | - | - | - | - |'}
""", encoding="utf-8")


def write_progress(removed: list[dict[str, str]], before: dict[str, int], after: dict[str, int]) -> None:
    by_section = Counter(item["section"] for item in removed)
    top = "；".join(f"{k} {v}" for k, v in by_section.most_common(12))
    PROGRESS_PATH.write_text(f"""# 第二批：全书尾项残文撤出

更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}

## 已完成

- 从主阅读版普通段落撤出尾项残文 {len(removed)} 段。
- 主要分布：{top or '无'}。
- 证据报告：`output/reports/remaining_reader_residue_removed.md`。

## 验收数据

| 指标 | 撤出前 | 撤出后 |
| --- | ---: | ---: |
| 长数字串/OCR表格残文 | {before['long_numeric_runs']} | {after['long_numeric_runs']} |
| 裸表题/续表 | {before['serial_titles']} | {after['serial_titles']} |
| 处理说明/待补录 | {before['bad_notes']} | {after['bad_notes']} |
| 英文粘连/页码残留 | {before['english_sticky']} | {after['english_sticky']} |

## 经验

- 进入尾项阶段后，残文分散在多个卷，统一按“普通段落残文”收敛效率更高。
- 自动撤出仍需保留证据报告，后续回源核录可按报告逐表恢复。

## 下一步计划

- 复跑结构审计和交付门禁。
- 对门禁剩余项逐条人工抽样，必要时补充更细的专项脚本；随后处理交付包清单、最终总检和打开验收。
""", encoding="utf-8")


def update_memory(removed: list[dict[str, str]], before: dict[str, int], after: dict[str, int]) -> None:
    entry = f"""
## 2026-06-29 第二批全书尾项残文撤出

- 新增脚本：`scripts/remove_remaining_reader_residue.py`。
- 从主阅读版普通段落撤出尾项 OCR/表格残文、处理说明和英文粘连 {len(removed)} 段。
- 长数字串/OCR表格残文：{before['long_numeric_runs']} -> {after['long_numeric_runs']}；裸表题/续表：{before['serial_titles']} -> {after['serial_titles']}；处理说明/待补录：{before['bad_notes']} -> {after['bad_notes']}；英文粘连：{before['english_sticky']} -> {after['english_sticky']}。
- 证据报告：`output/reports/remaining_reader_residue_removed.md`。
- 经验：尾项阶段可统一按普通段落残文收敛，但必须保留撤出清单用于后续回源核录。
- 下一步：复跑交付门禁，若仍有残留则逐条补刀；通过后再进入最终交付包清单/总检。
"""
    memory = MEMORY_PATH.read_text(encoding="utf-8") if MEMORY_PATH.exists() else ""
    marker = "## 2026-06-29 第二批全书尾项残文撤出"
    if marker not in memory:
        MEMORY_PATH.write_text(memory.rstrip() + "\n\n" + entry.lstrip(), encoding="utf-8")


def main() -> None:
    text = HTML_PATH.read_text(encoding="utf-8")
    before = audit(text)
    fixed, removed = remove_residue(text)
    if fixed != text:
        HTML_PATH.write_text(fixed, encoding="utf-8")
    after = audit(fixed)
    write_reports(removed, before, after)
    write_progress(removed, before, after)
    update_memory(removed, before, after)
    print("remaining reader residue removed")
    print(f"removed={len(removed)}")
    print(f"before={before}")
    print(f"after={after}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()
