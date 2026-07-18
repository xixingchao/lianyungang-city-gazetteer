# -*- coding: utf-8 -*-
"""Repair source-backed water directory, irrigation, transfer, and flood-control residuals."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "output" / "reports" / "full_summary_water_followup_batch359_20260708.md"
REPORT_JSON = ROOT / "output" / "reports" / "full_summary_water_followup_batch359_20260708.json"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260708_水利目录灌区调水防汛残留补修第三百五十九批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"
MARKER = "## 2026-07-08 水利目录灌区调水防汛残留补修第三百五十九批"

TARGETS = [
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
    ROOT / "workbench" / "body_chapters" / "连云港市志_上册_正文汇总.md",
]

REPLACEMENTS = [
    ("新述河治理", "新沭河治理", "上/part02/page_0024.txt 目录和 page_0268.txt 正文均为“新沭河治理”。"),
    ("沐南除涝", "沭南除涝", "上/part02/page_0024.txt 目录和 page_0293.txt 正文均为“沭南除涝”。"),
    ("沐北除涝", "沭北除涝", "上/part02/page_0296.txt 正文为“沭北除涝”。"),
    ("沐北放水涵洞", "沭北放水涵洞", "上/part02/page_0271.txt 明确为“沭北放水涵洞”。"),
    ("沐北通航闸", "沭北通航闸", "上/part02/page_0271.txt 明确为“沭北通航闸”。"),
    ("沐南灌溉涵洞", "沭南灌溉涵洞", "上/part02/page_0271.txt 明确为“沭南灌溉涵洞”。"),
    ("沐南通航闸", "沭南通航闸", "上/part02/page_0271.txt 明确为“沭南通航闸”。"),
    ("分新述\n河沐南和石安河灌区", "分新沭\n河沭南和石安河灌区", "上/part03/page_0030.txt 明确为“分新沭河沭南和石安河灌区”。"),
    ("沐新分干渠", "沭新分干渠", "上/part03/page_0030.txt 明确为“沭新分干渠”。"),
    ("新沐\n河南、沭新河北", "新沭\n河南、沭新河北", "上/part03/page_0030.txt 明确为“新沭河南、沭新河北”。"),
    ("新述河沭南引水涵洞", "新沭河沭南引水涵洞", "上/part03/page_0030.txt 明确为“新沭河沭南引水涵洞”。"),
    ("引新述河水灌溉", "引新沭河水灌溉", "上/part03/page_0031.txt 明确为“引新沭河水灌溉”。"),
    ("沐北总渠", "沭北总渠", "上/part03/page_0031.txt 明确为“沭北总渠”。"),
    ("新述河两岸兴建述南、述北", "新沭河两岸兴建沭南、沭北", "上/part03/page_0043.txt 明确为“新沭河两岸兴建沭南、沭北”。"),
    ("沐北旱田改水田", "沭北旱田改水田", "上/part03/page_0044.txt 明确为“沭北旱田改水田”。"),
    ("新沐河调引江淮水人沐北运", "新沭河调引江淮水入沭北运", "上/part03/page_0057.txt 明确为“调引沭南航道、新沭河江淮水，经沭北运河”。"),
    ("沭北引河自述北通航闸起", "沭北引河自沭北通航闸起", "上/part03/page_0057.txt 明确为“沭北引河自沭北通航闸起”。"),
    ("调引南航道、新沐河江淮水", "调引沭南航道、新沭河江淮水", "上/part03/page_0057.txt 明确为“调引沭南航道、新沭河江淮水”。"),
    ("经述北运河", "经沭北运河", "上/part03/page_0057.txt 明确为“经沭北运河”。"),
    ("述北闸至范口段述北运河", "沭北闸至范口段沭北运河", "上/part03/page_0057.txt 明确为“沭北闸至范口段沭北运河”。"),
    ("述北运河（述北闸至范口）", "沭北运河（沭北闸至范口）", "上/part03/page_0057.txt 明确为“沭北运河(沭北闸至范口)”。"),
    ("沟通沐南、述北航运", "沟通沭南、沭北航运", "上/part03/page_0058.txt 明确为“沟通沭南、沭北航运”。"),
    ("调引江淮水人赣榆县", "调引江淮水入赣榆县", "上/part03/page_0058.txt 明确为“调引江淮水入赣榆县”。"),
    ("辅助述南乌龙河排涝", "辅助沭南乌龙河排涝", "上/part03/page_0058.txt 明确为“辅助沭南乌龙河排涝”。"),
    ("1990年，述南\n通航闸", "1990年，沭南\n通航闸", "上/part03/page_0058.txt 明确为“1990年，沭南通航闸”。"),
    ("述北运河南端", "沭北运河南端", "上/part03/page_0058.txt 明确为“沭北运河南端”。"),
    ("辅助述北地区排涝", "辅助沭北地区排涝", "上/part03/page_0058.txt 明确为“辅助沭北地区排涝”。"),
    ("1990年，述北通\n航闸", "1990年，沭北通\n航闸", "上/part03/page_0058.txt 明确为“1990年，沭北通航闸”。"),
    ("是沐北\n引河", "是沭北\n引河", "上/part03/page_0058.txt 明确为“是沭北引河”。"),
    ("新沐河与石梁河水库", "新沭河与石梁河水库", "上/part03/page_0060.txt 明确为“新沭河与石梁河水库”。"),
    ("新述河行洪低于", "新沭河行洪低于", "上/part03/page_0060.txt 明确为“新沭河行洪低于”。"),
    ("新述河与石梁河水库", "新沭河与石梁河水库", "上/part03/page_0060.txt 明确为“新沭河与石梁河水库”。"),
    ("新述河下游安全行洪", "新沭河下游安全行洪", "上/part03/page_0067.txt 明确为“新沭河下游安全行洪”。"),
    ("沂述河中上游", "沂沭河中上游", "上/part03/page_0067.txt 明确为“沂沭河中上游”。"),
    ("水库以下新述河", "水库以下新沭河", "上/part03/page_0067.txt 明确为“水库以下新沭河”。"),
    ("因新述河泄洪", "因新沭河泄洪", "上/part03/page_0067.txt 对应“新沭河”泄洪语境。"),
]

CHECK_TERMS = ["新述河", "新沐河", "述南", "述北", "沐南", "沐北", "沂述", "沂沐"]


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
        "# 水利目录灌区调水防汛残留补修 batch359",
        "",
        f"- 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"- 修复总数：{total}",
        "- 范围：全书正文汇总、上册正文汇总中的目录、穿堤建筑物、灌区、调水线、防汛抗灾段。",
        "- 依据：上册 part02 page_0024、0271；上册 part03 page_0030、0031、0043、0044、0057、0058、0060、0067 页级 PaddleOCR 成句证据。",
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
    lines.extend(["", "## 保留边界", "", "- 正式 reader 中 `沐北航道` 暂未找到页级 OCR 证据，本批不处理。", "- 粮食、财政、港口及人物传记等非水利页残留继续另批核对。", "- 未处理 OCR 源文件、backup、obsolete、历史交付包。"])
    return "\n".join(lines) + "\n"


def upsert_memory(total: int, residuals: dict[str, int]) -> None:
    block = f"""{MARKER}

