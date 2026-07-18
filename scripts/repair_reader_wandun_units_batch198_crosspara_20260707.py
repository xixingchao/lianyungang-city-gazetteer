# -*- coding: utf-8 -*-
"""Repair cross-paragraph leftovers from batch198."""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FULL = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
MIDDLE = ROOT / "output" / "final_reader" / "连云港市志_中册.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_wandun_units_batch198_crosspara_20260707.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_wandun_units_batch198_crosspara_20260707.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260707_万吨单位错字补修第一百九十八批跨段补遗.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    ("民国26年上半年14.7方吨", "民国26年上半年14.7万吨", "14.7方吨"),
    ("数量为22.17方吨", "数量为22.17万吨", "22.17方吨"),
    ("1962~1969年出口煤炭122.66方吨", "1962~1969年出口煤炭122.66万吨", "122.66方吨"),
]


def plain(html: str) -> str:
    return re.sub(r"<[^>]+>", "", html)


def upsert_memory(total: int) -> None:
    marker = "## 2026-07-07 高置信 OCR 错字补修第一百九十八批跨段补遗：万吨单位"
    old = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    block = f"""
{marker}

- 复扫 batch198 后，中册仍有 3 处因 HTML 段落切分未命中的 `方吨 -> 万吨` 残留。
- 已补修 `民国26年上半年14.7万吨`、`数量为22.17万吨`、`1962~1969年出口煤炭122.66万吨`，合计 {total} 处；报告：`output/reports/reader_wandun_units_batch198_crosspara_20260707.md`。
- 未处理其它未逐条核证的 `方吨` 候选；未打开、展示或嵌入图片。
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
    evidence = {new: full_text.count(new) for _old, new, _html_bad in REPLACEMENTS}
    missing = {term: count for term, count in evidence.items() if count < 1}
    if missing:
        raise SystemExit(f"missing full-reader evidence: {missing}")

    html = MIDDLE.read_text(encoding="utf-8")
    before_plain = plain(html)
    changed_items = []
    for old, new, html_bad in REPLACEMENTS:
        plain_count = before_plain.count(old)
        html_count = html.count(html_bad)
        if plain_count and html_count:
            html = html.replace(html_bad, html_bad.replace("方吨", "万吨"), 1)
            changed_items.append({"old": old, "new": new, "changed": 1})
    MIDDLE.write_text(html, encoding="utf-8")
    after_plain = plain(html)
    total = sum(item["changed"] for item in changed_items)

    payload = {
        "time": now,
        "changed": total,
        "full_evidence_counts": evidence,
        "replacements": changed_items,
        "middle_remaining_fang_ton": after_plain.count("方吨"),
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 万吨单位错字补修第一百九十八批跨段补遗",
        "",
        f"> 生成时间：{now}",
        "",
        "## 范围",
        "",
        "- 当前中册阅读稿。",
        "- 补修 batch198 中因 HTML 段落切分未命中的 `方吨 -> 万吨` 残留。",
        "- 未做泛化替换；未打开、展示或嵌入图片。",
        "",
        "## 统计",
        "",
        f"- 修复：{total} 处",
        f"- 修后中册纯文本 `方吨` 剩余：{after_plain.count('方吨')} 处",
        "",
        "## 替换项",
        "",
    ]
    for item in changed_items:
        lines.append(f"- `{item['old']}` -> `{item['new']}`：{item['changed']} 处")
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    PROGRESS.write_text(REPORT_MD.read_text(encoding="utf-8"), encoding="utf-8")
    upsert_memory(total)
    print(json.dumps({"changed": total, "middle_remaining_fang_ton": after_plain.count("方吨"), "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
