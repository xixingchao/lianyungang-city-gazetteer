# -*- coding: utf-8 -*-
"""Remove source-backed education expense table residues from the final reader."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_education_expense_table_residues_20260705.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_education_expense_table_residues_20260705.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260705_教育经费表格残片清理.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    {
        "label": "表50-23 教育行政业务费支出标准表尾残片",
        "old": (
            "<p>学轮训幼儿园职干部班(每各类会生每学校轮调月）</p>\n"
            "<p>计人员项目城镇中学1至5班7至2班2班以上每人每月重点中学重点中学普通中学农村中学每人每月1.5元每班月定额14元每班月定额2元另加旧1.8元每学期生维持另自行车单独办公费0.720.630.540.860.770.20修理费每费每生造预算3.5全年5辆月2元每班每学期图书费4元医药按事业每班每学期卫生编制情3元茶水费况临时教学及增加预每班每月教学实3元验费1971年，市文教局规定小学图书、医药、茶水、教学费（包括上缴杂费的民小、耕小)每班标准10元。</p>"
        ),
        "new": "<p>1971年，市文教局规定小学图书、医药、茶水、教学费（包括上缴杂费的民小、耕小)每班标准10元。</p>",
        "sources": [
            "workbench/ocr/paddle_ocr/下/part01/page_0412.txt:4-82",
            "workbench/ocr/raw/下/part01/page_0413.txt:83-86",
        ],
    },
    {
        "label": "表50-24 教育事业费支出和基建投资完成情况表尾残片",
        "old": (
            "<p>106.40省补助专项经费343.38县区财政414.30404.75273.79337.18（万元）</p>\n"
            "<p>拨140.00137.90用于职教市地方机动财力75.0060.00245.00一无两有”（万元）</p>\n"
            "<p>教工住宅资（万元）</p>\n\n\n"
            "<p>90.00省基建款（万元）</p>\n\n\n\n"
            "<p>二、集资办学1980年，国家教委提出多渠道集资办学，尽快实现“校校无危房、班班有教室、学生人人有课桌凳”的“一无两有”基本要求，市、县政府和各级教育行政部门发动乡镇、企事业单位集资办学，改善办学条件。经过6年的努力，1986年完成“一无两有”工作。</p>"
        ),
        "new": (
            "<h5>二、集资办学</h5>\n"
            "<p>1980年，国家教委提出多渠道集资办学，尽快实现“校校无危房、班班有教室、学生人人有课桌凳”的“一无两有”基本要求，市、县政府和各级教育行政部门发动乡镇、企事业单位集资办学，改善办学条件。经过6年的努力，1986年完成“一无两有”工作。</p>"
        ),
        "sources": [
            "workbench/ocr/paddle_ocr/下/part01/page_0413.txt:6-89",
            "workbench/ocr/raw/下/part01/page_0413.txt:6-84",
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
        count = html.count(item["old"])
        if count == 1:
            html = html.replace(item["old"], item["new"], 1)
            status = "changed"
            changed = 1
        elif count == 0 and item["new"] in html:
            status = "already_applied"
            changed = 0
        else:
            raise RuntimeError(f"expected {item['label']} once, got {count}")
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
        "notes": "仅清理表格残片并恢复源页明确正文/小题边界；未重建表50-23、表50-24结构化表。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 教育经费表格残片清理",
        "",
        f"- 时间：{now}",
        f"- 范围：`{HTML.relative_to(ROOT)}` 第五十卷教育经费段。",
        "- 处理：删除表50-23、表50-24 的正文流压扁残片，保留并恢复源页明确的正文起点。",
        "- 说明：本批不重建结构化表，仅解决阅读版正文夹杂表格残片的问题。",
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

    marker = "## 2026-07-05 教育经费表格残片清理"
    append_once(
        MEMORY,
        marker,
        f"""
{marker}
- 新增并运行 `scripts/repair_reader_education_expense_table_residues_20260705.py`，据下册 part01 第 412、413 页 OCR 清理第五十卷教育经费段 2 处表格残片：表50-23 尾部压扁表头/数值、表50-24 尾部压扁数值。
- 恢复正文边界：保留 `1971年，市文教局规定...` 段落，并将 `二、集资办学` 拆为小题。
- 本批不重建结构化表，只处理阅读版正文夹杂表格残片。
- 报告：`output/reports/reader_education_expense_table_residues_20260705.md`。
""",
    )

    print("reader_education_expense_table_residues_repaired")
    print(f"changed={sum(item['changed'] for item in changes)}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()
