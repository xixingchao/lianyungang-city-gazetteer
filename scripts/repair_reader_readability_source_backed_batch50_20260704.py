# -*- coding: utf-8 -*-
"""Fiftieth source-backed reader readability repair batch."""

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
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_source_backed_batch50_20260704.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_source_backed_batch50_20260704.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260704_第五十批正文残留回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    {
        "label": "国营蔬菜公司销售额金额单位",
        "old": "全年蔬菜销售额70多方元",
        "new": "全年蔬菜销售额70多万元",
        "source": "workbench/ocr/paddle_ocr/中/part02/page_0149.txt:19",
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
        "scope": "第五十批正文残留回源修复",
        "targets": targets,
        "total_replacements": total,
        "verified_items": len(REPLACEMENTS),
        "principle": "依据中册 part02 PaddleOCR 分页文本修复最后一处正文源方元金额单位残留。",
        "evidence": ["workbench/ocr/paddle_ocr/中/part02/page_0149.txt:19"],
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 第五十批正文残留回源修复",
        "",
        f"- 时间：{now}",
        "- 原则：依据中册 part02 PaddleOCR 分页文本修复最后一处正文源 `方元` 金额单位残留。",
        f"- 核验项：{len(REPLACEMENTS)} 项。",
        f"- 本次替换：{total} 处。",
        "- 证据：`workbench/ocr/paddle_ocr/中/part02/page_0149.txt:19` 为 `全年蔬莱销售额70多万元...`；正文保留上下文既有 `蔬菜` 字形，仅修正金额单位。",
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

    marker = "## 2026-07-04 第五十批正文残留回源修复"
    memory = f"""
{marker}
- 依据 `workbench/ocr/paddle_ocr/中/part02/page_0149.txt:19`，修复国营蔬菜公司销售额 `全年蔬菜销售额70多方元` 为 `全年蔬菜销售额70多万元`，共 {total} 处。
- 同步目标：`workbench/body_chapters/连云港市志_全书_正文汇总.md`、`workbench/body_chapters/第三十卷至第四十二卷（中part02）.md`；最终阅读版未命中旧串。
- 处理后活动正文源 `方元` 残留清零；后续继续按证据链排查其它 OCR 风险类，不做无证据全局替换。
- 报告：`output/reports/reader_readability_source_backed_batch50_20260704.md`。
"""
    append_once(MEMORY, marker, memory)


if __name__ == "__main__":
    main()
