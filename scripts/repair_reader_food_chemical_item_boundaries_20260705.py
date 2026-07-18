# -*- coding: utf-8 -*-
"""Restore source-backed food and chemical item boundaries in the full reader."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_food_chemical_item_boundaries_20260705.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_food_chemical_item_boundaries_20260705.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260705_食品化工条目边界修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

ITEMS = [
    ("七、青岛食品厂石桥联营厂", "该厂位于赣榆县石桥镇驻地，为镇属企业。", "workbench/body_chapters/连云港市志_全书_正文汇总.md:124017-124018"),
    ("三、东海县肉类联合加工厂", "该厂位于东海县牛山镇钢铁路63号，为县属全民企业。", "workbench/body_chapters/连云港市志_全书_正文汇总.md:124293"),
    ("四、灌云县肉类联合加工厂", "该厂位于灌云县伊山镇胜利路东南首，为县属全民企业。", "workbench/body_chapters/连云港市志_全书_正文汇总.md:124304"),
    ("三、赣榆县酿造厂", "该厂位于赣榆县青口镇黄海路69号，为县属全民所有制企业。", "workbench/body_chapters/连云港市志_全书_正文汇总.md:126085"),
    ("五、连云港市酶制剂厂", "该厂位于连云港市海州幸福路52号，为市属全民所有制企业。", "workbench/body_chapters/连云港市志_全书_正文汇总.md:126121"),
    ("二、重点产品简介", "药用磷酸氢钙1964年，连云港市红旗化工厂试制。", "workbench/body_chapters/连云港市志_全书_正文汇总.md:127158"),
    ("三、连云港市海水化工一厂", "该厂始建于1958年，原为连云区鱼粉加工厂。", "workbench/body_chapters/连云港市志_全书_正文汇总.md:130304-130305"),
    ("四、江苏省盐业公司黄海化工厂", "该厂为从事海水综合利用的中型全民化工企业。", "workbench/body_chapters/连云港市志_全书_正文汇总.md:130322-130323"),
    ("五、连云港市化工厂", "该厂前身为1965年3月筹建的新浦农药厂。", "workbench/body_chapters/连云港市志_全书_正文汇总.md:130333-130334"),
    ("十一、南京化学工业（集团）公司连云港碱厂", "该厂原称江苏连云港碱厂，全民企业，国家七五”期间重点项目，", "workbench/body_chapters/连云港市志_全书_正文汇总.md:130416-130417"),
    ("三、赣榆县化肥总厂", "该厂始建于1966年4月。", "workbench/body_chapters/连云港市志_全书_正文汇总.md:131045-131046"),
    ("六、连云港市第二农药厂", "该厂原为建于1965年的连云港市综合化工厂，为市属全民企业。", "workbench/body_chapters/连云港市志_全书_正文汇总.md:131086-131087"),
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
        "# 食品化工条目边界修复",
        "",
        f"- 时间：{now}",
        f"- 范围：`{HTML.relative_to(ROOT)}`。",
        "- 处理：按正文汇总独立分行恢复食品工业、医药、化学工业 12 处产品/企业条目标题边界，仅拆标题，不改正文文字。",
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

    marker = "## 2026-07-05 食品化工条目边界修复"
    append_once(
        MEMORY,
        marker,
        f"""
{marker}
- 新增并运行 `scripts/repair_reader_food_chemical_item_boundaries_20260705.py`，按 `workbench/body_chapters/连云港市志_全书_正文汇总.md` 独立分行恢复食品工业、医药、化学工业 12 处产品/企业条目标题边界。
- 覆盖：`七、青岛食品厂石桥联营厂`、`三、东海县肉类联合加工厂`、`四、灌云县肉类联合加工厂`、`三、赣榆县酿造厂`、`五、连云港市酶制剂厂`、`二、重点产品简介`、`三、连云港市海水化工一厂`、`四、江苏省盐业公司黄海化工厂`、`五、连云港市化工厂`、`十一、南京化学工业（集团）公司连云港碱厂`、`三、赣榆县化肥总厂`、`六、连云港市第二农药厂`。
- 报告：`output/reports/reader_food_chemical_item_boundaries_20260705.md`。
""",
    )

    print("reader_food_chemical_item_boundaries_repaired")
    print(f"changed={sum(change['changed'] for change in changes)}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()
