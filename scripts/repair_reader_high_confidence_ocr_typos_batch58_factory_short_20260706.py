# -*- coding: utf-8 -*-
"""Batch 58: verified 工厂/入/干警 OCR residue fixes."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_MD = ROOT / "output" / "reports" / "reader_high_confidence_ocr_typos_batch58_factory_short_20260706.md"
REPORT_JSON = ROOT / "output" / "reports" / "reader_high_confidence_ocr_typos_batch58_factory_short_20260706.json"
PROGRESS_MD = ROOT / "output" / "reports" / "progress" / "20260706_高置信OCR错字补修第五十八批_工厂干警入短片段.md"

CHANGES = [
    {
        "old": "仅30分钟，工广变成一片废墟",
        "new": "仅30分钟，工厂变成一片废墟",
        "section": "海州鞭炮厂爆炸事故段",
        "evidence": [
            "workbench/ocr/paddle_ocr/中/part01/page_0049.txt:117 作工厂变成一片废",
            "workbench/ocr/raw/中/part01/page_0049.txt:118 为工广残留",
        ],
    },
    {
        "old": "连云港海洋渔业公司鱼品加工广后",
        "new": "连云港海洋渔业公司鱼品加工厂后",
        "section": "水产类罐头段",
        "evidence": [
            "workbench/ocr/paddle_ocr/中/part01/page_0078.txt:38 作鱼品加工厂后",
            "workbench/ocr/raw/中/part01/page_0078.txt:37 为鱼品加工广后残留",
        ],
    },
    {
        "old": "全市涂料生产工广有8家",
        "new": "全市涂料生产工厂有8家",
        "section": "涂料生产概况段",
        "evidence": [
            "workbench/ocr/paddle_ocr/中/part01/page_0291.txt:25 作涂料生产工厂有8家",
            "workbench/ocr/raw/中/part01/page_0291.txt:25 为工广残留",
        ],
    },
    {
        "old": "流水养鱼和工广化养鱼打下了基础",
        "new": "流水养鱼和工厂化养鱼打下了基础",
        "section": "海水养殖科技推广段",
        "evidence": [
            "workbench/ocr/paddle_ocr/下/part01/page_0438.txt:40 作工厂化养鱼",
            "主阅读版旧串为工广化养鱼残留",
        ],
    },
    {
        "old": "市公安于警学校成立",
        "new": "市公安干警学校成立",
        "section": "市公安局机构沿革段",
        "evidence": [
            "workbench/ocr/paddle_ocr/下/part01/page_0064.txt:5 作市公安干警学校成立",
            "主阅读版旧串为公安于警学校残留",
        ],
    },
    {
        "old": "陶瓷人海州的品种丰富",
        "new": "陶瓷入海州的品种丰富",
        "section": "宋代海州口岸贸易段",
        "evidence": [
            "workbench/ocr/paddle_ocr/中/part01/page_0456.txt:13 作陶瓷入海州的品种丰",
            "主阅读版旧串为陶瓷人海州残留",
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
        "note": "只修 PaddleOCR/raw OCR 或 PaddleOCR 与主阅读版旧串对照闭合的短片段；未展示、未嵌入页图。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 高置信 OCR 错字补修第五十八批：工厂、干警、入短片段",
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
        "- `日用化工广` 暂只见 raw 同页残留，未纳入本批。",
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
