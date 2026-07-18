# -*- coding: utf-8 -*-
"""Repair OCR-backed factory 广/厂 residues for batch 402."""

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
LOWER1 = ROOT / "workbench" / "body_chapters" / "第四十三卷至第五十一卷（下part01）.md"
LOWER2 = ROOT / "workbench" / "body_chapters" / "第五十二卷至第六十卷及附录（下part02）.md"
FULL_SRC = ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md"
MID_READER = ROOT / "output" / "final_reader" / "连云港市志_中册.html"
LOWER_READER = ROOT / "output" / "final_reader" / "连云港市志_下册.html"
FULL_READER = ROOT / "output" / "final_reader" / "连云港市志_全书.html"

REPORT = ROOT / "output" / "reports" / "verified_factory_residues_batch402_20260708.md"
REPORT_JSON = ROOT / "output" / "reports" / "verified_factory_residues_batch402_20260708.json"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260708_厂名形近残留补修第四百零二批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"
MARKER = "## 2026-07-08 厂名形近残留补修第四百零二批"

REPLACEMENTS: list[tuple[list[Path], str, str, str]] = [
    ([UPPER3, UPPER_SUMMARY, FULL_SRC], "学校、工广逐步普及", "学校、工厂逐步普及", "上册源稿同步：体育活动由学校、工厂逐步普及"),
    ([UPPER2, UPPER_SUMMARY, FULL_SRC], "第九七三四工广草浆", "第九七三四工厂草浆", "上册源稿同步：第九七三四工厂草浆黑液回收"),
    ([UPPER2, UPPER_SUMMARY, FULL_SRC], "工广进行治理效果", "工厂进行治理效果", "上册源稿同步：环保治理设施工厂监测"),
    ([UPPER2, UPPER_SUMMARY, FULL_SRC], "市台南化工广", "市台南化工厂", "上册源稿同步：市台南化工厂"),
    ([UPPER10, UPPER_SUMMARY, FULL_SRC], "饲料加工广90个", "饲料加工厂90个", "上册源稿同步：饲料加工厂90个"),
    ([UPPER10, UPPER_SUMMARY, FULL_SRC], "黄海化工广开始生产", "黄海化工厂开始生产", "上册源稿同步：黄海化工厂粉洗盐"),
    ([UPPER10, UPPER_SUMMARY, FULL_SRC], "新浦造纸广因", "新浦造纸厂因", "上册源稿同步：新浦造纸厂因蒸煮楼停产"),
    ([UPPER10, UPPER_SUMMARY, FULL_SRC], "市造纸广视察", "市造纸厂视察", "上册源稿同步：到市造纸厂视察"),
    ([UPPER10, UPPER_SUMMARY, FULL_SRC], "东海县木工广", "东海县木工厂", "上册源稿同步：东海县木工厂"),
    ([UPPER10, UPPER_SUMMARY, FULL_SRC], "新广占地6.6", "新厂占地6.6", "上册源稿同步：市毛巾厂新厂占地"),
    ([UPPER10, UPPER_SUMMARY, FULL_SRC], "市鞋帽广购进", "市鞋帽厂购进", "上册源稿同步：市鞋帽厂购进注塑机"),
    ([UPPER10, UPPER_SUMMARY, FULL_SRC], "新浦化工广", "新浦化工厂", "上册源稿同步：新浦化工厂塑料管材"),
    ([UPPER10, UPPER_SUMMARY, FULL_SRC], "玻璃二厂广房", "玻璃二厂厂房", "上册源稿同步：玻璃二厂厂房"),
    ([MID1, FULL_SRC], "市红旗化工广应", "市红旗化工厂应", "中册源稿同步：市红旗化工厂饲料级磷酸氢钙"),
    ([MID1, FULL_SRC], "市红旗化工广引进", "市红旗化工厂引进", "中册源稿同步：市红旗化工厂引进菌种"),
    ([MID1, FULL_SRC], "市锦屏化工广成功", "市锦屏化工厂成功", "中册源稿同步：市锦屏化工厂食品级磷酸"),
    ([MID1, FULL_SRC, MID_READER], "上海皮革化工广", "上海皮革化工厂", "中册源稿/reader：上海皮革化工厂"),
    ([MID1, FULL_SRC], "南京无线电广", "南京无线电厂", "中册源稿同步：南京无线电厂转让"),
    ([MID1, FULL_SRC, MID_READER, FULL_READER], "青岛食品广石桥联营厂", "青岛食品厂石桥联营厂", "中册源稿/reader：青岛食品厂石桥联营厂"),
    ([LOWER1, FULL_SRC, LOWER_READER, FULL_READER], "市造纸广讲授", "市造纸厂讲授", "下册源稿/reader：华罗庚到市造纸厂讲授"),
    ([LOWER2, FULL_SRC], "华兴铁工广", "华兴铁工厂", "下册源稿同步：华兴铁工厂副经理"),
    ([LOWER2, FULL_SRC], "工广女工", "工厂女工", "下册源稿同步：查治对象为工厂女工"),
    ([LOWER2, FULL_SRC], "新海印\n刷广", "新海印\n刷厂", "下册源稿同步：新海印刷厂跨行"),
    ([LOWER_READER], "新海印</p><p>刷广", "新海印</p><p>刷厂", "下册reader：新海印刷厂跨段"),
    ([LOWER2, FULL_SRC, LOWER_READER], "两广共检查", "两厂共检查", "下册源稿/reader：两厂共检查"),
]

