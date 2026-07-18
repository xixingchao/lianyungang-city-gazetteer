# -*- coding: utf-8 -*-
"""Remove source-backed hydrology rainstorm table residue from the full reader."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_hydrology_rainstorm_table_residue_20260705.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_hydrology_rainstorm_table_residue_20260705.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260705_水文暴雨表残片清理.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

OLD = (
    "<p>高水位（月·日）</p>\n\n\n\n"
    "<p>高水位（月·日）</p>\n\n\n\n"
    "<p>高水位（月·日）</p>\n\n\n\n\n"
    "<p>高水位（月·日）</p>\n\n"
    "<p>94.09.1517.367.31河58.733.5（33.3）</p>\n\n\n"
    "<p>62.07.515.96（5.1）</p>\n\n"
    "<p>东海（牛山）</p>\n"
    "<p>赣榆（青口）</p>\n"
    "<p>灌云（伊山）</p>\n"
    "<p>时段雨量年份日期雨量年份日期雨量年份日期雨量年份日期（月·日）</p>\n"
    "<p>（月·日）</p>\n"
    "<p>（月·日）</p>\n"
    "<p>（月·日）</p>\n\n"
    "<p>2。 赣榆站短历时暴雨统计用小塔山水库站1953～1980年资料代替。</p>\n"
)

NEW = (
    "<p>注：1.东海站短历时暴雨统计由石梁河水库站资料代替，其它统计1953～1980年的降雨资料采用麦坡站资料。</p>\n"
    "<p>2.赣榆站短历时暴雨统计用小塔山水库站1953～1980年资料代替。</p>\n"
)

SOURCES = [
    "workbench/ocr/raw/上/part01/page_0178.txt:3-164",
    "workbench/ocr/raw/上/part01/page_0179.txt:4-5",
]


def append_once(path: Path, marker: str, content: str) -> None:
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker not in old:
        path.write_text(old.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")


def main() -> None:
    html = HTML.read_text(encoding="utf-8")
    old_count = html.count(OLD)
    if old_count == 1:
        html = html.replace(OLD, NEW, 1)
        status = "changed"
        changed = 1
    elif old_count == 0 and html.count(NEW) >= 1:
        status = "already_applied"
        changed = 0
    else:
        raise RuntimeError(f"expected hydrology rainstorm residue once, got {old_count}")

    HTML.write_text(html, encoding="utf-8")

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "target": str(HTML.relative_to(ROOT)).replace("\\", "/"),
        "change": {
            "label": "水文短历时暴雨统计表残片",
            "status": status,
            "changed": changed,
            "sources": SOURCES,
        },
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 水文暴雨表残片清理",
        "",
        f"- 时间：{now}",
        f"- 范围：`{HTML.relative_to(ROOT)}`。",
        "- 处理：删除表1-21短历时暴雨统计表在正文流中残留的表头、数字串和站名碎片，恢复源页两条注释，保留其后表1-22结构化表。",
        "",
        "## 结果",
        "",
        f"- 水文短历时暴雨统计表残片：{status}，本次变更 {changed}",
    ]
    for source in SOURCES:
        lines.append(f"  - `{source}`")
    text = "\n".join(lines) + "\n"
    REPORT_MD.write_text(text, encoding="utf-8")
    PROGRESS.write_text(text, encoding="utf-8")

    marker = "## 2026-07-05 水文暴雨表残片清理"
    append_once(
        MEMORY,
        marker,
        f"""
{marker}
- 新增并运行 `scripts/repair_reader_hydrology_rainstorm_table_residue_20260705.py`，清理主阅读版水文段中表1-21短历时暴雨统计表残留的表头/数字串碎片，并按 `workbench/ocr/raw/上/part01/page_0178.txt:163-164` 恢复两条注释。
- 表1-22石梁河水库水位、蓄水量结构化表保留不动。
- 报告：`output/reports/reader_hydrology_rainstorm_table_residue_20260705.md`。
""",
    )

    print("reader_hydrology_rainstorm_table_residue_repaired")
    print(f"changed={changed}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()
