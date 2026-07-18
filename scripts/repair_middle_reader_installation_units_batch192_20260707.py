# -*- coding: utf-8 -*-
"""Repair middle-reader installation unit OCR residues using full-reader evidence."""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MIDDLE = ROOT / "output" / "final_reader" / "连云港市志_中册.html"
FULL = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "middle_reader_installation_units_batch192_20260707.json"
REPORT_MD = ROOT / "output" / "reports" / "middle_reader_installation_units_batch192_20260707.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260707_中册安装工程单位补修第一百九十二批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    ("35方于瓦的热电站", "35万千瓦的热电站"),
    ("3×100方大卡冷水机组", "3×100万大卡冷水机组"),
    ("1.5方吨发酵间", "1.5万吨发酵间"),
    ("3方吨包装间", "3万吨包装间"),
]

FULL_EVIDENCE = [
    "35万千瓦的热电站",
    "3×100万大卡冷水机组",
    "1.5万吨发酵间",
    "3万吨包装间",
]


def plain(html: str) -> str:
    return re.sub(r"<[^>]+>", "", html)


def upsert_memory(total: int) -> None:
    marker = "## 2026-07-07 高置信 OCR 错字补修第一百九十二批：中册安装工程单位"
    old = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    block = f"""
{marker}

- 对照当前全书 reader 的工业设备安装工程段，修复中册同段单位错识：`35方于瓦/3×100方大卡/1.5方吨/3方吨`。
- 已仅在 `output/final_reader/连云港市志_中册.html` 修复 {total} 处；报告：`output/reports/middle_reader_installation_units_batch192_20260707.md`。
- `学土` 经复核为 `中学...人，土木` 跨词命中，未改；其它大批 `方吨/方公斤` 未逐源确认，未动；未打开、展示或嵌入图片。
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
    evidence_counts = {term: full_text.count(term) for term in FULL_EVIDENCE}
    if not all(count == 1 for count in evidence_counts.values()):
        raise SystemExit(f"full reader evidence not unique: {evidence_counts}")

    before = MIDDLE.read_text(encoding="utf-8")
    after = before
    changed_items = []
    for old, new in REPLACEMENTS:
        count = after.count(old)
        if count:
            after = after.replace(old, new)
            changed_items.append({"old": old, "new": new, "changed": count})
    MIDDLE.write_text(after, encoding="utf-8")
    total = sum(item["changed"] for item in changed_items)
    after_text = plain(after)

    payload = {
        "time": now,
        "changed": total,
        "full_evidence_counts": evidence_counts,
        "replacements": changed_items,
        "remaining_bad_terms": {old: after_text.count(old) for old, _ in REPLACEMENTS},
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# 中册安装工程单位补修第一百九十二批",
        "",
        f"> 生成时间：{now}",
        "",
        "## 范围",
        "",
        "- 当前中册阅读稿。",
        "- 以当前全书 reader 同段正确单位为证据，修复工业设备安装工程段单位错识。",
        "- 未处理其它未逐源确认的 `方吨/方公斤` 候选；未打开、展示或嵌入图片。",
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
