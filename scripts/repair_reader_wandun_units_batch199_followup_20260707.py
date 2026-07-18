# -*- coding: utf-8 -*-
"""Repair four leftover evidence-backed 方吨/万吨 terms after batch199."""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FULL = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
MIDDLE = ROOT / "output" / "final_reader" / "连云港市志_中册.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_wandun_units_batch199_followup_20260707.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_wandun_units_batch199_followup_20260707.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260707_万吨单位错字补修第一百九十九批补遗.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    ("方吨啤酒灌装线", "万吨啤酒灌装线", "方吨</p><p>啤酒灌装线", "万吨</p><p>啤酒灌装线"),
    ("4个方吨级以上深水杂货泊位", "4个万吨级以上深水杂货泊位", "4个方吨级以上深水杂</p><p>货泊位", "4个万吨级以上深水杂</p><p>货泊位"),
    ("合成氨年生产能力达到3方吨", "合成氨年生产能力达到3万吨", "合成氨年生产</p><p>能力达到3方吨", "合成氨年生产</p><p>能力达到3万吨"),
    ("形成5方吨年产能力", "形成5万吨年产能力", "形成5方吨年</p><p>产能力", "形成5万吨年</p><p>产能力"),
]


def plain(html: str) -> str:
    return re.sub(r"<[^>]+>", "", html)


def upsert_memory(total: int, remaining: int) -> None:
    marker = "## 2026-07-07 高置信 OCR 错字补修第一百九十九批补遗：万吨单位"
    old = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    block = f"""
{marker}

- 复扫 batch199 后，中册仍有 4 处有全书证据或同段并列证据的 `方吨 -> 万吨` 残留。
- 已补修 `万吨啤酒灌装线`、`4个万吨级以上深水杂货泊位`、`合成氨年生产能力达到3万吨`、`形成5万吨年产能力`，合计 {total} 处；报告：`output/reports/reader_wandun_units_batch199_followup_20260707.md`。
- 修后中册纯文本 `方吨` 剩余 {remaining} 处，暂保留待源页核验；未打开、展示或嵌入图片。
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
    evidence = {new: full_text.count(new) for _old, new, _html_old, _html_new in REPLACEMENTS}
    missing = {term: count for term, count in evidence.items() if count < 1}
    if missing:
        raise SystemExit(f"missing full-reader evidence: {missing}")

    html = MIDDLE.read_text(encoding="utf-8")
    changed_items = []
    for old, new, html_old, html_new in REPLACEMENTS:
        count = html.count(html_old)
        if count:
            html = html.replace(html_old, html_new)
            changed_items.append({"old": old, "new": new, "changed": count})
    MIDDLE.write_text(html, encoding="utf-8")
    after_plain = plain(html)
    total = sum(item["changed"] for item in changed_items)
    remaining = after_plain.count("方吨")

    payload = {
        "time": now,
        "changed": total,
        "full_evidence_counts": evidence,
        "replacements": changed_items,
        "middle_remaining_fang_ton": remaining,
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# 万吨单位错字补修第一百九十九批补遗",
        "",
        f"> 生成时间：{now}",
        "",
        "## 范围",
        "",
        "- 当前中册阅读稿。",
        "- 补修 batch199 后仍有证据的 `方吨 -> 万吨/万吨级` 残留。",
        "- 未做泛化替换；未打开、展示或嵌入图片。",
        "",
        "## 统计",
        "",
        f"- 修复：{total} 处",
        f"- 修后中册纯文本 `方吨` 剩余：{remaining} 处",
        "",
        "## 替换项",
        "",
    ]
    for item in changed_items:
        lines.append(f"- `{item['old']}` -> `{item['new']}`：{item['changed']} 处")
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    PROGRESS.write_text(REPORT_MD.read_text(encoding="utf-8"), encoding="utf-8")
    upsert_memory(total, remaining)
    print(json.dumps({"changed": total, "middle_remaining_fang_ton": remaining, "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
