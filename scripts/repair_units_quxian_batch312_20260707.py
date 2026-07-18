# -*- coding: utf-8 -*-
"""Narrow OCR-backed unit and 朐县 residual repairs."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "output" / "reports" / "units_quxian_batch312_20260707.md"
REPORT_JSON = ROOT / "output" / "reports" / "units_quxian_batch312_20260707.json"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260707_单位与朐县残留补修第三百一十二批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

TARGETS = [
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
    ROOT / "workbench" / "body_chapters" / "连云港市志_上册_正文汇总.md",
    ROOT / "workbench" / "body_chapters" / "第十七卷至第二十九卷（中part01）.md",
    ROOT / "workbench" / "body_chapters" / "第四十三卷至第五十一卷（下part01）.md",
]

REPLACEMENTS = [
    ("道路清扫面积93方平方米", "道路清扫面积93万平方米", "PaddleOCR 上/part02/page_0075 为“道路清扫面积93万平方米”。"),
    ("苗圃1.6方平方米", "苗圃1.6万平方米", "PaddleOCR 上/part02/page_0085 为“苗圃1.6万平方米”。"),
    ("生产绿地38方平方米", "生产绿地38万平方米", "PaddleOCR 上/part02/page_0085 为“生产绿地38万平方米”。"),
    ("占地面积2方平方米", "占地面积2万平方米", "PaddleOCR 中/part01/page_0067 为“占地面积2万平方米”。"),
    ("建筑面积1.03方平方米", "建筑面积1.03万平方米", "PaddleOCR 下/part01/page_0393 为“建筑面积1.03万平方米”。"),
    ("建筑面积0.2方平方米", "建筑面积0.2万平方米", "PaddleOCR 上/part03/page_0225 为“建筑面积0.2万平方米”。"),
    ("装机2台套190干瓦", "装机2台套190千瓦", "PaddleOCR 上/part03/page_0032 为“装机2台套190千瓦”。"),
    ("人园幼儿116800人", "入园幼儿116800人", "PaddleOCR 下/part01/page_0336 为“入园幼儿116800人”。"),
    ("秦为胸县", "秦为朐县", "PaddleOCR 上/part01/page_0033 为“秦为朐县”。"),
    ("汉东海胸县关里", "汉东海朐县关里", "PaddleOCR 下/part02/page_0343 为“汉东海朐县关里”。"),
    ("立石胸界以为秦东门阙", "立石朐界以为秦东门阙", "PaddleOCR 上/part01/page_0032 为“立石朐界以为秦东门阙”。"),
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
        "# 单位与朐县残留补修 batch312",
        "",
        f"- 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"- 修复总数：{total}",
        "- 范围：正文汇总源稿及对应分册正文源稿。",
        "- 依据：PaddleOCR 上/part01/page_0032/page_0033、上/part02/page_0075/page_0085、上/part03/page_0032/page_0225、中/part01/page_0067、下/part01/page_0336/page_0393、下/part02/page_0343。",
        "- 原则：只处理页级 OCR 明确支持的窄短语；未处理 OCR 源文件、backup、obsolete、历史交付包。",
        "- 暂缓：`胸卤之盐` 页级 OCR 也为该字形，未作推断替换；其它 `胸/朐` 残留未逐页确认不处理。",
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
    marker = "## 2026-07-07 单位与朐县残留补修第三百一十二批"
    old = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker in old:
        return
    block = f"""
{marker}

- 依据 PaddleOCR 页级文本，窄语境补修单位、幼教与朐县相关源稿残留：`方平方米 -> 万平方米`、`干瓦 -> 千瓦`、`人园幼儿116800人 -> 入园幼儿116800人`、`秦为胸县/汉东海胸县关里/立石胸界 -> 秦为朐县/汉东海朐县关里/立石朐界`，共 {total} 处。
- 报告：`output/reports/units_quxian_batch312_20260707.md`；进度：`output/reports/progress/20260707_单位与朐县残留补修第三百一十二批.md`。
- `胸卤之盐` 页级 OCR 也为该字形，未作推断替换；其它 `胸/朐` 残留未逐页确认不处理；未处理 OCR 源文件、backup、obsolete、历史交付包；未打开、展示或嵌入图片。
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
