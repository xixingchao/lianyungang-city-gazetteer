# -*- coding: utf-8 -*-
"""Repair source-backed `人海/入海` geography contexts in full summary."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "output" / "reports" / "full_summary_ruhai_geo_batch352_20260708.md"
REPORT_JSON = ROOT / "output" / "reports" / "full_summary_ruhai_geo_batch352_20260708.json"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260708_全书汇总入海地理残留补修第三百五十二批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"
MARKER = "## 2026-07-08 全书汇总入海地理残留补修第三百五十二批"
TARGET = ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md"

REPLACEMENTS = [
    ("河流由此人海", "河流由此入海", "页级 PaddleOCR `workbench/ocr/paddle_ocr/上/part01/page_0032.txt` 明确为“河流由此入海”。"),
    ("黄河夺淮人海", "黄河夺淮入海", "页级 PaddleOCR `workbench/ocr/paddle_ocr/上/part01/page_0047.txt` 明确为“黄河夺淮入海”。"),
    ("遍布人海口", "遍布入海口", "页级 PaddleOCR `workbench/ocr/paddle_ocr/上/part01/page_0120.txt` 明确为“遍布入海口”。"),
    ("临洪河人海口附近", "临洪河入海口附近", "页级 PaddleOCR `workbench/ocr/paddle_ocr/上/part01/page_0128.txt` 明确为“临洪河入海口附近”。"),
    ("两端人海口地带", "两端入海口地带", "页级 PaddleOCR `workbench/ocr/paddle_ocr/上/part01/page_0128.txt` 明确为“两端入海口地带”。"),
]
CHECK_TERMS = ["河流由此人海", "黄河夺淮人海", "遍布人海口", "临洪河人海口附近", "两端人海口地带", "人海口", "入海口", "由此入海", "黄河夺淮入海"]


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


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
        "# 全书汇总入海地理残留补修 batch352",
        "",
        f"- 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"- 修复总数：{total}",
        "- 范围：全书正文汇总。",
        "- 依据：上册 part01 page_0032、0047、0120、0128 页级 PaddleOCR 成句证据。",
        "- 原则：只替换自然地理/大事记中的完整入海语境；不处理 `进人海州城` 等不同语义，不作 `人 -> 入` 全局替换。",
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
    return "\n".join(lines) + "\n"


def upsert_memory(total: int, residuals: dict[str, int]) -> None:
    block = f"""{MARKER}

- 依据上册 part01 page_0032、0047、0120、0128 页级 PaddleOCR 成句证据，补修全书正文汇总自然地理/大事记 `人海 -> 入海` 残留，共 {total} 处。
- 代表修复：`河流由此人海 -> 河流由此入海`、`黄河夺淮人海 -> 黄河夺淮入海`、`遍布人海口 -> 遍布入海口`、`临洪河人海口附近 -> 临洪河入海口附近`。
- 本批后检查范围：`河流由此人海` {residuals['河流由此人海']}，`黄河夺淮人海` {residuals['黄河夺淮人海']}，`遍布人海口` {residuals['遍布人海口']}，`临洪河人海口附近` {residuals['临洪河人海口附近']}。
- 未作 `人 -> 入` 全局替换；未处理 OCR 源文件、backup、obsolete、历史交付包；未打开、展示或嵌入图片。
- 报告：`output/reports/full_summary_ruhai_geo_batch352_20260708.md`；进度：`output/reports/progress/20260708_全书汇总入海地理残留补修第三百五十二批.md`。
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
