# -*- coding: utf-8 -*-
"""Narrow repairs for lower volume Song-Jin page 0158 residuals."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "output" / "reports" / "lower_song_jin_page158_batch316_20260707.md"
REPORT_JSON = ROOT / "output" / "reports" / "lower_song_jin_page158_batch316_20260707.json"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260707_下册宋金海州战事页残留补修第三百一十六批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

TARGETS = [
    ROOT / "output" / "final_reader" / "连云港市志_全书.html",
    ROOT / "output" / "final_reader" / "连云港市志_下册.html",
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
    ROOT / "workbench" / "body_chapters" / "第四十三卷至第五十一卷（下part01）.md",
]

REPLACEMENTS = [
    ("海州石漱南", "海州石湫南", "PaddleOCR 下/part01/page_0158 为“海州石湫南”。"),
    ("军土采集野菜", "军士采集野菜", "PaddleOCR 下/part01/page_0158 为“军士采集野菜”。"),
    ("军土周威率先致入城内", "军士周威率先攻入城内", "PaddleOCR 下/part01/page_0158 为“军士周威率先攻入城内”。"),
    ("周威率先致入城内", "周威率先攻入城内", "同页下册/正文源稿保留了缺前缀变体，按 PaddleOCR 改为“攻入城内”。"),
    ("宋车生擒王山", "宋军生擒王山", "PaddleOCR 下/part01/page_0158 为“宋军生擒王山”。"),
    ("文败宋兵", "又败宋兵", "PaddleOCR 下/part01/page_0158 为“又败宋兵”；不补猜前一处断字。"),
    ("助为虐", "助纣为虐", "PaddleOCR 下/part01/page_0158 为“助纣为虐”。"),
    ("巍胜攻取海州后", "魏胜攻取海州后", "PaddleOCR 下/part01/page_0158 为“魏胜攻取海州后”。"),
    ("巍胜在海州北", "魏胜在海州北", "PaddleOCR 下/part01/page_0158 为“魏胜在海州北”。"),
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
        "# 下册宋金海州战事页残留补修 batch316",
        "",
        f"- 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"- 修复总数：{total}",
        "- 范围：当前正式全书/下册 HTML、正式正文汇总及下册 part01 正文源稿。",
        "- 依据：`workbench/ocr/paddle_ocr/下/part01/page_0158.txt`。",
        "- 原则：只处理该页宋金海州战事上下文中可由页级 OCR 直接支持的残字；未补猜 `夜半，宋军 人` 中间缺字。",
        "- 暂缓：其它 `胸山/朐山`、古文诗文和跨页残留未逐页确认前不处理。",
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
    marker = "## 2026-07-07 下册宋金海州战事页残留补修第三百一十六批"
    old = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker in old:
        return
    block = f"""
{marker}

- 依据 `workbench/ocr/paddle_ocr/下/part01/page_0158.txt`，窄语境补修宋金海州战事页残字：`海州石漱南 -> 海州石湫南`、`军土采集野菜 -> 军士采集野菜`、`宋车生擒王山 -> 宋军生擒王山`、`文败宋兵 -> 又败宋兵`、`助为虐 -> 助纣为虐`、`巍胜 -> 魏胜` 等，共 {total} 处。
- 报告：`output/reports/lower_song_jin_page158_batch316_20260707.md`；进度：`output/reports/progress/20260707_下册宋金海州战事页残留补修第三百一十六批.md`。
- `夜半，宋军 人` 中间缺字未由页级 OCR 补出，未作推断；其它 `胸山/朐山`、古文诗文和跨页残留未逐页确认前不处理；未处理 OCR 源文件、backup、obsolete、历史交付包；未打开、展示或嵌入图片。
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
