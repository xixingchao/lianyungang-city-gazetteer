# -*- coding: utf-8 -*-
"""Remove source-backed welfare enterprise table residues from the final reader."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_welfare_enterprise_table_residues_20260705.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_welfare_enterprise_table_residues_20260705.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260705_福利企业表格残片清理.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

OLD = (
    "<p>（万元）</p>\n"
    "<p>人数（人）</p>\n\n"
    "<p>2、残疾职工累计数不含正常减员。</p>\n\n"
    "<p>156996025年利润额（万元）</p>\n"
    "<p>街道分做安置1536“四残\"人员数（人）</p>\n\n\n"
    "<p>连云港市卷尺厂22430124.3774.96302.70|500.00188105（市合成树脂厂）</p>"
)

SOURCES = [
    "output/final_reader/连云港市志_全书.html:18649-18658",
    "workbench/ocr/paddle_ocr/下/part01/page_0043.txt:4-170",
    "workbench/ocr/paddle_ocr/下/part01/page_0044.txt:4-45",
    "workbench/ocr/raw/下/part01/page_0044.txt:6-42",
]


def append_once(path: Path, marker: str, content: str) -> None:
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker not in old:
        path.write_text(old.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")


def main() -> None:
    html = HTML.read_text(encoding="utf-8")
    count = html.count(OLD)
    if count == 1:
        html = html.replace(OLD, "", 1)
        status = "changed"
        changed = 1
    elif count == 0 and "连云港市卷尺厂22430124" not in html and "156996025年利润额" not in html:
        status = "already_applied"
        changed = 0
    else:
        raise RuntimeError(f"expected welfare table residue once, got {count}")
    HTML.write_text(html, encoding="utf-8")

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "target": str(HTML.relative_to(ROOT)).replace("\\", "/"),
        "status": status,
        "changed": changed,
        "sources": SOURCES,
        "notes": "仅撤出第四十三卷社会福利生产末尾可见表格残片；未重建表43-9/43-10。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 福利企业表格残片清理",
        "",
        f"- 时间：{now}",
        f"- 范围：`{HTML.relative_to(ROOT)}` 第四十三卷社会福利生产末尾。",
        f"- 结果：{status}，本次变更 {changed}。",
        "- 处理：撤出第六章前表43-9/表43-10压扁残片，包括 `156996025年利润额` 与 `连云港市卷尺厂224...` 残行。",
        "- 说明：本批不重建结构化表，只解决阅读版正文中残片可见问题。",
        "",
        "## 证据",
        "",
    ]
    for source in SOURCES:
        lines.append(f"- `{source}`")
    text = "\n".join(lines) + "\n"
    REPORT_MD.write_text(text, encoding="utf-8")
    PROGRESS.write_text(text, encoding="utf-8")

    marker = "## 2026-07-05 福利企业表格残片清理"
    append_once(
        MEMORY,
        marker,
        f"""
{marker}
- 新增并运行 `scripts/repair_reader_welfare_enterprise_table_residues_20260705.py`，据下册 part01 第 43、44 页 OCR 撤出第四十三卷社会福利生产末尾可见表格残片：表43-9 尾部单位/注释残片、表43-10 首行 `连云港市卷尺厂224...` 压扁残片。
- 该残片位于 `第三节效益` 后、`第六章婚姻登记管理` 前；本批只清理阅读版可见残片，不重建结构化表。
- 报告：`output/reports/reader_welfare_enterprise_table_residues_20260705.md`。
""",
    )

    print("reader_welfare_enterprise_table_residues_repaired")
    print(f"changed={changed}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()
