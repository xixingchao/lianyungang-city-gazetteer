# -*- coding: utf-8 -*-
"""Generate the current table placeholder repair backlog."""

from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
JSON_PATH = ROOT / "output" / "reports" / "table_placeholder_backlog.json"
MD_PATH = ROOT / "output" / "reports" / "table_placeholder_backlog.md"
PROGRESS_PATH = ROOT / "output" / "reports" / "progress" / "20260629_表格专项清单_当前态.md"
MEMORY_PATH = ROOT / "PROJECT_MEMORY.md"

H2_RE = re.compile(r'<h2 id="([^"]+)">([^<]+)</h2>')
PLACEHOLDER_RE = re.compile(r'<p class="table-placeholder">(.*?)</p>', re.S)
PAGE_RE = re.compile(r'page-anchor: LYG-(\d+)')
TAG_RE = re.compile(r'<[^>]+>')
SPACE_RE = re.compile(r'\s+')
TABLE_HINT_RE = re.compile(r'([^。；;：:\n]{0,40}表\s*\d+\s*[-~—～]\s*\d+[^。；;：:\n]{0,40})')
TABLE_NAME_RE = re.compile(r'([^。；;：:\n]{4,50}表)')


def clean_html(value: str) -> str:
    value = TAG_RE.sub('', value)
    value = value.replace('&nbsp;', ' ')
    return SPACE_RE.sub(' ', value).strip()


def nearest_heading(html: str, pos: int) -> dict[str, str]:
    h2s = list(H2_RE.finditer(html[:pos]))
    if not h2s:
        return {"id": "", "title": ""}
    h2 = h2s[-1]
    return {"id": h2.group(1), "title": clean_html(h2.group(2))}


def nearest_page(html: str, pos: int) -> str:
    pages = list(PAGE_RE.finditer(html[:pos]))
    return pages[-1].group(1) if pages else ""


def snippet(html: str, start: int, end: int, width: int = 180) -> dict[str, str]:
    before = clean_html(html[max(0, start - width):start])[-width:]
    after = clean_html(html[end:end + width])[:width]
    return {"before": before, "after": after}


def table_hint(before: str, after: str) -> str:
    window = f"{before} {after}"
    matches = TABLE_HINT_RE.findall(window)
    if matches:
        return matches[-1].strip()[:80]
    matches = TABLE_NAME_RE.findall(window)
    if matches:
        return matches[-1].strip()[:80]
    return ""


def priority(count: int) -> str:
    if count >= 10:
        return "P0"
    if count >= 6:
        return "P1"
    if count >= 3:
        return "P2"
    return "P3"


def collect() -> dict[str, object]:
    html = HTML_PATH.read_text(encoding="utf-8")
    entries: list[dict[str, object]] = []
    for idx, match in enumerate(PLACEHOLDER_RE.finditer(html), start=1):
        heading = nearest_heading(html, match.start())
        context = snippet(html, match.start(), match.end())
        entries.append({
            "index": idx,
            "volume_id": heading["id"],
            "volume_title": heading["title"],
            "page_anchor": nearest_page(html, match.start()),
            "table_hint": table_hint(context["before"], context["after"]),
            "placeholder_text": clean_html(match.group(1)),
            "before": context["before"],
            "after": context["after"],
        })

    counts = Counter(entry["volume_title"] for entry in entries)
    by_volume: dict[str, list[dict[str, object]]] = defaultdict(list)
    for entry in entries:
        by_volume[str(entry["volume_title"])].append(entry)

    groups = []
    for volume, items in sorted(by_volume.items(), key=lambda kv: (-len(kv[1]), kv[0])):
        pages = sorted({str(item["page_anchor"]) for item in items if item["page_anchor"]}, key=lambda x: int(x))
        groups.append({
            "volume_title": volume,
            "count": len(items),
            "priority": priority(len(items)),
            "pages": pages,
            "items": items,
        })

    return {
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "html": str(HTML_PATH.relative_to(ROOT)),
        "total_placeholders": len(entries),
        "total_structured_tables": html.count('<table class="structured-table"'),
        "volume_count": len(counts),
        "groups": groups,
    }


