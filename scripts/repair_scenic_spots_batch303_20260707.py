# -*- coding: utf-8 -*-
"""Narrow page-OCR-backed repairs for the scenic spots chapter."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "output" / "reports" / "scenic_spots_batch303_20260707.md"
REPORT_JSON = ROOT / "output" / "reports" / "scenic_spots_batch303_20260707.json"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260707_风景名胜飞泉鸡鸣山页级OCR补修第三百零三批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

TARGETS = [
    ROOT / "output" / "final_reader" / "连云港市志_全书.html",
    ROOT / "output" / "final_reader" / "连云港市志_中册.html",
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
    ROOT / "workbench" / "body_chapters" / "第三十卷至第四十二卷（中part02）.md",
]

REPLACEMENTS = [
    ("今已妃，但鸡鸣石", "今已圮，但鸡鸣石", "PaddleOCR 中/part02/page_0097 为“今已圮”。"),
    ("诗日：“山不高兮水不深", "诗曰：“山不高兮水不深", "PaddleOCR 中/part02/page_0097 为“诗曰”。"),
    ("泉水于山石间迁回曲折", "泉水于山石间迂回曲折", "PaddleOCR 中/part02/page_0097 为“迂回曲折”。"),
    ("飞泉原名灌缨泉", "飞泉原名濯缨泉", "PaddleOCR 中/part02/page_0097 为“飞泉原名濯缨泉”。"),
    ("下有灌缨泉", "下有濯缨泉", "PaddleOCR 中/part02/page_0097 为“下有濯缨泉”。"),
    ("右曼卿飞泉诗", "石曼卿飞泉诗", "PaddleOCR 中/part02/page_0097 为“石曼卿飞泉诗”。"),
    ("诗日：“上狮", "诗曰：“上蹲狮", "PaddleOCR 中/part02/page_0097 为“诗曰：‘上蹲狮子石’”。"),
    ("上狮\n子石", "上蹲狮\n子石", "PaddleOCR 中/part02/page_0097 为“上蹲狮子石”。"),
    ("冠弃斯冷然", "冠弁斯泠然", "PaddleOCR 中/part02/page_0097 为“冠弁斯泠然”。"),
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
        "# 风景名胜飞泉鸡鸣山页级 OCR 补修 batch303",
        "",
        f"- 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"- 修复总数：{total}",
        "- 范围：当前正式全书 HTML、正式中册 HTML、正式正文汇总及中册 part02 正文源稿。",
        "- 依据：`workbench/ocr/paddle_ocr/中/part02/page_0097.txt`。",
        "- 原则：只处理飞泉/飞泉石刻/鸡鸣山同页 OCR 明确支持的窄短语；不处理全书其它 `诗日` 等高频疑点。",
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
    marker = "## 2026-07-07 风景名胜飞泉鸡鸣山页级OCR补修第三百零三批"
    old = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker in old:
        return
    block = f"""
{marker}

- 依据 `workbench/ocr/paddle_ocr/中/part02/page_0097.txt`，窄语境补修风景名胜飞泉/鸡鸣山页：`妃 -> 圮`、`诗日 -> 诗曰`、`迁回 -> 迂回`、`灌缨泉 -> 濯缨泉`、`右曼卿 -> 石曼卿`、`上狮子石 -> 上蹲狮子石`、`冠弃斯冷然 -> 冠弁斯泠然`，共 {total} 处。
- 报告：`output/reports/scenic_spots_batch303_20260707.md`；进度：`output/reports/progress/20260707_风景名胜飞泉鸡鸣山页级OCR补修第三百零三批.md`。
- 未全局处理其它 `诗日`；未处理 OCR 源文件、backup、obsolete、历史交付包；未打开、展示或嵌入图片。
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
