# -*- coding: utf-8 -*-
"""Batch 60: verified ISBN and 并入 short fixes."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_MD = ROOT / "output" / "reports" / "reader_high_confidence_ocr_typos_batch60_isbn_into_short_20260706.md"
REPORT_JSON = ROOT / "output" / "reports" / "reader_high_confidence_ocr_typos_batch60_isbn_into_short_20260706.json"
PROGRESS_MD = ROOT / "output" / "reports" / "progress" / "20260706_高置信OCR错字补修第六十批_ISBN并入短片段.md"

CHANGES = [
    {
        "old": "80124ISBN7-80122-571-6/K-240定价：（上中，下三明精装）398元",
        "new": "ISBN7-80122-571-6/K-240定价：（上、中、下三册精装）398元",
        "section": "卷末版权信息残留",
        "evidence": [
            "workbench/ocr/paddle_ocr/上/part01/page_0003.txt:22-23 作 ISBN7—80122-571—6/K·240、定价：(上、中、下三册精装)398元",
            "workbench/ocr/paddle_ocr/上/part02/page_0002.txt:22-23 同书版权页重复作同一 ISBN/定价",
            "主阅读版旧串为 80124/上中/三明 残留",
        ],
    },
    {
        "old": "连云港市地方志编繁委员会办公室2000年5月TSBN7-80122-571-6ISBN7-80122-$71-6/K-240定价：（上、中、下三册精装）398元",
        "new": "连云港市地方志编纂委员会办公室2000年5月ISBN7-80122-571-6ISBN7-80122-571-6/K-240定价：（上、中、下三册精装）398元",
        "section": "书末编纂始末署名和版权信息",
        "evidence": [
            "workbench/ocr/paddle_ocr/上/part01/page_0003.txt:22-23 作 ISBN7—80122-571—6/K·240、定价：(上、中、下三册精装)398元",
            "workbench/ocr/paddle_ocr/merged/连云港市志_上册_PaddleOCR汇总.md:35-36 同书版权页重复作 ISBN/定价",
            "同书前置页多处作 连云港市地方志编纂委员会；旧串为 编繁委员会/TSBN/$71 残留",
        ],
    },
    {
        "old": "夹山并人东华汽",
        "new": "夹山并入东华汽",
        "section": "商营长途汽车公司线性表残留",
        "evidence": [
            "workbench/ocr/raw/上/part02/page_0071.txt:18 作普益汽车公司并入东华汽车公司",
            "workbench/ocr/paddle_ocr/merged/连云港市志_上_part02_PaddleOCR汇总.md:6123 作普益汽车公司并入东华汽车公司",
            "主阅读版线性表旧串为 并人东华汽 残留",
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
        "note": "只修同书版权页或正文 OCR 对照闭合、旧串唯一命中的短片段；未展示、未嵌入页图。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 高置信 OCR 错字补修第六十批：ISBN 与并入短片段",
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
        "- 书末版权信息只归正字符误识别，不重排版式。",
        "- `避选` 等书末词双源证据仍弱，本批不猜改。",
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
