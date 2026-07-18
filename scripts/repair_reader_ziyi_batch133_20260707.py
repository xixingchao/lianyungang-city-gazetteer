# -*- coding: utf-8 -*-
"""Repair OCR residue 自已 -> 自己, preserving classical 不能自已."""

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
REPORT_JSON = ROOT / "output" / "reports" / "reader_ziyi_batch133_20260707.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_ziyi_batch133_20260707.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260707_自已残字回源补修第一百三十三批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

PRESERVE = "不能自已"


def contexts(plain: str, term: str) -> list[str]:
    out = []
    for m in re.finditer(term, plain):
        out.append(plain[max(0, m.start() - 45):m.start() + 70].replace("\n", " "))
    return out


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


def repair_text(text: str) -> tuple[str, int, int]:
    protected = "__PRESERVE_BU_NENG_ZI_YI__"
    preserve_count = text.count(PRESERVE)
    work = text.replace(PRESERVE, protected)
    changed = work.count("自已")
    work = work.replace("自已", "自己")
    split_changed = work.count("自</p><p>已")
    work = work.replace("自</p><p>已", "自</p><p>己")
    return work.replace(protected, PRESERVE), changed + split_changed, preserve_count


def main() -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    results = []
    for target in TARGETS:
        before = target.read_text(encoding="utf-8")
        before_plain = re.sub(r"<[^>]+>", "", before)
        after, changed, preserved = repair_text(before)
        target.write_text(after, encoding="utf-8")
        after_plain = re.sub(r"<[^>]+>", "", after)
        results.append({
            "target": str(target),
            "before": before_plain.count("自已"),
            "changed": changed,
            "preserved_bunengziyi": preserved,
            "after": after_plain.count("自已"),
            "remaining_contexts": contexts(after_plain, "自已"),
        })

    total_changed = sum(item["changed"] for item in results)
    payload = {
        "time": now,
        "scope": "current full/middle/lower reader OCR residue 自已 repair",
        "changed": total_changed,
        "targets": results,
        "left_untouched": [
            "`不能自已` 为固定书面语/古文用法，本批保留。",
            "本批没有打开、展示或嵌入图片。",
        ],
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 自已残字补修第一百三十三批",
        "",
        f"> 生成时间：{now}",
        "",
        "## 范围",
        "",
        "- 当前全书、中册、下册阅读稿。",
        "- 将正文语境中的 `自已` 修为 `自己`，保留固定用语 `不能自已`。",
        "",
        "## 统计",
        "",
        f"- 修复：{total_changed} 处",
        "",
        "## 文件",
        "",
    ]
    for item in results:
        lines.append(
            f"- `{item['target']}`：修复 {item['changed']} 处，保留 `不能自已` {item['preserved_bunengziyi']} 处，剩余 `自已` {item['after']} 处"
        )
    lines.extend(["", "## 剩余边界", ""])
    remaining = False
    for item in results:
        for ctx in item["remaining_contexts"]:
            remaining = True
            lines.append(f"- `{item['target']}`：{ctx}")
    if not remaining:
        lines.append("- 无。")
    lines.extend(["", "## 未处理边界", ""])
    for item in payload["left_untouched"]:
        lines.append(f"- {item}")
    report = "\n".join(lines) + "\n"
    REPORT_MD.write_text(report, encoding="utf-8")
    PROGRESS.write_text(report, encoding="utf-8")

    marker = "## 2026-07-07 高置信 OCR 错字补修第一百三十三批：自已残字"
    upsert_memory(marker, f"""
{marker}

- 对当前全书/中册/下册阅读稿核修 `自已` 残字：正文语境改为 `自己`，固定书面语/古文 `不能自已` 保留。
- 本批修复 {total_changed} 处；报告：`output/reports/reader_ziyi_batch133_20260707.md`。
- 未打开、展示或嵌入图片。
""")
    print(json.dumps({"changed": total_changed, "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()

