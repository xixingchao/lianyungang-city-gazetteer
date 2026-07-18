# -*- coding: utf-8 -*-
"""Repair OCR-backed salt shipping terms for batch 409."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

UPPER_PART3 = ROOT / "workbench" / "body_chapters" / "上" / "第十卷至第十六卷（part03）.md"
UPPER_SUMMARY = ROOT / "workbench" / "body_chapters" / "连云港市志_上册_正文汇总.md"
FULL_SRC = ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md"
PADDLE_UPPER_PART3 = ROOT / "workbench" / "body_chapters" / "paddle_上" / "第十卷至第十六卷（part03）.md"
PADDLE_UPPER_SUMMARY = ROOT / "workbench" / "body_chapters" / "连云港市志_上册_PaddleOCR正文汇总.md"

REPORT = ROOT / "output" / "reports" / "verified_salt_shipping_batch409_20260708.md"
REPORT_JSON = ROOT / "output" / "reports" / "verified_salt_shipping_batch409_20260708.json"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260708_盐业趸船淮盐残留补修第四百零九批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"
MARKER = "## 2026-07-08 盐业趸船淮盐残留补修第四百零九批"

REPLACEMENTS: list[tuple[list[Path], str, str, str]] = [
    ([UPPER_PART3, UPPER_SUMMARY, FULL_SRC], "3台船和6台提式扒舱机", "3台趸船和6台提式扒舱机", "陈港坨：3台趸船"),
    ([UPPER_PART3, UPPER_SUMMARY, FULL_SRC], "制造一组船皮带机", "制造一组趸船皮带机", "陈港坨：趸船皮带机"),
    ([FULL_SRC], "召开准盐海运实行", "召开淮盐海运实行", "全书汇总：淮盐海运实行包改散"),
    ([FULL_SRC], "遂开准盐海运之途", "遂开淮盐海运之途", "全书汇总：遂开淮盐海运之途"),
    ([PADDLE_UPPER_PART3, PADDLE_UPPER_SUMMARY], "自己设计、自已\n制造", "自己设计、自己\n制造", "派生 PaddleOCR 正文：自己制造"),
]

OCR_EVIDENCE = [
    ("workbench/ocr/paddle_ocr/上/part03/page_0157.txt", [5, 6, 7]),
    ("workbench/body_chapters/上/第四卷至第十卷（part02）.md", [7810]),
    ("workbench/body_chapters/上/第十卷至第十六卷（part03）.md", [5788, 5789, 5790]),
]

RESIDUES = ["3台船和6台提式扒舱机", "制造一组船皮带机", "准盐海运", "自已\n制造", "自己设计、自已"]
CHECKS = [UPPER_PART3, UPPER_SUMMARY, FULL_SRC, PADDLE_UPPER_PART3, PADDLE_UPPER_SUMMARY]


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
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    lines = [
        "# 盐业趸船淮盐残留补修 batch409",
        "",
        f"- 生成时间：{now}",
        "- 范围：现行上册正文源稿、上册正文汇总、全书正文汇总；同步派生 PaddleOCR 正文中同段 `自已制造`。",
        "- 修复：依据页级 PaddleOCR 与现行上册正文互证，补 `3台趸船`、`趸船皮带机`、`淮盐海运`，并将派生正文 `自己设计、自已制造` 改为 `自己设计、自己制造`。",
        "- 跳过：OCR 原始文件、backup、obsolete、历史交付包；未打开、展示或嵌入图片。",
        "",
        "## 修复明细",
    ]
    for item in results:
        lines.append(f"- `{item['path']}`：{item['label']}，状态 {item['status']}，本次替换 {item['fixed']} 处，新文本命中 {item['new_hits']}。")
    lines.extend(["", "## 证据摘录"])
    for hit in evidence_lines():
        lines.append(f"- {hit}")
    lines.extend(["", "## 残留复扫"])
    for path, counts in residues.items():
        shown = ", ".join(f"{key}={value}" for key, value in counts.items())
        lines.append(f"- `{path}`：{shown}")
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    REPORT_JSON.write_text(json.dumps({"time": now, "results": results, "evidence": evidence_lines(), "residues": residues}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    PROGRESS.write_text(REPORT.read_text(encoding="utf-8"), encoding="utf-8")


def update_memory() -> None:
    block = f"""{MARKER}

- 依据 `workbench/ocr/paddle_ocr/上/part03/page_0157.txt` 和现行上册正文互证，修复陈港坨盐业段 `3台船 -> 3台趸船`、`船皮带机 -> 趸船皮带机`、全书汇总 `准盐海运 -> 淮盐海运`。
- 同步派生 PaddleOCR 正文同段 `自己设计、自已制造 -> 自己设计、自己制造`；未处理 OCR 原始文件、backup、obsolete、历史交付包；未打开、展示或嵌入图片。
- 报告：`output/reports/verified_salt_shipping_batch409_20260708.md`；进度：`output/reports/progress/20260708_盐业趸船淮盐残留补修第四百零九批.md`。
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
    results = []
    for paths, old, new, label in REPLACEMENTS:
        for path in paths:
            results.append(apply_one(path, old, new, label))
    residues = residue_counts()
    write_report(results, residues)
    update_memory()
    print(json.dumps({"changed": sum(int(item["fixed"]) for item in results), "report": str(REPORT)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
