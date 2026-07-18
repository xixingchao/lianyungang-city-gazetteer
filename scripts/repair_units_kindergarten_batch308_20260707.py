# -*- coding: utf-8 -*-
"""Narrow OCR-backed unit and kindergarten residual repairs."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "output" / "reports" / "units_kindergarten_batch308_20260707.md"
REPORT_JSON = ROOT / "output" / "reports" / "units_kindergarten_batch308_20260707.json"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260707_单位与入园残留补修第三百零八批.md"
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
    ("赣愉县征收公粮182.97万公斤", "赣榆县征收公粮182.97万公斤", "PaddleOCR 中/part02/page_0286 为“赣榆县征收公粮182.97万公斤”。"),
    ("民国31年征收600万公厅", "民国31年征收600万公斤", "PaddleOCR 中/part02/page_0286 为“民国31年征收600万公斤”。"),
    ("0.79亿公厅", "0.79亿公斤", "PaddleOCR 上/part01/page_0071 为“0.79亿公斤”。"),
    ("250公厅芦笋良种", "250公斤芦笋良种", "PaddleOCR 中/part01/page_0078 为“250公斤芦笋良种”。"),
    ("板栗种子350公厅", "板栗种子350公斤", "PaddleOCR 中/part02/page_0165 为“板栗种子350公斤”。"),
    ("重5.1公厅", "重5.1公斤", "PaddleOCR 下/part02/page_0117 为“重5.1公斤”。"),
    ("7.5干瓦电动警报器", "7.5千瓦电动警报器", "PaddleOCR 下/part01/page_0189 为“7.5千瓦电动警报器”。"),
    ("农机动力26.92干瓦", "农机动力26.92千瓦", "PaddleOCR 上/part01/page_0265 为“农机动力26.92千瓦”。"),
    ("人园幼儿27397人", "入园幼儿27397人", "PaddleOCR 上/part01/page_0261 与下/part01/page_0336 为“入园幼儿27397人”。"),
    ("人园幼儿1187人", "入园幼儿1187人", "PaddleOCR 上/part01/page_0261 为“入园幼儿1187人”。"),
    ("人园幼儿30971人", "入园幼儿30971人", "PaddleOCR 下/part01/page_0336 为“入园幼儿30971人”。"),
    ("人园儿童 35970人", "入园儿童 35970人", "PaddleOCR 上/part01/page_0261 为“入园儿童 35970人”。"),
    ("人园率75.2", "入园率75.2", "PaddleOCR 上/part01/page_0261 为“入园率75.2%”。"),
    ("入园人托儿童6420人", "入园入托儿童6420人", "PaddleOCR 下/part01/page_0336 为“入园入托儿童6420人”。"),
    ("入园人托。", "入园入托。", "PaddleOCR 下/part01/page_0336 为“入园入托”。"),
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
        "# 单位与入园残留补修 batch308",
        "",
        f"- 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"- 修复总数：{total}",
        "- 范围：当前正式全书/中册/下册 HTML、正式正文汇总及对应分册正文源稿。",
        "- 依据：PaddleOCR 上/part01/page_0071/page_0261/page_0265，中/part01/page_0078，中/part02/page_0165/page_0286，下/part01/page_0189/page_0336，下/part02/page_0117。",
        "- 原则：只处理页级 OCR 明确支持的窄短语；未处理 OCR 源文件、backup、obsolete、历史交付包。",
        "- 暂缓：`准北盐` 等大范围历史专名疑点未回源前不处理；`人学10630人` 未找到足够页级 OCR 证据，未作推断替换。",
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
    marker = "## 2026-07-07 单位与入园残留补修第三百零八批"
    old = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker in old:
        return
    block = f"""
{marker}

- 依据 PaddleOCR 页级文本，窄语境补修单位与幼教段残留：`赣愉县 -> 赣榆县`、`公厅 -> 公斤`、`干瓦 -> 千瓦`、`人园/入园人托 -> 入园/入园入托` 等，共 {total} 处。
- 报告：`output/reports/units_kindergarten_batch308_20260707.md`；进度：`output/reports/progress/20260707_单位与入园残留补修第三百零八批.md`。
- `准北盐` 等大范围历史专名疑点未回源前不处理；`人学10630人` 未找到足够页级 OCR 证据，未作推断替换；未处理 OCR 源文件、backup、obsolete、历史交付包；未打开、展示或嵌入图片。
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
