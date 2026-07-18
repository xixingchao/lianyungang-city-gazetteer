# -*- coding: utf-8 -*-
"""Repair follow-up high-confidence 入 OCR residues."""

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
REPORT_JSON = ROOT / "output" / "reports" / "reader_ru_followup_batch179_20260707.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_ru_followup_batch179_20260707.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260707_入字高置信补修第一百七十九批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"
TERMS = ["拨人数为", "有线电视人户率", "考人"]

REPLACEMENTS = [
    ("拨人数为", "拨入数为", "拨入数为"),
    ("有线电视人户率", "有线电视入户率", "有线电视入户率"),
    ("考人江苏省立第十中学", "考入江苏省立第十中学", "考入江苏省立第十中学"),
    ("考人上海同济大学", "考入上海同济大学", "考入上海同济大学"),
    ("考人东海中学师范科", "考入东海中学师范科", "考入东海中学师范科"),
    ("考人江苏省立连云水产学校师范班", "考入江苏省立连云水产学校师范班", "考入连云水产学校"),
    ("考人江苏省立东海师范学校", "考入江苏省立东海师范学校", "考入东海师范学校"),
    ("考人灌云县立初级中学", "考入灌云县立初级中学", "考入灌云县立初级中学"),
    ("考人燕京大学", "考入燕京大学", "考入燕京大学"),
]

LEFT_UNTOUCHED = [
    "`统考人数/参加统考人数` 等合法相邻字保留。",
    "`安排人事/安排人力`、`归人民政府` 等合法相邻字保留。",
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
        "scope": "current reader high-confidence 入 OCR follow-up repair",
        "changed": total,
        "pattern_counts": {k: v for k, v in pattern_counts.items() if v},
        "targets": results,
        "left_untouched": LEFT_UNTOUCHED,
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 入字高置信补修第一百七十九批",
        "",
        f"> 生成时间：{now}",
        "",
        "## 范围",
        "",
        "- 当前全书、中册、下册阅读稿。",
        "- 修复 `拨入数/入户率/考入` 高置信 OCR 残字。",
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

    marker = "## 2026-07-07 高置信 OCR 错字补修第一百七十九批：入字高置信补遗"
    upsert_memory(marker, f"""
{marker}

- 核对当前阅读稿 `拨人数为/有线电视人户率/考人学校` 上下文，定点修复 `拨入数为/有线电视入户率/考入学校` 高置信项。
- 本批修复 {total} 处；报告：`output/reports/reader_ru_followup_batch179_20260707.md`。
- 保留 `统考人数/安排人事/归人民政府` 等合法边界；未打开、展示或嵌入图片。
""")
    print(json.dumps({"changed": total, "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
