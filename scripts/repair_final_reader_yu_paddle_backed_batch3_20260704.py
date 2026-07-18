# -*- coding: utf-8 -*-
"""Repair a third source-backed 馀->余 batch in the final reader."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "final_reader_yu_paddle_backed_batch3_20260704.json"
REPORT_MD = ROOT / "output" / "reports" / "final_reader_yu_paddle_backed_batch3_20260704.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260704_最终阅读版余字第三批回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    {
        "label": "私商10余家与小麦50余万公斤",
        "old": "10馀家私人商行和工厂。损失小麦50馀万公斤",
        "new": "10余家私人商行和工厂。损失小麦50余万公斤",
        "source": "workbench/ocr/raw/上/part01/page_0069.txt:18; workbench/ocr/paddle_ocr/上/part01/page_0069.txt:19; workbench/body_chapters/连云港市志_全书_正文汇总.md:2961",
    },
    {
        "label": "科技成果60余项",
        "old": "全区获省市科技成果奖60馀项。",
        "new": "全区获省市科技成果奖60余项。",
        "source": "workbench/ocr/raw/上/part01/page_0243.txt:7; workbench/ocr/paddle_ocr/上/part01/page_0243.txt:7; workbench/body_chapters/连云港市志_全书_正文汇总.md:13928",
    },
    {
        "label": "业余班7个",
        "old": "业馀班7个，在籍学生412人",
        "new": "业余班7个，在籍学生412人",
        "source": "workbench/ocr/raw/上/part01/page_0261.txt:12; workbench/ocr/paddle_ocr/上/part01/page_0261.txt:12; workbench/body_chapters/连云港市志_全书_正文汇总.md:14034",
    },
    {
        "label": "青少年业余体校",
        "old": "1985年县青少年业馀体校成立。",
        "new": "1985年县青少年业余体校成立。",
        "source": "workbench/ocr/raw/上/part01/page_0278.txt:16; workbench/ocr/paddle_ocr/上/part01/page_0278.txt:16; workbench/body_chapters/连云港市志_全书_正文汇总.md:14655",
    },
    {
        "label": "自然灾害100余次和40余次",
        "old": "自然灾害100馀次，其中重大自然灾害40馀次",
        "new": "自然灾害100余次，其中重大自然灾害40余次",
        "source": "workbench/ocr/raw/上/part01/page_0280.txt:23; workbench/ocr/paddle_ocr/上/part01/page_0280.txt:22; workbench/body_chapters/连云港市志_全书_正文汇总.md:14733",
    },
    {
        "label": "其余多未利用",
        "old": "其馀多未利用。",
        "new": "其余多未利用。",
        "source": "workbench/ocr/raw/上/part02/page_0060.txt:21; workbench/ocr/paddle_ocr/上/part02/page_0060.txt:22; workbench/body_chapters/连云港市志_全书_正文汇总.md:22391",
    },
    {
        "label": "花木馆树种花卉盆景",
        "old": "绿化树种86种，300馀株，花卉品种370馀种，各种盆景6000馀盆。",
        "new": "绿化树种86种，300余株，花卉品种370余种，各种盆景6000余盆。",
        "source": "workbench/ocr/raw/上/part02/page_0082.txt:16; workbench/ocr/paddle_ocr/上/part02/page_0082.txt:17; workbench/body_chapters/连云港市志_全书_正文汇总.md:23549",
    },
    {
        "label": "庭院养花76000余盆",
        "old": "居民庭院养花达76000馀盆",
        "new": "居民庭院养花达76000余盆",
        "source": "workbench/ocr/raw/上/part02/page_0085.txt:23; workbench/ocr/paddle_ocr/上/part02/page_0085.txt:23; workbench/body_chapters/连云港市志_全书_正文汇总.md:23668",
    },
    {
        "label": "调查商品400余个",
        "old": "调查商品扩大到八大类400馀个。",
        "new": "调查商品扩大到八大类400余个。",
        "source": "workbench/ocr/raw/上/part02/page_0167.txt:10; workbench/ocr/paddle_ocr/上/part02/page_0167.txt:9; workbench/body_chapters/连云港市志_全书_正文汇总.md:29504",
    },
    {
        "label": "统计分析300余篇",
        "old": "统计分析报告300馀篇。",
        "new": "统计分析报告300余篇。",
        "source": "workbench/ocr/raw/上/part02/page_0170.txt:27; workbench/ocr/paddle_ocr/上/part02/page_0170.txt:27; workbench/body_chapters/连云港市志_全书_正文汇总.md:29705",
    },
    {
        "label": "查阅资料2000余人次",
        "old": "接待查阅资料人数2000馀人次",
        "new": "接待查阅资料人数2000余人次",
        "source": "workbench/ocr/raw/上/part02/page_0183.txt:53; workbench/ocr/paddle_ocr/上/part02/page_0183.txt:51; workbench/body_chapters/连云港市志_全书_正文汇总.md:30609",
    },
    {
        "label": "物价检查员80余名",
        "old": "聘请80馀名物价检查员。",
        "new": "聘请80余名物价检查员。",
        "source": "workbench/ocr/raw/上/part02/page_0208.txt:26; workbench/ocr/paddle_ocr/上/part02/page_0208.txt:25; workbench/body_chapters/连云港市志_全书_正文汇总.md:31862",
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
        "scope": "最终阅读版余字第三批回源修复",
        "target": str(TARGET),
        "total_replacements": total,
        "items": items,
        "principle": "仅修复最终阅读版与正文汇总不一致，且 raw OCR 与 PaddleOCR 同句闭合为 `余` 的残留。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 最终阅读版余字第三批回源修复",
        "",
        f"- 时间：{now}",
        "- 原则：最终阅读版旧字、正文汇总已为 `余`，且 raw OCR/PaddleOCR 同句闭合后才修。",
        f"- 目标：`{TARGET}`",
        f"- 本次替换：{total} 处。",
        "- 暂缓：盐业/轻工等下一组候选，以及仅普通 OCR 命中的条目。",
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

    marker = "## 2026-07-04 最终阅读版余字第三批回源修复"
    memory = f"""
{marker}
- 依据正文汇总、raw OCR 与 PaddleOCR 同句闭合，修复最终阅读版 `馀 -> 余` 第三批残留，共 {total} 处。
- 本批覆盖上册 part01/part02 的私商损失、科技教育、自然灾害、水源、花木、物价统计与标准情报段。
- 暂缓盐业/轻工候选及仅普通 OCR 命中项，继续分批核。
- 报告：`output/reports/final_reader_yu_paddle_backed_batch3_20260704.md`。
"""
    append_once(MEMORY, marker, memory)
    print(json.dumps({"total_replacements": total, "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
