# -*- coding: utf-8 -*-
"""Repair next OCR-backed factory 广/厂 residues for batch 403."""

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

REPORT = ROOT / "output" / "reports" / "verified_factory_residues_batch403_20260708.md"
REPORT_JSON = ROOT / "output" / "reports" / "verified_factory_residues_batch403_20260708.json"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260708_厂名形近残留补修第四百零三批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"
MARKER = "## 2026-07-08 厂名形近残留补修第四百零三批"

REPLACEMENTS: list[tuple[list[Path], str, str, str]] = [
    ([LOWER1, FULL_SRC, LOWER_READER, FULL_READER], "造纸广、篓业生产厂", "造纸厂、篓业生产厂", "下册源稿/reader：社会福利企业造纸厂"),
    ([MID1, FULL_SRC, MID_READER], "涂料生产工广有8家", "涂料生产工厂有8家", "中册源稿/reader：涂料生产工厂"),
    ([MID2, FULL_SRC], "新建了-批广房", "新建了一批厂房", "中册源稿同步：新建了一批厂房"),
    ([MID1, FULL_SRC], "工广变成一片废", "工厂变成一片废", "中册源稿同步：鞭炮厂爆炸后工厂废墟"),
    ([MID1, FULL_SRC, MID_READER], "韩庄电厂广，", "韩庄电厂，", "中册源稿/reader：韩庄电厂后多余广"),
    ([MID2, FULL_SRC], "市锦屏化工广与湖北", "市锦屏化工厂与湖北", "中册源稿同步：锦屏化工厂与湖北联营"),
    ([LOWER2, FULL_SRC, LOWER_READER], "东北第一第二橡胶广广长", "东北第一第二橡胶厂厂长", "下册源稿/reader：东北第一第二橡胶厂厂长"),
    ([LOWER2, FULL_SRC, LOWER_READER], "山东橡胶总厂广长", "山东橡胶总厂厂长", "下册源稿/reader：山东橡胶总厂厂长"),
    ([LOWER2, FULL_SRC], "街头、工广、街道", "街头、工厂、街道", "下册源稿同步：街头、工厂、街道黑板报"),
    ([MID1, FULL_SRC], "新广址生产", "新厂址生产", "中册源稿同步：无线电专用设备厂新厂址"),
    ([MID1, FULL_SRC], "市化工广（原新浦农药厂）", "市化工厂（原新浦农药厂）", "中册源稿同步：市化工厂氯碱车间"),
    ([MID1, FULL_SRC], "东辛农场砖瓦\n广、", "东辛农场砖瓦\n厂、", "中册源稿同步：东辛农场砖瓦厂"),
    ([MID1, FULL_SRC, MID_READER], "东海县砖瓦厂广", "东海县砖瓦厂", "中册源稿/reader：东海县砖瓦厂"),
    ([MID1, FULL_SRC], "灌云龙\n苴砖广", "灌云龙\n苴砖厂", "中册源稿同步：灌云龙苴砖厂"),
    ([MID1, FULL_SRC, MID_READER], "浦南第二砖广", "浦南第二砖厂", "中册源稿/reader：浦南第二砖厂"),
    ([MID1, FULL_SRC, MID_READER], "房山采石厂广", "房山采石厂", "中册源稿/reader：房山采石厂"),
    ([MID1, FULL_SRC], "铁工广相继开业", "铁工厂相继开业", "中册源稿同步：铁工厂相继开业"),
    ([LOWER1, FULL_SRC], "工广或\n作坊", "工厂或\n作坊", "下册源稿同步：监所附设工厂或作坊"),
    ([LOWER1], "市棉织广建立", "市棉织厂建立", "下册源稿同步：市棉织厂建立职代会"),
    ([MID1, FULL_SRC], "日用化工广", "日用化工厂", "中册源稿同步：横沟乡日用化工厂"),
    ([MID1, FULL_SRC], "电广经常低压", "电厂经常低压", "中册源稿同步：电厂低压低周运行"),
    ([UPPER10, UPPER_SUMMARY, FULL_SRC], "并入新浦造纸广", "并入新浦造纸厂", "上册源稿同步：华伦造纸厂并入新浦造纸厂"),
]

