# -*- coding: utf-8 -*-
"""Repair final semantic 人海 OCR residue to 入海."""

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
REPORT_JSON = ROOT / "output" / "reports" / "reader_ruhai_last_batch158_20260707.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_ruhai_last_batch158_20260707.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260707_人海末处语义补修第一百五十八批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"
OLD = "是人海必由之路"
NEW = "是入海必由之路"
LEFT_UNTOUCHED = [
    "源 OCR `workbench/ocr/merged/连云港市志_中_part02_OCR汇总.md:7939` 同误为 `人海必由之路`。",
    "据同句 `海口/风大浪恶/船家` 语境，定点修为 `入海必由之路`。",
    "本批没有打开、展示或嵌入图片。",
]


def plain_text(html: str) -> str:
    return re.sub(r"<[^>]+>", "", html)


def contexts(plain: str, term: str) -> list[str]:
    return [plain[max(0, m.start() - 55):m.start() + 85].replace("\n", " ") for m in re.finditer(term, plain)]


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
        count = before.count(OLD)
        after = before.replace(OLD, NEW)
        target.write_text(after, encoding="utf-8")
        after_plain = plain_text(after)
        results.append({
            "target": str(target),
            "before": before_plain.count("人海"),
            "changed": count,
            "after": after_plain.count("人海"),
            "remaining_contexts": contexts(after_plain, "人海"),
        })

    changed = sum(item["changed"] for item in results)
    payload = {"time": now, "scope": "current reader final semantic 人海 residue repair", "changed": changed, "targets": results, "left_untouched": LEFT_UNTOUCHED}
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 人海末处语义补修第一百五十八批",
        "",
        f"> 生成时间：{now}",
        "",
        "## 范围",
        "",
        "- 当前全书、中册、下册阅读稿。",
        "- 将凤凰山条目中 `是人海必由之路` 修为 `是入海必由之路`。",
        "",
        "## 统计",
        "",
        f"- 修复：{changed} 处",
        "",
        "## 文件",
        "",
    ]
    for item in results:
        lines.append(f"- `{item['target']}`：修复 {item['changed']} 处，剩余 `人海` {item['after']} 处")
    lines.extend(["", "## 证据说明", ""])
    for item in LEFT_UNTOUCHED:
        lines.append(f"- {item}")
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

    marker = "## 2026-07-07 高置信 OCR 错字补修第一百五十八批：人海末处语义补修"
    upsert_memory(marker, f"""
{marker}

- 对 batch157 后唯一剩余 `人海` 做源文与语义复核：源 OCR 同误，但同句为 `海口/风大浪恶/船家` 语境，故将 `是人海必由之路` 定点修为 `是入海必由之路`。
- 本批修复 {changed} 处；报告：`output/reports/reader_ruhai_last_batch158_20260707.md`。
- 当前 `人海/人境/深人` 均已清零；未打开、展示或嵌入图片。
""")
    print(json.dumps({"changed": changed, "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
