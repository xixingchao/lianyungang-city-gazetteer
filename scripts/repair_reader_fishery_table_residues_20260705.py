# -*- coding: utf-8 -*-
"""Remove source-backed fishery table residues from the full reader."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_fishery_table_residues_20260705.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_fishery_table_residues_20260705.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260705_水产表格残片清理.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    {
        "label": "对虾放流表尾残片粘海参增殖",
        "old": (
            "<p>苗量（万尾）</p>\n"
            "<p>流量（万尾）</p>\n"
            "<p>（吨）</p>\n"
            "<p>苗量（万尾）</p>\n"
            "<p>流量（万尾）</p>\n"
            "<p>10000130006.0100201.05.1三、海参增殖1976年，市海带育苗场人工育出刺参大耳幼体30万头，投放前三岛附近海域增殖。</p>\n"
        ),
        "new": (
            "<h5>三、海参增殖</h5>\n"
            "<p>1976年，市海带育苗场人工育出刺参大耳幼体30万头，投放前三岛附近海域增殖。</p>\n"
        ),
        "sources": [
            "workbench/ocr/raw/上/part03/page_0116.txt:26-65",
            "workbench/ocr/raw/上/part03/page_0116.txt:66-68",
            "workbench/ocr/paddle_ocr/上/part03/page_0116.txt:26-67",
        ],
    },
    {
        "label": "海带制品产量表尾残片粘紫菜",
        "old": (
            "<p>年份产量（吨）</p>\n"
            "<p>年份产量（吨）</p>\n"
            "<p>0.5211935114671321912910四、紫菜连云港紫菜在古代即列为贡品。自然生长的鲜紫菜数量极少，不能形成批量生产。</p>\n"
        ),
        "new": (
            "<h5>四、紫菜</h5>\n"
            "<p>连云港紫菜在古代即列为贡品。自然生长的鲜紫菜数量极少，不能形成批量生产。</p>\n"
        ),
        "sources": [
            "workbench/ocr/raw/上/part03/page_0119.txt:14-87",
            "workbench/ocr/raw/上/part03/page_0119.txt:88-95",
            "workbench/ocr/paddle_ocr/上/part03/page_0119.txt:13-89",
        ],
    },
]


def append_once(path: Path, marker: str, content: str) -> None:
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker not in old:
        path.write_text(old.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")


def main() -> None:
    html = HTML.read_text(encoding="utf-8")
    changes = []
    for item in REPLACEMENTS:
        old_count = html.count(item["old"])
        if old_count == 1:
            html = html.replace(item["old"], item["new"], 1)
            status = "changed"
            changed = 1
        elif old_count == 0 and html.count(item["new"]) >= 1:
            status = "already_applied"
            changed = 0
        else:
            raise RuntimeError(f"expected {item['label']} once, got {old_count}")
        changes.append({
            "label": item["label"],
            "status": status,
            "changed": changed,
            "sources": item["sources"],
        })

    HTML.write_text(html, encoding="utf-8")

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "target": str(HTML.relative_to(ROOT)).replace("\\", "/"),
        "changes": changes,
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 水产表格残片清理",
        "",
        f"- 时间：{now}",
        f"- 范围：`{HTML.relative_to(ROOT)}`。",
        "- 处理：删除水产章中表12-9、表12-10残留在正文流里的表头和数字串，恢复 `三、海参增殖`、`四、紫菜` 小节边界。",
        "",
        "## 结果",
        "",
    ]
    for change in changes:
        lines.append(f"- {change['label']}：{change['status']}，本次变更 {change['changed']}")
        for source in change["sources"]:
            lines.append(f"  - `{source}`")
    text = "\n".join(lines) + "\n"
    REPORT_MD.write_text(text, encoding="utf-8")
    PROGRESS.write_text(text, encoding="utf-8")

    marker = "## 2026-07-05 水产表格残片清理"
    append_once(
        MEMORY,
        marker,
        f"""
{marker}
- 新增并运行 `scripts/repair_reader_fishery_table_residues_20260705.py`，清理主阅读版水产章两处表格残片：表12-9对虾放流量与捕获量对照表尾粘 `三、海参增殖`，表12-10海带制品产量统计表尾粘 `四、紫菜`。
- 源页证据：`workbench/ocr/raw/上/part03/page_0116.txt:26-68`、`workbench/ocr/raw/上/part03/page_0119.txt:14-95`，并用对应 Paddle OCR 互证。
- 报告：`output/reports/reader_fishery_table_residues_20260705.md`。
""",
    )

    print("reader_fishery_table_residues_repaired")
    print(f"changed={sum(item['changed'] for item in changes)}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()
