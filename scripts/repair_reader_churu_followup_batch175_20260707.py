# -*- coding: utf-8 -*-
"""Follow-up repair for high-confidence 出入 OCR residues."""

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
REPORT_JSON = ROOT / "output" / "reports" / "reader_churu_followup_batch175_20260707.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_churu_followup_batch175_20260707.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260707_出入残字补修第一百七十五批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"
TERMS = ["出人"]

REPLACEMENTS = [
    ("查验出人连云港口岸", "查验出入连云港口岸", "查验出入连云港口岸"),
    ("出人国境治安暂行条例", "出入国境治安暂行条例", "出入国境治安暂行条例"),
    ("新的输出人港", "新的输出入港", "新的输出入港"),
]

LEFT_UNTOUCHED = [
    "`无出人或出人不大` 暂留待源文核对。",
    "`杰出人物/出生未入户/抽出人员/兑人金额` 等合法或不稳定边界保留。",
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
        "scope": "current reader high-confidence 出入 OCR follow-up",
        "changed": total,
        "pattern_counts": {k: v for k, v in pattern_counts.items() if v},
        "targets": results,
        "left_untouched": LEFT_UNTOUCHED,
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 出入残字补修第一百七十五批",
        "",
        f"> 生成时间：{now}",
        "",
        "## 范围",
        "",
        "- 当前全书、中册、下册阅读稿。",
        "- 修复口岸、国境、港口语境中的 `出入` 高置信 OCR 残字。",
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

    marker = "## 2026-07-07 高置信 OCR 错字补修第一百七十五批：出入候选补遗"
    upsert_memory(marker, f"""
{marker}

- 跟进 batch174 后剩余 `出人`，只修复口岸/国境/港口语境 `出入` 高置信项。
- 本批修复 {total} 处；报告：`output/reports/reader_churu_followup_batch175_20260707.md`。
- 暂留 `无出人或出人不大` 待源文核对；未打开、展示或嵌入图片。
""")
    print(json.dumps({"changed": total, "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
