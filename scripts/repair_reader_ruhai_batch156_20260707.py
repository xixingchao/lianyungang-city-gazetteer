# -*- coding: utf-8 -*-
"""Repair fixed 人海 OCR residues to 入海/入海州."""

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
REPORT_JSON = ROOT / "output" / "reports" / "reader_ruhai_batch156_20260707.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_ruhai_batch156_20260707.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260707_人海残字补修第一百五十六批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    {"label": "导沭经沙入海", "old": "导述经沙人海", "new": "导述经沙入海"},
    {"label": "导淮入江入海", "old": "导淮入江人海", "new": "导淮入江入海"},
    {"label": "污水入海量", "old": "污水人海量", "new": "污水入海量"},
    {"label": "东流入海", "old": "东流人海", "new": "东流入海"},
    {"label": "入海口", "old": "人海口", "new": "入海口"},
    {"label": "入海求仙药", "old": "人海求仙药", "new": "入海求仙药"},
    {"label": "从淮入海", "old": "自淮人海", "new": "自淮入海"},
    {"label": "从淮入海", "old": "从淮人海", "new": "从淮入海"},
    {"label": "流入海州", "old": "流人海州", "new": "流入海州"},
    {"label": "迁入海州", "old": "迁人海州", "new": "迁入海州"},
    {"label": "进入海州", "old": "进人海州", "new": "进入海州"},
    {"label": "攻入海州", "old": "攻人海州", "new": "攻入海州"},
    {"label": "直入海州", "old": "直人海州", "new": "直入海州"},
    {"label": "入海州崇真中学", "old": "年人海</p><p>州崇真中学", "new": "年入海</p><p>州崇真中学"},
]
LEFT_UNTOUCHED = [
    "本批仅处理当前阅读稿中已核定的 `入海/入海州` 固定语境。",
    "不做 `人海` 裸词全局替换。",
    "本批没有打开、展示或嵌入图片。",
]


def plain_text(html: str) -> str:
    return re.sub(r"<[^>]+>", "", html)


def contexts(plain: str, term: str) -> list[str]:
    return [plain[max(0, m.start() - 55):m.start() + 85].replace("\n", " ") for m in re.finditer(term, plain)]


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
            "before": before_plain.count("人海"),
            "changed": sum(item["count"] for item in items),
            "after": after_plain.count("人海"),
            "items": items,
            "remaining_contexts": contexts(after_plain, "人海"),
        })

    changed = sum(item["changed"] for item in results)
    payload = {"time": now, "scope": "current reader 人海 OCR residue repair", "changed": changed, "targets": results, "left_untouched": LEFT_UNTOUCHED}
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 人海残字补修第一百五十六批",
        "",
        f"> 生成时间：{now}",
        "",
        "## 范围",
        "",
        "- 当前全书、中册、下册阅读稿。",
        "- 定点修复 `人海` 应为 `入海/入海州` 的水利、航运、战事、人物经历语境。",
        "",
        "## 统计",
        "",
        f"- 修复：{changed} 处",
        "",
        "## 文件",
        "",
    ]
    for item in results:
        lines.append(f"- `{item['target']}`：修复 {item['changed']} 处，剩余 `人海` {item['after']} 处")
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
    lines.extend(["", "## 未处理边界", ""])
    for item in LEFT_UNTOUCHED:
        lines.append(f"- {item}")
    report = "\n".join(lines) + "\n"
    REPORT_MD.write_text(report, encoding="utf-8")
    PROGRESS.write_text(report, encoding="utf-8")

    marker = "## 2026-07-07 高置信 OCR 错字补修第一百五十六批：人海残字"
    upsert_memory(marker, f"""
{marker}

- 核对当前阅读稿 `人海` 上下文，定点修复为 `入海/入海州`，覆盖水利工程、污水入海量、河流入海口、攻入海州、流入海州、入海州崇真中学等语境。
- 本批修复 {changed} 处；报告：`output/reports/reader_ruhai_batch156_20260707.md`。
- 未做 `人海` 裸词全局替换；未打开、展示或嵌入图片。
""")
    print(json.dumps({"changed": changed, "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
