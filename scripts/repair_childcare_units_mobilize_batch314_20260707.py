# -*- coding: utf-8 -*-
"""Narrow childcare, unit, and mobilization residual repairs."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "output" / "reports" / "childcare_units_mobilize_batch314_20260707.md"
REPORT_JSON = ROOT / "output" / "reports" / "childcare_units_mobilize_batch314_20260707.json"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260707_托幼单位动员残留补修第三百一十四批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

TARGETS = [
    ROOT / "output" / "final_reader" / "连云港市志_全书.html",
    ROOT / "output" / "final_reader" / "连云港市志_中册.html",
    ROOT / "output" / "final_reader" / "连云港市志_下册.html",
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
    ROOT / "workbench" / "body_chapters" / "连云港市志_上册_正文汇总.md",
    ROOT / "workbench" / "body_chapters" / "第十七卷至第二十九卷（中part01）.md",
    ROOT / "workbench" / "body_chapters" / "第三十卷至第四十二卷（中part02）.md",
    ROOT / "workbench" / "body_chapters" / "第五十二卷至第六十卷及附录（下part02）.md",
]

REPLACEMENTS = [
    ("儿童人托", "儿童入托", "PaddleOCR 下/part02/page_0204 为“儿童入托”。"),
    ("人托率", "入托率", "PaddleOCR 下/part02/page_0204 为“入托率”。"),
    ("超生女子人托费", "超生女子入托费", "托幼语境，PaddleOCR 上/part01/page_0296 同段为“优先入托”。"),
    ("优先人托", "优先入托", "PaddleOCR 上/part01/page_0296 为“优先入托”。"),
    ("每公厅1.1元", "每公斤1.1元", "PaddleOCR 中/part01/page_0109 为“每公斤1.1元”。"),
    ("东海县政府动员工9.7万人", "东海县政府动员9.7万人", "正式全书同段已为“动员9.7万人”，上下文为动员群众修路；页级 OCR 同误作“动员工”。"),
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
        "# 托幼单位动员残留补修 batch314",
        "",
        f"- 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"- 修复总数：{total}",
        "- 范围：当前正式全书/中册/下册 HTML、正式正文汇总及对应分册正文源稿。",
        "- 依据：PaddleOCR 下/part02/page_0204、上/part01/page_0296、中/part01/page_0109；`动员工9.7万人` 依据正式全书同段对照和动员群众修路语境。",
        "- 原则：只处理托幼、单位、动员修路窄短语；未处理 OCR 源文件、backup、obsolete、历史交付包。",
        "- 暂缓：古文/诗文中的 `自已`、`已已`、`竟流` 未逐页校勘前不处理。",
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
    marker = "## 2026-07-07 托幼单位动员残留补修第三百一十四批"
    old = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker in old:
        return
    block = f"""
{marker}

- 依据 PaddleOCR 页级文本和正式全书同段对照，窄语境补修托幼、单位和动员修路残留：`儿童人托/人托率/优先人托 -> 儿童入托/入托率/优先入托`、`每公厅1.1元 -> 每公斤1.1元`、`东海县政府动员工9.7万人 -> 东海县政府动员9.7万人`，共 {total} 处。
- 报告：`output/reports/childcare_units_mobilize_batch314_20260707.md`；进度：`output/reports/progress/20260707_托幼单位动员残留补修第三百一十四批.md`。
- 古文/诗文中的 `自已`、`已已`、`竟流` 未逐页校勘前不处理；未处理 OCR 源文件、backup、obsolete、历史交付包；未打开、展示或嵌入图片。
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
