# -*- coding: utf-8 -*-
"""Repair remaining source-backed `器血/器皿` contexts."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "output" / "reports" / "glassware_remaining_verified_contexts_batch340_20260708.md"
REPORT_JSON = ROOT / "output" / "reports" / "glassware_remaining_verified_contexts_batch340_20260708.json"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260708_器皿残留语境补修第三百四十批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"
MARKER = "## 2026-07-08 器皿残留语境补修第三百四十批"

TARGETS = [
    ROOT / "output" / "final_reader" / "连云港市志_全书.html",
    ROOT / "output" / "final_reader" / "连云港市志_中册.html",
    ROOT / "output" / "final_reader" / "连云港市志_下册.html",
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
    ROOT / "workbench" / "body_chapters" / "第十七卷至第二十九卷（中part01）.md",
    ROOT / "workbench" / "body_chapters" / "第四十三卷至第五十一卷（下part01）.md",
]

REPLACEMENTS = [
    {
        "old": "铜窑器血的输出口岸",
        "new": "铜窑器皿的输出口岸",
        "evidence": "页级 PaddleOCR `workbench/ocr/paddle_ocr/中/part01/page_0456.txt` 明确为“铜窑器皿的输出口岸”。",
    },
    {
        "old": "供奉器血等都被大火吞噬",
        "new": "供奉器皿等都被大火吞噬",
        "evidence": "页级 PaddleOCR `workbench/ocr/paddle_ocr/下/part01/page_0176.txt` 明确为“供奉器皿等都被大火吞噬”。",
    },
]

CHECK_TERMS = [
    "铜窑器血的输出口岸",
    "铜窑器皿的输出口岸",
    "供奉器血等都被大火吞噬",
    "供奉器皿等都被大火吞噬",
    "器血",
    "器皿",
]


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def apply_fix() -> tuple[list[dict], dict[str, int]]:
    changes: list[dict] = []
    for path in TARGETS:
        if not path.exists():
            continue
        text = read(path)
        updated = text
        for item in REPLACEMENTS:
            count = updated.count(item["old"])
            if not count:
                continue
            updated = updated.replace(item["old"], item["new"])
            changes.append({
                "path": rel(path),
                "old": item["old"],
                "new": item["new"],
                "count": count,
                "evidence": item["evidence"],
            })
        if updated != text:
            path.write_text(updated, encoding="utf-8")

    residuals = {
        term: sum(read(path).count(term) for path in TARGETS if path.exists())
        for term in CHECK_TERMS
    }
    return changes, residuals


def render(changes: list[dict], residuals: dict[str, int]) -> str:
    total = sum(item["count"] for item in changes)
    lines = [
        "# 器皿残留语境补修 batch340",
        "",
        f"- 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"- 修复总数：{total}",
        "- 范围：正式全书、中册、下册，以及对应当前正文汇总/分册源稿。",
        "- 依据：中册 page_0456 与下册 page_0176 页级 PaddleOCR 成句证据。",
        "- 原则：只替换两个完整语境短语；不作 `器血 -> 器皿` 全局替换。",
        "- 图片处理：未打开、展示或嵌入图片。",
        "",
        "## 替换明细",
    ]
    if changes:
        for item in changes:
            lines.append(f"- `{item['path']}`：`{item['old']}` -> `{item['new']}`；次数 {item['count']}；依据：{item['evidence']}")
    else:
        lines.append("- 本次未产生新增替换。")
    lines.extend(["", "## 检查结果", ""])
    for term, count in residuals.items():
        lines.append(f"- `{term}`：{count}")
    lines.extend([
        "",
        "## 保留边界",
        "",
        "- 方言残段中的 `器血` 未在本批处理，留待逐页核对，不凭词义猜改。",
    ])
    return "\n".join(lines) + "\n"


def upsert_memory(total: int, residuals: dict[str, int]) -> None:
    block = f"""{MARKER}

- 依据页级 PaddleOCR `workbench/ocr/paddle_ocr/中/part01/page_0456.txt` 与 `workbench/ocr/paddle_ocr/下/part01/page_0176.txt`，补修 `铜窑器血的输出口岸 -> 铜窑器皿的输出口岸`、`供奉器血等都被大火吞噬 -> 供奉器皿等都被大火吞噬`，同步正式阅读稿与对应源稿，共 {total} 处。
- 本批后检查范围：`铜窑器血的输出口岸` {residuals['铜窑器血的输出口岸']}，`供奉器血等都被大火吞噬` {residuals['供奉器血等都被大火吞噬']}，`器血` {residuals['器血']}，`器皿` {residuals['器皿']}。
- 剩余 `器血` 为方言残段，未在本批处理；未作 `器血 -> 器皿` 全局替换；未处理 OCR 源文件、backup、obsolete、历史交付包；未打开、展示或嵌入图片。
- 报告：`output/reports/glassware_remaining_verified_contexts_batch340_20260708.md`；进度：`output/reports/progress/20260708_器皿残留语境补修第三百四十批.md`。
"""
    old = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    start = old.find(MARKER)
    if start < 0:
        MEMORY.write_text(old.rstrip() + "\n\n" + block.strip() + "\n", encoding="utf-8")
        return
    next_start = old.find("\n## ", start + 1)
    if next_start < 0:
        new = old[:start].rstrip() + "\n\n" + block.strip() + "\n"
    else:
        new = old[:start].rstrip() + "\n\n" + block.strip() + old[next_start:]
    MEMORY.write_text(new, encoding="utf-8")


def main() -> None:
    changes, residuals = apply_fix()
    total = sum(item["count"] for item in changes)
    data = {
        "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "total": total,
        "changes": changes,
        "residuals": residuals,
        "replacements": REPLACEMENTS,
    }
    REPORT_JSON.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    report = render(changes, residuals)
    REPORT.write_text(report, encoding="utf-8")
    PROGRESS.write_text(report, encoding="utf-8")
    upsert_memory(total, residuals)
    print(f"total={total}")
    print(f"residuals={residuals}")
    print(f"report={REPORT}")


if __name__ == "__main__":
    main()