OCR_EVIDENCE = [
    ("workbench/ocr/paddle_ocr/上/part01/page_0262.txt", [17]),
    ("workbench/ocr/paddle_ocr/上/part02/page_0106.txt", [25]),
    ("workbench/ocr/paddle_ocr/上/part02/page_0120.txt", [23]),
    ("workbench/ocr/paddle_ocr/上/part02/page_0181.txt", [63]),
    ("workbench/ocr/paddle_ocr/上/part03/page_0081.txt", [28]),
    ("workbench/ocr/paddle_ocr/上/part03/page_0148.txt", [18]),
    ("workbench/ocr/paddle_ocr/上/part03/page_0173.txt", [17]),
    ("workbench/ocr/paddle_ocr/上/part03/page_0175.txt", [24]),
    ("workbench/ocr/paddle_ocr/上/part03/page_0217.txt", [7]),
    ("workbench/ocr/paddle_ocr/上/part03/page_0249.txt", [8]),
    ("workbench/ocr/paddle_ocr/上/part03/page_0284.txt", [10]),
    ("workbench/ocr/paddle_ocr/上/part03/page_0285.txt", [31]),
    ("workbench/ocr/paddle_ocr/上/part03/page_0220.txt", [4]),
    ("workbench/ocr/paddle_ocr/中/part01/page_0176.txt", [10, 23]),
    ("workbench/ocr/paddle_ocr/中/part01/page_0177.txt", [22]),
    ("workbench/ocr/paddle_ocr/中/part01/page_0181.txt", [34]),
    ("workbench/ocr/paddle_ocr/中/part01/page_0238.txt", [27]),
    ("workbench/ocr/paddle_ocr/中/part01/page_0417.txt", [11]),
    ("workbench/ocr/paddle_ocr/下/part01/page_0447.txt", [8]),
    ("workbench/ocr/paddle_ocr/下/part02/page_0370.txt", [5]),
    ("workbench/ocr/paddle_ocr/下/part02/page_0202.txt", [15, 16, 17]),
]

RESIDUES = [
    "学校、工广逐步普及",
    "第九七三四工广草浆",
    "工广进行治理效果",
    "市台南化工广",
    "饲料加工广90个",
    "黄海化工广开始生产",
    "新浦造纸广因",
    "市造纸广视察",
    "市造纸广讲授",
    "东海县木工广",
    "新广占地6.6",
    "市鞋帽广购进",
    "新浦化工广",
    "玻璃二厂广房",
    "市红旗化工广应",
    "市红旗化工广引进",
    "市锦屏化工广成功",
    "上海皮革化工广",
    "南京无线电广",
    "青岛食品广石桥联营厂",
    "华兴铁工广",
    "工广女工",
    "新海印\n刷广",
    "新海印</p><p>刷广",
    "两广共检查",
]
CHECKS = [UPPER3, UPPER2, UPPER10, UPPER_SUMMARY, MID1, LOWER1, LOWER2, FULL_SRC, MID_READER, LOWER_READER, FULL_READER]


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
        "# 厂名形近残留补修 batch402",
        "",
        f"- 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "- 范围：现行上册/中册/下册正文源稿、上册正文汇总、全书正文汇总，以及当前中册/下册/全书 reader 中仍残留的同源坏形态。",
        "- 修复：依据页级 PaddleOCR 证据，补修工厂、化工厂、造纸厂、鞋帽厂、食品厂、印刷厂、厂房等 `广 -> 厂` 形近残留。",
        "- 保留：`两广提督`、`增广生员`、`张广生`、`广告` 等合法 `广` 不处理；backup、obsolete、历史交付包和 OCR 源文件不处理。",
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

- 依据上册 PaddleOCR page_0262、0106、0120、0181、0081、0148、0173、0175、0217、0220、0249、0284、0285，中册 page_0176、0177、0181、0238、0417，下册 page_0447、0202、0370，补修工厂、化工厂、造纸厂、鞋帽厂、食品厂、印刷厂、厂房等 `广 -> 厂` 形近残留。
- 修复范围为现行上册/中册/下册正文源稿、上册正文汇总、全书正文汇总，以及当前中册/下册/全书 reader 中仍残留的同源坏形态；合法 `两广提督`、`增广生员`、`张广生`、`广告` 等未处理。
- 未处理 OCR 源文件、backup、obsolete、历史交付包；未作全局 `广 -> 厂` 替换；未打开、展示或嵌入图片。
- 报告：`output/reports/verified_factory_residues_batch402_20260708.md`；进度：`output/reports/progress/20260708_厂名形近残留补修第四百零二批.md`。
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
