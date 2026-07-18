# -*- coding: utf-8 -*-
"""Repair high-confidence 逮捕 OCR residue."""

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
REPORT_JSON = ROOT / "output" / "reports" / "reader_daibu_batch185_20260707.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_daibu_batch185_20260707.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260707_逮捕残字补修第一百八十五批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"
OLD = "速捕"
NEW = "逮捕"


def plain(html: str) -> str:
    return re.sub(r"<[^>]+>", "", html)


def contexts(text: str, term: str) -> list[str]:
    return [text[max(0, m.start() - 80):m.start() + 130].replace("\n", " ") for m in re.finditer(re.escape(term), text)]


def upsert_memory(total: int) -> None:
    marker = "## 2026-07-07 高置信 OCR 错字补修第一百八十五批：逮捕候选"
    old = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    block = f"""
{marker}

- 核对当前阅读稿 `速捕`，上下文均为 `依法逮捕/逮捕人犯/逮捕道首/大逮捕/逮捕证/批准逮捕` 等司法、历史语境，判定为 `逮捕` OCR 误识。
- 已在当前全书、中册、下册 reader 定点修复 {total} 处；报告：`output/reports/reader_daibu_batch185_20260707.md`。
- 未处理其它 `捕` 字组合；未打开、展示或嵌入图片。
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
    results = []
    for target in TARGETS:
        before = target.read_text(encoding="utf-8")
        before_plain = plain(before)
        before_contexts = contexts(before_plain, OLD)
        count = before.count(OLD)
        after = before.replace(OLD, NEW)
        target.write_text(after, encoding="utf-8")
        after_plain = plain(after)
        results.append({
            "target": str(target),
            "changed": count,
            "before_plain_count": before_plain.count(OLD),
            "after_plain_count": after_plain.count(OLD),
            "before_contexts": before_contexts,
        })
    total = sum(item["changed"] for item in results)
    payload = {
        "time": now,
        "scope": "current reader high-confidence 逮捕 OCR repair",
        "old": OLD,
        "new": NEW,
        "changed": total,
        "targets": results,
        "left_untouched": ["其它 `捕` 字组合", "raw OCR", "图片或截图"],
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# 逮捕残字补修第一百八十五批",
        "",
        f"> 生成时间：{now}",
        "",
        "## 范围",
        "",
        "- 当前全书、中册、下册阅读稿。",
        "- 修复司法、历史语境中 `速捕` 对 `逮捕` 的 OCR 误识。",
        "- 未处理其它 `捕` 字组合；未打开、展示或嵌入图片。",
        "",
        "## 统计",
        "",
        f"- 修复：{total} 处",
        "",
        "## 文件",
        "",
    ]
    for item in results:
        lines.append(f"- `{item['target']}`：修复 {item['changed']} 处；剩余 `速捕` {item['after_plain_count']} 处")
    report = "\n".join(lines) + "\n"
    REPORT_MD.write_text(report, encoding="utf-8")
    PROGRESS.write_text(report, encoding="utf-8")
    upsert_memory(total)
    print(json.dumps({"changed": total, "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
