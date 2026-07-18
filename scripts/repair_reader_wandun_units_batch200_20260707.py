# -*- coding: utf-8 -*-
"""Repair the remaining evidence-backed water-crystal 方吨 residues."""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FULL = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
MIDDLE = ROOT / "output" / "final_reader" / "连云港市志_中册.html"
LOWER = ROOT / "output" / "final_reader" / "连云港市志_下册.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_wandun_units_batch200_20260707.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_wandun_units_batch200_20260707.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260707_万吨单位错字补修第二百批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = {
    MIDDLE: [
        ("估算水晶总储量25.54方吨", "估算水晶总储量25.54万吨"),
        ("可采资源总量约2.55方吨", "可采资源总量约2.55万吨"),
    ],
    LOWER: [
        ("水晶矿地质储量药17方吨", "水晶矿地质储量约17万吨"),
    ],
}


def plain(html: str) -> str:
    return re.sub(r"<[^>]+>", "", html)


def upsert_memory(total: int, middle_remaining: int, lower_remaining: int) -> None:
    marker = "## 2026-07-07 高置信 OCR 错字补修第二百批：水晶储量万吨单位"
    old = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    block = f"""
{marker}

- 对照当前全书 reader 正确文本，修复中册/下册水晶储量段 `方吨 -> 万吨` 和 `药17 -> 约17` 残留 {total} 处。
- 下册对应 OCR 源页 `workbench/ocr/paddle_ocr/下/part01/page_0442.txt` 同样为 `水晶矿地质储量约17万吨`；报告：`output/reports/reader_wandun_units_batch200_20260707.md`。
- 修后剩余 `方吨`：中册 {middle_remaining} 处、下册 {lower_remaining} 处；未打开、展示或嵌入图片。
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
    evidence = {new: full_text.count(new) for items in REPLACEMENTS.values() for _old, new in items}
    missing = {term: count for term, count in evidence.items() if count < 1}
    if missing:
        raise SystemExit(f"missing full-reader evidence: {missing}")

    changed_items = []
    remaining = {}
    for path, items in REPLACEMENTS.items():
        html = path.read_text(encoding="utf-8")
        for old, new in items:
            count = html.count(old)
            if count:
                html = html.replace(old, new)
                changed_items.append({"file": path.name, "old": old, "new": new, "changed": count})
        path.write_text(html, encoding="utf-8")
        remaining[path.name] = plain(html).count("方吨")

    total = sum(item["changed"] for item in changed_items)
    payload = {
        "time": now,
        "changed": total,
        "full_evidence_counts": evidence,
        "replacements": changed_items,
        "remaining_fang_ton": remaining,
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 万吨单位错字补修第二百批",
        "",
        f"> 生成时间：{now}",
        "",
        "## 范围",
        "",
        "- 当前中册、下册阅读稿。",
        "- 以当前全书 reader 正确句为证据，修复水晶储量段 `方吨 -> 万吨` 和 `药17 -> 约17`。",
        "- 下册另以 `workbench/ocr/paddle_ocr/下/part01/page_0442.txt` 佐证。",
        "- 未做泛化替换；未打开、展示或嵌入图片。",
        "",
        "## 统计",
        "",
        f"- 修复：{total} 处",
        f"- 修后中册纯文本 `方吨` 剩余：{remaining.get(MIDDLE.name, 0)} 处",
        f"- 修后下册纯文本 `方吨` 剩余：{remaining.get(LOWER.name, 0)} 处",
        "",
        "## 替换项",
        "",
    ]
    for item in changed_items:
        lines.append(f"- `{item['file']}`：`{item['old']}` -> `{item['new']}`：{item['changed']} 处")
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    PROGRESS.write_text(REPORT_MD.read_text(encoding="utf-8"), encoding="utf-8")
    upsert_memory(total, remaining.get(MIDDLE.name, 0), remaining.get(LOWER.name, 0))
    print(json.dumps({"changed": total, "remaining_fang_ton": remaining, "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
