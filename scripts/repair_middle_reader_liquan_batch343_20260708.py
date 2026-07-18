# -*- coding: utf-8 -*-
"""Repair source-backed `季全/李全` residual in the sea trade paragraph."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "output" / "reports" / "middle_reader_liquan_batch343_20260708.md"
REPORT_JSON = ROOT / "output" / "reports" / "middle_reader_liquan_batch343_20260708.json"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260708_中册海运李全残留补修第三百四十三批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"
MARKER = "## 2026-07-08 中册海运李全残留补修第三百四十三批"

TARGETS = [
    ROOT / "output" / "final_reader" / "连云港市志_全书.html",
    ROOT / "output" / "final_reader" / "连云港市志_中册.html",
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
    ROOT / "workbench" / "body_chapters" / "第十七卷至第二十九卷（中part01）.md",
]
OLD = "起义领袖季全以武"
NEW = "起义领袖李全以武"
EVIDENCE = "页级 PaddleOCR `workbench/ocr/paddle_ocr/中/part01/page_0456.txt` 明确为“起义领袖李全以武力发展起来的海上贸易活动”。"
CHECK_TERMS = [OLD, NEW, "季全以武", "李全以武"]


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
        count = text.count(OLD)
        if not count:
            continue
        path.write_text(text.replace(OLD, NEW), encoding="utf-8")
        changes.append({"path": rel(path), "old": OLD, "new": NEW, "count": count, "evidence": EVIDENCE})
    residuals = {term: sum(read(path).count(term) for path in TARGETS if path.exists()) for term in CHECK_TERMS}
    return changes, residuals


def render(changes: list[dict], residuals: dict[str, int]) -> str:
    total = sum(item["count"] for item in changes)
    lines = [
        "# 中册海运李全残留补修 batch343",
        "",
        f"- 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"- 修复总数：{total}",
        "- 范围：正式全书、正式中册、全书正文汇总、中册 part01 当前源稿。",
        f"- 依据：{EVIDENCE}",
        "- 原则：只替换完整人物语境短语；不作姓名宽泛替换。",
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

- 依据页级 PaddleOCR `workbench/ocr/paddle_ocr/中/part01/page_0456.txt`，补修海运段 `起义领袖季全以武 -> 起义领袖李全以武`，同步正式阅读稿与中册源稿，共 {total} 处。
- 本批后检查范围：`起义领袖季全以武` {residuals[OLD]}，`季全以武` {residuals['季全以武']}，`李全以武` {residuals['李全以武']}。
- 未作姓名宽泛替换；未处理 OCR 源文件、backup、obsolete、历史交付包；未打开、展示或嵌入图片。
- 报告：`output/reports/middle_reader_liquan_batch343_20260708.md`；进度：`output/reports/progress/20260708_中册海运李全残留补修第三百四十三批.md`。
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
