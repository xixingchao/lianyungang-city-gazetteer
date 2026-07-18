# -*- coding: utf-8 -*-
"""Repair more source-backed 广/厂 factory-name residues for batch 397."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

MID1 = ROOT / "workbench" / "body_chapters" / "第十七卷至第二十九卷（中part01）.md"
FULL_SRC = ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md"
MID_READER = ROOT / "output" / "final_reader" / "连云港市志_中册.html"
FULL_READER = ROOT / "output" / "final_reader" / "连云港市志_全书.html"

REPORT = ROOT / "output" / "reports" / "verified_factory_names_batch397_20260708.md"
REPORT_JSON = ROOT / "output" / "reports" / "verified_factory_names_batch397_20260708.json"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260708_中册厂名形近残留补修第三百九十七批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"
MARKER = "## 2026-07-08 中册厂名形近残留补修第三百九十七批"

ALL = [MID1, FULL_SRC, MID_READER, FULL_READER]
SRC_ONLY = [MID1, FULL_SRC]

REPLACEMENTS: list[tuple[list[Path], str, str, str]] = [
    (ALL, "市农业机械厂、新海连市浅井水泵广生产", "市农业机械厂、新海连市浅井水泵厂生产", "浅井水泵厂生产水利启闭机"),
    (ALL, "市水泵广生产的IS型", "市水泵厂生产的IS型", "市水泵厂生产IS型离心泵"),
    ([FULL_SRC], "市新海印刷厂、水泵广、化工矿业专科学校", "市新海印刷厂、水泵厂、化工矿业专科学校", "南小区水泵厂职工宿舍楼"),
    (SRC_ONLY, "连云港市农业机械广试制成功", "连云港市农业机械厂试制成功", "农业机械厂试制松针粉加工设备"),
    (SRC_ONLY, "更名为连云港市农业机械广。", "更名为连云港市农业机械厂。", "连云港市农业机械厂更名沿革"),
    (ALL, "市农业\n机械广、市车辆厂、市机械修配广", "市农业\n机械厂、市车辆厂、市机械修配厂", "机械工业公司下辖厂名"),
    ([MID_READER], "市农业</p><p>机械广、市车辆厂、市机械修配广", "市农业</p><p>机械厂、市车辆厂、市机械修配厂", "机械工业公司下辖厂名-reader分段"),
    ([FULL_READER], "市农业机械广、市车辆厂、市机械修配广", "市农业机械厂、市车辆厂、市机械修配厂", "机械工业公司下辖厂名-reader连续文本"),
    (ALL, "连云港车辆广、连云港", "连云港车辆厂、连云港", "通用机械主要厂家车辆厂"),
]

OCR_EVIDENCE = [
    ("workbench/ocr/paddle_ocr/中/part01/page_0197.txt", [22]),
    ("workbench/ocr/paddle_ocr/中/part01/page_0211.txt", [24, 25]),
    ("workbench/ocr/paddle_ocr/上/part02/page_0092.txt", [31]),
    ("workbench/ocr/paddle_ocr/中/part01/page_0200.txt", [37]),
    ("workbench/ocr/paddle_ocr/中/part01/page_0202.txt", [5, 6]),
    ("workbench/ocr/paddle_ocr/中/part01/page_0193.txt", [22]),
    ("workbench/ocr/paddle_ocr/中/part01/page_0203.txt", [29, 30]),
]

RESIDUES = [
    "浅井水泵广生产",
    "市水泵广生产的IS型",
    "水泵广、化工矿业专科学校",
    "农业机械广试制成功",
    "更名为连云港市农业机械广",
    "机械修配广",
    "连云港车辆广",
]
CHECKS = [MID1, FULL_SRC, MID_READER, FULL_READER]


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def apply_one(path: Path, old: str, new: str, label: str) -> dict[str, object]:
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
        text = read(path)
        out[rel(path)] = {needle: text.count(needle) for needle in RESIDUES}
    return out


def write_report(results: list[dict[str, object]], residues: dict[str, dict[str, int]]) -> None:
    lines = [
        "# 中册厂名形近残留补修 batch397",
        "",
        f"- 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "- 范围：现行中册正文源稿、全书正文汇总、当前中册/全书 reader；另同步全书汇总中南小区一处上册证据残留。",
        "- 修复：水泵厂、农业机械厂、机械修配厂、车辆厂等可由页级 PaddleOCR 证实的 `广 -> 厂` 形近残留。",
        "- 保留：未逐页证实的其它 `广生产/广投资/广试制` 命中留待后续核对；未处理 OCR 源文件、backup、obsolete、历史交付包。",
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
    REPORT_JSON.write_text(json.dumps({"time": datetime.now().strftime("%Y-%m-%d %H:%M"), "results": results, "evidence": evidence_lines(), "residues": residues}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    PROGRESS.write_text(REPORT.read_text(encoding="utf-8"), encoding="utf-8")


def update_memory() -> None:
    block = f"""{MARKER}

- 依据中册 PaddleOCR page_0193、0197、0200、0202、0203、0211 与上册 page_0092，补修水泵厂、农业机械厂、机械修配厂、车辆厂等 `广 -> 厂` 形近残留。
- 修复范围为现行中册正文源稿、全书正文汇总、当前中册/全书 reader；另同步全书正文汇总中南小区 `水泵厂` 一处。
- 未逐页证实的其它 `广生产/广投资/广试制` 命中保留待核；未处理 OCR 源文件、backup、obsolete、历史交付包；未打开、展示或嵌入图片。
- 报告：`output/reports/verified_factory_names_batch397_20260708.md`；进度：`output/reports/progress/20260708_中册厂名形近残留补修第三百九十七批.md`。
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
