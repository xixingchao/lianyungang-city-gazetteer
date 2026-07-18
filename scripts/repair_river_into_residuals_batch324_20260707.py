# -*- coding: utf-8 -*-
"""Narrow river 入/蔷薇河 residual repairs backed by page OCR."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "output" / "reports" / "river_into_residuals_batch324_20260707.md"
REPORT_JSON = ROOT / "output" / "reports" / "river_into_residuals_batch324_20260707.json"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260707_河道入流残留补修第三百二十四批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

TARGETS = [
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
    ROOT / "workbench" / "body_chapters" / "连云港市志_上册_正文汇总.md",
    ROOT / "workbench" / "body_chapters" / "第十七卷至第二十九卷（中part01）.md",
    ROOT / "workbench" / "body_chapters" / "第三十卷至第四十二卷（中part02）.md",
]

REPLACEMENTS = [
    ("人蕃薇河", "入蔷薇河", "PaddleOCR 上/part01/page_0169 与上/part03/page_0050 为“入蔷薇河”。"),
    ("人薇河", "入蔷薇河", "PaddleOCR 上/part01/page_0169 为“入蔷薇河”。"),
    ("人临洪河", "入临洪河", "PaddleOCR 上/part01/page_0169 为“入临洪河”。"),
    ("汇人蕃薇河", "汇入蔷薇河", "PaddleOCR 中/part02/page_0046 为“汇入蔷薇河”语境；同段淮沭新河入蔷薇河。"),
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
        "# 河道入流残留补修 batch324",
        "",
        f"- 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"- 修复总数：{total}",
        "- 范围：正式正文汇总、上册正文汇总和相关中册分册源稿。",
        "- 依据：PaddleOCR 上/part01/page_0169、上/part03/page_0050、中/part02/page_0046。",
        "- 原则：只处理完整河道入流短语；未处理 OCR 源文件、backup、obsolete、历史交付包。",
        "- 暂缓：普通 `人海` 残留语境复杂，本批不作全局处理。",
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
    marker = "## 2026-07-07 河道入流残留补修第三百二十四批"
    old = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker in old:
        return
    block = f"""
{marker}

- 依据 PaddleOCR 上/part01/page_0169、上/part03/page_0050、中/part02/page_0046，窄语境补修河道入流残留：`人蕃薇河/人薇河 -> 入蔷薇河`、`人临洪河 -> 入临洪河`、`汇人蕃薇河 -> 汇入蔷薇河`，共 {total} 处。
- 报告：`output/reports/river_into_residuals_batch324_20260707.md`；进度：`output/reports/progress/20260707_河道入流残留补修第三百二十四批.md`。
- 普通 `人海` 残留语境复杂，本批不作全局处理；未处理 OCR 源文件、backup、obsolete、历史交付包；未打开、展示或嵌入图片。
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
