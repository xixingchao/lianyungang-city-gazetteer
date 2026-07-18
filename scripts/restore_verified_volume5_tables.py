# -*- coding: utf-8 -*-
"""Restore verified structured tables in volume 5 after residue cleanup."""

from __future__ import annotations

import html
import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
DATA_DIR = ROOT / "workbench" / "table_entries" / "上" / "data"
PROGRESS_PATH = ROOT / "output" / "reports" / "progress" / "20260629_第二批_第五卷已核表恢复.md"
MEMORY_PATH = ROOT / "PROJECT_MEMORY.md"

TABLES = [
    ("LYG-上-T009", ["1990年连云港市建制镇规划情况表表5-1"]),
    ("LYG-上-T011", ["1983~1990年连云港市节约用水情况表", "1983～1990年连云港市节约用水情况表", "四、节约用水"]),
    ("LYG-上-T013", ["1961年新浦地区住房调查统计表表5-12"]),
]

SECTION_RE = re.compile(r'(<h2 id="第五卷-城乡建设">.*?</h2>)(.*?)(?=<h2 id="第六卷-环境保护">)', re.S)


def make_table(data: dict) -> str:
    caption = f"{data.get('table_number', '').strip()} {data.get('title', '').strip()}".strip()
    headers = data.get("columns", [])
    rows = data.get("rows", [])
    ths = "".join(f"<th>{html.escape(str(h))}</th>" for h in headers)
    trs = []
    for row in rows:
        trs.append("<tr>" + "".join(f"<td>{html.escape(str(v))}</td>" for v in row) + "</tr>")
    return f'<table class="structured-table"><caption>{html.escape(caption)}</caption><thead><tr>{ths}</tr></thead><tbody>{"".join(trs)}</tbody></table>'


def has_empty_marker(data: dict) -> bool:
    return any("待对照原图录入" in str(cell) for row in data.get("rows", []) for cell in row)


def restore() -> list[str]:
    html_text = HTML_PATH.read_text(encoding="utf-8")
    match = SECTION_RE.search(html_text)
    if not match:
        raise RuntimeError("Cannot locate 第五卷 section")
    heading, block = match.groups()
    actions: list[str] = []

    for table_id, markers in TABLES:
        data = json.loads((DATA_DIR / f"{table_id}.json").read_text(encoding="utf-8"))
        caption = f"{data.get('table_number', '').strip()} {data.get('title', '').strip()}".strip()
        if has_empty_marker(data):
            actions.append(f"跳过空壳表：{table_id} {caption}")
            continue
        if f"<caption>{html.escape(caption)}</caption>" in block:
            actions.append(f"已存在：{table_id} {caption}")
            continue
        marker = next((item for item in markers if item in block), "")
        marker_pos = block.find(marker) if marker else -1
        if marker_pos == -1:
            actions.append(f"未找到恢复位置：{table_id} {caption}")
            continue
        para_end = block.find("</p>", marker_pos)
        if para_end == -1:
            actions.append(f"未找到表题段落结尾：{table_id} {caption}")
            continue
        insert_pos = para_end + len("</p>")
        block = block[:insert_pos] + "\n" + make_table(data) + block[insert_pos:]
        actions.append(f"恢复已核结构化表：{table_id} {caption}")

    fixed = html_text[: match.start()] + heading + block + html_text[match.end():]
    if fixed != html_text:
        HTML_PATH.write_text(fixed, encoding="utf-8")
    return actions


def write_progress(actions: list[str]) -> None:
    action_lines = "\n".join(f"- {a}" for a in actions) or "- 本次复跑未产生新改动，脚本保持幂等。"
    content = f"""# 第二批：第五卷已核结构化表恢复

更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}

## 已完成
{action_lines}

## 验收说明

- 本轮纠正表格残文撤出时过度保守的问题：已核结构化表不应从阅读版移除。
- 仍保留撤出原则：空壳 `待对照原图录入` 表和 OCR 串行残文不得出现在主阅读版。
- 恢复脚本会跳过含 `待对照原图录入` 的空壳表，避免把未核实数据伪装成交付表。
- 恢复表只渲染标题、表头和数据，不把表格 JSON 内部 notes 暴露到主阅读版。

## 下一步计划

- 复跑交付门禁，确认第五卷仍无空壳表和长数字串，同时保留已核结构化表展示。
"""
    PROGRESS_PATH.write_text(content, encoding="utf-8")


def update_memory(actions: list[str]) -> None:
    restored = len([a for a in actions if a.startswith("恢复已核")])
    entry = f"""
## 2026-06-29 第二批第五卷已核表恢复

- 新增脚本：`scripts/restore_verified_volume5_tables.py`。
- 纠正第二批表格残文撤出时的过度保守问题：恢复第五卷已核结构化表展示，保留空壳表和 OCR 残文撤出原则。
- 恢复项：{restored}；恢复脚本会跳过含 `待对照原图录入` 的空壳表，且不把内部 notes 暴露到主阅读版。
- 已写入进度文档：`output/reports/progress/20260629_第二批_第五卷已核表恢复.md`。
"""
    memory = MEMORY_PATH.read_text(encoding="utf-8") if MEMORY_PATH.exists() else ""
    marker = "## 2026-06-29 第二批第五卷已核表恢复"
    if marker not in memory:
        MEMORY_PATH.write_text(memory.rstrip() + "\n\n" + entry.lstrip(), encoding="utf-8")


def main() -> None:
    actions = restore()
    write_progress(actions)
    update_memory(actions)
    print("verified volume 5 tables restored")
    for action in actions:
        print(f"- {action}")
    if not actions:
        print("- no changes")
    print(f"progress={PROGRESS_PATH}")


if __name__ == "__main__":
    main()
