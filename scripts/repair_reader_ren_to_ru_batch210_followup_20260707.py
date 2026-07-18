# -*- coding: utf-8 -*-
"""Follow up cross-paragraph middle-reader 人->入 residues from batch210."""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FULL = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
MIDDLE = ROOT / "output" / "final_reader" / "连云港市志_中册.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_ren_to_ru_batch210_followup_20260707.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_ren_to_ru_batch210_followup_20260707.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260707_人入残留补修第二百一十批补遗.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    ("电子产品，逐步打</p><p>人国际市场", "电子产品，逐步打</p><p>入国际市场", "电子产品，逐步打入国际市场"),
    ("木帆船多经海道人</p><p>临洪河", "木帆船多经海道入</p><p>临洪河", "木帆船多经海道入临洪河"),
    ("出口香港，打人国际市</p><p>场", "出口香港，打入国际市</p><p>场", "出口香港，打入国际市场"),
    ("由入省库改为人</p><p>市库", "由入省库改为入</p><p>市库", "由入省库改为入市库"),
]


def plain(html: str) -> str:
    return re.sub(r"<[^>]+>", "", html)


def count_candidates(text: str, full_text: str) -> int:
    total = 0
    for m in re.finditer("人", text):
        ctx = text[max(0, m.start() - 18): min(len(text), m.end() + 18)]
        rel = m.start() - max(0, m.start() - 18)
        good = ctx[:rel] + "入" + ctx[rel + 1:]
        if full_text.count(good) and not full_text.count(ctx):
            total += 1
    return total


def main() -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    full_text = plain(FULL.read_text(encoding="utf-8"))
    evidence = {evidence: full_text.count(evidence) for _old, _new, evidence in REPLACEMENTS}
    missing = {term: count for term, count in evidence.items() if count < 1}
    if missing:
        raise SystemExit(f"missing full-reader evidence: {missing}")
    html = MIDDLE.read_text(encoding="utf-8")
    changed_items = []
    for old, new, _evidence in REPLACEMENTS:
        count = html.count(old)
        if count:
            html = html.replace(old, new)
            changed_items.append({"old": plain(old), "new": plain(new), "changed": count})
    MIDDLE.write_text(html, encoding="utf-8")
    total = sum(item["changed"] for item in changed_items)
    remaining = count_candidates(plain(html), full_text)
    payload = {"time": now, "changed": total, "replacements": changed_items, "middle_remaining_ren_to_ru_candidates": remaining}
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# 人入残留补修第二百一十批补遗",
        "",
        f"> 生成时间：{now}",
        "",
        "## 统计",
        "",
        f"- 修复：{total} 处",
        f"- 修后中册 `人 -> 入` 短上下文候选剩余：{remaining} 条",
        "- 未做单字替换；未打开、展示或嵌入图片。",
        "",
        "## 替换项",
        "",
    ]
    for item in changed_items:
        lines.append(f"- `{item['old']}` -> `{item['new']}`：{item['changed']} 处")
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    PROGRESS.write_text(REPORT_MD.read_text(encoding="utf-8"), encoding="utf-8")
    MEMORY.write_text(MEMORY.read_text(encoding="utf-8").rstrip() + f"\n\n## 2026-07-07 高置信 OCR 错字补修第二百一十批补遗：中册人入残留\n\n- 补修 batch210 漏过的跨段 `人 -> 入` 残留 {total} 处。\n- 修后按短上下文扫描，中册 `人 -> 入` 候选剩余 {remaining} 条；报告：`output/reports/reader_ren_to_ru_batch210_followup_20260707.md`。\n- 未打开、展示或嵌入图片。\n", encoding="utf-8")
    print(json.dumps({"changed": total, "remaining_candidates": remaining, "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
