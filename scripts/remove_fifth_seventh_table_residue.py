# -*- coding: utf-8 -*-
"""Move obvious table OCR residue out of volumes 5 and 7 reader sections."""

from __future__ import annotations

import json
import re
from collections import Counter
from datetime import datetime
from html import unescape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_MD = ROOT / "output" / "reports" / "volume5_7_table_residue_removed.md"
REPORT_JSON = ROOT / "output" / "reports" / "volume5_7_table_residue_removed.json"
PROGRESS_PATH = ROOT / "output" / "reports" / "progress" / "20260629_第二批_第五卷第七卷表格残文撤出.md"
MEMORY_PATH = ROOT / "PROJECT_MEMORY.md"

SECTIONS = [
    ("第五卷城乡建设", "第五卷-城乡建设", "第六卷-环境保护", re.compile(r"表5-\d+")),
    ("第七卷经济综情", "第七卷-经济综情", "第八卷-经济综合管理", re.compile(r"表7-\d+")),
]

SECTION_RE_TEMPLATE = r'(<h2 id="{start}">.*?</h2>)(.*?)(?=<h2 id="{end}">)'
P_OR_TABLE_RE = re.compile(r'(?P<node><p>.*?</p>|<table class="structured-table">.*?</table>\n?)', re.S)
LONG_NUM_RE = re.compile(r"[0-9][0-9.]{25,}")


def strip_tags(value: str) -> str:
    value = re.sub(r"<[^>]+>", "", value)
    value = unescape(value)
    value = re.sub(r"\s+", " ", value).strip()
    return value


def digit_ratio(text: str) -> float:
    if not text:
        return 0.0
    return sum(ch.isdigit() for ch in text) / max(len(text), 1)


def should_remove(text: str, html_node: str, table_re: re.Pattern[str]) -> tuple[bool, str]:
    has_table_no = bool(table_re.search(text))
    has_empty_marker = "待对照原图录入" in text
    has_long_num = bool(LONG_NUM_RE.search(text))
    is_table = html_node.startswith("<table")
    if is_table and not has_empty_marker:
        return False, ""

    if has_empty_marker:
        return True, "空壳待录入表/段落"
    if has_table_no and len(text) >= 80:
        return True, "表号 OCR 残文段"
    if has_long_num and digit_ratio(text) >= 0.35:
        return True, "高密度数字串表格残文"
    if has_long_num and has_table_no:
        return True, "带表号长数字串残文"
    if is_table and has_table_no and len(text) >= 220:
        return True, "疑似未核长表展示"
    return False, ""


def process_section(section_name: str, block: str, table_re: re.Pattern[str]) -> tuple[str, list[dict[str, str | int]]]:
    removed: list[dict[str, str | int]] = []

    def repl(match: re.Match[str]) -> str:
        node = match.group("node")
        text = strip_tags(node)
        remove, reason = should_remove(text, node, table_re)
        if not remove:
            return node
        removed.append(
            {
                "section": section_name,
                "reason": reason,
                "text": text,
                "html": node.strip(),
            }
        )
        return ""

    fixed = P_OR_TABLE_RE.sub(repl, block)
    fixed = re.sub(r"\n{3,}", "\n\n", fixed)
    return fixed, removed


def render_report(items: list[dict[str, str | int]]) -> str:
    by_section = Counter(str(item["section"]) for item in items)
    by_reason = Counter(str(item["reason"]) for item in items)
    lines = [
        "# 第五卷、第七卷表格残文撤出主阅读版记录",
        "",
        f"> 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"> 基于：`{HTML_PATH.relative_to(ROOT)}`",
        "",
        "## 处理结论",
        "",
        "- 本轮只撤出明显不符合交付阅读的表格 OCR 残文、空壳待录入表和高密度数字串。",
        "- 撤出内容完整保存到本报告和 JSON，后续需回源 PDF 核录后再作为正式结构化表嵌回正文。",
        "- 这不是删表交付，而是把未核工作台内容从读者主入口移出。",
        "",
        "## 统计",
        "",
        "| 分类 | 数量 |",
        "|---|---:|",
    ]
    for key, count in by_section.most_common():
        lines.append(f"| {key} | {count} |")
    for key, count in by_reason.most_common():
        lines.append(f"| {key} | {count} |")

    lines.extend([
        "",
        "## 明细",
        "",
        "| 序号 | 章节 | 原因 | 摘录 |",
        "|---:|---|---|---|",
    ])
    for idx, item in enumerate(items, 1):
        text = str(item["text"]).replace("|", "\\|")
        if len(text) > 160:
            text = text[:159] + "..."
        lines.append(f"| {idx} | {item['section']} | {item['reason']} | {text} |")
    return "\n".join(lines) + "\n"


