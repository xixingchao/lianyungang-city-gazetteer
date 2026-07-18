# -*- coding: utf-8 -*-
"""Repair source-backed package-material wording residue, batch 232."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = [
    ROOT / "output" / "final_reader" / "连云港市志_全书.html",
    ROOT / "output" / "final_reader" / "连云港市志_中册.html",
    ROOT / "workbench" / "body_chapters" / "第三十卷至第四十二卷（中part02）.md",
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
]
REPORT_JSON = ROOT / "output" / "reports" / "reader_package_change_batch232_20260707.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_package_change_batch232_20260707.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260707_出口包装改变残留补修第二百三十二批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"
EVIDENCE = ROOT / "workbench" / "ocr" / "paddle_ocr" / "中" / "part02" / "page_0206.txt"
EVIDENCE_SNIPPET = "装材料的供应有了改变"
ITEMS = [
    ("出口商品包装材料的供应有了故变", "出口商品包装材料的供应有了改变"),
    ("装材料的供应有了故变", "装材料的供应有了改变"),
]


def ensure_evidence() -> None:
    text = EVIDENCE.read_text(encoding="utf-8", errors="ignore")
    if EVIDENCE_SNIPPET not in text:
        raise SystemExit(f"missing evidence: {EVIDENCE.relative_to(ROOT)}: {EVIDENCE_SNIPPET}")


def main() -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    ensure_evidence()
    changes = []
    for path in TARGETS:
        text = path.read_text(encoding="utf-8", errors="ignore")
        file_items = []
        for old, new in ITEMS:
            count = text.count(old)
            if count:
                text = text.replace(old, new)
                file_items.append({"old": old, "new": new, "count": count})
        if file_items:
            path.write_text(text, encoding="utf-8")
        changes.append({"file": str(path.relative_to(ROOT)), "items": file_items})

    residuals = {
        old: {
            str(path.relative_to(ROOT)): path.read_text(encoding="utf-8", errors="ignore").count(old)
            for path in TARGETS
        }
        for old, _ in ITEMS
    }
    payload = {"time": now, "changes": changes, "residuals": residuals, "evidence": str(EVIDENCE.relative_to(ROOT))}
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 出口包装改变残留补修第二百三十二批",
        "",
        f"> 生成时间：{now}",
        "",
        "## 范围",
        "",
        "- 修复对外经济贸易卷出口包装段 `故变 -> 改变` 残留。",
        "- 证据来自页级 PaddleOCR；未做全局替换。",
        "- 未打开、展示或嵌入图片。",
        "",
        "## 修改统计",
        "",
        "| 文件 | 原文 | 新文 | 次数 | 证据 |",
        "|---|---|---|---:|---|",
    ]
    for item in changes:
        for change in item["items"]:
            lines.append(f"| `{item['file']}` | `{change['old']}` | `{change['new']}` | {change['count']} | `{EVIDENCE.relative_to(ROOT)}` |")
    lines.extend(["", "## 残留计数", ""])
    for old, files in residuals.items():
        lines.append(f"- `{old}`：{sum(files.values())}")
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    PROGRESS.write_text(REPORT_MD.read_text(encoding="utf-8"), encoding="utf-8")

    memory = MEMORY.read_text(encoding="utf-8", errors="ignore").rstrip()
    memory += "\n\n## 2026-07-07 出口包装改变残留补修第二百三十二批\n\n"
    memory += "- 依据 `workbench/ocr/paddle_ocr/中/part02/page_0206.txt`，修复对外经济贸易卷出口包装段 `供应有了故变 -> 供应有了改变`。\n"
    memory += "- 同步范围：当前中册/全书阅读稿及相关正文源稿；报告：`output/reports/reader_package_change_batch232_20260707.md`。\n"
    memory += "- 未做全局替换，未打开、展示或嵌入图片。\n"
    MEMORY.write_text(memory + "\n", encoding="utf-8")

    print(json.dumps({
        "changed_files": sum(1 for item in changes if item["items"]),
        "changed_items": sum(change["count"] for item in changes for change in item["items"]),
        "residual_total": sum(sum(files.values()) for files in residuals.values()),
        "report": str(REPORT_MD),
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
