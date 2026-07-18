# -*- coding: utf-8 -*-
"""Tiny childcare 入托 residual repair backed by PaddleOCR."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "output" / "reports" / "childcare_residual_batch315_20260707.md"
REPORT_JSON = ROOT / "output" / "reports" / "childcare_residual_batch315_20260707.json"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260707_托幼入托残留补修第三百一十五批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

TARGETS = [
    ROOT / "output" / "final_reader" / "连云港市志_下册.html",
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
    ROOT / "workbench" / "body_chapters" / "第五十二卷至第六十卷及附录（下part02）.md",
]

REPLACEMENTS = [
    ("儿童人托", "儿童入托", "PaddleOCR 下/part02/page_0204 为“儿童入托”。"),
    ("人托率", "入托率", "PaddleOCR 下/part02/page_0204 为“入托率”。"),
]


def main() -> None:
    changes = []
    for path in TARGETS:
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        original = text
        for old, new, reason in REPLACEMENTS:
            count = text.count(old)
            if count:
                text = text.replace(old, new)
                changes.append({"path": str(path.relative_to(ROOT)).replace("\\", "/"), "old": old, "new": new, "count": count, "reason": reason})
        if text != original:
            path.write_text(text, encoding="utf-8")

    residuals = {}
    for old, _new, _reason in REPLACEMENTS:
        residuals[old] = sum(path.read_text(encoding="utf-8", errors="ignore").count(old) for path in TARGETS if path.exists())
    total = sum(item["count"] for item in changes)
    data = {"time": datetime.now().strftime("%Y-%m-%d %H:%M"), "total": total, "changes": changes, "residuals": residuals}
    REPORT_JSON.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# 托幼入托残留补修 batch315",
        "",
        f"- 生成时间：{data['time']}",
        f"- 修复总数：{total}",
        "- 范围：当前正式下册 HTML、正式正文汇总及下册 part02 正文源稿。",
        "- 依据：`workbench/ocr/paddle_ocr/下/part02/page_0204.txt`。",
        "- 原则：只处理 batch314 后托幼统计段漏网短语；未处理 OCR 源文件、backup、obsolete、历史交付包。",
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

    marker = "## 2026-07-07 托幼入托残留补修第三百一十五批"
    old_memory = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker not in old_memory:
        block = f"""
{marker}

- 依据 `workbench/ocr/paddle_ocr/下/part02/page_0204.txt`，补修 batch314 后托幼统计段漏网残留：`儿童人托 -> 儿童入托`、`人托率 -> 入托率`，共 {total} 处。
- 报告：`output/reports/childcare_residual_batch315_20260707.md`；进度：`output/reports/progress/20260707_托幼入托残留补修第三百一十五批.md`。
- 未处理 OCR 源文件、backup、obsolete、历史交付包；未打开、展示或嵌入图片。
"""
        MEMORY.write_text(old_memory.rstrip() + "\n\n" + block.strip() + "\n", encoding="utf-8")
    print(f"total={total}")
    print(f"residuals_nonzero={bad}")
    print(f"report={REPORT}")


if __name__ == "__main__":
    main()
