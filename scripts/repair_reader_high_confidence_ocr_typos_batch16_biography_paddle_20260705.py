# -*- coding: utf-8 -*-
"""Sixteenth batch: biography repairs backed by page-level PaddleOCR."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_MD = ROOT / "output" / "reports" / "reader_high_confidence_ocr_typos_batch16_biography_paddle_20260705.md"
REPORT_JSON = ROOT / "output" / "reports" / "reader_high_confidence_ocr_typos_batch16_biography_paddle_20260705.json"

CHANGES = [
    {
        "old": "武汉卫成司令部副官处处长",
        "new": "武汉卫戍司令部副官处处长",
        "section": "李云鹤传",
        "evidence": ["workbench/ocr/paddle_ocr/下/part02/page_0355.txt:28"],
    },
    {
        "old": "出任日照、诸城、沂水、县中心县委书记",
        "new": "出任日照、诸城、沂水、莒县中心县委书记",
        "section": "李云鹤传",
        "evidence": ["workbench/ocr/paddle_ocr/下/part02/page_0355.txt:37"],
    },
    {
        "old": "在益都、临胸一带组织八路军鲁东游击队十支队",
        "new": "在益都、临朐一带组织八路军鲁东游击队十支队",
        "section": "李云鹤传",
        "evidence": ["workbench/ocr/paddle_ocr/下/part02/page_0355.txt:40"],
    },
    {
        "old": "民国27年，季云鹤·改任广绕、寿光、益都三县中心县委书记",
        "new": "民国27年，李云鹤改任广饶、寿光、益都三县中心县委书记",
        "section": "李云鹤传",
        "evidence": [
            "workbench/ocr/paddle_ocr/下/part02/page_0355.txt:40-41 读作 `李云鹤/改任`",
            "地名固定组合：广饶、寿光、益都三县",
        ],
    },
    {
        "old": "任睢铜地委书记",
        "new": "任邳睢铜地委书记",
        "section": "李云鹤传",
        "evidence": ["workbench/ocr/paddle_ocr/下/part02/page_0356.txt:3"],
    },
    {
        "old": "将国民党南行署过渡为抗日政权",
        "new": "将国民党邳南行署过渡为抗日政权",
        "section": "李云鹤传",
        "evidence": ["workbench/ocr/paddle_ocr/下/part02/page_0356.txt:4"],
    },
    {
        "old": "季李云鹤积劳成疾",
        "new": "李云鹤积劳成疾",
        "section": "李云鹤传",
        "evidence": ["workbench/ocr/paddle_ocr/下/part02/page_0356.txt:6"],
    },
    {
        "old": "民国元年（1912年）人盐城县立第二高等小学读书",
        "new": "民国元年（1912年）入盐城县立第二高等小学读书",
        "section": "曹仲权传",
        "evidence": ["workbench/ocr/paddle_ocr/下/part02/page_0357.txt:16"],
    },
    {
        "old": "民国16年考入南京国立第四中山大学，获理学学土学位",
        "new": "民国16年考入南京国立第四中山大学，获理学学士学位",
        "section": "曹仲权传",
        "evidence": ["workbench/ocr/paddle_ocr/下/part02/page_0357.txt:17"],
    },
]


def main() -> None:
    html = HTML.read_text(encoding="utf-8")
    applied = []
    for change in CHANGES:
        count = html.count(change["old"])
        if count != 1:
            raise RuntimeError(f"expected one hit for {change['old']!r}, found {count}")
        html = html.replace(change["old"], change["new"])
        applied.append({**change, "count": count})
    HTML.write_text(html, encoding="utf-8")

    payload = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "reader": str(HTML.relative_to(ROOT)).replace("\\", "/"),
        "changes": applied,
        "note": "精确替换人物传略中由 raw OCR 造成、页级 PaddleOCR 可反证的短片段。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 高置信 OCR 错字补修第十六批：人物传略 PaddleOCR 对照",
        "",
        f"> 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "## 修复项",
        "",
    ]
    for item in applied:
        lines.append(f"- `{item['old']}` -> `{item['new']}`（{item['section']}；命中 {item['count']} 处）")
        for evidence in item["evidence"]:
            lines.append(f"  - 证据：`{evidence}`")
    lines += [
        "",
        "## 边界",
        "",
        "- 只修主阅读版；不改 raw/PaddleOCR 中间源。",
        "- 不批量替换 `加人/考人`，本批只处理已落入具体人物条目的精确短片段。",
        "- 未展示、未嵌入页图。",
        "",
    ]
    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(f"changed={sum(item['count'] for item in applied)}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()
