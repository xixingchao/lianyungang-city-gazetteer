# -*- coding: utf-8 -*-
"""Nineteenth batch: small PaddleOCR-backed biography fixes."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_MD = ROOT / "output" / "reports" / "reader_high_confidence_ocr_typos_batch19_biography_short_paddle_20260705.md"
REPORT_JSON = ROOT / "output" / "reports" / "reader_high_confidence_ocr_typos_batch19_biography_short_paddle_20260705.json"

CHANGES = [
    {
        "old": "1951～1960年任新海油厂分广厂长。",
        "new": "1951～1960年任新海油厂分厂厂长。",
        "section": "上官寿元简介",
        "evidence": [
            "workbench/ocr/raw/下/part02/page_0370.txt:24-25 raw 作分广厂长",
            "workbench/ocr/paddle_ocr/下/part02/page_0370.txt:24-25 PaddleOCR 作分厂厂长",
        ],
    },
    {
        "old": "王太岚(1939 ~，）山东省东阿县人。",
        "new": "王太岚(1939~) 山东省东阿县人。",
        "section": "王太岚简介",
        "evidence": [
            "workbench/ocr/raw/下/part02/page_0397.txt:41-42 raw 存在跨行括号错识",
            "workbench/ocr/paddle_ocr/下/part02/page_0397.txt:37 PaddleOCR 作王太岚(1939~) 山东省东阿县人。",
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
        "note": "只修两处页级 PaddleOCR 明确反证的简介短片段。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 高置信 OCR 错字补修第十九批：人物简介短片段",
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
        "- `民国33年人山东抗大学习` 与 `同年人南京体育学院学习` 虽疑似 `入`，但当前 raw/PaddleOCR 同作 `人`，本批不猜改。",
        "- 未展示、未嵌入页图。",
        "",
    ]
    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(f"changed={sum(item['count'] for item in applied)}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()
