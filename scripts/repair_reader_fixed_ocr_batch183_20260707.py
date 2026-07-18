# -*- coding: utf-8 -*-
"""Repair a small batch of high-confidence fixed OCR residues."""

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
REPORT_JSON = ROOT / "output" / "reports" / "reader_fixed_ocr_batch183_20260707.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_fixed_ocr_batch183_20260707.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260707_固定错字补修第一百八十三批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    ("烈土", "烈士", "烈士"),
    ("内阁学土", "内阁学士", "内阁学士"),
    ("理学学土学位", "理学学士学位", "理学学士学位"),
    ("博（硕）土", "博（硕）士", "博（硕）士"),
    ("出上于西郭宝墓", "出土于西郭宝墓", "出土于西郭宝墓"),
    ("凳下腺、舌下腺", "颌下腺、舌下腺", "颌下腺"),
    ("橙骨切除并安装人工骨", "镫骨切除并安装人工镫骨", "镫骨切除并安装人工镫骨"),
    ("加强劳动力管理同题", "加强劳动力管理问题", "加强劳动力管理问题"),
    ("于部违法乱纪", "干部违法乱纪", "干部违法乱纪"),
    ("脱产于部", "脱产干部", "脱产干部"),
    ("党政领导于部", "党政领导干部", "党政领导干部"),
    ("1方多件", "1万多件", "1万多件"),
]

RESIDUAL_TERMS = [
    "烈土",
    "内阁学土",
    "理学学土学位",
    "博（硕）土",
    "出上于西郭宝墓",
    "凳下腺",
    "橙骨切除并安装人工骨",
    "加强劳动力管理同题",
    "于部违法乱纪",
    "脱产于部",
    "党政领导于部",
    "1方多件",
]

LEFT_UNTOUCHED = [
    "`郡守王同题字其上` 保留，未按 `同题 -> 问题` 泛化。",
    "`准北盐税` 属表题/表格问题，留待表格回源批次处理。",
    "未处理用户新贴长段正文中的混排问题；该类问题需要另按源页定位。",
    "未打开、展示或嵌入图片。",
]


def plain_text(html: str) -> str:
    return re.sub(r"<[^>]+>", "", html)


def contexts(plain: str, term: str) -> list[str]:
    return [
        plain[max(0, m.start() - 65):m.start() + 95].replace("\n", " ")
        for m in re.finditer(re.escape(term), plain)
    ]


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
        for needle, replacement, label in REPLACEMENTS:
            count = after.count(needle)
            if count:
                after = after.replace(needle, replacement)
                pattern_counts[label] += count
                file_patterns.append({"needle": needle, "replacement": replacement, "label": label, "count": count})
        target.write_text(after, encoding="utf-8")
        after_plain = plain_text(after)
        results.append({
            "target": str(target),
            "changed": sum(item["count"] for item in file_patterns),
            "before_terms": {term: before_plain.count(term) for term in RESIDUAL_TERMS},
            "after_terms": {term: after_plain.count(term) for term in RESIDUAL_TERMS},
            "patterns": file_patterns,
            "remaining_contexts": {term: contexts(after_plain, term) for term in RESIDUAL_TERMS if after_plain.count(term)},
        })

    total = sum(item["changed"] for item in results)
    payload = {
        "time": now,
        "scope": "current reader high-confidence fixed OCR repair",
        "changed": total,
        "pattern_counts": {k: v for k, v in pattern_counts.items() if v},
        "targets": results,
        "left_untouched": LEFT_UNTOUCHED,
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 固定错字补修第一百八十三批",
        "",
        f"> 生成时间：{now}",
        "",
        "## 范围",
        "",
        "- 当前全书、中册、下册阅读稿。",
        "- 只修复上下文明确的固定 OCR 错字：烈士、学士、干部、问题、出土、颌下腺、镫骨、万多件等。",
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

    marker = "## 2026-07-07 高置信 OCR 错字补修第一百八十三批：固定错字候选"
    upsert_memory(marker, f"""
{marker}

- 核对当前阅读稿固定 OCR 错字候选，定点修复烈士、学士、干部、问题、出土、颌下腺、镫骨、万多件等高置信项。
- 本批修复 {total} 处；报告：`output/reports/reader_fixed_ocr_batch183_20260707.md`。
- 保留 `郡守王同题字其上` 和 `准北盐税` 等待源/表格边界；未处理用户新贴长段正文混排问题；未打开、展示或嵌入图片。
""")
    print(json.dumps({"changed": total, "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
