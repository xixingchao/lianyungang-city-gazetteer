# -*- coding: utf-8 -*-
"""Repair source-backed water-page residuals in body summaries."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "output" / "reports" / "full_summary_water_pages_batch357_20260708.md"
REPORT_JSON = ROOT / "output" / "reports" / "full_summary_water_pages_batch357_20260708.json"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260708_全书汇总水利页新沭河残留补修第三百五十七批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"
MARKER = "## 2026-07-08 全书汇总水利页新沭河残留补修第三百五十七批"

TARGETS = [
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
    ROOT / "workbench" / "body_chapters" / "连云港市志_上册_正文汇总.md",
]

REPLACEMENTS = [
    ("沂水东调新述河人海规划", "沂水东调新沭河入海规划", "上/part02/page_0268.txt 明确为“沂水东调新沭河入海规划”。"),
    ("进行新沐河扩大工程", "进行新沭河扩大工程", "上/part02/page_0268.txt 明确为“新沭河扩大工程”。"),
    ("新沐河治理", "新沭河治理", "上/part02/page_0268.txt 标题为“第一节新沭河治理”。"),
    ("沐河古称述水", "沭河古称沭水", "上/part02/page_0268.txt 明确为“沭河古称沭水”。"),
    ("阻沐水西流", "阻沭水西流", "上/part02/page_0268.txt 明确为“阻沭水西流”。"),
    ("分述水之源", "分沭水之源", "上/part02/page_0268.txt 明确为“分沭水之源”。"),
    ("引沐水入赣榆大沙河", "引沭水入赣榆大沙河", "上/part02/page_0268.txt 明确为“引沭水入赣榆大沙河”。"),
    ("治理述河下游", "治理沭河下游", "上/part02/page_0268.txt 对应沭河下游语境。"),
    ("沂述下游连续5年洪灾", "沂沭下游连续5年洪灾", "上/part02/page_0268.txt 明确为“沂沭下游连续5年洪灾”。"),
    ("解除沂述洪水灾害", "解除沂沭洪水灾害", "上/part02/page_0268.txt 明确为“解除沂沭洪水灾害”。"),
    ("导沐工程治理初步方案", "导沭工程治理初步方案", "上/part02/page_0268.txt 明确为“导沭工程治理初步方案”。"),
    ("导述”的治理原则", "导沭”的治理原则", "上/part02/page_0268.txt 明确为“导沭”的治理原则。"),
    ("导述经沙入海河段", "导沭经沙入海河段", "上/part02/page_0268.txt 明确为“导沭经沙入海河段”。"),
    ("但新述\n河境内", "但新沭\n河境内", "上/part02/page_0269.txt 同段为新沭河。"),
    ("新述河行洪3070", "新沭河行洪3070", "上/part02/page_0269.txt 明确为“新沭河行洪3070”。"),
    ("蒋庄漫水闻消力池", "蒋庄漫水闸消力池", "上/part02/page_0269.txt 明确为“蒋庄漫水闸消力池”。"),
    ("新沐河中游兴建石梁河水库", "新沭河中游兴建石梁河水库", "上/part02/page_0269.txt 明确为“新沭河中游兴建石梁河水库”。"),
    ("形成“-河一库控制”", "形成“一河一库控制”", "上/part02/page_0269.txt 明确为“一河一库控制”。"),
    ("利用蕃薇河入海通道", "利用蔷薇河入海通道", "上/part02/page_0269.txt 明确为“蔷薇河入海通道”。"),
    ("沭河道和新述河", "沭河道和新沭河", "上/part02/page_0269.txt 明确为“沭河道和新沭河”。"),
    ("新述河泄洪量", "新沭河泄洪量", "上/part02/page_0269.txt 明确为“新沭河泄洪量”。"),
    ("石梁河水库位于新述河中游", "石梁河水库位于新沭河中游", "上/part02/page_0274.txt 明确为“新沭河中游”。"),
    ("山东省临沐县接壤", "山东省临沭县接壤", "上/part02/page_0274.txt 明确为“临沭县”。"),
    ("保障新述河防洪安全", "保障新沭河防洪安全", "上/part02/page_0274.txt 明确为“新沭河防洪安全”。"),
    ("《沂\n沐泗流域规划报告》", "《沂\n沭泗流域规划报告》", "上/part02/page_0274.txt 明确为“沂沭泗流域规划报告”。"),
    ("拦洪蕃水", "拦洪蓄水", "上/part02/page_0274.txt 明确为“拦洪蓄水”。"),
    ("1978年新述河大官庄闸", "1978年新沭河大官庄闸", "上/part02/page_0274.txt 明确为“1978年新沭河大官庄闸”。"),
    ("新述河自由分流", "新沭河自由分流", "上/part02/page_0274.txt 明确为“新沭河自由分流”。"),
    ("老述河大官庄", "老沭河大官庄", "上/part02/page_0274.txt 明确为“老沭河大官庄”。"),
    ("述河大官庄以上", "沭河大官庄以上", "上/part02/page_0274.txt 明确为“沭河大官庄以上”。"),
]

CHECK_TERMS = [old for old, _, _ in REPLACEMENTS] + ["新述河", "新沐河", "导述", "述南", "述北"]


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
        "# 全书汇总水利页新沭河残留补修 batch357",
        "",
        f"- 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"- 修复总数：{total}",
        "- 范围：全书正文汇总、上册正文汇总的水利 LYG-S-0568/0569/0574 对应段。",
        "- 依据：上册 part02 page_0268、page_0269、page_0274 页级 PaddleOCR 成句证据。",
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
    for term, count in residuals.items():
        if count:
            lines.append(f"- `{term}`：{count}")
    lines.extend(["", "## 保留边界", "", "- 其它水利页残留继续按页级 OCR 分批处理；目录、表格和题名不在本批处理。", "- 未处理 OCR 源文件、backup、obsolete、历史交付包。"])
    return "\n".join(lines) + "\n"


def upsert_memory(total: int, residuals: dict[str, int]) -> None:
    block = f"""{MARKER}

- 依据上册 part02 page_0268、page_0269、page_0274 页级 PaddleOCR 成句证据，补修全书正文汇总/上册正文汇总水利 LYG-S-0568/0569/0574 对应段残留，共 {total} 处。
- 代表修复：`沂水东调新述河人海规划 -> 沂水东调新沭河入海规划`、`导沐工程治理初步方案 -> 导沭工程治理初步方案`、`导述经沙入海河段 -> 导沭经沙入海河段`、`新述河行洪3070 -> 新沭河行洪3070`、`石梁河水库位于新述河中游 -> 石梁河水库位于新沭河中游`、`老述河大官庄 -> 老沭河大官庄`。
- 本批后检查范围：`新述河` {residuals['新述河']}，`新沐河` {residuals['新沐河']}，`导述` {residuals['导述']}，`述南` {residuals['述南']}，`述北` {residuals['述北']}。
- 未作 `述 -> 沭`、`沐 -> 沭`、`人 -> 入` 全局替换；未处理 OCR 源文件、backup、obsolete、历史交付包；未打开、展示或嵌入图片。
- 报告：`output/reports/full_summary_water_pages_batch357_20260708.md`；进度：`output/reports/progress/20260708_全书汇总水利页新沭河残留补修第三百五十七批.md`。
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
    print(f"residuals={{'新述河': {residuals['新述河']}, '新沐河': {residuals['新沐河']}, '导述': {residuals['导述']}, '述南': {residuals['述南']}, '述北': {residuals['述北']}}}")
    print(f"report={REPORT}")


if __name__ == "__main__":
    main()
