# -*- coding: utf-8 -*-
"""Repair source-backed `输人/输入` residual in import-goods context."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "output" / "reports" / "middle_source_import_goods_batch347_20260708.md"
REPORT_JSON = ROOT / "output" / "reports" / "middle_source_import_goods_batch347_20260708.json"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260708_中册输入货物残留补修第三百四十七批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"
MARKER = "## 2026-07-08 中册输入货物残留补修第三百四十七批"

TARGETS = [ROOT / "workbench" / "body_chapters" / "第十七卷至第二十九卷（中part01）.md"]
CHECK_FILES = TARGETS + [
    ROOT / "output" / "final_reader" / "连云港市志_全书.html",
    ROOT / "output" / "final_reader" / "连云港市志_中册.html",
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
]
OLD = "来自青岛的货物占输人货物"
NEW = "来自青岛的货物占输入货物"
EVIDENCE = "页级 PaddleOCR `workbench/ocr/paddle_ocr/中/part01/page_0503.txt` 明确为“来自青岛的货物占输入货物的22%”。"


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def apply_fix() -> tuple[list[dict], dict[str, int]]:
    changes: list[dict] = []
    for path in TARGETS:
        text = read(path)
        count = text.count(OLD)
        if not count:
            continue
        path.write_text(text.replace(OLD, NEW), encoding="utf-8")
        changes.append({"path": rel(path), "old": OLD, "new": NEW, "count": count, "evidence": EVIDENCE})
    residuals = {
        OLD: sum(read(path).count(OLD) for path in CHECK_FILES if path.exists()),
        NEW: sum(read(path).count(NEW) for path in CHECK_FILES if path.exists()),
        "输人货物": sum(read(path).count("输人货物") for path in CHECK_FILES if path.exists()),
        "输入货物": sum(read(path).count("输入货物") for path in CHECK_FILES if path.exists()),
    }
    return changes, residuals


def render(changes: list[dict], residuals: dict[str, int]) -> str:
    total = sum(item["count"] for item in changes)
    lines = [
        "# 中册输入货物残留补修 batch347",
        "",
        f"- 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"- 修复总数：{total}",
        "- 范围：中册 part01 当前源稿。",
        f"- 依据：{EVIDENCE}",
        "- 原则：只替换完整货物统计语境；不作 `人 -> 入` 全局替换。",
        "- 图片处理：未打开、展示或嵌入图片。",
        "",
        "## 替换明细",
    ]
    if changes:
        for item in changes:
            lines.append(f"- `{item['path']}`：`{item['old']}` -> `{item['new']}`；次数 {item['count']}。")
    else:
        lines.append("- 本次未产生新增替换。")
    lines.extend(["", "## 检查结果", ""])
    for term, count in residuals.items():
        lines.append(f"- `{term}`：{count}")
    return "\n".join(lines) + "\n"


def upsert_memory(total: int, residuals: dict[str, int]) -> None:
    block = f"""{MARKER}

- 依据页级 PaddleOCR `workbench/ocr/paddle_ocr/中/part01/page_0503.txt`，补修中册 part01 源稿 `来自青岛的货物占输人货物 -> 来自青岛的货物占输入货物`，共 {total} 处。
- 本批后检查范围：`来自青岛的货物占输人货物` {residuals[OLD]}，`输人货物` {residuals['输人货物']}。
- 未作 `人 -> 入` 全局替换；未处理 OCR 源文件、backup、obsolete、历史交付包；未打开、展示或嵌入图片。
- 报告：`output/reports/middle_source_import_goods_batch347_20260708.md`；进度：`output/reports/progress/20260708_中册输入货物残留补修第三百四十七批.md`。
"""
    old = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    start = old.find(MARKER)
    if start < 0:
        MEMORY.write_text(old.rstrip() + "\n\n" + block.strip() + "\n", encoding="utf-8")
        return
    next_start = old.find("\n## ", start + 1)
    new = old[:start].rstrip() + "\n\n" + block.strip() + ("\n" if next_start < 0 else old[next_start:])
    MEMORY.write_text(new, encoding="utf-8")


def main() -> None:
    changes, residuals = apply_fix()
    total = sum(item["count"] for item in changes)
    data = {"time": datetime.now().strftime("%Y-%m-%d %H:%M"), "total": total, "changes": changes, "residuals": residuals, "evidence": EVIDENCE}
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
