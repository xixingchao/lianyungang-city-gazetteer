# -*- coding: utf-8 -*-
"""Repair the remaining cross-paragraph 人学 OCR residue."""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = [
    ROOT / "output" / "final_reader" / "连云港市志_全书.html",
    ROOT / "output" / "final_reader" / "连云港市志_中册.html",
    ROOT / "output" / "final_reader" / "连云港市志_下册.html",
]
REPORT_JSON = ROOT / "output" / "reports" / "reader_ruxue_crosspara_batch162_20260707.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_ruxue_crosspara_batch162_20260707.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260707_人学跨段残字补修第一百六十二批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"
PATTERN = "中小学人学</p><p>新生"
REPLACEMENT = "中小学入学</p><p>新生"
TERM = "人学"


def plain_text(html: str) -> str:
    return re.sub(r"<[^>]+>", "", html)


def contexts(plain: str, term: str) -> list[str]:
    return [plain[max(0, m.start() - 75):m.start() + 110].replace("\n", " ") for m in re.finditer(term, plain)]


def upsert_memory(marker: str, content: str) -> None:
    old = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker not in old:
        MEMORY.write_text(old.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")
        return
    start = old.index(marker)
    next_start = old.find("\n## ", start + 1)
    new = old[:start].rstrip() + "\n\n" + content.strip() + "\n"
    if next_start != -1:
        new += "\n" + old[next_start:].lstrip()
    MEMORY.write_text(new, encoding="utf-8")


def main() -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    results = []
    for target in TARGETS:
        before = target.read_text(encoding="utf-8")
        before_plain = plain_text(before)
        changed = before.count(PATTERN)
        after = before.replace(PATTERN, REPLACEMENT)
        target.write_text(after, encoding="utf-8")
        after_plain = plain_text(after)
        results.append({
            "target": str(target),
            "before": before_plain.count(TERM),
            "changed": changed,
            "after": after_plain.count(TERM),
            "remaining_contexts": contexts(after_plain, TERM),
        })

    total = sum(item["changed"] for item in results)
    payload = {
        "time": now,
        "scope": "current reader cross-paragraph 人学 OCR residue repair",
        "pattern": PATTERN,
        "replacement": REPLACEMENT,
        "changed": total,
        "targets": results,
        "note": "Only repairs 中小学入学新生 split across paragraph tags; no images opened or embedded.",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 人学跨段残字补修第一百六十二批",
        "",
        f"> 生成时间：{now}",
        "",
        "## 范围",
        "",
        "- 当前全书、中册、下册阅读稿。",
        "- 仅修复跨段标签造成的 `中小学人学新生`，恢复为 `中小学入学新生`。",
        "- 未打开、展示或嵌入图片。",
        "",
        "## 统计",
        "",
        f"- 修复：{total} 处",
        "",
        "## 文件",
        "",
    ]
    for item in results:
        lines.append(f"- `{item['target']}`：修复 {item['changed']} 处，剩余 `人学` {item['after']} 处")
    lines.extend(["", "## 剩余边界", ""])
    remaining = False
    for item in results:
        for ctx in item["remaining_contexts"]:
            remaining = True
            lines.append(f"- `{item['target']}`：{ctx}")
    if not remaining:
        lines.append("- 无。")
    report = "\n".join(lines) + "\n"
    REPORT_MD.write_text(report, encoding="utf-8")
    PROGRESS.write_text(report, encoding="utf-8")

    marker = "## 2026-07-07 高置信 OCR 错字补修第一百六十二批：人学跨段残字"
    upsert_memory(marker, f"""
{marker}

- 核对当前下册阅读稿残留 `中小学人学</p><p>新生`，语义应为 `中小学入学新生`。
- 本批仅定点修复该跨段形态，共 {total} 处；报告：`output/reports/reader_ruxue_crosspara_batch162_20260707.md`。
- 未处理其它 `人/入` 残字族；未打开、展示或嵌入图片。
""")
    print(json.dumps({"changed": total, "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
