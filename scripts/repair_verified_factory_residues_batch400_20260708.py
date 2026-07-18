# -*- coding: utf-8 -*-
"""Repair final OCR-backed 广/厂 residue tail for batch 400."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

UPPER3 = ROOT / "workbench" / "body_chapters" / "上" / "第三卷_区县概况.md"
UPPER2 = ROOT / "workbench" / "body_chapters" / "上" / "第四卷至第十卷（part02）.md"
UPPER10 = ROOT / "workbench" / "body_chapters" / "上" / "第十卷至第十六卷（part03）.md"
UPPER_SUMMARY = ROOT / "workbench" / "body_chapters" / "连云港市志_上册_正文汇总.md"
MID1 = ROOT / "workbench" / "body_chapters" / "第十七卷至第二十九卷（中part01）.md"
FULL_SRC = ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md"
MID_READER = ROOT / "output" / "final_reader" / "连云港市志_中册.html"
FULL_READER = ROOT / "output" / "final_reader" / "连云港市志_全书.html"

REPORT = ROOT / "output" / "reports" / "verified_factory_residues_batch400_20260708.md"
REPORT_JSON = ROOT / "output" / "reports" / "verified_factory_residues_batch400_20260708.json"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260708_厂名形近残留补修第四百批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"
MARKER = "## 2026-07-08 厂名形近残留补修第四百批"

REPLACEMENTS: list[tuple[list[Path], str, str, str]] = [
    ([UPPER2, UPPER_SUMMARY, FULL_SRC], "市化肥广生产", "市化肥厂生产", "上册源稿同步：市化肥厂生产水煤气"),
    ([UPPER3, UPPER_SUMMARY, FULL_SRC], "临洪粉丝广建成", "临洪粉丝厂建成", "上册源稿同步：临洪粉丝厂建成"),
    ([UPPER10, UPPER_SUMMARY, FULL_SRC], "五七造纸广投资", "五七造纸厂投资", "上册源稿同步：五七造纸厂投资技改"),
    ([UPPER10, UPPER_SUMMARY, FULL_SRC], "市塑料四广投资", "市塑料四厂投资", "上册源稿同步：市塑料四厂投资席梦思线"),
    ([UPPER10, UPPER_SUMMARY, FULL_SRC], "新浦分店印刷广更名", "新浦分店印刷厂更名", "上册源稿同步：新浦分店印刷厂更名"),
    ([MID1, FULL_SRC], "贝雕广生产", "贝雕厂生产", "中册源稿同步：市贝雕厂生产贝雕画"),
    ([MID1, FULL_SRC], "海州电器广开始", "海州电器厂开始", "中册源稿同步：海州电器厂开始生产启动器"),
    ([MID1, FULL_SRC], "灌云县工艺\n美术品广", "灌云县工艺\n美术品厂", "中册源稿/全书汇总：灌云县工艺美术品厂更名"),
    ([MID_READER], "灌云县工艺</p><p>美术品广", "灌云县工艺</p><p>美术品厂", "reader分段：灌云县工艺美术品厂更名"),
    ([FULL_READER], "灌云县工艺美术品广", "灌云县工艺美术品厂", "reader连续文本：灌云县工艺美术品厂更名"),
    ([MID1, FULL_SRC, MID_READER], "东海县黄川酿酒广", "东海县黄川酿酒厂", "中册表格/reader：东海县黄川酿酒厂"),
]

OCR_EVIDENCE = [
    ("workbench/ocr/paddle_ocr/上/part01/page_0235.txt", [12]),
    ("workbench/ocr/paddle_ocr/上/part02/page_0073.txt", [32]),
    ("workbench/ocr/paddle_ocr/上/part03/page_0178.txt", [11]),
    ("workbench/ocr/paddle_ocr/上/part03/page_0182.txt", [38]),
    ("workbench/ocr/paddle_ocr/上/part03/page_0214.txt", [15]),
    ("workbench/ocr/paddle_ocr/中/part01/page_0024.txt", [29, 30]),
    ("workbench/ocr/paddle_ocr/中/part01/page_0032.txt", [21, 22]),
    ("workbench/ocr/paddle_ocr/中/part01/page_0096.txt", [147]),
    ("workbench/ocr/paddle_ocr/中/part01/page_0219.txt", [6]),
]

RESIDUES = [
    "市化肥广生产",
    "临洪粉丝广建成",
    "五七造纸广投资",
    "市塑料四广投资",
    "新浦分店印刷广更名",
    "贝雕广生产",
    "海州电器广开始",
    "灌云县工艺\n美术品广",
    "灌云县工艺</p><p>美术品广",
    "灌云县工艺美术品广",
    "东海县黄川酿酒广",
]
CHECKS = [UPPER3, UPPER2, UPPER10, UPPER_SUMMARY, MID1, FULL_SRC, MID_READER, FULL_READER]


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
        "# 厂名形近残留补修 batch400",
        "",
        f"- 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "- 范围：现行上册/中册正文源稿、上册正文汇总、全书正文汇总、当前中册/全书 reader。",
        "- 修复：市化肥厂、临洪粉丝厂、五七造纸厂、市塑料四厂、新浦分店印刷厂、市贝雕厂、海州电器厂、灌云县工艺美术品厂、东海县黄川酿酒厂等可由页级 PaddleOCR 证实的 `广 -> 厂` 形近残留。",
        "- 保留：backup、obsolete、历史交付包不处理；未处理 OCR 源文件。",
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

- 依据上册 PaddleOCR page_0235、0073、0178、0182、0214 与中册 page_0024、0032、0096、0219，补修市化肥厂、临洪粉丝厂、五七造纸厂、市塑料四厂、新浦分店印刷厂、市贝雕厂、海州电器厂、灌云县工艺美术品厂、东海县黄川酿酒厂等 `广 -> 厂` 形近残留。
- 修复范围为现行上册/中册正文源稿、上册正文汇总、全书正文汇总、当前中册/全书 reader；backup、obsolete、历史交付包不处理。
- 未处理 OCR 源文件；未打开、展示或嵌入图片。
- 报告：`output/reports/verified_factory_residues_batch400_20260708.md`；进度：`output/reports/progress/20260708_厂名形近残留补修第四百批.md`。
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
