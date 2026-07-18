# -*- coding: utf-8 -*-
"""Sync source-backed 入海/厂名称 residues for batch 412."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

MID_PART1 = ROOT / "workbench" / "body_chapters" / "第十七卷至第二十九卷（中part01）.md"
MID_PART2 = ROOT / "workbench" / "body_chapters" / "第三十卷至第四十二卷（中part02）.md"
LOWER_PART2 = ROOT / "workbench" / "body_chapters" / "第五十二卷至第六十卷及附录（下part02）.md"
FULL_SRC = ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md"
MID_HTML = ROOT / "output" / "final_reader" / "连云港市志_中册.html"
LOWER_HTML = ROOT / "output" / "final_reader" / "连云港市志_下册.html"
FULL_HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"

REPORT = ROOT / "output" / "reports" / "verified_ruhai_factory_sync_batch412_20260708.md"
REPORT_JSON = ROOT / "output" / "reports" / "verified_ruhai_factory_sync_batch412_20260708.json"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260708_入海与厂名称源稿同步补修第四百一十二批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"
MARKER = "## 2026-07-08 入海与厂名称源稿同步补修第四百一十二批"

REPLACEMENTS: list[tuple[list[Path], str, str, str, str]] = [
    (
        [MID_PART2, FULL_SRC, MID_HTML, FULL_HTML],
        "徐福为其人海求仙药",
        "徐福为其入海求仙药",
        "徐福东渡语境：入海求仙药",
        "`workbench/ocr/paddle_ocr/中/part02/page_0114.txt:27` 作 `要徐福为其入海求仙药`；当前 reader 已同文，源稿残留 `人海`。",
    ),
    (
        [MID_PART2, FULL_SRC, MID_HTML, FULL_HTML],
        "自淮人海",
        "自淮入海",
        "漕运诏令：自淮入海",
        "`workbench/ocr/paddle_ocr/中/part02/page_0245.txt:10` 作 `诏令运十二万石自淮入海`；当前 reader 已同文，源稿残留 `人海`。",
    ),
    (
        [LOWER_PART2, FULL_SRC, LOWER_HTML, FULL_HTML],
        "导淮入江人海之研究",
        "导淮入江入海之研究",
        "著作名：导淮入江入海之研究",
        "`workbench/ocr/paddle_ocr/下/part02/page_0350.txt:28` 作 `导淮入江入海之研究`；当前 reader 已同文，源稿残留 `人海`。",
    ),
    (
        [MID_PART1, FULL_SRC, MID_HTML, FULL_HTML],
        "无线电专用设备广名称",
        "无线电专用设备厂名称",
        "企业名称：无线电专用设备厂名称",
        "`workbench/ocr/paddle_ocr/中/part01/page_0265.txt:29` 作 `无线电专用设备厂名称`；同页多处均为 `无线电专用设备厂`。",
    ),
]

EVIDENCE_REFS = [
    ("workbench/ocr/paddle_ocr/中/part02/page_0114.txt", [25, 26, 27, 28]),
    ("workbench/ocr/paddle_ocr/中/part02/page_0245.txt", [10]),
    ("workbench/ocr/paddle_ocr/下/part02/page_0350.txt", [28]),
    ("workbench/ocr/paddle_ocr/中/part01/page_0265.txt", [24, 26, 29]),
]

RESIDUES = [
    "人海求仙药",
    "自淮人海",
    "导淮入江人海",
    "无线电专用设备广名称",
]

SCAN_TARGETS = [MID_PART1, MID_PART2, LOWER_PART2, FULL_SRC, MID_HTML, LOWER_HTML, FULL_HTML]


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def apply_one(path: Path, old: str, new: str, label: str, basis: str) -> dict[str, object]:
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
    return {
        "path": rel(path),
        "label": label,
        "basis": basis,
        "status": status,
        "fixed": old_count,
        "new_hits": after.count(new),
    }


def evidence_lines() -> list[str]:
    out: list[str] = []
    for rel_path, nums in EVIDENCE_REFS:
        path = ROOT / rel_path
        if not path.exists():
            out.append(f"{rel_path}: missing")
            continue
        lines = read(path).splitlines()
        for num in nums:
            if 1 <= num <= len(lines):
                out.append(f"{rel_path}:{num}: {lines[num - 1].strip()}")
    return out


def residue_counts() -> dict[str, dict[str, int]]:
    out: dict[str, dict[str, int]] = {}
    for path in SCAN_TARGETS:
        if path.exists():
            text = read(path)
            out[rel(path)] = {needle: text.count(needle) for needle in RESIDUES}
    return out


def write_report(results: list[dict[str, object]], residues: dict[str, dict[str, int]]) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    lines = [
        "# 入海与厂名称源稿同步补修 batch412",
        "",
        f"- 生成时间：{now}",
        "- 范围：中册 part01/part02、下册 part02、全书正文汇总、当前中册/下册/全书 reader。",
        "- 修复：精确同步 `人海 -> 入海` 三处源稿残留，并修复当前 reader 仍残留的 `无线电专用设备广名称 -> 无线电专用设备厂名称`。",
        "- 跳过：OCR 原始文件、backup、obsolete、历史交付包；未打开、展示或嵌入图片。",
        "",
        "## 修复明细",
    ]
    for item in results:
        lines.append(
            f"- `{item['path']}`：{item['label']}，状态 {item['status']}，"
            f"本次替换 {item['fixed']} 处，新文本命中 {item['new_hits']}。依据：{item['basis']}"
        )
    lines.extend(["", "## 证据摘录"])
    for hit in evidence_lines():
        lines.append(f"- {hit}")
    lines.extend(["", "## 残留复扫"])
    for path, counts in residues.items():
        shown = ", ".join(f"{key}={value}" for key, value in counts.items())
        lines.append(f"- `{path}`：{shown}")
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    REPORT_JSON.write_text(
        json.dumps({"time": now, "results": results, "evidence": evidence_lines(), "residues": residues}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    PROGRESS.write_text(REPORT.read_text(encoding="utf-8"), encoding="utf-8")


def update_memory() -> None:
    block = f"""{MARKER}

- 补修中册 part01/part02、下册 part02、全书正文汇总、当前中册/下册/全书 reader 中 4 处证据明确残留：`徐福为其人海求仙药 -> 徐福为其入海求仙药`、`自淮人海 -> 自淮入海`、`导淮入江人海之研究 -> 导淮入江入海之研究`、`无线电专用设备广名称 -> 无线电专用设备厂名称`。
- 其中三处 `入海` 在当前 reader 已正确，本批主要同步源稿；`无线电专用设备厂名称` 依据 `workbench/ocr/paddle_ocr/中/part01/page_0265.txt:29` 并同步当前中册/全书 reader。
- 未处理 OCR 原始文件、backup、obsolete、历史交付包；未打开、展示或嵌入图片。
- 报告：`output/reports/verified_ruhai_factory_sync_batch412_20260708.md`；进度：`output/reports/progress/20260708_入海与厂名称源稿同步补修第四百一十二批.md`。
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
    for paths, old, new, label, basis in REPLACEMENTS:
        for path in paths:
            results.append(apply_one(path, old, new, label, basis))
    residues = residue_counts()
    write_report(results, residues)
    update_memory()
    changed = sum(int(item["fixed"]) for item in results)
    print(json.dumps({"changed": changed, "report": str(REPORT)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
