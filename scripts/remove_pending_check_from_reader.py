# -*- coding: utf-8 -*-
"""Move pending-check workbench tables out of the final reader.

These tables were created as audit placeholders, not verified reader-facing
content. Keep their evidence in reports, then remove them from the main HTML.
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
REPORT_MD = ROOT / "output" / "reports" / "pending_check_removed_from_reader.md"
REPORT_JSON = ROOT / "output" / "reports" / "pending_check_removed_from_reader.json"
PROGRESS_PATH = ROOT / "output" / "reports" / "progress" / "20260629_第二批_pending_check撤出主阅读版.md"
MEMORY_PATH = ROOT / "PROJECT_MEMORY.md"

TABLE_RE = re.compile(r'<table class="structured-table pending-check">.*?</table>\n?', re.S)
H2_RE = re.compile(r'<h2[^>]*>(.*?)</h2>', re.S)
CAPTION_RE = re.compile(r'<caption>(.*?)</caption>', re.S)
ROW_RE = re.compile(r'<tr><td>(.*?)</td><td>(.*?)</td></tr>', re.S)


def strip_tags(value: str) -> str:
    value = re.sub(r"<[^>]+>", "", value)
    value = unescape(value)
    value = re.sub(r"\s+", " ", value).strip()
    return value


def detect_section(html_text: str, pos: int) -> str:
    section = "未进入正文"
    for match in H2_RE.finditer(html_text, 0, pos):
        section = strip_tags(match.group(1)) or section
    return section


def caption_volume(caption: str) -> str:
    m = re.search(r"（(.+?)）", caption)
    return m.group(1) if m else "未识别"


def extract_items(html_text: str) -> list[dict[str, str | int]]:
    items: list[dict[str, str | int]] = []
    for match in TABLE_RE.finditer(html_text):
        block = match.group(0)
        cap_match = CAPTION_RE.search(block)
        caption = strip_tags(cap_match.group(1)) if cap_match else "未命名 pending-check"
        rows = {strip_tags(k): strip_tags(v) for k, v in ROW_RE.findall(block)}
        current_section = detect_section(html_text, match.start())
        intended = caption_volume(caption)
        items.append(
            {
                "line_hint": html_text.count("\n", 0, match.start()) + 1,
                "current_section": current_section,
                "intended_section": intended,
                "caption": caption,
                "table_hint": rows.get("表格线索", ""),
                "before": rows.get("前文定位", ""),
                "after": rows.get("后文定位", ""),
                "status": "removed_from_reader_pending_source_pdf_verification",
            }
        )
    return items


def render_report(items: list[dict[str, str | int]], before_count: int, after_count: int) -> str:
    mismatch = sum(1 for item in items if str(item["intended_section"]) not in str(item["current_section"]))
    by_intended = Counter(str(item["intended_section"]) for item in items)
    lines = [
        "# pending-check 核对表撤出主阅读版记录",
        "",
        f"> 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"> 基于：`{HTML_PATH.relative_to(ROOT)}`",
        "",
        "## 处理结论",
        "",
        "- `pending-check` 表属于工作台核对项，不是已核对结构化表，不能进入最终阅读版。",
        "- 本轮已将其从主阅读 HTML 撤出，并完整保存定位信息到本报告和 JSON。",
        "- 这些表格后续必须回源 PDF 核录，确认后再作为正式结构化表嵌入正文。",
        "",
        "## 统计",
        "",
        "| 指标 | 数值 |",
        "|---|---:|",
        f"| 撤出前 pending-check 表 | {before_count} |",
        f"| 撤出后 pending-check 表 | {after_count} |",
        f"| 当前章节与标题标注不一致项 | {mismatch} |",
        "",
        "## 按标注章节分布",
        "",
        "| 标注章节 | 数量 |",
        "|---|---:|",
    ]
    for key, count in by_intended.most_common():
        lines.append(f"| {key} | {count} |")

    lines.extend([
        "",
        "## 明细",
        "",
        "| 原行号 | 当前所在章节 | 标注章节 | 标题 | 表格线索 |",
        "|---:|---|---|---|---|",
    ])
    for item in items:
        hint = str(item["table_hint"]).replace("|", "\\|")
        if len(hint) > 120:
            hint = hint[:119] + "..."
        lines.append(
            f"| {item['line_hint']} | {item['current_section']} | {item['intended_section']} | {item['caption']} | {hint} |"
        )
    return "\n".join(lines) + "\n"


def write_progress(items: list[dict[str, str | int]], before_count: int, after_count: int) -> None:
    mismatch = sum(1 for item in items if str(item["intended_section"]) not in str(item["current_section"]))
    content = f"""# 第二批：pending-check 核对表撤出主阅读版

