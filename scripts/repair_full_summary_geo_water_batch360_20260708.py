# -*- coding: utf-8 -*-
"""Repair source-backed geography and overview water residuals in full summary."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "output" / "reports" / "full_summary_geo_water_batch360_20260708.md"
REPORT_JSON = ROOT / "output" / "reports" / "full_summary_geo_water_batch360_20260708.json"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260708_全书汇总地理县情水利散点补修第三百六十批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"
MARKER = "## 2026-07-08 全书汇总地理县情水利散点补修第三百六十批"

TARGETS = [ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md"]

REPLACEMENTS = [
    ("4月30日新述河工程开工", "4月30日新沭河工程开工", "`workbench/body_chapters/上/总述与大事记.md` 与 `连云港市志_上册_PaddleOCR正文汇总.md` 明确为“4月30日 新沭河工程开工”。"),
    ("山东省临沐县大官庄拦述河", "山东省临沭县大官庄拦沭河", "`workbench/body_chapters/上/总述与大事记.md` 明确为“临沭县大官庄拦沭河”。"),
    ("限制沐水南下", "限制沭水南下", "`workbench/body_chapters/上/总述与大事记.md` 明确为“限制沭水南下”。"),
    ("主要排洪河道新沂河、新述河", "主要排洪河道新沂河、新沭河", "上/part01/page_0124.txt 明确为“新沂河、新沭河”。"),
    ("新沐河、临洪河", "新沭河、临洪河", "上/part01/page_0128.txt 明确为“新沭河、临洪河”。"),
    ("新述河、朱嵇河流域", "新沭河、朱嵇河流域", "上/part01/page_0129.txt 明确为“新沭河、朱嵇河流域”。"),
    ("境内新沂河、新述河、薇河", "境内新沂河、新沭河、蔷薇河", "上/part01/page_0135.txt 明确为“新沂河、新沭河、蔷薇河”。"),
    ("人述北运河水系", "入沭北运河水系", "上/part01/page_0168.txt 朱稽河段对应沭北运河水系语境。"),
    ("新沐河开挖于民国38年", "新沭河开挖于民国38年", "上/part01/page_0168.txt 明确为“新沭河开挖于民国38年”。"),
    ("下游合新述河入临洪河", "下游合新沭河入临洪河", "上/part01/page_0169.txt 明确为“下游合新沭河入临洪河”。"),
    ("沂、述河尾间", "沂、沭河尾间", "上册水涝页同一水系语境，page_0267 明确为“沂沭河下游”。"),
    ("沂述河水患", "沂沭河水患", "上/part02/page_0267.txt、page_0272.txt 明确为“沂沭”。"),
    ("南隔新述河", "南隔新沭河", "上/part01/page_0254.txt 明确为“南隔新沭河”。"),
    ("新述河、述北河", "新沭河、沭北河", "上/part01/page_0255.txt 明确为“新沭河、沭北河”。"),
    ("隔新述河与赣榆县", "隔新沭河与赣榆县", "上/part01/page_0263.txt 明确为“隔新沭河与赣榆县”。"),
    ("沂述河下游", "沂沭河下游", "上/part02/page_0267.txt 明确为“沂沭河下游”。"),
    ("沂涨犯沐，述涨犯沂，沂述下游", "沂涨犯沭，沭涨犯沂，沂沭下游", "上/part02/page_0272.txt 明确为“沂涨犯沭，沭涨犯沂，沂沭下游”。"),
    ("沂述泗流域发生大洪水", "沂沭泗流域发生大洪水", "上/part02/page_0272.txt 明确为“沂沭泗流域发生大洪水”。"),
]

CHECK_TERMS = ["新述河", "新沐河", "述南", "述北", "沐南", "沐北", "临沐县", "沂述", "沂沐", "拦述河", "限制沐水"]


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def apply_fix() -> tuple[list[dict], dict[str, int]]:
    changes: list[dict] = []
    for path in TARGETS:
        if not path.exists():
            continue
        text = read(path)
        updated = text
        for old, new, evidence in REPLACEMENTS:
            count = updated.count(old)
            if count:
                updated = updated.replace(old, new)
                changes.append({"path": rel(path), "old": old, "new": new, "count": count, "evidence": evidence})
        if updated != text:
            path.write_text(updated, encoding="utf-8")
    residuals = {term: sum(read(path).count(term) for path in TARGETS if path.exists()) for term in CHECK_TERMS}
    return changes, residuals


def render(changes: list[dict], residuals: dict[str, int]) -> str:
    total = sum(c["count"] for c in changes)
    lines = [
        "# 全书汇总地理县情水利散点补修 batch360",
        "",
        f"- 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"- 修复总数：{total}",
        "- 范围：全书正文汇总中的大事记、自然地理、河流、县情、防洪概述散点。",
        "- 依据：上册总述与大事记、上册 part01 page_0124、0128、0129、0135、0168、0169、0254、0255、0263，以及上册 part02 page_0267、0272 页级证据。",
        "- 原则：只修完整短语；不作 `述 -> 沭`、`沐 -> 沭`、`人 -> 入` 全局替换。",
        "- 图片处理：未打开、展示或嵌入图片。",
        "",
        "## 替换明细",
    ]
    for item in changes:
        old = item["old"].replace("\n", "\\n")
        new = item["new"].replace("\n", "\\n")
        lines.append(f"- `{item['path']}`：`{old}` -> `{new}`；次数 {item['count']}；依据：{item['evidence']}")
    if not changes:
        lines.append("- 本次未产生新增替换。")
    lines.extend(["", "## 检查结果", ""])
    for term in CHECK_TERMS:
        lines.append(f"- `{term}`：{residuals[term]}")
    lines.extend(["", "## 保留边界", "", "- 港口、财政、人物传记等跨卷散点继续另批核对；未找到页级证据的不处理。", "- 未处理 OCR 源文件、backup、obsolete、历史交付包。"])
    return "\n".join(lines) + "\n"


def upsert_memory(total: int, residuals: dict[str, int]) -> None:
    block = f"""{MARKER}

