# -*- coding: utf-8 -*-
"""Repair OCR-backed 广/厂 factory-name residues for batch 398."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

MID1 = ROOT / "workbench" / "body_chapters" / "第十七卷至第二十九卷（中part01）.md"
LOW1 = ROOT / "workbench" / "body_chapters" / "第四十三卷至第五十一卷（下part01）.md"
FULL_SRC = ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md"
MID_READER = ROOT / "output" / "final_reader" / "连云港市志_中册.html"
LOW_READER = ROOT / "output" / "final_reader" / "连云港市志_下册.html"
FULL_READER = ROOT / "output" / "final_reader" / "连云港市志_全书.html"

REPORT = ROOT / "output" / "reports" / "verified_factory_residues_batch398_20260708.md"
REPORT_JSON = ROOT / "output" / "reports" / "verified_factory_residues_batch398_20260708.json"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260708_厂名形近残留补修第三百九十八批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"
MARKER = "## 2026-07-08 厂名形近残留补修第三百九十八批"

MID_ALL = [MID1, FULL_SRC, MID_READER, FULL_READER]
LOW_ALL = [LOW1, FULL_SRC, LOW_READER, FULL_READER]

REPLACEMENTS: list[tuple[list[Path], str, str, str]] = [
    (MID_ALL, "海州古楼街综合广生产", "海州古楼街综合厂生产", "海州古楼街综合厂生产木制摇类玩具"),
    (MID_ALL, "灌云县酒广投资", "灌云县酒厂投资", "灌云县酒厂投资高粱酒车间"),
    (MID_ALL, "灌云县镜花缘酒广", "灌云县镜花缘酒厂", "灌云县镜花缘酒厂成立"),
    (MID_ALL, "市洪门果酒广", "市洪门果酒厂", "市洪门果酒厂生产山楂酒"),
    (MID_ALL, "土城、朱堵农具广生产", "土城、朱堵农具厂生产", "土城、朱堵农具厂生产肥播机"),
    ([MID1, FULL_SRC], "连云港市变压器\n广试制", "连云港市变压器\n厂试制", "连云港市变压器厂试制大型变压器-source"),
    ([MID_READER], "连云港市变压器</p><p>广试制", "连云港市变压器</p><p>厂试制", "连云港市变压器厂试制大型变压器-reader分段"),
    ([FULL_READER], "连云港市变压器广试制", "连云港市变压器厂试制", "连云港市变压器厂试制大型变压器-reader连续文本"),
    ([MID1, FULL_SRC], "上海电\n梯广生产", "上海电\n梯厂生产", "上海电梯厂生产载人电梯-source"),
    ([MID_READER], "上海电</p><p>梯广生产", "上海电</p><p>梯厂生产", "上海电梯厂生产载人电梯-reader分段"),
    ([FULL_READER], "上海电梯广生产", "上海电梯厂生产", "上海电梯厂生产载人电梯-reader连续文本"),
    (MID_ALL, "市黄海电器广生产", "市黄海电器厂生产", "市黄海电器厂生产日光灯具"),
    (LOW_ALL, "变压器广等20余个", "变压器厂等20余个", "变压器厂等科研机构"),
    (LOW_ALL, "农机修造一广试制", "农机修造一厂试制", "灌云县农机修造一厂试制旋耕机"),
    (LOW_ALL, "市变压器广总装车间", "市变压器厂总装车间", "市变压器厂总装车间工程"),
]

OCR_EVIDENCE = [
    ("workbench/ocr/paddle_ocr/中/part01/page_0031.txt", [75, 76]),
    ("workbench/ocr/paddle_ocr/中/part01/page_0084.txt", [41]),
    ("workbench/ocr/paddle_ocr/中/part01/page_0085.txt", [4, 31, 32]),
    ("workbench/ocr/paddle_ocr/中/part01/page_0193.txt", [38, 39]),
    ("workbench/ocr/paddle_ocr/中/part01/page_0196.txt", [38]),
    ("workbench/ocr/paddle_ocr/中/part01/page_0319.txt", [30, 31]),
    ("workbench/ocr/paddle_ocr/中/part01/page_0413.txt", [18, 19]),
    ("workbench/ocr/paddle_ocr/下/part01/page_0428.txt", [7]),
    ("workbench/ocr/paddle_ocr/下/part01/page_0436.txt", [8]),
    ("workbench/ocr/paddle_ocr/下/part01/page_0447.txt", [40]),
    ("workbench/ocr/paddle_ocr/下/part01/page_0448.txt", [4]),
]

RESIDUES = [
    "海州古楼街综合广",
    "灌云县酒广",
    "灌云县镜花缘酒广",
    "市洪门果酒广",
    "土城、朱堵农具广",
    "连云港市变压器广试制",
    "连云港市变压器</p><p>广试制",
    "上海电梯广生产",
    "上海电</p><p>梯广生产",
    "市黄海电器广",
    "变压器广等20余个",
    "农机修造一广试制",
    "市变压器广总装车间",
]
CHECKS = [MID1, LOW1, FULL_SRC, MID_READER, LOW_READER, FULL_READER]


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
        "# 厂名形近残留补修 batch398",
        "",
        f"- 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "- 范围：现行中册/下册正文源稿、全书正文汇总、当前中册/下册/全书 reader。",
        "- 修复：综合厂、酒厂、果酒厂、农具厂、变压器厂、电梯厂、电器厂等可由页级 PaddleOCR 证实的 `广 -> 厂` 形近残留。",
        "- 保留：未逐页证实的其它 `广生产/广投资/广试制/广更名` 命中留待后续核对；未处理 OCR 源文件、backup、obsolete、历史交付包。",
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

- 依据中册 PaddleOCR page_0031、0084、0085、0193、0196、0319、0413 与下册 page_0428、0436、0447、0448，补修综合厂、灌云县酒厂、镜花缘酒厂、洪门果酒厂、农具厂、变压器厂、上海电梯厂、黄海电器厂等 `广 -> 厂` 形近残留。
- 修复范围为现行中册/下册正文源稿、全书正文汇总、当前中册/下册/全书 reader；未逐页证实的其它 `广生产/广投资/广试制/广更名` 命中保留待核。
- 未处理 OCR 源文件、backup、obsolete、历史交付包；未打开、展示或嵌入图片。
- 报告：`output/reports/verified_factory_residues_batch398_20260708.md`；进度：`output/reports/progress/20260708_厂名形近残留补修第三百九十八批.md`。
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
