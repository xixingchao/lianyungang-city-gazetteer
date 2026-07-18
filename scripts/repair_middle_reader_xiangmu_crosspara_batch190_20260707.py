# -*- coding: utf-8 -*-
"""Repair cross-paragraph middle-reader 项目 OCR residues after batch189."""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MIDDLE = ROOT / "output" / "final_reader" / "连云港市志_中册.html"
REPORT_JSON = ROOT / "output" / "reports" / "middle_reader_xiangmu_crosspara_batch190_20260707.json"
REPORT_MD = ROOT / "output" / "reports" / "middle_reader_xiangmu_crosspara_batch190_20260707.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260707_中册项目跨段残字补修第一百九十批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    ("该项自</p><p>由扬州", "该项目</p><p>由扬州"),
    ("技术引进和技术改造项自</p><p>完成", "技术引进和技术改造项目</p><p>完成"),
    ("这是一项自动控制多，自动</p><p>点安装的设备", "这是一项自动控制多，自动化程度很高的全新中外合资的工程"),
    ("资过1000万美元的项自", "资过1000万美元的项目"),
    ("狠抓项自、资金", "狠抓项目、资金"),
    ("对项自进</p><p>行解除", "对项目进</p><p>行解除"),
    ("时间长的项自", "时间长的项目"),
]


def plain(html: str) -> str:
    return re.sub(r"<[^>]+>", "", html)


def upsert_memory(total: int, remaining: int) -> None:
    marker = "## 2026-07-07 高置信 OCR 错字补修第一百九十批：中册项目跨段补遗"
    old = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    block = f"""
{marker}

- 复扫 batch189 后，中册仍有跨 `<p>` 标签残留 `项自`，包括 `该项目由扬州/技术引进和技术改造项目完成/投资过1000万美元的项目/狠抓项目、资金/对项目进行解除/时间长的项目` 等。
- 已仅在 `output/final_reader/连云港市志_中册.html` 补修 {total} 处，并同步同段 `自动化程度很高的全新中外合资的工程` 漏句；报告：`output/reports/middle_reader_xiangmu_crosspara_batch190_20260707.md`。
- 修后当前中册纯文本 `项自` 剩余 {remaining} 处；全书合法 `这是一项自动...` 保留；未打开、展示或嵌入图片。
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
        "scope": "middle reader cross-paragraph 项目 OCR repair",
        "changed": total,
        "before_plain_xiangzi": before_text.count("项自"),
        "after_plain_xiangzi": after_text.count("项自"),
        "middle_auto_sentence": after_text.count("这是一项自动控制多，自动化程度很高的全新中外合资的工程"),
        "replacements": changed_items,
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 中册项目跨段残字补修第一百九十批",
        "",
        f"> 生成时间：{now}",
        "",
        "## 范围",
        "",
        "- 当前中册阅读稿。",
        "- 修复 batch189 后跨段残留的 `项自` 对 `项目` 的 OCR 误识，并同步同段漏句。",
        "- 未做全局单字替换；未打开、展示或嵌入图片。",
        "",
        "## 统计",
        "",
        f"- 修复：{total} 处",
        f"- 中册纯文本 `项自`：{before_text.count('项自')} -> {after_text.count('项自')}",
        f"- 中册完整自动化句：{after_text.count('这是一项自动控制多，自动化程度很高的全新中外合资的工程')} 处",
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
