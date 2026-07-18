# -*- coding: utf-8 -*-
"""Repair OCR-backed factory 广/厂 residues for batch 405."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

UPPER10 = ROOT / "workbench" / "body_chapters" / "上" / "第十卷至第十六卷（part03）.md"
UPPER_SUMMARY = ROOT / "workbench" / "body_chapters" / "连云港市志_上册_正文汇总.md"
MID1 = ROOT / "workbench" / "body_chapters" / "第十七卷至第二十九卷（中part01）.md"
MID2 = ROOT / "workbench" / "body_chapters" / "第三十卷至第四十二卷（中part02）.md"
LOWER1 = ROOT / "workbench" / "body_chapters" / "第四十三卷至第五十一卷（下part01）.md"
LOWER2 = ROOT / "workbench" / "body_chapters" / "第五十二卷至第六十卷及附录（下part02）.md"
FULL_SRC = ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md"
MID_READER = ROOT / "output" / "final_reader" / "连云港市志_中册.html"
LOWER_READER = ROOT / "output" / "final_reader" / "连云港市志_下册.html"
FULL_READER = ROOT / "output" / "final_reader" / "连云港市志_全书.html"

REPORT = ROOT / "output" / "reports" / "verified_factory_residues_batch405_20260708.md"
REPORT_JSON = ROOT / "output" / "reports" / "verified_factory_residues_batch405_20260708.json"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260708_厂名形近残留补修第四百零五批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"
MARKER = "## 2026-07-08 厂名形近残留补修第四百零五批"

REPLACEMENTS: list[tuple[list[Path], str, str, str]] = [
    ([MID1, FULL_SRC], "鱼品加工广后", "鱼品加工厂后", "中册源稿同步：鱼品加工厂后"),
    (
        [MID1, FULL_SRC],
        "圆弧板，供大型建筑物的圆柱装饰。\n加工广，生产各种大理石、花岗石及其它石材制品。",
        "圆弧板，供大型建筑物的圆柱装饰。\n1989年，连云港市经济技术开发区石材公司与黑龙江铁力林业局联营兴办龙云石材\n加工厂，生产各种大理石、花岗石及其它石材制品。",
        "中册源稿同步：龙云石材加工厂句首缺漏",
    ),
    (
        [MID_READER],
        "圆弧板，供大型建筑物的圆柱装饰。</p><p>加工广，生产各种大理石、花岗石及其它石材制品。",
        "圆弧板，供大型建筑物的圆柱装饰。</p><p>1989年，连云港市经济技术开发区石材公司与黑龙江铁力林业局联营兴办龙云石材</p><p>加工厂，生产各种大理石、花岗石及其它石材制品。",
        "中册 reader：龙云石材加工厂句首缺漏",
    ),
    ([MID1, FULL_SRC], "组\n：长单位，广长陶文新", "组\n长单位，厂长陶文新", "中册源稿同步：厂长陶文新"),
    ([MID_READER], "组</p><p>：长单位，广长陶文新", "组</p><p>长单位，厂长陶文新", "中册 reader：厂长陶文新"),
    ([MID_READER], "新海电广为充分利用", "新海电厂为充分利用", "中册 reader：新海电厂"),
    ([MID1, FULL_SRC, MID_READER], "器械广", "器械厂", "中册源稿/reader：连云港医疗器械厂"),
    ([MID2, FULL_SRC, MID_READER], "东风制药广", "东风制药厂", "中册源稿/reader：国营东风制药厂"),
    ([MID1, FULL_SRC, MID_READER, FULL_READER], "食品广东海联营", "食品厂东海联营", "中册源稿/reader：食品厂东海联营厂"),
    (
        [MID1, FULL_SRC],
        "1987年3月开工，1989年11月工的灌云棉纺织厂广房位于",
        "1987年3月开工，1989年11月竣工的灌云棉纺织厂厂房位于",
        "中册源稿同步：灌云棉纺织厂厂房",
    ),
    ([LOWER1, FULL_SRC, LOWER_READER, FULL_READER], "制药广新产品", "制药厂新产品", "下册源稿/reader：制药厂新产品研究所"),
    ([LOWER2, FULL_SRC], "工广、医院", "工厂、医院", "下册源稿同步：雕塑屹立在工厂、医院"),
    ([MID1, LOWER2, FULL_SRC, MID_READER], "广长（经理）", "厂长（经理）", "中/下源稿及中册 reader：厂长（经理）负责制"),
    ([UPPER10, UPPER_SUMMARY, FULL_SRC], "市造纸广基础", "市造纸厂基础", "上册源稿同步：市造纸厂基础"),
    ([UPPER10, UPPER_SUMMARY, FULL_SRC], "维尼纶\n广开始", "维尼纶\n厂开始", "上册源稿同步：市维尼纶厂开始筹建"),
    ([UPPER10, UPPER_SUMMARY, FULL_SRC], "麻纺织广", "麻纺织厂", "上册源稿同步：市麻纺织厂"),
]

OCR_EVIDENCE = [
    ("workbench/ocr/paddle_ocr/中/part01/page_0078.txt", [38]),
    ("workbench/ocr/paddle_ocr/中/part01/page_0290.txt", [23, 24, 25]),
    ("workbench/ocr/paddle_ocr/中/part01/page_0168.txt", [11, 12]),
    ("workbench/ocr/paddle_ocr/中/part01/page_0273.txt", [5]),
    ("workbench/ocr/paddle_ocr/中/part01/page_0129.txt", [19, 20, 21]),
    ("workbench/ocr/paddle_ocr/中/part02/page_0366.txt", [14, 15]),
    ("workbench/ocr/paddle_ocr/中/part01/page_0066.txt", [5, 6]),
    ("workbench/ocr/paddle_ocr/中/part01/page_0303.txt", [33, 34]),
    ("workbench/ocr/paddle_ocr/下/part01/page_0418.txt", [36, 37]),
    ("workbench/ocr/paddle_ocr/下/part02/page_0023.txt", [16, 17]),
    ("workbench/ocr/paddle_ocr/下/part02/page_0423.txt", [32, 33]),
    ("workbench/ocr/paddle_ocr/中/part01/page_0409.txt", [10]),
    ("workbench/ocr/paddle_ocr/上/part03/page_0176.txt", [25]),
    ("workbench/ocr/paddle_ocr/上/part03/page_0227.txt", [19, 20, 21]),
]

RESIDUES = [
    "鱼品加工广",
    "加工广，生产各种大理石",
    "广长陶文新",
    "新海电广",
    "器械广",
    "东风制药广",
    "食品广东海联营",
    "棉纺织厂广房",
    "制药广新产品",
    "工广、医院",
    "广长（经理）",
    "市造纸广基础",
    "维尼纶\n广开始",
    "维尼纶</p><p>广开始",
    "麻纺织广",
]
CHECKS = [UPPER10, UPPER_SUMMARY, MID1, MID2, LOWER1, LOWER2, FULL_SRC, MID_READER, LOWER_READER, FULL_READER]


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
        "# 厂名形近残留补修 batch405",
        "",
        f"- 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "- 范围：现行上册/中册/下册正文源稿、上册正文汇总、全书正文汇总，以及当前中册/下册/全书 reader 中仍残留的同源坏形态。",
        "- 修复：依据页级 PaddleOCR 证据，补修鱼品加工厂、龙云石材加工厂、厂长陶文新、新海电厂、医疗器械厂、东风制药厂、食品厂东海联营厂、灌云棉纺织厂厂房、制药厂新产品研究所、工厂医院场所、厂长（经理）负责制、市造纸厂、市维尼纶厂、市麻纺织厂等 `广 -> 厂` 残留。",
        "- 保留：正常词 `广泛`、`广播`、`推广`、`广场`、`广告` 等不处理；OCR 源文件、backup、obsolete、历史交付包不处理。",
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

- 依据中册 PaddleOCR `page_0066.txt`、`page_0078.txt`、`page_0129.txt`、`page_0168.txt`、`page_0273.txt`、`page_0290.txt`、`page_0303.txt`、`part02/page_0366.txt`，下册 `part01/page_0418.txt`、`part02/page_0023.txt`、`part02/page_0423.txt`，上册 `part03/page_0176.txt`、`part03/page_0227.txt`，补修鱼品加工厂、龙云石材加工厂、厂长陶文新、新海电厂、医疗器械厂、东风制药厂、食品厂东海联营厂、灌云棉纺织厂厂房、制药厂新产品研究所、工厂/医院场所、厂长（经理）负责制、市造纸厂、市维尼纶厂、市麻纺织厂等残留。
- 修复范围为现行上册/中册/下册正文源稿、上册正文汇总、全书正文汇总，以及当前中册/下册/全书 reader 中同源坏形态；未处理 OCR 源文件、backup、obsolete、历史交付包；未打开、展示或嵌入图片。
- 正常词 `广泛`、`广播`、`推广`、`广场`、`广告` 等继续保留。
- 报告：`output/reports/verified_factory_residues_batch405_20260708.md`；进度：`output/reports/progress/20260708_厂名形近残留补修第四百零五批.md`。
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
