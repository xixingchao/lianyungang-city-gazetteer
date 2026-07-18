# -*- coding: utf-8 -*-
"""Repair OCR-backed 人/入 term residues for batch 407."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

UPPER_OVERVIEW = ROOT / "workbench" / "body_chapters" / "上" / "总述与大事记.md"
UPPER_COUNTY = ROOT / "workbench" / "body_chapters" / "上" / "第三卷_区县概况.md"
UPPER_PART2 = ROOT / "workbench" / "body_chapters" / "上" / "第四卷至第十卷（part02）.md"
LOWER_PART2 = ROOT / "workbench" / "body_chapters" / "第五十二卷至第六十卷及附录（下part02）.md"
UPPER_SUMMARY = ROOT / "workbench" / "body_chapters" / "连云港市志_上册_正文汇总.md"
FULL_SRC = ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md"

READERS = [
    ROOT / "output" / "final_reader" / "连云港市志_上册.html",
    ROOT / "output" / "final_reader" / "连云港市志_下册.html",
    ROOT / "output" / "final_reader" / "连云港市志_全书.html",
]

REPORT = ROOT / "output" / "reports" / "verified_ren_ru_terms_batch407_20260708.md"
REPORT_JSON = ROOT / "output" / "reports" / "verified_ren_ru_terms_batch407_20260708.json"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260708_人入形近术语残留补修第四百零七批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"
MARKER = "## 2026-07-08 人入形近术语残留补修第四百零七批"

REPLACEMENTS: list[tuple[list[Path], str, str, str]] = [
    ([UPPER_OVERVIEW, UPPER_SUMMARY, FULL_SRC], "喇叭人户率70%", "喇叭入户率70%", "总述广播电视：喇叭入户率70%"),
    ([UPPER_OVERVIEW, UPPER_SUMMARY], "人党宣誓在陇海公寓", "入党宣誓在陇海公寓", "大事记：入党宣誓在陇海公寓"),
    ([UPPER_COUNTY, UPPER_SUMMARY, FULL_SRC], "喇叭人户率78%", "喇叭入户率78%", "赣榆县概况：喇叭入户率78%"),
    ([UPPER_PART2, UPPER_SUMMARY, FULL_SRC], "排人港口\n水域", "排入港口\n水域", "环境保护：排入港口水域"),
    ([LOWER_PART2, FULL_SRC], "喇叭人户率为78%", "喇叭入户率为78%", "下册广播章：喇叭入户率为78%"),
]

OCR_EVIDENCE = [
    ("workbench/ocr/paddle_ocr/上/part01/page_0039.txt", [12]),
    ("workbench/ocr/paddle_ocr/上/part01/page_0116.txt", [28]),
    ("workbench/ocr/paddle_ocr/上/part01/page_0262.txt", [7]),
    ("workbench/ocr/paddle_ocr/上/part02/page_0126.txt", [121, 122]),
    ("workbench/ocr/paddle_ocr/下/part02/page_0147.txt", [8, 27]),
]

RESIDUES = ["人党宣誓", "喇叭人户率", "排人港口"]
CHECKS = [UPPER_OVERVIEW, UPPER_COUNTY, UPPER_PART2, LOWER_PART2, UPPER_SUMMARY, FULL_SRC, *READERS]


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
        "# 人入形近术语残留补修 batch407",
        "",
        f"- 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "- 范围：现行上册/下册正文源稿、上册正文汇总、全书正文汇总；当前 reader 只复扫，不主动重写。",
        "- 修复：依据 PaddleOCR 正文证据与同章术语一致性，补修 `入党宣誓`、`喇叭入户率`、`排入港口水域`。",
        "- 保留：`人户分离`、`参加人数`、`在编人员`、`外流人员` 等正常词不处理；OCR 源文件、backup、obsolete、历史交付包不处理。",
        "- 图片处理：未打开、展示或嵌入图片。",
        "",
        "## 修复明细",
    ]
    for item in results:
        lines.append(f"- `{item['path']}`：{item['label']}，状态 {item['status']}，本次替换 {item['fixed']} 处，新文本命中 {item['new_hits']}。")
    lines.extend(["", "## OCR/术语证据摘录"])
    for hit in evidence_lines():
        lines.append(f"- {hit}")
    lines.append("- 下册 `workbench/ocr/paddle_ocr/下/part02/page_0147.txt:8` 原 OCR 仍作 `喇叭人户率为78%`，但同页第 27 行和同章通用术语均为 `入户率`，当前 reader 亦已同步为 `喇叭入户率为78%`，故按术语一致性修正文稿。")
    lines.extend(["", "## 残留复扫"])
    for path, counts in residues.items():
        shown = ", ".join(f"{key}={value}" for key, value in counts.items())
        lines.append(f"- `{path}`：{shown}")
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    REPORT_JSON.write_text(
        json.dumps({"time": datetime.now().strftime("%Y-%m-%d %H:%M"), "results": results, "evidence": evidence_lines(), "residues": residues}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    PROGRESS.write_text(REPORT.read_text(encoding="utf-8"), encoding="utf-8")


def update_memory() -> None:
    block = f"""{MARKER}

- 依据 PaddleOCR `上/part01/page_0039.txt`、`page_0116.txt`、`page_0262.txt`、`上/part02/page_0126.txt`，补修上册现行源稿和汇总中的 `喇叭人户率70% -> 喇叭入户率70%`、`人党宣誓在陇海公寓 -> 入党宣誓在陇海公寓`、`喇叭人户率78% -> 喇叭入户率78%`、`排人港口水域 -> 排入港口水域`。
- 下册广播章 `喇叭人户率为78%` 依同页 `入户率达67%`、同章术语和当前 reader 文本同步修为 `喇叭入户率为78%`；该处 OCR 本身仍误作 `人户率`，报告中已注明。
- 修复范围为现行正文源稿、上册正文汇总、全书正文汇总；当前 reader 只复扫；未处理 OCR 源文件、backup、obsolete、历史交付包；未打开、展示或嵌入图片。
- 报告：`output/reports/verified_ren_ru_terms_batch407_20260708.md`；进度：`output/reports/progress/20260708_人入形近术语残留补修第四百零七批.md`。
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