更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}

## 本批范围

- 范围：`output/final_reader/连云港市志_全书.html` 中全部 `pending-check` 核对表。
- 重点关注：用户截图和门禁同时命中的第五卷城乡建设、第七卷经济综情。
- 原因：`pending-check` 是工作台核对项，不是已核对结构化表；且本轮核查发现部分核对项当前所在章节与标题标注不一致，说明主阅读版已被污染。

## 已完成

- 从主阅读版撤出 `pending-check` 表：{before_count} -> {after_count}。
- 将撤出明细完整保存到：`output/reports/pending_check_removed_from_reader.md`。
- 将结构化明细保存到：`output/reports/pending_check_removed_from_reader.json`。
- 当前章节与标题标注不一致项：{mismatch}。

## 验收说明

- 撤出并不代表表格已完成；它只是把未核工作项移出读者主入口。
- 后续需按报告中的标注章节回源 PDF 核录，确认后再作为正式结构化表嵌回正文。
- 本批符合东辛交付原则：最终阅读版不显示校对说明、占位卡片或未核工作台内容。

## 下一步计划

1. 继续处理第五卷城乡建设、第七卷经济综情中剩余的 `待对照原图录入` 空表和长数字串表格残文。
2. 对能从源 MD/表格站确认的表格，补成正式结构化表；不能确认的登记专项报告，不留在主阅读版。
3. 复跑 `scripts/audit_delivery_quality.py`，记录问题总量和类型变化。
"""
    PROGRESS_PATH.write_text(content, encoding="utf-8")


def update_memory(before_count: int, after_count: int, item_count: int) -> None:
    entry = f"""
## 2026-06-29 第二批 pending-check 撤出主阅读版

- 新增脚本：`scripts/remove_pending_check_from_reader.py`。
- 从最终阅读版撤出 `pending-check` 工作台核对表：{before_count} -> {after_count}。
- 撤出明细 {item_count} 条已保存：`output/reports/pending_check_removed_from_reader.md`、`output/reports/pending_check_removed_from_reader.json`。
- 本批只移出未核工作项，不宣称这些表格已完成；后续需按报告回源 PDF 核录后再嵌回正式结构化表。
- 已写入进度文档：`output/reports/progress/20260629_第二批_pending_check撤出主阅读版.md`。
"""
    memory = MEMORY_PATH.read_text(encoding="utf-8") if MEMORY_PATH.exists() else ""
    marker = "## 2026-06-29 第二批 pending-check 撤出主阅读版"
    if marker not in memory:
        MEMORY_PATH.write_text(memory.rstrip() + "\n\n" + entry.lstrip(), encoding="utf-8")


def main() -> None:
    html_text = HTML_PATH.read_text(encoding="utf-8")
    items = extract_items(html_text)
    before_count = len(items)
    fixed = TABLE_RE.sub("", html_text)
    after_count = len(TABLE_RE.findall(fixed))

    REPORT_JSON.write_text(json.dumps(items, ensure_ascii=False, indent=2), encoding="utf-8")
    REPORT_MD.write_text(render_report(items, before_count, after_count), encoding="utf-8")
    if fixed != html_text:
        HTML_PATH.write_text(fixed, encoding="utf-8")
    write_progress(items, before_count, after_count)
    update_memory(before_count, after_count, len(items))

    print("pending-check removed")
    print(f"before={before_count}")
    print(f"after={after_count}")
    print(f"report={REPORT_MD}")
    print(f"progress={PROGRESS_PATH}")


if __name__ == "__main__":
    main()
