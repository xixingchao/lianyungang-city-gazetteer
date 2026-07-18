# -*- coding: utf-8 -*-
"""Repair source-backed `引人/引入` residuals."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "output" / "reports" / "middle_yinru_batch348_20260708.md"
REPORT_JSON = ROOT / "output" / "reports" / "middle_yinru_batch348_20260708.json"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260708_中册引入残留补修第三百四十八批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"
MARKER = "## 2026-07-08 中册引入残留补修第三百四十八批"

TARGETS = [
    ROOT / "output" / "final_reader" / "连云港市志_中册.html",
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
    ROOT / "workbench" / "body_chapters" / "第十七卷至第二十九卷（中part01）.md",
    ROOT / "workbench" / "body_chapters" / "第三十卷至第四十二卷（中part02）.md",
]
CHECK_FILES = TARGETS + [ROOT / "output" / "final_reader" / "连云港市志_全书.html"]

REPLACEMENTS = [
    {
        "old": "引人电网电源",
        "new": "引入电网电源",
        "evidence": "页级 PaddleOCR `workbench/ocr/paddle_ocr/中/part01/page_0341.txt` 明确为“引入电网电源”。",
    },
    {
        "old": "投入产出原则引人了税收减免",
        "new": "投入产出”原则引入了税收减免",
        "evidence": "页级 PaddleOCR `workbench/ocr/paddle_ocr/中/part02/page_0337.txt` 明确为“将‘投入产出’原则引入了税收减免的审核”。",
    },
    {
        "old": "“投入产出原则引人了税收减免",
        "new": "“投入产出”原则引入了税收减免",
        "evidence": "页级 PaddleOCR `workbench/ocr/paddle_ocr/中/part02/page_0337.txt` 明确为“将‘投入产出’原则引入了税收减免的审核”。",
    },
]
CHECK_TERMS = ["引人电网电源", "引入电网电源", "原则引人了税收", "原则引入了税收", "投入产出原则引人", "投入产出”原则引入"]


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
            changes.append({"path": rel(path), "old": item["old"], "new": item["new"], "count": count, "evidence": item["evidence"]})
        if updated != text:
            path.write_text(updated, encoding="utf-8")
    residuals = {term: sum(read(path).count(term) for path in CHECK_FILES if path.exists()) for term in CHECK_TERMS}
    return changes, residuals


def render(changes: list[dict], residuals: dict[str, int]) -> str:
    total = sum(item["count"] for item in changes)
    lines = [
        "# 中册引入残留补修 batch348",
        "",
        f"- 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"- 修复总数：{total}",
        "- 范围：正式中册、全书正文汇总、中册 part01 与 part02 当前源稿。",
        "- 依据：中册 part01 page_0341、part02 page_0337 页级 PaddleOCR 成句证据。",
        "- 原则：只替换完整引入语境；不作 `人 -> 入` 全局替换。",
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

- 依据页级 PaddleOCR `workbench/ocr/paddle_ocr/中/part01/page_0341.txt` 与 `workbench/ocr/paddle_ocr/中/part02/page_0337.txt`，补修 `引人电网电源 -> 引入电网电源`、`投入产出原则引人了税收减免 -> 投入产出”原则引入了税收减免`，同步正式中册与当前源稿，共 {total} 处。
- 本批后检查范围：`引人电网电源` {residuals['引人电网电源']}，`原则引人了税收` {residuals['原则引人了税收']}，`投入产出原则引人` {residuals['投入产出原则引人']}。
- 未作 `人 -> 入` 全局替换；未处理 OCR 源文件、backup、obsolete、历史交付包；未打开、展示或嵌入图片。
- 报告：`output/reports/middle_yinru_batch348_20260708.md`；进度：`output/reports/progress/20260708_中册引入残留补修第三百四十八批.md`。
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
