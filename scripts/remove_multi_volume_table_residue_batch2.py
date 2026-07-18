# -*- coding: utf-8 -*-
"""Remove table OCR residue from the next high-priority volume batch."""

from __future__ import annotations

import json
import re
from collections import Counter
from datetime import datetime
from html import unescape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_MD = ROOT / "output" / "reports" / "multi_volume_table_residue_batch2_removed.md"
REPORT_JSON = ROOT / "output" / "reports" / "multi_volume_table_residue_batch2_removed.json"
PROGRESS_PATH = ROOT / "output" / "reports" / "progress" / "20260629_第二批_多卷表格残文撤出_batch2.md"
MEMORY_PATH = ROOT / "PROJECT_MEMORY.md"

P_RE = re.compile(r"<p>(.*?)</p>", re.S)
TABLE_RE = re.compile(r'<table class="structured-table".*?</table>', re.S)
LONG_NUM_RE = re.compile(r"[0-9][0-9.]{25,}")
BAD_NOTE_RE = re.compile(r"源\s*OCR|待对照原图|待校正|待补录|补录|核对型")

TARGETS = [
    {
        "title": "第二十卷化学工业",
        "start": "第二十卷",
        "end": "第二十一卷",
        "table_re": re.compile(r"表\s*20\s*[-－— ]*\s*\d+|表20-\d+"),
        "tails": ["二、碱", "三、无机盐", "硅酸钠1958年", "1990年，全市年生产能力"],
    },
    {
        "title": "第八卷经济综合管理",
        "start": "第八卷",
        "end": "第九卷",
        "table_re": re.compile(r"表\s*8\s*[-－— ]*\s*\d+|表8-\d+"),
        "tails": ["七、自然科学技术人员普查", "十二、农村住户调查"],
    },
    {
        "title": "第四十一卷政党",
        "start": "第四十一卷",
        "end": "第四十二卷",
        "table_re": re.compile(r"表\s*41\s*[-－— ]*\s*\d+|表41-\d+"),
        "tails": [],
    },
    {
        "title": "第五十卷教育",
        "start": "第五十卷",
        "end": "第五十一卷",
        "table_re": re.compile(r"表\s*50\s*[-－— ]*\s*\d+|表50-\d+|表507"),
        "tails": ["加强对“防近”工作的宣传", "贸易、金融财会"],
    },
    {
        "title": "第十三卷盐业",
        "start": "第十三卷",
        "end": "第十四卷",
        "table_re": re.compile(r"表\s*13\s*[-－— ]*\s*\d+|表13-\d+"),
        "tails": ["三、设施", "盐田海盐生产的基本设施是盐田"],
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
        "bad_notes": len(BAD_NOTE_RE.findall(plain)),
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
        if BAD_NOTE_RE.search(plain):
            reason = "读者可见源OCR/待补录等处理说明"
        elif table_re.search(plain):
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
        before = r["before"]; after = r["after"]
        assert isinstance(before, dict) and isinstance(after, dict)
        stat_rows.append(
            f"| {r['title']} | {before['long_numeric_runs']} | {after['long_numeric_runs']} | {before['serial_titles']} | {after['serial_titles']} | {before['bad_notes']} | {after['bad_notes']} | {r['removed_count']} |"
        )
    rows = []
    for idx, item in enumerate(removed, 1):
        excerpt = item["removed_excerpt"].replace("|", "｜")
        tail = (item["preserved_tail"] or "-").replace("|", "｜")
        rows.append(f"| {idx} | {item['volume']} | {item['reason']} | {excerpt} | {tail} |")
    REPORT_MD.write_text(f"""# 多卷表格残文撤出报告 batch2

生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}

## 原则

本批处理第二十卷化学工业、第八卷经济综合管理、第四十一卷政党、第五十卷教育、第十三卷盐业中的读者可见表格 OCR 残文和处理说明。未核表格不进入主阅读版；与正文粘连的段落保留可识别正文尾段。

## 统计

| 章节 | 长数字串前 | 长数字串后 | 串行表题前 | 串行表题后 | 说明标记前 | 说明标记后 | 撤出段落 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
{chr(10).join(stat_rows)}

## 撤出清单

| 序号 | 章节 | 原因 | 撤出摘录 | 保留正文尾段 |
| ---: | --- | --- | --- | --- |
{chr(10).join(rows) or '| - | - | - | - | - |'}
""", encoding="utf-8")


def write_progress(results: list[dict[str, object]], removed: list[dict[str, str]]) -> None:
    counts = Counter(item["volume"] for item in removed)
    summary = "；".join(f"{k} {v}" for k, v in counts.items())
    stat_rows = "\n".join(
        f"| {r['title']} | {r['before']['long_numeric_runs']} | {r['after']['long_numeric_runs']} | {r['before']['serial_titles']} | {r['after']['serial_titles']} | {r['before']['bad_notes']} | {r['after']['bad_notes']} |"  # type: ignore[index]
        for r in results
    )
    PROGRESS_PATH.write_text(f"""# 第二批：多卷表格残文撤出 batch2

更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}

## 已完成

- 从第二十卷化学工业、第八卷经济综合管理、第四十一卷政党、第五十卷教育、第十三卷盐业撤出表格 OCR 残文/处理说明 {len(removed)} 段。
- 分卷数量：{summary}。
- 证据报告：`output/reports/multi_volume_table_residue_batch2_removed.md`。

## 验收摘要

| 章节 | 长数字串前 | 长数字串后 | 串行表题前 | 串行表题后 | 说明标记前 | 说明标记后 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
{stat_rows}

## 经验

- 表格残文和工作台说明经常分散在相邻段落，必须同时清理，否则门禁仍会提示读者可见处理痕迹。
- 参数化处理只能处理“明确残文”；后续仍需按门禁样例做抽查和补刀。

## 下一步计划

- 复跑结构审计和交付门禁。
- 继续处理第四卷人口、第二十七卷乡镇企业、第三十三卷商业等残留高发卷，并清理第十卷水利可见处理说明。
""", encoding="utf-8")


def update_memory(results: list[dict[str, object]], removed: list[dict[str, str]]) -> None:
    lines = []
    for r in results:
        before = r["before"]; after = r["after"]
        lines.append(f"  - {r['title']}：长数字串 {before['long_numeric_runs']} -> {after['long_numeric_runs']}；串行表题 {before['serial_titles']} -> {after['serial_titles']}；说明标记 {before['bad_notes']} -> {after['bad_notes']}；撤出 {r['removed_count']} 段。")  # type: ignore[index]
    entry = f"""
## 2026-06-29 第二批多卷表格残文撤出 batch2

- 新增脚本：`scripts/remove_multi_volume_table_residue_batch2.py`。
- 批量处理第二十卷化学工业、第八卷经济综合管理、第四十一卷政党、第五十卷教育、第十三卷盐业，撤出表格 OCR 残文/处理说明 {len(removed)} 段。
{chr(10).join(lines)}
- 证据报告：`output/reports/multi_volume_table_residue_batch2_removed.md`。
- 经验：读者可见 `源 OCR`、`待补录` 说明与表格残文同属非交付内容，必须一起撤出并登记待回源核录。
- 下一步：复跑门禁后继续处理第四卷人口、第二十七卷、第三十三卷等残留高发卷。
"""
    memory = MEMORY_PATH.read_text(encoding="utf-8") if MEMORY_PATH.exists() else ""
    marker = "## 2026-06-29 第二批多卷表格残文撤出 batch2"
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
    print("multi-volume table residue batch2 removed")
    print(f"removed={len(all_removed)}")
    for r in results:
        print(f"{r['title']}: before={r['before']} after={r['after']} removed={r['removed_count']}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()
