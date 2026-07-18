# -*- coding: utf-8 -*-
"""Remove duplicate verified T001 block when the table already appears inline."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_volume1_t001_duplicate_block_20260705.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_volume1_t001_duplicate_block_20260705.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260705_第一卷地层系统表重复块清理.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

CAPTION = "表1-1 连云港市地层系统表"
INLINE_MARKER = f"<caption>{CAPTION}</caption>"
BLOCK_START = '<section class="verified-table-block" id="table-LYG-上-T001">'
NEXT_BLOCK = '<section class="verified-table-block" id="table-LYG-上-T002">'
SOURCE = "workbench/table_entries/上/data/LYG-上-T001.json"


def append_once(path: Path, marker: str, content: str) -> None:
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker not in old:
        path.write_text(old.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")


def main() -> None:
    html = HTML.read_text(encoding="utf-8")
    caption_count_before = html.count(INLINE_MARKER)
    if caption_count_before != 2:
        raise RuntimeError(f"expected two T001 captions before cleanup, got {caption_count_before}")
    start = html.index(BLOCK_START)
    end = html.index(NEXT_BLOCK, start)
    removed = html[start:end]
    if INLINE_MARKER not in removed:
        raise RuntimeError("verified T001 block did not contain expected caption")

    new_html = html[:start] + html[end:]
    caption_count_after = new_html.count(INLINE_MARKER)
    if caption_count_after != 1:
        raise RuntimeError(f"expected one T001 caption after cleanup, got {caption_count_after}")
    HTML.write_text(new_html, encoding="utf-8")

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "第一卷自然环境 / 表1-1 连云港市地层系统表",
        "source": SOURCE,
        "caption_count_before": caption_count_before,
        "caption_count_after": caption_count_after,
        "removed_block_id": "table-LYG-上-T001",
        "principle": "正文自然位置已保留同表，删除卷末已核集合中的重复展示块，不改表格数据。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    md = f"""# 第一卷地层系统表重复块清理

- 时间：{now}
- 范围：第一卷自然环境 / 表1-1 连云港市地层系统表。
- 数据依据：`{SOURCE}`。

## 处理

- 清理前最终阅读版中 `{CAPTION}` 出现 {caption_count_before} 次。
- 删除卷末“已核结构化表格”集合内重复的 `table-LYG-上-T001` 展示块。
- 保留正文自然位置的同表，表格数据未改。
- 清理后最终阅读版中 `{CAPTION}` 出现 {caption_count_after} 次。
"""
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")

    marker = "## 2026-07-05 第一卷地层系统表重复块清理"
    append_once(
        MEMORY,
        marker,
        f"""
{marker}
- 最终阅读版中 `表1-1 连云港市地层系统表` 同时出现在正文自然位置和卷末已核集合；本轮删除卷末重复展示块 `table-LYG-上-T001`，保留正文位置表格。
- 表格数据未改，结构化源仍在 `{SOURCE}` 与结构化表格站点中。
- 报告：`output/reports/reader_volume1_t001_duplicate_block_20260705.md`。
""",
    )

    print("volume1_t001_duplicate_block_removed")
    print(f"caption_count_before={caption_count_before}")
    print(f"caption_count_after={caption_count_after}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()
