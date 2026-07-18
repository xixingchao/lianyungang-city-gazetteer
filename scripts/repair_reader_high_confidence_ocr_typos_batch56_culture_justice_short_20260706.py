# -*- coding: utf-8 -*-
"""Batch 56: verified culture and justice OCR residue fixes."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_MD = ROOT / "output" / "reports" / "reader_high_confidence_ocr_typos_batch56_culture_justice_short_20260706.md"
REPORT_JSON = ROOT / "output" / "reports" / "reader_high_confidence_ocr_typos_batch56_culture_justice_short_20260706.json"
PROGRESS_MD = ROOT / "output" / "reports" / "progress" / "20260706_高置信OCR错字补修第五十六批_文化司法短片段.md"

CHANGES = [
    {
        "old": "编繁《连云港市志》",
        "new": "编纂《连云港市志》",
        "section": "社会科学机构段",
        "evidence": [
            "workbench/ocr/paddle_ocr/下/part01/page_0458.txt:12 作编纂《连云港市志》",
            "workbench/ocr/raw/下/part01/page_0458.txt:12 为编繁《连云港市志》残留",
        ],
    },
    {
        "old": "组织史资料》的编繁工作",
        "new": "组织史资料》的编纂工作",
        "section": "档案馆史料编研段",
        "evidence": [
            "workbench/ocr/paddle_ocr/下/part02/page_0054.txt:35 作编纂工作",
            "workbench/ocr/raw/下/part02/page_0054.txt:35 为编繁工作残留",
        ],
    },
    {
        "old": "“诊语卷”三部分为一体。1986年，姜威编繁的《西游记外传》",
        "new": "“谚语卷”三部分为一体。1986年，姜威编纂的《西游记外传》",
        "section": "民间文学集成段",
        "evidence": [
            "workbench/ocr/paddle_ocr/下/part02/page_0020.txt:4-5 作谚语卷、姜威编纂的《西游记外传》",
            "workbench/ocr/raw/下/part02/page_0020.txt:4-5 为诊语卷、编繁残留",
        ],
    },
    {
        "old": "《玄辩学》、《猪八戒出生记》",
        "new": "《玄奘辩学》、《猪八戒出生记》",
        "section": "民间文学集成段",
        "evidence": [
            "workbench/ocr/paddle_ocr/下/part02/page_0020.txt:5 作《玄奘辩学》",
            "workbench/ocr/raw/下/part02/page_0020.txt:5 为《玄辩学》残留",
        ],
    },
    {
        "old": "2月，淮北盐特区司法科并人市法院。3月，看守所移交市公安局",
        "new": "2月，淮北盐特区司法科并入市法院。3月，看守所移交市公安局",
        "section": "人民审判机构段",
        "evidence": [
            "workbench/ocr/paddle_ocr/下/part01/page_0114.txt:15-16 作司法科并入市法院",
            "workbench/ocr/raw/下/part01/page_0114.txt:15 为司法科并人残留",
        ],
    },
    {
        "old": "1953年2月，淮北盐特区司法科并人市法院。1954年",
        "new": "1953年2月，淮北盐特区司法科并入市法院。1954年",
        "section": "司法行政机构段",
        "evidence": [
            "workbench/ocr/paddle_ocr/下/part01/page_0142.txt:7 作司法科并入市法院",
            "workbench/ocr/raw/下/part01/page_0142.txt:7 为司法科并人残留",
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
        "note": "只修 PaddleOCR/raw OCR 对照闭合、旧串唯一命中的文化与司法短片段；未展示、未嵌入页图。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 高置信 OCR 错字补修第五十六批：文化司法短片段",
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
        "- 书末编纂始末页仍缺更强页级证据，本批不处理。",
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
