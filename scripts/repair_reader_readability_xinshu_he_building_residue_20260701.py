# -*- coding: utf-8 -*-
"""Remove duplicate flattened reader residue for verified table LYG-上-T027."""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
TABLE_JSON = ROOT / "workbench" / "table_entries" / "上" / "data" / "LYG-上-T027.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_xinshu_he_building_residue_20260701.md"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_xinshu_he_building_residue_20260701.json"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260701_新沭河穿堤建筑物表重复残文修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

RESIDUE_RE = re.compile(
    r"\n?<p>别（米）</p>\s*"
    r"<p>（个）</p>\s*"
    r"<p>（米）</p>\s*"
    r"<p>（米）</p>\s*"
    r"<p>（米）</p>\s*"
    r"<p>（米）</p>\s*"
    r"<p>李曹埠电排涵1\.01\.516\.515\.01\.58.*?元宝港闸1×6\.51×7\.5</p>\s*",
    re.S,
)

REQUIRED_HTML_MARKERS = [
    'id="table-LYG-上-T027"',
    "表10-3 1990年新沭河连云港市境内穿堤建筑物情况表",
    "李曹埠电排涵",
    "元宝港闸",
]


def verify_existing_table() -> dict[str, object]:
    html = HTML.read_text(encoding="utf-8")
    missing = [marker for marker in REQUIRED_HTML_MARKERS if marker not in html]
    if missing:
        raise RuntimeError(f"verified table markers missing from final reader: {missing}")
    data = json.loads(TABLE_JSON.read_text(encoding="utf-8"))
    if data.get("status") != "verified":
        raise RuntimeError("LYG-上-T027 is not verified")
    if data.get("table_number") != "表10-3":
        raise RuntimeError("LYG-上-T027 table number mismatch")
    if not any(row and row[0] == "李曹埠电排涵" for row in data.get("rows", [])):
        raise RuntimeError("LYG-上-T027 row marker not found")
    return data


def remove_residue() -> int:
    text = HTML.read_text(encoding="utf-8")
    new, count = RESIDUE_RE.subn("\n", text, count=1)
    if count != 1:
        raise RuntimeError(f"expected to remove 1 residue block, removed {count}")
    HTML.write_text(new, encoding="utf-8")
    return count


def write_reports(table: dict[str, object], removed: int) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    result = {
        "time": now,
        "table_id": table.get("table_id"),
        "table_number": table.get("table_number"),
        "title": table.get("title"),
        "status": table.get("status"),
        "source_pages": table.get("pages"),
        "reader_residue_blocks_removed": removed,
        "data_changed": False,
        "source_json": str(TABLE_JSON.relative_to(ROOT)).replace("\\", "/"),
        "final_reader": str(HTML.relative_to(ROOT)).replace("\\", "/"),
    }
    REPORT_JSON.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    md = f"""# 新沭河穿堤建筑物表重复残文修复

- 时间：{now}
- 表ID：`{table.get('table_id')}`
- 表题：{table.get('table_number')} {table.get('title')}
- 结构化表：`workbench/table_entries/上/data/LYG-上-T027.json`
- 最终阅读版：`output/final_reader/连云港市志_全书.html`

## 修复动作

- 确认最终阅读版已存在 verified 表块 `table-LYG-上-T027`，且表内包含 `李曹埠电排涵` 至 `元宝港闸` 的记录。
- 撤出正文中重复出现的压平表头单位残片和 `李曹埠电排涵...元宝港闸` 串行残文：{removed} 组。
- 未改动 `LYG-上-T027` 结构化表数据。

## 核对说明

- 本次属于重复残文清理：结构化表已在此前回源核录为 verified。
- 删除范围止于 `元宝港闸1×6.51×7.5` 段落；其后的 `（83 公里）`、`（92 公里）` 等正文距离注记未处理。
"""
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")


def update_memory(removed: int) -> None:
    marker = "## 2026-07-01 新沭河穿堤建筑物表重复残文修复"
    memory = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker in memory:
        return
    entry = f"""
{marker}

- 对正文可读性审计命中的第十卷水利残文 `李曹埠电排涵...元宝港闸` 做重复表文清理。
- 先确认 `output/final_reader/连云港市志_全书.html` 已存在 verified 表块 `table-LYG-上-T027`，且 `workbench/table_entries/上/data/LYG-上-T027.json` 状态为 verified。
- 从最终阅读版撤出压平表头单位残片及串行残文 {removed} 组；未修改结构化表数据。
- 报告：`output/reports/reader_readability_xinshu_he_building_residue_20260701.md`。
"""
    MEMORY.write_text(memory.rstrip() + "\n\n" + entry.lstrip(), encoding="utf-8")


def main() -> None:
    table = verify_existing_table()
    removed = remove_residue()
    write_reports(table, removed)
    update_memory(removed)
    print(f"verified_table={table.get('table_id')}")
    print(f"reader_residue_blocks_removed={removed}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()
