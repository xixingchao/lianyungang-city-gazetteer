# -*- coding: utf-8 -*-
"""Batch 52: verified people and water OCR residue fixes."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_MD = ROOT / "output" / "reports" / "reader_high_confidence_ocr_typos_batch52_people_water_short_20260706.md"
REPORT_JSON = ROOT / "output" / "reports" / "reader_high_confidence_ocr_typos_batch52_people_water_short_20260706.json"
PROGRESS_MD = ROOT / "output" / "reports" / "progress" / "20260706_高置信OCR错字补修第五十二批_人物水利短片段.md"

CHANGES = [
    {
        "old": "灌云县农机广",
        "new": "灌云县农机厂",
        "section": "高家鸿履历单位段",
        "evidence": [
            "workbench/ocr/paddle_ocr/下/part02/page_0399.txt:16 作灌云县农机厂",
            "workbench/ocr/raw/下/part02/page_0399.txt:16 为灌云县农机广残留",
        ],
    },
    {
        "old": "减轻谣役，务政宽平",
        "new": "减轻徭役，务政宽平",
        "section": "俞廷瑞政绩段",
        "evidence": [
            "workbench/ocr/paddle_ocr/下/part02/page_0382.txt:34 作徭役",
            "workbench/ocr/raw/下/part02/page_0382.txt:34 为谣役残留",
        ],
    },
    {
        "old": "编繁县志，后人凡论及地方文献的",
        "new": "编纂县志，后人凡论及地方文献的",
        "section": "俞廷瑞编纂县志段",
        "evidence": [
            "workbench/ocr/paddle_ocr/下/part02/page_0382.txt:34 作编纂县志",
            "workbench/ocr/raw/下/part02/page_0382.txt:34 为编繁县志残留",
        ],
    },
    {
        "old": "武同举编繁成功《淮系年鉴》，1950年又编繁出版《江苏水利全书》，为治理华东水惠造福于民",
        "new": "武同举编纂成功《淮系年鉴》，1950年又编纂出版《江苏水利全书》，为治理华东水患造福于民",
        "section": "武同举水利著述段",
        "evidence": [
            "workbench/ocr/paddle_ocr/下/part01/page_0436.txt:23-24 作编纂成功、又编纂出版、水患造福于民",
            "workbench/ocr/raw/下/part01/page_0436.txt:23-24 为编繁/水惠残留",
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
        "note": "只修 PaddleOCR/raw OCR 对照闭合、旧串唯一命中的人物与水利短片段；未展示、未嵌入页图。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 高置信 OCR 错字补修第五十二批：人物水利短片段",
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
        "- 书末编纂始末页暂无 PaddleOCR 页文本支撑的疑点，本批不猜改。",
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
