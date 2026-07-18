# -*- coding: utf-8 -*-
"""Remove source-backed insurance claims table residue from the full reader."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_insurance_claims_table_residue_20260705.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_insurance_claims_table_residue_20260705.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260705_保险赔案表残片清理.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

OLD = (
    "<p>1520880.00企业财产保险14766机动车辆保险2594.801214.002030拖拉机保险1005货物运输保险137.501067船舶保险272.5025213485. 10"
    "家庭财产保险1147农业保险131.20467485715.10三、主要案例1985年8月19日晚，连云港海运分公司503号驳船载500吨水泥停靠在连云港庙岭"
    "新建码头南侧泊位待卸，20日因风雨交加致使该船船体与码头水下部分伸出螺杆碰撞，造成左航载重水线下船壳板60多处损坏，"
    "于当日沉没，所载水泥全部报废，驳船修复费14万元，市保险公司共赔付连云港海运分公司503驳船沉海案费用21.56万元。</p>\n"
)

NEW = (
    "<h5>三、主要案例</h5>\n"
    "<p>1985年8月19日晚，连云港海运分公司503号驳船载500吨水泥停靠在连云港庙岭新建码头南侧泊位待卸，"
    "20日因风雨交加致使该船船体与码头水下部分伸出螺杆碰撞，造成左航载重水线下船壳板60多处损坏，"
    "于当日沉没，所载水泥全部报废，驳船修复费14万元，市保险公司共赔付连云港海运分公司503驳船沉海案费用21.56万元。</p>\n"
)

SOURCES = [
    "workbench/ocr/raw/中/part02/page_0384.txt:12-39",
    "workbench/ocr/raw/中/part02/page_0384.txt:40-44",
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
        raise RuntimeError(f"expected insurance claims table residue once, got {old_count}")

    HTML.write_text(html, encoding="utf-8")

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "target": str(HTML.relative_to(ROOT)).replace("\\", "/"),
        "change": {
            "label": "保险赔案统计表残片",
            "status": status,
            "changed": changed,
            "sources": SOURCES,
        },
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 保险赔案表残片清理",
        "",
        f"- 时间：{now}",
        f"- 范围：`{HTML.relative_to(ROOT)}`。",
        "- 处理：删除表40-16国内财产保险主要险种赔款支出统计表在正文流中的表尾数字串，恢复 `三、主要案例` 小标题和首段案例正文。",
        "",
        "## 结果",
        "",
        f"- 保险赔案统计表残片：{status}，本次变更 {changed}",
    ]
    for source in SOURCES:
        lines.append(f"  - `{source}`")
    text = "\n".join(lines) + "\n"
    REPORT_MD.write_text(text, encoding="utf-8")
    PROGRESS.write_text(text, encoding="utf-8")

    marker = "## 2026-07-05 保险赔案表残片清理"
    append_once(
        MEMORY,
        marker,
        f"""
{marker}
- 新增并运行 `scripts/repair_reader_insurance_claims_table_residue_20260705.py`，清理主阅读版保险业务章中表40-16表尾数字串粘 `三、主要案例` 的残片。
- 源页证据：`workbench/ocr/raw/中/part02/page_0384.txt:12-44`。
- 报告：`output/reports/reader_insurance_claims_table_residue_20260705.md`。
""",
    )

    print("reader_insurance_claims_table_residue_repaired")
    print(f"changed={changed}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()
