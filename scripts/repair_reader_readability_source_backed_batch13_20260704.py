# -*- coding: utf-8 -*-
"""Repair a fourteenth small source-backed reader residue batch."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = [
    ROOT / "output" / "final_reader" / "连云港市志_全书.html",
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
]
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_source_backed_batch13_20260704.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_source_backed_batch13_20260704.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260704_第十四批正文残留回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    (
        "干部四化",
        "总路线和千部“四化”",
        "总路线和干部“四化”",
        "workbench/ocr/paddle_ocr/中/part02/page_0438.txt:27",
    ),
    (
        "选拔一批干部任领导职务",
        "选拔一批于部任领导职务",
        "选拔一批干部任领导职务",
        "workbench/ocr/paddle_ocr/中/part02/page_0438.txt:28",
    ),
    (
        "提拔科以上干部",
        "提拨科以上干部1386名",
        "提拔科以上干部1386名",
        "workbench/ocr/paddle_ocr/中/part02/page_0438.txt:28",
    ),
    (
        "提拔干部中文化程度",
        "提拔于部中大中专以上文化程度的547人",
        "提拔干部中大中专以上文化程度的547人",
        "workbench/ocr/paddle_ocr/中/part02/page_0439.txt:5",
    ),
    (
        "科技干部61人",
        "科技于部61人",
        "科技干部61人",
        "workbench/ocr/paddle_ocr/merged/连云港市志_上_part01_PaddleOCR汇总.md:16089",
    ),
]

SKIPPED = [
    "下册治安司法、人事、社团等 `于部/千部` 残留暂未一次性定位到页级强证据，继续逐页核证。",
    "人物传记中大量 `加人中国共产党` 不做全局替换，需另按页段成批证明。",
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
        "scope": "第十四批正文可读性残留回源修复",
        "targets": targets,
        "total_replacements": total,
        "verified_items": len(REPLACEMENTS),
        "skipped": SKIPPED,
        "principle": "只修复页级 PaddleOCR 明确支撑的长上下文问题。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 第十四批正文残留回源修复",
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
## 2026-07-04 第十四批正文残留回源修复

- 对最终阅读版和正文汇总补做 {len(REPLACEMENTS)} 项页级 PaddleOCR 支撑修复，共替换 {total} 处。
- 修复范围包括政党干部调配段 `千部/于部/提拨` 残留，以及东海科技人员段 `科技于部61人`。
- 依据：`output/reports/reader_readability_source_backed_batch13_20260704.md`。
- 暂缓：下册人事、治安司法、社团等未定位强证据项，以及人物传记 `加人中国共产党` 批量残留。
"""
    upsert_memory(MEMORY, "## 2026-07-04 第十四批正文残留回源修复", memory)
    print(json.dumps({"total_replacements": total, "verified_items": len(REPLACEMENTS), "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
