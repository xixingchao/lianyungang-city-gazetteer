# -*- coding: utf-8 -*-
"""Restore remaining source-backed numbered item boundaries in the full reader."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_remaining_item_boundaries_20260705.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_remaining_item_boundaries_20260705.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260705_剩余段首条目边界修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

ITEMS = [
    ("三、东部盐土粮棉区", "位于市境东南部沿海，", "workbench/body_chapters/连云港市志_全书_正文汇总.md:32929-32930", ""),
    ("一、资源", "全市海岸线北起绣针河南至灌河口，", "workbench/body_chapters/连云港市志_全书_正文汇总.md:48088-48089", "同名标题多处，本项按盐业章原盐小节正文首句唯一匹配。"),
    ("一、剪刀", "连云港市剪刀生产始于西汉时期。", "workbench/body_chapters/连云港市志_全书_正文汇总.md:52440-52441; workbench/ocr/raw/上/part03/page_0204.txt:30-32", "源标题为 `一、剪　刀`，reader 规范化为 `一、剪刀`。"),
    ("二、连云港市工艺制品厂", "连云港市工艺制品厂是全市较早从事柳编工艺生产专业的厂家，", "workbench/body_chapters/连云港市志_全书_正文汇总.md:121861-121862", ""),
    ("二、连云港市玻璃制品厂", "连云港市玻璃制品厂为市属集体企业，", "workbench/body_chapters/连云港市志_全书_正文汇总.md:123201-123202", ""),
    ("一、连云港市第一建筑工程公司", "该公司组建于1949年，", "workbench/body_chapters/连云港市志_全书_正文汇总.md:138756-138757; workbench/ocr/raw/中/part01/page_0321.txt:14-17", "源/OCR 标题识别为 `一、连云港市第一一建筑工程公司`，reader 规范化为 `一、连云港市第一建筑工程公司`。"),
    ("二、主要活动", "自身建设九三学社市委委派-一名专职副秘书长，", "workbench/body_chapters/连云港市志_全书_正文汇总.md:89783-89784", "重名标题多处，本项按九三学社正文首句唯一匹配。"),
    ("二、烧龙王纸", "盐民认为潮涨潮落以及海水含盐多少都是龙王的法力。", "workbench/body_chapters/连云港市志_全书_正文汇总.md:106265-106266", ""),
    ("二、孕妇禁忌", "孕妇在日常生活中有严格的俗规：", "workbench/body_chapters/连云港市志_全书_正文汇总.md:106478-106479", ""),
    ("一、订婚", "海属地区婚姻建国前多由“父母之命，媒灼之言”而定，", "workbench/body_chapters/连云港市志_全书_正文汇总.md:106508-106509", ""),
    ("一、连云港市发展的初步设想", "我市地理位置优越，", "workbench/body_chapters/连云港市志_全书_正文汇总.md:118370-118371", ""),
]


def append_once(path: Path, marker: str, content: str) -> None:
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker not in old:
        path.write_text(old.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")


def main() -> None:
    html = HTML.read_text(encoding="utf-8")
    changes = []
    for title, lead, source, note in ITEMS:
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
        changes.append({"label": title, "status": status, "changed": changed, "source": source, "note": note})

    HTML.write_text(html, encoding="utf-8")

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {"time": now, "target": str(HTML.relative_to(ROOT)).replace("\\", "/"), "changes": changes}
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 剩余段首条目边界修复",
        "",
        f"- 时间：{now}",
        f"- 范围：`{HTML.relative_to(ROOT)}`。",
        "- 处理：按正文汇总/OCR 独立分行恢复剩余 11 处段首编号条目标题边界，仅拆标题，不改正文文字。",
        "",
        "## 结果",
        "",
    ]
    for change in changes:
        lines.append(f"- {change['label']}：{change['status']}，本次变更 {change['changed']}")
        lines.append(f"  - `{change['source']}`")
        if change["note"]:
            lines.append(f"  - 说明：{change['note']}")
    text = "\n".join(lines) + "\n"
    REPORT_MD.write_text(text, encoding="utf-8")
    PROGRESS.write_text(text, encoding="utf-8")

    marker = "## 2026-07-05 剩余段首条目边界修复"
    append_once(
        MEMORY,
        marker,
        f"""
{marker}
- 新增并运行 `scripts/repair_reader_remaining_item_boundaries_20260705.py`，按 `workbench/body_chapters/连云港市志_全书_正文汇总.md` 与必要 OCR 证据恢复剩余 11 处段首编号条目标题边界。
- 覆盖：`三、东部盐土粮棉区`、盐业章 `一、资源`、`一、剪刀`、`二、连云港市工艺制品厂`、`二、连云港市玻璃制品厂`、`一、连云港市第一建筑工程公司`、九三学社 `二、主要活动`、`二、烧龙王纸`、`二、孕妇禁忌`、`一、订婚`、`一、连云港市发展的初步设想`。
- 特别说明：`一、剪刀` 源标题含全角空格；`一、连云港市第一建筑工程公司` 源/OCR 题名多识别一个“一”；`一、资源`、`二、主要活动` 为重名标题，本轮按正文首句唯一匹配。
- 报告：`output/reports/reader_remaining_item_boundaries_20260705.md`。
""",
    )

    print("reader_remaining_item_boundaries_repaired")
    print(f"changed={sum(change['changed'] for change in changes)}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()
