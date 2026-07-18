# -*- coding: utf-8 -*-
"""Thirty-first source-backed reader readability repair batch."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = [
    ROOT / "output" / "final_reader" / "连云港市志_全书.html",
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
]
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_source_backed_batch31_20260704.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_source_backed_batch31_20260704.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260704_第三十一批正文残留回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    {
        "label": "民国三十六年水灾灾民人数",
        "old": "仅东海县有灾民50方人，断炊者20方人",
        "new": "仅东海县有灾民50万人，断炊者20万人",
        "source": "workbench/ocr/paddle_ocr/下/part01/page_0028.txt:22",
    },
]


def append_memory(path: Path, marker: str, content: str) -> None:
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker not in old:
        path.write_text(old.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")


def main() -> None:
    targets = []
    for path in TARGETS:
        text = path.read_text(encoding="utf-8")
        items = []
        for item in REPLACEMENTS:
            count = text.count(item["old"])
            if count:
                text = text.replace(item["old"], item["new"])
            items.append({**item, "count": count})
        path.write_text(text, encoding="utf-8")
        verify = path.read_text(encoding="utf-8")
        residuals = [item["old"] for item in REPLACEMENTS if item["old"] in verify]
        if residuals:
            raise RuntimeError(f"replacement verification failed for {path}: {residuals}")
        targets.append({"target": str(path), "changed": sum(item["count"] for item in items), "items": items})

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    total = sum(target["changed"] for target in targets)
    payload = {
        "time": now,
        "scope": "第三十一批正文残留回源修复",
        "targets": targets,
        "total_replacements": total,
        "verified_items": len(REPLACEMENTS),
        "principle": "只修复页级 OCR 可直接证明且 final reader/body summary 不一致的救灾人数残留。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 第三十一批正文残留回源修复",
        "",
        f"- 时间：{now}",
        "- 原则：只修页级 OCR 可直接证明且 final reader/body summary 不一致的救灾人数残留。",
        f"- 核验项：{len(REPLACEMENTS)} 项。",
        f"- 本次替换：{total} 处。",
        "- 说明：final reader 已为正确值，本批主要补齐正文汇总残留。",
        "",
        "## 文件",
    ]
    for target in targets:
        lines.append(f"- `{target['target']}`：{target['changed']} 处")
    lines += ["", "## 明细"]
    for target in targets:
        for item in target["items"]:
            if item["count"]:
                lines.append(
                    f"- {item['label']}：依据 `{item['source']}`；`{target['target']}` 命中 {item['count']} 处。"
                )
    lines.append("")
    content = "\n".join(lines)
    REPORT_MD.write_text(content, encoding="utf-8")
    PROGRESS.write_text(content, encoding="utf-8")

    marker = "## 2026-07-04 第三十一批正文残留回源修复"
    memory = f"""
{marker}
- 修复页级 OCR 直接证明且 final reader/body summary 不一致的救灾人数残留，共 {total} 处。
- 依据页：`workbench/ocr/paddle_ocr/下/part01/page_0028.txt:22`。
- 同步目标：`output/final_reader/连云港市志_全书.html` 与 `workbench/body_chapters/连云港市志_全书_正文汇总.md`；实际命中正文汇总 1 处。
- 报告：`output/reports/reader_readability_source_backed_batch31_20260704.md`。
"""
    append_memory(MEMORY, marker, memory)


if __name__ == "__main__":
    main()
