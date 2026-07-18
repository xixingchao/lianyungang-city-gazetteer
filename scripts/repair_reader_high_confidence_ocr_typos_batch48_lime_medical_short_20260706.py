# -*- coding: utf-8 -*-
"""Batch 48: verified lime factory and medical short OCR fixes."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_MD = ROOT / "output" / "reports" / "reader_high_confidence_ocr_typos_batch48_lime_medical_short_20260706.md"
REPORT_JSON = ROOT / "output" / "reports" / "reader_high_confidence_ocr_typos_batch48_lime_medical_short_20260706.json"

CHANGES = [
    {
        "old": "1984年春，市石灰广为扩大生产，进行技改扩建，投资40万元，新建一座17米高的双筒立窑，座51米高的砖混结构的烟简。",
        "new": "1984年春，市石灰厂为扩大生产，进行技改扩建，投资40万元，新建一座17米高的双筒立窑，一座51米高的砖混结构的烟筒。",
        "section": "石灰厂技改扩建段",
        "evidence": ["workbench/ocr/paddle_ocr/中/part01/page_0278.txt:35 作市石灰厂为扩大生产", "workbench/ocr/paddle_ocr/中/part01/page_0279.txt:4 作一座51米高的砖混结构的烟筒"],
    },
    {
        "old": "因港口扩建需要，沟石灰厂迁至平山西侧",
        "new": "因港口扩建需要，墟沟石灰厂迁至平山西侧",
        "section": "墟沟石灰厂迁建段",
        "evidence": ["workbench/ocr/paddle_ocr/中/part01/page_0279.txt:6 作墟沟石灰厂迁至平山西侧"],
    },
    {
        "old": "连云港市第建筑公司（后简称市一建）与市石灰厂进行商",
        "new": "连云港市第一建筑公司（后简称市一建）与市石灰厂进行磋商",
        "section": "市一建与石灰厂磋商段",
        "evidence": ["workbench/ocr/paddle_ocr/中/part01/page_0279.txt:7-8 作连云港市第一建筑公司、进行磋商"],
    },
    {
        "old": "进行丙酮酸嗨测定、性病LISR测定",
        "new": "进行丙酮酸晦测定、性病LISR测定",
        "section": "检验科1988年检测项目段",
        "evidence": ["workbench/ocr/paddle_ocr/下/part02/page_0188.txt:37-38 作进行丙酮酸晦测定、性病LISR测定"],
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
        "note": "只修页级 PaddleOCR 闭合且旧串唯一命中的石灰厂与医学短片段；未展示、未嵌入页图。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 高置信 OCR 错字补修第四十八批：石灰厂与医学短片段",
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
        "- `于部违法乱纪`、`麦粘肿`、`B2一微蛋白`、`LISR` 等页级 OCR 仍未给出更正证据，本批不处理。",
        "- 未展示、未嵌入页图。",
        "",
    ]
    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(f"changed={sum(item['count'] for item in applied)}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()
