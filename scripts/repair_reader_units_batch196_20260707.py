# -*- coding: utf-8 -*-
"""Follow-up for verified vegetable purchase unit residues."""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MIDDLE = ROOT / "output" / "final_reader" / "连云港市志_中册.html"
FULL = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_units_batch196_20260707.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_units_batch196_20260707.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260707_单位错字补遗第一百九十六批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    ("葱65万公</p><p>厅", "葱65万公</p><p>斤"),
    ("1357方公斤", "1357万公斤"),
]
EVIDENCE = ["葱65万公斤", "1357万公斤"]


def plain(html: str) -> str:
    return re.sub(r"<[^>]+>", "", html)


def upsert_memory(total: int) -> None:
    marker = "## 2026-07-07 高置信 OCR 错字补修第一百九十六批：单位错字补遗"
    old = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    block = f"""
{marker}

- 复扫 batch195 后，中册蔬菜收购段仍有 `葱65万公厅`、`1357方公斤` 两处跨段/短语残留；当前全书 reader 同段为 `葱65万公斤`、`1357万公斤`。
- 已仅在 `output/final_reader/连云港市志_中册.html` 补修 {total} 处；报告：`output/reports/reader_units_batch196_20260707.md`。
- 未做泛化单位替换；未打开、展示或嵌入图片。
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
    full_text = plain(FULL.read_text(encoding="utf-8"))
    evidence_counts = {term: full_text.count(term) for term in EVIDENCE}
    if any(count < 1 for count in evidence_counts.values()):
        raise SystemExit(f"missing full evidence: {evidence_counts}")

    before = MIDDLE.read_text(encoding="utf-8")
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
        "full_evidence_counts": evidence_counts,
        "replacements": changed_items,
        "remaining": {old: after_text.count(plain(old)) for old, _new in REPLACEMENTS},
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# 单位错字补遗第一百九十六批",
        "",
        f"> 生成时间：{now}",
        "",
        "## 范围",
        "",
        "- 当前中册阅读稿。",
        "- 按当前全书 reader 同段证据，补修蔬菜收购段单位残留。",
        "- 未做泛化单位替换；未打开、展示或嵌入图片。",
        "",
        "## 统计",
        "",
        f"- 修复：{total} 处",
        "",
        "## 替换项",
        "",
    ]
    for item in changed_items:
        lines.append(f"- `{item['old']}` -> `{item['new']}`：{item['changed']} 处")
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    PROGRESS.write_text(REPORT_MD.read_text(encoding="utf-8"), encoding="utf-8")
    upsert_memory(total)
    print(json.dumps({"changed": total, "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
