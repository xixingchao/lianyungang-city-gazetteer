# -*- coding: utf-8 -*-
"""Repair high-confidence 放入/插入/送入/装入 OCR residues."""

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
REPORT_JSON = ROOT / "output" / "reports" / "reader_ru_motion_batch180_20260707.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_ru_motion_batch180_20260707.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260707_放入送入残字补修第一百八十批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"
TERMS = ["放人醋中", "插人在竹制", "送人流通书库", "送人阅览室", "装人日本货轮", "非植人型电子耳蜗", "排人课表"]

REPLACEMENTS = [
    ("放人醋中", "放入醋中", "放入醋中"),
    ("装人日本货轮", "装入日本货轮", "装入日本货轮"),
    ("插人在竹制", "插入在竹制", "插入竹制笔套"),
    ("送一套人基藏书库", "送一套入基藏书库", "送入基藏书库"),
    ("送人流通书库", "送入流通书库", "送入流通书库"),
    ("送人阅览室", "送入阅览室", "送入阅览室"),
    ("非植人型电子耳蜗", "非植入型电子耳蜗", "非植入型电子耳蜗"),
    ("排人课表", "排入课表", "排入课表"),
]

LEFT_UNTOUCHED = [
    "`投放人工鱼礁/安排人力/释放人犯/安装人工/铺装人行道` 等合法相邻字保留。",
    "`送一套入基藏书库` 保留原文 `基藏书库` 术语，只修 `人 -> 入`。",
    "未做裸 `人 -> 入` 替换；未打开、展示或嵌入图片。",
]


def tag_tolerant_pattern(text: str) -> str:
    return r"(?:<[^>]+>)*".join(re.escape(ch) for ch in text)


def tag_preserving_replacement(dest: str):
    def repl(match: re.Match[str]) -> str:
        out: list[str] = []
        char_index = 0
        for piece in re.split(r"(<[^>]+>)", match.group(0)):
            if not piece:
                continue
            if piece.startswith("<"):
                out.append(piece)
            else:
                for _ in piece:
                    out.append(dest[char_index])
                    char_index += 1
        return "".join(out)

    return repl


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
    pattern_counts = {label: 0 for _, _, label in REPLACEMENTS}
    results = []
    compiled = [(tag_tolerant_pattern(src), tag_preserving_replacement(dst), label) for src, dst, label in REPLACEMENTS]

    for target in TARGETS:
        before = target.read_text(encoding="utf-8")
        before_plain = plain_text(before)
        after = before
        file_patterns = []
        for pattern, replacement, label in compiled:
            after, count = re.subn(pattern, replacement, after)
            if count:
                pattern_counts[label] += count
                file_patterns.append({"pattern": pattern, "label": label, "count": count})
        target.write_text(after, encoding="utf-8")
        after_plain = plain_text(after)
        results.append({
            "target": str(target),
            "changed": sum(item["count"] for item in file_patterns),
            "before_terms": {term: before_plain.count(term) for term in TERMS},
            "after_terms": {term: after_plain.count(term) for term in TERMS},
            "patterns": file_patterns,
            "remaining_contexts": {term: contexts(after_plain, term) for term in TERMS if after_plain.count(term)},
        })

    total = sum(item["changed"] for item in results)
    payload = {
        "time": now,
        "scope": "current reader high-confidence motion 入 OCR repair",
        "changed": total,
        "pattern_counts": {k: v for k, v in pattern_counts.items() if v},
        "targets": results,
        "left_untouched": LEFT_UNTOUCHED,
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 放入送入残字补修第一百八十批",
        "",
        f"> 生成时间：{now}",
        "",
        "## 范围",
        "",
        "- 当前全书、中册、下册阅读稿。",
        "- 修复 `放入/插入/送入/装入/排入/植入` 高置信 OCR 残字。",
        "- 未做裸 `人 -> 入` 替换；未打开、展示或嵌入图片。",
        "",
        "## 统计",
        "",
        f"- 修复：{total} 处",
        "",
        "## 替换项",
        "",
    ]
    for label, count in sorted(((k, v) for k, v in pattern_counts.items() if v), key=lambda x: x[0]):
        lines.append(f"- {label}：{count} 处")
    lines.extend(["", "## 文件", ""])
    for item in results:
        after_bits = ", ".join(f"{k}:{v}" for k, v in item["after_terms"].items() if v)
        lines.append(f"- `{item['target']}`：修复 {item['changed']} 处；剩余 {after_bits or '无'}")
    lines.extend(["", "## 未处理边界", ""])
    for item in LEFT_UNTOUCHED:
        lines.append(f"- {item}")
    report = "\n".join(lines) + "\n"
    REPORT_MD.write_text(report, encoding="utf-8")
    PROGRESS.write_text(report, encoding="utf-8")

    marker = "## 2026-07-07 高置信 OCR 错字补修第一百八十批：放入送入候选"
    upsert_memory(marker, f"""
{marker}

- 核对当前阅读稿 `放人/插人/送人/装人/排人` 上下文，定点修复 `放入/插入/送入/装入/排入/植入` 高置信项。
- 本批修复 {total} 处；报告：`output/reports/reader_ru_motion_batch180_20260707.md`。
- 保留 `投放人工鱼礁/安排人力/释放人犯/安装人工/铺装人行道` 等合法边界；未打开、展示或嵌入图片。
""")
    print(json.dumps({"changed": total, "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
