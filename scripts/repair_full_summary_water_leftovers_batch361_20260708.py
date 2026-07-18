# -*- coding: utf-8 -*-
"""Repair remaining source-backed water-summary leftovers."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "output" / "reports" / "full_summary_water_leftovers_batch361_20260708.md"
REPORT_JSON = ROOT / "output" / "reports" / "full_summary_water_leftovers_batch361_20260708.json"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260708_全书汇总水利剩余可证残留补修第三百六十一批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"
MARKER = "## 2026-07-08 全书汇总水利剩余可证残留补修第三百六十一批"

TARGETS = [
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
    ROOT / "workbench" / "body_chapters" / "连云港市志_上册_正文汇总.md",
]

REPLACEMENTS = [
    ("新述河大官庄闸全开", "新沭河大官庄闸全开", "上/part02/page_0274.txt 明确为“新沭河大官庄闸全开”。"),
    ("民国时期又进行沂述尾间工程", "民国时期又进行沂沭尾间工程", "上/part02/page_0267.txt 与 page_0289.txt 明确为“沂沭尾间工程”。"),
    ("开辟新沐河、新沂河", "开辟新沭河、新沂河", "上/part02/page_0290.txt 明确为“开辟新沭河、新沂河”。"),
    ("解决沂述河洪水危害", "解决沂沭河洪水危害", "上/part02/page_0290.txt 对应解除沂沭洪水危害语境。"),
    ("实施沂述尾闻工程", "实施沂沭尾间工程", "上/part02/page_0289.txt 明确为“实施沂沭尾间工程”。"),
    ("在新述河扩大", "在新沭河扩大", "上/part02/page_0294、0297.txt 均明确为“在新沭河扩大”。"),
    ("沐北运河", "沭北运河", "上/part02/page_0298.txt 明确为“沭北运河”。"),
    ("沐北闸", "沭北闸", "上/part02/page_0298.txt 明确为“沭北闸”。"),
    ("太平庄闸位于东海县太平庄西北1公里新沐河上", "太平庄闸位于东海县太平庄西北1公里新沭河上", "上/part02/page_0303.txt 明确为“新沭河上”。"),
    ("赣榆县因新沐河扩大", "赣榆县因新沭河扩大", "上/part03/page_0044.txt 与水利同段均为“新沭河扩大”。"),
    ("新沐河堤防管理所", "新沭河堤防管理所", "上/part03/page_0060.txt、前后水利语境均为新沭河堤防。"),
    ("沂述泗管理局", "沂沭泗管理局", "上/part02/page_0274.txt 明确为沂沭泗流域语境。"),
]

CHECK_TERMS = ["新述河", "新沐河", "述南", "述北", "沐南", "沐北", "临沐县", "沂述", "沂沐"]


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
        "# 全书汇总水利剩余可证残留补修 batch361",
        "",
        f"- 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"- 修复总数：{total}",
        "- 范围：全书正文汇总、上册正文汇总中的水利剩余可证短语。",
        "- 依据：上册 part02 page_0274、0289、0290、0294、0297、0298、0303 及相关水利页级证据。",
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
    lines.extend(["", "## 保留边界", "", "- 人物、供销、港口、财政和题名/书名残留未在本批处理。", "- 未处理 OCR 源文件、backup、obsolete、历史交付包。"])
    return "\n".join(lines) + "\n"


def upsert_memory(total: int, residuals: dict[str, int]) -> None:
    block = f"""{MARKER}

- 依据上册 part02 page_0274、0289、0290、0294、0297、0298、0303 及相关水利页级证据，补修全书正文汇总/上册正文汇总水利剩余可证短语，共 {total} 处。
- 代表修复：`新述河大官庄闸全开 -> 新沭河大官庄闸全开`、`沂述尾间工程 -> 沂沭尾间工程`、`开辟新沐河、新沂河 -> 开辟新沭河、新沂河`、`沐北运河/沐北闸 -> 沭北运河/沭北闸`、`新沐河堤防管理所 -> 新沭河堤防管理所`。
- 本批后检查范围：`新述河` {residuals['新述河']}，`新沐河` {residuals['新沐河']}，`述南` {residuals['述南']}，`述北` {residuals['述北']}，`沐南` {residuals['沐南']}，`沐北` {residuals['沐北']}，`临沐县` {residuals['临沐县']}，`沂述` {residuals['沂述']}，`沂沐` {residuals['沂沐']}。
- 人物、供销、港口、财政和题名/书名残留未在本批处理；未作 `述 -> 沭`、`沐 -> 沭`、`人 -> 入` 全局替换；未处理 OCR 源文件、backup、obsolete、历史交付包；未打开、展示或嵌入图片。
- 报告：`output/reports/full_summary_water_leftovers_batch361_20260708.md`；进度：`output/reports/progress/20260708_全书汇总水利剩余可证残留补修第三百六十一批.md`。
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
