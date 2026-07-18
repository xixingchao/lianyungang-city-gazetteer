# -*- coding: utf-8 -*-
"""Remove reader-facing serial OCR table residue from volume 44.

This batch does not attempt to reconstruct tables from OCR. It removes paragraphs
that are clearly table residue from the main reader and records evidence for
later source-image table reconstruction.
"""

from __future__ import annotations

import json
import re
from datetime import datetime
from html import unescape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_MD = ROOT / "output" / "reports" / "volume44_serial_table_residue_removed.md"
REPORT_JSON = ROOT / "output" / "reports" / "volume44_serial_table_residue_removed.json"
PROGRESS_PATH = ROOT / "output" / "reports" / "progress" / "20260629_第二批_第四十四卷表格残文撤出主阅读版.md"
MEMORY_PATH = ROOT / "PROJECT_MEMORY.md"

SECTION_RE = re.compile(r'(<h2 id="第四十四卷-治安司法">.*?</h2>)(.*?)(?=<h2 id="第四十五卷-军事">)', re.S)
P_RE = re.compile(r"<p>(.*?)</p>", re.S)
TABLE_RE = re.compile(r'<table class="structured-table".*?</table>', re.S)
TABLE_TITLE_RE = re.compile(r"表\s*44\s*[-－— ]*\s*\d+|表44\s*[-－— ]*\s*\d+|表\s*44\s+\d+")
LONG_NUM_RE = re.compile(r"[0-9][0-9.]{25,}")
SERIAL_HINT_RE = re.compile(r"续上表|单位[:：]|年份|受案|结案|审结|判决发生法律效力|已经发生法律效力")

# Narrative headings/subheads that were glued after OCR table residue in the same paragraph.
TAIL_MARKERS = [
    "九、交通管理",
    "十、消防机构",
    "十、消机构",
    "三、出庭公诉",
    "抢劫案件",
    "强奸案件",
    "盗窃案件",
    "流氓案件",
    "拐卖人口案件",
    "诈骗案件",
    "投机倒把案件",
    "四、减刑、假释、特赦",
    "二、财产权益案件",
    "房屋",
    "三、民事案件的执行",
]


def strip_tags(value: str) -> str:
    value = re.sub(r"<[^>]+>", " ", value)
    return re.sub(r"\s+", " ", unescape(value)).strip()


def audit(section: str) -> dict[str, int]:
    plain_without_tables = strip_tags(TABLE_RE.sub(" ", section))
    return {
        "structured_tables": section.count('<table class="structured-table"'),
        "long_numeric_runs": len(LONG_NUM_RE.findall(plain_without_tables)),
        "suspect_serial_tables": len(TABLE_TITLE_RE.findall(plain_without_tables)),
        "empty_markers": section.count("待对照原图录入"),
    }


def looks_like_table_residue(plain: str) -> bool:
    if TABLE_TITLE_RE.search(plain):
        return True
    if plain.startswith("续上表"):
        return True
    if LONG_NUM_RE.search(plain) and SERIAL_HINT_RE.search(plain):
        return True
    # Continuation rows often start with dense bare numbers after the table title
    # was split into a previous paragraph.
    if LONG_NUM_RE.search(plain) and len(re.findall(r"\d", plain)) >= 45 and len(plain) < 900:
        return True
    return False


def split_tail(plain: str) -> tuple[str, str | None]:
    positions = [(plain.find(marker), marker) for marker in TAIL_MARKERS if plain.find(marker) > 0]
    if not positions:
        return plain, None
    pos, marker = min(positions)
    removed = plain[:pos].strip()
    tail = plain[pos:].strip()
    # Repair one known OCR omission in a subhead when preserving narrative text.
    if marker == "十、消机构":
        tail = tail.replace("十、消机构", "十、消防机构", 1)
    return removed, tail


def remove_residue(section: str) -> tuple[str, list[dict[str, str]]]:
    removed: list[dict[str, str]] = []

    def repl(match: re.Match[str]) -> str:
        inner = match.group(1)
        plain = strip_tags(inner)
        if not looks_like_table_residue(plain):
            return match.group(0)
        removed_text, tail = split_tail(plain)
        removed.append({
            "reason": "第四十四卷表格被 OCR 串行为正文，未达到主阅读版交付标准",
            "removed_excerpt": removed_text[:900],
            "preserved_tail": tail or "",
        })
        if tail:
            return f"<p>{tail}</p>"
        return ""

    return P_RE.sub(repl, section), removed


