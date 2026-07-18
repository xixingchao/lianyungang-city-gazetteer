# -*- coding: utf-8 -*-
"""Repair source-backed `人党/入党` residuals in full body summary."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "output" / "reports" / "full_summary_rudang_batch349_20260708.md"
REPORT_JSON = ROOT / "output" / "reports" / "full_summary_rudang_batch349_20260708.json"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260708_全书汇总入党残留补修第三百四十九批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"
MARKER = "## 2026-07-08 全书汇总入党残留补修第三百四十九批"
TARGET = ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md"

REPLACEMENTS = [
    ("人党宣誓在陇海公寓举行", "入党宣誓在陇海公寓举行", "页级 PaddleOCR `workbench/ocr/paddle_ocr/上/part01/page_0116.txt` 明确为“入党宣誓在陇海公寓举行”。"),
    ("女青年人党", "女青年入党", "页级 PaddleOCR `workbench/ocr/paddle_ocr/中/part02/page_0407.txt` 明确为“女青年入党”。"),
    ("培养人党对象", "培养入党对象", "页级 PaddleOCR `workbench/ocr/paddle_ocr/中/part02/page_0407.txt` 明确为“培养入党对象”。"),
    ("开始后，人党的9000多名党员", "开始后，入党的9000多名党员", "页级 PaddleOCR `workbench/ocr/paddle_ocr/中/part02/page_0444.txt` 明确为“开始后，入党的9000多名党员”。"),
    ("集体人党的办法", "集体入党的办法", "页级 PaddleOCR `workbench/ocr/paddle_ocr/中/part02/page_0463.txt` 明确为“集体入党的办法”。"),
    ("重新填人党申 请书", "重新填入党申 请书", "页级 PaddleOCR `workbench/ocr/paddle_ocr/中/part02/page_0465.txt` 明确为“重新填入党申请书”。"),
    ("填写人党申请书", "填写入党申请书", "页级 PaddleOCR `workbench/ocr/paddle_ocr/中/part02/page_0465.txt` 明确为“填写入党申请书”。"),
]
CHECK_TERMS = ["人党宣誓", "女青年人党", "培养人党对象", "人党的9000多名党员", "集体人党的办法", "填人党申", "填写人党申请书", "人党", "入党"]


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
        "# 全书汇总入党残留补修 batch349",
        "",
        f"- 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"- 修复总数：{total}",
        "- 范围：全书正文汇总。",
        "- 依据：上册 part01 page_0116 与中册 part02 page_0407、0444、0463、0465 页级 PaddleOCR 成句证据。",
        "- 原则：只替换正文完整入党语境；不处理烈士表格 `人党团` 等表格残段，不作 `人 -> 入` 全局替换。",
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
    lines.extend(["", "## 保留边界", "", "- 剩余 `人党` 主要在烈士名录表格列名/行内 OCR 残段与方言/人名上下文中，未在本批处理。"])
    return "\n".join(lines) + "\n"


def upsert_memory(total: int, residuals: dict[str, int]) -> None:
    block = f"""{MARKER}

- 依据上册 part01 page_0116 与中册 part02 page_0407、0444、0463、0465 页级 PaddleOCR 成句证据，补修全书正文汇总中 `人党 -> 入党` 正文语境，共 {total} 处。
- 代表修复：`人党宣誓 -> 入党宣誓`、`女青年人党 -> 女青年入党`、`培养人党对象 -> 培养入党对象`、`集体人党的办法 -> 集体入党的办法`、`填写人党申请书 -> 填写入党申请书`。
- 本批后检查范围：`人党宣誓` {residuals['人党宣誓']}，`女青年人党` {residuals['女青年人党']}，`培养人党对象` {residuals['培养人党对象']}，`集体人党的办法` {residuals['集体人党的办法']}；剩余 `人党` {residuals['人党']} 主要为表格残段，未处理。
- 未作 `人 -> 入` 全局替换；未处理 OCR 源文件、backup、obsolete、历史交付包；未打开、展示或嵌入图片。
- 报告：`output/reports/full_summary_rudang_batch349_20260708.md`；进度：`output/reports/progress/20260708_全书汇总入党残留补修第三百四十九批.md`。
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
