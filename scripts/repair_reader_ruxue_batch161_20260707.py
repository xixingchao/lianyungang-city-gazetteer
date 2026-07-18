# -*- coding: utf-8 -*-
"""Repair high-confidence 人学 OCR residues to 入学."""

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
REPORT_JSON = ROOT / "output" / "reports" / "reader_ruxue_batch161_20260707.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_ruxue_batch161_20260707.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260707_人学残字补修第一百六十一批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"
TERM = "人学"

REPLACEMENTS = [
    ("小孩人学", "小孩入学"),
    ("子女人学", "子女入学"),
    ("平民子女人学", "平民子女入学"),
    ("应人学聋儿童", "应入学聋儿童"),
    ("犯人人学率", "犯人入学率"),
    ("对人学学生", "对入学学生"),
    ("人学学生", "入学学生"),
    ("人学职工", "入学职工"),
    ("人学前班", "入学前班"),
    ("幼儿人学", "幼儿入学"),
    ("学生人学年龄", "学生入学年龄"),
    ("儿童6岁人学", "儿童6岁入学"),
    ("小学人学年龄", "小学入学年龄"),
    ("人学年龄", "入学年龄"),
    ("人学教育", "入学教育"),
    ("师范生人学", "师范生入学"),
    ("中小学人学新生", "中小学入学新生"),
    ("残疾儿童人学", "残疾儿童入学"),
    ("学龄儿童人学率", "学龄儿童入学率"),
    ("小学生人学率", "小学生入学率"),
    ("人学率", "入学率"),
]

LEGAL_LEFT = [
    "聋哑人学校",
    "人学习",
    "人学完",
    "人学拳术",
    "郡人学博",
]


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
    pattern_counts = {old: 0 for old, _ in REPLACEMENTS}
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
            "before": before_plain.count(TERM),
            "changed": sum(item["count"] for item in file_patterns),
            "after": after_plain.count(TERM),
            "patterns": file_patterns,
            "remaining_contexts": contexts(after_plain, TERM),
        })

    total = sum(item["changed"] for item in results)
    payload = {
        "time": now,
        "scope": "current reader high-confidence 人学 OCR residue repair",
        "changed": total,
        "pattern_counts": {k: v for k, v in pattern_counts.items() if v},
        "targets": results,
        "legal_left": LEGAL_LEFT,
        "note": "No naked 人学 replacement; no images opened or embedded.",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 人学残字补修第一百六十一批",
        "",
        f"> 生成时间：{now}",
        "",
        "## 范围",
        "",
        "- 当前全书、中册、下册阅读稿。",
        "- 仅修复教育语境中可判定为 `入学` 的 `人学` 残字。",
        "- 未打开、展示或嵌入图片。",
        "",
        "## 统计",
        "",
        f"- 修复：{total} 处",
        "",
        "## 替换项",
        "",
    ]
    for old, count in sorted(((k, v) for k, v in pattern_counts.items() if v), key=lambda x: x[0]):
        new = dict(REPLACEMENTS)[old]
        lines.append(f"- `{old}` -> `{new}`：{count} 处")
    lines.extend(["", "## 文件", ""])
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
    lines.extend(["", "## 未处理边界", ""])
    for item in LEGAL_LEFT:
        lines.append(f"- `{item}` 语境保留。")
    report = "\n".join(lines) + "\n"
    REPORT_MD.write_text(report, encoding="utf-8")
    PROGRESS.write_text(report, encoding="utf-8")

    marker = "## 2026-07-07 高置信 OCR 错字补修第一百六十一批：人学残字"
    upsert_memory(marker, f"""
{marker}

- 核对当前阅读稿 `人学`，区分 `入学` OCR 残字与合法相邻字（如 `聋哑人学校`、`人学习`、`人学完`、`郡人学博`）。
- 本批仅修复教育语境高置信 `入学` 项，共 {total} 处；报告：`output/reports/reader_ruxue_batch161_20260707.md`。
- 未做裸 `人学 -> 入学` 替换；未打开、展示或嵌入图片。
""")
    print(json.dumps({"changed": total, "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
