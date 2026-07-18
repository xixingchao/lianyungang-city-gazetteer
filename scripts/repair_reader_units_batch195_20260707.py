# -*- coding: utf-8 -*-
"""Repair verified 万公斤/万头 unit residues in split readers."""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FULL = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
MIDDLE = ROOT / "output" / "final_reader" / "连云港市志_中册.html"
LOWER = ROOT / "output" / "final_reader" / "连云港市志_下册.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_units_batch195_20260707.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_units_batch195_20260707.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260707_单位错字补修第一百九十五批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

TARGET_REPLACEMENTS = {
    MIDDLE: [
        ("全年收购本地菜1357方公斤", "全年收购本地菜1357万公斤"),
        ("小麦11.12方公斤", "小麦11.12万公斤"),
        ("小麦78.84方公斤", "小麦78.84万公斤"),
        ("粮食788方公斤", "粮食788万公斤"),
        ("人均收入4.5方公斤", "人均收入4.5万公斤"),
        ("贸易粮5方公斤", "贸易粮5万公斤"),
        ("当年宰杀22方头", "当年宰杀22万头"),
        ("年宰量36方头", "年宰量36万头"),
        ("生猪存栏101方头", "生猪存栏101万头"),
    ],
    LOWER: [
        ("运肥1250方公斤", "运肥1250万公斤"),
    ],
}

SKIPPED = ["方头鱼", "方头乳鸽", "地方头人", "方立方米", "其它未逐源确认的方吨候选"]


def plain(html: str) -> str:
    return re.sub(r"<[^>]+>", "", html)


def upsert_memory(total: int, remaining: dict[str, dict[str, int]]) -> None:
    marker = "## 2026-07-07 高置信 OCR 错字补修第一百九十五批：万公斤万头单位"
    old = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    block = f"""
{marker}

- 对照当前全书 reader 正确文本，修复分册中 `方公斤/方头` 对 `万公斤/万头` 的单位错识：中册 9 处、下册 1 处。
- 本批仅替换已核完整短语，合计修复 {total} 处；报告：`output/reports/reader_units_batch195_20260707.md`。
- 保留 `方头鱼/方头乳鸽/地方头人/方立方米/其它未逐源确认的方吨候选`；未打开、展示或嵌入图片。
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
    evidence = {}
    for replacements in TARGET_REPLACEMENTS.values():
        for _old, new in replacements:
            evidence[new] = full_text.count(new)
    missing = {term: count for term, count in evidence.items() if count < 1}
    if missing:
        raise SystemExit(f"missing full-reader evidence: {missing}")

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
            "remaining_bad_terms": {old: after_text.count(old) for old, _new in replacements},
        })

    remaining = {Path(r["target"]).name: r["remaining_bad_terms"] for r in results}
    payload = {
        "time": now,
        "changed": total,
        "full_evidence_counts": evidence,
        "targets": results,
        "skipped": SKIPPED,
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 单位错字补修第一百九十五批",
        "",
        f"> 生成时间：{now}",
        "",
        "## 范围",
        "",
        "- 当前中册、下册阅读稿。",
        "- 以当前全书 reader 正确句为证据，修复分册 `方公斤/方头` 对 `万公斤/万头` 的单位错识。",
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
    lines.extend(["", "## 保留边界", ""])
    for item in SKIPPED:
        lines.append(f"- `{item}`")
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    PROGRESS.write_text(REPORT_MD.read_text(encoding="utf-8"), encoding="utf-8")
    upsert_memory(total, remaining)
    print(json.dumps({"changed": total, "remaining": remaining, "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
