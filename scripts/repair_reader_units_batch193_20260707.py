# -*- coding: utf-8 -*-
"""Repair high-confidence unit OCR residues in current readers."""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOWER = ROOT / "output" / "final_reader" / "连云港市志_下册.html"
MIDDLE = ROOT / "output" / "final_reader" / "连云港市志_中册.html"
FULL = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_units_batch193_20260707.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_units_batch193_20260707.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260707_单位错字补修第一百九十三批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

TARGET_REPLACEMENTS = {
    LOWER: [
        ("0.6万公厅酒精", "0.6万公斤酒精"),
        ("11.3万公厅炸药", "11.3万公斤炸药"),
        ("7.5公厅小麦", "7.5公斤小麦"),
        ("90公厅挺举", "90公斤挺举"),
        ("5.1公厅，通高", "5.1公斤，通高"),
    ],
    MIDDLE: [
        ("农网损失电量3732方于瓦时", "农网损失电量3732万千瓦时"),
    ],
}
FULL_EVIDENCE = "农网损失电量3732万千瓦时"


def plain(html: str) -> str:
    return re.sub(r"<[^>]+>", "", html)


def upsert_memory(total: int) -> None:
    marker = "## 2026-07-07 高置信 OCR 错字补修第一百九十三批：单位错字"
    old = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    block = f"""
{marker}

- 核对当前 reader 单位残留，修复下册重量语境 `公厅 -> 公斤` 5 处，并按当前全书 reader 证据修复中册供电线损 `3732方于瓦时 -> 3732万千瓦时` 1 处。
- 本批合计修复 {total} 处；报告：`output/reports/reader_units_batch193_20260707.md`。
- 保留 `办公厅`、`列人` 跨词、`输人` 跨词及其它未逐源确认的 `方吨/方公斤/广` 候选；未打开、展示或嵌入图片。
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
    if full_text.count(FULL_EVIDENCE) != 1:
        raise SystemExit(f"full evidence count for {FULL_EVIDENCE!r} is {full_text.count(FULL_EVIDENCE)}")

    results = []
    total = 0
    for target, replacements in TARGET_REPLACEMENTS.items():
        before = target.read_text(encoding="utf-8")
        after = before
        per_file = []
        for old, new in replacements:
            count = after.count(old)
            if count:
                after = after.replace(old, new)
                per_file.append({"old": old, "new": new, "changed": count})
                total += count
        target.write_text(after, encoding="utf-8")
        after_text = plain(after)
        results.append({
            "target": str(target),
            "changed": sum(item["changed"] for item in per_file),
            "replacements": per_file,
            "remaining_bad_terms": {old: after_text.count(old) for old, _ in replacements},
        })

    payload = {
        "time": now,
        "changed": total,
        "full_evidence": FULL_EVIDENCE,
        "targets": results,
        "skipped": ["办公厅", "列人跨词", "输人跨词", "其它未逐源确认的方吨/方公斤/广候选"],
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# 单位错字补修第一百九十三批",
        "",
        f"> 生成时间：{now}",
        "",
        "## 范围",
        "",
        "- 当前中册、下册阅读稿。",
        "- 修复下册重量单位 `公厅 -> 公斤` 和中册供电线损 `方于瓦时 -> 万千瓦时`。",
        "- 未做大范围单位替换；未打开、展示或嵌入图片。",
        "",
        "## 统计",
        "",
        f"- 修复：{total} 处",
        "",
        "## 替换项",
        "",
    ]
    for result in results:
        lines.append(f"- `{result['target']}`：修复 {result['changed']} 处")
        for item in result["replacements"]:
            lines.append(f"  - `{item['old']}` -> `{item['new']}`：{item['changed']} 处")
    lines.extend(["", "## 保留边界", "", "- `办公厅`", "- `列人` 跨词：`序列人行道`", "- `输人` 跨词：`运输人员`", "- 其它未逐源确认的 `方吨/方公斤/广` 候选"])
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    PROGRESS.write_text(REPORT_MD.read_text(encoding="utf-8"), encoding="utf-8")
    upsert_memory(total)
    print(json.dumps({"changed": total, "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
