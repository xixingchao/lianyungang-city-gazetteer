# -*- coding: utf-8 -*-
"""Repair one Paddle-backed middle-volume residue for the artificial crystal project."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "output" / "final_reader" / "连云港市志_中册.html"
REPORT_JSON = ROOT / "output" / "reports" / "middle_reader_crystal_project_batch117_20260706.json"
REPORT_MD = ROOT / "output" / "reports" / "middle_reader_crystal_project_batch117_20260706.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260706_中册人造水晶技改项目残留回源补修第一百一十七批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    {
        "label": "东海县水晶厂技改项目",
        "old": "1986年初，该厂投资200方元，新增年产5吨的人造水晶技改项自。",
        "new": "1986年初，该厂投资200万元，新增年产5吨的人造水晶技改项目。",
        "source": "workbench/ocr/paddle_ocr/中/part01/page_0259.txt:25；raw 同页误作 `投资200方元`、`技改项自`",
    },
]

LEFT_UNTOUCHED = [
    "本批只同步当前中册分册读者；全书版和正文源稿已是正确文本，未重复改动。",
    "乱码副本 HTML 不属于当前中文主交付，本批不处理。",
    "未展示、未嵌入图片。",
]


def upsert_memory(path: Path, marker: str, content: str) -> None:
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker not in old:
        path.write_text(old.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")
        return
    start = old.index(marker)
    next_start = old.find("\n## ", start + 1)
    new = old[:start].rstrip() + "\n\n" + content.strip() + "\n"
    if next_start != -1:
        new += "\n" + old[next_start:].lstrip()
    path.write_text(new, encoding="utf-8")


def main() -> None:
    text = TARGET.read_text(encoding="utf-8")
    items = []
    for item in REPLACEMENTS:
        count = text.count(item["old"])
        if count:
            text = text.replace(item["old"], item["new"])
        items.append({**item, "count": count})
    TARGET.write_text(text, encoding="utf-8")

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    changed = sum(i["count"] for i in items)
    payload = {
        "time": now,
        "scope": "Paddle-backed middle reader residue: artificial crystal project",
        "changed_this_run": changed,
        "target": str(TARGET),
        "items": items,
        "left_untouched": LEFT_UNTOUCHED,
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 中册人造水晶技改项目残留补修第一百一十七批：Paddle 回源核对",
        "",
        f"> 生成时间：{now}",
        "",
        "## 修复范围",
        "",
        "- 当前中册阅读版 `output/final_reader/连云港市志_中册.html`。",
        "- 仅处理 Paddle 页级 OCR 明确反证的 `方元/项自` 残留。",
        "",
        "## 统计",
        "",
        f"- 本次替换：{changed} 处",
        "",
        "## 修复项",
        "",
    ]
    for item in REPLACEMENTS:
        lines.append(f"- {item['label']}: `{item['old']}` -> `{item['new']}`；源/定位：`{item['source']}`")
    lines.extend(["", "## 未处理边界", ""])
    for item in LEFT_UNTOUCHED:
        lines.append(f"- {item}")
    report = "\n".join(lines) + "\n"
    REPORT_MD.write_text(report, encoding="utf-8")
    PROGRESS.write_text(report, encoding="utf-8")

    marker = "## 2026-07-06 高置信 OCR 错字补修第一百一十七批：中册人造水晶技改项目残留"
    upsert_memory(MEMORY, marker, f"""
{marker}

- 按 `workbench/ocr/paddle_ocr/中/part01/page_0259.txt:25` 回源，修复当前中册分册读者中东海县水晶厂段 `投资200方元，新增年产5吨的人造水晶技改项自` 为 `投资200万元，新增年产5吨的人造水晶技改项目`。
- 全书版和正文源稿在本轮复查时已是正确文本，仅中册分册命中 1 处；报告：`output/reports/middle_reader_crystal_project_batch117_20260706.md`。
- 边界：乱码副本 HTML 不作为当前中文主交付目标；未展示、未嵌入图片。
""")
    print(json.dumps({"changed_this_run": changed, "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
