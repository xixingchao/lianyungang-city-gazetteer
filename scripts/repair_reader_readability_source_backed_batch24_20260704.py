# -*- coding: utf-8 -*-
"""Twenty-fourth source-backed reader readability repair batch."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = [
    ROOT / "output" / "final_reader" / "连云港市志_全书.html",
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
]
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_source_backed_batch24_20260704.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_source_backed_batch24_20260704.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260704_第二十四批正文残留回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    (
        "知识分子入党段正文汇总残留",
        "有624名知识分子加人中国共产党",
        "有624名知识分子加入中国共产党",
        "workbench/ocr/paddle_ocr/merged/连云港市志_上_part01_PaddleOCR汇总.md:5289-5290",
    ),
    (
        "万毅入党段正文汇总残留",
        "发展第一一师六六七团团长万毅加人中国共产党",
        "发展第一一师六六七团团长万毅加入中国共产党",
        "workbench/ocr/paddle_ocr/merged/连云港市志_上_part01_PaddleOCR汇总.md:5731-5733",
    ),
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
        "scope": "第二十四批正文残留回源修复",
        "targets": targets,
        "total_replacements": total,
        "verified_items": len(REPLACEMENTS),
        "principle": "只修复最终阅读版已正确、正文汇总仍残留且有上册 OCR 汇总证明的两处入党段。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 第二十四批正文残留回源修复",
        "",
        f"- 时间：{now}",
        "- 原则：只修最终阅读版已正确、正文汇总仍残留且有上册 OCR 汇总证明的两处入党段。",
        f"- 核验项：{len(REPLACEMENTS)} 项。",
        f"- 本次替换：{total} 处。",
        "",
        "## 文件",
    ]
    for target in targets:
        lines.append(f"- `{target['target']}`：{target['changed']} 处")
    lines += ["", "## 明细"]
    for target in targets:
        for item in target["items"]:
            if item["count"]:
                lines.append(f"- {item['label']}：依据 `{item['source']}`；`{target['target']}` 命中 {item['count']} 处。")
    lines.append("")
    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")
    PROGRESS.write_text("\n".join(lines), encoding="utf-8")

    marker = "## 2026-07-04 第二十四批正文残留回源修复"
    memory = f"""
{marker}
- 修复正文汇总中两处已由上册 OCR 汇总证明的 `加人中国共产党` 残留：知识分子政策段、万毅入党段。
- 最终阅读版对应段此前已为 `加入`，本批用于同步正文汇总。
- 报告：`output/reports/reader_readability_source_backed_batch24_20260704.md`。
"""
    append_memory(MEMORY, marker, memory)


if __name__ == "__main__":
    main()
