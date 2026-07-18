# -*- coding: utf-8 -*-
"""Batch 53: verified labor and united-front OCR residue fixes."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_MD = ROOT / "output" / "reports" / "reader_high_confidence_ocr_typos_batch53_labor_united_front_short_20260706.md"
REPORT_JSON = ROOT / "output" / "reports" / "reader_high_confidence_ocr_typos_batch53_labor_united_front_short_20260706.json"
PROGRESS_MD = ROOT / "output" / "reports" / "progress" / "20260706_高置信OCR错字补修第五十三批_工会统战短片段.md"

CHANGES = [
    {
        "old": "工会会员因人股集资，购票可享受8折优待",
        "new": "工会会员因入股集资，购票可享受8折优待",
        "section": "职工俱乐部电影放映段",
        "evidence": [
            "workbench/ocr/paddle_ocr/下/part01/page_0318.txt:19 作因入股集资",
            "workbench/ocr/raw/下/part01/page_0318.txt:19 为因人股集资残留",
        ],
    },
    {
        "old": "海运工会人股集资，并动员工人参加义务劳动",
        "new": "海运工会入股集资，并动员工人参加义务劳动",
        "section": "工人电影院筹建段",
        "evidence": [
            "workbench/ocr/paddle_ocr/下/part02/page_0042.txt:27 作海运工会入股集资",
            "workbench/ocr/raw/下/part02/page_0042.txt:27 为海运工会人股集资残留",
        ],
    },
    {
        "old": "实行公私合营并人国营商店",
        "new": "实行公私合营并入国营商店",
        "section": "统一战线私营商业改造段",
        "evidence": [
            "workbench/ocr/paddle_ocr/中/part02/page_0452.txt:25 作并入国营商店",
            "output/final_reader/连云港市志_全书.html 原文为并人国营商店残留",
        ],
    },
    {
        "old": "各负盈号的合作小组或单独经营",
        "new": "各负盈亏的合作小组或单独经营",
        "section": "统一战线私营商业改造段",
        "evidence": [
            "workbench/ocr/paddle_ocr/中/part02/page_0452.txt:26 作各负盈亏",
            "workbench/ocr/raw/中/part02/page_0452.txt:27 为各负盈号残留",
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
        "note": "只修 PaddleOCR/raw OCR 对照闭合、旧串唯一命中的工会与统战短片段；未展示、未嵌入页图。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 高置信 OCR 错字补修第五十三批：工会统战短片段",
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
        "- `并人沭阳县` 目前缺少同页 PaddleOCR 直接支撑，本批不猜改。",
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
