# -*- coding: utf-8 -*-
"""Repair OCR residue 进人 after protecting legal adjacent-word phrases."""

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
REPORT_JSON = ROOT / "output" / "reports" / "reader_jinru_batch138_20260707.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_jinru_batch138_20260707.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260707_进人残字回源补修第一百三十八批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

PROTECT = ["引进人才", "促进人才", "先进人物", "新进人员", "先进人类"]
REPLACEMENTS = [
    {"label": "进口货物", "old": "进人货物", "new": "进口货物"},
    {"label": "进入同段", "old": "进人", "new": "进入"},
    {"label": "进入跨段", "old": "进</p><p>人", "new": "进</p><p>入"},
]

LEFT_UNTOUCHED = [
    "保留 `引进人才/促进人才/先进人物/新进人员/先进人类` 等合法相邻字组合。",
    "`方人/准阳` 等其它残字族不纳入本批。",
    "本批没有打开、展示或嵌入图片。",
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


def repair(text: str) -> tuple[str, int, list[dict[str, int]]]:
    protected = {}
    work = text
    for index, phrase in enumerate(PROTECT):
        token = f"__PROTECT_JINREN_{index}__"
        protected[token] = phrase
        work = work.replace(phrase, token)

    items = []
    changed = 0
    for item in REPLACEMENTS:
        count = work.count(item["old"])
        if count:
            work = work.replace(item["old"], item["new"])
        changed += count
        items.append({**item, "count": count})

    for token, phrase in protected.items():
        work = work.replace(token, phrase)
    return work, changed, items


def main() -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    results = []
    for target in TARGETS:
        before = target.read_text(encoding="utf-8")
        before_plain = plain_text(before)
        after, changed, items = repair(before)
        target.write_text(after, encoding="utf-8")
        after_plain = plain_text(after)
        results.append({
            "target": str(target),
            "before": before_plain.count("进人"),
            "changed": changed,
            "after": after_plain.count("进人"),
            "items": items,
            "protected_counts": {phrase: before_plain.count(phrase) for phrase in PROTECT},
            "remaining_contexts": contexts(after_plain, "进人"),
        })

    changed = sum(item["changed"] for item in results)
    payload = {
        "time": now,
        "scope": "current reader 进人 residue repair with protected legal phrases",
        "patterns": len(REPLACEMENTS),
        "changed": changed,
        "targets": results,
        "left_untouched": LEFT_UNTOUCHED,
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 进人残字补修第一百三十八批",
        "",
        f"> 生成时间：{now}",
        "",
        "## 范围",
        "",
        "- 当前全书、中册、下册阅读稿。",
        "- 保护合法相邻字组合后，将高置信 `进人` 修为 `进入`；税务语境 `进人货物` 修为 `进口货物`。",
        "",
        "## 统计",
        "",
        f"- 证据形态：{len(REPLACEMENTS)} 项",
        f"- 修复：{changed} 处",
        "",
        "## 文件",
        "",
    ]
    for item in results:
        lines.append(f"- `{item['target']}`：修复 {item['changed']} 处，剩余 `进人` {item['after']} 处")
    lines.extend(["", "## 修复项", ""])
    for item in REPLACEMENTS:
        lines.append(f"- {item['label']}：`{item['old']}` -> `{item['new']}`")
    lines.extend(["", "## 保留项", ""])
    for phrase in PROTECT:
        total = sum(item["protected_counts"][phrase] for item in results)
        lines.append(f"- `{phrase}`：{total} 处")
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

    marker = "## 2026-07-07 高置信 OCR 错字补修第一百三十八批：进人残字"
    upsert_memory(marker, f"""
{marker}

- 保护 `引进人才/促进人才/先进人物/新进人员/先进人类` 等合法相邻字组合后，核修当前阅读稿 `进人` 残字。
- 本批修复 {changed} 处，其中 `进人货物` 修为 `进口货物`，其余高置信语境修为 `进入`；报告：`output/reports/reader_jinru_batch138_20260707.md`。
- 未处理 `方人/准阳` 等其它残字族；未打开、展示或嵌入图片。
""")
    print(json.dumps({"changed": changed, "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