def write_reports(removed: list[dict[str, str]], before: dict[str, int], after: dict[str, int]) -> None:
    payload = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "scope": "第四十四卷 治安司法",
        "principle": "撤出未核表格 OCR 残文；不以 OCR 串行文本伪装正式表格。",
        "before": before,
        "after": after,
        "removed": removed,
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    rows = []
    for idx, item in enumerate(removed, 1):
        excerpt = item["removed_excerpt"].replace("|", "｜")
        tail = (item["preserved_tail"] or "-").replace("|", "｜")
        rows.append(f"| {idx} | {excerpt} | {tail} |")
    rows_text = "\n".join(rows) or "| - | - | - |"
    REPORT_MD.write_text(f"""# 第四十四卷表格残文撤出主阅读版报告

生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}

## 原则

按东辛农场志交付口径，主阅读版不得显示未核表格残文。本批只处理第四十四卷内可明确识别的表44-*串行 OCR 表格段；能识别同段后续正文的，保留正文尾段；不能确认表格数据的，不重构、不补录、不伪装为成品表。

## 统计

| 指标 | 撤出前 | 撤出后 |
| --- | ---: | ---: |
| 第四十四卷结构化表格 | {before['structured_tables']} | {after['structured_tables']} |
| 正文长数字串 | {before['long_numeric_runs']} | {after['long_numeric_runs']} |
| 疑似表44串行表题 | {before['suspect_serial_tables']} | {after['suspect_serial_tables']} |
| `待对照原图录入` | {before['empty_markers']} | {after['empty_markers']} |
| 撤出段落 | {len(removed)} | - |

## 撤出清单

| 序号 | 撤出摘录 | 保留正文尾段 |
| ---: | --- | --- |
{rows_text}

## 后续

这些表格需要回源页图/PDF 核录后，才能作为正式结构化表嵌回正文；本报告即为待核表线索清单的一部分。
""", encoding="utf-8")


def write_progress(removed: list[dict[str, str]], before: dict[str, int], after: dict[str, int]) -> None:
    PROGRESS_PATH.write_text(f"""# 第二批：第四十四卷表格残文撤出主阅读版

更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}

## 已完成

- 按东辛交付标准，从第四十四卷主阅读版撤出串行 OCR 表格残文 {len(removed)} 段。
- 对表格残文与正文粘连的段落，保留了可识别的正文尾段，例如交通管理、出庭公诉、抢劫案件、强奸案件、盗窃案件、民事案件执行等小节起文。
- 证据报告：`output/reports/volume44_serial_table_residue_removed.md`。

## 验收数据

| 指标 | 撤出前 | 撤出后 |
| --- | ---: | ---: |
| 第四十四卷结构化表格 | {before['structured_tables']} | {after['structured_tables']} |
| 正文长数字串 | {before['long_numeric_runs']} | {after['long_numeric_runs']} |
| 疑似表44串行表题 | {before['suspect_serial_tables']} | {after['suspect_serial_tables']} |
| `待对照原图录入` | {before['empty_markers']} | {after['empty_markers']} |

## 经验

- 下册 JSON/HTML 中的 `verified` 不能直接视为已核；第四十四卷此前空壳表与正文残文并存，主阅读版应先撤出未核内容，再回源核录。
- 表格 OCR 常与下一小节正文粘在同一个段落，处理时必须先识别正文尾段，否则会把可读正文一并删除。

## 下一步计划

- 复跑 `scripts/audit_delivery_quality.py` 和 `scripts/audit_full_reader.py`。
- 下一批按门禁排序处理第五十卷教育或第四十六卷人事中的 `待对照原图录入`/空表问题；第四十四卷撤出的表格后续按源页 p2032-p2123 单独核录。
""", encoding="utf-8")


def update_memory(removed: list[dict[str, str]], before: dict[str, int], after: dict[str, int]) -> None:
    entry = f"""
## 2026-06-29 第二批第四十四卷表格残文撤出

- 新增脚本：`scripts/remove_volume44_serial_table_residue.py`。
- 从第四十四卷治安司法主阅读版撤出串行 OCR 表格残文 {len(removed)} 段，不把 OCR 串行文本伪装为正式结构化表。
- 对表格残文与正文粘连的段落，保留可识别正文尾段；其中包括交通管理、出庭公诉、抢劫案件、强奸案件、盗窃案件、民事案件执行等。
- 第四十四卷正文长数字串：{before['long_numeric_runs']} -> {after['long_numeric_runs']}；疑似表44串行表题：{before['suspect_serial_tables']} -> {after['suspect_serial_tables']}。
- 证据报告：`output/reports/volume44_serial_table_residue_removed.md`。
- 经验：下册表格必须以源图/PDF 为最终依据，`verified` 或占位清零都不能替代交付验收；表格残文撤出时必须保护同段正文尾巴。
- 下一步：复跑交付门禁后，转入第五十卷教育/第四十六卷人事等空表和待核说明高发卷；第四十四卷撤出表格另列回源核录任务。
"""
    memory = MEMORY_PATH.read_text(encoding="utf-8") if MEMORY_PATH.exists() else ""
    marker = "## 2026-06-29 第二批第四十四卷表格残文撤出"
    if marker not in memory:
        MEMORY_PATH.write_text(memory.rstrip() + "\n\n" + entry.lstrip(), encoding="utf-8")


def main() -> None:
    text = HTML_PATH.read_text(encoding="utf-8")
    match = SECTION_RE.search(text)
    if not match:
        raise RuntimeError("Cannot locate 第四十四卷 section")
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
    print("volume 44 serial table residue removed")
    print(f"removed={len(removed)}")
    print(f"before={before}")
    print(f"after={after}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()
