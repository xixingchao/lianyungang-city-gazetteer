# -*- coding: utf-8 -*-
"""Thirtieth batch: PaddleOCR-backed cadre and labor OCR fixes."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_MD = ROOT / "output" / "reports" / "reader_high_confidence_ocr_typos_batch30_cadre_labor_20260706.md"
REPORT_JSON = ROOT / "output" / "reports" / "reader_high_confidence_ocr_typos_batch30_cadre_labor_20260706.json"

CHANGES = [
    {
        "old": "科、股级千部1097人",
        "new": "科、股级干部1097人",
        "section": "干部考察分批段",
        "evidence": [
            "workbench/ocr/raw/下/part01/page_0216.txt:9 raw 作科、股级千部1097人",
            "workbench/ocr/paddle_ocr/下/part01/page_0216.txt:9 PaddleOCR 作科、股级干部1097人",
        ],
    },
    {
        "old": "脱产于部（包括工程技术人员和中级以上医务人员）",
        "new": "脱产干部（包括工程技术人员和中级以上医务人员）",
        "section": "干部考察鉴定段",
        "evidence": [
            "workbench/ocr/raw/下/part01/page_0216.txt:10 raw 作脱产于部",
            "workbench/ocr/paddle_ocr/下/part01/page_0216.txt:10 PaddleOCR 作脱产干部",
        ],
    },
    {
        "old": "城市于部和职工家属",
        "new": "城市干部和职工家属",
        "section": "精简职工对象段",
        "evidence": [
            "workbench/ocr/raw/下/part01/page_0248.txt:8 raw 作城市于部和职工家属",
            "workbench/ocr/paddle_ocr/下/part01/page_0248.txt:7 PaddleOCR 作城市干部和职工家属",
        ],
    },
    {
        "old": "下放千部享受同工种的津贴标准",
        "new": "下放干部享受同工种的津贴标准",
        "section": "煤矿井下津贴标准段",
        "evidence": [
            "workbench/ocr/raw/下/part01/page_0264.txt:15 raw 作千部享受同工种的津贴标准",
            "workbench/ocr/paddle_ocr/下/part01/page_0264.txt:14-15 PaddleOCR 作下放干部享受同工种的津贴标准",
        ],
    },
    {
        "old": "在并下连续工作3年或累计满5年的",
        "new": "在井下连续工作3年或累计满5年的",
        "section": "煤矿井下津贴待遇基数段",
        "evidence": [
            "workbench/ocr/raw/下/part01/page_0264.txt:16 raw 作在并下连续工作",
            "workbench/ocr/paddle_ocr/下/part01/page_0264.txt:16 PaddleOCR 作在井下连续工作",
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
        "note": "只修 raw/PaddleOCR 可闭合的干部、人事、劳动短片段；未展示、未嵌入页图。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 高置信 OCR 错字补修第三十批：干部与劳动短片段",
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
        "- 未全局替换 `千部/干部`、`于部/干部`、`并下/井下` 等模式。",
        "- `党政领导于部`、`于部考察工作` 等同页 PaddleOCR 未能给出更强证据，本批暂缓。",
        "- 未展示、未嵌入页图。",
        "",
    ]
    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(f"changed={sum(item['count'] for item in applied)}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()
