# -*- coding: utf-8 -*-
"""Seventeenth batch: two page-level PaddleOCR backed 入/人 repairs."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_MD = ROOT / "output" / "reports" / "reader_high_confidence_ocr_typos_batch17_ru_candidates_20260705.md"
REPORT_JSON = ROOT / "output" / "reports" / "reader_high_confidence_ocr_typos_batch17_ru_candidates_20260705.json"

CHANGES = [
    {
        "old": "板浦江苏省第八师范并人海州十一中学，成立东海中学",
        "new": "板浦江苏省第八师范并入海州十一中学，成立东海中学",
        "section": "中等教育发展概况",
        "evidence": [
            "workbench/ocr/raw/下/part01/page_0374.txt:34 raw 作 `并人`",
            "workbench/ocr/paddle_ocr/下/part01/page_0374.txt:44 PaddleOCR 作 `并入`",
        ],
    },
    {
        "old": "14岁人灌云县立初级中学，品学兼优",
        "new": "14岁入灌云县立初级中学，品学兼优",
        "section": "张明传",
        "evidence": [
            "workbench/ocr/raw/下/part02/page_0374.txt:40 raw 作 `14岁人`",
            "workbench/ocr/paddle_ocr/下/part02/page_0374.txt:41 PaddleOCR 作 `14岁入`",
        ],
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
        "note": "只修两个已由页级 PaddleOCR 明确反证的 入/人 短片段。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 高置信 OCR 错字补修第十七批：入/人短片段",
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
        "- 只修主阅读版；不改中间 OCR 原文。",
        "- 不批量替换 `并人/人灌云/加人/考人`，仅处理本批两处精确证据项。",
        "- 未展示、未嵌入页图。",
        "",
    ]
    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(f"changed={sum(item['count'] for item in applied)}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()
