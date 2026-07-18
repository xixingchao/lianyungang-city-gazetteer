# -*- coding: utf-8 -*-
"""Restore source-backed tourism and scenic-site item boundaries."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_tourism_scenic_item_boundaries_20260705.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_tourism_scenic_item_boundaries_20260705.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260705_旅游名胜条目边界修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

ITEMS = [
    ("十二、凤凰山", "凤凰山是南云台山的南缘，", "workbench/body_chapters/连云港市志_全书_正文汇总.md:63720-63721"),
    ("三、保驾山", "保驾山紧靠宿城水库东南侧。", "workbench/body_chapters/连云港市志_全书_正文汇总.md:63749-63750"),
    ("四、船山飞瀑", "船山飞瀑在宿城山东北部，", "workbench/body_chapters/连云港市志_全书_正文汇总.md:63758-63759"),
    ("三、曲阳古城", "曲阳古城在东海县西南的曲阳乡。", "workbench/body_chapters/连云港市志_全书_正文汇总.md:64045-64046"),
    ("七、抗日山烈士陵园", "陵园在赣榆县夹山乡境内，", "workbench/body_chapters/连云港市志_全书_正文汇总.md:64075-64076"),
    ("八、新石器时代石棺群", "位于灌云县伊山镇北500米处的老龙涧山麓，", "workbench/body_chapters/连云港市志_全书_正文汇总.md:64081-64082"),
    ("九、伊庐山", "伊庐山在灌云县城东北，", "workbench/body_chapters/连云港市志_全书_正文汇总.md:64086-64087"),
    ("四、连云港市科技活动中心", "位于连云港市墟沟镇海棠路西的北山腰，", "workbench/body_chapters/连云港市志_全书_正文汇总.md:64143-64144"),
    ("五、连云港远洋宾馆", "位于连云港市墟沟镇东3公里。", "workbench/body_chapters/连云港市志_全书_正文汇总.md:64150-64151"),
    ("三、市境内主要旅游路线", "市境内有三条主要旅游路线，", "workbench/body_chapters/连云港市志_全书_正文汇总.md:64213-64214"),
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
        "# 旅游名胜条目边界修复",
        "",
        f"- 时间：{now}",
        f"- 范围：`{HTML.relative_to(ROOT)}`。",
        "- 处理：按正文汇总独立分行恢复旅游、名胜 10 处条目标题边界，仅拆标题，不改正文文字。",
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

    marker = "## 2026-07-05 旅游名胜条目边界修复"
    append_once(
        MEMORY,
        marker,
        f"""
{marker}
- 新增并运行 `scripts/repair_reader_tourism_scenic_item_boundaries_20260705.py`，按 `workbench/body_chapters/连云港市志_全书_正文汇总.md` 独立分行恢复旅游、名胜 10 处条目标题边界。
- 覆盖：`十二、凤凰山`、`三、保驾山`、`四、船山飞瀑`、`三、曲阳古城`、`七、抗日山烈士陵园`、`八、新石器时代石棺群`、`九、伊庐山`、`四、连云港市科技活动中心`、`五、连云港远洋宾馆`、`三、市境内主要旅游路线`。
- 报告：`output/reports/reader_tourism_scenic_item_boundaries_20260705.md`。
""",
    )

    print("reader_tourism_scenic_item_boundaries_repaired")
    print(f"changed={sum(change['changed'] for change in changes)}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()
