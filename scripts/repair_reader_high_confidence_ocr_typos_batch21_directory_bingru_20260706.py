# -*- coding: utf-8 -*-
"""Twenty-first batch: PaddleOCR-backed directory, bingru, and place-name fixes."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_MD = ROOT / "output" / "reports" / "reader_high_confidence_ocr_typos_batch21_directory_bingru_20260706.md"
REPORT_JSON = ROOT / "output" / "reports" / "reader_high_confidence_ocr_typos_batch21_directory_bingru_20260706.json"

CHANGES = [
    {
        "old": "参加过南麻、临胸、沙市集等战役",
        "new": "参加过南麻、临朐、沙市集等战役",
        "section": "支前担架队段",
        "evidence": [
            "workbench/ocr/raw/中/part02/page_0412.txt:5 raw 作临胸",
            "workbench/ocr/paddle_ocr/中/part02/page_0412.txt:5 PaddleOCR 作临朐",
        ],
    },
    {
        "old": "先后编制了案卷目录、文件自录、专题文件目录、文件、人物卡片等",
        "new": "先后编制了案卷目录、文件目录、专题文件目录、文件、人物卡片等",
        "section": "连云港市档案馆检索工具段",
        "evidence": [
            "workbench/ocr/raw/下/part02/page_0054.txt:26 raw 作文件自录",
            "workbench/ocr/paddle_ocr/下/part02/page_0054.txt:26 PaddleOCR 作文件目录",
        ],
    },
    {
        "old": "题文件自录118册，卡片21000张，开放档案全引文件目录56册，资料总登记自录24册，",
        "new": "面提供档案服务，编制了多种科学适用的检索工具和参考资料，其中案卷目录341册，专题文件目录118册，卡片21000张，开放档案全引文件目录56册，资料总登记目录24册，",
        "section": "赣榆县档案馆检索工具段",
        "evidence": [
            "workbench/ocr/raw/下/part02/page_0055.txt:13 raw 漏行且作题文件自录、资料总登记自录",
            "workbench/ocr/paddle_ocr/下/part02/page_0055.txt:12-14 PaddleOCR 给出完整句与目录",
        ],
    },
    {
        "old": "书标、自录卡、书袋卡等统一一作出规定",
        "new": "书标、目录卡、书袋卡等统一作出规定",
        "section": "图书馆辅导组段",
        "evidence": [
            "workbench/ocr/raw/下/part02/page_0067.txt:36 raw 作自录卡、统一一作出规定",
            "workbench/ocr/paddle_ocr/下/part02/page_0067.txt:36 PaddleOCR 作目录卡、统一作出规定",
        ],
    },
    {
        "old": "市财政局监察科并人市审计局",
        "new": "市财政局监察科并入市审计局",
        "section": "财政监察段",
        "evidence": [
            "workbench/ocr/raw/中/part02/page_0309.txt:15 raw 作并人市审计局",
            "workbench/ocr/paddle_ocr/中/part02/page_0309.txt:15 PaddleOCR 作并入市审计局",
        ],
    },
    {
        "old": "从市财政局分出，并人市人行。",
        "new": "从市财政局分出，并入市人行。",
        "section": "建设银行机构沿革段",
        "evidence": [
            "workbench/ocr/raw/中/part02/page_0347.txt:21 raw 作并人市人行",
            "workbench/ocr/paddle_ocr/中/part02/page_0347.txt:21 PaddleOCR 作并入市人行",
        ],
    },
]


def main() -> None:
    html = HTML.read_text(encoding="utf-8")
    applied = []
    for change in CHANGES:
        count = html.count(change["old"])
        if count != 1:
            raise RuntimeError(f"expected one hit for {change['section']}, found {count}")
        html = html.replace(change["old"], change["new"])
        applied.append({**change, "count": count})
    HTML.write_text(html, encoding="utf-8")

    payload = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "reader": str(HTML.relative_to(ROOT)).replace("\\", "/"),
        "changes": applied,
        "note": "只修页级 PaddleOCR 与 raw OCR 对照闭合的目录、自录、并入和临朐短片段。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 高置信 OCR 错字补修第二十一批：目录、并入与临朐短片段",
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
        "- 只修主阅读版；不改中间 OCR 原文。",
        "- 不批量替换全部自录/并人/临胸，只处理本批已回源闭合项。",
        "- 未展示、未嵌入页图。",
        "",
    ]
    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(f"changed={sum(item['count'] for item in applied)}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()
