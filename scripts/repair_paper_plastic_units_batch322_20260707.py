# -*- coding: utf-8 -*-
"""Narrow paper and plastic unit residual repairs backed by page OCR."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "output" / "reports" / "paper_plastic_units_batch322_20260707.md"
REPORT_JSON = ROOT / "output" / "reports" / "paper_plastic_units_batch322_20260707.json"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260707_造纸塑料单位残留补修第三百二十二批.md"
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
    ROOT / "workbench" / "body_chapters" / "第五十二卷至第六十卷及附录（下part02）.md",
]

REPLACEMENTS = [
    ("盒装面币纸折叠机", "盒装面巾纸折叠机", "PaddleOCR 上/part03/page_0175 为“盒装面巾纸折叠机”。"),
    ("餐巾纸和面币纸", "餐巾纸和面巾纸", "PaddleOCR 上/part03/page_0176 为“餐巾纸和面巾纸”。"),
    ("市塑料四广为配合连云港碱厂生产", "市塑料四厂为配合连云港碱厂生产", "PaddleOCR 上/part03/page_0285 为“市塑料四厂为配合连云港碱厂生产”。"),
    ("投\n力增至1500方条", "产品年产能\n力增至1500万条", "PaddleOCR 上/part03/page_0285 为“产品年产能力增至1500万条”。"),
    ("年产能力为2870方条", "年产能力为2870万条", "PaddleOCR 上/part03/page_0285 为“年产能力为2870万条”。"),
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
        "# 造纸塑料单位残留补修 batch322",
        "",
        f"- 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"- 修复总数：{total}",
        "- 范围：当前正式全书/中册/下册 HTML、正式正文汇总及相关分册正文源稿。",
        "- 依据：PaddleOCR 上/part03/page_0175、0176、0285。",
        "- 原则：只处理完整短语；未处理 OCR 源文件、backup、obsolete、历史交付包。",
        "- 图片处理：未打开、展示或嵌入图片。",
        "",
        "## 替换明细",
    ]
    for item in changes:
        old = item["old"].replace("\n", "\\n")
        new = item["new"].replace("\n", "\\n")
        lines.append(f"- `{item['path']}`：`{old}` -> `{new}`；次数 {item['count']}；依据：{item['reason']}")
    lines.extend(["", "## 残留计数", ""])
    bad = {key.replace("\n", "\\n"): value for key, value in residuals.items() if value}
    if not bad:
        lines.append("- 本批检查短语在当前检查范围中均为 0。")
    else:
        for key, value in bad.items():
            lines.append(f"- `{key}`：{value}")
    return "\n".join(lines) + "\n"


def append_memory(total: int) -> None:
    marker = "## 2026-07-07 造纸塑料单位残留补修第三百二十二批"
    old = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker in old:
        return
    block = f"""
{marker}

- 依据 PaddleOCR 上/part03/page_0175、0176、0285，窄语境补修造纸与塑料袋段源稿残留：`面币纸 -> 面巾纸`、`市塑料四广 -> 市塑料四厂`、`1500方条/2870方条 -> 1500万条/2870万条`，共 {total} 处。
- 报告：`output/reports/paper_plastic_units_batch322_20260707.md`；进度：`output/reports/progress/20260707_造纸塑料单位残留补修第三百二十二批.md`。
- 未处理 OCR 源文件、backup、obsolete、历史交付包；未打开、展示或嵌入图片。
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
