# -*- coding: utf-8 -*-
"""Forty-third source-backed reader readability repair batch."""

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
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_source_backed_batch43_20260704.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_source_backed_batch43_20260704.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260704_第四十三批正文残留回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    {
        "label": "1985年基本建设全年支出",
        "old": "1985年，全年支出1506方元，其中交通邮",
        "new": "1985年，全年支出1506万元，其中交通邮",
        "source": "workbench/ocr/merged/连云港市志_中_part02_OCR汇总.md:23135",
    },
    {
        "label": "企业挖潜改造资金化工支出",
        "old": "工业部门中，化工1056方元，轻工646万元",
        "new": "工业部门中，化工1056万元，轻工646万元",
        "source": "workbench/ocr/merged/连云港市志_中_part02_OCR汇总.md:27098",
    },
    {
        "label": "1984年现金投放量",
        "old": "现金投放量9523方元",
        "new": "现金投放量9523万元",
        "source": "workbench/ocr/merged/连云港市志_中_part02_OCR汇总.md:25638",
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
        "scope": "第四十三批正文残留回源修复",
        "targets": targets,
        "total_replacements": total,
        "verified_items": len(REPLACEMENTS),
        "principle": "仅修复中册 OCR 汇总明确写作万元、正文同段残作方元的金额单位。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 第四十三批正文残留回源修复",
        "",
        f"- 时间：{now}",
        "- 原则：仅修复中册 OCR 汇总明确写作万元、正文同段残作方元的金额单位。",
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

    marker = "## 2026-07-04 第四十三批正文残留回源修复"
    memory = f"""
{marker}
- 修复中册财政、金融段 `方元` 金额单位残留，共 {total} 处。
- 本批只纳入 OCR 汇总明确给出 `万元` 的 3 个同段金额：`1506万元`、`1056万元`、`9523万元`。
- 暂不处理 OCR 自身仍为 `方元` 的商业、财政总览和其它金额项，避免无证据扩修。
- 报告：`output/reports/reader_readability_source_backed_batch43_20260704.md`。
"""
    append_once(MEMORY, marker, memory)


if __name__ == "__main__":
    main()
