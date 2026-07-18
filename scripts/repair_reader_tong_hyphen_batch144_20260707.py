# -*- coding: utf-8 -*-
"""Repair fixed 统- OCR hyphen residues."""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = [
    ROOT / "output" / "final_reader" / "连云港市志_全书.html",
    ROOT / "output" / "final_reader" / "连云港市志_中册.html",
    ROOT / "output" / "final_reader" / "连云港市志_下册.html",
]
REPORT_JSON = ROOT / "output" / "reports" / "reader_tong_hyphen_batch144_20260707.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_tong_hyphen_batch144_20260707.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260707_统一统订连字符残字补修第一百四十四批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    {"label": "统一", "old": "统-一", "new": "统一"},
    {"label": "统订货", "old": "统-订货", "new": "统订货"},
    {"label": "统经营", "old": "统-经营", "new": "统经营"},
]


def plain_text(html: str) -> str:
    return re.sub(r"<[^>]+>", "", html)


def contexts(plain: str, term: str) -> list[str]:
    return [plain[max(0, m.start() - 45):m.start() + 70].replace("\n", " ") for m in re.finditer(term, plain)]


def upsert_memory(marker: str, content: str) -> None:
    old = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker not in old:
        MEMORY.write_text(old.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")
        return
    start = old.index(marker)
    next_start = old.find("\n## ", start + 1)
    new = old[:start].rstrip() + "\n\n" + content.strip() + "\n"
    if next_start != -1:
        new += "\n" + old[next_start:].lstrip()
    MEMORY.write_text(new, encoding="utf-8")


def main() -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    results = []
    for target in TARGETS:
        before = target.read_text(encoding="utf-8")
        before_plain = plain_text(before)
        text = before
        items = []
        for item in REPLACEMENTS:
            count = text.count(item["old"])
            if count:
                text = text.replace(item["old"], item["new"])
            items.append({**item, "count": count})
        target.write_text(text, encoding="utf-8")
        after_plain = plain_text(text)
        results.append({
            "target": str(target),
            "before": before_plain.count("统-"),
            "changed": sum(item["count"] for item in items),
            "after": after_plain.count("统-"),
            "items": items,
            "remaining_contexts": contexts(after_plain, "统-"),
        })

    changed = sum(item["changed"] for item in results)
    payload = {
        "time": now,
        "scope": "current reader fixed 统- hyphen residue repair",
        "changed": changed,
        "targets": results,
        "left_untouched": ["不处理其它连字符或破折号。", "本批没有打开、展示或嵌入图片。"],
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 统一统订连字符残字补修第一百四十四批",
        "",
        f"> 生成时间：{now}",
        "",
        "## 范围",
        "",
        "- 当前全书、中册、下册阅读稿。",
        "- 修复固定语境中的 `统-` 误连字符残留。",
        "",
        "## 统计",
        "",
        f"- 修复：{changed} 处",
        "",
        "## 文件",
        "",
    ]
    for item in results:
        lines.append(f"- `{item['target']}`：修复 {item['changed']} 处，剩余 `统-` {item['after']} 处")
    lines.extend(["", "## 修复项", ""])
    for item in REPLACEMENTS:
        total = sum(result_item["count"] for result in results for result_item in result["items"] if result_item["old"] == item["old"])
        if total:
            lines.append(f"- {item['label']}：`{item['old']}` -> `{item['new']}`，{total} 处")
    lines.extend(["", "## 剩余边界", ""])
    remaining = False
    for item in results:
        for ctx in item["remaining_contexts"]:
            remaining = True
            lines.append(f"- `{item['target']}`：{ctx}")
    if not remaining:
        lines.append("- 无。")
    lines.extend(["", "## 未处理边界", "", "- 不处理其它连字符或破折号。", "- 本批未打开、展示或嵌入图片。"])
    report = "\n".join(lines) + "\n"
    REPORT_MD.write_text(report, encoding="utf-8")
    PROGRESS.write_text(report, encoding="utf-8")

    marker = "## 2026-07-07 高置信 OCR 错字补修第一百四十四批：统-连字符残字"
    upsert_memory(marker, f"""
{marker}

- 修复当前阅读稿固定语境 `统-` 误连字符残留：`统一/统订货/统经营`。
- 本批修复 {changed} 处；报告：`output/reports/reader_tong_hyphen_batch144_20260707.md`。
- 未处理其它连字符或破折号；未打开、展示或嵌入图片。
""")
    print(json.dumps({"changed": changed, "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
