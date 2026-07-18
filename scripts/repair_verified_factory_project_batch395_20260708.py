# -*- coding: utf-8 -*-
"""Repair source-backed 厂/项目 OCR residues for batch 395."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

UPPER3 = ROOT / "workbench" / "body_chapters" / "上" / "第十卷至第十六卷（part03）.md"
UPPER_SUMMARY = ROOT / "workbench" / "body_chapters" / "连云港市志_上册_正文汇总.md"
MID1 = ROOT / "workbench" / "body_chapters" / "第十七卷至第二十九卷（中part01）.md"
FULL_SRC = ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md"
MID_READER = ROOT / "output" / "final_reader" / "连云港市志_中册.html"
FULL_READER = ROOT / "output" / "final_reader" / "连云港市志_全书.html"

REPORT = ROOT / "output" / "reports" / "verified_factory_project_batch395_20260708.md"
REPORT_JSON = ROOT / "output" / "reports" / "verified_factory_project_batch395_20260708.json"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260708_可证厂项目形近残留补修第三百九十五批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"
MARKER = "## 2026-07-08 可证厂项目形近残留补修第三百九十五批"

REPLACEMENTS: list[tuple[list[Path], str, str, str]] = [
    (
        [UPPER3, UPPER_SUMMARY, FULL_SRC, FULL_READER],
        "盐业机械广研制",
        "盐业机械厂研制",
        "盐业机械厂研制压池破碴两用机",
    ),
    (
        [MID1, FULL_SRC, MID_READER, FULL_READER],
        "车辆广研制",
        "车辆厂研制",
        "车辆厂研制集装箱自装卸半挂汽车列车",
    ),
    (
        [MID1, FULL_SRC, MID_READER, FULL_READER],
        "皮革机械广研制",
        "皮革机械厂研制",
        "皮革机械厂研制通过式压花机",
    ),
    (
        [MID1, FULL_SRC, MID_READER, FULL_READER],
        "对项自进",
        "对项目进",
        "海关统计对项目进行解除",
    ),
]

OCR_EVIDENCE = [
    ("workbench/ocr/paddle_ocr/上/part03/page_0139.txt", [22]),
    ("workbench/ocr/paddle_ocr/中/part01/page_0206.txt", [25]),
    ("workbench/ocr/paddle_ocr/中/part01/page_0217.txt", [12]),
    ("workbench/ocr/paddle_ocr/中/part01/page_0503.txt", [25, 26]),
]

RESIDUES = [
    "盐业机械广研制",
    "车辆广研制",
    "皮革机械广研制",
    "对项自进",
]
CHECK_PATHS = [UPPER3, UPPER_SUMMARY, MID1, FULL_SRC, MID_READER, FULL_READER]


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def apply_one(path: Path, old: str, new: str, label: str) -> dict[str, object]:
    if not path.exists():
        return {"path": rel(path), "label": label, "status": "missing", "fixed": 0, "new_hits": 0}
    text = read(path)
    old_count = text.count(old)
    if old_count:
        text = text.replace(old, new)
        path.write_text(text, encoding="utf-8")
        status = "fixed"
    elif new in text:
        status = "already_fixed"
    else:
        status = "not_present"
    after = read(path)
    return {
        "path": rel(path),
        "label": label,
        "status": status,
        "fixed": old_count,
        "new_hits": after.count(new),
    }


def evidence_lines() -> list[str]:
    out: list[str] = []
    for rel_path, nums in OCR_EVIDENCE:
        path = ROOT / rel_path
        lines = read(path).splitlines()
        for num in nums:
            if 1 <= num <= len(lines):
                out.append(f"{rel_path}:{num}: {lines[num - 1].strip()}")
    return out


def residue_counts() -> dict[str, dict[str, int]]:
    counts: dict[str, dict[str, int]] = {}
    for path in CHECK_PATHS:
        if path.exists():
            text = read(path)
            counts[rel(path)] = {needle: text.count(needle) for needle in RESIDUES}
    return counts


def write_report(results: list[dict[str, object]], residues: dict[str, dict[str, int]]) -> None:
    lines = [
        "# 可证厂项目形近残留补修 batch395",
        "",
        f"- 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "- 范围：现行上册/中册正文源稿、上册汇总、全书正文汇总、当前中册/全书 reader。",
        "- 修复：`盐业机械广研制 -> 盐业机械厂研制`、`车辆广研制 -> 车辆厂研制`、`皮革机械广研制 -> 皮革机械厂研制`、`对项自进 -> 对项目进`。",
        "- 依据：对应页级 PaddleOCR 明确读为 `厂研制`、`对项目进/行解除`。",
        "- 保留：`这是一项自动控制多` 属正常跨词命中；`行解除` 未扩修，留待后续原图复核。",
        "- 图片处理：未打开、展示或嵌入图片。",
        "",
        "## 修复明细",
    ]
    for item in results:
        lines.append(
            f"- `{item['path']}`：{item['label']}，状态 {item['status']}，本次替换 {item['fixed']} 处，新文本命中 {item['new_hits']}。"
        )
    lines.extend(["", "## OCR 证据摘录"])
    for hit in evidence_lines():
        lines.append(f"- {hit}")
    lines.extend(["", "## 残留复扫"])
    for path, counts in residues.items():
        shown = ", ".join(f"{key}={value}" for key, value in counts.items())
        lines.append(f"- `{path}`：{shown}")
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    REPORT_JSON.write_text(
        json.dumps(
            {
                "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "results": results,
                "evidence": evidence_lines(),
                "residues": residues,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    PROGRESS.write_text(REPORT.read_text(encoding="utf-8"), encoding="utf-8")


def update_memory() -> None:
    block = f"""{MARKER}

- 依据 `workbench/ocr/paddle_ocr/上/part03/page_0139.txt`、`workbench/ocr/paddle_ocr/中/part01/page_0206.txt`、`page_0217.txt`、`page_0503.txt`，补修 `广/厂` 与 `项自/项目` 形近残留。
- 修复范围包括现行上册/中册正文源稿、上册正文汇总、全书正文汇总、当前中册/全书 reader；`这是一项自动控制多` 属正常跨词命中，未处理；`行解除` 未扩修，留待后续原图复核。
- 未处理 OCR 源文件、backup、obsolete、历史交付包；未打开、展示或嵌入图片。
- 报告：`output/reports/verified_factory_project_batch395_20260708.md`；进度：`output/reports/progress/20260708_可证厂项目形近残留补修第三百九十五批.md`。
"""
    old = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    start = old.find(MARKER)
    if start < 0:
        MEMORY.write_text(old.rstrip() + "\n\n" + block.strip() + "\n", encoding="utf-8")
        return
    next_start = old.find("\n## ", start + 1)
    if next_start < 0:
        MEMORY.write_text(old[:start].rstrip() + "\n\n" + block.strip() + "\n", encoding="utf-8")
    else:
        MEMORY.write_text(old[:start].rstrip() + "\n\n" + block.strip() + old[next_start:], encoding="utf-8")


def main() -> None:
    results: list[dict[str, object]] = []
    for paths, old, new, label in REPLACEMENTS:
        for path in paths:
            results.append(apply_one(path, old, new, label))
    residues = residue_counts()
    write_report(results, residues)
    update_memory()
    print("results=" + json.dumps(results, ensure_ascii=False))
    print(f"report={REPORT}")


if __name__ == "__main__":
    main()
