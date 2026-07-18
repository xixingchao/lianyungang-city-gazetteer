# -*- coding: utf-8 -*-
"""Follow-up repairs for remaining high-confidence 人/入 residues."""

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
REPORT_JSON = ROOT / "output" / "reports" / "reader_renru_followup_batch166_20260707.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_renru_followup_batch166_20260707.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260707_人入残字跟进补修第一百六十六批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"
TERMS = ["人库", "人选", "人社", "加人"]

REPLACEMENTS = [
    ("灌云县人</p><p>库公粮", "灌云县入</p><p>库公粮"),
    ("人库时", "入库时"),
    ("人库合同", "入库合同"),
    ("组织人库", "组织入库"),
    ("当年人库", "当年入库"),
    ("税年人库", "税款入库"),
    ("编自、人</p><p>库", "编目、入</p><p>库"),
    ("人社股金", "入社股金"),
    ("（人选江苏省男子足球队", "（入选江苏省男子足球队"),
    ("后又人选国家女子足球队", "后又入选国家女子足球队"),
    ("加人中国共产党", "加入中国共产党"),
]

LEFT_UNTOUCHED = [
    "候选人语义 `组成人员的人选/代表人选/人选名单` 保留。",
    "合法相邻字 `出人库登记` 保留为出入库语义边界，不在本批改写。",
    "合法相邻字 `参加人数/参加人员/增加人员/泥人厂/负责人社址` 保留。",
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
        "scope": "current reader remaining high-confidence 人/入 OCR repair",
        "changed": total,
        "pattern_counts": {k: v for k, v in pattern_counts.items() if v},
        "targets": results,
        "left_untouched": LEFT_UNTOUCHED,
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 人入残字跟进补修第一百六十六批",
        "",
        f"> 生成时间：{now}",
        "",
        "## 范围",
        "",
        "- 当前全书、中册、下册阅读稿。",
        "- 定点修复剩余高置信 `入库/入社/入选/加入` 残字。",
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

    marker = "## 2026-07-07 高置信 OCR 错字补修第一百六十六批：人入跟进二"
    upsert_memory(marker, f"""
{marker}

- 跟进当前阅读稿剩余 `人库/人选/人社/加人`，定点修复入库、入社股金、入选足球队、加入中国共产党等高置信项。
- 本批修复 {total} 处；报告：`output/reports/reader_renru_followup_batch166_20260707.md`。
- 保留候选人 `人选`、`出人库登记`、`参加人数/增加人员/泥人厂/负责人社址` 等合法边界；未打开、展示或嵌入图片。
""")
    print(json.dumps({"changed": total, "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
