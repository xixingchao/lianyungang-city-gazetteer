# -*- coding: utf-8 -*-
"""Tiny source residual repairs backed by PaddleOCR."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "output" / "reports" / "source_residuals_batch305_20260707.md"
REPORT_JSON = ROOT / "output" / "reports" / "source_residuals_batch305_20260707.json"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260707_正文源稿残留补修第三百零五批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

TARGETS = [
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
    ROOT / "workbench" / "body_chapters" / "连云港市志_上册_正文汇总.md",
]

REPLACEMENTS = [
    ("市境相继论陷", "市境相继沦陷", "PaddleOCR 上/part01/page_0215 为“市境相继沦陷”。"),
    ("狮子崖有灌缨泉", "狮子崖有濯缨泉", "PaddleOCR 上/part01/page_0139 为“狮子崖有濯缨泉”。"),
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
        "# 正文源稿残留补修 batch305",
        "",
        f"- 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"- 修复总数：{total}",
        "- 范围：正文源稿汇总与上册正文汇总。",
        "- 依据：`workbench/ocr/paddle_ocr/上/part01/page_0215.txt`、`workbench/ocr/paddle_ocr/上/part01/page_0139.txt`。",
        "- 原则：只同步正式 reader 已正确、且页级 OCR 明确支持的源稿残留；未处理 OCR 源文件、backup、obsolete、历史交付包。",
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
    marker = "## 2026-07-07 正文源稿残留补修第三百零五批"
    old = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker in old:
        return
    block = f"""
{marker}

- 依据 `workbench/ocr/paddle_ocr/上/part01/page_0215.txt` 与 `workbench/ocr/paddle_ocr/上/part01/page_0139.txt`，同步补修正文源稿残留：`市境相继论陷 -> 市境相继沦陷`、`狮子崖有灌缨泉 -> 狮子崖有濯缨泉`，共 {total} 处。
- 报告：`output/reports/source_residuals_batch305_20260707.md`；进度：`output/reports/progress/20260707_正文源稿残留补修第三百零五批.md`。
- 未处理 `入口门廊迁回曲折`，因页级 OCR 也读作该字形；未处理 OCR 源文件、backup、obsolete、历史交付包；未打开、展示或嵌入图片。
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
