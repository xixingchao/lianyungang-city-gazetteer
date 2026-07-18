# -*- coding: utf-8 -*-
"""Follow-up repair for remaining full-summary `人党/入党` prose contexts."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "output" / "reports" / "full_summary_rudang_followup_batch350_20260708.md"
REPORT_JSON = ROOT / "output" / "reports" / "full_summary_rudang_followup_batch350_20260708.json"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260708_全书汇总入党残留补修第三百五十批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"
MARKER = "## 2026-07-08 全书汇总入党残留补修第三百五十批"
TARGET = ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md"

REPLACEMENTS = [
    ("重新填人党申 请书", "重新填入党申 请书", "页级 PaddleOCR `workbench/ocr/paddle_ocr/中/part02/page_0465.txt` 明确为“重新填入党申请书”。"),
    ("民国31年重新人党", "民国31年重新入党", "页级 PaddleOCR `workbench/ocr/paddle_ocr/下/part02/page_0385.txt` 明确为“民国31年重新入党”。"),
    ("1939年）12月人党", "1939年）12月入党", "页级 PaddleOCR `workbench/ocr/paddle_ocr/下/part02/page_0386.txt` 明确为“1939年)12月入党”。"),
]
CHECK_TERMS = ["填人党申", "重新人党", "12月人党", "人党", "入党"]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def apply_fix() -> tuple[list[dict], dict[str, int]]:
    text = read(TARGET)
    updated = text
    changes: list[dict] = []
    for old, new, evidence in REPLACEMENTS:
        count = updated.count(old)
        if not count:
            continue
        updated = updated.replace(old, new)
        changes.append({"path": rel(TARGET), "old": old, "new": new, "count": count, "evidence": evidence})
    if updated != text:
        TARGET.write_text(updated, encoding="utf-8")
    after = read(TARGET)
    residuals = {term: after.count(term) for term in CHECK_TERMS}
    return changes, residuals


def render(changes: list[dict], residuals: dict[str, int]) -> str:
    total = sum(item["count"] for item in changes)
    lines = [
        "# 全书汇总入党残留补修 batch350",
        "",
        f"- 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"- 修复总数：{total}",
        "- 范围：全书正文汇总。",
        "- 依据：中册 part02 page_0465、下册 part02 page_0385、page_0386 页级 PaddleOCR 成句证据。",
        "- 原则：只替换剩余正文完整入党语境；不处理烈士表格 `人党团` 等表格残段，不作 `人 -> 入` 全局替换。",
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
    lines.extend(["", "## 保留边界", "", "- 剩余 `人党` 主要在烈士名录表格列名/行内 OCR 残段与正常 `工人党` 语境中，未在本批处理。"])
    return "\n".join(lines) + "\n"


def upsert_memory(total: int, residuals: dict[str, int]) -> None:
    block = f"""{MARKER}

- 依据中册 part02 page_0465、下册 part02 page_0385、page_0386 页级 PaddleOCR 成句证据，补修全书正文汇总剩余正文 `人党 -> 入党` 语境，共 {total} 处。
- 代表修复：`重新填人党申请书 -> 重新填入党申请书`、`民国31年重新人党 -> 民国31年重新入党`、`1939年）12月人党 -> 1939年）12月入党`。
- 本批后检查范围：`填人党申` {residuals['填人党申']}，`重新人党` {residuals['重新人党']}，`12月人党` {residuals['12月人党']}；剩余 `人党` {residuals['人党']} 主要为表格残段和正常 `工人党` 语境，未处理。
- 未作 `人 -> 入` 全局替换；未处理 OCR 源文件、backup、obsolete、历史交付包；未打开、展示或嵌入图片。
- 报告：`output/reports/full_summary_rudang_followup_batch350_20260708.md`；进度：`output/reports/progress/20260708_全书汇总入党残留补修第三百五十批.md`。
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
    data = {"time": datetime.now().strftime("%Y-%m-%d %H:%M"), "total": total, "changes": changes, "residuals": residuals, "replacements": REPLACEMENTS}
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
