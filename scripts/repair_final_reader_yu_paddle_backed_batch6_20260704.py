# -*- coding: utf-8 -*-
"""Repair a sixth source-backed 馀->余 batch in the final reader."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "final_reader_yu_paddle_backed_batch6_20260704.json"
REPORT_MD = ROOT / "output" / "reports" / "final_reader_yu_paddle_backed_batch6_20260704.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260704_最终阅读版余字第六批回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    {
        "label": "郝部2个师1万余人",
        "old": "消灭郝部2个师1万馀人。",
        "new": "消灭郝部2个师1万余人。",
        "source": "workbench/ocr/raw/上/part01/page_0264.txt:36; workbench/ocr/paddle_ocr/上/part01/page_0264.txt:36; workbench/body_chapters/连云港市志_全书_正文汇总.md:14170",
    },
    {
        "label": "菜地扩大6000余亩",
        "old": "1958年，菜地扩大到6000馀亩",
        "new": "1958年，菜地扩大到6000余亩",
        "source": "workbench/ocr/raw/上/part02/page_0254.txt:22; workbench/ocr/paddle_ocr/上/part02/page_0254.txt:22; workbench/body_chapters/连云港市志_全书_正文汇总.md:34780",
    },
    {
        "label": "塑料大棚1万余亩",
        "old": "共发展塑料大棚1万馀亩。",
        "new": "共发展塑料大棚1万余亩。",
        "source": "workbench/ocr/raw/上/part02/page_0255.txt:7; workbench/ocr/paddle_ocr/上/part02/page_0255.txt:7; workbench/body_chapters/连云港市志_全书_正文汇总.md:34804",
    },
    {
        "label": "播种机3500余台",
        "old": "小型拖拉机配套的播种机3500馀台",
        "new": "小型拖拉机配套的播种机3500余台",
        "source": "workbench/ocr/raw/上/part02/page_0263.txt:17; workbench/ocr/paddle_ocr/上/part02/page_0263.txt:16; workbench/body_chapters/连云港市志_全书_正文汇总.md:35136",
    },
    {
        "label": "印刷厂2050余公斤铅字",
        "old": "2050馀公斤铅字，以及新华书店从滨海根据地带来的2台石印机等设备",
        "new": "2050余公斤铅字，以及新华书店从滨海根据地带来的2台石印机等设备",
        "source": "workbench/ocr/raw/上/part03/page_0182.txt:34; workbench/ocr/paddle_ocr/上/part03/page_0182.txt:36; workbench/body_chapters/连云港市志_全书_正文汇总.md:51512",
    },
    {
        "label": "纺织手工作坊190余户",
        "old": "手工作坊190馀户，均勉强维持生计。",
        "new": "手工作坊190余户，均勉强维持生计。",
        "source": "workbench/ocr/raw/上/part03/page_0226.txt:19; workbench/ocr/paddle_ocr/上/part03/page_0226.txt:22; workbench/body_chapters/连云港市志_全书_正文汇总.md:53596",
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
        "scope": "最终阅读版余字第六批回源修复",
        "target": str(TARGET),
        "total_replacements": total,
        "items": items,
        "principle": "仅修复最终阅读版与正文汇总不一致，且 raw OCR 与 PaddleOCR 同句/同页闭合为 `余` 的残留。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 最终阅读版余字第六批回源修复",
        "",
        f"- 时间：{now}",
        "- 原则：最终阅读版旧字、正文汇总已为 `余`，且 raw OCR/PaddleOCR 闭合后才修。",
        f"- 目标：`{TARGET}`",
        f"- 本次替换：{total} 处。",
        "- 暂缓：`有校舍10馀间`、`员工200馀人` 等未取得足够直接证据的残留。",
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

    marker = "## 2026-07-04 最终阅读版余字第六批回源修复"
    memory = f"""
{marker}
- 依据正文汇总、raw OCR 与 PaddleOCR 闭合，修复最终阅读版 `馀 -> 余` 第六批残留，共 {total} 处。
- 本批覆盖赣榆郝鹏举段、蔬菜基地/塑料大棚、播种机、印刷铅字、纺织手工作坊。
- 暂缓 `有校舍10馀间`、`员工200馀人` 等未取得足够直接证据的残留。
- 报告：`output/reports/final_reader_yu_paddle_backed_batch6_20260704.md`。
"""
    append_once(MEMORY, marker, memory)
    print(json.dumps({"total_replacements": total, "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
