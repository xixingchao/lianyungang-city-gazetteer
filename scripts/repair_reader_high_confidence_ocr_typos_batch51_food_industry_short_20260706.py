# -*- coding: utf-8 -*-
"""Batch 51: verified food industry OCR residue fixes."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_MD = ROOT / "output" / "reports" / "reader_high_confidence_ocr_typos_batch51_food_industry_short_20260706.md"
REPORT_JSON = ROOT / "output" / "reports" / "reader_high_confidence_ocr_typos_batch51_food_industry_short_20260706.json"
PROGRESS_MD = ROOT / "output" / "reports" / "progress" / "20260706_高置信OCR错字补修第五十一批_食品工业短片段.md"

CHANGES = [
    {
        "old": "连云港市酶制剂广",
        "new": "连云港市酶制剂厂",
        "section": "酶制剂厂名称段",
        "evidence": [
            "workbench/ocr/paddle_ocr/中/part01/page_0103.txt:27 作连云港市酶制剂厂",
            "workbench/ocr/raw/中/part01/page_0103.txt:26 为连云港市酶制剂广残留",
        ],
    },
    {
        "old": "19821989年，企业先后与上海医药工业研究院",
        "new": "1982~1989年，企业先后与上海医药工业研究院",
        "section": "酶制剂厂协作年份段",
        "evidence": [
            "workbench/ocr/paddle_ocr/中/part01/page_0103.txt:29 作1982~1989年",
            "workbench/ocr/raw/中/part01/page_0103.txt:28 为19821989年残留",
        ],
    },
    {
        "old": "部分外销本、香港",
        "new": "部分外销日本、香港",
        "section": "朱堵粉丝厂外销地区段",
        "evidence": [
            "workbench/ocr/paddle_ocr/中/part01/page_0107.txt:21 作部分外销日本、香港",
            "workbench/ocr/raw/中/part01/page_0107.txt:21 为部分外销本、香港残留",
        ],
    },
]


def main() -> None:
    html = HTML.read_text(encoding="utf-8")
    applied = []
    for change in CHANGES:
        count = html.count(change["old"])
        if count != 1:
            raise RuntimeError(f"expected one hit for {change['section']}, found {count}: {change['old']}")
        html = html.replace(change["old"], change["new"])
        applied.append({**change, "count": count})
    HTML.write_text(html, encoding="utf-8")

    payload = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "reader": str(HTML.relative_to(ROOT)).replace("\\", "/"),
        "changes": applied,
        "note": "只修 PaddleOCR 与 raw OCR 对照闭合、旧串唯一命中的食品工业短片段；未展示、未嵌入页图。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 高置信 OCR 错字补修第五十一批：食品工业短片段",
        "",
        f"> 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "## 修复项",
        "",
    ]
    for item in applied:
        lines.append(f"- {item['section']}：`{item['old']}` -> `{item['new']}`（命中 {item['count']} 处）")
        for evidence in item["evidence"]:
            lines.append(f"  - 证据：`{evidence}`")
    lines += [
        "",
        "## 边界",
        "",
        "- 只修主阅读版，不改 OCR 原文。",
        "- 每项旧串均要求唯一命中。",
        "- 同页 raw 的其它错字若当前主阅读版已不存在，本批不重复处理。",
        "- 未展示、未嵌入页图。",
        "",
    ]
    text = "\n".join(lines)
    REPORT_MD.write_text(text, encoding="utf-8")
    PROGRESS_MD.write_text(text, encoding="utf-8")
    print(f"changed={sum(item['count'] for item in applied)}")
    print(f"report={REPORT_MD}")
    print(f"progress={PROGRESS_MD}")


if __name__ == "__main__":
    main()
