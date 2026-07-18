# -*- coding: utf-8 -*-
"""Batch 42: one verified medical technology OCR fix."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_MD = ROOT / "output" / "reports" / "reader_high_confidence_ocr_typos_batch42_medical_short_20260706.md"
REPORT_JSON = ROOT / "output" / "reports" / "reader_high_confidence_ocr_typos_batch42_medical_short_20260706.json"

CHANGES = [
    {
        "old": "1959年，市人民医院进行再植牙手术及凳下腺、舌下腺、颌骨等囊肿的摘除手术。",
        "new": "1959年，新海连市立医院施行牙再植术、颌下腮、舌下腺、颌骨囊肿摘除术。",
        "section": "科技应用与推广医疗技术段",
        "evidence": [
            "workbench/ocr/paddle_ocr/下/part01/page_0449.txt:14-15 作新海连市立医院施行牙再植术、颌下腮、舌下腺、颌骨囊肿摘除术",
            "workbench/ocr/raw/下/part01/page_0449.txt:16-17 同样支持颌下腮、舌下腺、颌骨囊肿摘除术",
        ],
    },
]


def main() -> None:
    html = HTML.read_text(encoding="utf-8")
    applied = []
    for change in CHANGES:
        count = html.count(change["old"])
        if count != 1:
            raise RuntimeError(f"expected one hit for {change['section']}, found {count}: {change['old'][:80]}")
        html = html.replace(change["old"], change["new"])
        applied.append({**change, "count": count})
    HTML.write_text(html, encoding="utf-8")

    payload = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "reader": str(HTML.relative_to(ROOT)).replace("\\", "/"),
        "changes": applied,
        "note": "只修已由页级 PaddleOCR 与 raw OCR 闭合的医学技术短片段；未展示、未嵌入页图。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 高置信 OCR 错字补修第四十二批：医学技术短片段",
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
        "- `麦粘肿`、`B2一微蛋白`、`丙酮酸嗨`、`LISR` 暂未定位到同等强源页证据，本批不处理。",
        "- 未展示、未嵌入页图。",
        "",
    ]
    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(f"changed={sum(item['count'] for item in applied)}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()