- 依据上册总述与大事记、上册 part01 page_0124/0128/0129/0135/0168/0169/0254/0255/0263，以及上册 part02 page_0267/0272 页级证据，补修全书正文汇总大事记、自然地理、河流、县情、防洪概述散点，共 {total} 处。
- 代表修复：`4月30日新述河工程开工 -> 4月30日新沭河工程开工`、`主要排洪河道新沂河、新述河 -> 新沂河、新沭河`、`新沐河、临洪河 -> 新沭河、临洪河`、`新述河、述北河 -> 新沭河、沭北河`、`沂涨犯沐，述涨犯沂，沂述下游 -> 沂涨犯沭，沭涨犯沂，沂沭下游`。
- 本批后检查范围：`新述河` {residuals['新述河']}，`新沐河` {residuals['新沐河']}，`述南` {residuals['述南']}，`述北` {residuals['述北']}，`沐南` {residuals['沐南']}，`沐北` {residuals['沐北']}，`临沐县` {residuals['临沐县']}，`沂述` {residuals['沂述']}，`沂沐` {residuals['沂沐']}。
- 港口、财政、人物传记等跨卷散点继续另批核对；未作 `述 -> 沭`、`沐 -> 沭`、`人 -> 入` 全局替换；未处理 OCR 源文件、backup、obsolete、历史交付包；未打开、展示或嵌入图片。
- 报告：`output/reports/full_summary_geo_water_batch360_20260708.md`；进度：`output/reports/progress/20260708_全书汇总地理县情水利散点补修第三百六十批.md`。
"""
    old = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    start = old.find(MARKER)
    if start < 0:
        MEMORY.write_text(old.rstrip() + "\n\n" + block.strip() + "\n", encoding="utf-8")
        return
    next_start = old.find("\n## ", start + 1)
    new = old[:start].rstrip() + "\n\n" + block.strip() + ("\n" if next_start < 0 else old[next_start:])
    MEMORY.write_text(new, encoding="utf-8")


def main() -> None:
    changes, residuals = apply_fix()
    total = sum(c["count"] for c in changes)
    data = {"time": datetime.now().strftime("%Y-%m-%d %H:%M"), "total": total, "changes": changes, "residuals": residuals, "targets": [rel(p) for p in TARGETS]}
    REPORT_JSON.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    report = render(changes, residuals)
    REPORT.write_text(report, encoding="utf-8")
    PROGRESS.write_text(report, encoding="utf-8")
    upsert_memory(total, residuals)
    print(f"total={total}")
    print(residuals)
    print(f"report={REPORT}")


if __name__ == "__main__":
    main()
