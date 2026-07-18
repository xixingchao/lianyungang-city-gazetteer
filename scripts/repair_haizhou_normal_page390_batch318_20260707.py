# -*- coding: utf-8 -*-
"""Narrow repairs for Haizhou Normal page 0390 and page 0158 leftovers."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "output" / "reports" / "haizhou_normal_page390_batch318_20260707.md"
REPORT_JSON = ROOT / "output" / "reports" / "haizhou_normal_page390_batch318_20260707.json"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260707_海州师范学校页余项补修第三百一十八批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

TARGETS = [
    ROOT / "output" / "final_reader" / "连云港市志_全书.html",
    ROOT / "output" / "final_reader" / "连云港市志_下册.html",
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
    ROOT / "workbench" / "body_chapters" / "第四十三卷至第五十一卷（下part01）.md",
]

REPLACEMENTS = [
    ("军土周威率先攻入城内", "军士周威率先攻入城内", "PaddleOCR 下/part01/page_0158 为“军士周威率先攻入城内”。"),
    ("如杨光、武同儒", "如杨光銮、武同儒", "PaddleOCR 下/part01/page_0390 为“杨光銮、武同儒”。"),
    ("海师桃李满天下，方余名校友", "海师桃李满天下，万余名校友", "PaddleOCR 下/part01/page_0390 为“万余名校友”。"),
    ("顾东石等20多位烈土", "顾东石等20多位烈士", "PaddleOCR 下/part01/page_0390 为“顾东石等20多位烈士”。"),
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
        "# 海州师范学校页余项补修 batch318",
        "",
        f"- 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"- 修复总数：{total}",
        "- 范围：当前正式全书/下册 HTML、正式正文汇总及下册 part01 正文源稿。",
        "- 依据：`workbench/ocr/paddle_ocr/下/part01/page_0390.txt` 与 `workbench/ocr/paddle_ocr/下/part01/page_0158.txt`。",
        "- 原则：只处理海州师范学校页可证实姓名/数量/烈士字形，以及宋金页 `军土周威` 源稿余项；未处理 OCR 源文件、backup、obsolete、历史交付包。",
        "- 暂缓：`宋军人`、古文诗文中的 `已已/竟流/胸顿足` 未取得强证据前不处理。",
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
    marker = "## 2026-07-07 海州师范学校页余项补修第三百一十八批"
    old = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker in old:
        return
    block = f"""
{marker}

- 依据 `workbench/ocr/paddle_ocr/下/part01/page_0390.txt` 与 `page_0158.txt`，窄语境补修海州师范学校页和宋金页余项：`杨光 -> 杨光銮`、`方余名校友 -> 万余名校友`、`烈土 -> 烈士`、`军土周威 -> 军士周威`，共 {total} 处。
- 报告：`output/reports/haizhou_normal_page390_batch318_20260707.md`；进度：`output/reports/progress/20260707_海州师范学校页余项补修第三百一十八批.md`。
- `宋军人`、古文诗文中的 `已已/竟流/胸顿足` 未取得强证据前不处理；未处理 OCR 源文件、backup、obsolete、历史交付包；未打开、展示或嵌入图片。
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
