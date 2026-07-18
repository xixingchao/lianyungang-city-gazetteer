# -*- coding: utf-8 -*-
"""Repair OCR-backed factory 广/厂 residues for batch 406."""

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
MID_READER = ROOT / "output" / "final_reader" / "连云港市志_中册.html"
FULL_READER = ROOT / "output" / "final_reader" / "连云港市志_全书.html"

REPORT = ROOT / "output" / "reports" / "verified_factory_residues_batch406_20260708.md"
REPORT_JSON = ROOT / "output" / "reports" / "verified_factory_residues_batch406_20260708.json"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260708_厂名形近残留补修第四百零六批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"
MARKER = "## 2026-07-08 厂名形近残留补修第四百零六批"

REPLACEMENTS: list[tuple[list[Path], str, str, str]] = [
    ([MID1, FULL_SRC], "专业工广", "专业工厂", "中册源稿同步：专业工厂"),
    ([MID1, FULL_SRC], "锦屏机\n械广", "锦屏机\n械厂", "中册源稿同步：锦屏机械厂"),
    ([MID1, FULL_SRC], "制药广改名", "制药厂改名", "中册源稿同步：一师制药厂改名"),
    ([MID1, FULL_SRC], "市第二农药广", "市第二农药厂", "中册源稿同步：市第二农药厂"),
    ([MID1, FULL_SRC, MID_READER], "市石灰广为扩大", "市石灰厂为扩大", "中册源稿/reader：市石灰厂为扩大生产"),
    ([UPPER10, UPPER_SUMMARY, FULL_SRC], "棉纺织广", "棉纺织厂", "上册源稿同步：棉纺织厂"),
    ([UPPER10, UPPER_SUMMARY, FULL_SRC], "市纺织广深化", "市纺织厂深化", "上册源稿同步：市纺织厂深化改革"),
    ([UPPER10, UPPER_SUMMARY, FULL_SRC], "棉织广，", "棉织厂，", "上册源稿同步：棉织厂"),
    ([UPPER10, UPPER_SUMMARY, FULL_SRC], "染织广5个", "染织厂5个", "上册源稿同步：染织厂5个厂家"),
    ([UPPER10, UPPER_SUMMARY, FULL_SRC], "市针织广了解到", "市针织厂了解到", "上册源稿同步：市针织厂了解到"),
    ([UPPER10, UPPER_SUMMARY], "塑料四广为", "塑料四厂为", "上册源稿同步：市塑料四厂"),
    ([LOWER2, FULL_SRC], "分广厂\n长", "分厂厂\n长", "下册源稿同步：新海油厂分厂厂长"),
    ([FULL_READER], "分广厂长", "分厂厂长", "全书 reader：新海油厂分厂厂长"),
]

OCR_EVIDENCE = [
    ("workbench/ocr/paddle_ocr/中/part01/page_0284.txt", [8, 9]),
    ("workbench/ocr/paddle_ocr/中/part01/page_0220.txt", [28, 29]),
    ("workbench/ocr/paddle_ocr/中/part01/page_0123.txt", [34]),
    ("workbench/ocr/paddle_ocr/中/part01/page_0169.txt", [210]),
    ("workbench/ocr/paddle_ocr/中/part01/page_0278.txt", [35]),
    ("workbench/ocr/paddle_ocr/上/part03/page_0228.txt", [4, 5]),
    ("workbench/ocr/paddle_ocr/上/part03/page_0233.txt", [17]),
    ("workbench/ocr/paddle_ocr/上/part03/page_0235.txt", [18]),
    ("workbench/ocr/paddle_ocr/上/part03/page_0236.txt", [18]),
    ("workbench/ocr/paddle_ocr/上/part03/page_0238.txt", [9]),
    ("workbench/ocr/paddle_ocr/上/part03/page_0246.txt", [12]),
    ("workbench/ocr/paddle_ocr/上/part03/page_0285.txt", [14]),
    ("workbench/ocr/paddle_ocr/下/part02/page_0370.txt", [24, 25]),
]

RESIDUES = [
    "专业工广",
    "锦屏机\n械广",
    "锦屏机械广",
    "制药广改名",
    "市第二农药广",
    "市石灰广为扩大",
    "棉纺织广",
    "市纺织广深化",
    "棉织广，",
    "染织广5个",
    "市针织广了解到",
    "塑料四广为",
    "分广厂\n长",
    "分广厂长",
]
CHECKS = [UPPER10, UPPER_SUMMARY, MID1, LOWER2, FULL_SRC, MID_READER, FULL_READER]


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
        "# 厂名形近残留补修 batch406",
        "",
        f"- 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "- 范围：现行上册/中册/下册正文源稿、上册正文汇总、全书正文汇总，以及当前中册/全书 reader 中同源坏形态。",
        "- 修复：依据页级 PaddleOCR 证据，补修专业工厂、锦屏机械厂、一师制药厂、市第二农药厂、市石灰厂、棉纺织厂、市纺织厂、棉织厂、染织厂、市针织厂、市塑料四厂、新海油厂分厂厂长等 `广 -> 厂` 残留。",
        "- 保留：正常词 `广泛`、`广播`、`推广长话`、`广为流传`、`广场`、`广告` 等不处理；OCR 源文件、backup、obsolete、历史交付包不处理。",
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
        json.dumps({"time": datetime.now().strftime("%Y-%m-%d %H:%M"), "results": results, "evidence": evidence_lines(), "residues": residues}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    PROGRESS.write_text(REPORT.read_text(encoding="utf-8"), encoding="utf-8")


def update_memory() -> None:
    block = f"""{MARKER}

- 依据中册 PaddleOCR `page_0123.txt`、`page_0169.txt`、`page_0220.txt`、`page_0278.txt`、`page_0284.txt`，上册 `part03/page_0228.txt`、`page_0233.txt`、`page_0235.txt`、`page_0236.txt`、`page_0238.txt`、`page_0246.txt`、`page_0285.txt`，下册 `part02/page_0370.txt`，补修专业工厂、锦屏机械厂、一师制药厂、市第二农药厂、市石灰厂、棉纺织厂、市纺织厂、棉织厂、染织厂、市针织厂、市塑料四厂、新海油厂分厂厂长等残留。
- 修复范围为现行上册/中册/下册正文源稿、上册正文汇总、全书正文汇总，以及当前中册/全书 reader 中同源坏形态；未处理 OCR 源文件、backup、obsolete、历史交付包；未打开、展示或嵌入图片。
- 正常词 `广泛`、`广播`、`推广长话`、`广为流传`、`广场`、`广告` 等继续保留。
- 报告：`output/reports/verified_factory_residues_batch406_20260708.md`；进度：`output/reports/progress/20260708_厂名形近残留补修第四百零六批.md`。
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
