# -*- coding: utf-8 -*-
"""Repair a fifth source-backed 馀->余 batch in the final reader."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "final_reader_yu_paddle_backed_batch5_20260704.json"
REPORT_MD = ROOT / "output" / "reports" / "final_reader_yu_paddle_backed_batch5_20260704.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260704_最终阅读版余字第五批回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    {
        "label": "各类业余教育",
        "old": "发展各类业馀教育，提高人民群众科学文化水平",
        "new": "发展各类业余教育，提高人民群众科学文化水平",
        "source": "workbench/ocr/raw/上/part01/page_0104.txt:26; workbench/ocr/paddle_ocr/上/part01/page_0104.txt:26; workbench/body_chapters/连云港市志_全书_正文汇总.md:4323",
    },
    {
        "label": "新浦区职工业余学校",
        "old": "1982年新浦区职工业馀学校创立。",
        "new": "1982年新浦区职工业余学校创立。",
        "source": "workbench/ocr/raw/上/part01/page_0237.txt:16; workbench/ocr/paddle_ocr/上/part01/page_0237.txt:17; workbench/body_chapters/连云港市志_全书_正文汇总.md:13200",
    },
    {
        "label": "体操表演300余人",
        "old": "有5个代表队、300馀人表演团体操、童子军操。",
        "new": "有5个代表队、300余人表演团体操、童子军操。",
        "source": "workbench/ocr/raw/上/part01/page_0262.txt:15; workbench/ocr/paddle_ocr/上/part01/page_0262.txt:15; workbench/body_chapters/连云港市志_全书_正文汇总.md:14076",
    },
    {
        "label": "乒乓球业余训练队",
        "old": "成立县篮球队和乒乓球业馀训练队。",
        "new": "成立县篮球队和乒乓球业余训练队。",
        "source": "workbench/ocr/raw/上/part01/page_0262.txt:18; workbench/ocr/paddle_ocr/上/part01/page_0262.txt:18; workbench/body_chapters/连云港市志_全书_正文汇总.md:14079",
    },
]


def append_once(path: Path, marker: str, content: str) -> None:
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker not in old:
        path.write_text(old.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")


def main() -> None:
    text = TARGET.read_text(encoding="utf-8")
    items = []
    for item in REPLACEMENTS:
        count = text.count(item["old"])
        if count:
            text = text.replace(item["old"], item["new"])
        items.append({**item, "count": count})
    TARGET.write_text(text, encoding="utf-8")

    verify = TARGET.read_text(encoding="utf-8")
    residuals = [item["old"] for item in REPLACEMENTS if item["old"] in verify]
    if residuals:
        raise RuntimeError(f"replacement verification failed: {residuals}")

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    total = sum(item["count"] for item in items)
    payload = {
        "time": now,
        "scope": "最终阅读版余字第五批回源修复",
        "target": str(TARGET),
        "total_replacements": total,
        "items": items,
        "principle": "仅修复最终阅读版与正文汇总不一致，且 raw OCR 与 PaddleOCR 同句闭合为 `余` 的业余/数量词残留。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 最终阅读版余字第五批回源修复",
        "",
        f"- 时间：{now}",
        "- 原则：最终阅读版旧字、正文汇总已为 `余`，且 raw OCR/PaddleOCR 同句闭合后才修。",
        f"- 目标：`{TARGET}`",
        f"- 本次替换：{total} 处。",
        "- 暂缓：同页 `有校舍10馀间` 尚未取得直接源证据闭合。",
        "",
        "## 明细",
    ]
    for item in items:
        if item["count"]:
            lines.append(f"- {item['label']}：{item['count']} 处；依据 `{item['source']}`。")
    lines.append("")
    content = "\n".join(lines)
    REPORT_MD.write_text(content, encoding="utf-8")
    PROGRESS.write_text(content, encoding="utf-8")

    marker = "## 2026-07-04 最终阅读版余字第五批回源修复"
    memory = f"""
{marker}
- 依据正文汇总、raw OCR 与 PaddleOCR 同句闭合，修复最终阅读版 `馀 -> 余` 第五批残留，共 {total} 处。
- 本批覆盖 `业余教育`、`职工业余学校`、赣榆体育段 `300余人表演` 和 `乒乓球业余训练队`。
- 暂缓同页 `有校舍10馀间`，因本轮未取得直接源证据闭合。
- 报告：`output/reports/final_reader_yu_paddle_backed_batch5_20260704.md`。
"""
    append_once(MEMORY, marker, memory)
    print(json.dumps({"total_replacements": total, "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
