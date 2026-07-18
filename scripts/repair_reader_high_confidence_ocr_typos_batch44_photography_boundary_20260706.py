# -*- coding: utf-8 -*-
"""Batch 44: verified photography paragraph boundary fixes."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_MD = ROOT / "output" / "reports" / "reader_high_confidence_ocr_typos_batch44_photography_boundary_20260706.md"
REPORT_JSON = ROOT / "output" / "reports" / "reader_high_confidence_ocr_typos_batch44_photography_boundary_20260706.json"

CHANGES = [
    {
        "old": "1990年成立连云港市人1959年，报社记者李训敦",
        "new": "1990年成立连云港市人像摄影协会、连云港港务局摄影协会、锦屏磷矿摄影协会。1959年，报社记者李训敦",
        "section": "文化摄影协会跨页断裂",
        "evidence": [
            "workbench/ocr/paddle_ocr/下/part02/page_0023.txt:39 作1990年成立连云港市人",
            "workbench/ocr/paddle_ocr/下/part02/page_0024.txt:3 作像摄影协会、连云港港务局摄影协会、锦屏磷矿摄影协会。",
        ],
    },
    {
        "old": "1989年，连云港市文化局为庆祝连云本市展出。",
        "new": "1989年，连云港市文化局为庆祝连云港市与日本堺市结为友好城市5周年而举办“连云港赞”美术、摄影作品展览，作品还赴日本堺市展出。",
        "section": "文化摄影友城五周年展览断裂",
        "evidence": [
            "workbench/ocr/paddle_ocr/下/part02/page_0024.txt:19-21 作庆祝连云港市与日本堺市结为友好城市5周年而举办“连云港赞”美术、摄影作品展览，作品还赴日本堺市展出。",
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
        "note": "只修页级 PaddleOCR 闭合且旧串唯一命中的文化摄影小节断裂；未展示、未嵌入页图。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 高置信 OCR 错字补修第四十四批：摄影小节断裂",
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
        "- 只处理下册文化卷摄影小节 `page_0023` 至 `page_0024` 已闭合断裂。",
        "- 未展示、未嵌入页图。",
        "",
    ]
    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(f"changed={sum(item['count'] for item in applied)}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()
