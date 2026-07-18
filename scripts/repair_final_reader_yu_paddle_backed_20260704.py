# -*- coding: utf-8 -*-
"""Repair a small source-backed 馀->余 batch in the final reader."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "final_reader_yu_paddle_backed_20260704.json"
REPORT_MD = ROOT / "output" / "reports" / "final_reader_yu_paddle_backed_20260704.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260704_最终阅读版余字小批回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    {
        "label": "序言十余年之功",
        "old": "《连云港市志》编纂积十馀年之功",
        "new": "《连云港市志》编纂积十余年之功",
        "source": "workbench/ocr/raw/上/part01/page_0014.txt:10; workbench/ocr/paddle_ocr/merged/连云港市志_上册_PaddleOCR汇总.md:1472",
    },
    {
        "label": "沂蒙山余脉",
        "old": "沂蒙山馀脉",
        "new": "沂蒙山余脉",
        "source": "workbench/ocr/raw/上/part01/page_0029.txt:11; page_0134.txt:26; page_0136.txt:6; page_0255.txt:7; page_0264.txt:11; workbench/ocr/paddle_ocr/merged/连云港市志_上册_PaddleOCR汇总.md:2378,6539,6590,15505,15856",
    },
    {
        "label": "矿产资源40余种",
        "old": "40馀种",
        "new": "40余种",
        "source": "workbench/ocr/raw/上/part01/page_0030.txt:10; page_0125.txt:6; page_0188.txt:26; workbench/ocr/paddle_ocr/merged/连云港市志_上册_PaddleOCR汇总.md:2402,6042,12327",
    },
    {
        "label": "其余各朝",
        "old": "其馀各朝",
        "new": "其余各朝",
        "source": "workbench/ocr/raw/上/part01/page_0030.txt:21; workbench/ocr/paddle_ocr/merged/连云港市志_上册_PaddleOCR汇总.md:2413",
    },
    {
        "label": "扁担会300余人",
        "old": "300馀人）为骨干",
        "new": "300余人）为骨干",
        "source": "workbench/ocr/raw/上/part01/page_0031.txt:16; workbench/ocr/paddle_ocr/merged/连云港市志_上册_PaddleOCR汇总.md:2446",
    },
    {
        "label": "遣唐使500余人",
        "old": "500馀人，乘10条",
        "new": "500余人，乘10条",
        "source": "workbench/ocr/merged/连云港市志_上册_OCR汇总.md:2833; workbench/ocr/paddle_ocr/merged/连云港市志_上册_PaddleOCR汇总.md:2488",
    },
    {
        "label": "图书藏书51.4万余册",
        "old": "51.4万馀册",
        "new": "51.4万余册",
        "source": "workbench/ocr/raw/上/part01/page_0039.txt:4; workbench/ocr/paddle_ocr/merged/连云港市志_上册_PaddleOCR汇总.md:2755",
    },
    {
        "label": "报纸10余种",
        "old": "10馀种报纸",
        "new": "10余种报纸",
        "source": "workbench/body_chapters/上/总述与大事记.md:309; workbench/ocr/paddle_ocr/merged/连云港市志_上册_PaddleOCR汇总.md:2759",
    },
    {
        "label": "天花300余人发病",
        "old": "300馀人发病",
        "new": "300余人发病",
        "source": "workbench/ocr/raw/上/part01/page_0064.txt:4; workbench/ocr/paddle_ocr/merged/连云港市志_上册_PaddleOCR汇总.md:3575",
    },
    {
        "label": "起义官兵2500余人",
        "old": "2500馀人，由黄埔港",
        "new": "2500余人，由黄埔港",
        "source": "workbench/ocr/raw/上/part01/page_0070.txt:34; workbench/ocr/paddle_ocr/merged/连云港市志_上册_PaddleOCR汇总.md:3850",
    },
    {
        "label": "教师代表1300余人",
        "old": "1300馀人",
        "new": "1300余人",
        "source": "workbench/ocr/raw/上/part01/page_0112.txt:22; workbench/ocr/paddle_ocr/merged/连云港市志_上册_PaddleOCR汇总.md:5562",
    },
    {
        "label": "信教群众31500余人",
        "old": "31500馀人",
        "new": "31500余人",
        "source": "workbench/ocr/raw/上/part01/page_0118.txt:26; workbench/ocr/paddle_ocr/merged/连云港市志_上册_PaddleOCR汇总.md:5818",
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
        "scope": "最终阅读版余字小批回源修复",
        "target": str(TARGET),
        "total_replacements": total,
        "items": items,
        "principle": "仅修复 raw OCR 与 PaddleOCR 汇总/正文同句均闭合为 `余` 的最终阅读版残留，不处理人名等未核项。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 最终阅读版余字小批回源修复",
        "",
        f"- 时间：{now}",
        "- 原则：仅修复 raw OCR 与 PaddleOCR 同句闭合的 `馀 -> 余` 残留。",
        f"- 目标：`{TARGET}`",
        f"- 本次替换：{total} 处。",
        "- 暂缓：人名中的 `馀`、未取得同句源证据的普通数量词。",
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

    marker = "## 2026-07-04 最终阅读版余字小批回源修复"
    memory = f"""
{marker}
- 依据 raw OCR 与 PaddleOCR 汇总/正文同句闭合，修复最终阅读版 `馀 -> 余` 小批残留，共 {total} 处。
- 只改 `output/final_reader/连云港市志_全书.html`；正文源多处已为 `余`，未做反向大范围同步。
- 暂缓人名及未取得同句源证据的其它 `馀` 命中，避免把可能的专名或原文用字误改。
- 报告：`output/reports/final_reader_yu_paddle_backed_20260704.md`。
"""
    append_once(MEMORY, marker, memory)
    print(json.dumps({"total_replacements": total, "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
