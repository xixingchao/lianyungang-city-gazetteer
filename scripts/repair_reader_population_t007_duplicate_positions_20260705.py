# -*- coding: utf-8 -*-
"""Remove duplicate displays of population table T007, keeping the source-natural position."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_population_t007_duplicate_positions_20260705.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_population_t007_duplicate_positions_20260705.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260705_第四卷人口表4-3重复展示清理.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

CAPTION = "表4-3 1949~1990年连云港市人口自然变动情况表"
CAPTION_MARKER = f"<caption>{CAPTION}</caption>"
EARLY_ANCHOR = "<h4 id=\"第四卷-第一章人口规模-第二节人口变动\">第二节人口变动</h4>"
CORRECT_PRECEDING = "<p>以1970年人口自然增长水平推算，1971～1990年的20年中，全市累计避免出生97.60万人。</p>"
VERIFIED_ID = "table-LYG-上-T007"
SOURCE = "workbench/ocr/raw/上/part01/page_0283.txt; workbench/table_entries/上/data/LYG-上-T007.json"


def append_once(path: Path, marker: str, content: str) -> None:
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker not in old:
        path.write_text(old.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")


def table_bounds_around_caption(html: str, caption_pos: int) -> tuple[int, int]:
    start = html.rfind('<table class="structured-table">', 0, caption_pos)
    if start < 0:
        raise RuntimeError("table start not found")
    end = html.index("</table>", caption_pos) + len("</table>")
    return start, end


def remove_verified_block(html: str, block_id: str) -> tuple[str, str]:
    start_marker = f'<section class="verified-table-block" id="{block_id}">'
    start = html.index(start_marker)
    end = html.index("</section>", start) + len("</section>")
    return html[:start] + html[end:], html[start:end]


def main() -> None:
    html = HTML.read_text(encoding="utf-8")
    before = html.count(CAPTION_MARKER)
    if before != 4:
        raise RuntimeError(f"expected four T007 captions before cleanup, got {before}")

    second_section = html.index(EARLY_ANCHOR)
    first_caption = html.index(CAPTION_MARKER)
    if first_caption > second_section:
        raise RuntimeError("first T007 caption is not before 第二节人口变动")
    early_start, early_end = table_bounds_around_caption(html, first_caption)
    early_removed = html[early_start:early_end]
    html = html[:early_start] + html[early_end:]

    correct_pos = html.index(CORRECT_PRECEDING)
    correct_caption = html.index(CAPTION_MARKER, correct_pos)
    if correct_caption < correct_pos:
        raise RuntimeError("correct T007 caption not after source-natural preceding paragraph")
    correct_start, correct_end = table_bounds_around_caption(html, correct_caption)
    adjacent_caption = html.index(CAPTION_MARKER, correct_end)
    if adjacent_caption > html.index("<p>二、机械变动", correct_end):
        raise RuntimeError("expected adjacent duplicate T007 before 二、机械变动")
    adjacent_start, adjacent_end = table_bounds_around_caption(html, adjacent_caption)
    adjacent_removed = html[adjacent_start:adjacent_end]
    html = html[:adjacent_start] + html[adjacent_end:]

    html, verified_removed = remove_verified_block(html, VERIFIED_ID)
    after = html.count(CAPTION_MARKER)
    if after != 1:
        raise RuntimeError(f"expected one T007 caption after cleanup, got {after}")
    if CAPTION_MARKER not in early_removed or CAPTION_MARKER not in adjacent_removed or CAPTION_MARKER not in verified_removed:
        raise RuntimeError("removed blocks did not contain expected caption")

    HTML.write_text(html, encoding="utf-8")

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "第四卷人口 / 表4-3 人口自然变动情况表",
        "source": SOURCE,
        "caption_count_before": before,
        "caption_count_after": after,
        "removed": ["第一节人口总量末尾提前插入的重复表", "正确位置后紧贴的重复表", VERIFIED_ID],
        "kept": "第二节人口变动 / 一、自然变动 后、源文自然位置的表格",
        "principle": "只删除重复展示，不改表格数据。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    md = f"""# 第四卷人口表4-3重复展示清理

- 时间：{now}
- 范围：第四卷人口 / 表4-3 人口自然变动情况表。
- 依据：`{SOURCE}`。

## 处理

- 清理前 `{CAPTION}` 在最终阅读版出现 {before} 次。
- 删除第一节人口总量末尾提前插入的重复表。
- 删除正确位置后紧贴的第二份重复表。
- 删除卷末已核集合重复展示块 `{VERIFIED_ID}`。
- 保留第二节人口变动 / 一、自然变动 后、源文自然位置的表格。
- 清理后 `{CAPTION}` 在最终阅读版出现 {after} 次。

表格数据未改，结构化表格 JSON 与结构化表格站点未改。
"""
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")

    marker = "## 2026-07-05 第四卷人口表4-3重复展示清理"
    append_once(
        MEMORY,
        marker,
        f"""
{marker}
- 依据 `{SOURCE}` 确认 `表4-3 1949~1990年连云港市人口自然变动情况表` 源文自然位置在第二节人口变动 / 一、自然变动 后。
- 删除第一节末尾提前插入的重复表、正确位置后紧贴的重复表，以及卷末已核集合重复块 `{VERIFIED_ID}`，保留正确位置表格。
- 报告：`output/reports/reader_population_t007_duplicate_positions_20260705.md`。
""",
    )

    print("population_t007_duplicate_positions_removed")
    print(f"caption_count_before={before}")
    print(f"caption_count_after={after}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()
