# -*- coding: utf-8 -*-
"""Repair a tiny PaddleOCR-backed readability batch."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = [
    ROOT / "output" / "final_reader" / "连云港市志_全书.html",
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
]
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_paddle_backed_micro_20260704.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_paddle_backed_micro_20260704.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260704_PaddleOCR闭合小批错字修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    {
        "label": "计划生育列入规划并进入计划控制",
        "old": "工作，将人口增长计划列人全市国民经济、社会发展总体规划。自此，人口生育进人计划",
        "new": "工作，将人口增长计划列入全市国民经济、社会发展总体规划。自此，人口生育进入计划",
        "source": "workbench/body_chapters/paddle_上/第四卷_人口（part01_部分）.md:371; workbench/ocr/paddle_ocr/merged/连云港市志_上册_PaddleOCR汇总.md:16827",
    },
    {
        "label": "计划管理进入计划发展轨道",
        "old": "放进行统一管理，国民经济开始进人计划发展的轨道",
        "new": "放进行统一管理，国民经济开始进入计划发展的轨道",
        "source": "workbench/body_chapters/paddle_上/第四卷至第十卷（part02）.md:10085; workbench/ocr/paddle_ocr/merged/连云港市志_上册_PaddleOCR汇总.md:30915",
    },
    {
        "label": "采用国际标准培训人数",
        "old": "参加人数40馀人",
        "new": "参加人数40余人",
        "source": "workbench/ocr/paddle_ocr/merged/连云港市志_上册_PaddleOCR汇总.md:32246",
    },
    {
        "label": "采标列入厂长目标责任制",
        "old": "列人厂长自标责任制",
        "new": "列入厂长目标责任制",
        "source": "workbench/body_chapters/paddle_上/第四卷至第十卷（part02）.md:11289; workbench/ocr/paddle_ocr/merged/连云港市志_上册_PaddleOCR汇总.md:32248",
    },
]


def append_once(path: Path, marker: str, content: str) -> None:
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
        "scope": "PaddleOCR 闭合小批错字修复",
        "targets": targets,
        "total_replacements": total,
        "verified_items": len(REPLACEMENTS),
        "principle": "仅修复同段 PaddleOCR 明确闭合的少量字形，不扩展为 `人/入/自/目/余` 全局规则。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# PaddleOCR 闭合小批错字修复",
        "",
        f"- 时间：{now}",
        "- 原则：仅修复同段 PaddleOCR 明确闭合的少量字形。",
        f"- 核验项：{len(REPLACEMENTS)} 项。",
        f"- 本次替换：{total} 处。",
        "- 暂缓：`自已/并人/进人/深人` 等未取得独立闭合证据的其它命中。",
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
    content = "\n".join(lines)
    REPORT_MD.write_text(content, encoding="utf-8")
    PROGRESS.write_text(content, encoding="utf-8")

    marker = "## 2026-07-04 PaddleOCR 闭合小批错字修复"
    memory = f"""
{marker}
- 依据上册 PaddleOCR 正文/汇总，修复 `列人/进人/自标/馀` 等小批可读性残留，共 {total} 处。
- 同步目标：`output/final_reader/连云港市志_全书.html`、`workbench/body_chapters/连云港市志_全书_正文汇总.md`。
- 本批不扩展为全局 `人/入/自/目/余` 规则，未闭合的 `自已/并人/深人/进人` 继续逐条核。
- 报告：`output/reports/reader_readability_paddle_backed_micro_20260704.md`。
"""
    append_once(MEMORY, marker, memory)
    print(json.dumps({"total_replacements": total, "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
