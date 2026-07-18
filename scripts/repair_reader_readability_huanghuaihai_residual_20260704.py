# -*- coding: utf-8 -*-
"""Repair source-backed Huanghuaihai OCR residuals."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = [
    ROOT / "output" / "final_reader" / "连云港市志_全书.html",
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
    ROOT / "workbench" / "body_chapters" / "第三十卷至第四十二卷（中part02）.md",
]
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_huanghuaihai_residual_20260704.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_huanghuaihai_residual_20260704.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260704_黄淮海错识残留回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    {
        "label": "三麦种植区名",
        "old": "境内是黄准海旱作麦区",
        "new": "境内是黄淮海旱作麦区",
        "source": "workbench/body_chapters/paddle_上/第四卷至第十卷（part02）.md:13933; workbench/ocr/paddle_ocr/上/part02/page_0228.txt:22",
    },
    {
        "label": "粮食专项资金开发区名",
        "old": "开始黄准海平原农业开",
        "new": "开始黄淮海平原农业开",
        "source": "workbench/body_chapters/paddle_上/第十卷至第十六卷（part03）.md:3376; workbench/ocr/paddle_ocr/上/part03/page_0040.txt:10",
    },
    {
        "label": "一期黄淮海开发总投资",
        "old": "市一期黄准海开发完成总投资",
        "new": "市一期黄淮海开发完成总投资",
        "source": "workbench/ocr/paddle_ocr/中/part02/page_0306.txt:10",
    },
    {
        "label": "一期黄淮海开发项目",
        "old": "一期黄准海开发项目",
        "new": "一期黄淮海开发项目",
        "source": "workbench/ocr/paddle_ocr/中/part02/page_0306.txt:12",
    },
    {
        "label": "黄淮海农业综合发展项目",
        "old": "黄准海农业综合发展项目",
        "new": "黄淮海农业综合发展项目",
        "source": "workbench/ocr/paddle_ocr/中/part02/page_0306.txt:17",
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
        "scope": "黄淮海 OCR 错识残留回源修复",
        "targets": targets,
        "total_replacements": total,
        "verified_items": len(REPLACEMENTS),
        "principle": "仅修复页级 PaddleOCR 或同锚 PaddleOCR 正文明确证明的 `黄准海` 错识，不扩展到其它 `准/淮` 候选。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 黄淮海错识残留回源修复",
        "",
        f"- 时间：{now}",
        "- 原则：仅修复页级 PaddleOCR 或同锚 PaddleOCR 正文明确证明的 `黄准海` 错识。",
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
    content = "\n".join(lines)
    REPORT_MD.write_text(content, encoding="utf-8")
    PROGRESS.write_text(content, encoding="utf-8")

    marker = "## 2026-07-04 黄淮海错识残留回源修复"
    memory = f"""
{marker}
- 依据上册 PaddleOCR 正文/分页和中册 part02 `page_0306.txt`，修复 `黄准海` 为 `黄淮海`，共 {total} 处。
- 同步目标：`output/final_reader/连云港市志_全书.html`、`workbench/body_chapters/连云港市志_全书_正文汇总.md`、`workbench/body_chapters/第三十卷至第四十二卷（中part02）.md`。
- 本批只处理 `黄准海`，不扩展到其它 `准/淮` 或海岸线候选。
- 报告：`output/reports/reader_readability_huanghuaihai_residual_20260704.md`。
"""
    append_once(MEMORY, marker, memory)
    print(json.dumps({"total_replacements": total, "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
