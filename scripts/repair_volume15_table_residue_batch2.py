# -*- coding: utf-8 -*-
"""Repair volume 15 table residue using verified table data where safe."""

from __future__ import annotations

import html
import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
DATA_DIR = ROOT / "workbench" / "table_entries" / "上" / "data"
REPORT_MD = ROOT / "output" / "reports" / "volume15_table_residue_batch2.md"
REPORT_JSON = ROOT / "output" / "reports" / "volume15_table_residue_batch2.json"
PROGRESS_PATH = ROOT / "output" / "reports" / "progress" / "20260629_第二批_第十五卷表格残文收敛.md"
MEMORY_PATH = ROOT / "PROJECT_MEMORY.md"
SECTION_RE = re.compile(r'(<h2 id="第十五卷-纺织工业">.*?</h2>)(.*?)(?=<h2 id="第十六卷-皮塑工业">)', re.S)
TABLE_RE = re.compile(r'<table class="structured-table".*?</table>', re.S)


def strip_tags(value: str) -> str:
    value = re.sub(r"<[^>]+>", "", value)
    return re.sub(r"\s+", " ", value).strip()


def make_table(table_id: str, caption_override: str | None = None) -> str:
    data = json.loads((DATA_DIR / f"{table_id}.json").read_text(encoding="utf-8"))
    caption = caption_override or f"{data.get('table_number', '').strip()} {data.get('title', '').strip()}".strip()
    headers = data.get("columns", [])
    rows = data.get("rows", [])
    ths = "".join(f"<th>{html.escape(str(h))}</th>" for h in headers)
    trs = []
    for row in rows:
        trs.append("<tr>" + "".join(f"<td>{html.escape(str(cell))}</td>" for cell in row) + "</tr>")
    return f'<table class="structured-table"><caption>{html.escape(caption)}</caption><thead><tr>{ths}</tr></thead><tbody>{"".join(trs)}</tbody></table>'


def audit(section: str) -> dict[str, int]:
    plain = strip_tags(section)
    return {
        "structured_tables": section.count('<table class="structured-table"'),
        "captioned_tables": section.count("<caption>"),
        "long_numeric_runs": len(re.findall(r"[0-9][0-9.]{25,}", plain)),
        "blank_cell_rows": len(re.findall(r"<tr>(?:<td>[^<]*</td>){1,2}(?:<td></td>){4,}</tr>", section)),
        "workbench_markers": sum(plain.count(x) for x in ["源 OCR", "待对照原图", "待原图", "待校正", "待补录", "待核对", "备注"]),
    }


def remove_first_table_after(section: str, marker: str) -> tuple[str, str]:
    start = section.find(marker)
    if start == -1:
        return section, ""
    match = TABLE_RE.search(section, start)
    if not match:
        return section, ""
    removed = match.group(0)
    return section[: match.start()] + section[match.end():], removed


def replace_first_table_after(section: str, marker: str, replacement: str) -> tuple[str, str]:
    start = section.find(marker)
    if start == -1:
        return section, ""
    match = TABLE_RE.search(section, start)
    if not match:
        return section, ""
    removed = match.group(0)
    return section[: match.start()] + replacement + section[match.end():], removed


def remove_paras_between(section: str, start_marker: str, end_marker: str) -> tuple[str, list[str]]:
    start = section.find(start_marker)
    end = section.find(end_marker, start if start != -1 else 0)
    if start == -1 or end == -1 or end <= start:
        return section, []
    block = section[start:end]
    paras = re.findall(r"<p>.*?</p>", block, re.S)
    if not paras:
        return section, []
    new_block = TABLE_RE.sub("", block)
    for para in paras:
        new_block = new_block.replace(para, "")
    return section[:start] + new_block + section[end:], [strip_tags(p)[:260] for p in paras]


