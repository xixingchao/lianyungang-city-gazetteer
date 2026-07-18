# -*- coding: utf-8 -*-
"""Remove table OCR residue from 第三十六卷 粮油购销."""

from __future__ import annotations

import json
import re
from datetime import datetime
from html import unescape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_MD = ROOT / "output" / "reports" / "volume36_grain_table_residue_removed.md"
REPORT_JSON = ROOT / "output" / "reports" / "volume36_grain_table_residue_removed.json"
PROGRESS_PATH = ROOT / "output" / "reports" / "progress" / "20260629_第二批_第三十六卷粮油购销表格残文撤出.md"
MEMORY_PATH = ROOT / "PROJECT_MEMORY.md"

SECTION_RE = re.compile(r'(<h2 id="第三十六卷-[^"]+">.*?</h2>)(.*?)(?=<h2 id="第三十七卷-[^"]+">)', re.S)
P_RE = re.compile(r"<p>(.*?)</p>", re.S)
TABLE_RE = re.compile(r'<table class="structured-table".*?</table>', re.S)
TABLE36_RE = re.compile(r"表\s*36\s*[-－— ]*\s*\d+|表36\s*[-－— ]*\s*\d+|表36\d+")
LONG_NUM_RE = re.compile(r"[0-9][0-9.]{25,}")

TAIL_MARKERS = [
    "1958年，粮食部门",
    "二、合同定购",
    "销售历史上",
    "食油1956年",
    "海州，唐时设司库参军",
    "二、储量",
    "连云港市历来使用石磨",
    "三、设施",
]


def strip_tags(value: str) -> str:
    value = re.sub(r"<[^>]+>", " ", value)
    return re.sub(r"\s+", " ", unescape(value)).strip()


def audit(section: str) -> dict[str, int]:
    plain = strip_tags(TABLE_RE.sub(" ", section))
    return {
        "structured_tables": section.count('<table class="structured-table"'),
        "long_numeric_runs": len(LONG_NUM_RE.findall(plain)),
        "table36_serial_titles": len(TABLE36_RE.findall(plain)),
    }


def split_tail(plain: str) -> tuple[str, str | None]:
    hits = [(plain.find(marker), marker) for marker in TAIL_MARKERS if plain.find(marker) > 0]
    if not hits:
        return plain, None
    pos, _ = min(hits)
    return plain[:pos].strip(), plain[pos:].strip()


def residue_reason(plain: str) -> str | None:
    if TABLE36_RE.search(plain):
        return "第三十六卷裸表题/表格OCR残文"
    if LONG_NUM_RE.search(plain):
        return "第三十六卷表格数字被OCR串行为正文"
    return None


def remove_residue(section: str) -> tuple[str, list[dict[str, str]]]:
    removed: list[dict[str, str]] = []

    def repl(match: re.Match[str]) -> str:
        plain = strip_tags(match.group(1))
        reason = residue_reason(plain)
        if not reason:
            return match.group(0)
        removed_text, tail = split_tail(plain)
        removed.append({
            "reason": reason,
            "removed_excerpt": removed_text[:1200],
            "preserved_tail": tail or "",
        })
        if tail:
            return f"<p>{tail}</p>"
        return ""

    return P_RE.sub(repl, section), removed


