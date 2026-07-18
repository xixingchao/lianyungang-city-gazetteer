# -*- coding: utf-8 -*-
"""Repair remaining source-verified foreign-currency OCR slips in final reader."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_foreign_currency_residual_20260704.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_foreign_currency_residual_20260704.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260704_外币金额残留回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SOURCE = (
    "workbench/ocr/paddle_ocr/中/part01/page_0215.txt:27; "
    "workbench/ocr/paddle_ocr/中/part01/page_0512.txt:14; "
    "workbench/ocr/paddle_ocr/中/part02/page_0117.txt:36; "
    "workbench/ocr/paddle_ocr/中/part02/page_0189.txt:30-31"
)

REPLACEMENTS = [
    ("机械工业升降机创汇", "创汇20方美元", "创汇20万美元", "中/part01/page_0215.txt:27"),
    ("口岸棉花水湿担保", "船方提供20方美元的银行担保", "船方提供20万美元的银行担保", "中/part01/page_0512.txt:14"),
    ("名胜旅游神州宾馆投资", "共同投资300方美元兴建", "共同投资300万美元兴建", "中/part02/page_0117.txt:36"),
    ("外贸杀菌温度测试仪金额", "用汇1.09方美元", "用汇1.09万美元", "中/part02/page_0189.txt:30-31"),
    ("外贸杀菌温度测试仪厂名", "市罐头广从丹麦引进杀菌温度测试仪", "市罐头厂从丹麦引进杀菌温度测试仪", "中/part02/page_0189.txt:30"),
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
        "scope": "第二十一卷机械工业、第二十九卷口岸、第三十二卷名胜旅游、第三十五卷对外经济贸易",
        "source": SOURCE,
        "reader_path": str(HTML),
        "verified_items": len(REPLACEMENTS),
        "current_run_replacements": sum(counts.values()),
        "items": items,
        "principle": "仅修复页级 OCR 可直接证明的外币金额单位和同句厂名错识。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# 外币金额残留回源修复",
        "",
        f"- 时间：{now}",
        f"- 范围：{payload['scope']}",
        f"- 源文：`{SOURCE}`",
        f"- 阅读器：`{HTML}`",
        f"- 本批核验修复：{payload['verified_items']} 项",
        f"- 本次脚本复跑实际改写：{payload['current_run_replacements']} 处",
        "- 重点：清理 `20方美元/300方美元/1.09方美元` 等残留，并据同页源文修正 `市罐头广` 为 `市罐头厂`。",
        "- 说明：本批不处理尚未逐条回源确认的 `方元` 残留。",
        "",
    ]
    text = "\n".join(lines)
    REPORT_MD.write_text(text, encoding="utf-8")
    PROGRESS.write_text(text, encoding="utf-8")
    memory = f"""
## 2026-07-04 外币金额残留回源修复

- 对第二十一卷机械工业、第二十九卷口岸、第三十二卷名胜旅游、第三十五卷对外经济贸易做外币金额残留回源修复。
- 源文依据：`{SOURCE}`。
- 修复 `创汇20方美元/船方提供20方美元/共同投资300方美元/用汇1.09方美元` → `万美元`。
- 同页源文确认 `市罐头广从丹麦引进杀菌温度测试仪` 应为 `市罐头厂从丹麦引进杀菌温度测试仪`。
- 报告：`output/reports/reader_readability_foreign_currency_residual_20260704.md`。
"""
    upsert_memory(MEMORY, "## 2026-07-04 外币金额残留回源修复", memory)


def main() -> None:
    counts = patch_reader()
    write_reports(counts)
    print(json.dumps({"current_run_replacements": sum(counts.values()), "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
