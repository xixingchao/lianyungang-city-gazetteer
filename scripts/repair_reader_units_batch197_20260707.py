# -*- coding: utf-8 -*-
"""Repair verified middle-reader 公斤 residues written as 公厅."""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FULL = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
MIDDLE = ROOT / "output" / "final_reader" / "连云港市志_中册.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_units_batch197_20260707.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_units_batch197_20260707.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260707_单位错字补修第一百九十七批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    ("250公厅芦笋", "250公斤芦笋"),
    ("每公厅1.1元", "每公斤1.1元"),
    ("青椒10多万公厅", "青椒10多万公斤"),
    ("种子350公厅", "种子350公斤"),
    ("不足50公厅", "不足50公斤"),
    ("17.8公厅", "17.8公斤"),
    ("由13公厅恢复", "由13公斤恢复"),
    ("均140公厅", "均140公斤"),
    ("600万公厅", "600万公斤"),
]


def plain(html: str) -> str:
    return re.sub(r"<[^>]+>", "", html)


def upsert_memory(total: int) -> None:
    marker = "## 2026-07-07 高置信 OCR 错字补修第一百九十七批：中册公斤单位"
    old = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    block = f"""
{marker}

- 对照当前全书 reader 正确文本，修复中册 `公厅` 对 `公斤` 的重量单位错识 9 处。
- 本批仅替换含数字/价格的完整短语，合计修复 {total} 处；报告：`output/reports/reader_units_batch197_20260707.md`。
- 保留 `办公厅` 等非重量语境；未做泛化 `公厅 -> 公斤`；未打开、展示或嵌入图片。
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
    after_text = plain(after)
    total = sum(item["changed"] for item in changed_items)
    payload = {
        "time": now,
        "changed": total,
        "full_evidence_counts": evidence,
        "replacements": changed_items,
        "middle_remaining_public_ting": after_text.count("公厅"),
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# 单位错字补修第一百九十七批",
        "",
        f"> 生成时间：{now}",
        "",
        "## 范围",
        "",
        "- 当前中册阅读稿。",
        "- 以当前全书 reader 正确句为证据，修复 `公厅` 对 `公斤` 的重量单位错识。",
        "- 未做泛化替换；未打开、展示或嵌入图片。",
        "",
        "## 统计",
        "",
        f"- 修复：{total} 处",
        f"- 修后中册纯文本 `公厅` 剩余：{after_text.count('公厅')} 处",
        "",
        "## 替换项",
        "",
    ]
    for item in changed_items:
        lines.append(f"- `{item['old']}` -> `{item['new']}`：{item['changed']} 处")
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    PROGRESS.write_text(REPORT_MD.read_text(encoding="utf-8"), encoding="utf-8")
    upsert_memory(total)
    print(json.dumps({"changed": total, "middle_remaining_public_ting": after_text.count("公厅"), "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
