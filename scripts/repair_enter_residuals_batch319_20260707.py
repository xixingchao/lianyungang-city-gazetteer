# -*- coding: utf-8 -*-
"""Narrow enter/into residual repairs backed by page OCR."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "output" / "reports" / "enter_residuals_batch319_20260707.md"
REPORT_JSON = ROOT / "output" / "reports" / "enter_residuals_batch319_20260707.json"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260707_人入类残留补修第三百一十九批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

TARGETS = [
    ROOT / "output" / "final_reader" / "连云港市志_全书.html",
    ROOT / "output" / "final_reader" / "连云港市志_中册.html",
    ROOT / "output" / "final_reader" / "连云港市志_下册.html",
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
    ROOT / "workbench" / "body_chapters" / "连云港市志_上册_正文汇总.md",
    ROOT / "workbench" / "body_chapters" / "第十七卷至第二十九卷（中part01）.md",
    ROOT / "workbench" / "body_chapters" / "第三十卷至第四十二卷（中part02）.md",
    ROOT / "workbench" / "body_chapters" / "第四十三卷至第五十一卷（下part01）.md",
]

REPLACEMENTS = [
    ("潜人连云港市", "潜入连云港市", "PaddleOCR 下/part01/page_0184 为“潜入连云港市”。"),
    ("传人连云港市", "传入连云港市", "PaddleOCR 上/part03/page_0101 为“传入连云港市”。"),
    ("并人连云港市物资贸易中心", "并入连云港市物资贸易中心", "PaddleOCR 中/part02/page_0263 为“并入连云港市物资贸易中心”。"),
    ("被批准迁人连云港市", "被批准迁入连云港市", "PaddleOCR 上/part01/page_0285 为“被批准迁入连云港市”。"),
    ("从省外迁人的占36.1%", "从省外迁入的占36.1%", "PaddleOCR 上/part01/page_0285 为“从省外迁入的占36.1%”。"),
    ("从甘肃迁人连云港市", "从甘肃迁入连云港市", "PaddleOCR 中/part01/page_0235、page_0266 为“从甘肃迁入连云港市”。"),
]


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
    for old, _new, _reason in REPLACEMENTS:
        residuals[old] = 0
        for path in TARGETS:
            if path.exists():
                residuals[old] += path.read_text(encoding="utf-8", errors="ignore").count(old)
    return changes, residuals


def render(changes: list[dict], residuals: dict[str, int]) -> str:
    total = sum(item["count"] for item in changes)
    lines = [
        "# 人入类残留补修 batch319",
        "",
        f"- 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"- 修复总数：{total}",
        "- 范围：当前正式全书/中册/下册 HTML、正式正文汇总及相关分册正文源稿。",
        "- 依据：PaddleOCR 下/part01/page_0184，上/part03/page_0101，上/part01/page_0285，中/part01/page_0235、0266，中/part02/page_0263。",
        "- 原则：只处理完整短语；未处理 OCR 源文件、backup、obsolete、历史交付包。",
        "- 暂缓：`宋军人`、古文诗文与无直接 OCR 证据的 `人/入` 疑点继续保留。",
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
    marker = "## 2026-07-07 人入类残留补修第三百一十九批"
    old = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker in old:
        return
    block = f"""
{marker}

- 依据多页 PaddleOCR 文本，窄语境补修 `人/入` 类残留：`潜人连云港市 -> 潜入连云港市`、`传人连云港市 -> 传入连云港市`、`并人连云港市物资贸易中心 -> 并入连云港市物资贸易中心`、`迁人/迁人的 -> 迁入/迁入的`、`从甘肃迁人连云港市 -> 从甘肃迁入连云港市`，共 {total} 处。
- 报告：`output/reports/enter_residuals_batch319_20260707.md`；进度：`output/reports/progress/20260707_人入类残留补修第三百一十九批.md`。
- `宋军人`、古文诗文与无直接 OCR 证据的 `人/入` 疑点继续保留；未处理 OCR 源文件、backup、obsolete、历史交付包；未打开、展示或嵌入图片。
"""
    MEMORY.write_text(old.rstrip() + "\n\n" + block.strip() + "\n", encoding="utf-8")


def main() -> None:
    changes, residuals = apply_replacements()
    total = sum(item["count"] for item in changes)
    data = {"time": datetime.now().strftime("%Y-%m-%d %H:%M"), "total": total, "changes": changes, "residuals": residuals}
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