- 依据上册 part02 page_0024、0271 与上册 part03 page_0030、0031、0043、0044、0057、0058、0060、0067 页级 PaddleOCR 成句证据，补修水利目录、穿堤建筑物、灌区、调水线、防汛段残留，共 {total} 处。
- 代表修复：`新述河治理 -> 新沭河治理`、`沐南/沐北除涝 -> 沭南/沭北除涝`、`新述河沭南引水涵洞 -> 新沭河沭南引水涵洞`、`述北运河 -> 沭北运河`、`调引江淮水人赣榆县 -> 调引江淮水入赣榆县`、`新述河行洪低于 -> 新沭河行洪低于`、`沂述河中上游 -> 沂沭河中上游`。
- 本批后检查范围：`新述河` {residuals['新述河']}，`新沐河` {residuals['新沐河']}，`述南` {residuals['述南']}，`述北` {residuals['述北']}，`沐南` {residuals['沐南']}，`沐北` {residuals['沐北']}，`沂述` {residuals['沂述']}，`沂沐` {residuals['沂沐']}。
- 正式 reader 中 `沐北航道` 暂未找到页级 OCR 证据，本批不处理；未作 `述 -> 沭`、`沐 -> 沭`、`人 -> 入` 全局替换；未处理 OCR 源文件、backup、obsolete、历史交付包；未打开、展示或嵌入图片。
- 报告：`output/reports/full_summary_water_followup_batch359_20260708.md`；进度：`output/reports/progress/20260708_水利目录灌区调水防汛残留补修第三百五十九批.md`。
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
