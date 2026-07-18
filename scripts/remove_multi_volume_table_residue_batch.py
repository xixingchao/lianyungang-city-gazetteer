# -*- coding: utf-8 -*-
"""Remove table OCR residue from several high-priority volumes."""

from __future__ import annotations

import json
import re
from collections import Counter
from datetime import datetime
from html import unescape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_MD = ROOT / "output" / "reports" / "multi_volume_table_residue_batch_removed.md"
REPORT_JSON = ROOT / "output" / "reports" / "multi_volume_table_residue_batch_removed.json"
PROGRESS_PATH = ROOT / "output" / "reports" / "progress" / "20260629_第二批_多卷表格残文撤出.md"
MEMORY_PATH = ROOT / "PROJECT_MEMORY.md"

P_RE = re.compile(r"<p>(.*?)</p>", re.S)
TABLE_RE = re.compile(r'<table class="structured-table".*?</table>', re.S)
LONG_NUM_RE = re.compile(r"[0-9][0-9.]{25,}")

TARGETS = [
    {
        "key": "volume29",
        "title": "第二十九卷口岸",
        "start": "第二十九卷",
        "end": "第三十卷",
        "table_re": re.compile(r"表\s*29\s*[-－— ]*\s*\d+|表29-\d+"),
        "tails": ["六、外轮航修站", "“二五”计划期间", "1980年后", "1985年的货物流向"],
    },
    {
        "key": "volume40",
        "title": "第四十卷金融",
        "start": "第四十卷",
        "end": "第四十一卷",
        "table_re": re.compile(r"表\s*40\s*[-－— ]*\s*\d+|表40-\d+|表40\d+"),
        "tails": ["二、城镇储蓄", "城市信用社存款", "解放前夕", "1949~1990年连云港市各类存款余额统计表"],
    },
    {
        "key": "volume43",
        "title": "第四十三卷民政 信访",
        "start": "第四十三卷",
        "end": "第四十四卷",
        "table_re": re.compile(r"表\s*43\s*[-－— ]*\s*\d+|表43-\d+"),
        "tails": ["缩编后设区", "注：籁榆县情况特殊", "港口系属", "1953年3月9日", "1984年3月28日"],
    },
    {
        "key": "volume46",
        "title": "第四十六卷人事",
        "start": "第四十六卷",
        "end": "第四十七卷",
        "table_re": re.compile(r"表\s*46\s*[-－— ]*\s*\d+|表46-\d+"),
        "tails": ["注：1987年度", "1960~1965年", "二、易地调动", "民国38年"],
    },
]


def strip_tags(value: str) -> str:
    value = re.sub(r"<[^>]+>", " ", value)
    return re.sub(r"\s+", " ", unescape(value)).strip()


def section_re(start: str, end: str) -> re.Pattern[str]:
    return re.compile(r'(<h2 id="' + re.escape(start) + r'-[^"]+">.*?</h2>)(.*?)(?=<h2 id="' + re.escape(end) + r'-[^"]+">)', re.S)


def audit(section: str, table_re: re.Pattern[str]) -> dict[str, int]:
    plain = strip_tags(TABLE_RE.sub(" ", section))
    return {
        "structured_tables": section.count('<table class="structured-table"'),
        "long_numeric_runs": len(LONG_NUM_RE.findall(plain)),
        "serial_titles": len(table_re.findall(plain)),
    }


def split_tail(plain: str, tails: list[str]) -> tuple[str, str | None]:
    hits = [(plain.find(marker), marker) for marker in tails if plain.find(marker) > 0]
    if not hits:
        return plain, None
    pos, _ = min(hits)
    return plain[:pos].strip(), plain[pos:].strip()


def remove_for_target(section: str, target: dict[str, object]) -> tuple[str, list[dict[str, str]]]:
    table_re = target["table_re"]
    tails = target["tails"]
    assert isinstance(table_re, re.Pattern)
    assert isinstance(tails, list)
    removed: list[dict[str, str]] = []

    def repl(match: re.Match[str]) -> str:
        plain = strip_tags(match.group(1))
        reason = None
        if table_re.search(plain):
            reason = "裸表题/表格OCR残文"
        elif LONG_NUM_RE.search(plain):
            reason = "表格数字被OCR串行为正文"
        if not reason:
            return match.group(0)
        removed_text, tail = split_tail(plain, tails)
        removed.append({
            "volume": str(target["title"]),
            "reason": reason,
            "removed_excerpt": removed_text[:1000],
            "preserved_tail": tail or "",
        })
        if tail:
            return f"<p>{tail}</p>"
        return ""

    return P_RE.sub(repl, section), removed


