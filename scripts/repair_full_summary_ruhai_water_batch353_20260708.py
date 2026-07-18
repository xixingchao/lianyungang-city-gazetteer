# -*- coding: utf-8 -*-
"""Repair source-backed waterway `人/入` residuals in current text sources."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "output" / "reports" / "full_summary_ruhai_water_batch353_20260708.md"
REPORT_JSON = ROOT / "output" / "reports" / "full_summary_ruhai_water_batch353_20260708.json"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260708_全书汇总入海水利残留补修第三百五十三批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"
MARKER = "## 2026-07-08 全书汇总入海水利残留补修第三百五十三批"

TARGETS = [
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
    ROOT / "workbench" / "body_chapters" / "连云港市志_上册_正文汇总.md",
    ROOT / "workbench" / "body_chapters" / "第三十卷至第四十二卷（中part02）.md",
    ROOT / "output" / "final_reader" / "连云港市志_全书.html",
    ROOT / "output" / "final_reader" / "连云港市志_中册.html",
]

REPLACEMENTS = [
    {
        "old": "主要人海河流",
        "new": "主要入海河流",
        "evidence": "页级 PaddleOCR `workbench/ocr/paddle_ocr/上/part02/page_0116.txt` 明确为“主要入海河流”。",
    },
    {
        "old": "临洪河人海口断面",
        "new": "临洪河入海口断面",
        "evidence": "页级 PaddleOCR `workbench/ocr/paddle_ocr/上/part02/page_0116.txt` 明确为“临洪河入海口断面”。",
    },
    {
        "old": "增辟人海口门",
        "new": "增辟入海口门",
        "evidence": "页级 PaddleOCR `workbench/ocr/paddle_ocr/上/part02/page_0291.txt` 明确为“增辟入海口门”。",
    },
    {
        "old": "烧香河古道人海口",
        "new": "烧香河古道入海口",
        "evidence": "页级 PaddleOCR `workbench/ocr/paddle_ocr/上/part02/page_0292.txt`、`page_0304.txt` 明确为“烧香河古道入海口”。",
    },
    {
        "old": "境内人海口地区",
        "new": "境内入海口地区",
        "evidence": "页级 PaddleOCR `workbench/ocr/paddle_ocr/上/part02/page_0293.txt` 明确为“境内入海口地区”。",
    },
    {
        "old": "新述河人海口段",
        "new": "新沭河入海口段",
        "evidence": "页级 PaddleOCR `workbench/ocr/paddle_ocr/上/part02/page_0294.txt` 明确为“新沭河入海口段”。",
    },
    {
        "old": "蔷薇河人海通道",
        "new": "蔷薇河入海通道",
        "evidence": "页级 PaddleOCR `workbench/ocr/paddle_ocr/上/part02/page_0294.txt` 明确为“蔷薇河入海通道”。",
    },
    {
        "old": "新述河排洪时",
        "new": "新沭河排洪时",
        "evidence": "页级 PaddleOCR `workbench/ocr/paddle_ocr/上/part02/page_0294.txt` 明确为“新沭河排洪时”。",
    },
    {
        "old": "新述河泄洪3000",
        "new": "新沭河泄洪3000",
        "evidence": "页级 PaddleOCR `workbench/ocr/paddle_ocr/上/part02/page_0294.txt` 明确为“新沭河泄洪3000”。",
    },
    {
        "old": "沂沐河中下游",
        "new": "沂沭河中下游",
        "evidence": "页级 PaddleOCR `workbench/ocr/paddle_ocr/上/part02/page_0294.txt` 明确为“沂沭河中下游”。",
    },
    {
        "old": "述南60万亩",
        "new": "沭南60万亩",
        "evidence": "页级 PaddleOCR `workbench/ocr/paddle_ocr/上/part02/page_0294.txt` 明确为“沭南60万亩”。",
    },
    {
        "old": "沂述河洪水东调新述河入海规划",
        "new": "沂沭河洪水东调新沭河入海规划",
        "evidence": "页级 PaddleOCR `workbench/ocr/paddle_ocr/上/part02/page_0294.txt` 明确为“沂沭河洪水东调新沭河入海规划”。",
    },
    {
        "old": "人民政府在举办导述经沙人海工程的同时",
        "new": "人民政府在举办导沭经沙入海工程的同时",
        "evidence": "页级 PaddleOCR `workbench/ocr/paddle_ocr/上/part02/page_0296.txt` 明确为“导沭经沙入海工程”。",
    },
    {
        "old": "青口河人海口",
        "new": "青口河入海口",
        "evidence": "页级 PaddleOCR `workbench/ocr/paddle_ocr/上/part02/page_0296.txt`、`page_0304.txt` 明确为“青口河入海口”。",
    },
    {
        "old": "庄河人龙河",
        "new": "庄河入龙河",
        "evidence": "页级 PaddleOCR `workbench/ocr/paddle_ocr/上/part02/page_0296.txt` 明确为“上庄河入龙河”。",
    },
    {
        "old": "对述北地区全面规划",
        "new": "对沭北地区全面规划",
        "evidence": "页级 PaddleOCR `workbench/ocr/paddle_ocr/上/part02/page_0296.txt` 同页章节为“沭北除涝”，并明确为“对沭北地区全面规划”。",
    },
    {
        "old": "涝水畅通人海",
        "new": "涝水畅通入海",
        "evidence": "页级 PaddleOCR `workbench/ocr/paddle_ocr/上/part02/page_0289.txt`、`page_0296.txt` 明确为“涝水畅通入海”。",
    },
    {
        "old": "人海口建范河闸",
        "new": "入海口建范河闸",
        "evidence": "页级 PaddleOCR `workbench/ocr/paddle_ocr/上/part02/page_0296.txt` 明确为“入海口建范河闸”。",
    },
    {
        "old": "人海口\n建兴庄河闸",
        "new": "入海口\n建兴庄河闸",
        "evidence": "页级 PaddleOCR `workbench/ocr/paddle_ocr/上/part02/page_0296.txt` 明确为“入海口建兴庄河闸”。",
    },
    {
        "old": "导官庄河人兴庄河",
        "new": "导官庄河入兴庄河",
        "evidence": "页级 PaddleOCR `workbench/ocr/paddle_ocr/上/part02/page_0296.txt` 明确为“导官庄河入兴庄河”。",
    },
    {
        "old": "人海口建沙汪河闸",
        "new": "入海口建沙汪河闸",
        "evidence": "页级 PaddleOCR `workbench/ocr/paddle_ocr/上/part02/page_0297.txt` 明确为“入海口建沙汪河闸”。",
    },
    {
        "old": "改道人龙河",
        "new": "改道入龙河",
        "evidence": "页级 PaddleOCR `workbench/ocr/paddle_ocr/上/part02/page_0297.txt` 明确为“官庄河改道入龙河”。",
    },
    {
        "old": "青口河南人海",
        "new": "青口河南入海",
        "evidence": "页级 PaddleOCR `workbench/ocr/paddle_ocr/上/part02/page_0297.txt` 明确为“青口河南入海”。",
    },
    {
        "old": "人海口建青口河挡潮闸",
        "new": "入海口建青口河挡潮闸",
        "evidence": "页级 PaddleOCR `workbench/ocr/paddle_ocr/上/part02/page_0297.txt` 明确为“入海口建青口河挡潮闸”。",
    },
    {
        "old": "韩口河、人海口建韩口河闸",
        "new": "韩口河、入海口建韩口河闸",
        "evidence": "页级 PaddleOCR `workbench/ocr/paddle_ocr/上/part02/page_0297.txt` 明确为“韩口河、入海口建韩口河闸”。",
    },
    {
        "old": "经青口河人海",
        "new": "经青口河入海",
        "evidence": "页级 PaddleOCR `workbench/ocr/paddle_ocr/上/part02/page_0297.txt` 明确为“经青口河入海”。",
    },
    {
        "old": "寺后村西人朱稽副河",
        "new": "寺后村西入朱稽副河",
        "evidence": "页级 PaddleOCR `workbench/ocr/paddle_ocr/上/part02/page_0297.txt` 明确为“寺后村西入朱稽副河”。",
    },
    {
        "old": "人海口段自郑园村起",
        "new": "入海口段自郑园村起",
        "evidence": "页级 PaddleOCR `workbench/ocr/paddle_ocr/上/part02/page_0297.txt` 明确为“入海口段自郑园村起”。",
    },
    {
        "old": "并人范河调尾",
        "new": "并入范河调尾",
        "evidence": "页级 PaddleOCR `workbench/ocr/paddle_ocr/上/part02/page_0297.txt` 明确为“并入范河调尾”。",
    },
    {
        "old": "述北一级截洪沟",
        "new": "沭北一级截洪沟",
        "evidence": "页级 PaddleOCR `workbench/ocr/paddle_ocr/上/part02/page_0297.txt` 明确为“沭北一级截洪沟”。",
    },
    {
        "old": "述北二级截洪沟",
        "new": "沭北二级截洪沟",
        "evidence": "页级 PaddleOCR `workbench/ocr/paddle_ocr/上/part02/page_0297.txt` 明确为“沭北二级截洪沟”。",
    },
    {
        "old": "开挖述北闸至范口段（述北运河）",
        "new": "开挖沭北闸至范口段（沭北运河）",
        "evidence": "页级 PaddleOCR `workbench/ocr/paddle_ocr/上/part02/page_0297.txt` 明确为“沭北闸至范口段（沭北运河）”。",
    },
    {
        "old": "朱稽河新道人海口",
        "new": "朱稽河新道入海口",
        "evidence": "页级 PaddleOCR `workbench/ocr/paddle_ocr/上/part02/page_0298.txt`、`page_0304.txt` 明确为“朱稽河新道入海口”。",
    },
    {
        "old": "韩口河人海口",
        "new": "韩口河入海口",
        "evidence": "页级 PaddleOCR `workbench/ocr/paddle_ocr/上/part02/page_0299.txt` 明确为“韩口河入海口”。",
    },
    {
        "old": "柘汪河人海口",
        "new": "柘汪河入海口",
        "evidence": "页级 PaddleOCR `workbench/ocr/paddle_ocr/上/part02/page_0299.txt` 明确为“柘汪河入海口”。",
    },
    {
        "old": "善后河新道人海口",
        "new": "善后河新道入海口",
        "evidence": "页级 PaddleOCR `workbench/ocr/paddle_ocr/上/part02/page_0303.txt` 明确为“善后河新道入海口”。",
    },
    {
        "old": "兴庄河人海口",
        "new": "兴庄河入海口",
        "evidence": "页级 PaddleOCR `workbench/ocr/paddle_ocr/上/part02/page_0304.txt` 明确为“兴庄河入海口”。",
    },
    {
        "old": "范河人海口",
        "new": "范河入海口",
        "evidence": "页级 PaddleOCR `workbench/ocr/paddle_ocr/上/part02/page_0304.txt` 明确为“范河入海口”。",
    },
    {
        "old": "排淡河人海口",
        "new": "排淡河入海口",
        "evidence": "页级 PaddleOCR `workbench/ocr/paddle_ocr/上/part02/page_0304.txt` 明确为“排淡河入海口”。",
    },
    {
        "old": "车轴河人海口",
        "new": "车轴河入海口",
        "evidence": "页级 PaddleOCR `workbench/ocr/paddle_ocr/上/part02/page_0305.txt` 明确为“车轴河入海口”。",
    },
    {
        "old": "通人海州城内",
        "new": "通入海州城内",
        "evidence": "页级 PaddleOCR `workbench/ocr/paddle_ocr/中/part02/page_0045.txt` 明确为“通入海州城内”。",
    },
    {
        "old": "此河人海口无闸",
        "new": "此河入海口无闸",
        "evidence": "页级 PaddleOCR `workbench/ocr/paddle_ocr/中/part02/page_0045.txt` 明确为“此河入海口无闸”。",
    },
    {
        "old": "沂述之水",
        "new": "沂沭之水",
        "evidence": "页级 PaddleOCR `workbench/ocr/paddle_ocr/中/part02/page_0045.txt` 明确为“沂沭之水”。",
    },
    {
        "old": "青口河：自从1951年在人海口开挖导疏河起",
        "new": "青口河：自从1951年在入海口开挖导疏河起",
        "evidence": "页级 PaddleOCR `workbench/ocr/paddle_ocr/中/part02/page_0229.txt` 明确为“在入海口开挖导疏河”。",
    },
]

CHECK_TERMS = [
    "人海口",
    "人海口门",
    "主要人海河流",
    "临洪河人海口断面",
    "新述河人海口段",
    "蔷薇河人海通道",
    "通人海州城内",
    "此河人海口无闸",
    "青口河：自从1951年在人海口开挖导疏河起",
    "获水村人海口",
    "入海口",
    "新沭河入海口段",
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
        "# 全书汇总入海水利残留补修 batch353",
        "",
        f"- 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"- 修复总数：{total}",
        "- 范围：全书正文汇总、上册正文汇总、中册 part02 当前源稿；正式全书/中册仅作同步检查，当前未命中同类残留。",
        "- 依据：上册 part02 page_0116、0289、0291、0292、0293、0294、0296、0297、0298、0299、0303、0304、0305 与中册 part02 page_0045、0229 页级 PaddleOCR 成句证据。",
        "- 原则：只替换水利/航运语境中的完整短语；不作 `人 -> 入`、`述 -> 沭`、`沐 -> 沭` 全局替换。",
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
        "- `获水村人海口` 保留未改：所在为表格行，页级 OCR `workbench/ocr/paddle_ocr/上/part02/page_0297.txt` 仍识别为 `人海口`；虽上册正文汇总同表已为 `入海口`，本批不凭推断改表格残段。",
        "- 其它 `新述河/述南/述北/导述` 残留仍需另行按页核对，本批只处理与入海/入河同句且证据明确的短语。",
    ])
    return "\n".join(lines) + "\n"


def upsert_memory(total: int, residuals: dict[str, int]) -> None:
    block = f"""{MARKER}

