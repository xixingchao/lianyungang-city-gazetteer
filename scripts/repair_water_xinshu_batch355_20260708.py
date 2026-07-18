# -*- coding: utf-8 -*-
"""Repair source-backed `新沭河/沂沭/沭南/沭北` water-chapter residuals."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "output" / "reports" / "water_xinshu_batch355_20260708.md"
REPORT_JSON = ROOT / "output" / "reports" / "water_xinshu_batch355_20260708.json"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260708_水利卷新沭河沂沭残留补修第三百五十五批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"
MARKER = "## 2026-07-08 水利卷新沭河沂沭残留补修第三百五十五批"

TARGETS = [
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
    ROOT / "workbench" / "body_chapters" / "连云港市志_上册_正文汇总.md",
    ROOT / "output" / "final_reader" / "连云港市志_全书.html",
]

REPLACEMENTS = [
    {"old": "民国政府始兴办沂沐尾间工\n程", "new": "民国政府始兴办沂沭尾间工\n程", "evidence": "页级 PaddleOCR `workbench/ocr/paddle_ocr/上/part02/page_0267.txt` 明确为“沂沭尾间工程”。"},
    {"old": "进行沂沐尾间\n工程", "new": "进行沂沭尾间\n工程", "evidence": "页级 PaddleOCR `workbench/ocr/paddle_ocr/上/part02/page_0268.txt` 明确为“沂沭尾间工程”。"},
    {"old": "沂沐下游河道尽遭淤塞", "new": "沂沭下游河道尽遭淤塞", "evidence": "页级 PaddleOCR `workbench/ocr/paddle_ocr/上/part02/page_0288.txt` 明确为“沂沭下游河道尽遭淤塞”。"},
    {"old": "沂沐洪水开始相互侵扰", "new": "沂沭洪水开始相互侵扰", "evidence": "页级 PaddleOCR `workbench/ocr/paddle_ocr/上/part02/page_0288.txt` 明确为“沂沭洪水开始相互侵扰”。"},
    {"old": "沂沐河中上游连降暴雨", "new": "沂沭河中上游连降暴雨", "evidence": "页级 PaddleOCR `workbench/ocr/paddle_ocr/上/part03/page_0068.txt` 明确为“沂沭河中上游连降暴雨”。"},
    {"old": "沂述河洪水出路", "new": "沂沭河洪水出路", "evidence": "页级 PaddleOCR `workbench/ocr/paddle_ocr/上/part02/page_0267.txt`、`page_0268.txt` 明确为“沂沭河洪水出路”。"},
    {"old": "沂述上游泄洪量", "new": "沂沭上游泄洪量", "evidence": "页级 PaddleOCR `workbench/ocr/paddle_ocr/上/part02/page_0268.txt` 明确为“沂沭上游泄洪量”。"},
    {"old": "导沐整沂", "new": "导沭整沂", "evidence": "页级 PaddleOCR `workbench/ocr/paddle_ocr/上/part02/page_0268.txt` 明确为“导沭整沂”。"},
    {"old": "导沂整述", "new": "导沂整沭", "evidence": "页级 PaddleOCR `workbench/ocr/paddle_ocr/上/part01/page_0035.txt`、`上/part02/page_0268.txt`、`下/part02/page_0365.txt` 明确为“导沂整沭”。"},
    {"old": "新述河、新沂河", "new": "新沭河、新沂河", "evidence": "页级 PaddleOCR `workbench/ocr/paddle_ocr/上/part02/page_0268.txt` 明确为“新沭河、新沂河”。"},
    {"old": "新述河行洪安全", "new": "新沭河行洪安全", "evidence": "页级 PaddleOCR `workbench/ocr/paddle_ocr/上/part02/page_0268.txt` 明确为“新沭河行洪安全”。"},
    {"old": "新沐河整修工程", "new": "新沭河整修工程", "evidence": "页级 PaddleOCR `workbench/ocr/paddle_ocr/上/part02/page_0268.txt` 明确为“新沭河整修工程”。"},
    {"old": "沂水东调新述河入海规划", "new": "沂水东调新沭河入海规划", "evidence": "页级 PaddleOCR `workbench/ocr/paddle_ocr/上/part02/page_0268.txt` 明确为“沂水东调新沭河入海规划”。"},
    {"old": "新述河扩大工程未\n按计划全部完成", "new": "新沭河扩大工程未\n按计划全部完成", "evidence": "页级 PaddleOCR `workbench/ocr/paddle_ocr/上/part02/page_0268.txt` 明确为“新沭河扩大工程未按计划全部完成”。"},
    {"old": "新述河仅能安全行洪", "new": "新沭河仅能安全行洪", "evidence": "页级 PaddleOCR `workbench/ocr/paddle_ocr/上/part02/page_0268.txt` 明确为“新沭河仅能安全行洪”。"},
    {"old": "第一节新述河治理", "new": "第一节新沭河治理", "evidence": "页级 PaddleOCR `workbench/ocr/paddle_ocr/上/part02/page_0268.txt` 明确章节题为“第一节新沭河治理”。"},
    {"old": "导述经沙入海工程", "new": "导沭经沙入海工程", "evidence": "页级 PaddleOCR `workbench/ocr/paddle_ocr/上/part02/page_0268.txt` 明确为“导沭经沙入海工程”。"},
    {"old": "导述委员会", "new": "导沭委员会", "evidence": "页级 PaddleOCR `workbench/ocr/paddle_ocr/上/part02/page_0268.txt` 明确为“导沭委员会”。"},
    {"old": "导述经沙人海工程", "new": "导沭经沙入海工程", "evidence": "页级 PaddleOCR `workbench/ocr/paddle_ocr/上/part02/page_0268.txt` 明确为“导沭经沙入海工程”。"},
    {"old": "山东省临述县", "new": "山东省临沭县", "evidence": "页级 PaddleOCR `workbench/ocr/paddle_ocr/上/part02/page_0268.txt`、`page_0274.txt` 明确为“山东省临沭县”。"},
    {"old": "拦沐河", "new": "拦沭河", "evidence": "页级 PaddleOCR `workbench/ocr/paddle_ocr/上/part02/page_0268.txt` 明确为“拦沭河”。"},
    {"old": "限制述水南下", "new": "限制沭水南下", "evidence": "页级 PaddleOCR `workbench/ocr/paddle_ocr/上/part02/page_0268.txt` 明确为“限制沭水南下”。"},
    {"old": "开辟新述河至临", "new": "开辟新沭河至临", "evidence": "页级 PaddleOCR `workbench/ocr/paddle_ocr/上/part02/page_0268.txt` 明确为“开辟新沭河至临洪口”。"},
    {"old": "华东沂述汶运治导会议", "new": "华东沂沭汶运治导会议", "evidence": "页级 PaddleOCR `workbench/ocr/paddle_ocr/上/part02/page_0268.txt` 明确为“华东沂沭汶运治导会议”。"},
    {"old": "定名新沐河", "new": "定名新沭河", "evidence": "页级 PaddleOCR `workbench/ocr/paddle_ocr/上/part02/page_0268.txt` 明确为“定名新沭河”。"},
    {"old": "1952年新述河初步建成", "new": "1952年新沭河初步建成", "evidence": "页级 PaddleOCR `workbench/ocr/paddle_ocr/上/part02/page_0268.txt` 明确为“1952年新沭河初步建成”。"},
    {"old": "新述河全长78公里", "new": "新沭河全长78公里", "evidence": "页级 PaddleOCR `workbench/ocr/paddle_ocr/上/part02/page_0269.txt` 明确为“新沭河全长78公里”。"},
    {"old": "新述河上游21.4公里", "new": "新沭河上游21.4公里", "evidence": "页级 PaddleOCR `workbench/ocr/paddle_ocr/上/part02/page_0269.txt` 明确为“新沭河上游21.4公里”。"},
    {"old": "新述河初建设计", "new": "新沭河初建设计", "evidence": "页级 PaddleOCR `workbench/ocr/paddle_ocr/上/part02/page_0269.txt` 明确为“新沭河初建设计”。"},
    {"old": "治淮委员会召开沂述泗流域", "new": "治淮委员会召开沂沭泗流域", "evidence": "页级 PaddleOCR `workbench/ocr/paddle_ocr/上/part02/page_0269.txt` 明确为“沂沭泗流域”。"},
    {"old": "新述河下游险工", "new": "新沭河下游险工", "evidence": "页级 PaddleOCR `workbench/ocr/paddle_ocr/上/part02/page_0269.txt` 明确为“新沭河下游险工”。"},
    {"old": "新述河南北堤", "new": "新沭河南北堤", "evidence": "页级 PaddleOCR `workbench/ocr/paddle_ocr/上/part02/page_0269.txt` 明确为“新沭河南北堤”。"},
    {"old": "使新述河形成", "new": "使新沭河形成", "evidence": "页级 PaddleOCR `workbench/ocr/paddle_ocr/上/part02/page_0269.txt` 明确为“使新沭河形成”。"},
    {"old": "新述河为束水漫滩排洪河道", "new": "新沭河为束水漫滩排洪河道", "evidence": "页级 PaddleOCR `workbench/ocr/paddle_ocr/上/part02/page_0269.txt` 明确为“新沭河为束水漫滩排洪河道”。"},
    {"old": "水位雍高", "new": "水位壅高", "evidence": "页级 PaddleOCR `workbench/ocr/paddle_ocr/上/part02/page_0269.txt`、`上/part03/page_0067.txt` 明确为“水位壅高”。"},
    {"old": "影响新沐河两岸", "new": "影响新沭河两岸", "evidence": "页级 PaddleOCR `workbench/ocr/paddle_ocr/上/part02/page_0269.txt` 明确为“影响新沭河两岸”。"},
    {"old": "述南、述北受淹农田70万", "new": "沭南、沭北受淹农田70万", "evidence": "页级 PaddleOCR `workbench/ocr/paddle_ocr/上/part02/page_0269.txt` 明确为“沭南、沭北受淹农田70万”。"},
    {"old": "分沂入\n述河道", "new": "分沂入\n沭河道", "evidence": "页级 PaddleOCR `workbench/ocr/paddle_ocr/上/part02/page_0269.txt` 明确为“分沂入沭河道”。"},
    {"old": "沂述河上游", "new": "沂沭河上游", "evidence": "页级 PaddleOCR `workbench/ocr/paddle_ocr/上/part02/page_0269.txt` 明确为“沂沭河上游”。"},
    {"old": "从新沐河人海", "new": "从新沭河入海", "evidence": "页级 PaddleOCR `workbench/ocr/paddle_ocr/上/part02/page_0269.txt` 明确为“从新沭河入海”。"},
    {"old": "人海。新述河泄洪量", "new": "入海。新沭河泄洪量", "evidence": "页级 PaddleOCR `workbench/ocr/paddle_ocr/上/part02/page_0269.txt` 明确为“入海。新沭河泄洪量”。"},
    {"old": "新沐河扩大工程<", "new": "新沭河扩大工程<", "evidence": "页级 PaddleOCR `workbench/ocr/paddle_ocr/上/part02/page_0269.txt` 明确为“新沭河扩大工程”。"},
    {"old": "完成新河石梁河水库", "new": "完成新沭河石梁河水库", "evidence": "页级 PaddleOCR `workbench/ocr/paddle_ocr/上/part02/page_0269.txt` 明确为“完成新沭河石梁河水库至太平庄闸段”。"},
    {"old": "沐南、沐北通航闸", "new": "沭南、沭北通航闸", "evidence": "页级 PaddleOCR `workbench/ocr/paddle_ocr/上/part02/page_0269.txt` 明确为“沭南、沭北通航闸”。"},
    {"old": "完成述南、述北部分附属工程", "new": "完成沭南、沭北部分附属工程", "evidence": "页级 PaddleOCR `workbench/ocr/paddle_ocr/上/part02/page_0269.txt` 明确为“完成沭南、沭北部分附属工程”。"},
    {"old": "新述河清障复堤", "new": "新沭河清障复堤", "evidence": "页级 PaddleOCR `workbench/ocr/paddle_ocr/上/part02/page_0270.txt` 明确为“新沭河清障复堤”。"},
    {"old": "因新述河扩大工程于1980年停缓建", "new": "因新沭河扩大工程于1980年停缓建", "evidence": "页级 PaddleOCR `workbench/ocr/paddle_ocr/上/part02/page_0270.txt` 明确为“新沭河扩大工程”。"},
    {"old": "境内新述河行洪能力", "new": "境内新沭河行洪能力", "evidence": "页级 PaddleOCR `workbench/ocr/paddle_ocr/上/part02/page_0270.txt` 明确为“境内新沭河行洪能力”。"},
    {"old": "1990年新述河", "new": "1990年新沭河", "evidence": "页级 PaddleOCR `workbench/ocr/paddle_ocr/上/part02/page_0270.txt` 明确表题为“1990年新沭河...”。"},
]
CHECK_TERMS = [
    "沂沐尾间",
    "沂沐下游",
    "导沐整沂",
    "导沂整述",
    "新述河",
    "新沐河",
    "山东省临述县",
    "拦沐河",
    "限制述水南下",
    "沐南、沐北通航闸",
    "述南、述北",
    "水位雍高",
    "从新沐河人海",
    "人海。新述河泄洪量",
    "新沭河",
    "沂沭河",
]


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
        for item in REPLACEMENTS:
            count = updated.count(item["old"])
            if not count:
                continue
            updated = updated.replace(item["old"], item["new"])
            changes.append({"path": rel(path), "old": item["old"], "new": item["new"], "count": count, "evidence": item["evidence"]})
        if updated != text:
            path.write_text(updated, encoding="utf-8")
    residuals = {term: sum(read(path).count(term) for path in TARGETS if path.exists()) for term in CHECK_TERMS}
    return changes, residuals


def render(changes: list[dict], residuals: dict[str, int]) -> str:
    total = sum(item["count"] for item in changes)
    lines = [
        "# 水利卷新沭河沂沭残留补修 batch355",
        "",
        f"- 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"- 修复总数：{total}",
        "- 范围：全书正文汇总、上册正文汇总、正式全书中水利卷防洪段。",
        "- 依据：上册 part02 page_0267~0270、0274，part03 page_0068 及相关页级 PaddleOCR 成句证据。",
        "- 原则：只替换水利卷防洪语境中的完整短语；不作 `述 -> 沭`、`沐 -> 沭`、`人 -> 入` 全局替换。",
        "- 图片处理：未打开、展示或嵌入图片。",
        "",
        "## 替换明细",
    ]
    if changes:
        for item in changes:
            old = item["old"].replace("\n", "\\n")
            new = item["new"].replace("\n", "\\n")
            lines.append(f"- `{item['path']}`：`{old}` -> `{new}`；次数 {item['count']}；依据：{item['evidence']}")
    else:
        lines.append("- 本次未产生新增替换。")
    lines.extend(["", "## 检查结果", ""])
    for term, count in residuals.items():
        lines.append(f"- `{term}`：{count}")
    lines.extend([
        "",
        "## 保留边界",
        "",
        "- `导淮入江人海之研究`、`泗、沂、述分治合治之研究` 等题名/著作名残留未在本批处理。",
        "- 正式全书里粮食、党史、农机等章节的 `导述/述南` 零散残留另按各自页级 OCR 处理。",
        "- 目录和表格密集区中 `沐南/沐北` 仍需结合目录页或表格页单独核对。",
    ])
    return "\n".join(lines) + "\n"


def upsert_memory(total: int, residuals: dict[str, int]) -> None:
    block = f"""{MARKER}

