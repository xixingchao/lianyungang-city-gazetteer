# -*- coding: utf-8 -*-
"""Restore source-backed governance, labor, women and education item boundaries."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_governance_labor_women_education_item_boundaries_20260705.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_governance_labor_women_education_item_boundaries_20260705.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260705_政务人事妇教条目边界修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

ITEMS = [
    ("一、灌云县各界人民代表会议", "从1950年1月至1954年2月，", "workbench/body_chapters/连云港市志_全书_正文汇总.md:91877-91878"),
    ("二、离退休军队干部安置和管理", "1981年，连云港市成立军队退休干部安置领导小组。", "workbench/body_chapters/连云港市志_全书_正文汇总.md:150915-150916"),
    ("三、军队转业干部家属随迁调动", "建国后至70年代初，", "workbench/body_chapters/连云港市志_全书_正文汇总.md:163733-163734"),
    ("五、等级工资制", "在抗日根据地和解放区内的军工企业，", "workbench/body_chapters/连云港市志_全书_正文汇总.md:164281-164282"),
    ("一、企业民主管理", "民主改革运动解放初期，", "workbench/body_chapters/连云港市志_全书_正文汇总.md:166648-166649"),
    ("四、职工教育培训", "民国38年（1949年）7月9日，", "workbench/body_chapters/连云港市志_全书_正文汇总.md:166805-166806"),
    ("一、市区妇女组织", "民国17年（1928年）初，", "workbench/body_chapters/连云港市志_全书_正文汇总.md:167263-167264"),
    ("二、支援人民战争", "民国27年（1938年）2月，", "workbench/body_chapters/连云港市志_全书_正文汇总.md:167384-167385"),
    ("三、促进生产劳动", "民国31年（1942年）初，", "workbench/body_chapters/连云港市志_全书_正文汇总.md:167432-167433"),
    ("三、文昭学堂", "清光绪三十一年（1905年），", "workbench/body_chapters/连云港市志_全书_正文汇总.md:168125-168126"),
    ("五、精勤学堂", "清光绪三十二年（1906年），", "workbench/body_chapters/连云港市志_全书_正文汇总.md:168132-168133"),
    ("二、培智学校", "1986年在新浦南极路小学办起了全市第一个培智班。", "workbench/body_chapters/连云港市志_全书_正文汇总.md:169849-169850"),
    ("一、教育研究机构", "民国11年（1922年），", "workbench/body_chapters/连云港市志_全书_正文汇总.md:172829-172830"),
]


def append_once(path: Path, marker: str, content: str) -> None:
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker not in old:
        path.write_text(old.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")


def main() -> None:
    html = HTML.read_text(encoding="utf-8")
    changes = []
    for title, lead, source in ITEMS:
        old = f"<p>{title}{lead}"
        new = f"<h5>{title}</h5>\n<p>{lead}"
        old_count = html.count(old)
        if old_count == 1:
            html = html.replace(old, new, 1)
            status = "changed"
            changed = 1
        elif old_count == 0 and html.count(new) >= 1:
            status = "already_applied"
            changed = 0
        else:
            raise RuntimeError(f"expected {title} once, got {old_count}")
        changes.append({"label": title, "status": status, "changed": changed, "source": source})

    HTML.write_text(html, encoding="utf-8")

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {"time": now, "target": str(HTML.relative_to(ROOT)).replace("\\", "/"), "changes": changes}
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 政务人事妇教条目边界修复",
        "",
        f"- 时间：{now}",
        f"- 范围：`{HTML.relative_to(ROOT)}`。",
        "- 处理：按正文汇总独立分行恢复政务、人事劳动、妇女、教育 13 处条目标题边界，仅拆标题，不改正文文字。",
        "- 跳过：`二、主要活动` 重名较多，需单独定位上下文后再处理。",
        "",
        "## 结果",
        "",
    ]
    for change in changes:
        lines.append(f"- {change['label']}：{change['status']}，本次变更 {change['changed']}")
        lines.append(f"  - `{change['source']}`")
    text = "\n".join(lines) + "\n"
    REPORT_MD.write_text(text, encoding="utf-8")
    PROGRESS.write_text(text, encoding="utf-8")

    marker = "## 2026-07-05 政务人事妇教条目边界修复"
    append_once(
        MEMORY,
        marker,
        f"""
{marker}
- 新增并运行 `scripts/repair_reader_governance_labor_women_education_item_boundaries_20260705.py`，按 `workbench/body_chapters/连云港市志_全书_正文汇总.md` 独立分行恢复政务、人事劳动、妇女、教育 13 处条目标题边界。
- 覆盖：`一、灌云县各界人民代表会议`、`二、离退休军队干部安置和管理`、`三、军队转业干部家属随迁调动`、`五、等级工资制`、`一、企业民主管理`、`四、职工教育培训`、`一、市区妇女组织`、`二、支援人民战争`、`三、促进生产劳动`、`三、文昭学堂`、`五、精勤学堂`、`二、培智学校`、`一、教育研究机构`。
- `二、主要活动` 重名较多，本轮保守跳过，后续按上下文单独处理。
- 报告：`output/reports/reader_governance_labor_women_education_item_boundaries_20260705.md`。
""",
    )

    print("reader_governance_labor_women_education_item_boundaries_repaired")
    print(f"changed={sum(change['changed'] for change in changes)}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()
