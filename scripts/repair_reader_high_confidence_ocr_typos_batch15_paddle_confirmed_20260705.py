# -*- coding: utf-8 -*-
"""Fifteenth batch: PaddleOCR-confirmed short repairs in the main reader."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_MD = ROOT / "output" / "reports" / "reader_high_confidence_ocr_typos_batch15_paddle_confirmed_20260705.md"
REPORT_JSON = ROOT / "output" / "reports" / "reader_high_confidence_ocr_typos_batch15_paddle_confirmed_20260705.json"

CHANGES = [
    {
        "old": "顽寇迄未得暹，爱刻石志念",
        "new": "顽寇迄未得逞，爰刻石志念",
        "section": "万寿山石刻跋文",
        "evidence": [
            "workbench/ocr/raw/下/part02/page_0106.txt:41 raw 作 `顽寇迄未得暹，爱刻石志念`",
            "workbench/ocr/paddle_ocr/下/part02/page_0106.txt:41 PaddleOCR 作 `顽寇迄未得逞，爰刻石志念`",
        ],
    },
    {
        "old": "参加暴动大楼。并决定以云台山为根据地",
        "new": "参加暴动的农民挥舞扁担镰刀，高呼“创共产，救穷人，除山霸，还山林”的口号，捣毁南北两个办公大楼。并决定以云台山为根据地",
        "section": "武同儒传",
        "evidence": [
            "workbench/ocr/raw/下/part02/page_0362.txt:28-29 raw 漏掉中间行，形成 `参加暴动/大楼`",
            "workbench/ocr/paddle_ocr/下/part02/page_0362.txt:29-31 PaddleOCR 补出 `参加暴动的农民挥舞扁担镰刀...捣毁南北两个办公大楼`",
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
        "note": "只修主阅读版中两处已由页级 PaddleOCR 反证/补足的短片段。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 高置信 OCR 错字补修第十五批：PaddleOCR 确证短片段",
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
        "- 不改中间 OCR 原文文件，只修主阅读版。",
        "- 不批量处理 `加入/考入` 等仍需逐条核对的候选。",
        "- 未展示、未嵌入页图。",
        "",
    ]
    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(f"changed={sum(item['count'] for item in applied)}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()
