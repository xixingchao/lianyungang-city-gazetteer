# -*- coding: utf-8 -*-
"""Follow-up repair for remaining fixed 人土 OCR residues."""

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
REPORT_JSON = ROOT / "output" / "reports" / "reader_rentu_followup_batch142_20260707.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_rentu_followup_batch142_20260707.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260707_人土残字跟进补修第一百四十二批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

PROTECT = ["他人土地权"]
REPLACEMENTS = [
    {"label": "跨段藏入土特产品", "old": "藏人土特产</p><p>品", "new": "藏入土特产</p><p>品"},
    {"label": "党外人士", "old": "党外人土", "new": "党外人士"},
    {"label": "知名人士", "old": "知名人土", "new": "知名人士"},
    {"label": "社会人士", "old": "社会人土", "new": "社会人士"},
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


def repair(text: str) -> tuple[str, list[dict[str, int]]]:
    protected = {}
    work = text
    for index, phrase in enumerate(PROTECT):
        token = f"__PROTECT_RENTU_FOLLOWUP_{index}__"
        protected[token] = phrase
        work = work.replace(phrase, token)

    items = []
    for item in REPLACEMENTS:
        count = work.count(item["old"])
        if count:
            work = work.replace(item["old"], item["new"])
        items.append({**item, "count": count})

    for token, phrase in protected.items():
        work = work.replace(token, phrase)
    return work, items


def main() -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    results = []
    for target in TARGETS:
        before = target.read_text(encoding="utf-8")
        before_plain = plain_text(before)
        after, items = repair(before)
        target.write_text(after, encoding="utf-8")
        after_plain = plain_text(after)
        results.append({
            "target": str(target),
            "before": before_plain.count("人土"),
            "changed": sum(item["count"] for item in items),
            "after": after_plain.count("人土"),
            "items": items,
            "remaining_contexts": contexts(after_plain, "人土"),
        })

    changed = sum(item["changed"] for item in results)
    payload = {
        "time": now,
        "scope": "current reader remaining fixed 人土 OCR residue repair",
        "changed": changed,
        "targets": results,
        "protected": PROTECT,
        "left_untouched": ["保留 `他人土地权` 合法跨词命中。", "本批没有打开、展示或嵌入图片。"],
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 人土残字跟进补修第一百四十二批",
        "",
        f"> 生成时间：{now}",
        "",
        "## 范围",
        "",
        "- 当前全书、中册、下册阅读稿。",
        "- 补修 batch141 后剩余的固定 `人土` 残字，保护 `他人土地权`。",
        "",
        "## 统计",
        "",
        f"- 修复：{changed} 处",
        "",
        "## 文件",
        "",
    ]
    for item in results:
        lines.append(f"- `{item['target']}`：修复 {item['changed']} 处，剩余 `人土` {item['after']} 处")
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
    lines.extend(["", "## 未处理边界", "", "- 保留 `他人土地权` 合法跨词命中。", "- 本批未打开、展示或嵌入图片。"])
    report = "\n".join(lines) + "\n"
    REPORT_MD.write_text(report, encoding="utf-8")
    PROGRESS.write_text(report, encoding="utf-8")

    marker = "## 2026-07-07 高置信 OCR 错字补修第一百四十二批：人土残字跟进"
    upsert_memory(marker, f"""
{marker}

- 跟进修复 batch141 后剩余固定 `人土` 残字：`藏入土特产品/党外人士/知名人士/社会人士`。
- 本批修复 {changed} 处；报告：`output/reports/reader_rentu_followup_batch142_20260707.md`。
- 当前剩余 `人土` 均为 `他人土地权` 合法跨词命中；未打开、展示或嵌入图片。
""")
    print(json.dumps({"changed": changed, "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
