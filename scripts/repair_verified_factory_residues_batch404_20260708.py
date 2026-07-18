# -*- coding: utf-8 -*-
"""Repair OCR-backed factory 广/厂 residues for batch 404."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

MID1 = ROOT / "workbench" / "body_chapters" / "第十七卷至第二十九卷（中part01）.md"
FULL_SRC = ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md"
MID_READER = ROOT / "output" / "final_reader" / "连云港市志_中册.html"
FULL_READER = ROOT / "output" / "final_reader" / "连云港市志_全书.html"

REPORT = ROOT / "output" / "reports" / "verified_factory_residues_batch404_20260708.md"
REPORT_JSON = ROOT / "output" / "reports" / "verified_factory_residues_batch404_20260708.json"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260708_厂名形近残留补修第四百零四批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"
MARKER = "## 2026-07-08 厂名形近残留补修第四百零四批"

REPLACEMENTS: list[tuple[list[Path], str, str, str]] = [
    ([MID1, FULL_SRC], "华兴铁\n工广迁往徐州市", "华兴铁\n工厂迁往徐州市", "中册源稿同步：华兴铁工厂迁往徐州市"),
    ([MID_READER], "华兴铁</p><p>工广迁往徐州市", "华兴铁</p><p>工厂迁往徐州市", "中册 reader：华兴铁工厂迁往徐州市"),
    ([MID1, FULL_SRC], "水产品冷\n冻加工广约79家", "水产品冷\n冻加工厂约79家", "中册源稿同步：水产品冷冻加工厂约79家"),
    ([MID1, FULL_SRC], "云台等采\n右广，采用机器打眼", "云台等采\n石厂，采用机器打眼", "中册源稿同步：云台等采石厂"),
    ([MID_READER], "云台等采</p><p>右广，采用机器打眼", "云台等采</p><p>石厂，采用机器打眼", "中册 reader：云台等采石厂"),
    ([FULL_READER], "云台等采右广，采用机器打眼", "云台等采石厂，采用机器打眼", "全书 reader：云台等采石厂"),
    ([MID1, FULL_SRC, MID_READER, FULL_READER], "采石广", "采石厂", "中册源稿/reader：灌云县采石公司下设采石厂"),
]

OCR_EVIDENCE = [
    ("workbench/ocr/paddle_ocr/中/part01/page_0197.txt", [16, 17]),
    ("workbench/ocr/paddle_ocr/中/part01/page_0062.txt", [25, 26]),
    ("workbench/ocr/paddle_ocr/中/part01/page_0269.txt", [19, 20]),
    ("workbench/ocr/paddle_ocr/中/part01/page_0276.txt", [20, 21]),
]

RESIDUES = [
    "工广迁往",
    "华兴铁\n工广",
    "华兴铁</p><p>工广",
    "冷\n冻加工广",
    "采\n右广",
    "采</p><p>右广",
    "采右广",
    "采石广",
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
        text = read(path)
        out[rel(path)] = {needle: text.count(needle) for needle in RESIDUES}
    return out


def write_report(results: list[dict[str, object]], residues: dict[str, dict[str, int]]) -> None:
    lines = [
        "# 厂名形近残留补修 batch404",
        "",
        f"- 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "- 范围：现行中册正文源稿、全书正文汇总、当前中册 reader、当前全书 reader。",
        "- 修复：依据页级 PaddleOCR 证据，补修华兴铁工厂迁往徐州市、水产品冷冻加工厂约79家、灌云采石公司下设采石厂等 `广 -> 厂` 形近残留。",
        "- 保留：OCR 同段显示 `罘山`，当前源稿作 `栗山`，本批只修 `采石厂` 字形残留，不顺手改山名；backup、obsolete、历史包和 OCR 源文件不处理。",
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

- 依据中册 PaddleOCR `page_0197.txt`、`page_0062.txt`、`page_0269.txt`、`page_0276.txt`，补修 `华兴铁工厂迁往徐州市`、`水产品冷冻加工厂约79家`、`云台等采石厂`、`采石厂，所采石料` 等 `广 -> 厂` 形近残留。
- 修复范围为现行中册正文源稿、全书正文汇总、当前中册 reader、当前全书 reader；未处理 OCR 源文件、backup、obsolete、历史交付包；未打开、展示或嵌入图片。
- 同段 OCR 显示 `罘山`，当前源稿作 `栗山`，本批未顺手改山名，只处理已闭环的厂名/厂类残留。
- 报告：`output/reports/verified_factory_residues_batch404_20260708.md`；进度：`output/reports/progress/20260708_厂名形近残留补修第四百零四批.md`。
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
