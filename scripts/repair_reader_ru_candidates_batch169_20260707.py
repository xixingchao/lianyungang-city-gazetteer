# -*- coding: utf-8 -*-
"""Repair high-confidence 入 OCR residues from 列/迁/混/划/编 groups."""

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
REPORT_JSON = ROOT / "output" / "reports" / "reader_ru_candidates_batch169_20260707.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_ru_candidates_batch169_20260707.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260707_入字候选残字补修第一百六十九批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"
TERMS = ["列人", "迁人", "混人", "划人", "编人"]

REGEX_REPLACEMENTS = [
    (r"(?<!序)列人", "列入", "非 `序列人行道` 的 `列人`"),
    (r"迁人内地", "迁入内地", "迁入内地"),
    (r"混人革命根据地", "混入革命根据地", "混入革命根据地"),
    (r"划人(?=市级预算|行政支出|东海县|江苏省|连云港市|云台区|4家工厂)", "划入", "划入行政/预算/区划/企业语境"),
    (r"编人(?=现役|主力|华中|九十八军|八路军|该团|灌云县|华东|预备役|县长|东海县|新四军|中国国民党|滨海|主攻团)", "编入", "编入军队/预备役语境"),
]

LEFT_UNTOUCHED = [
    "`数值序列人行道面积` 保留为表格说明中的合法相邻字。",
    "`采编人员/在编人员/扩编人防/编人员` 等合法编制或采编语境保留。",
    "未做裸 `人 -> 入` 替换；未打开、展示或嵌入图片。",
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
    pattern_counts = {label: 0 for _, _, label in REGEX_REPLACEMENTS}
    results = []
    for target in TARGETS:
        before = target.read_text(encoding="utf-8")
        before_plain = plain_text(before)
        after = before
        file_patterns = []
        for pattern, replacement, label in REGEX_REPLACEMENTS:
            after, count = re.subn(pattern, replacement, after)
            if count:
                pattern_counts[label] += count
                file_patterns.append({"pattern": pattern, "replacement": replacement, "label": label, "count": count})
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
        "scope": "current reader high-confidence 入 OCR candidate repair",
        "changed": total,
        "pattern_counts": {k: v for k, v in pattern_counts.items() if v},
        "targets": results,
        "left_untouched": LEFT_UNTOUCHED,
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 入字候选残字补修第一百六十九批",
        "",
        f"> 生成时间：{now}",
        "",
        "## 范围",
        "",
        "- 当前全书、中册、下册阅读稿。",
        "- 修复 `列入/迁入/混入/划入/编入` 高置信 OCR 残字。",
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

    marker = "## 2026-07-07 高置信 OCR 错字补修第一百六十九批：入字候选"
    upsert_memory(marker, f"""
{marker}

- 核对当前阅读稿 `列人/迁人/混人/划人/编人` 上下文，修复 `列入/迁入/混入/划入/编入` 高置信残字。
- 本批修复 {total} 处；报告：`output/reports/reader_ru_candidates_batch169_20260707.md`。
- 保留 `数值序列人行道面积`、`采编人员/在编人员/扩编人防` 等合法相邻字；未打开、展示或嵌入图片。
""")
    print(json.dumps({"changed": total, "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