def repair(section: str) -> tuple[str, list[dict[str, str]]]:
    actions: list[dict[str, str]] = []

    section, removed_paras = remove_paras_between(
        section,
        "1970～1990年连云港市化纤业生产经营情况统计表表15-1",
        '<table class="structured-table"',
    )
    for item in removed_paras:
        actions.append({"action": "撤出表15-1串行OCR段落", "detail": item})
    section, removed_table = replace_first_table_after(
        section,
        "1970～1990年连云港市化纤业生产经营情况统计表表15-1",
        make_table("LYG-上-T041", "表15-1 1970～1990年连云港市化纤业生产经营情况统计表"),
    )
    if removed_table:
        actions.append({"action": "恢复表15-1为带caption正式表", "detail": strip_tags(removed_table)[:260]})

    section, removed_paras = remove_paras_between(
        section,
        "1949～1990年部分年份连云港市棉纺织、印染业主要产品产量统计表表15-2",
        '<table class="structured-table"',
    )
    for item in removed_paras:
        actions.append({"action": "撤出表15-2串行OCR表头段落", "detail": item})
    section, removed_table = replace_first_table_after(
        section,
        "1949～1990年部分年份连云港市棉纺织、印染业主要产品产量统计表表15-2",
        make_table("LYG-上-T042", "表15-2 1949～1990年部分年份连云港市棉纺织、印染业主要产品产量统计表"),
    )
    if removed_table:
        actions.append({"action": "恢复表15-2为带caption正式表", "detail": strip_tags(removed_table)[:260]})
    section, duplicate = remove_first_table_after(section, "表15-2 1949～1990年部分年份连云港市棉纺织、印染业主要产品产量统计表")
    if duplicate:
        actions.append({"action": "撤出表15-2重复无caption表", "detail": strip_tags(duplicate)[:260]})
    section, removed_paras = remove_paras_between(
        section,
        "续上表产棉布棉纱品帆布色织布印染布",
        '<h4 id="第十五卷-第二章棉纺织印染-第四节主要企业简介">',
    )
    for item in removed_paras:
        actions.append({"action": "撤出表15-2续表串行表头", "detail": item})

    section, removed_paras = remove_paras_between(
        section,
        "1959～1990年部分年份连云港市麻纺织业生产经营情况统计表表15-5",
        "<h4 id=\"第十五卷-第四章麻毛丝织-第二节毛纺织\"",
    )
    for item in removed_paras:
        actions.append({"action": "撤出表15-5串行OCR段落", "detail": item})

    section, removed_paras = remove_paras_between(
        section,
        "1981～1990年连云港市毛纺丝织业主要产品产量统计表表15-6",
        "<h4 id=\"第十五卷-第四章麻毛丝织-第四节主要企业简介\"",
    )
    for item in removed_paras:
        actions.append({"action": "撤出表15-6串行OCR段落", "detail": item})

    section, removed_paras = remove_paras_between(
        section,
        "1975～1990年连云港市纺织企业工业总产值统计表表15-9",
        "连云港市纺织工业获奖产品一览表表15-11",
    )
    for item in removed_paras:
        actions.append({"action": "撤出表15-9/15-10串行OCR段落", "detail": item})
    for _ in range(8):
        section, table = remove_first_table_after(section, "1975～1990年连云港市纺织企业工业总产值统计表表15-9")
        if not table:
            break
        actions.append({"action": "撤出表15-10空壳/重复结构化表", "detail": strip_tags(table)[:260]})

    return section, actions


