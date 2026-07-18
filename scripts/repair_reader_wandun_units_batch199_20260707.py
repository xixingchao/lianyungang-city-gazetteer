# -*- coding: utf-8 -*-
"""Repair another evidence-backed batch of 方吨/万吨 residues in middle reader."""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FULL = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
MIDDLE = ROOT / "output" / "final_reader" / "连云港市志_中册.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_wandun_units_batch199_20260707.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_wandun_units_batch199_20260707.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260707_万吨单位错字补修第一百九十九批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    ("加工白条肉1.74方吨", "加工白条肉1.74万吨"),
    ("年产能力为1.5方吨", "年产能力为1.5万吨"),
    ("全市白酒生产能力3.5方吨", "全市白酒生产能力3.5万吨"),
    ("年增1方吨啤酒能力", "年增1万吨啤酒能力"),
    ("年产能力增到1.5方吨", "年产能力增到1.5万吨"),
    ("年产能力4.5方吨", "年产能力4.5万吨"),
    ("方吨啤酒灌装线", "万吨啤酒灌装线"),
    ("合成氨年生产能力达3.6方吨", "合成氨年生产能力达3.6万吨"),
    ("合成氨年生产能力达5.6方吨", "合成氨年生产能力达5.6万吨"),
    ("形成5方吨年产能力", "形成5万吨年产能力"),
    ("锦屏磷矿1.5方吨磷酸厂", "锦屏磷矿1.5万吨磷酸厂"),
    ("年开采量30方吨", "年开采量30万吨"),
    ("4个方吨级以上深水杂货泊位", "4个万吨级以上深水杂货泊位"),
    ("可供2.5方吨级船舶", "可供2.5万吨级船舶"),
    ("能堆存10方吨煤炭", "能堆存10万吨煤炭"),
    ("磷矿石33方吨", "磷矿石33万吨"),
    ("载重1.08方吨", "载重1.08万吨"),
    ("淮北海盐5.62方吨", "淮北海盐5.62万吨"),
    ("食盐积压5方吨", "食盐积压5万吨"),
    ("年出口豆（生）油2方吨", "年出口豆（生）油2万吨"),
    ("当年产量1.6方吨", "当年产量1.6万吨"),
    ("碳铵14.70方吨", "碳铵14.70万吨"),
    ("合成氨年生产能力达到3方吨", "合成氨年生产能力达到3万吨"),
    ("年产1方吨石灰膏", "年产1万吨石灰膏"),
    ("年总产量达11.43方吨", "年总产量达11.43万吨"),
]


def plain(html: str) -> str:
    return re.sub(r"<[^>]+>", "", html)


def upsert_memory(total: int, remaining: int) -> None:
    marker = "## 2026-07-07 高置信 OCR 错字补修第一百九十九批：万吨单位"
    old = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    block = f"""
{marker}

- 对照当前全书 reader 正确文本，继续修复中册 `方吨` 对 `万吨/万吨级` 的单位错识 {total} 处。
- 本批仅替换带上下文的完整短语；报告：`output/reports/reader_wandun_units_batch199_20260707.md`。
- 修后中册纯文本 `方吨` 剩余 {remaining} 处，多为水晶储量、表格残片或仍需源页核验项；未打开、展示或嵌入图片。
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
    evidence = {new: full_text.count(new) for _old, new in REPLACEMENTS}
    missing = {term: count for term, count in evidence.items() if count < 1}
    if missing:
        raise SystemExit(f"missing full-reader evidence: {missing}")

    before = MIDDLE.read_text(encoding="utf-8")
    after = before
    changed_items = []
    for old, new in REPLACEMENTS:
        count = after.count(old)
        if count:
            after = after.replace(old, new)
            changed_items.append({"old": old, "new": new, "changed": count})
    MIDDLE.write_text(after, encoding="utf-8")
    after_plain = plain(after)
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
        "# 万吨单位错字补修第一百九十九批",
        "",
        f"> 生成时间：{now}",
        "",
        "## 范围",
        "",
        "- 当前中册阅读稿。",
        "- 以当前全书 reader 正确句为证据，修复 `方吨` 对 `万吨/万吨级` 的单位错识。",
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