def write_reports(results: list[dict[str, object]], removed: list[dict[str, str]]) -> None:
    payload = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "scope": [r["title"] for r in results],
        "results": results,
        "removed": removed,
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    stat_rows = []
    for r in results:
        before = r["before"]
        after = r["after"]
        assert isinstance(before, dict) and isinstance(after, dict)
        stat_rows.append(
            f"| {r['title']} | {before['long_numeric_runs']} | {after['long_numeric_runs']} | {before['serial_titles']} | {after['serial_titles']} | {r['removed_count']} |"
        )
    rows = []
    for idx, item in enumerate(removed, 1):
        excerpt = item["removed_excerpt"].replace("|", "｜")
        tail = (item["preserved_tail"] or "-").replace("|", "｜")
        rows.append(f"| {idx} | {item['volume']} | {item['reason']} | {excerpt} | {tail} |")
    REPORT_MD.write_text(f"""# 多卷表格残文撤出报告

生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}

## 原则

本批处理第二十九卷口岸、第四十卷金融、第四十三卷民政信访、第四十六卷人事中读者可见的表格 OCR 残文。未核表格不进入主阅读版；与正文粘连的段落保留可识别正文尾段。

## 统计

| 章节 | 长数字串前 | 长数字串后 | 串行表题前 | 串行表题后 | 撤出段落 |
| --- | ---: | ---: | ---: | ---: | ---: |
{chr(10).join(stat_rows)}

## 撤出清单

| 序号 | 章节 | 原因 | 撤出摘录 | 保留正文尾段 |
| ---: | --- | --- | --- | --- |
{chr(10).join(rows) or '| - | - | - | - | - |'}
""", encoding="utf-8")


def write_progress(results: list[dict[str, object]], removed: list[dict[str, str]]) -> None:
    counts = Counter(item["volume"] for item in removed)
    summary = "；".join(f"{k} {v}" for k, v in counts.items())
    PROGRESS_PATH.write_text(f"""# 第二批：多卷表格残文撤出

更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}

## 已完成

- 从第二十九卷口岸、第四十卷金融、第四十三卷民政信访、第四十六卷人事撤出表格 OCR 残文 {len(removed)} 段。
- 分卷数量：{summary}。
- 证据报告：`output/reports/multi_volume_table_residue_batch_removed.md`。

## 验收摘要

| 章节 | 长数字串前 | 长数字串后 | 串行表题前 | 串行表题后 |
| --- | ---: | ---: | ---: | ---: |
""" + "\n".join(
        f"| {r['title']} | {r['before']['long_numeric_runs']} | {r['after']['long_numeric_runs']} | {r['before']['serial_titles']} | {r['after']['serial_titles']} |"  # type: ignore[index]
        for r in results
    ) + """

## 经验

- 同类高发卷可以参数化处理，但仍必须分卷记录撤出证据和保留正文尾段。
- 对未核统计表采取撤出登记，不把 OCR 串行数字作为正文交付。

## 下一步计划

- 复跑结构审计和交付门禁。
- 继续按新门禁处理第二十卷化学工业、第八卷经济综合管理、第四十一卷政党、第五十卷教育等残留高发卷。
""", encoding="utf-8")


def update_memory(results: list[dict[str, object]], removed: list[dict[str, str]]) -> None:
    lines = []
    for r in results:
        before = r["before"]; after = r["after"]
        lines.append(f"  - {r['title']}：长数字串 {before['long_numeric_runs']} -> {after['long_numeric_runs']}；串行表题 {before['serial_titles']} -> {after['serial_titles']}；撤出 {r['removed_count']} 段。")  # type: ignore[index]
    entry = f"""
## 2026-06-29 第二批多卷表格残文撤出

- 新增脚本：`scripts/remove_multi_volume_table_residue_batch.py`。
- 批量处理第二十九卷口岸、第四十卷金融、第四十三卷民政信访、第四十六卷人事，撤出表格 OCR 残文 {len(removed)} 段。
{chr(10).join(lines)}
- 证据报告：`output/reports/multi_volume_table_residue_batch_removed.md`。
- 经验：同类表格残文可以参数化处理，但主阅读版只保留可读正文，未核统计表统一登记待回源核录。
- 下一步：复跑门禁后继续处理剩余高发卷，直至读者可见残文清零。
"""
    memory = MEMORY_PATH.read_text(encoding="utf-8") if MEMORY_PATH.exists() else ""
    marker = "## 2026-06-29 第二批多卷表格残文撤出"
    if marker not in memory:
        MEMORY_PATH.write_text(memory.rstrip() + "\n\n" + entry.lstrip(), encoding="utf-8")


def main() -> None:
    text = HTML_PATH.read_text(encoding="utf-8")
    results: list[dict[str, object]] = []
    all_removed: list[dict[str, str]] = []
    for target in TARGETS:
        regex = section_re(str(target["start"]), str(target["end"]))
        match = regex.search(text)
        if not match:
            raise RuntimeError(f"Cannot locate {target['title']}")
        heading, section = match.groups()
        table_re = target["table_re"]
        assert isinstance(table_re, re.Pattern)
        before = audit(section, table_re)
        new_section, removed = remove_for_target(section, target)
        text = text[:match.start()] + heading + new_section + text[match.end():]
        after = audit(new_section, table_re)
        results.append({"title": target["title"], "before": before, "after": after, "removed_count": len(removed)})
        all_removed.extend(removed)
    HTML_PATH.write_text(text, encoding="utf-8")
    write_reports(results, all_removed)
    write_progress(results, all_removed)
    update_memory(results, all_removed)
    print("multi-volume table residue removed")
    print(f"removed={len(all_removed)}")
    for r in results:
        print(f"{r['title']}: before={r['before']} after={r['after']} removed={r['removed_count']}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()
