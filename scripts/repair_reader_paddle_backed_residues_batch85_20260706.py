# -*- coding: utf-8 -*-
"""Repair small PaddleOCR-backed warehouse and inscription residues."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = [
    ROOT / "output" / "final_reader" / "连云港市志_全书.html",
    ROOT / "workbench" / "body_chapters" / "第三十卷至第四十二卷（中part02）.md",
    ROOT / "workbench" / "body_chapters" / "第五十二卷至第六十卷及附录（下part02）.md",
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
]
REPORT_JSON = ROOT / "output" / "reports" / "reader_paddle_backed_residues_batch85_20260706.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_paddle_backed_residues_batch85_20260706.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260706_高置信OCR错字补修第八十五批_仓廒文曰款曰.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    {
        "label": "通济仓廒房",
        "old": "通济仓明洪武三年（1370年）在海州治西创建，廠房37间。正德十一年（1516年）",
        "new": "通济仓明洪武三年（1370年）在海州治西创建，廒房37间。正德十一年（1516年）",
        "source": "workbench/ocr/paddle_ocr/中/part02/page_0236.txt",
    },
    {
        "label": "通济仓廒房断行源稿",
        "old": "通济仓\n明洪武三年（1370年）在海州治西创建，廠房37间。正德十一年（1516年）",
        "new": "通济仓\n明洪武三年（1370年）在海州治西创建，廒房37间。正德十一年（1516年）",
        "source": "workbench/ocr/paddle_ocr/中/part02/page_0236.txt",
    },
    {
        "label": "上列仓廒",
        "old": "上列仓廠已成颓垣，荡然无存。",
        "new": "上列仓廒已成颓垣，荡然无存。",
        "source": "workbench/ocr/paddle_ocr/中/part02/page_0236.txt",
    },
    {
        "label": "建筑卷款曰",
        "old": "款日：“大宋绍圣戊寅年夏四月上旬”。",
        "new": "款曰：“大宋绍圣戊寅年夏四月上旬”。",
        "source": "workbench/ocr/paddle_ocr/下/part02/page_0095.txt",
    },
    {
        "label": "旅游白虎山文曰",
        "old": "文17行，每行7字，文日·“徽猷阁待制知海州事张叔夜…宣和庚子重阳日同登”。",
        "new": "文17行，每行7字，文曰：“徽猷阁待制知海州事张叔夜…宣和庚子重阳日同登”。",
        "source": "workbench/ocr/paddle_ocr/下/part02/page_0104.txt",
    },
]


def upsert_memory(path: Path, marker: str, content: str) -> None:
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker not in old:
        path.write_text(old.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")
        return
    start = old.index(marker)
    next_start = old.find("\n## ", start + 1)
    new = old[:start].rstrip() + "\n\n" + content.strip() + "\n"
    if next_start != -1:
        new += "\n" + old[next_start:].lstrip()
    path.write_text(new, encoding="utf-8")


def main() -> None:
    applied = []
    for target in TARGETS:
        text = target.read_text(encoding="utf-8")
        items = []
        for item in REPLACEMENTS:
            count = text.count(item["old"])
            if count:
                text = text.replace(item["old"], item["new"])
            items.append({**item, "count": count})
        target.write_text(text, encoding="utf-8")
        verify = target.read_text(encoding="utf-8")
        residuals = [item["old"] for item in REPLACEMENTS if item["old"] in verify]
        if residuals:
            raise RuntimeError(f"replacement verification failed for {target}: {residuals[:3]}")
        applied.append({"target": str(target), "changed": sum(item["count"] for item in items), "items": items})

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "PaddleOCR-backed warehouse and inscription residue repair",
        "replacement_patterns": len(REPLACEMENTS),
        "changed_total": sum(target["changed"] for target in applied),
        "targets": applied,
        "principle": "Only exact context phrases backed by cited PaddleOCR pages are changed.",
        "skipped": "Other 文日/诗日/款日 instances in ancient-text or unsourced contexts are left for page-level verification.",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 高置信 OCR 错字补修第八十五批：仓廒、文曰、款曰",
        "",
        f"> 生成时间：{now}",
        "",
        "## 修复范围",
        "",
        "- 主阅读版、中册 part02 源稿、下册 part02 源稿、全书正文汇总中的少量残留。",
        "- 仅处理 PaddleOCR 同页明确支撑的 `廒房/仓廒/文曰/款曰`。",
        "- 古籍诗文中的 `诗日`、旧志序文中的 `编繁` 等仍按硬点保留，不做全局替换。",
        "",
        "## 统计",
        "",
        f"- 证据短语：{len(REPLACEMENTS)} 项",
        f"- 本次实际替换：{payload['changed_total']} 处",
        "",
        "## 文件",
        "",
    ]
    for target in applied:
        lines.append(f"- `{target['target']}`：{target['changed']} 处")
    lines.extend(["", "## 修复项", ""])
    for item in REPLACEMENTS:
        lines.append(f"- {item['label']}: `{item['old']}` -> `{item['new']}`；源：`{item['source']}`")
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    PROGRESS.write_text(REPORT_MD.read_text(encoding="utf-8"), encoding="utf-8")

    memory = f"""
## 2026-07-06 高置信 OCR 错字补修第八十五批：仓廒、文曰、款曰

- 依据 PaddleOCR 页 `中/part02/page_0236`、`下/part02/page_0095`、`下/part02/page_0104`，修复主阅读版及对应源稿/汇总中的 5 个精确短片段。
- 典型修复：`廠房37间` -> `廒房37间`，`上列仓廠` -> `上列仓廒`，`款日：“大宋绍圣...` -> `款曰：“大宋绍圣...`，张叔夜题名说明 `文日·` -> `文曰：`。
- 本批证据短语 {len(REPLACEMENTS)} 项，实际替换 {payload['changed_total']} 处；报告：`output/reports/reader_paddle_backed_residues_batch85_20260706.md`。
- 边界：古籍诗文中的 `诗日`、旧志序文中的 `编繁` 等仍需逐页证据，未做全局替换；未展示、未嵌入图片。
"""
    upsert_memory(MEMORY, "## 2026-07-06 高置信 OCR 错字补修第八十五批：仓廒、文曰、款曰", memory)
    print(json.dumps({"patterns": len(REPLACEMENTS), "changed_total": payload["changed_total"], "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
