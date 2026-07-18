# -*- coding: utf-8 -*-
"""Restore source-backed commerce, material supply and finance item boundaries."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_commerce_material_finance_item_boundaries_20260705.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_commerce_material_finance_item_boundaries_20260705.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260705_商业物资金融条目边界修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

ITEMS = [
    ("二、连云港市百货大楼", "位于新浦解放中路56号。", "workbench/body_chapters/连云港市志_全书_正文汇总.md:64949-64950"),
    ("七、连云港市食品公司", "位于新浦解放东路59号。", "workbench/body_chapters/连云港市志_全书_正文汇总.md:64986-64987"),
    ("八、连云港市蔬菜公司", "位于新浦南极路108号。", "workbench/body_chapters/连云港市志_全书_正文汇总.md:64996-64997"),
    ("九、连云港市生产资料服务公司", "1978年8月成立，", "workbench/body_chapters/连云港市志_全书_正文汇总.md:77004-77005"),
    ("十二、连云港市物资储运公司", "前身为1977年7月江苏省物资局在连云港兴建的二线储运仓库，", "workbench/body_chapters/连云港市志_全书_正文汇总.md:77022-77023"),
    ("一、物资串换", "是以连云港地产或其他途径获得的优势产品同外地协作串换连云港短缺物资，", "workbench/body_chapters/连云港市志_全书_正文汇总.md:77343-77344"),
    ("十、物资贸易中心仓库", "该仓库共有二处。", "workbench/body_chapters/连云港市志_全书_正文汇总.md:77681-77682"),
    ("一、工业贷款", "国营生产企业贷款解放初期，", "workbench/body_chapters/连云港市志_全书_正文汇总.md:81999-82000"),
    ("九、沿海城市经济技术开发贷款", "1985~1990年，", "workbench/body_chapters/连云港市志_全书_正文汇总.md:82819-82820"),
    ("十、其它类贷款", "购汇人民币贷款1985～1990年，", "workbench/body_chapters/连云港市志_全书_正文汇总.md:82828-82829"),
    ("一、代理发行人民胜利折实公债", "1950年发行人民胜利折实公债，", "workbench/body_chapters/连云港市志_全书_正文汇总.md:83373-83374"),
    ("二、代理发行国家经济建设公债", "1954～1958年连续发行5年。", "workbench/body_chapters/连云港市志_全书_正文汇总.md:83378-83379"),
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
        "# 商业物资金融条目边界修复",
        "",
        f"- 时间：{now}",
        f"- 范围：`{HTML.relative_to(ROOT)}`。",
        "- 处理：按正文汇总独立分行恢复商业、物资、金融 12 处条目标题边界，仅拆标题，不改正文文字。",
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

    marker = "## 2026-07-05 商业物资金融条目边界修复"
    append_once(
        MEMORY,
        marker,
        f"""
{marker}
- 新增并运行 `scripts/repair_reader_commerce_material_finance_item_boundaries_20260705.py`，按 `workbench/body_chapters/连云港市志_全书_正文汇总.md` 独立分行恢复商业、物资、金融 12 处条目标题边界。
- 覆盖：`二、连云港市百货大楼`、`七、连云港市食品公司`、`八、连云港市蔬菜公司`、`九、连云港市生产资料服务公司`、`十二、连云港市物资储运公司`、`一、物资串换`、`十、物资贸易中心仓库`、`一、工业贷款`、`九、沿海城市经济技术开发贷款`、`十、其它类贷款`、`一、代理发行人民胜利折实公债`、`二、代理发行国家经济建设公债`。
- 报告：`output/reports/reader_commerce_material_finance_item_boundaries_20260705.md`。
""",
    )

    print("reader_commerce_material_finance_item_boundaries_repaired")
    print(f"changed={sum(change['changed'] for change in changes)}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()
