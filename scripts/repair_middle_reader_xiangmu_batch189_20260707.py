# -*- coding: utf-8 -*-
"""Sync middle-reader 项目 OCR residues from current full reader evidence."""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MIDDLE = ROOT / "output" / "final_reader" / "连云港市志_中册.html"
FULL = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "middle_reader_xiangmu_batch189_20260707.json"
REPORT_MD = ROOT / "output" / "reports" / "middle_reader_xiangmu_batch189_20260707.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260707_中册项目残字补修第一百八十九批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    ("画框条生产线项自工试产", "画框条生产线项目竣工试产"),
    ("该项自由扬州", "该项目由扬州"),
    ("氯化钾、氯化镁、漠素等项自", "氯化钾、氯化镁、漠素等项目"),
    ("技术引进和技术改造项自完成", "技术引进和技术改造项目完成"),
    ("国家优秀项自奖", "国家优秀项目奖"),
    ("啤酒广安装项自有", "啤酒厂安装项目有"),
    ("一般项自有定额", "一般项目有定额"),
    ("“三资”项自和", "“三资”项目和"),
    ("投资过1000万美元的项自", "投资过1000万美元的项目"),
    ("投资过500万美元的项自", "投资过500万美元的项目"),
    ("狠抓项自、资金", "狠抓项目、资金"),
    ("开发区项自引进", "开发区项目引进"),
    ("重点建设项自之一", "重点建设项目之一"),
    ("对项自进行解除", "对项目进行解除"),
    ("项自批件", "项目批件"),
    ("时间长的项自", "时间长的项目"),
    ("经审定批准项自", "经审定批准项目"),
    ("这是一项自动控制多，自动点安装的设备", "这是一项自动控制多，自动化程度很高的全新中外合资的工程"),
]

FULL_EVIDENCE = [
    "画框条生产线项目竣工试产",
    "该项目由扬州",
    "氯化钾、氯化镁、溴素等项目",
    "技术引进和技术改造项目完成",
    "啤酒厂安装项目有",
    "一般项目有定额",
    "投资过1000万美元的项目",
    "项目、资金的引进",
    "开发区项目引进",
    "项目批件",
    "经审定批准项目",
    "这是一项自动控制多，自动化程度很高的全新中外合资的工程",
]


def plain(html: str) -> str:
    return re.sub(r"<[^>]+>", "", html)


def upsert_memory(total: int, remaining: int) -> None:
    marker = "## 2026-07-07 高置信 OCR 错字补修第一百八十九批：中册项目残字"
    old = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    block = f"""
{marker}

- 复核 `项自` 残留：当前全书 reader 对应段多已为 `项目`，中册 reader 残留 `项自` 属分册同步缺口；全书合法 `这是一项自动...` 保留。
- 已仅在 `output/final_reader/连云港市志_中册.html` 定点修复项目语境和一处同段漏句，合计 {total} 处；报告：`output/reports/middle_reader_xiangmu_batch189_20260707.md`。
- 修后当前中册纯文本 `项自` 剩余 {remaining} 处；未打开、展示或嵌入图片。
""".strip()
    if marker not in old:
        MEMORY.write_text(old.rstrip() + "\n\n" + block + "\n", encoding="utf-8")
        return
    start = old.index(marker)
    next_start = old.find("\n## ", start + 1)
    new = old[:start].rstrip() + "\n\n" + block + "\n"
    if next_start != -1:
        new += "\n" + old[next_start:].lstrip()
    MEMORY.write_text(new, encoding="utf-8")


def main() -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    full = FULL.read_text(encoding="utf-8")
    full_text = plain(full)
    evidence_counts = {term: full_text.count(term) for term in FULL_EVIDENCE}
    if evidence_counts["这是一项自动控制多，自动化程度很高的全新中外合资的工程"] != 1:
        raise SystemExit("full reader evidence for 自动化程度句 not unique")

    before = MIDDLE.read_text(encoding="utf-8")
    before_text = plain(before)
    after = before
    changed_items = []
    for old, new in REPLACEMENTS:
        count = after.count(old)
        if count:
            after = after.replace(old, new)
            changed_items.append({"old": old, "new": new, "changed": count})
    MIDDLE.write_text(after, encoding="utf-8")
    after_text = plain(after)
    total = sum(item["changed"] for item in changed_items)

    payload = {
        "time": now,
        "scope": "middle reader 项目 OCR repair using current full reader evidence",
        "changed": total,
        "before_plain_xiangzi": before_text.count("项自"),
        "after_plain_xiangzi": after_text.count("项自"),
        "full_evidence_counts": evidence_counts,
        "replacements": changed_items,
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 中册项目残字补修第一百八十九批",
        "",
        f"> 生成时间：{now}",
        "",
        "## 范围",
        "",
        "- 当前中册阅读稿。",
        "- 以当前全书 reader 对应正确段落为证据，修复中册 `项自` 对 `项目` 的同步缺口。",
        "- 保留全书合法 `这是一项自动...`；未做全局单字替换；未打开、展示或嵌入图片。",
        "",
        "## 统计",
        "",
        f"- 修复：{total} 处",
        f"- 中册纯文本 `项自`：{before_text.count('项自')} -> {after_text.count('项自')}",
        "",
        "## 替换项",
        "",
    ]
    for item in changed_items:
        lines.append(f"- `{item['old']}` -> `{item['new']}`：{item['changed']} 处")
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    PROGRESS.write_text(REPORT_MD.read_text(encoding="utf-8"), encoding="utf-8")
    upsert_memory(total, after_text.count("项自"))
    print(json.dumps({"changed": total, "middle_xiangzi_remaining": after_text.count("项自"), "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
