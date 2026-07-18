# -*- coding: utf-8 -*-
"""Repair source-backed Shunan/Shubei drainage residuals in body summaries."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "output" / "reports" / "full_summary_shunan_shubei_batch358_20260708.md"
REPORT_JSON = ROOT / "output" / "reports" / "full_summary_shunan_shubei_batch358_20260708.json"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260708_沭南沭北除涝残留补修第三百五十八批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"
MARKER = "## 2026-07-08 沭南沭北除涝残留补修第三百五十八批"

TARGETS = [
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
    ROOT / "workbench" / "body_chapters" / "连云港市志_上册_正文汇总.md",
]

REPLACEMENTS = [
    ("整治述北诸河", "整治沭北诸河", "上/part02/page_0289.txt 明确为“整治沭北诸河”。"),
    ("在述南、述北主要河道", "在沭南、沭北主要河道", "上/part02/page_0289.txt 明确为“沭南、沭北主要河道”。"),
    ("新沭河排洪与述南、述北地区", "新沭河排洪与沭南、沭北地区", "上/part02/page_0289.txt 明确为“沭南、沭北地区”。"),
    ("在述北地区实施", "在沭北地区实施", "上/part02/page_0289.txt 明确为“在沭北地区实施”。"),
    ("在述南地区兴建", "在沭南地区兴建", "上/part02/page_0289.txt 明确为“在沭南地区兴建”。"),
    ("新述河扩大工程停、缓建，述南、述北地区", "新沭河扩大工程停、缓建，沭南、沭北地区", "上/part02/page_0289.txt 明确为“新沭河扩大工程停、缓建，沭南、沭北地区”。"),
    ("实施“导述整沂”", "实施“导沭整沂”", "上/part02/page_0290.txt 明确为“导沭整沂”。"),
    ("就水利而言的沐南地区，是指新述河南", "就水利而言的沭南地区，是指新沭河南", "上/part02/page_0293.txt 明确为“沭南地区，是指新沭河南”。"),
    ("提出导沐经沙入海", "提出导沭经沙入海", "上/part02/page_0293.txt 明确为“导沭经沙入海”。"),
    ("沂述洪水为害", "沂沭洪水为害", "上/part02/page_0294.txt 明确为“沂沭洪水为害”。"),
    ("治理沂述的同时", "治理沂沭的同时", "上/part02/page_0294.txt 明确为“治理沂沭”。"),
    ("沂述洪水出路", "沂沭洪水出路", "上/part02/page_0294.txt 明确为“沂沭洪水出路”。"),
    ("实施导述整沂", "实施导沭整沂", "上/part02/page_0294.txt 明确为“导沭整沂”。"),
    ("开辟新述河，分\n泄述河洪水", "开辟新沭河，分\n泄沭河洪水", "上/part02/page_0294.txt 明确为“开辟新沭河，分泄沭河洪水”。"),
    ("解除沐南地区洪水灾害", "解除沭南地区洪水灾害", "上/part02/page_0294.txt 明确为“解除沭南地区洪水灾害”。"),
    ("新述河扩大工程开工。因新述河", "新沭河扩大工程开工。因新沭河", "上/part02/page_0294.txt 明确为“新沭河扩大工程开工。因新沭河”。"),
    ("影响述南地区排涝", "影响沭南地区排涝", "上/part02/page_0294.txt 明确为“影响沭南地区排涝”。"),
    ("解决述南洪涝矛盾", "解决沭南洪涝矛盾", "上/part02/page_0294.txt 明确为“解决沭南洪涝矛盾”。"),
    ("列入述南除涝治理工程", "列入沭南除涝治理工程", "上/part02/page_0295.txt 明确为“列入沭南除涝治理工程”。"),
    ("述南抽排站", "沭南抽排站", "上/part02/page_0295.txt 明确为“沭南抽排站”。"),
    ("述\n南地区降雨", "沭\n南地区降雨", "上/part02/page_0295.txt 明确为“沭南地区降雨”。"),
    ("新述河行洪3500", "新沭河行洪3500", "上/part02/page_0295.txt 明确为“新沭河行洪3500”。"),
    ("新沐河扩大工程停、缓建", "新沭河扩大工程停、缓建", "上/part02/page_0295.txt 明确为“新沭河扩大工程停、缓建”。"),
    ("述南除涝工程", "沭南除涝工程", "上/part02/page_0295.txt 明确为“沭南除涝工程”。"),
    ("对新述河扩大工程", "对新沭河扩大工程", "上/part02/page_0295.txt 明确为“对新沭河扩大工程”。"),
    ("1990年连云港市述南引排干支河基本惰况表", "1990年连云港市沭南引排干支河基本情况表", "上/part02/page_0295.txt 明确为“沭南...基本情况表”。"),
    ("就水利而言的述北地区，是指新述河以北", "就水利而言的沭北地区，是指新沭河以北", "上/part02/page_0296.txt 明确为“沭北地区，是指新沭河以北”。"),
    ("对述北诸河", "对沭北诸河", "上/part02/page_0296.txt 明确为“对沭北诸河”。"),
    ("对述北地区全面规", "对沭北地区全面规", "上/part02/page_0296.txt 明确为“对沭北地区全面规”。"),
    ("述北诸河上游", "沭北诸河上游", "上/part02/page_0297.txt 明确为“沭北诸河上游”。"),
    ("实施沂述河洪水东调新述河人海规划", "实施沂沭河洪水东调新沭河入海规划", "上/part02/page_0297.txt 明确为“沂沭河洪水东调新沭河入海规划”。"),
    ("开工新述河扩大工程。致使新述", "开工新沭河扩大工程。致使新沭", "上/part02/page_0297.txt 明确为“新沭河扩大工程。致使新沭”。"),
    ("列入沐北洼地除涝工程", "列入沭北洼地除涝工程", "上/part02/page_0297.txt 明确为“沭北洼地除涝工程”。"),
    ("青口河、新述河", "青口河、新沭河", "上/part02/page_0297.txt 明确为“青口河、新沭河”。"),
    ("因新述河扩大工程停、缓建，沐北洼地除涝工程", "因新沭河扩大工程停、缓建，沭北洼地除涝工程", "上/part02/page_0297.txt 明确为“新沭河扩大工程停、缓建，沭北洼地除涝工程”。"),
    ("述北地区排涝标准", "沭北地区排涝标准", "上/part02/page_0297.txt 明确为“沭北地区排涝标准”。"),
    ("1990年连云港市沐北引排干河基本情况表", "1990年连云港市沭北引排干河基本情况表", "上/part02/page_0297.txt 明确为“沭北引排干河基本情况表”。"),
    ("1990年连云港市述北样板控制河道基本情况表", "1990年连云港市沭北样板控制河道基本情况表", "上/part02/page_0298.txt 明确为“沭北样板控制河道基本情况表”。"),
    ("沐北一级", "沭北一级", "上/part02/page_0298.txt 明确为“沭北一级”。"),
    ("沐北二级", "沭北二级", "上/part02/page_0298.txt 明确为“沭北二级”。"),
    ("1990年连云港市述北主要控制涵闸基本情况表", "1990年连云港市沭北主要控制涵闸基本情况表", "上/part02/page_0298.txt 明确为“沭北主要控制涵闸基本情况表”。"),
]

CHECK_TERMS = [old for old, _, _ in REPLACEMENTS] + ["新述河", "新沐河", "导述", "述南", "述北", "沐南", "沐北"]


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
        "# 沭南沭北除涝残留补修 batch358",
        "",
        f"- 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"- 修复总数：{total}",
        "- 范围：全书正文汇总、上册正文汇总的 LYG-S-0589/0590/0593~0598 对应段。",
        "- 依据：上册 part02 page_0289、0290、0293、0294、0295、0296、0297、0298 页级 PaddleOCR 成句证据。",
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
    for term in ["新述河", "新沐河", "导述", "述南", "述北", "沐南", "沐北"]:
        lines.append(f"- `{term}`：{residuals[term]}")
    lines.extend(["", "## 保留边界", "", "- 古文、题名、目录和未逐页确认的残留继续保留；后续另批核对。", "- 未处理 OCR 源文件、backup、obsolete、历史交付包。"])
    return "\n".join(lines) + "\n"


def upsert_memory(total: int, residuals: dict[str, int]) -> None:
    block = f"""{MARKER}

