# -*- coding: utf-8 -*-
"""Batch 40: small verified qiaojuan/Sakai follow-up fixes."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_MD = ROOT / "output" / "reports" / "reader_high_confidence_ocr_typos_batch40_qiao_sakai_residues_20260706.md"
REPORT_JSON = ROOT / "output" / "reports" / "reader_high_confidence_ocr_typos_batch40_qiao_sakai_residues_20260706.json"

CHANGES = [
    {
        "old": "连云港市先后与日本市、韩国木浦市、澳大利亚大吉郎市等城市结为友好城市。",
        "new": "连云港市先后与日本堺市、韩国木浦市、澳大利亚大吉郎市等城市结为友好城市。",
        "section": "政府扩大开放友好城市",
        "evidence": [
            "workbench/ocr/raw/中/part02/page_0495.txt:24 raw 作日本市",
            "workbench/ocr/paddle_ocr/中/part02/page_0495.txt:24 PaddleOCR 作日本堺市",
        ],
    },
    {
        "old": "消除了归侨、侨着的思想顾虑。",
        "new": "消除了归侨、侨眷的思想顾虑。",
        "section": "清理归侨侨眷档案思想顾虑",
        "evidence": [
            "workbench/ocr/raw/下/part01/page_0300.txt:10 raw 作侨着",
            "workbench/ocr/paddle_ocr/下/part01/page_0300.txt:10 PaddleOCR 作侨眷",
        ],
    },
    {
        "old": "对全市归侨、侨着在“文化大革命”中被查抄财物的退还情况",
        "new": "对全市归侨、侨眷在“文化大革命”中被查抄财物的退还情况",
        "section": "归侨侨眷查抄财物退还",
        "evidence": [
            "workbench/ocr/raw/下/part01/page_0300.txt:12-13 raw 作侨着",
            "workbench/ocr/paddle_ocr/下/part01/page_0300.txt:12-13 PaddleOCR 作侨眷",
        ],
    },
    {
        "old": "兴农百业知识竞赛活动，举办归侨、侨着、青年学生夏令营等活动。",
        "new": "兴农百业知识竞赛活动，举办归侨、侨眷、青年学生夏令营等活动。",
        "section": "团市委归侨侨眷青年学生夏令营",
        "evidence": [
            "workbench/ocr/raw/下/part01/page_0323.txt:37 raw 作侨着",
            "workbench/ocr/paddle_ocr/下/part01/page_0323.txt:37 PaddleOCR 作侨眷",
        ],
    },
    {
        "old": "被日本市美协和博物馆收藏，其组画《三国圣贤图》被甘本大阪佛教协会收藏。",
        "new": "被日本堺市美协和博物馆收藏，其组画《三国圣贤图》被日本大阪佛教协会收藏。",
        "section": "王宏喜赴日画作收藏",
        "evidence": [
            "workbench/ocr/raw/下/part02/page_0398.txt:8-9 raw 作日本市/甘本大阪",
            "workbench/ocr/paddle_ocr/下/part02/page_0398.txt:8-9 PaddleOCR 作日本堺市/日本大阪",
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
        "note": "Batch39 后续：只修已由 raw/PaddleOCR 闭合的侨眷、堺市和日本大阪短片段；未展示、未嵌入页图。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 高置信 OCR 错字补修第四十批：侨眷与堺市残留补修",
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
        "- 未处理尚未定位源页的疑似残留。",
        "- 未展示、未嵌入页图。",
        "",
    ]
    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(f"changed={sum(item['count'] for item in applied)}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()
