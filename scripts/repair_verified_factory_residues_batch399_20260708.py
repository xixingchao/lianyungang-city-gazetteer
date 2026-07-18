# -*- coding: utf-8 -*-
"""Repair another OCR-backed 广/厂 factory-name residue set for batch 399."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

MID1 = ROOT / "workbench" / "body_chapters" / "第十七卷至第二十九卷（中part01）.md"
FULL_SRC = ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md"
MID_READER = ROOT / "output" / "final_reader" / "连云港市志_中册.html"
FULL_READER = ROOT / "output" / "final_reader" / "连云港市志_全书.html"

REPORT = ROOT / "output" / "reports" / "verified_factory_residues_batch399_20260708.md"
REPORT_JSON = ROOT / "output" / "reports" / "verified_factory_residues_batch399_20260708.json"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260708_厂名形近残留补修第三百九十九批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"
MARKER = "## 2026-07-08 厂名形近残留补修第三百九十九批"

ALL = [MID1, FULL_SRC, MID_READER, FULL_READER]
SRC_ONLY = [MID1, FULL_SRC]

REPLACEMENTS: list[tuple[list[Path], str, str, str]] = [
    (ALL, "市混凝土构件广建成", "市混凝土构件厂建成", "市混凝土构件厂建成圆孔板挤压生产线"),
    (ALL, "新海油广生产", "新海油厂生产", "新海油厂生产谷维素"),
    (SRC_ONLY, "曙光化工广生产", "曙光化工厂生产", "曙光化工厂生产无水硫酸钠"),
    (ALL, "灌云县玩具广更名", "灌云县玩具厂更名", "灌云县玩具厂更名为连云港市童车厂"),
    (ALL, "赣榆县石英广更名", "赣榆县石英厂更名", "赣榆县石英厂更名为赣榆县陶瓷厂"),
    (ALL, "赣榆县标准件广", "赣榆县标准件厂", "赣榆县标准件厂生产小规格标准件"),
    (ALL, "海州五金制造广", "海州五金制造厂", "海州五金制造厂更名为海州标准件厂"),
    (ALL, "赣榆县粮食酒广", "赣榆县粮食酒厂", "赣榆县粮食酒厂生产大曲酒"),
    (ALL, "连云港微波电器广", "连云港微波电器厂", "连云港微波电器厂引进微波炉组件"),
]

OCR_EVIDENCE = [
    ("workbench/ocr/paddle_ocr/中/part01/page_0032.txt", [37, 38, 39]),
    ("workbench/ocr/paddle_ocr/中/part01/page_0048.txt", [10, 11]),
    ("workbench/ocr/paddle_ocr/中/part01/page_0123.txt", [10, 11]),
    ("workbench/ocr/paddle_ocr/中/part01/page_0210.txt", [4, 5, 6]),
    ("workbench/ocr/paddle_ocr/中/part01/page_0243.txt", [6, 7]),
    ("workbench/ocr/paddle_ocr/中/part01/page_0313.txt", [30, 31]),
    ("workbench/ocr/paddle_ocr/中/part01/page_0402.txt", [37, 38]),
]

RESIDUES = [
    "市混凝土构件广建成",
    "新海油广生产",
    "曙光化工广生产",
    "灌云县玩具广更名",
    "赣榆县石英广更名",
    "赣榆县标准件广",
    "海州五金制造广",
    "赣榆县粮食酒广",
    "连云港微波电器广",
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
        "# 厂名形近残留补修 batch399",
        "",
        f"- 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "- 范围：现行中册正文源稿、全书正文汇总、当前中册/全书 reader；其中 `曙光化工厂生产` 当前仅同步源稿。",
        "- 修复：混凝土构件厂、新海油厂、曙光化工厂、玩具厂、石英厂、标准件厂、五金制造厂、粮食酒厂、微波电器厂等可由页级 PaddleOCR 证实的 `广 -> 厂` 形近残留。",
        "- 保留：未逐页证实的 `灌云县工艺美术品广` 等其它命中留待后续核对；未处理 OCR 源文件、backup、obsolete、历史交付包。",
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

- 依据中册 PaddleOCR page_0032、0048、0123、0210、0243、0313、0402，补修混凝土构件厂、新海油厂、曙光化工厂、玩具厂、石英厂、标准件厂、五金制造厂、粮食酒厂、微波电器厂等 `广 -> 厂` 形近残留。
- 修复范围为现行中册正文源稿、全书正文汇总、当前中册/全书 reader；其中 `曙光化工厂生产` 当前仅同步源稿。
- 未逐页证实的 `灌云县工艺美术品广` 等其它命中保留待核；未处理 OCR 源文件、backup、obsolete、历史交付包；未打开、展示或嵌入图片。
- 报告：`output/reports/verified_factory_residues_batch399_20260708.md`；进度：`output/reports/progress/20260708_厂名形近残留补修第三百九十九批.md`。
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
