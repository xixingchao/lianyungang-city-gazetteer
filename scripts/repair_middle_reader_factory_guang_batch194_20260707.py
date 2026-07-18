# -*- coding: utf-8 -*-
"""Repair middle-reader factory OCR residues where 厂 was read as 广."""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MIDDLE = ROOT / "output" / "final_reader" / "连云港市志_中册.html"
FULL = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "middle_reader_factory_guang_batch194_20260707.json"
REPORT_MD = ROOT / "output" / "reports" / "middle_reader_factory_guang_batch194_20260707.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260707_中册厂字残留补修第一百九十四批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    ("广房", "厂房"),
    ("广内", "厂内"),
    ("该广", "该厂"),
    ("化肥广", "化肥厂"),
]
SKIPPED = ["市广", "本广", "日本广播", "市广播", "全市广大"]


def plain(html: str) -> str:
    return re.sub(r"<[^>]+>", "", html)


def contexts(text: str, term: str) -> list[str]:
    return [text[max(0, m.start() - 60):m.start() + 100].replace("\n", " ") for m in re.finditer(re.escape(term), text)]


def upsert_memory(total: int, remaining: dict[str, int]) -> None:
    marker = "## 2026-07-07 高置信 OCR 错字补修第一百九十四批：中册厂字残留"
    old = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    rem = ", ".join(f"{k}:{v}" for k, v in remaining.items())
    block = f"""
{marker}

- 复核中册 `广` 类残留，`广房/广内/该广/化肥广` 均处在企业厂房、厂内、该厂、化肥厂语境；当前全书 reader 对应残字为 0。
- 已仅在 `output/final_reader/连云港市志_中册.html` 定点修复 {total} 处；报告：`output/reports/middle_reader_factory_guang_batch194_20260707.md`。
- 保留 `市广/本广` 等广播、广大跨词边界；修后中册相关残留：{rem}；未打开、展示或嵌入图片。
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
    full_residue = {old: full_text.count(old) for old, _ in REPLACEMENTS}
    if any(full_residue.values()):
        raise SystemExit(f"full reader still has target residue: {full_residue}")

    before = MIDDLE.read_text(encoding="utf-8")
    before_text = plain(before)
    before_contexts = {old: contexts(before_text, old) for old, _ in REPLACEMENTS}
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
    remaining = {old: after_text.count(old) for old, _ in REPLACEMENTS}

    payload = {
        "time": now,
        "changed": total,
        "full_residue_before": full_residue,
        "middle_before_contexts": before_contexts,
        "middle_remaining": remaining,
        "replacements": changed_items,
        "skipped": SKIPPED,
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# 中册厂字残留补修第一百九十四批",
        "",
        f"> 生成时间：{now}",
        "",
        "## 范围",
        "",
        "- 当前中册阅读稿。",
        "- 修复企业语境中 `广` 对 `厂` 的 OCR 误识。",
        "- 未处理 `市广/本广` 等广播、广大跨词边界；未打开、展示或嵌入图片。",
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
    lines.extend(["", "## 保留边界", ""])
    for item in SKIPPED:
        lines.append(f"- `{item}`")
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    PROGRESS.write_text(REPORT_MD.read_text(encoding="utf-8"), encoding="utf-8")
    upsert_memory(total, remaining)
    print(json.dumps({"changed": total, "remaining": remaining, "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