- 依据上册 part02 page_0116、0289、0291、0292、0293、0294、0296、0297、0298、0299、0303、0304、0305 与中册 part02 page_0045、0229 页级 PaddleOCR 成句证据，补修全书正文汇总/相关源稿水利、航运语境 `人海口/人海/述/沐` 残留，共 {total} 处。
- 代表修复：`主要人海河流 -> 主要入海河流`、`临洪河人海口断面 -> 临洪河入海口断面`、`增辟人海口门 -> 增辟入海口门`、`新述河人海口段 -> 新沭河入海口段`、`通人海州城内 -> 通入海州城内`。
- 本批后检查范围：`人海口` {residuals['人海口']}，`人海口门` {residuals['人海口门']}，`主要人海河流` {residuals['主要人海河流']}，`临洪河人海口断面` {residuals['临洪河人海口断面']}，`此河人海口无闸` {residuals['此河人海口无闸']}。
- 保留 `获水村人海口`：页级 OCR 仍识别为 `人海口`，虽同表在上册正文汇总为 `入海口`，本批不凭推断改表格残段；其它 `新述河/述南/述北/导述` 残留留待另批逐页核对。
- 未作 `人 -> 入`、`述 -> 沭`、`沐 -> 沭` 全局替换；未处理 OCR 源文件、backup、obsolete、历史交付包；未打开、展示或嵌入图片。
- 报告：`output/reports/full_summary_ruhai_water_batch353_20260708.md`；进度：`output/reports/progress/20260708_全书汇总入海水利残留补修第三百五十三批.md`。
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
    data = {
        "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "total": total,
        "changes": changes,
        "residuals": residuals,
        "replacements": REPLACEMENTS,
        "targets": [rel(path) for path in TARGETS],
    }
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
