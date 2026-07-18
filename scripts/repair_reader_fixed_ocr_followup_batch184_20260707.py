# -*- coding: utf-8 -*-
"""Follow-up for tag-split fixed OCR residues after batch183."""

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
REPORT_JSON = ROOT / "output" / "reports" / "reader_fixed_ocr_followup_batch184_20260707.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_fixed_ocr_followup_batch184_20260707.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260707_固定错字跨标签补修第一百八十四批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"
TERMS = ["烈土", "加强劳动力管理同题"]

REPLACEMENTS = [
    (r"白乡建成烈(?P<gap>(?:<[^>]+>)+)土公墓", r"白乡建成烈\g<gap>士公墓", "烈士公墓"),
    (r"加强劳动力管理(?P<gap>(?:<[^>]+>)+)同题", r"加强劳动力管理\g<gap>问题", "加强劳动力管理问题"),
]

LEFT_UNTOUCHED = [
    "`郡守王同题字其上` 保留。",
    "`准北盐税` 留待表格回源批次处理。",
    "未打开、展示或嵌入图片。",
]


def plain_text(html: str) -> str:
    return re.sub(r"<[^>]+>", "", html)


def contexts(plain: str, term: str) -> list[str]:
    return [plain[max(0, m.start() - 65):m.start() + 95].replace("\n", " ") for m in re.finditer(re.escape(term), plain)]


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
        "scope": "current reader tag-split fixed OCR follow-up",
        "changed": total,
        "pattern_counts": {k: v for k, v in pattern_counts.items() if v},
        "targets": results,
        "left_untouched": LEFT_UNTOUCHED,
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 固定错字跨标签补修第一百八十四批",
        "",
        f"> 生成时间：{now}",
        "",
        "## 范围",
        "",
        "- 当前全书、中册、下册阅读稿。",
        "- 修复 batch183 后纯文本扫描发现的跨标签残留 `烈士公墓`、`加强劳动力管理问题`。",
        "- 未做单字泛化替换；未打开、展示或嵌入图片。",
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

    marker = "## 2026-07-07 高置信 OCR 错字补修第一百八十四批：固定错字跨标签补遗"
    upsert_memory(marker, f"""
{marker}

- 复扫 batch183 后发现跨标签残留，定点修复 `白乡建成烈士公墓`、`加强劳动力管理问题`。
- 本批修复 {total} 处；报告：`output/reports/reader_fixed_ocr_followup_batch184_20260707.md`。
- 保留 `郡守王同题字其上` 和 `准北盐税`；未打开、展示或嵌入图片。
""")
    print(json.dumps({"changed": total, "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
