# -*- coding: utf-8 -*-
"""Batch 59: verified remaining 工广 -> 工厂 short fixes."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_MD = ROOT / "output" / "reports" / "reader_high_confidence_ocr_typos_batch59_factory_short_20260706.md"
REPORT_JSON = ROOT / "output" / "reports" / "reader_high_confidence_ocr_typos_batch59_factory_short_20260706.json"
PROGRESS_MD = ROOT / "output" / "reports" / "progress" / "20260706_高置信OCR错字补修第五十九批_工厂短片段.md"

CHANGES = [
    {
        "old": "东海县横沟乡日用化工广；建于1988年的新浦精细化工厂",
        "new": "东海县横沟乡日用化工厂；建于1988年的新浦精细化工厂",
        "section": "乡镇化工企业结构段",
        "evidence": [
            "workbench/ocr/paddle_ocr/中/part01/page_0403.txt 作日用化工厂",
            "workbench/ocr/raw/中/part01/page_0403.txt:27 为日用化工广残留",
        ],
    },
    {
        "old": "监所附设工广或作坊",
        "new": "监所附设工厂或作坊",
        "section": "劳动改造组织段",
        "evidence": [
            "workbench/ocr/paddle_ocr/下/part01/page_0151.txt:6 作监所附设工厂或",
            "workbench/ocr/raw/下/part01/page_0151.txt:8 为工广残留",
        ],
    },
    {
        "old": "市第一文化馆在街头、工广、街道建立黑板报",
        "new": "市第一文化馆在街头、工厂、街道建立黑板报",
        "section": "阵地宣传段",
        "evidence": [
            "workbench/ocr/paddle_ocr/下/part02/page_0050.txt:23 作街头、工厂、街道",
            "workbench/ocr/raw/下/part02/page_0050.txt:24 为街头、工广、街道残留",
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
        "note": "只修 PaddleOCR/raw OCR 对照闭合、旧串唯一命中的工厂短片段；未展示、未嵌入页图。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 高置信 OCR 错字补修第五十九批：工厂短片段",
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
        "- `施工广泛使用` 与 `农村体育经济交流会` 为双源一致或跨词命中，不纳入修复。",
        "- `劳改队撤销，并人徐州第四监狱` 双源仍作 `并人`，不猜改。",
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
