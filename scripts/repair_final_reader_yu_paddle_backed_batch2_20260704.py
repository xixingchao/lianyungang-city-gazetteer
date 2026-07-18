# -*- coding: utf-8 -*-
"""Repair a second small source-backed 馀->余 batch in the final reader."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "final_reader_yu_paddle_backed_batch2_20260704.json"
REPORT_MD = ROOT / "output" / "reports" / "final_reader_yu_paddle_backed_batch2_20260704.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260704_最终阅读版余字第二批回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    {
        "label": "卢公暹万余起义",
        "old": "东海人卢公暹率众万馀起义，驻守苍山。",
        "new": "东海人卢公暹率众万余起义，驻守苍山。",
        "source": "workbench/ocr/raw/上/part01/page_0045.txt:16; workbench/ocr/paddle_ocr/上/part01/page_0045.txt:16; workbench/body_chapters/连云港市志_全书_正文汇总.md:2116",
    },
    {
        "label": "盐民2700余人",
        "old": "淹死盐民2700馀人。",
        "new": "淹死盐民2700余人。",
        "source": "workbench/ocr/raw/上/part01/page_0051.txt:5; workbench/ocr/paddle_ocr/上/part01/page_0051.txt:5; workbench/body_chapters/连云港市志_全书_正文汇总.md:2287",
    },
    {
        "label": "400余只盐船",
        "old": "400馀只盐船被烧毁",
        "new": "400余只盐船被烧毁",
        "source": "workbench/ocr/raw/上/part01/page_0054.txt:28; workbench/ocr/paddle_ocr/上/part01/page_0054.txt:28; workbench/body_chapters/连云港市志_全书_正文汇总.md:2401",
    },
    {
        "label": "霍乱40余日",
        "old": "持续40馀日，死人无数。",
        "new": "持续40余日，死人无数。",
        "source": "workbench/ocr/raw/上/part01/page_0060.txt:5; workbench/ocr/paddle_ocr/上/part01/page_0060.txt:5; workbench/body_chapters/连云港市志_全书_正文汇总.md:2576",
    },
    {
        "label": "治蝗2万余人",
        "old": "每日出动2万馀人扑灭蝗虫。",
        "new": "每日出动2万余人扑灭蝗虫。",
        "source": "workbench/ocr/raw/上/part01/page_0061.txt:26; workbench/ocr/paddle_ocr/上/part01/page_0061.txt:27; workbench/body_chapters/连云港市志_全书_正文汇总.md:2633",
    },
    {
        "label": "盐工8000余人",
        "old": "盐工8000馀人，年产盐57700吨。",
        "new": "盐工8000余人，年产盐57700吨。",
        "source": "workbench/ocr/raw/上/part01/page_0067.txt:25; workbench/ocr/paddle_ocr/上/part01/page_0067.txt:24; workbench/body_chapters/连云港市志_全书_正文汇总.md:2861",
    },
    {
        "label": "军粮10余万公斤",
        "old": "运送军粮10馀万公斤，胜利完成支前任务。",
        "new": "运送军粮10余万公斤，胜利完成支前任务。",
        "source": "workbench/ocr/raw/上/part01/page_0069.txt:5; workbench/ocr/paddle_ocr/上/part01/page_0069.txt:5; workbench/body_chapters/连云港市志_全书_正文汇总.md:2921",
    },
    {
        "label": "学员240余人",
        "old": "共有学员240馀人。",
        "new": "共有学员240余人。",
        "source": "workbench/ocr/raw/上/part01/page_0071.txt:15; workbench/ocr/paddle_ocr/上/part01/page_0071.txt:14; workbench/body_chapters/连云港市志_全书_正文汇总.md:3010",
    },
    {
        "label": "杀人凶手70余名",
        "old": "查出70馀名杀人凶手线索",
        "new": "查出70余名杀人凶手线索",
        "source": "workbench/ocr/raw/上/part01/page_0093.txt:23; workbench/ocr/paddle_ocr/上/part01/page_0093.txt:24; workbench/body_chapters/连云港市志_全书_正文汇总.md:3897",
    },
    {
        "label": "其余20种获铜牌",
        "old": "其馀20种获铜牌。",
        "new": "其余20种获铜牌。",
        "source": "workbench/ocr/raw/上/part01/page_0118.txt:33; workbench/ocr/paddle_ocr/上/part01/page_0118.txt:36; workbench/body_chapters/连云港市志_全书_正文汇总.md:4892",
    },
    {
        "label": "余为海中列岛",
        "old": "除锦屏山外，馀为海中列岛。",
        "new": "除锦屏山外，余为海中列岛。",
        "source": "workbench/ocr/raw/上/part01/page_0136.txt:13; workbench/ocr/paddle_ocr/上/part01/page_0136.txt:12; workbench/body_chapters/连云港市志_全书_正文汇总.md:5602",
    },
    {
        "label": "古银杏十余株",
        "old": "古银杏树还有十馀株。",
        "new": "古银杏树还有十余株。",
        "source": "workbench/ocr/raw/上/part01/page_0194.txt:18; workbench/ocr/paddle_ocr/上/part01/page_0194.txt:17; workbench/body_chapters/连云港市志_全书_正文汇总.md:11000",
    },
    {
        "label": "鸳鸯400余只",
        "old": "发现400馀只。",
        "new": "发现400余只。",
        "source": "workbench/ocr/raw/上/part01/page_0196.txt:8; workbench/ocr/paddle_ocr/上/part01/page_0196.txt:8; workbench/body_chapters/连云港市志_全书_正文汇总.md:11086",
    },
    {
        "label": "倒塌房屋1300余间",
        "old": "倒塌房屋1300馀间。",
        "new": "倒塌房屋1300余间。",
        "source": "workbench/ocr/raw/上/part01/page_0206.txt:27; workbench/ocr/paddle_ocr/上/part01/page_0206.txt:27; workbench/body_chapters/连云港市志_全书_正文汇总.md:11561",
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
        "scope": "最终阅读版余字第二批回源修复",
        "target": str(TARGET),
        "total_replacements": total,
        "items": items,
        "principle": "仅修复最终阅读版与正文汇总不一致，且 raw OCR 与 PaddleOCR 同句闭合为 `余` 的残留。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 最终阅读版余字第二批回源修复",
        "",
        f"- 时间：{now}",
        "- 原则：最终阅读版旧字、正文汇总已为 `余`，且 raw OCR/PaddleOCR 同句闭合后才修。",
        f"- 目标：`{TARGET}`",
        f"- 本次替换：{total} 处。",
        "- 暂缓：仅普通 OCR 命中、未取得 PaddleOCR 同句闭合的候选。",
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

    marker = "## 2026-07-04 最终阅读版余字第二批回源修复"
    memory = f"""
{marker}
- 依据正文汇总、raw OCR 与 PaddleOCR 同句闭合，修复最终阅读版 `馀 -> 余` 第二批残留，共 {total} 处。
- 只改 `output/final_reader/连云港市志_全书.html`；正文汇总当前 `馀` 为 0，本批用于对齐读者页。
- 暂缓仅普通 OCR 命中或涉及专名/语义需另核的其它 `馀` 残留。
- 报告：`output/reports/final_reader_yu_paddle_backed_batch2_20260704.md`。
"""
    append_once(MEMORY, marker, memory)
    print(json.dumps({"total_replacements": total, "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
