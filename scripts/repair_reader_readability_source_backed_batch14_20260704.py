# -*- coding: utf-8 -*-
"""Repair a fifteenth small source-backed reader residue batch."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = [
    ROOT / "output" / "final_reader" / "连云港市志_全书.html",
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
]
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_source_backed_batch14_20260704.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_source_backed_batch14_20260704.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260704_第十五批正文残留回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    (
        "双拥部队干部",
        "76名灌云籍部队于部和战士",
        "76名灌云籍部队干部和战士",
        "workbench/ocr/paddle_ocr/下/part01/page_0022.txt:15",
    ),
    (
        "双拥小孩入学",
        "小孩人学等实际困难",
        "小孩入学等实际困难",
        "workbench/ocr/paddle_ocr/下/part01/page_0022.txt:20",
    ),
    (
        "社团管理干部",
        "社团管理于部和市属有关部委",
        "社团管理干部和市属有关部委",
        "workbench/ocr/paddle_ocr/下/part01/page_0058.txt:3",
    ),
    (
        "检察县处级干部",
        "县处级于部犯罪要案6件、6人",
        "县处级干部犯罪要案6件、6人",
        "workbench/ocr/paddle_ocr/下/part01/page_0108.txt:13",
    ),
    (
        "人事一般干部",
        "一般于部的思想教育、调配、提拔、监察、工资待遇",
        "一般干部的思想教育、调配、提拔、监察、工资待遇",
        "workbench/ocr/paddle_ocr/下/part01/page_0194.txt:6",
    ),
    (
        "干部文化补习学校",
        "于部文化补习学校",
        "干部文化补习学校",
        "workbench/ocr/paddle_ocr/下/part01/page_0194.txt:17",
    ),
    (
        "县处级干部教育",
        "600多名县处级于部参加",
        "600多名县处级干部参加",
        "workbench/ocr/paddle_ocr/下/part01/page_0204.txt:17",
    ),
    (
        "人民调解主管干部",
        "主管于部担任",
        "主管干部担任",
        "workbench/ocr/paddle_ocr/下/part01/page_0148.txt:6",
    ),
    (
        "调解干部会议",
        "先进调解于部会议",
        "先进调解干部会议",
        "workbench/ocr/paddle_ocr/下/part01/page_0148.txt:14",
    ),
]

SKIPPED = [
    "`page_0204.txt` 自身仍有 `受训于部10000多人次`，源 OCR 未能独立证明，暂缓。",
    "司法宣传、普法、科技进修学院、附录对外开放等残留待继续定位页级证据。",
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
        "scope": "第十五批正文可读性残留回源修复",
        "targets": targets,
        "total_replacements": total,
        "verified_items": len(REPLACEMENTS),
        "skipped": SKIPPED,
        "principle": "只修复页级 PaddleOCR 明确支撑的长上下文问题。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 第十五批正文残留回源修复",
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
## 2026-07-04 第十五批正文残留回源修复

- 对最终阅读版和正文汇总补做 {len(REPLACEMENTS)} 项下册页级 PaddleOCR 支撑修复，共替换 {total} 处。
- 修复范围包括优抚安置、社团登记管理、检察经济犯罪、人事干部管理/教育、司法调解中的 `于部/人学` 残留。
- 依据：`output/reports/reader_readability_source_backed_batch14_20260704.md`。
- 暂缓：源 OCR 自身未能证明的 `受训于部10000多人次`，以及司法宣传、普法、科技、附录对外开放等仍需继续定位页级证据的残留。
"""
    upsert_memory(MEMORY, "## 2026-07-04 第十五批正文残留回源修复", memory)
    print(json.dumps({"total_replacements": total, "verified_items": len(REPLACEMENTS), "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
