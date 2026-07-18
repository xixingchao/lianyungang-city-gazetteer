# -*- coding: utf-8 -*-
"""Twenty-seventh batch: small PaddleOCR-backed reader OCR fixes."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_MD = ROOT / "output" / "reports" / "reader_high_confidence_ocr_typos_batch27_medicine_food_cppcc_20260706.md"
REPORT_JSON = ROOT / "output" / "reports" / "reader_high_confidence_ocr_typos_batch27_medicine_food_cppcc_20260706.json"

CHANGES = [
    {
        "old": "连云港食品总厂襄河乳品广因奶源严重缺乏",
        "new": "连云港食品总厂襄河乳品厂因奶源严重缺乏",
        "section": "食品工业乳制品段",
        "evidence": [
            "workbench/ocr/raw/中/part01/page_0107.txt:5 raw 作襄河乳品广因",
            "workbench/ocr/paddle_ocr/中/part01/page_0107.txt:5 PaddleOCR 作襄河乳品厂因",
            "workbench/ocr/paddle_ocr/中/part01/page_0106.txt:34 前页作连云港食品总厂襄河乳品厂",
        ],
    },
    {
        "old": "业务由徐州医药公司统一一管理",
        "new": "业务由徐州医药公司统一管理",
        "section": "医药购销新海连药房段",
        "evidence": [
            "workbench/ocr/raw/中/part01/page_0133.txt:21 raw 作统一一管理",
            "workbench/ocr/paddle_ocr/中/part01/page_0133.txt:23 PaddleOCR 作统一管理",
        ],
    },
    {
        "old": "1956年7月，该药房晋升为云县）一市药品供应。",
        "new": "1956年7月，该药房晋升为徐州医药分公司新海连支公司，负责三县（当时徐州地区的东海、赣榆县和淮阴地区的灌云县）一市药品供应。",
        "section": "医药购销新海连药房段",
        "evidence": [
            "workbench/ocr/raw/中/part01/page_0133.txt:24-25 raw 漏失晋升机构名，仅余云县）一市药品供应",
            "workbench/ocr/paddle_ocr/中/part01/page_0133.txt:27-28 PaddleOCR 作徐州医药分公司新海连支公司，负责三县...云县)一市药品供应",
        ],
    },
    {
        "old": "<h4>六、祖国统一一联谊、对外联络委员会</h4>",
        "new": "<h4>六、祖国统一联谊、对外联络委员会</h4>",
        "section": "政协祖国统一联谊对外联络委员会标题",
        "evidence": [
            "workbench/ocr/raw/中/part02/page_0543.txt:4 raw 标题作祖国统一一联谊",
            "workbench/ocr/raw/中/part02/page_0543.txt:7 同页正文作改称祖国统一联谊、对外联络委员会",
            "workbench/ocr/raw/中/part02/page_0543.txt:10 同页成员名单作祖国统一联谊、对外联络委员会",
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
        "note": "只修主阅读版中 raw/PaddleOCR 或同页上下文闭合的短片段；未展示、未嵌入页图。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 高置信 OCR 错字补修第二十七批：医药食品政协短片段",
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
        "- 只修 `output/final_reader/连云港市志_全书.html`，不改 OCR 原文。",
        "- 未全局替换 `统一一`、`广因`、`云县）一市` 等模式。",
        "- 未处理源页证据仍弱的医学术语、人大视察段和大段转换异常文本。",
        "- 未展示、未嵌入页图。",
        "",
    ]
    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(f"changed={sum(item['count'] for item in applied)}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()
