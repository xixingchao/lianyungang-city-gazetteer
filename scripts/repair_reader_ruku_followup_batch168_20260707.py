# -*- coding: utf-8 -*-
"""Repair remaining clear 入库 OCR residues."""

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
REPORT_JSON = ROOT / "output" / "reports" / "reader_ruku_followup_batch168_20260707.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_ruku_followup_batch168_20260707.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260707_入库残字跟进补修第一百六十八批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"
TERM = "人库"

REPLACEMENTS = [
    ("清理库房。人库</p><p>时", "清理库房。入库</p><p>时"),
    ("人库合</p><p>同定购粮", "入库合</p><p>同定购粮"),
    ("组</p><p>织人库", "组</p><p>织入库"),
    ("当</p><p>年人库", "当</p><p>年入库"),
]

LEFT_UNTOUCHED = [
    "`税年人库625.5万元` 已有项目记忆标注源 OCR 仍写 `人库`，本批继续不凭习惯替换。",
    "`出人库登记` 保留，后续如需要可按原文另核。",
    "未做裸词全局替换；未打开、展示或嵌入图片。",
]


def plain_text(html: str) -> str:
    return re.sub(r"<[^>]+>", "", html)


def contexts(plain: str, term: str) -> list[str]:
    return [plain[max(0, m.start() - 65):m.start() + 95].replace("\n", " ") for m in re.finditer(term, plain)]


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
    pattern_counts = {old: 0 for old, _ in REPLACEMENTS}
    results = []
    for target in TARGETS:
        before = target.read_text(encoding="utf-8")
        before_plain = plain_text(before)
        after = before
        file_patterns = []
        for old, new in REPLACEMENTS:
            count = after.count(old)
            if count:
                after = after.replace(old, new)
                pattern_counts[old] += count
                file_patterns.append({"old": old, "new": new, "count": count})
        target.write_text(after, encoding="utf-8")
        after_plain = plain_text(after)
        results.append({
            "target": str(target),
            "changed": sum(item["count"] for item in file_patterns),
            "before": before_plain.count(TERM),
            "after": after_plain.count(TERM),
            "patterns": file_patterns,
            "remaining_contexts": contexts(after_plain, TERM),
        })

    total = sum(item["changed"] for item in results)
    payload = {
        "time": now,
        "scope": "current reader remaining clear 入库 OCR repair",
        "changed": total,
        "pattern_counts": {k: v for k, v in pattern_counts.items() if v},
        "targets": results,
        "left_untouched": LEFT_UNTOUCHED,
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 入库残字跟进补修第一百六十八批",
        "",
        f"> 生成时间：{now}",
        "",
        "## 范围",
        "",
        "- 当前全书、中册、下册阅读稿。",
        "- 定点修复粮食、税款入库语境中的 `人库` 残字。",
        "- 未做裸词全局替换；未打开、展示或嵌入图片。",
        "",
        "## 统计",
        "",
        f"- 修复：{total} 处",
        "",
        "## 替换项",
        "",
    ]
    for old, count in sorted(((k, v) for k, v in pattern_counts.items() if v), key=lambda x: x[0]):
        lines.append(f"- `{old}` -> `{dict(REPLACEMENTS)[old]}`：{count} 处")
    lines.extend(["", "## 文件", ""])
    for item in results:
        lines.append(f"- `{item['target']}`：修复 {item['changed']} 处；剩余 `人库` {item['after']} 处")
    lines.extend(["", "## 未处理边界", ""])
    for item in LEFT_UNTOUCHED:
        lines.append(f"- {item}")
    report = "\n".join(lines) + "\n"
    REPORT_MD.write_text(report, encoding="utf-8")
    PROGRESS.write_text(report, encoding="utf-8")

    marker = "## 2026-07-07 高置信 OCR 错字补修第一百六十八批：入库跟进"
    upsert_memory(marker, f"""
{marker}

- 跟进当前中册阅读稿 `人库` 残留，定点修复 `入库时`、`入库合同定购粮`、`组织入库`、`当年入库`。
- 本批修复 {total} 处；报告：`output/reports/reader_ruku_followup_batch168_20260707.md`。
- 继续保留 `税年人库625.5万元` 与 `出人库登记` 边界；未打开、展示或嵌入图片。
""")
    print(json.dumps({"changed": total, "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
