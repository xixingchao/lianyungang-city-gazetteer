# -*- coding: utf-8 -*-
"""Thirty-first batch: PaddleOCR-backed transport, food, military, social fixes."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_MD = ROOT / "output" / "reports" / "reader_high_confidence_ocr_typos_batch31_transport_food_military_social_20260706.md"
REPORT_JSON = ROOT / "output" / "reports" / "reader_high_confidence_ocr_typos_batch31_transport_food_military_social_20260706.json"

CHANGES = [
    {
        "old": "1949年成立工会，人会工人260余人",
        "new": "1949年成立工会，入会工人260余人",
        "section": "赣榆县装卸搬运段",
        "evidence": [
            "workbench/ocr/raw/中/part02/page_0050.txt:21 raw 作人会工人260余",
            "workbench/ocr/paddle_ocr/中/part02/page_0050.txt:21 PaddleOCR 作入会工人260余",
        ],
    },
    {
        "old": "农田水利和配变以下机电排粮，于部每夜补助0.1公斤",
        "new": "农田水利和配变以下机电排灌工程民工每标准劳动日补助0.25公斤；调用干部参加施工每人每月补助1公斤；夜餐粮，干部每夜补助0.1公斤",
        "section": "工程民工补助粮段",
        "evidence": [
            "workbench/ocr/raw/中/part02/page_0229.txt:5 raw 漏作配变以下机电排粮，于部每夜补助",
            "workbench/ocr/paddle_ocr/中/part02/page_0229.txt:4-6 PaddleOCR 作配变以下机电排灌工程、调用干部、夜餐粮、干部每夜补助",
        ],
    },
    {
        "old": "实行“行业归口”安置，如草绳、造纸厂、鞋帽厂等行业",
        "new": "实行“行业归口”安置，如草绳厂、造纸厂、鞋帽厂等行业",
        "section": "复员建设军人行业归口安置段",
        "evidence": [
            "workbench/ocr/raw/下/part01/page_0026.txt:9 raw 漏草绳厂的厂字",
            "workbench/ocr/paddle_ocr/下/part01/page_0026.txt:9 PaddleOCR 作草绳厂、造纸厂、鞋帽厂",
        ],
    },
    {
        "old": "1954年11月前人伍的志愿兵复员后按照“原籍安置”的原则，在农村人伍的志愿兵复员回乡后",
        "new": "1954年11月前入伍的志愿兵复员后按照“原籍安置”的原则，在农村入伍的志愿兵复员回乡后",
        "section": "志愿兵原籍安置段",
        "evidence": [
            "workbench/ocr/raw/下/part01/page_0026.txt:13-14 raw 作前人伍、农村人伍",
            "workbench/ocr/paddle_ocr/下/part01/page_0026.txt:13-14 PaddleOCR 作前入伍、农村入伍",
        ],
    },
    {
        "old": "在城镇人伍的志愿兵，按“归口包于”的办法安置",
        "new": "在城镇入伍的志愿兵，按“归口包干”的办法安置",
        "section": "城镇志愿兵归口包干安置段",
        "evidence": [
            "workbench/ocr/raw/下/part01/page_0026.txt:15 raw 作城镇人伍、归口包于",
            "workbench/ocr/paddle_ocr/下/part01/page_0026.txt:15 PaddleOCR 作城镇入伍、归口包干",
        ],
    },
    {
        "old": "义务兵人伍时原是家居农村或城郊的农民",
        "new": "义务兵入伍时原是家居农村或城郊的农民",
        "section": "义务兵退伍暂行规定段",
        "evidence": [
            "workbench/ocr/raw/下/part01/page_0026.txt:17 raw 作义务兵人伍时",
            "workbench/ocr/paddle_ocr/下/part01/page_0026.txt:17 PaddleOCR 作义务兵入伍时",
        ],
    },
    {
        "old": "根据省有关规定，对农村人伍的二、三等残废军人",
        "new": "根据省有关规定，对农村入伍的二、三等残废军人",
        "section": "伤病残退伍军人安置段",
        "evidence": [
            "workbench/ocr/raw/下/part01/page_0027.txt:25 raw 作农村人伍",
            "workbench/ocr/paddle_ocr/下/part01/page_0027.txt:25 PaddleOCR 作农村入伍",
        ],
    },
    {
        "old": "对“文化大革命”前人会的会员进行调查登记",
        "new": "对“文化大革命”前入会的会员进行调查登记",
        "section": "灌云县工商联会员调查段",
        "evidence": [
            "workbench/ocr/raw/下/part01/page_0341.txt:5 raw 作前人会的会员",
            "workbench/ocr/paddle_ocr/下/part01/page_0341.txt:5 PaddleOCR 作前入会的会员",
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
        "note": "只修 raw/PaddleOCR 可闭合的交通、粮食补助、兵役安置、工商联短片段；未展示、未嵌入页图。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 高置信 OCR 错字补修第三十一批：交通、粮食补助、兵役与社团短片段",
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
        "- 未全局替换 `人会/入会`、`人伍/入伍`、`于部/干部`、`包于/包干` 等模式。",
        "- 医学术语、人大视察段、公安查禁卖淫段仍缺本批同等强证据，本批暂缓。",
        "- 未展示、未嵌入页图。",
        "",
    ]
    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(f"changed={sum(item['count'] for item in applied)}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()
