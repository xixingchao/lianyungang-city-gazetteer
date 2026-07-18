# -*- coding: utf-8 -*-
"""Repair source-verified money-unit slips in commerce and foreign trade volumes."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_commerce_trade_money_20260704.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_commerce_trade_money_20260704.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260704_商业外贸金额单位回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SOURCE = (
    "workbench/ocr/paddle_ocr/中/part02/page_0134.txt:39-41; page_0149.txt:19; "
    "page_0185.txt:3-5; page_0190.txt:7-11"
)

REPLACEMENTS = [
    ("商业邻县调给", "调给邻县919方元", "调给邻县919万元", "page_0134.txt:39-41"),
    ("商业蔬菜销售额", "全年蔬菜销售额70多方元", "全年蔬菜销售额70多万元", "page_0149.txt:19"),
    ("外贸棉花创汇", "出口创汇1199方美元", "出口创汇1199万美元", "page_0185.txt:3-5"),
    ("外贸痔疮治疗仪", "用汇0.5方美元", "用汇0.5万美元", "page_0190.txt:7"),
    ("外贸输油臂技术", "用汇125方马克", "用汇125万马克", "page_0190.txt:9-10"),
    ("外贸动态心电图机", "用汇3方美元", "用汇3万美元", "page_0190.txt:10-11"),
]

SKIPPED = [
    "`1.09方美元` 尚未在页级 OCR 中精确定位，本批保留。",
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
    residuals = [old for _label, old, new, _source in REPLACEMENTS if old in text and old not in new]
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
        "scope": "第三十三卷商业、第三十五卷对外经济贸易",
        "source": SOURCE,
        "reader_path": str(HTML),
        "verified_items": len(REPLACEMENTS),
        "current_run_replacements": sum(counts.values()),
        "items": items,
        "skipped": SKIPPED,
        "principle": "仅修复页级 OCR 可直接证明的商业和外贸金额单位错识。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# 商业外贸金额单位回源修复",
        "",
        f"- 时间：{now}",
        f"- 范围：{payload['scope']}",
        f"- 源文：`{SOURCE}`",
        f"- 阅读器：`{HTML}`",
        f"- 本批核验修复：{payload['verified_items']} 项",
        f"- 本次脚本复跑实际改写：{payload['current_run_replacements']} 处",
        "- 重点：修正 `919方元/70多方元/1199方美元/0.5方美元/125方马克/3方美元` 等金额单位错识。",
        "- 保留：" + "；".join(SKIPPED),
        "",
    ]
    text = "\n".join(lines)
    REPORT_MD.write_text(text, encoding="utf-8")
    PROGRESS.write_text(text, encoding="utf-8")
    memory = f"""
## 2026-07-04 商业外贸金额单位回源修复

- 对第三十三卷商业、第三十五卷对外经济贸易做金额单位错识回源修复。
- 源文依据：`{SOURCE}`。
- 修复 `919方元/70多方元/1199方美元/0.5方美元/125方马克/3方美元` → 对应 `万元/万美元/万马克`。
- `1.09方美元` 尚未在页级 OCR 中精确定位，本批保留。
- 报告：`output/reports/reader_readability_commerce_trade_money_20260704.md`。
"""
    upsert_memory(MEMORY, "## 2026-07-04 商业外贸金额单位回源修复", memory)


def main() -> None:
    counts = patch_reader()
    write_reports(counts)
    print(json.dumps({"current_run_replacements": sum(counts.values()), "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