- 依据上册 part02 page_0267~0270、0274，part03 page_0068 等页级 PaddleOCR 成句证据，补修水利卷防洪段 `新述河/新沐河/沂沐/导述/临述/述南述北` 等同源残留，共 {total} 处。
- 代表修复：`新述河 -> 新沭河` 相关完整短语、`导沐整沂 -> 导沭整沂`、`导沂整述 -> 导沂整沭`、`山东省临述县 -> 山东省临沭县`、`述南、述北 -> 沭南、沭北`、`水位雍高 -> 水位壅高`。
- 本批后检查范围：`导沂整述` {residuals['导沂整述']}，`山东省临述县` {residuals['山东省临述县']}，`述南、述北` {residuals['述南、述北']}，`水位雍高` {residuals['水位雍高']}，`从新沐河人海` {residuals['从新沐河人海']}。
- 保留题名/著作名和非水利卷零散残留另批核对；未作 `述 -> 沭`、`沐 -> 沭`、`人 -> 入` 全局替换；未处理 OCR 源文件、backup、obsolete、历史交付包；未打开、展示或嵌入图片。
- 报告：`output/reports/water_xinshu_batch355_20260708.md`；进度：`output/reports/progress/20260708_水利卷新沭河沂沭残留补修第三百五十五批.md`。
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
    total = sum(item["count"] for item in changes)
    data = {"time": datetime.now().strftime("%Y-%m-%d %H:%M"), "total": total, "changes": changes, "residuals": residuals, "replacements": REPLACEMENTS, "targets": [rel(path) for path in TARGETS]}
    REPORT_JSON.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    report = render(changes, residuals)
    REPORT.write_text(report, encoding="utf-8")
    PROGRESS.write_text(report, encoding="utf-8")
    upsert_memory(total, residuals)
    print(f"total={total}")
    print(f"residuals={residuals}")
    print(f"report={REPORT}")


if __name__ == "__main__":
    main()
