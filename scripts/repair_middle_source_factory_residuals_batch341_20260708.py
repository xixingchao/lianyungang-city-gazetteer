# -*- coding: utf-8 -*-
"""Repair middle-volume source `该广/该厂` residuals with page OCR evidence."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "output" / "reports" / "middle_source_factory_residuals_batch341_20260708.md"
REPORT_JSON = ROOT / "output" / "reports" / "middle_source_factory_residuals_batch341_20260708.json"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260708_中册源稿厂字残留补修第三百四十一批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"
MARKER = "## 2026-07-08 中册源稿厂字残留补修第三百四十一批"

TARGETS = [
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
    ROOT / "workbench" / "body_chapters" / "第十七卷至第二十九卷（中part01）.md",
]

REPLACEMENTS = [
    {
        "old": "该广位于新浦海连中路26号",
        "new": "该厂位于新浦海连中路26号",
        "evidence": "页级 PaddleOCR `workbench/ocr/paddle_ocr/中/part01/page_0102.txt` 明确为“该厂位于新浦海连中路26号”。",
    },
    {
        "old": "该广占地9.6万平方米",
        "new": "该厂占地9.6万平方米",
        "evidence": "页级 PaddleOCR `workbench/ocr/paddle_ocr/中/part01/page_0213.txt` 明确为“该厂占地9.6万平方米”。",
    },
]

CHECK_FILES = TARGETS + [
    ROOT / "output" / "final_reader" / "连云港市志_全书.html",
    ROOT / "output" / "final_reader" / "连云港市志_中册.html",
]
CHECK_TERMS = [item["old"] for item in REPLACEMENTS] + [item["new"] for item in REPLACEMENTS]


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
        term: sum(read(path).count(term) for path in CHECK_FILES if path.exists())
        for term in CHECK_TERMS
    }
    return changes, residuals


def render(changes: list[dict], residuals: dict[str, int]) -> str:
    total = sum(item["count"] for item in changes)
    lines = [
        "# 中册源稿厂字残留补修 batch341",
        "",
        f"- 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"- 修复总数：{total}",
        "- 范围：全书正文汇总、中册 part01 当前源稿。",
        "- 依据：中册 page_0102、page_0213 页级 PaddleOCR 成句证据，且正式阅读稿对应语境已为 `该厂`。",
        "- 原则：只替换两个完整厂名语境短语；不作 `广 -> 厂` 全局替换。",
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
        "- 未处理其它 `广/厂` 宽泛候选，仍需逐条回源。",
    ])
    return "\n".join(lines) + "\n"


def upsert_memory(total: int, residuals: dict[str, int]) -> None:
    block = f"""{MARKER}

- 依据页级 PaddleOCR `workbench/ocr/paddle_ocr/中/part01/page_0102.txt` 与 `workbench/ocr/paddle_ocr/中/part01/page_0213.txt`，补修中册当前源稿 `该广位于新浦海连中路26号 -> 该厂位于新浦海连中路26号`、`该广占地9.6万平方米 -> 该厂占地9.6万平方米`，同步全书正文汇总，共 {total} 处。
- 本批后检查范围：`该广位于新浦海连中路26号` {residuals['该广位于新浦海连中路26号']}，`该广占地9.6万平方米` {residuals['该广占地9.6万平方米']}。
- 未作 `广 -> 厂` 全局替换；未处理 OCR 源文件、backup、obsolete、历史交付包；未打开、展示或嵌入图片。
- 报告：`output/reports/middle_source_factory_residuals_batch341_20260708.md`；进度：`output/reports/progress/20260708_中册源稿厂字残留补修第三百四十一批.md`。
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
