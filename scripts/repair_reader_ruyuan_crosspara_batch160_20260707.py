# -*- coding: utf-8 -*-
"""Repair the remaining cross-paragraph 人院 OCR residue."""

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
REPORT_JSON = ROOT / "output" / "reports" / "reader_ruyuan_crosspara_batch160_20260707.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_ruyuan_crosspara_batch160_20260707.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260707_人院跨段残字补修第一百六十批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

PATTERN = "病人人</p><p>院预交保证金"
REPLACEMENT = "病人入</p><p>院预交保证金"
TERM = "人院"


def plain_text(html: str) -> str:
    return re.sub(r"<[^>]+>", "", html)


def contexts(plain: str, term: str) -> list[str]:
    return [plain[max(0, m.start() - 70):m.start() + 100].replace("\n", " ") for m in re.finditer(term, plain)]


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
        "scope": "current reader cross-paragraph 人院 OCR residue repair",
        "pattern": PATTERN,
        "replacement": REPLACEMENT,
        "changed": total,
        "targets": results,
        "note": "Only repairs 病人入院预交保证金 split across paragraph tags; no images opened or embedded.",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 人院跨段残字补修第一百六十批",
        "",
        f"> 生成时间：{now}",
        "",
        "## 范围",
        "",
        "- 当前全书、中册、下册阅读稿。",
        "- 仅修复跨段标签造成的 `病人人院预交保证金`，恢复为 `病人入院预交保证金`。",
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
        lines.append(f"- `{item['target']}`：修复 {item['changed']} 处，剩余 `人院` {item['after']} 处")
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

    marker = "## 2026-07-07 高置信 OCR 错字补修第一百六十批：人院跨段残字"
    upsert_memory(marker, f"""
{marker}

- 核对当前下册阅读稿残留 `人院`，为跨段标签 `病人人</p><p>院预交保证金`，语义应为 `病人入院预交保证金`。
- 本批仅定点修复该跨段形态，共 {total} 处；报告：`output/reports/reader_ruyuan_crosspara_batch160_20260707.md`。
- 未处理其它 `人/入` 残字族；未打开、展示或嵌入图片。
""")
    print(json.dumps({"changed": total, "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
