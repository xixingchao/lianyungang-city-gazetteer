# -*- coding: utf-8 -*-
"""Follow-up repair for 入 OCR candidates missed by first pass."""

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
REPORT_JSON = ROOT / "output" / "reports" / "reader_ru_candidates_followup_batch170_20260707.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_ru_candidates_followup_batch170_20260707.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260707_入字候选跟进补修第一百七十批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"
TERMS = ["列人", "迁人", "划人", "编人"]

REGEX_REPLACEMENTS = [
    (r"列人省医药公司", "列入省医药公司", "列入省医药公司"),
    (r"迁人(?=市工艺|新浦|连云港市|开发区|新址|新馆|者有|墟沟镇|新教堂)", "迁入", "迁入厂址/新址/新馆/迁居语境"),
    (r"迁人手续", "迁入手续", "迁入手续"),
    (r"划人金库", "划入金库", "划入金库"),
    (r"编人(?=预备役|东海县常备大队)", "编入", "编入预备役/常备大队"),
]

LEFT_UNTOUCHED = [
    "`宿迁人` 为籍贯/人物说明，保留。",
    "`采编人员/在编人员/扩编人防` 等合法相邻字保留。",
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
        "scope": "current reader 入 OCR candidate follow-up repair",
        "changed": total,
        "pattern_counts": {k: v for k, v in pattern_counts.items() if v},
        "targets": results,
        "left_untouched": LEFT_UNTOUCHED,
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 入字候选跟进补修第一百七十批",
        "",
        f"> 生成时间：{now}",
        "",
        "## 范围",
        "",
        "- 当前全书、中册、下册阅读稿。",
        "- 跟进修复 `列入/迁入/划入/编入` 高置信漏项。",
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

    marker = "## 2026-07-07 高置信 OCR 错字补修第一百七十批：入字候选跟进"
    upsert_memory(marker, f"""
{marker}

- 跟进 `batch169` 后 `列人/迁人/划人/编人` 残留，修复列入省医药公司、迁入厂址/新址/新馆、划入金库、编入预备役/常备大队等高置信项。
- 本批修复 {total} 处；报告：`output/reports/reader_ru_candidates_followup_batch170_20260707.md`。
- 保留 `宿迁人`、`采编人员/在编人员/扩编人防` 等合法相邻字；未打开、展示或嵌入图片。
""")
    print(json.dumps({"changed": total, "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
