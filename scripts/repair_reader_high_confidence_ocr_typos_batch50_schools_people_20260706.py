# -*- coding: utf-8 -*-
"""Batch 50: verified school and people-name OCR residue fixes."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_MD = ROOT / "output" / "reports" / "reader_high_confidence_ocr_typos_batch50_schools_people_20260706.md"
REPORT_JSON = ROOT / "output" / "reports" / "reader_high_confidence_ocr_typos_batch50_schools_people_20260706.json"
PROGRESS_MD = ROOT / "output" / "reports" / "progress" / "20260706_高置信OCR错字补修第五十批_学校与人物短片段.md"

CHANGES = [
    {
        "old": "蕃薇中学、陇东中学",
        "new": "蔷薇中学、陇东中学",
        "section": "中学学制学校名段",
        "evidence": [
            "workbench/ocr/paddle_ocr/下/part01/page_0375.txt:12 作蔷薇中学、陇东中学、延安中学...",
            "workbench/ocr/raw/下/part01/page_0375.txt:12 为蕃薇中学残留，PaddleOCR 校正为蔷薇中学",
        ],
    },
    {
        "old": "连云6港市蕃薇中学",
        "new": "连云港市蔷薇中学",
        "section": "市级体育传统项目学校名单段",
        "evidence": [
            "workbench/ocr/paddle_ocr/下/part02/page_0229.txt:35 作连云6港市蔷薇中学；同页仅残留多余 6",
            "workbench/ocr/raw/下/part02/page_0229.txt:33 为连云6港市蕃薇中学残留",
            "workbench/ocr/paddle_ocr/下/part01/page_0379.txt 与 page_0382.txt 表格均作蔷薇中学",
        ],
    },
    {
        "old": "导淮入江人海之研究",
        "new": "导淮入江入海之研究",
        "section": "武同举著作名段",
        "evidence": [
            "workbench/ocr/paddle_ocr/下/part02/page_0350.txt:28 作导淮入江入海之研究",
            "workbench/ocr/raw/下/part02/page_0350.txt:27 为导淮入江人海之研究残留",
        ],
    },
    {
        "old": "泗、沂、述分治合治之研究",
        "new": "泗、沂、沭分治合治之研究",
        "section": "武同举沂沭著作名段",
        "evidence": [
            "workbench/ocr/paddle_ocr/下/part02/page_0350.txt:29 作泗、沂、沭分治合治之研究",
            "workbench/ocr/raw/下/part02/page_0350.txt:28 为泗、沂、述分治合治之研究残留",
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
        "note": "只修 PaddleOCR 与同章表格证据闭合、旧串唯一命中的学校与人物短片段；未展示、未嵌入页图。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 高置信 OCR 错字补修第五十批：学校与人物短片段",
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
        "- `新浦据蓄薇河` 等附录古文段源证不足，本批不猜改。",
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
