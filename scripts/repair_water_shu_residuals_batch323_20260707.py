# -*- coding: utf-8 -*-
"""Narrow 水利章 沭/入 residual repairs backed by page OCR."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "output" / "reports" / "water_shu_residuals_batch323_20260707.md"
REPORT_JSON = ROOT / "output" / "reports" / "water_shu_residuals_batch323_20260707.json"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260707_水利沭字残留补修第三百二十三批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

TARGETS = [
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
]

REPLACEMENTS = [
    ("江淮沐水", "江淮沭水", "PaddleOCR 上/part03/page_0049、0050 为“江淮沭水”。"),
    ("江淮述水", "江淮沭水", "PaddleOCR 上/part03/page_0049、0050 为“江淮沭水”。"),
    ("江准述水", "江淮沭水", "PaddleOCR 上/part03/page_0049 为“江淮沭水”。"),
    ("准述新河", "淮沭新河", "PaddleOCR 上/part03/page_0049、0050、0051 为“淮沭新河”。"),
    ("述新河", "沭新河", "PaddleOCR 上/part03/page_0050、0051 为“沭新河”。"),
    ("述新渠", "沭新渠", "PaddleOCR 上/part03/page_0050、0051 为“沭新渠”。"),
    ("述北引河", "沭北引河", "PaddleOCR 上/part03/page_0049、0050 为“沭北引河”。"),
    ("沐新河", "沭新河", "PaddleOCR 上/part03/page_0050、0051 为“沭新河”。"),
    ("沐新渠", "沭新渠", "PaddleOCR 上/part03/page_0050、0051 为“沭新渠”。"),
    ("沐新进水闸", "沭新进水闸", "PaddleOCR 上/part03/page_0050 为“沭新进水闸”。"),
    ("沐新退水闸", "沭新退水闸", "PaddleOCR 上/part03/page_0050 为“沭新退水闸”。"),
    ("沐北引河", "沭北引河", "PaddleOCR 上/part03/page_0050 为“沭北引河”。"),
    ("沐阳南偏泓", "沭阳南偏泓", "PaddleOCR 上/part03/page_0050 为“沭阳南偏泓”。"),
    ("述南航道", "沭南航道", "PaddleOCR 上/part03/page_0050 为“沭南航道”。"),
    ("调引述水", "调引沭水", "PaddleOCR 上/part03/page_0050 为“调引沭水”。"),
    ("调引准水", "调引淮水", "PaddleOCR 上/part03/page_0051 为“调引淮水”。"),
    ("人述新", "入沭新", "PaddleOCR 上/part03/page_0050 为“入沭新”。"),
    ("人沐新", "入沭新", "PaddleOCR 上/part03/page_0050 为“入沭新”。"),
    ("人蕃薇河", "入蔷薇河", "PaddleOCR 上/part03/page_0050 为“入蔷薇河”。"),
    ("人新沂", "入新沂", "PaddleOCR 上/part03/page_0050 为“入新沂”。"),
    ("人盐河", "入盐河", "PaddleOCR 上/part03/page_0050 为“入盐河”。"),
    ("人石梁河", "入石梁河", "PaddleOCR 上/part03/page_0050、0053 为“入石梁河”。"),
    ("人古城渠", "入古城渠", "PaddleOCR 上/part03/page_0050 为“入古城渠”。"),
    ("人小塔山", "入小塔山", "PaddleOCR 上/part03/page_0050 为“入小塔山”。"),
    ("人龙梁河", "入龙梁河", "PaddleOCR 上/part03/page_0050、0053 为“入龙梁河”。"),
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
        "# 水利沭字残留补修 batch323",
        "",
        f"- 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"- 修复总数：{total}",
        "- 范围：`workbench/body_chapters/连云港市志_全书_正文汇总.md`。",
        "- 依据：PaddleOCR 上/part03/page_0049、0050、0051、0053。",
        "- 原则：只处理水利章完整专名或固定短语；未处理 OCR 源文件、backup、obsolete、历史交付包。",
        "- 暂缓：`述阳` 等跨章节地名残留未在本批全局处理，需按页继续核对。",
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
    marker = "## 2026-07-07 水利沭字残留补修第三百二十三批"
    old = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker in old:
        return
    block = f"""
{marker}

- 依据 PaddleOCR 上/part03/page_0049、0050、0051、0053，窄语境补修全书正文汇总水利章 `沭/入` 残留：`江淮沐水/江淮述水/江准述水 -> 江淮沭水`、`述新河/沐新河 -> 沭新河`、`述新渠/沐新渠 -> 沭新渠`、`述北引河/沐北引河 -> 沭北引河` 及同段 `人... -> 入...` 固定短语，共 {total} 处。
- 报告：`output/reports/water_shu_residuals_batch323_20260707.md`；进度：`output/reports/progress/20260707_水利沭字残留补修第三百二十三批.md`。
- `述阳` 等跨章节地名残留留待按页继续核对；未处理 OCR 源文件、backup、obsolete、历史交付包；未打开、展示或嵌入图片。
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