def write_reports(actions: list[dict[str, str]], before: dict[str, int], after: dict[str, int]) -> None:
    payload = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "scope": "第十五卷 纺织工业 第二批表格残文收敛",
        "before": before,
        "after": after,
        "actions": actions,
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    rows = "\n".join(
        f"| {idx} | {item['action']} | {item['detail']} |" for idx, item in enumerate(actions, 1)
    ) or "| - | - | - |"
    REPORT_MD.write_text(f"""# 第十五卷表格残文收敛报告（二）

生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}

## 处理原则

- 表15-1、表15-2已有表格站行列数据，本轮恢复为带 caption 的正式结构化表。
- 表15-5、表15-6、表15-9、表15-10相关残文/空壳表未达到主阅读版交付标准，本轮撤出主阅读版，保留报告证据，待源 PDF 核录后重建。

## 统计

| 指标 | 处理前 | 处理后 |
| --- | ---: | ---: |
| 第十五卷结构化表格 | {before['structured_tables']} | {after['structured_tables']} |
| 带 caption 表格 | {before['captioned_tables']} | {after['captioned_tables']} |
| 长数字串 | {before['long_numeric_runs']} | {after['long_numeric_runs']} |
| 空白占主的表格行 | {before['blank_cell_rows']} | {after['blank_cell_rows']} |
| 工作台字段命中 | {before['workbench_markers']} | {after['workbench_markers']} |

## 动作清单

| 序号 | 动作 | 摘录 |
| ---: | --- | --- |
{rows}
""", encoding="utf-8")


def write_progress(actions: list[dict[str, str]], before: dict[str, int], after: dict[str, int]) -> None:
    action_lines = "\n".join(f"- {item['action']}" for item in actions) or "- 本次复跑未产生新改动。"
    PROGRESS_PATH.write_text(f"""# 第二批：第十五卷表格残文收敛

更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}

## 已完成
{action_lines}

## 验收数据

| 指标 | 处理前 | 处理后 |
| --- | ---: | ---: |
| 第十五卷结构化表格 | {before['structured_tables']} | {after['structured_tables']} |
| 带 caption 表格 | {before['captioned_tables']} | {after['captioned_tables']} |
| 长数字串 | {before['long_numeric_runs']} | {after['long_numeric_runs']} |
| 空白占主的表格行 | {before['blank_cell_rows']} | {after['blank_cell_rows']} |
| 工作台字段命中 | {before['workbench_markers']} | {after['workbench_markers']} |

## 下一步计划

- 复跑交付门禁和结构审计。
- 第十五卷剩余疑点转入表15-11获奖产品表核查；若仍有长串残留，继续撤出或重建。
""", encoding="utf-8")


def update_memory(actions: list[dict[str, str]], before: dict[str, int], after: dict[str, int]) -> None:
    entry = f"""
## 2026-06-29 第二批第十五卷表格残文收敛

- 新增脚本：`scripts/repair_volume15_table_residue_batch2.py`。
- 表15-1、表15-2使用表格站数据恢复为带 caption 的正式结构化表。
- 表15-5、表15-6、表15-9/15-10相关串行 OCR 残文和空壳/重复结构化表撤出主阅读版，证据写入 `output/reports/volume15_table_residue_batch2.md`。
- 第十五卷长数字串：{before['long_numeric_runs']} -> {after['long_numeric_runs']}；结构化表：{before['structured_tables']} -> {after['structured_tables']}；带 caption 表：{before['captioned_tables']} -> {after['captioned_tables']}。
- 进度文档：`output/reports/progress/20260629_第二批_第十五卷表格残文收敛.md`。
"""
    memory = MEMORY_PATH.read_text(encoding="utf-8") if MEMORY_PATH.exists() else ""
    marker = "## 2026-06-29 第二批第十五卷表格残文收敛"
    if marker not in memory:
        MEMORY_PATH.write_text(memory.rstrip() + "\n\n" + entry.lstrip(), encoding="utf-8")


def main() -> None:
    text = HTML_PATH.read_text(encoding="utf-8")
    match = SECTION_RE.search(text)
    if not match:
        raise RuntimeError("Cannot locate 第十五卷 section")
    heading, section = match.groups()
    before = audit(section)
    new_section, actions = repair(section)
    fixed = text[: match.start()] + heading + new_section + text[match.end():]
    if fixed != text:
        HTML_PATH.write_text(fixed, encoding="utf-8")
    after = audit(new_section)
    write_reports(actions, before, after)
    write_progress(actions, before, after)
    update_memory(actions, before, after)
    print("volume 15 table residue batch2 repaired")
    print(f"actions={len(actions)}")
    print(f"before={before}")
    print(f"after={after}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()
