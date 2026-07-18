# -*- coding: utf-8 -*-
"""Follow-up repair for high-confidence 入 OCR residues after batch172."""

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
REPORT_JSON = ROOT / "output" / "reports" / "reader_ru_verbs_batch173_20260707.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_ru_verbs_batch173_20260707.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260707_入字动词残字补修第一百七十三批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"
TERMS = ["纳人", "陷人", "流人"]

REPLACEMENTS = [
    (r"纳(?P<gap>(?:<[^>]+>)+)人地方预算", r"纳\g<gap>入地方预算", "纳入地方预算"),
    (r"纳(?P<gap>(?:<[^>]+>)+)人市人民银行宏观控制之内", r"纳\g<gap>入市人民银行宏观控制之内", "纳入宏观控制"),
    (r"陷(?P<gap>(?:<[^>]+>)+)人敌人重围", r"陷\g<gap>入敌人重围", "陷入敌人重围"),
    (r"徽剧、(?P<gap1>(?:<[^>]+>)+)京剧的流(?P<gap2>(?:<[^>]+>)+)人", r"徽剧、\g<gap1>京剧的流\g<gap2>入", "剧种流入"),
    (r"徽剧、(?P<gap>(?:<[^>]+>)+)京剧的流人", r"徽剧、\g<gap>京剧的流入", "剧种流入分册残留"),
]

LEFT_UNTOUCHED = [
    "`缺陷人口` 为合法词，未改。",
    "`外流人员/内流人员/抓流人员` 等社会救济语境保留。",
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
    pattern_counts = {label: 0 for _, _, label in REPLACEMENTS}
    results = []
    for target in TARGETS:
        before = target.read_text(encoding="utf-8")
        before_plain = plain_text(before)
        after = before
        file_patterns = []
        for pattern, replacement, label in REPLACEMENTS:
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
        "scope": "current reader high-confidence 入 verb OCR follow-up",
        "changed": total,
        "pattern_counts": {k: v for k, v in pattern_counts.items() if v},
        "targets": results,
        "left_untouched": LEFT_UNTOUCHED,
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 入字动词残字补修第一百七十三批",
        "",
        f"> 生成时间：{now}",
        "",
        "## 范围",
        "",
        "- 当前全书、中册、下册阅读稿。",
        "- 修复 batch172 后残留的 `纳入/陷入/流入` 高置信项。",
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

    marker = "## 2026-07-07 高置信 OCR 错字补修第一百七十三批：入字动词候选补遗"
    upsert_memory(marker, f"""
{marker}

- 复扫 batch172 后残留 `纳人/陷人/流人`，只修复短语白名单命中的高置信项。
- 本批修复 {total} 处；报告：`output/reports/reader_ru_verbs_batch173_20260707.md`。
- 保留 `缺陷人口`、`外流人员/内流人员/抓流人员` 等边界；未打开、展示或嵌入图片。
""")
    print(json.dumps({"changed": total, "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