def write_json(data: dict[str, object]) -> None:
    JSON_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def write_markdown(data: dict[str, object]) -> None:
    lines = [
        "# 连云港市志表格占位符专项清单",
        "",
        f"> 生成时间：{data['generated_at']}",
        f"> 基于：`{data['html']}`",
        "",
        "## 总览",
        "",
        "| 指标 | 数值 |",
        "| --- | ---: |",
        f"| 正文表格占位符 | {data['total_placeholders']} |",
        f"| 结构化表格 | {data['total_structured_tables']} |",
        f"| 涉及章节/H2 | {data['volume_count']} |",
        "",
        "## 优先级规则",
        "",
        "- P0：单卷占位符 >= 10，优先集中修复。",
        "- P1：单卷占位符 6-9，第二批修复。",
        "- P2：单卷占位符 3-5，第三批修复。",
        "- P3：单卷占位符 1-2，收尾修复。",
        "",
        "## 分卷优先级",
        "",
        "| 优先级 | 卷/章节 | 占位符 | 页锚 |",
        "| --- | --- | ---: | --- |",
    ]
    for group in data["groups"]:  # type: ignore[index]
        pages = ", ".join(group["pages"][:18])  # type: ignore[index]
        if len(group["pages"]) > 18:  # type: ignore[index]
            pages += " ..."
        lines.append(f"| {group['priority']} | {group['volume_title']} | {group['count']} | {pages} |")

    lines += ["", "## 明细", ""]
    for group in data["groups"]:  # type: ignore[index]
        lines += [
            f"### {group['priority']} {group['volume_title']}（{group['count']} 处）",
            "",
            "| 序号 | 页锚 | 表格线索 | 占位符 | 前文 | 后文 |",
            "| ---: | ---: | --- | --- | --- | --- |",
        ]
        for item in group["items"]:  # type: ignore[index]
            before = str(item["before"]).replace("|", "&#124;")
            after = str(item["after"]).replace("|", "&#124;")
            text = str(item["placeholder_text"]).replace("|", "&#124;")
            hint = str(item.get("table_hint", "")).replace("|", "&#124;")
            lines.append(f"| {item['index']} | {item['page_anchor']} | {hint} | {text} | {before} | {after} |")
        lines.append("")

    MD_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_progress(data: dict[str, object]) -> None:
    groups = data["groups"]  # type: ignore[index]
    top = groups[:6]
    top_lines = "\n".join(f"- {g['priority']} `{g['volume_title']}`：{g['count']} 处" for g in top)
    content = f"""# 2026-06-29 表格专项清单当前态

## 本轮范围
- 范围：最终阅读版正文表格占位符。
- 目标：生成当前态表格专项清单，作为后续按批修复和验收的基线。
- 输入：`output/final_reader/连云港市志_全书.html`。
- 输出：`output/reports/table_placeholder_backlog.md`、`output/reports/table_placeholder_backlog.json`。

## 当前统计
- 正文表格占位符：{data['total_placeholders']} 处。
- 结构化表格：{data['total_structured_tables']} 处。
- 涉及章节/H2：{data['volume_count']} 个。

## 优先修复对象
{top_lines}

## 已完成
- 新增脚本：`scripts/audit_table_placeholders.py`。
- 逐个记录占位符所在卷、最近页锚、表格线索、占位符文本、前后文片段。
- 生成 P0/P1/P2/P3 优先级分组，便于后续逐卷修表。

## 下一步计划
- 从 P0 开始修复：第一卷自然环境、第十卷水利。
- 每完成一卷表格替换后复跑本脚本、全书审计和 typecheck，并写进度文档。
"""
    PROGRESS_PATH.write_text(content, encoding="utf-8")


def update_memory(data: dict[str, object]) -> None:
    entry = f"""
## 2026-06-29 表格专项清单当前态完成

已生成当前态表格占位符专项清单：

- 新增脚本：`scripts/audit_table_placeholders.py`。
- 输出 Markdown：`output/reports/table_placeholder_backlog.md`。
- 输出 JSON：`output/reports/table_placeholder_backlog.json`。
- 当前正文表格占位符 {data['total_placeholders']} 处，结构化表格 {data['total_structured_tables']} 处，涉及章节/H2 {data['volume_count']} 个。
- P0 修复对象：第一卷自然环境、第十卷水利。
- 已写入进度文档：`output/reports/progress/20260629_表格专项清单_当前态.md`。

下一步：按 P0 卷逐个替换占位表格并验收。
"""
    memory = MEMORY_PATH.read_text(encoding="utf-8") if MEMORY_PATH.exists() else ""
    marker = "## 2026-06-29 表格专项清单当前态完成"
    if marker in memory:
        start = memory.find(marker)
        next_entry = memory.find("\n## ", start + len(marker))
        if next_entry == -1:
            memory = memory[:start].rstrip() + "\n" + entry
        else:
            memory = memory[:start].rstrip() + "\n" + entry.rstrip() + "\n" + memory[next_entry:].lstrip()
    else:
        memory = memory.rstrip() + "\n" + entry
    MEMORY_PATH.write_text(memory, encoding="utf-8")


def main() -> None:
    data = collect()
    write_json(data)
    write_markdown(data)
    write_progress(data)
    update_memory(data)
    print(f"placeholders={data['total_placeholders']}")
    print(f"structured_tables={data['total_structured_tables']}")
    print(f"volumes={data['volume_count']}")
    print(f"markdown={MD_PATH}")
    print(f"json={JSON_PATH}")


if __name__ == "__main__":
    main()
