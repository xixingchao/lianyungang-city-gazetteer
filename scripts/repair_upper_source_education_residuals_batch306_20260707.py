# -*- coding: utf-8 -*-
"""Upper source education residual repairs backed by PaddleOCR."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "output" / "reports" / "upper_source_education_residuals_batch306_20260707.md"
REPORT_JSON = ROOT / "output" / "reports" / "upper_source_education_residuals_batch306_20260707.json"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260707_上册正文教育残留补修第三百零六批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

TARGETS = [
    ROOT / "workbench" / "body_chapters" / "连云港市志_上册_正文汇总.md",
]

REPLACEMENTS = [
    ("29.5方平方米", "29.5万平方米", "PaddleOCR 上/part01/page_0237 为“29.5万平方米”。"),
    ("解\n放前岁", "解\n放前夕", "PaddleOCR 上/part01/page_0247 为“解放前夕”。"),
    ("人学率", "入学率", "PaddleOCR 上/part01/page_0237/page_0247/page_0248/page_0253 等为“入学率”。"),
    ("人园儿童5125人", "入园儿童5125人", "PaddleOCR 上/part01/page_0247 为“入园儿童5125人”。"),
    ("人园幼儿3877人", "入园幼儿3877人", "PaddleOCR 上/part01/page_0253 为“入园幼儿3877人”。"),
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
        "# 上册正文教育残留补修 batch306",
        "",
        f"- 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"- 修复总数：{total}",
        "- 范围：上册正文汇总源稿。",
        "- 依据：`workbench/ocr/paddle_ocr/上/part01/page_0237.txt`、`page_0247.txt`、`page_0248.txt`、`page_0253.txt`。",
        "- 原则：只同步页级 OCR 明确支持的教育段源稿残留；未处理 OCR 源文件、backup、obsolete、历史交付包。",
        "- 暂缓：`人学10630人` 未找到足够页级 OCR 证据，未作推断替换。",
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
    marker = "## 2026-07-07 上册正文教育残留补修第三百零六批"
    old = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker in old:
        return
    block = f"""
{marker}

- 依据 `workbench/ocr/paddle_ocr/上/part01/page_0237.txt`、`page_0247.txt`、`page_0248.txt`、`page_0253.txt`，同步补修上册正文汇总教育段残留：`29.5方平方米 -> 29.5万平方米`、`解放前岁 -> 解放前夕`、`人学率 -> 入学率`、`人园儿童/幼儿 -> 入园儿童/幼儿`，共 {total} 处。
- 报告：`output/reports/upper_source_education_residuals_batch306_20260707.md`；进度：`output/reports/progress/20260707_上册正文教育残留补修第三百零六批.md`。
- `人学10630人` 未找到足够页级 OCR 证据，未作推断替换；未处理 OCR 源文件、backup、obsolete、历史交付包；未打开、展示或嵌入图片。
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
