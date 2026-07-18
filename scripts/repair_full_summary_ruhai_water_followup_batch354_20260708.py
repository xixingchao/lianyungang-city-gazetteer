# -*- coding: utf-8 -*-
"""Repair one follow-up waterway residual after batch353."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "output" / "reports" / "full_summary_ruhai_water_followup_batch354_20260708.md"
REPORT_JSON = ROOT / "output" / "reports" / "full_summary_ruhai_water_followup_batch354_20260708.json"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260708_全书汇总入海水利残留补修第三百五十四批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"
MARKER = "## 2026-07-08 全书汇总入海水利残留补修第三百五十四批"
TARGET = ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md"

REPLACEMENTS = [
    {
        "old": "由于新述河太平庄闸以下河床淤积严重，芦苇丛生，人海口段\n对虾塘阻水，减少行洪800立方米每秒，致上游水位雍高0.5米，确定新述河安全行洪流",
        "new": "由于新沭河太平庄闸以下河床淤积严重，芦苇丛生，入海口段\n对虾塘阻水，减少行洪800立方米每秒，致上游水位壅高0.5米，确定新沭河安全行洪流",
        "evidence": "页级 PaddleOCR `workbench/ocr/paddle_ocr/上/part03/page_0067.txt` 明确为“新沭河太平庄闸以下...入海口段...壅高0.5米...新沭河安全行洪流”。",
    }
]
CHECK_TERMS = [
    "人海口",
    "获水村人海口",
    "芦苇丛生，人海口段",
    "新述河太平庄闸以下",
    "确定新述河安全行洪流",
    "水位雍高0.5米",
    "新沭河太平庄闸以下",
    "芦苇丛生，入海口段",
    "水位壅高0.5米",
]


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def apply_fix() -> tuple[list[dict], dict[str, int]]:
    text = read(TARGET)
    updated = text
    changes: list[dict] = []
    for item in REPLACEMENTS:
        count = updated.count(item["old"])
        if not count:
            continue
        updated = updated.replace(item["old"], item["new"])
        changes.append({"path": rel(TARGET), "old": item["old"], "new": item["new"], "count": count, "evidence": item["evidence"]})
    if updated != text:
        TARGET.write_text(updated, encoding="utf-8")
    after = read(TARGET)
    residuals = {term: after.count(term) for term in CHECK_TERMS}
    return changes, residuals


def render(changes: list[dict], residuals: dict[str, int]) -> str:
    total = sum(item["count"] for item in changes)
    lines = [
        "# 全书汇总入海水利残留补修 follow-up batch354",
        "",
        f"- 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"- 修复总数：{total}",
        "- 范围：全书正文汇总。",
        "- 依据：上册 part03 page_0067 页级 PaddleOCR 成句证据。",
        "- 原则：只替换防汛调度段一个完整句内片段；不作 `人 -> 入`、`述 -> 沭`、`雍 -> 壅` 全局替换。",
        "- 图片处理：未打开、展示或嵌入图片。",
        "",
        "## 替换明细",
    ]
    if changes:
        for item in changes:
            old = item["old"].replace("\n", "\\n")
            new = item["new"].replace("\n", "\\n")
            lines.append(f"- `{item['path']}`：`{old}` -> `{new}`；次数 {item['count']}；依据：{item['evidence']}")
    else:
        lines.append("- 本次未产生新增替换。")
    lines.extend(["", "## 检查结果", ""])
    for term, count in residuals.items():
        lines.append(f"- `{term}`：{count}")
    lines.extend([
        "",
        "## 保留边界",
        "",
        "- `获水村人海口` 仍保留未改：所在为表格行，页级 OCR `workbench/ocr/paddle_ocr/上/part02/page_0297.txt` 仍识别为 `人海口`；不凭推断改表格残段。",
    ])
    return "\n".join(lines) + "\n"


def upsert_memory(total: int, residuals: dict[str, int]) -> None:
    block = f"""{MARKER}

- 依据页级 PaddleOCR `workbench/ocr/paddle_ocr/上/part03/page_0067.txt`，补修 batch353 后漏网的防汛调度段 `新述河...人海口段...雍高...新述河安全行洪流 -> 新沭河...入海口段...壅高...新沭河安全行洪流`，共 {total} 处。
- 本批后检查范围：`人海口` {residuals['人海口']}，其中 `获水村人海口` {residuals['获水村人海口']} 处作为表格残段保留；`芦苇丛生，人海口段` {residuals['芦苇丛生，人海口段']}，`新述河太平庄闸以下` {residuals['新述河太平庄闸以下']}，`水位雍高0.5米` {residuals['水位雍高0.5米']}。
- 未作 `人 -> 入`、`述 -> 沭`、`雍 -> 壅` 全局替换；未处理 OCR 源文件、backup、obsolete、历史交付包；未打开、展示或嵌入图片。
- 报告：`output/reports/full_summary_ruhai_water_followup_batch354_20260708.md`；进度：`output/reports/progress/20260708_全书汇总入海水利残留补修第三百五十四批.md`。
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
