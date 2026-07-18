# -*- coding: utf-8 -*-
"""Repair source-checked 收人 -> 收入 OCR slips in final reader."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_shouru_residual_20260704.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_shouru_residual_20260704.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260704_收人收入残留回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SOURCE = (
    "workbench/ocr/paddle_ocr/中/part02/page_0281.txt:30-39; page_0282.txt:20-35; "
    "page_0306.txt:35; page_0334.txt:39-40; page_0336.txt:22-25; "
    "workbench/ocr/merged/连云港市志_中_part02_OCR汇总.md:34986-34987; "
    "workbench/ocr/paddle_ocr/下/part01/page_0411.txt:13-14"
)

REPLACEMENTS = [
    ("财政按收入项目划分", "主要是按收人项目划分", "主要是按收入项目划分", "中/part02/page_0281.txt:30-31"),
    ("公用企业收入", "公用企业收人、文教卫生企业收入", "公用企业收入、文教卫生企业收入", "中/part02/page_0281.txt:37-39"),
    ("中央预算收入盐税", "中央预算收人的盐税", "中央预算收入的盐税", "中/part02/page_0282.txt:20-22"),
    ("企业收入超收分成", "盐税15%，企业收人、工商各税", "盐税15%，企业收入、工商各税", "中/part02/page_0282.txt:34-35"),
    ("收入基数单项承包", "由省确定收人基数", "由省确定收入基数", "中/part02/财政收入同段源文"),
    ("预算内收入占比", "预算内收人23%", "预算内收入23%", "中/part02/page_0306.txt:35"),
    ("组织收入计划", "组织收人计划", "组织收入计划", "中/part02/page_0334.txt:39-40"),
    ("公共事业收入", "公共事业的收人，农业生产合作社", "公共事业的收入，农业生产合作社", "中/part02/page_0336.txt:22-24"),
    ("农民纯收入", "农民年人均纯收人814元", "农民年人均纯收入814元", "中_part02_OCR汇总.md:34986-34987"),
    ("教育经费年收入", "田赋附加亩捐年收人约2万元", "田赋附加亩捐年收入约2万元", "下/part01/page_0411.txt:13-14"),
]


def patch_reader() -> dict[str, int]:
    text = HTML.read_text(encoding="utf-8")
    counts: dict[str, int] = {}
    for label, old, new, _source in REPLACEMENTS:
        count = text.count(old)
        if count:
            text = text.replace(old, new)
        elif new not in text:
            raise RuntimeError(f"neither old nor new text found: {label}")
        counts[label] = count
    HTML.write_text(text, encoding="utf-8")
    verify_reader()
    return counts


def verify_reader() -> None:
    text = HTML.read_text(encoding="utf-8")
    missing = [new for _label, _old, new, _source in REPLACEMENTS if new not in text]
    residuals = [old for _label, old, _new, _source in REPLACEMENTS if old in text]
    if missing or residuals:
        raise RuntimeError(f"verification failed: missing={missing}, residuals={residuals}")


def upsert_memory(path: Path, marker: str, content: str) -> None:
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker not in old:
        path.write_text(old.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")
        return
    start = old.index(marker)
    next_start = old.find("\n## ", start + 1)
    if next_start == -1:
        new = old[:start].rstrip() + "\n\n" + content.strip() + "\n"
    else:
        new = old[:start].rstrip() + "\n\n" + content.strip() + "\n\n" + old[next_start:].lstrip()
    path.write_text(new, encoding="utf-8")


def write_reports(counts: dict[str, int]) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    items = [
        {"label": label, "old": old, "new": new, "source": source, "count": counts[label]}
        for label, old, new, source in REPLACEMENTS
    ]
    payload = {
        "time": now,
        "scope": "财政、税务、政务、教育正文 `收人` 残留",
        "source": SOURCE,
        "reader_path": str(HTML),
        "verified_items": len(REPLACEMENTS),
        "current_run_replacements": sum(counts.values()),
        "items": items,
        "principle": "仅修复源文或页级 OCR 支持为 `收入` 的 `收人`；其它 `人/入` 类残留另批处理。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# 收人/收入残留回源修复",
        "",
        f"- 时间：{now}",
        f"- 范围：{payload['scope']}",
        f"- 源文：`{SOURCE}`",
        f"- 阅读器：`{HTML}`",
        f"- 本批核验条目：{payload['verified_items']} 项",
        f"- 本次脚本复跑实际改写：{payload['current_run_replacements']} 处",
        "- `划人/纳人/投人` 等其它残留未在本批处理。",
        "",
    ]
    text = "\n".join(lines)
    REPORT_MD.write_text(text, encoding="utf-8")
    PROGRESS.write_text(text, encoding="utf-8")
    memory = f"""
## 2026-07-04 收人/收入残留回源修复

- 对财政、税务、政务、教育正文 `收人` 残留做小批回源修复。
- 源文依据：`{SOURCE}`。
- 修复 `按收人项目划分/公用企业收人/中央预算收人的盐税/企业收人/收人基数/预算内收人23%/组织收人计划/公共事业的收人/纯收人814元/年收人约2万元` 等 10 处为 `收入`。
- `交人` 剩余 1 处为 `移交人民政府` 合法跨词片段，不处理。
- 报告：`output/reports/reader_readability_shouru_residual_20260704.md`。
"""
    upsert_memory(MEMORY, "## 2026-07-04 收人/收入残留回源修复", memory)


def main() -> None:
    counts = patch_reader()
    write_reports(counts)
    print(json.dumps({"current_run_replacements": sum(counts.values()), "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
