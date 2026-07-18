# -*- coding: utf-8 -*-
"""Follow up cross-paragraph lower-reader 人->入 residues from batch211."""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FULL = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
LOWER = ROOT / "output" / "final_reader" / "连云港市志_下册.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_ren_to_ru_batch211_followup_20260707.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_ren_to_ru_batch211_followup_20260707.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260707_人入残留补修第二百一十一批补遗.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    ("全市幼儿园1933所，人园</p><p>幼儿134587人", "全市幼儿园1933所，入园</p><p>幼儿134587人", "全市幼儿园1933所，入园幼儿134587人"),
    ("海运工会人股集</p><p>资", "海运工会入股集</p><p>资", "海运工会入股集资"),
    ("后受党派遣，打</p><p>人国民党新安镇公安分局", "后受党派遣，打</p><p>入国民党新安镇公安分局", "打入国民党新安镇公安分局"),
    ("因疲劳沉</p><p>人水底", "因疲劳沉</p><p>入水底", "因疲劳沉入水底"),
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
    html = LOWER.read_text(encoding="utf-8")
    changed_items = []
    for old, new, _evidence in REPLACEMENTS:
        count = html.count(old)
        if count:
            html = html.replace(old, new)
            changed_items.append({"old": plain(old), "new": plain(new), "changed": count})
    LOWER.write_text(html, encoding="utf-8")
    total = sum(item["changed"] for item in changed_items)
    remaining = count_candidates(plain(html), full_text)
    payload = {"time": now, "changed": total, "replacements": changed_items, "lower_remaining_ren_to_ru_candidates": remaining}
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# 人入残留补修第二百一十一批补遗",
        "",
        f"> 生成时间：{now}",
        "",
        "## 统计",
        "",
        f"- 修复：{total} 处",
        f"- 修后下册 `人 -> 入` 短上下文候选剩余：{remaining} 条",
        "- 未做单字替换；未打开、展示或嵌入图片。",
        "",
        "## 替换项",
        "",
    ]
    for item in changed_items:
        lines.append(f"- `{item['old']}` -> `{item['new']}`：{item['changed']} 处")
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    PROGRESS.write_text(REPORT_MD.read_text(encoding="utf-8"), encoding="utf-8")
    MEMORY.write_text(MEMORY.read_text(encoding="utf-8").rstrip() + f"\n\n## 2026-07-07 高置信 OCR 错字补修第二百一十一批补遗：下册人入残留\n\n- 补修 batch211 漏过的跨段 `人 -> 入` 残留 {total} 处。\n- 修后按短上下文扫描，下册 `人 -> 入` 候选剩余 {remaining} 条；报告：`output/reports/reader_ren_to_ru_batch211_followup_20260707.md`。\n- 未打开、展示或嵌入图片。\n", encoding="utf-8")
    print(json.dumps({"changed": total, "remaining_candidates": remaining, "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
