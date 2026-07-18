# -*- coding: utf-8 -*-
"""Synchronize OCR-backed print/brick factory residue repairs for batch 401."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

UPPER10 = ROOT / "workbench" / "body_chapters" / "上" / "第十卷至第十六卷（part03）.md"
UPPER_SUMMARY = ROOT / "workbench" / "body_chapters" / "连云港市志_上册_正文汇总.md"
MID1 = ROOT / "workbench" / "body_chapters" / "第十七卷至第二十九卷（中part01）.md"
LOWER2 = ROOT / "workbench" / "body_chapters" / "第五十二卷至第六十卷及附录（下part02）.md"
FULL_SRC = ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md"
UPPER_READER = ROOT / "output" / "final_reader" / "连云港市志_上册.html"
MID_READER = ROOT / "output" / "final_reader" / "连云港市志_中册.html"
LOWER_READER = ROOT / "output" / "final_reader" / "连云港市志_下册.html"
FULL_READER = ROOT / "output" / "final_reader" / "连云港市志_全书.html"

REPORT = ROOT / "output" / "reports" / "verified_factory_residues_batch401_20260708.md"
REPORT_JSON = ROOT / "output" / "reports" / "verified_factory_residues_batch401_20260708.json"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260708_厂名形近残留补修第四百零一批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"
MARKER = "## 2026-07-08 厂名形近残留补修第四百零一批"

REPLACEMENTS: list[tuple[list[Path], str, str, str]] = [
    ([UPPER10, UPPER_SUMMARY, FULL_SRC], "赣榆县印刷广", "赣榆县印刷厂", "上册源稿同步：赣榆县印刷厂"),
    ([UPPER10, UPPER_SUMMARY, FULL_SRC], "备印刷广", "备印刷厂", "上册源稿同步：报社自备印刷厂"),
    ([UPPER10, UPPER_SUMMARY, FULL_SRC], "新海印刷广", "新海印刷厂", "上册源稿同步：新海印刷厂划出"),
    ([MID1, FULL_SRC], "煤渣砖广", "煤渣砖厂", "中册源稿同步：扩建煤渣砖厂"),
    ([MID1, FULL_SRC], "炉渣砖广", "炉渣砖厂", "中册源稿同步：炉渣砖厂更名"),
    ([LOWER2, FULL_SRC], "送印刷广切边", "送印刷厂切边", "下册源稿同步：送印刷厂切边"),
    ([LOWER2, FULL_SRC], "报社有印刷广", "报社有印刷厂", "下册源稿同步：报社有印刷厂"),
    ([LOWER2, FULL_SRC], "关印刷广印刷", "关印刷厂印刷", "下册源稿同步：机关印刷厂印刷"),
]

OCR_EVIDENCE = [
    ("workbench/ocr/paddle_ocr/上/part03/page_0181.txt", [36]),
    ("workbench/ocr/paddle_ocr/上/part03/page_0184.txt", [16, 17]),
    ("workbench/ocr/paddle_ocr/上/part03/page_0186.txt", [19]),
    ("workbench/ocr/paddle_ocr/上/part03/page_0188.txt", [31, 32]),
    ("workbench/ocr/paddle_ocr/中/part01/page_0273.txt", [8, 10]),
    ("workbench/ocr/paddle_ocr/下/part02/page_0067.txt", [7]),
    ("workbench/ocr/paddle_ocr/下/part02/page_0131.txt", [26]),
    ("workbench/ocr/paddle_ocr/下/part02/page_0142.txt", [24, 25]),
]

RESIDUES = [
    "赣榆县印刷广",
    "备印刷广",
    "新海印刷广",
    "煤渣砖广",
    "炉渣砖广",
    "送印刷广切边",
    "报社有印刷广",
    "关印刷广印刷",
    "在市机关印刷广印刷",
]
CHECKS = [UPPER10, UPPER_SUMMARY, MID1, LOWER2, FULL_SRC, UPPER_READER, MID_READER, LOWER_READER, FULL_READER]


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def apply_one(path: Path, old: str, new: str, label: str) -> dict[str, object]:
    text = read(path)
    old_count = text.count(old)
    if old_count:
        path.write_text(text.replace(old, new), encoding="utf-8")
        status = "fixed"
    elif new in text:
        status = "already_fixed"
    else:
        status = "not_present"
    after = read(path)
    return {"path": rel(path), "label": label, "status": status, "fixed": old_count, "new_hits": after.count(new)}


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
    out: dict[str, dict[str, int]] = {}
    for path in CHECKS:
        if path.exists():
            text = read(path)
            out[rel(path)] = {needle: text.count(needle) for needle in RESIDUES}
    return out


def write_report(results: list[dict[str, object]], residues: dict[str, dict[str, int]]) -> None:
    lines = [
        "# 厂名形近残留补修 batch401",
        "",
        f"- 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "- 范围：现行上册/中册/下册正文源稿、上册正文汇总、全书正文汇总；当前正式 reader 只做残留复扫。",
        "- 修复：依据页级 PaddleOCR 证据，同步印刷厂、煤渣砖厂、炉渣砖厂等 `广 -> 厂` 形近残留。",
        "- 保留：backup、obsolete、历史交付包和 OCR 源文件不处理；未作全局 `广 -> 厂` 替换。",
        "- 图片处理：未打开、展示或嵌入图片。",
        "",
        "## 修复明细",
    ]
    for item in results:
        lines.append(f"- `{item['path']}`：{item['label']}，状态 {item['status']}，本次替换 {item['fixed']} 处，新文本命中 {item['new_hits']}。")
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
            {"time": datetime.now().strftime("%Y-%m-%d %H:%M"), "results": results, "evidence": evidence_lines(), "residues": residues},
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    PROGRESS.write_text(REPORT.read_text(encoding="utf-8"), encoding="utf-8")


def update_memory() -> None:
    block = f"""{MARKER}

- 依据上册 PaddleOCR page_0181、0184、0186、0188，中册 page_0273，下册 page_0067、0131、0142，补修印刷厂、煤渣砖厂、炉渣砖厂等 `广 -> 厂` 形近残留。
- 修复范围为现行上册/中册/下册正文源稿、上册正文汇总、全书正文汇总；当前正式 reader 仅复扫确认相关坏形态为 0。
- 未处理 OCR 源文件、backup、obsolete、历史交付包；未作全局 `广 -> 厂` 替换；未打开、展示或嵌入图片。
- 报告：`output/reports/verified_factory_residues_batch401_20260708.md`；进度：`output/reports/progress/20260708_厂名形近残留补修第四百零一批.md`。
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
