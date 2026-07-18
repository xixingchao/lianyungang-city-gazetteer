# -*- coding: utf-8 -*-
"""Final middle-reader 项目 OCR follow-up after batch190."""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MIDDLE = ROOT / "output" / "final_reader" / "连云港市志_中册.html"
REPORT_JSON = ROOT / "output" / "reports" / "middle_reader_xiangmu_followup_batch191_20260707.json"
REPORT_MD = ROOT / "output" / "reports" / "middle_reader_xiangmu_followup_batch191_20260707.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260707_中册项目残字补遗第一百九十一批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    ("项自由扬州", "项目由扬州"),
    ("项</p><p>自完成", "项目</p><p>完成"),
    ("狠抓项</p><p>自、资金", "狠抓项目</p><p>、资金"),
    ("的项</p><p>自，或者属于能源", "的项目</p><p>，或者属于能源"),
]


def plain(html: str) -> str:
    return re.sub(r"<[^>]+>", "", html)


def upsert_memory(total: int, remaining: int) -> None:
    marker = "## 2026-07-07 高置信 OCR 错字补修第一百九十一批：中册项目残字补遗"
    old = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    block = f"""
{marker}

- 复扫 batch190 后，中册 `项自` 仅余 4 处项目误识和 1 处合法 `这是一项自动...`。
- 已补修 `项目由扬州/技术引进和技术改造项目完成/狠抓项目、资金/回收投资时间长的项目` 4 处；报告：`output/reports/middle_reader_xiangmu_followup_batch191_20260707.md`。
- 修后当前中册纯文本 `项自` 剩余 {remaining} 处，为合法 `这是一项自动...`；未打开、展示或嵌入图片。
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
        "changed": total,
        "before_plain_xiangzi": before_text.count("项自"),
        "after_plain_xiangzi": after_text.count("项自"),
        "remaining_is_legal_auto": after_text.count("这是一项自动控制多，自动化程度很高的全新中外合资的工程"),
        "replacements": changed_items,
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# 中册项目残字补遗第一百九十一批",
        "",
        f"> 生成时间：{now}",
        "",
        "## 范围",
        "",
        "- 当前中册阅读稿。",
        "- 修复 batch190 后剩余项目语境 `项自`；保留合法 `这是一项自动...`。",
        "- 未做全局单字替换；未打开、展示或嵌入图片。",
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