def write_progress(items: list[dict[str, str | int]], before_stats: dict[str, dict[str, int]], after_stats: dict[str, dict[str, int]]) -> None:
    lines = [
        "# 第二批：第五卷、第七卷表格残文撤出",
        "",
        f"更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "## 本批范围",
        "",
        "- 第五卷城乡建设。",
        "- 第七卷经济综情。",
        "- 处理对象：空壳待录入表、表号 OCR 残文段、高密度数字串表格残文。",
        "",
        "## 已完成",
        "",
        f"- 从主阅读版撤出问题节点：{len(items)} 个。",
        "- 撤出明细：`output/reports/volume5_7_table_residue_removed.md`。",
        "- JSON 明细：`output/reports/volume5_7_table_residue_removed.json`。",
        "",
        "## 统计变化",
        "",
        "| 章节 | 指标 | 修复前 | 修复后 |",
        "|---|---|---:|---:|",
    ]
    for section in before_stats:
        for key in before_stats[section]:
            lines.append(f"| {section} | {key} | {before_stats[section][key]} | {after_stats[section][key]} |")
    lines.extend([
        "",
        "## 验收说明",
        "",
        "- 本批未把未核表格伪装成成品表。",
        "- 撤出内容均已保留证据，后续回源 PDF 核录后再嵌回正式表。",
        "- 符合东辛交付原则：最终阅读主入口不得显示校对说明、空壳表或表格 OCR 残文。",
        "",
        "## 下一步计划",
        "",
        "1. 复跑交付质量门禁，记录全书问题数量变化。",
        "2. 对第五卷、第七卷剩余长数字串进行人工复核，避免误删正文。",
        "3. 进入截图涉及的第十五卷纺织工业和附录英文总述专项。",
    ])
    PROGRESS_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def update_memory(item_count: int) -> None:
    entry = f"""
## 2026-06-29 第二批第五卷第七卷表格残文撤出

- 新增脚本：`scripts/remove_fifth_seventh_table_residue.py`。
- 从第五卷城乡建设、第七卷经济综情主阅读版撤出空壳待录入表、表号 OCR 残文和高密度数字串表格残文，共 {item_count} 个节点。
- 撤出证据保存：`output/reports/volume5_7_table_residue_removed.md`、`output/reports/volume5_7_table_residue_removed.json`。
- 本批不宣称表格完成；后续需回源 PDF 核录后再作为正式结构化表嵌回正文。
- 已写入进度文档：`output/reports/progress/20260629_第二批_第五卷第七卷表格残文撤出.md`。
"""
    memory = MEMORY_PATH.read_text(encoding="utf-8") if MEMORY_PATH.exists() else ""
    marker = "## 2026-06-29 第二批第五卷第七卷表格残文撤出"
    if marker not in memory:
        MEMORY_PATH.write_text(memory.rstrip() + "\n\n" + entry.lstrip(), encoding="utf-8")


def section_stats(block: str) -> dict[str, int]:
    text = strip_tags(block)
    return {
        "待录入": block.count("待对照原图录入"),
        "长数字串": len(LONG_NUM_RE.findall(text)),
        "structured-table": block.count('<table class="structured-table"'),
    }


def main() -> None:
    html = HTML_PATH.read_text(encoding="utf-8")
    all_removed: list[dict[str, str | int]] = []
    before_stats: dict[str, dict[str, int]] = {}
    after_stats: dict[str, dict[str, int]] = {}
    fixed = html

    for section_name, start_id, end_id, table_re in SECTIONS:
        pattern = re.compile(SECTION_RE_TEMPLATE.format(start=re.escape(start_id), end=re.escape(end_id)), re.S)
        match = pattern.search(fixed)
        if not match:
            raise RuntimeError(f"Cannot locate section {section_name}")
        heading, block = match.groups()
        before_stats[section_name] = section_stats(block)
        new_block, removed = process_section(section_name, block, table_re)
        after_stats[section_name] = section_stats(new_block)
        all_removed.extend(removed)
        fixed = fixed[: match.start()] + heading + new_block + fixed[match.end():]

    REPORT_JSON.write_text(json.dumps(all_removed, ensure_ascii=False, indent=2), encoding="utf-8")
    REPORT_MD.write_text(render_report(all_removed), encoding="utf-8")
    if fixed != html:
        HTML_PATH.write_text(fixed, encoding="utf-8")
    write_progress(all_removed, before_stats, after_stats)
    update_memory(len(all_removed))

    print("volume 5/7 residue removed")
    print(f"removed={len(all_removed)}")
    for section in before_stats:
        print(section, before_stats[section], "->", after_stats[section])
    print(f"report={REPORT_MD}")
    print(f"progress={PROGRESS_PATH}")


if __name__ == "__main__":
    main()
