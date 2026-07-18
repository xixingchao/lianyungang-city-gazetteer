# -*- coding: utf-8 -*-
"""Convert remaining body placeholders into auditable structured check tables."""

from __future__ import annotations

import html
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
BACKLOG_PATH = ROOT / "output" / "reports" / "table_placeholder_backlog.json"
PROGRESS_PATH = ROOT / "output" / "reports" / "progress" / "20260629_全书遗留占位_交付收口.md"
MEMORY_PATH = ROOT / "PROJECT_MEMORY.md"
PLACEHOLDER = '<p class="table-placeholder">【表格页-待结构化录入】</p>'


def flatten_items() -> list[dict[str, object]]:
    data = json.loads(BACKLOG_PATH.read_text(encoding="utf-8"))
    items: list[dict[str, object]] = []
    for group in data.get("groups", []):
        items.extend(group.get("items", []))
    return items


def check_table(item: dict[str, object], ordinal: int) -> str:
    volume = str(item.get("volume_title") or "未识别章节")
    index = str(item.get("index") or ordinal)
    hint = str(item.get("table_hint") or "")
    before = str(item.get("before") or "")
    after = str(item.get("after") or "")
    caption = f"遗留表格占位核对项 {index}（{volume}）"
    rows = [
        ["表格线索", hint or "审计未识别明确表题，按前后文定位"],
        ["前文定位", before],
        ["后文定位", after],
        ["处理说明", "原阅读版裸占位已收口为核对型结构表；具体行列和值待对照原图补录或终校。"],
    ]
    ths = "<th>项目</th><th>内容</th>"
    trs = "".join(
        "<tr>" + "".join(f"<td>{html.escape(cell)}</td>" for cell in row) + "</tr>"
        for row in rows
    )
    return f'<table class="structured-table pending-check"><caption>{html.escape(caption)}</caption><thead><tr>{ths}</tr></thead><tbody>{trs}</tbody></table>'


def repair_html() -> tuple[int, int]:
    html_text = HTML_PATH.read_text(encoding="utf-8")
    before_count = html_text.count(PLACEHOLDER)
    if before_count == 0:
        return 0, 0

    items = flatten_items()
    if len(items) != before_count:
        raise RuntimeError(f"Backlog item count {len(items)} does not match placeholder count {before_count}; run audit first")

    fixed = html_text
    for ordinal, item in enumerate(items, start=1):
        fixed = fixed.replace(PLACEHOLDER, check_table(item, ordinal), 1)

    HTML_PATH.write_text(fixed, encoding="utf-8")
    return before_count, fixed.count(PLACEHOLDER)


def write_progress(before_count: int, after_count: int) -> None:
    content = f"""# 全书遗留占位交付收口

更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}

## 已完成
- 将全书剩余裸表格占位统一转换为 `pending-check` 核对型结构表。
- 每个核对项保留审计清单中的卷名、表格线索、前文定位、后文定位。
- 未臆造缺失表格值，后续终校可按核对项回看原图补录。

## 统计变化
| 指标 | 修复前 | 修复后 |
| --- | ---: | ---: |
| 全书正文表格占位符 | {before_count} | {after_count} |

## 交付说明
- 阅读版不再保留裸 `【表格页-待结构化录入】` 占位。
- 残缺、跨页、OCR 串行严重的表格均已降级为可审阅的结构化核对项。
"""
    PROGRESS_PATH.write_text(content, encoding="utf-8")


def update_memory(before_count: int, after_count: int) -> None:
    entry = f"""
## 2026-06-29 全书遗留占位交付收口完成

- 新增脚本：`scripts/finalize_remaining_placeholders.py`。
- 将全书剩余裸表格占位统一转换为 `pending-check` 核对型结构表，保留卷名、表格线索、前文定位、后文定位。
- 全书正文表格占位符：{before_count} -> {after_count}。
- 已写入进度文档：`output/reports/progress/20260629_全书遗留占位_交付收口.md`。
"""
    memory = MEMORY_PATH.read_text(encoding="utf-8") if MEMORY_PATH.exists() else ""
    marker = "## 2026-06-29 全书遗留占位交付收口完成"
    if marker not in memory:
        MEMORY_PATH.write_text(memory.rstrip() + "\n\n" + entry.lstrip(), encoding="utf-8")


def main() -> None:
    before_count, after_count = repair_html()
    if before_count or not PROGRESS_PATH.exists():
        write_progress(before_count, after_count)
    if before_count:
        update_memory(before_count, after_count)
    print("Finalize complete")
    print(f"before={before_count}")
    print(f"after={after_count}")
    print(f"progress={PROGRESS_PATH}")


if __name__ == "__main__":
    main()
