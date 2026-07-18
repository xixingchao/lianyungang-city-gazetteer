# -*- coding: utf-8 -*-
"""Repair narrowly source-backed enterprise residues, batch 105."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = [
    ROOT / "output" / "final_reader" / "连云港市志_全书.html",
    ROOT / "workbench" / "body_chapters" / "第十七卷至第二十九卷（中part01）.md",
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
]
REPORT_JSON = ROOT / "output" / "reports" / "reader_raw_backed_enterprise_gaiguang_batch105_20260706.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_raw_backed_enterprise_gaiguang_batch105_20260706.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260706_机械电子化工企业残留回源补修第一百零五批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    {
        "label": "异维C钠食品添加剂",
        "old": "异维C纳",
        "new": "异维C钠",
        "source": "workbench/ocr/raw/中/part01/page_0187.txt:65-68；同页多处为异维C钠",
    },
    {
        "label": "丙烯酸树脂",
        "old": "芮烯酸树脂",
        "new": "丙烯酸树脂",
        "source": "workbench/ocr/raw/中/part01/page_0187.txt:65-67；同页为丙烯酸树脂",
    },
    {
        "label": "制碘厂该厂获评",
        "old": "该广先后被评为省先进企业",
        "new": "该厂先后被评为省先进企业",
        "source": "workbench/ocr/raw/中/part01/page_0187.txt:63-68；上下文为该厂",
    },
    {
        "label": "东海县农机修造厂收割机",
        "old": "东海县农机修造广先后开发4GL收割机系列产品",
        "new": "东海县农机修造厂先后开发4GL收割机系列产品",
        "source": "workbench/ocr/raw/中/part01/page_0199.txt:4-9；同页下文为东海县农机修造厂",
    },
    {
        "label": "东海县农机修造厂技改",
        "old": "同年，该广投资160万元对收割机生产线进行技术改造",
        "new": "同年，该厂投资160万元对收割机生产线进行技术改造",
        "source": "workbench/ocr/raw/中/part01/page_0199.txt:4-9；上下文为东海县农机修造厂",
    },
    {
        "label": "赣榆县农机修造厂碾米机",
        "old": "该广不断改进生产工艺，增添设备",
        "new": "该厂不断改进生产工艺，增添设备",
        "source": "workbench/ocr/raw/中/part01/page_0200.txt:15-23；上下文为赣榆县农机修造厂",
    },
    {
        "label": "赣榆县农机修造厂碾米机断行",
        "old": "该广不断改进生产工",
        "new": "该厂不断改进生产工",
        "source": "workbench/ocr/raw/中/part01/page_0200.txt:15-23；源稿断行形态",
    },
    {
        "label": "连云港市水泵厂产品",
        "old": "该广产品有IS型全系列单级单吸清水离心泵",
        "new": "该厂产品有IS型全系列单级单吸清水离心泵",
        "source": "workbench/ocr/raw/中/part01/page_0214.txt:13-23；上下文为连云港市水泵厂",
    },
    {
        "label": "东海县农机修造厂滚齿机",
        "old": "东海县农机修造广1971年7月试制成功1台Y-38型滚齿机床",
        "new": "东海县农机修造厂1971年7月试制成功1台Y-38型滚齿机床",
        "source": "workbench/ocr/raw/中/part01/page_0226.txt:19-32；上下文为东海县农机修造厂",
    },
    {
        "label": "北京电视设备厂转让",
        "old": "北京电视设备广转让U/V转换器的生产技术",
        "new": "北京电视设备厂转让U/V转换器的生产技术",
        "source": "workbench/ocr/raw/中/part01/page_0250.txt:24-38；上下文为北京电视设备厂",
    },
    {
        "label": "联营厂伟视国产化",
        "old": "该广组织技术人员对“伟视”产品国产化",
        "new": "该厂组织技术人员对“伟视”产品国产化",
        "source": "workbench/ocr/raw/中/part01/page_0250.txt:34-38；上下文为联营厂/市无线电厂",
    },
    {
        "label": "无线电专用设备厂冲床",
        "old": "1971～1973年，该广年生产冲床100多台",
        "new": "1971～1973年，该厂年生产冲床100多台",
        "source": "workbench/ocr/raw/中/part01/page_0263.txt:24-31；上下文为连云港市无线电专用设备厂",
    },
]

LEFT_UNTOUCHED = [
    "建材、玻璃纤维、针织段剩余 `该广/广` 另行逐页处理。",
    "`一一批/一一些` 不做全局替换。",
    "本批未使用或展示页图。",
]


def upsert_memory(path: Path, marker: str, content: str) -> None:
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker not in old:
        path.write_text(old.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")
        return
    start = old.index(marker)
    next_start = old.find("\n## ", start + 1)
    new = old[:start].rstrip() + "\n\n" + content.strip() + "\n"
    if next_start != -1:
        new += "\n" + old[next_start:].lstrip()
    path.write_text(new, encoding="utf-8")


def main() -> None:
    applied = []
    for target in TARGETS:
        text = target.read_text(encoding="utf-8")
        items = []
        for item in REPLACEMENTS:
            count = text.count(item["old"])
            if count:
                text = text.replace(item["old"], item["new"])
            items.append({**item, "count": count})
        target.write_text(text, encoding="utf-8")
        verify = target.read_text(encoding="utf-8")
        residuals = [item["old"] for item in REPLACEMENTS if item["old"] in verify]
        if residuals:
            raise RuntimeError(f"replacement verification failed for {target}: {residuals[:3]}")
        for item in items:
            item["verified"] = verify.count(item["new"])
        applied.append({"target": str(target), "changed": sum(item["count"] for item in items), "items": items})

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "Raw OCR context-backed machinery, electronics and chemistry residue repair",
        "replacement_patterns": len(REPLACEMENTS),
        "changed_this_run": sum(target["changed"] for target in applied),
        "verified_total": sum(item["verified"] for target in applied for item in target["items"]),
        "targets": applied,
        "left_untouched": LEFT_UNTOUCHED,
        "principle": "Only exact contexts with source-page evidence are changed.",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 机械电子化工企业残留补修第一百零五批：raw OCR 回源",
        "",
        f"> 生成时间：{now}",
        "",
        "## 修复范围",
        "",
        "- 主阅读版及对应正文源稿/汇总中的化工、农业机械、水泵、电子设备和冲床段残留。",
        "- 只处理源页上下文能够闭合的精确短语。",
        "",
        "## 统计",
        "",
        f"- 证据短语：{len(REPLACEMENTS)} 项",
        f"- 本次运行新增替换：{payload['changed_this_run']} 处",
        f"- 当前核验覆盖：{payload['verified_total']} 处",
        "",
        "## 文件",
        "",
    ]
    for target in applied:
        lines.append(f"- `{target['target']}`：{target['changed']} 处")
    lines.extend(["", "## 修复项", ""])
    for item in REPLACEMENTS:
        lines.append(f"- {item['label']}: `{item['old']}` -> `{item['new']}`；源/定位：`{item['source']}`")
    lines.extend(["", "## 未处理边界", ""])
    for item in LEFT_UNTOUCHED:
        lines.append(f"- {item}")
    report = "\n".join(lines) + "\n"
    REPORT_MD.write_text(report, encoding="utf-8")
    PROGRESS.write_text(report, encoding="utf-8")

    marker = "## 2026-07-06 高置信 OCR 错字补修第一百零五批：机械电子化工企业残留"
    upsert_memory(MEMORY, marker, f"""
{marker}

- 继续按当前主交付 `output/final_reader/连云港市志_全书.html` 做回源修复，处理化工段 `异维C纳/芮烯酸树脂`、农业机械段 `农机修造广/该广`、水泵厂 `该广产品`、电子共用电视天线系统 `电视设备广/该广`、冲床段 `该广年生产`。
- 本批证据短语 {len(REPLACEMENTS)} 项，当前核验覆盖 {payload['verified_total']} 处；报告：`output/reports/reader_raw_backed_enterprise_gaiguang_batch105_20260706.md`。
- 边界：建材、玻璃纤维、针织段剩余 `该广/广` 留待下一批；未展示、未嵌入图片。
""")
    print(json.dumps({"patterns": len(REPLACEMENTS), "changed_this_run": payload["changed_this_run"], "verified_total": payload["verified_total"], "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
