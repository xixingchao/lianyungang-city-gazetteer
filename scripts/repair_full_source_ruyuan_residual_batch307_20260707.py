# -*- coding: utf-8 -*-
"""Full source 入园 residual sync backed by PaddleOCR."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "output" / "reports" / "full_source_ruyuan_residual_batch307_20260707.md"
REPORT_JSON = ROOT / "output" / "reports" / "full_source_ruyuan_residual_batch307_20260707.json"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260707_全书正文入园残留补修第三百零七批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"
TARGET = ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md"

REPLACEMENTS = [
    ("人园儿童5125人", "入园儿童5125人", "PaddleOCR 上/part01/page_0247 为“入园儿童5125人”。"),
    ("人园幼儿3877人", "入园幼儿3877人", "PaddleOCR 上/part01/page_0253 为“入园幼儿3877人”。"),
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
        "# 全书正文入园残留补修 batch307",
        "",
        f"- 生成时间：{data['time']}",
        f"- 修复总数：{total}",
        "- 范围：全书正文汇总源稿。",
        "- 依据：`workbench/ocr/paddle_ocr/上/part01/page_0247.txt`、`page_0253.txt`。",
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
    marker = "## 2026-07-07 全书正文入园残留补修第三百零七批"
    old_memory = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker not in old_memory:
        block = f"""
{marker}

- 依据 `workbench/ocr/paddle_ocr/上/part01/page_0247.txt` 与 `page_0253.txt`，同步补修全书正文汇总残留：`人园儿童5125人 -> 入园儿童5125人`、`人园幼儿3877人 -> 入园幼儿3877人`，共 {total} 处。
- 报告：`output/reports/full_source_ruyuan_residual_batch307_20260707.md`；进度：`output/reports/progress/20260707_全书正文入园残留补修第三百零七批.md`。
- 未处理 OCR 源文件、backup、obsolete、历史交付包；未打开、展示或嵌入图片。
"""
        MEMORY.write_text(old_memory.rstrip() + "\n\n" + block.strip() + "\n", encoding="utf-8")
    print(f"total={total}")
    print(f"residuals_nonzero={bad}")
    print(f"report={REPORT}")


if __name__ == "__main__":
    main()
