# -*- coding: utf-8 -*-
"""Narrow page-OCR-backed cross-volume residue repairs."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "output" / "reports" / "cross_volume_ocr_batch301_20260707.md"
REPORT_JSON = ROOT / "output" / "reports" / "cross_volume_ocr_batch301_20260707.json"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260707_跨册页级OCR残字补修第三百零一批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

TARGETS = [
    ROOT / "output" / "final_reader" / "连云港市志_全书.html",
    ROOT / "output" / "final_reader" / "连云港市志_上册.html",
    ROOT / "output" / "final_reader" / "连云港市志_中册.html",
    ROOT / "output" / "final_reader" / "连云港市志_下册.html",
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
    ROOT / "workbench" / "body_chapters" / "连云港市志_上册_正文汇总.md",
    ROOT / "workbench" / "body_chapters" / "第十七卷至第二十九卷（中part01）.md",
    ROOT / "workbench" / "body_chapters" / "第三十卷至第四十二卷（中part02）.md",
    ROOT / "workbench" / "body_chapters" / "第四十三卷至第五十一卷（下part01）.md",
]

REPLACEMENTS = [
    (
        "分团千事会千事7人",
        "分团干事会干事7人",
        "PaddleOCR 中/part02/page_0465 为“分团干事会干事7人”。",
    ),
    (
        "劳保千事",
        "劳保干事",
        "PaddleOCR 下/part01/page_0317 为“车间设劳保干事”。",
    ),
    (
        "准海线上T接110千伏伊山变电所",
        "淮海线上T接110千伏伊山变电所",
        "PaddleOCR 中/part01/page_0348 为“淮海线上T接110千伏伊山变电所”。",
    ),
    (
        "新海发电广改设计循环水泵",
        "新海发电厂改设计循环水泵",
        "PaddleOCR 下/part01/page_0441 为“新海发电厂改设计循环水泵”。",
    ),
    (
        "平方公单范围内",
        "平方公里范围内",
        "PaddleOCR 中/part01/page_0431 为“起步区0.65平方公里范围内”。",
    ),
    (
        "长6公单",
        "长6公里",
        "PaddleOCR 上/part02/page_0059 为“玉带河，长6公里”。",
    ),
    (
        "提高到265方公斤",
        "提高到265万公斤",
        "PaddleOCR 上/part03/page_0049 为“提高到265万公斤”。",
    ),
]

CHECK_TERMS = [old for old, _new, _reason in REPLACEMENTS]


def apply_replacements() -> tuple[list[dict], dict[str, int]]:
    changes: list[dict] = []
    for path in TARGETS:
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        original = text
        for old, new, reason in REPLACEMENTS:
            count = text.count(old)
            if count:
                text = text.replace(old, new)
                changes.append({
                    "path": str(path.relative_to(ROOT)).replace("\\", "/"),
                    "old": old,
                    "new": new,
                    "count": count,
                    "reason": reason,
                })
        if text != original:
            path.write_text(text, encoding="utf-8")
    residuals: dict[str, int] = {}
    for term in CHECK_TERMS:
        residuals[term] = 0
        for path in TARGETS:
            if path.exists():
                residuals[term] += path.read_text(encoding="utf-8", errors="ignore").count(term)
    return changes, residuals


def render(changes: list[dict], residuals: dict[str, int]) -> str:
    total = sum(item["count"] for item in changes)
    lines = [
        "# 跨册页级 OCR 残字补修 batch301",
        "",
        f"- 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"- 修复总数：{total}",
        "- 范围：当前正式全书/分册 HTML、正式正文汇总及对应分册正文源稿。",
        "- 依据：PaddleOCR 上册 part02/page_0059、上册 part03/page_0049、中册 part01/page_0348/page_0431、中册 part02/page_0465、下册 part01/page_0317/page_0441。",
        "- 原则：只处理页级 OCR 明确支持的窄短语；不处理 OCR 源文件、backup、obsolete、历史交付包。",
        "- 图片处理：未打开、展示或嵌入图片。",
        "",
        "## 替换明细",
    ]
    for item in changes:
        lines.append(f"- `{item['path']}`：`{item['old']}` -> `{item['new']}`；次数 {item['count']}；依据：{item['reason']}")
    lines.extend(["", "## 残留计数", ""])
    bad = {key: value for key, value in residuals.items() if value}
    if not bad:
        lines.append("- 本批检查短语在当前检查范围中均为 0。")
    else:
        for key, value in bad.items():
            lines.append(f"- `{key}`：{value}")
    return "\n".join(lines) + "\n"


def append_memory(total: int) -> None:
    marker = "## 2026-07-07 跨册页级OCR残字补修第三百零一批"
    old = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker in old:
        return
    block = f"""
{marker}

- 依据 PaddleOCR 页级文本，跨册窄语境补修 `千事 -> 干事`、`准海线 -> 淮海线`、`发电广 -> 发电厂`、`平方公单/长6公单 -> 平方公里/长6公里`、`265方公斤 -> 265万公斤` 等残字，共 {total} 处。
- 报告：`output/reports/cross_volume_ocr_batch301_20260707.md`；进度：`output/reports/progress/20260707_跨册页级OCR残字补修第三百零一批.md`。
- 未处理 OCR 源文件、backup、obsolete、历史交付包；未打开、展示或嵌入图片。
"""
    MEMORY.write_text(old.rstrip() + "\n\n" + block.strip() + "\n", encoding="utf-8")


def main() -> None:
    changes, residuals = apply_replacements()
    total = sum(item["count"] for item in changes)
    data = {
        "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "total": total,
        "changes": changes,
        "residuals": residuals,
    }
    REPORT_JSON.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    report = render(changes, residuals)
    REPORT.write_text(report, encoding="utf-8")
    PROGRESS.write_text(report, encoding="utf-8")
    append_memory(total)
    print(f"total={total}")
    print(f"residuals_nonzero={ {k: v for k, v in residuals.items() if v} }")
    print(f"report={REPORT}")


if __name__ == "__main__":
    main()
