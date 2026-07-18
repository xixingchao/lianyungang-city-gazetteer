# -*- coding: utf-8 -*-
"""Repair evidence-backed middle-reader 水泥厂 residues written as 水泥广."""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FULL = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
MIDDLE = ROOT / "output" / "final_reader" / "连云港市志_中册.html"
REPORT_JSON = ROOT / "output" / "reports" / "middle_reader_cement_factory_batch202_20260707.json"
REPORT_MD = ROOT / "output" / "reports" / "middle_reader_cement_factory_batch202_20260707.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260707_中册水泥厂残留补修第二百零二批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    (
        "赣榆县欢墩水泥广更名为赣榆县第二水泥厂",
        "赣榆县欢墩水泥厂更名为赣榆县第二水泥厂",
        "赣榆县欢墩水泥广更名为</p><p>赣榆县第二水泥厂",
        "赣榆县欢墩水泥厂更名为</p><p>赣榆县第二水泥厂",
    ),
    (
        "当年，全市8家水泥广生产水泥37.4万吨",
        "当年，全市8家水泥厂生产水泥37.4万吨",
        "当年，全市8家水泥广生产水泥37.4万吨",
        "当年，全市8家水泥厂生产水泥37.4万吨",
    ),
    (
        "扩建了市水泥广，于1980年投产",
        "扩建了市水泥厂，于1980年投产",
        "扩建了市水泥广，于1980</p><p>年投产",
        "扩建了市水泥厂，于1980</p><p>年投产",
    ),
]


def plain(html: str) -> str:
    return re.sub(r"<[^>]+>", "", html)


def upsert_memory(total: int, remaining: int) -> None:
    marker = "## 2026-07-07 高置信 OCR 错字补修第二百零二批：中册水泥厂残留"
    old = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    block = f"""
{marker}

- 对照当前全书 reader 正确文本，修复中册 `水泥广` 对 `水泥厂` 的错识 {total} 处。
- 未修 `形成生产能力20吨`，因当前全书 reader 同样为 `20吨`，需源页核验；报告：`output/reports/middle_reader_cement_factory_batch202_20260707.md`。
- 修后中册纯文本 `水泥广` 剩余 {remaining} 处；未打开、展示或嵌入图片。
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
    remaining = after_plain.count("水泥广")

    payload = {
        "time": now,
        "changed": total,
        "full_evidence_counts": evidence,
        "replacements": changed_items,
        "middle_remaining_cement_guang": remaining,
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# 中册水泥厂残留补修第二百零二批",
        "",
        f"> 生成时间：{now}",
        "",
        "## 范围",
        "",
        "- 当前中册阅读稿。",
        "- 以当前全书 reader 正确句为证据，修复 `水泥广` 对 `水泥厂` 的错识。",
        "- 未做泛化替换；未打开、展示或嵌入图片。",
        "",
        "## 统计",
        "",
        f"- 修复：{total} 处",
        f"- 修后中册纯文本 `水泥广` 剩余：{remaining} 处",
        "",
        "## 替换项",
        "",
    ]
    for item in changed_items:
        lines.append(f"- `{item['old']}` -> `{item['new']}`：{item['changed']} 处")
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    PROGRESS.write_text(REPORT_MD.read_text(encoding="utf-8"), encoding="utf-8")
    upsert_memory(total, remaining)
    print(json.dumps({"changed": total, "middle_remaining_cement_guang": remaining, "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
