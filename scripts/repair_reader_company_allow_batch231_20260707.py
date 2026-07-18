# -*- coding: utf-8 -*-
"""Repair source-backed company/allow OCR residues, batch 231."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = [
    ROOT / "output" / "final_reader" / "连云港市志_全书.html",
    ROOT / "output" / "final_reader" / "连云港市志_中册.html",
    ROOT / "output" / "final_reader" / "连云港市志_下册.html",
    ROOT / "workbench" / "body_chapters" / "第十七卷至第二十九卷（中part01）.md",
    ROOT / "workbench" / "body_chapters" / "第三十卷至第四十二卷（中part02）.md",
    ROOT / "workbench" / "body_chapters" / "第四十三卷至第五十一卷（下part01）.md",
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
]
REPORT_JSON = ROOT / "output" / "reports" / "reader_company_allow_batch231_20260707.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_company_allow_batch231_20260707.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260707_公司允许类正文残留补修第二百三十一批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

ITEMS = [
    ("医药公可饮片加工组", "医药公司饮片加工组", "workbench/ocr/paddle_ocr/中/part01/page_0122.txt", "医药公司饮片加工组"),
    ("德意志联邦共和国养格机械有限公可引进矽", "德意志联邦共和国乔格机械有限公司引进矽", "workbench/ocr/paddle_ocr/中/part01/page_0220.txt", "乔格机械有限公司引进矽"),
    ("进出口专业公可自选材料", "进出口专业公司自选材料", "workbench/ocr/paddle_ocr/中/part02/page_0206.txt", "进出口专业公司自选材料"),
    ("充许棉农\n自留1.5~2.5公斤", "允许棉农\n自留1.5~2.5公斤", "workbench/ocr/paddle_ocr/中/part02/page_0169.txt", "允许棉农\n自留1.5~2.5公斤"),
    ("充许棉农</p>", "允许棉农</p>", "workbench/ocr/paddle_ocr/中/part02/page_0169.txt", "允许棉农\n自留1.5~2.5公斤"),
    ("充许棉农</p><p>自留1.5~2.5公斤", "允许棉农</p><p>自留1.5~2.5公斤", "workbench/ocr/paddle_ocr/中/part02/page_0169.txt", "允许棉农\n自留1.5~2.5公斤"),
    ("应当充许多渠道经营", "应当允许多渠道经营", "workbench/ocr/paddle_ocr/中/part02/page_0234.txt", "应当允许多渠道经营"),
    ("市场和充许自由购销的物资", "市场和允许自由购销的物资", "workbench/ocr/paddle_ocr/中/part02/page_0263.txt", "市场和允许自由购销的物资"),
    ("亦充许参加当地社会统一招工", "亦允许参加当地社会统一招工", "workbench/ocr/paddle_ocr/下/part01/page_0241.txt", "亦允许参加当地社会统一招工"),
]


def ensure_evidence() -> None:
    missing = []
    for _, _, rel, snippet in ITEMS:
        text = (ROOT / rel).read_text(encoding="utf-8", errors="ignore")
        if snippet not in text:
            missing.append(f"{rel}: {snippet}")
    if missing:
        raise SystemExit("missing evidence: " + "; ".join(missing))


def main() -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    ensure_evidence()
    changes = []
    for path in TARGETS:
        text = path.read_text(encoding="utf-8", errors="ignore")
        original = text
        file_items = []
        for old, new, evidence, _ in ITEMS:
            count = text.count(old)
            if count:
                text = text.replace(old, new)
                file_items.append({"old": old, "new": new, "count": count, "evidence": evidence})
        if text != original:
            path.write_text(text, encoding="utf-8")
        changes.append({"file": str(path.relative_to(ROOT)), "items": file_items})

    residuals = {old: {str(path.relative_to(ROOT)): path.read_text(encoding="utf-8", errors="ignore").count(old) for path in TARGETS} for old, _, _, _ in ITEMS}
    payload = {"time": now, "changes": changes, "residuals": residuals}
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 公司允许类正文残留补修第二百三十一批",
        "",
        f"> 生成时间：{now}",
        "",
        "## 范围",
        "",
        "- 修复当前阅读稿和正文源稿中 `公可 -> 公司`、`充许 -> 允许` 的小批残留。",
        "- 所有替换均有页级 PaddleOCR 文本支撑；未做全局替换。",
        "- 未打开、展示或嵌入图片。",
        "",
        "## 修改统计",
        "",
        "| 文件 | 原文 | 新文 | 次数 | 证据 |",
        "|---|---|---|---:|---|",
    ]
    for item in changes:
        for change in item["items"]:
            lines.append(f"| `{item['file']}` | `{change['old']}` | `{change['new']}` | {change['count']} | `{change['evidence']}` |")
    lines.extend(["", "## 残留计数", ""])
    for old, files in residuals.items():
        lines.append(f"- `{old}`：{sum(files.values())}")
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    PROGRESS.write_text(REPORT_MD.read_text(encoding="utf-8"), encoding="utf-8")

    memory = MEMORY.read_text(encoding="utf-8", errors="ignore").rstrip()
    memory += "\n\n## 2026-07-07 公司允许类正文残留补修第二百三十一批\n\n"
    memory += "- 依据页级 PaddleOCR，修复 `医药公可/机械有限公可/进出口专业公可` 与 `充许棉农/充许多渠道/充许自由购销/亦充许参加` 等残留。\n"
    memory += "- 同步范围：当前中册/下册/全书阅读稿及相关正文源稿；报告：`output/reports/reader_company_allow_batch231_20260707.md`。\n"
    memory += "- 本批未做全局替换，未打开、展示或嵌入图片。\n"
    MEMORY.write_text(memory + "\n", encoding="utf-8")

    print(json.dumps({
        "changed_files": sum(1 for item in changes if item["items"]),
        "changed_items": sum(change["count"] for item in changes for change in item["items"]),
        "residual_total": sum(sum(files.values()) for files in residuals.values()),
        "report": str(REPORT_MD),
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
