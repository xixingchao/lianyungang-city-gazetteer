# -*- coding: utf-8 -*-
"""Repair an eleventh small source-backed reader residue batch."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = [
    ROOT / "output" / "final_reader" / "连云港市志_全书.html",
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
]
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_source_backed_batch10_20260704.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_source_backed_batch10_20260704.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260704_第十一批正文残留回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    (
        "新浦手工业逐步向机器生产",
        "新浦的手工业生产遂步向机器生产发展",
        "新浦的手工业生产逐步向机器生产发展",
        "workbench/ocr/paddle_ocr/上/part02/page_0131.txt:18",
    ),
    (
        "棉供应逐步转由供销社",
        "棉供应计划、市场安排和批发业务遂步转由供销合作社负责",
        "棉供应计划、市场安排和批发业务逐步转由供销合作社负责",
        "workbench/ocr/paddle_ocr/中/part02/page_0170.txt:9",
    ),
    (
        "物资企业自主权逐步扩大",
        "工厂和企业的自主权遂步扩大",
        "工厂和企业的自主权逐步扩大",
        "workbench/ocr/paddle_ocr/中/part02/page_0264.txt:35",
    ),
    (
        "物资计划外允许自销",
        "计划外超产物资充许自销",
        "计划外超产物资允许自销",
        "workbench/ocr/paddle_ocr/中/part02/page_0264.txt:35",
    ),
    (
        "五保户供给逐步改村乡统筹",
        "民政部门督促检查，遂步改“五保户”供给为村统筹、乡统筹",
        "民政部门督促检查，逐步改“五保户”供给为村统筹、乡统筹",
        "workbench/ocr/paddle_ocr/下/part01/page_0031.txt:35",
    ),
    (
        "地名标牌逐步实现",
        "遂步实现街有街牌、路有路牌、巷有巷牌、门有门牌、村有村牌",
        "逐步实现街有街牌、路有路牌、巷有巷牌、门有门牌、村有村牌",
        "workbench/ocr/paddle_ocr/下/part01/page_0056.txt:31",
    ),
    (
        "医院逐步添置器械",
        "各医院遂步添置",
        "各医院逐步添置",
        "workbench/ocr/paddle_ocr/下/part02/page_0190.txt:6",
    ),
]

SKIPPED = [
    "`逐遂步问东延伸` 暂未取得清晰 PaddleOCR 纠正文本，本批暂缓。",
    "继续避免 `遂步` 全局替换，只处理页级证据明确项。",
]


def upsert_memory(path: Path, marker: str, content: str) -> None:
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker not in old:
        path.write_text(old.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")
        return
    start = old.index(marker)
    next_start = old.find("\n## ", start + 1)
    if next_start == -1:
        new = old[:start].rstrip() + "\n\n" + content.strip() + "\n"
    else:
        new = old[:start].rstrip() + "\n\n" + content.strip() + "\n\n" + old[next_start:].lstrip()
    path.write_text(new, encoding="utf-8")


def main() -> None:
    targets = []
    for path in TARGETS:
        text = path.read_text(encoding="utf-8")
        items = []
        for label, old, new, source in REPLACEMENTS:
            count = text.count(old)
            if count:
                text = text.replace(old, new)
            items.append({"label": label, "old": old, "new": new, "source": source, "count": count})
        path.write_text(text, encoding="utf-8")
        verify = path.read_text(encoding="utf-8")
        residuals = [old for _label, old, _new, _source in REPLACEMENTS if old in verify]
        if residuals:
            raise RuntimeError(f"replacement verification failed for {path}: {residuals}")
        targets.append({"target": str(path), "changed": sum(item["count"] for item in items), "items": items})

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    total = sum(item["changed"] for item in targets)
    payload = {
        "time": now,
        "scope": "第十一批正文可读性残留回源修复",
        "targets": targets,
        "total_replacements": total,
        "verified_items": len(REPLACEMENTS),
        "skipped": SKIPPED,
        "principle": "只修复页级 PaddleOCR 明确支撑的长上下文问题。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 第十一批正文残留回源修复",
        "",
        f"- 时间：{now}",
        "- 原则：只修页级 PaddleOCR 明确支撑的长上下文问题。",
        f"- 核验项：{len(REPLACEMENTS)} 项。",
        f"- 本次替换：{total} 处。",
        "",
        "## 文件",
    ]
    for target in targets:
        lines.append(f"- `{target['target']}`：{target['changed']} 处")
    lines.extend(["", "## 修复项"])
    for label, old, new, source in REPLACEMENTS:
        lines.append(f"- {label}: `{old}` -> `{new}`；源：`{source}`")
    lines.extend(["", "## 暂缓"])
    for item in SKIPPED:
        lines.append(f"- {item}")
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    PROGRESS.write_text(REPORT_MD.read_text(encoding="utf-8"), encoding="utf-8")

    memory = f"""
## 2026-07-04 第十一批正文残留回源修复

- 对最终阅读版和正文汇总补做 {len(REPLACEMENTS)} 项页级 PaddleOCR 支撑修复，共替换 {total} 处。
- 修复范围包括新浦手工业、棉供应、物资自主权、五保户供给、地名标牌、医院器械中的 `遂步` 残留，并同页修复 `充许自销` 为 `允许自销`。
- 依据：`output/reports/reader_readability_source_backed_batch10_20260704.md`。
- 暂缓：`逐遂步问东延伸` 等未取得强证据项。
"""
    upsert_memory(MEMORY, "## 2026-07-04 第十一批正文残留回源修复", memory)
    print(json.dumps({"total_replacements": total, "verified_items": len(REPLACEMENTS), "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