def write_reports(removed: list[dict[str, str]], before: dict[str, int], after: dict[str, int]) -> None:
    payload = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "scope": "第三十六卷 粮油购销",
        "before": before,
        "after": after,
        "removed": removed,
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    rows = []
    for idx, item in enumerate(removed, 1):
        excerpt = item["removed_excerpt"].replace("|", "｜")
        tail = (item["preserved_tail"] or "-").replace("|", "｜")
        rows.append(f"| {idx} | {item['reason']} | {excerpt} | {tail} |")
    rows_text = "\n".join(rows) or "| - | - | - | - |"
    REPORT_MD.write_text(f"""# 第三十六卷粮油购销表格残文撤出报告

生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}

## 原则

粮油购销卷中多张统计表被 OCR 串行为正文。按东辛交付标准，未核表格不得在主阅读版展示；本批撤出表格残文，保留能识别的正文尾段，并登记待回源核录。

## 统计

| 指标 | 撤出前 | 撤出后 |
| --- | ---: | ---: |
| 第三十六卷结构化表 | {before['structured_tables']} | {after['structured_tables']} |
| 正文长数字串 | {before['long_numeric_runs']} | {after['long_numeric_runs']} |
| 表36-*裸表题/串行表题 | {before['table36_serial_titles']} | {after['table36_serial_titles']} |
| 撤出段落 | {len(removed)} | - |

## 撤出清单

| 序号 | 原因 | 撤出摘录 | 保留正文尾段 |
| ---: | --- | --- | --- |
{rows_text}
""", encoding="utf-8")


def write_progress(removed: list[dict[str, str]], before: dict[str, int], after: dict[str, int]) -> None:
    PROGRESS_PATH.write_text(f"""# 第二批：第三十六卷粮油购销表格残文撤出

更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}

## 已完成

- 从第三十六卷粮油购销主阅读版撤出表格 OCR 残文 {len(removed)} 段。
- 对表格残文与正文粘连的段落，保留了合同定购、销售、食油、储量、设施、粮油加工等正文尾段。
- 证据报告：`output/reports/volume36_grain_table_residue_removed.md`。

## 验收数据

| 指标 | 撤出前 | 撤出后 |
| --- | ---: | ---: |
| 第三十六卷结构化表 | {before['structured_tables']} | {after['structured_tables']} |
| 正文长数字串 | {before['long_numeric_runs']} | {after['long_numeric_runs']} |
| 表36-*裸表题/串行表题 | {before['table36_serial_titles']} | {after['table36_serial_titles']} |

## 经验

- 粮油统计表多为长年序列，OCR 残文对读者可读性破坏很大，未核录前应撤出主阅读版。
- 同段正文尾巴需要显式保护，避免将章节叙述一并移除。

## 下一步计划

- 复跑结构审计和交付门禁。
- 根据新门禁继续处理第二十九卷口岸、第四十卷金融、第四十三卷民政信访等高发卷。
""", encoding="utf-8")


def update_memory(removed: list[dict[str, str]], before: dict[str, int], after: dict[str, int]) -> None:
    entry = f"""
## 2026-06-29 第二批第三十六卷粮油购销表格残文撤出

- 新增脚本：`scripts/remove_volume36_grain_table_residue.py`。
- 从第三十六卷粮油购销主阅读版撤出表格 OCR 残文 {len(removed)} 段，并保留可识别正文尾段。
- 第三十六卷正文长数字串：{before['long_numeric_runs']} -> {after['long_numeric_runs']}；表36-*裸表题/串行表题：{before['table36_serial_titles']} -> {after['table36_serial_titles']}。
- 证据报告：`output/reports/volume36_grain_table_residue_removed.md`。
- 经验：长年序列统计表未核录前不得留在主阅读版；撤残文时必须保护合同定购、销售、储量、加工等正文尾段。
- 下一步：按新门禁继续处理第二十九卷、第四十卷、第四十三卷等表格残文高发卷。
"""
    memory = MEMORY_PATH.read_text(encoding="utf-8") if MEMORY_PATH.exists() else ""
    marker = "## 2026-06-29 第二批第三十六卷粮油购销表格残文撤出"
    if marker not in memory:
        MEMORY_PATH.write_text(memory.rstrip() + "\n\n" + entry.lstrip(), encoding="utf-8")


def main() -> None:
    text = HTML_PATH.read_text(encoding="utf-8")
    match = SECTION_RE.search(text)
    if not match:
        raise RuntimeError("Cannot locate 第三十六卷 section")
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
    print("volume 36 grain table residue removed")
    print(f"removed={len(removed)}")
    print(f"before={before}")
    print(f"after={after}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()
