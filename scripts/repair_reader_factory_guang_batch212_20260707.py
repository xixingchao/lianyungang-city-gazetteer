# -*- coding: utf-8 -*-
"""Repair two evidence-backed lower-reader 印刷广->印刷厂 residues."""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FULL = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
LOWER = ROOT / "output" / "final_reader" / "连云港市志_下册.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_factory_guang_batch212_20260707.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_factory_guang_batch212_20260707.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260707_厂字残留补修第二百一十二批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    ("报社有印刷广", "报社有印刷厂"),
    ("在市机</p><p>关印刷广印刷", "在市机</p><p>关印刷厂印刷"),
]


def plain(html: str) -> str:
    return re.sub(r"<[^>]+>", "", html)


def count_factory_candidates(text: str, full_text: str) -> int:
    total = 0
    for m in re.finditer("广", text):
        ctx = text[max(0, m.start() - 18): min(len(text), m.end() + 18)]
        rel = m.start() - max(0, m.start() - 18)
        good = ctx[:rel] + "厂" + ctx[rel + 1:]
        if full_text.count(good) and not full_text.count(ctx):
            total += 1
    return total


def main() -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    full_text = plain(FULL.read_text(encoding="utf-8"))
    evidence = {plain(new): full_text.count(plain(new)) for _old, new in REPLACEMENTS}
    missing = {term: count for term, count in evidence.items() if count < 1}
    if missing:
        raise SystemExit(f"missing full-reader evidence: {missing}")
    html = LOWER.read_text(encoding="utf-8")
    changed_items = []
    for old, new in REPLACEMENTS:
        count = html.count(old)
        if count:
            html = html.replace(old, new)
            changed_items.append({"old": plain(old), "new": plain(new), "changed": count})
    LOWER.write_text(html, encoding="utf-8")
    total = sum(item["changed"] for item in changed_items)
    remaining = count_factory_candidates(plain(html), full_text)
    payload = {"time": now, "changed": total, "replacements": changed_items, "lower_remaining_factory_candidates": remaining, "deferred": ["送印刷广切边"]}
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# 厂字残留补修第二百一十二批",
        "",
        f"> 生成时间：{now}",
        "",
        "## 范围",
        "",
        "- 当前下册阅读稿。",
        "- 以当前全书 reader 正确句为证据，修复 `印刷广 -> 印刷厂` 固定短语错识。",
        "- `送印刷广切边` 在当前全书同样为坏形态，暂留待源页核验。",
        "- 未做单字替换；未打开、展示或嵌入图片。",
        "",
        "## 统计",
        "",
        f"- 修复：{total} 处",
        f"- 修后下册 `广 -> 厂` 短上下文候选剩余：{remaining} 条",
        "",
        "## 替换项",
        "",
    ]
    for item in changed_items:
        lines.append(f"- `{item['old']}` -> `{item['new']}`：{item['changed']} 处")
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    PROGRESS.write_text(REPORT_MD.read_text(encoding="utf-8"), encoding="utf-8")
    MEMORY.write_text(MEMORY.read_text(encoding="utf-8").rstrip() + f"\n\n## 2026-07-07 高置信 OCR 错字补修第二百一十二批：下册印刷厂残留\n\n- 对照当前全书 reader 正确文本，修复下册 `印刷广 -> 印刷厂` 高置信残留 {total} 处。\n- `送印刷广切边` 在当前全书同样为坏形态，暂留待源页核验；报告：`output/reports/reader_factory_guang_batch212_20260707.md`。\n- 未打开、展示或嵌入图片。\n", encoding="utf-8")
    print(json.dumps({"changed": total, "remaining_candidates": remaining, "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
