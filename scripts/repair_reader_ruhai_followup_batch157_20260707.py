# -*- coding: utf-8 -*-
"""Follow-up repair for remaining fixed 人海 OCR residues."""

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
REPORT_JSON = ROOT / "output" / "reports" / "reader_ruhai_followup_batch157_20260707.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_ruhai_followup_batch157_20260707.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260707_人海残字跟进补修第一百五十七批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    {"label": "瓷器入海州", "old": "陶瓷人海州", "new": "陶瓷入海州"},
    {"label": "通入海州城", "old": "通人海州城", "new": "通入海州城"},
    {"label": "洋桥入海", "old": "洋桥人海", "new": "洋桥入海"},
    {"label": "攻入海州跨段", "old": "攻人海</p><p>州", "new": "攻入海</p><p>州"},
    {"label": "编入海赣独立团", "old": "编人海赣独立团", "new": "编入海赣独立团"},
    {"label": "入海州崇真中学", "old": "）人海</p><p>州崇真中学", "new": "）入海</p><p>州崇真中学"},
]
LEFT_UNTOUCHED = [
    "暂留 `人海必由之路` 1 处，需进一步源页确认是否为 `入海必由之路`。",
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
    payload = {"time": now, "scope": "current reader remaining fixed 人海 OCR residue repair", "changed": changed, "targets": results, "left_untouched": LEFT_UNTOUCHED}
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 人海残字跟进补修第一百五十七批",
        "",
        f"> 生成时间：{now}",
        "",
        "## 范围",
        "",
        "- 当前全书、中册、下册阅读稿。",
        "- 跟进修复 batch156 后剩余高置信 `入海/入海州/编入海赣` 语境。",
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

    marker = "## 2026-07-07 高置信 OCR 错字补修第一百五十七批：人海残字跟进"
    upsert_memory(marker, f"""
{marker}

- 跟进 batch156 后剩余 `人海` 残字，修复 `陶瓷入海州/通入海州城/洋桥入海/攻入海州/编入海赣独立团/入海州崇真中学` 等语境。
- 本批修复 {changed} 处；报告：`output/reports/reader_ruhai_followup_batch157_20260707.md`。
- 暂留 `人海必由之路` 1 处待源页确认；未打开、展示或嵌入图片。
""")
    print(json.dumps({"changed": changed, "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
