# -*- coding: utf-8 -*-
"""Tiny upper-source area residual repairs backed by PaddleOCR."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "output" / "reports" / "upper_area_spacing_batch313_20260707.md"
REPORT_JSON = ROOT / "output" / "reports" / "upper_area_spacing_batch313_20260707.json"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260707_上册面积残留补修第三百一十三批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"
TARGET = ROOT / "workbench" / "body_chapters" / "连云港市志_上册_正文汇总.md"

REPLACEMENTS = [
    ("道路清扫面积93方平方米", "道路清扫面积93万平方米", "PaddleOCR 上/part02/page_0075 为“道路清扫面积93万平方米”。"),
    ("苗圃1.6方平方米", "苗圃1.6万平方米", "PaddleOCR 上/part02/page_0085 为“苗圃1.6万平方米”。"),
]


def main() -> None:
    text = TARGET.read_text(encoding="utf-8", errors="ignore")
    changes = []
    for old, new, reason in REPLACEMENTS:
        count = text.count(old)
        if count:
            text = text.replace(old, new)
            changes.append({"path": str(TARGET.relative_to(ROOT)).replace("\\", "/"), "old": old, "new": new, "count": count, "reason": reason})
    TARGET.write_text(text, encoding="utf-8")
    residuals = {old: TARGET.read_text(encoding="utf-8", errors="ignore").count(old) for old, _new, _reason in REPLACEMENTS}
    total = sum(item["count"] for item in changes)
    data = {"time": datetime.now().strftime("%Y-%m-%d %H:%M"), "total": total, "changes": changes, "residuals": residuals}
    REPORT_JSON.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# 上册面积残留补修 batch313",
        "",
        f"- 生成时间：{data['time']}",
        f"- 修复总数：{total}",
        "- 范围：上册正文汇总源稿。",
        "- 依据：`workbench/ocr/paddle_ocr/上/part02/page_0075.txt`、`workbench/ocr/paddle_ocr/上/part02/page_0085.txt`。",
        "- 图片处理：未打开、展示或嵌入图片。",
        "",
        "## 替换明细",
    ]
    for item in changes:
        lines.append(f"- `{item['path']}`：`{item['old']}` -> `{item['new']}`；次数 {item['count']}；依据：{item['reason']}")
    lines += ["", "## 残留计数", ""]
    bad = {k: v for k, v in residuals.items() if v}
    lines.append("- 本批检查短语在当前检查范围中均为 0。" if not bad else str(bad))
    report = "\n".join(lines) + "\n"
    REPORT.write_text(report, encoding="utf-8")
    PROGRESS.write_text(report, encoding="utf-8")
    marker = "## 2026-07-07 上册面积残留补修第三百一十三批"
    old_memory = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker not in old_memory:
        block = f"""
{marker}

- 依据 `workbench/ocr/paddle_ocr/上/part02/page_0075.txt` 与 `page_0085.txt`，补修上册正文汇总面积残留：`道路清扫面积93方平方米 -> 道路清扫面积93万平方米`、`苗圃1.6方平方米 -> 苗圃1.6万平方米`，共 {total} 处。
- 报告：`output/reports/upper_area_spacing_batch313_20260707.md`；进度：`output/reports/progress/20260707_上册面积残留补修第三百一十三批.md`。
- 未处理 OCR 源文件、backup、obsolete、历史交付包；未打开、展示或嵌入图片。
"""
        MEMORY.write_text(old_memory.rstrip() + "\n\n" + block.strip() + "\n", encoding="utf-8")
    print(f"total={total}")
    print(f"residuals_nonzero={bad}")
    print(f"report={REPORT}")


if __name__ == "__main__":
    main()
