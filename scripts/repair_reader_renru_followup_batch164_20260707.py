# -*- coding: utf-8 -*-
"""Follow-up repairs for split high-confidence 人/入 OCR residues."""

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
REPORT_JSON = ROOT / "output" / "reports" / "reader_renru_followup_batch164_20260707.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_renru_followup_batch164_20260707.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260707_人入残字跟进补修第一百六十四批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"
TERMS = ["加人", "人库", "人选"]

REPLACEMENTS = [
    ("加</p><p>人中国共产党", "加入</p><p>中国共产党"),
    ("加</p><p>人共产党", "加入</p><p>共产党"),
    ("征超议购人库", "征超议购入库"),
    ("人选原矿品位", "入选原矿品位"),
    ("老人人选", "老人入选"),
]

LEFT_UNTOUCHED = [
    "`参加人数/参加人员/增加人员` 等合法相邻字保留。",
    "`代表人选/人选名单/组成人员的人选` 等候选人语义保留。",
    "未做裸词全局替换；未打开、展示或嵌入图片。",
]


def plain_text(html: str) -> str:
    return re.sub(r"<[^>]+>", "", html)


def contexts(plain: str, term: str) -> list[str]:
    return [plain[max(0, m.start() - 55):m.start() + 85].replace("\n", " ") for m in re.finditer(term, plain)]


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
            "before_terms": {term: before_plain.count(term) for term in TERMS},
            "after_terms": {term: after_plain.count(term) for term in TERMS},
            "patterns": file_patterns,
            "remaining_contexts": {term: contexts(after_plain, term) for term in TERMS if after_plain.count(term)},
        })

    total = sum(item["changed"] for item in results)
    payload = {
        "time": now,
        "scope": "current reader follow-up high-confidence 人/入 OCR repair",
        "changed": total,
        "pattern_counts": {k: v for k, v in pattern_counts.items() if v},
        "targets": results,
        "left_untouched": LEFT_UNTOUCHED,
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 人入残字跟进补修第一百六十四批",
        "",
        f"> 生成时间：{now}",
        "",
        "## 范围",
        "",
        "- 当前全书、中册、下册阅读稿。",
        "- 定点修复跨段 `加入中国共产党`、`入库`、`入选` 高置信残留。",
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
        after_bits = ", ".join(f"{k}:{v}" for k, v in item["after_terms"].items() if v)
        lines.append(f"- `{item['target']}`：修复 {item['changed']} 处；剩余 {after_bits or '无'}")
    lines.extend(["", "## 未处理边界", ""])
    for item in LEFT_UNTOUCHED:
        lines.append(f"- {item}")
    report = "\n".join(lines) + "\n"
    REPORT_MD.write_text(report, encoding="utf-8")
    PROGRESS.write_text(report, encoding="utf-8")

    marker = "## 2026-07-07 高置信 OCR 错字补修第一百六十四批：人入跟进"
    upsert_memory(marker, f"""
{marker}

- 跟进 `batch163` 后残留，定点修复跨段 `加入中国共产党/加入共产党`、`征超议购入库`、`入选原矿品位`、`老人入选`。
- 本批修复 {total} 处；报告：`output/reports/reader_renru_followup_batch164_20260707.md`。
- 保留 `参加人数/增加人员` 与候选人语义 `人选`；未打开、展示或嵌入图片。
""")
    print(json.dumps({"changed": total, "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