- 依据上册 part02 page_0289、0290、0293、0294、0295、0296、0297、0298 页级 PaddleOCR 成句证据，补修全书正文汇总/上册正文汇总沭南、沭北除涝段残留，共 {total} 处。
- 代表修复：`述南/述北 -> 沭南/沭北` 对应完整短语、`新述河扩大工程 -> 新沭河扩大工程`、`导述整沂 -> 导沭整沂`、`沂述河洪水东调新述河人海规划 -> 沂沭河洪水东调新沭河入海规划`、`基本惰况表 -> 基本情况表`。
- 本批后检查范围：`新述河` {residuals['新述河']}，`新沐河` {residuals['新沐河']}，`导述` {residuals['导述']}，`述南` {residuals['述南']}，`述北` {residuals['述北']}，`沐南` {residuals['沐南']}，`沐北` {residuals['沐北']}。
- 未作 `述 -> 沭`、`沐 -> 沭`、`人 -> 入` 全局替换；未处理 OCR 源文件、backup、obsolete、历史交付包；未打开、展示或嵌入图片。
- 报告：`output/reports/full_summary_shunan_shubei_batch358_20260708.md`；进度：`output/reports/progress/20260708_沭南沭北除涝残留补修第三百五十八批.md`。
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
    print({term: residuals[term] for term in ["新述河", "新沐河", "导述", "述南", "述北", "沐南", "沐北"]})
    print(f"report={REPORT}")


if __name__ == "__main__":
    main()
