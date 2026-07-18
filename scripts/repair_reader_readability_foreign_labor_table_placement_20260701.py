# -*- coding: utf-8 -*-
"""Move verified table 35-10 to its reader location and remove flattened residue."""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
DATA = ROOT / "workbench" / "table_entries" / "中" / "data" / "LYG-中-T093.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_foreign_labor_table_placement_20260701.md"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_foreign_labor_table_placement_20260701.json"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260701_第三十五卷对外工程劳务表残文修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

TABLE_RE = re.compile(
    r"\n?<section class=\"verified-table-block\" id=\"table-LYG-中-T093\">.*?</section>\s*",
    re.S,
)

RESIDUE_RE = re.compile(
    r"\n?<p>\(人\)1987\.3中江公司东海一建科威特.*?1991\. 12</p>\s*",
    re.S,
)


def patch_reader() -> tuple[int, int]:
    text = HTML.read_text(encoding="utf-8")
    table_matches = list(TABLE_RE.finditer(text))
    if len(table_matches) != 1:
        raise RuntimeError(f"expected exactly one existing T093 table block, found {len(table_matches)}")
    table_block = table_matches[0].group(0).strip()

    without_old, removed = TABLE_RE.subn("\n", text, count=1)
    new, replaced = RESIDUE_RE.subn("\n" + table_block + "\n", without_old, count=1)
    if replaced != 1:
        raise RuntimeError(f"expected to replace one flattened foreign labor residue, replaced {replaced}")
    HTML.write_text(new, encoding="utf-8")
    return removed, replaced


def write_reports(removed: int, replaced: int) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    entry = json.loads(DATA.read_text(encoding="utf-8"))
    result = {
        "time": now,
        "table_id": "LYG-中-T093",
        "table_number": entry.get("table_number"),
        "title": entry.get("title"),
        "source_pages": entry.get("pages"),
        "existing_reader_table_blocks_removed": removed,
        "reader_flattened_blocks_replaced": replaced,
        "json_changed": False,
        "site_changed": False,
        "rows": entry.get("row_count"),
        "columns": entry.get("col_count"),
    }
    REPORT_JSON.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    md = f"""# 第三十五卷对外工程劳务表残文修复

- 时间：{now}
- 表ID：`LYG-中-T093`
- 表题：表35-10 `1987~1990年连云港市对外工程和劳务合作项目表`
- 源页：`workbench/ocr/paddle_ocr/中/part02/page_0204.txt`

## 修复动作

- 保持现有 verified 结构化表 `workbench/table_entries/中/data/LYG-中-T093.json` 不变。
- 从最终阅读版中移除原先夹在结构化表集合末尾的 `table-LYG-中-T093` 表块：{removed} 组。
- 将第三十五卷第四章第三节“国际劳务合作”下 `(人)1987.3中江公司...1991. 12` 压平残文替换为同一 verified 表块：{replaced} 组。

## 核对说明

- 该残文与 `LYG-中-T093` 完全对应，不新增表、不改表数据。
- 修复目标是阅读版位置和残文清理：表35-10 应出现在“第三节国际劳务合作”下，而不是滞留在结构化表集合末尾。
"""
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")


def update_memory(removed: int, replaced: int) -> None:
    marker = "## 2026-07-01 第三十五卷对外工程劳务表残文修复"
    memory = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker in memory:
        return
    entry = f"""
{marker}

- 对正文可读性审计命中的第三十五卷对外经济贸易 `(人)1987.3中江公司东海一建...1991. 12` 摊平残文处理。
- 确认该段已由 `workbench/table_entries/中/data/LYG-中-T093.json` 覆盖：表35-10《1987~1990年连云港市对外工程和劳务合作项目表》，19 行 9 列。
- 本轮未改表数据，仅将阅读版中已有 `table-LYG-中-T093` 表块移动到“第三节国际劳务合作”处，移除原错误位置 {removed} 组，并替换压平残文 {replaced} 组。
- 报告：`output/reports/reader_readability_foreign_labor_table_placement_20260701.md`。
"""
    MEMORY.write_text(memory.rstrip() + "\n\n" + entry.lstrip(), encoding="utf-8")


def main() -> None:
    removed, replaced = patch_reader()
    write_reports(removed, replaced)
    update_memory(removed, replaced)
    print(f"existing_reader_table_blocks_removed={removed}")
    print(f"reader_flattened_blocks_replaced={replaced}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()