OCR_EVIDENCE = [
    ("workbench/ocr/paddle_ocr/下/part01/page_0040.txt", [18]),
    ("workbench/ocr/paddle_ocr/中/part01/page_0291.txt", [25]),
    ("workbench/ocr/paddle_ocr/中/part02/page_0294.txt", [25]),
    ("workbench/ocr/paddle_ocr/中/part01/page_0049.txt", [117]),
    ("workbench/ocr/paddle_ocr/中/part01/page_0333.txt", [10, 34]),
    ("workbench/ocr/paddle_ocr/中/part02/page_0371.txt", [23]),
    ("workbench/ocr/paddle_ocr/下/part02/page_0369.txt", [28]),
    ("workbench/ocr/paddle_ocr/下/part02/page_0050.txt", [23]),
    ("workbench/ocr/paddle_ocr/中/part01/page_0263.txt", [32]),
    ("workbench/ocr/paddle_ocr/中/part01/page_0154.txt", [36]),
    ("workbench/ocr/paddle_ocr/中/part01/page_0271.txt", [29, 30]),
    ("workbench/ocr/paddle_ocr/中/part01/page_0399.txt", [26]),
    ("workbench/ocr/paddle_ocr/中/part01/page_0276.txt", [18, 19]),
    ("workbench/ocr/paddle_ocr/中/part01/page_0192.txt", [14]),
    ("workbench/ocr/paddle_ocr/下/part01/page_0151.txt", [6]),
    ("workbench/ocr/paddle_ocr/下/part01/page_0314.txt", [5]),
    ("workbench/ocr/paddle_ocr/中/part01/page_0403.txt", [28]),
    ("workbench/ocr/paddle_ocr/上/part03/page_0173.txt", [14]),
]

RESIDUES = [
    "造纸广、篓业生产厂",
    "涂料生产工广有8家",
    "新建了-批广房",
    "工广变成一片废",
    "韩庄电厂广，",
    "市锦屏化工广与湖北",
    "东北第一第二橡胶广广长",
    "山东橡胶总厂广长",
    "街头、工广、街道",
    "新广址生产",
    "市化工广（原新浦农药厂）",
    "东辛农场砖瓦\n广、",
    "东海县砖瓦厂广",
    "灌云龙\n苴砖广",
    "浦南第二砖广",
    "房山采石厂广",
    "铁工广相继开业",
    "工广或\n作坊",
    "市棉织广建立",
    "日用化工广",
    "电广经常低压",
    "并入新浦造纸广",
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
        "# 厂名形近残留补修 batch403",
        "",
        f"- 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "- 范围：现行上册/中册/下册正文源稿、上册正文汇总、全书正文汇总，以及当前中册/下册/全书 reader 中仍残留的同源坏形态。",
        "- 修复：依据页级 PaddleOCR 证据，补修工厂、厂房、厂址、化工厂、造纸厂、砖瓦厂、采石厂、橡胶厂厂长等 `广 -> 厂` 形近残留；`韩庄电厂广，` 按 OCR 修为 `韩庄电厂，`。",
        "- 保留：未逐页闭环的 `采右广`、合法 `两广提督`、`增广生员`、`广告` 等不处理；backup、obsolete、历史交付包和 OCR 源文件不处理。",
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

- 依据中册 PaddleOCR page_0049、0154、0192、0263、0271、0276、0291、0333、0399、0403、part02 page_0294、0371，上册 page_0173，下册 page_0040、0050、0151、0314、0369，补修工厂、厂房、厂址、化工厂、造纸厂、砖瓦厂、采石厂、橡胶厂厂长等 `广 -> 厂` 形近残留。
- `韩庄电厂广，` 按 OCR 原文修为 `韩庄电厂，`，未误补成“电厂厂”；未逐页闭环的 `采右广` 继续保留待核。
- 修复范围为现行上册/中册/下册正文源稿、上册正文汇总、全书正文汇总，以及当前中册/下册/全书 reader 中仍残留的同源坏形态；未处理 OCR 源文件、backup、obsolete、历史交付包；未打开、展示或嵌入图片。
- 报告：`output/reports/verified_factory_residues_batch403_20260708.md`；进度：`output/reports/progress/20260708_厂名形近残留补修第四百零三批.md`。
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
