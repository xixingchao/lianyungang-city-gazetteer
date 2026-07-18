# -*- coding: utf-8 -*-
"""Batch 54: verified industry factory-name OCR residue fixes."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_MD = ROOT / "output" / "reports" / "reader_high_confidence_ocr_typos_batch54_industry_factory_short_20260706.md"
REPORT_JSON = ROOT / "output" / "reports" / "reader_high_confidence_ocr_typos_batch54_industry_factory_short_20260706.json"
PROGRESS_MD = ROOT / "output" / "reports" / "progress" / "20260706_高置信OCR错字补修第五十四批_工业厂名短片段.md"

CHANGES = [
    {
        "old": "新海电厂附属电机广分别开始生产小型变压器",
        "new": "新海电厂附属电机厂分别开始生产小型变压器",
        "section": "电工电器及材料概述段",
        "evidence": [
            "workbench/ocr/paddle_ocr/中/part01/page_0218.txt:31 作新海电厂附属电机厂",
            "workbench/ocr/raw/中/part01/page_0218.txt:31 为新海电厂附属电机广残留",
        ],
    },
    {
        "old": "海州电器广开始生产QJ3减压启动器",
        "new": "海州电器厂开始生产QJ3减压启动器",
        "section": "电工电器及材料概述段",
        "evidence": [
            "workbench/ocr/paddle_ocr/中/part01/page_0219.txt:6 作海州电器厂",
            "workbench/ocr/raw/中/part01/page_0219.txt:6 为海州电器广残留",
        ],
    },
    {
        "old": "东辛农场水泥预制广、新浦区水泥制品广、市房产公司预制厂",
        "new": "东辛农场水泥预制厂、新浦区水泥制品厂、市房产公司预制厂",
        "section": "混凝土空心板企业段",
        "evidence": [
            "workbench/ocr/paddle_ocr/中/part01/page_0282.txt:7 作东辛农场水泥预制厂、新浦区水泥制品厂",
            "workbench/ocr/raw/中/part01/page_0282.txt:8 为预制广/制品广残留",
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
        "note": "只修 PaddleOCR/raw OCR 对照闭合、旧串唯一命中的工业厂名短片段；未展示、未嵌入页图。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 高置信 OCR 错字补修第五十四批：工业厂名短片段",
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
        "- 其他 `广` 字样未取得同页证据闭合，本批不处理。",
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
