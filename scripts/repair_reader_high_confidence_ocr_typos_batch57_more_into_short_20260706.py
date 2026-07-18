# -*- coding: utf-8 -*-
"""Batch 57: verified remaining 并入 OCR residue fixes."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_MD = ROOT / "output" / "reports" / "reader_high_confidence_ocr_typos_batch57_more_into_short_20260706.md"
REPORT_JSON = ROOT / "output" / "reports" / "reader_high_confidence_ocr_typos_batch57_more_into_short_20260706.json"
PROGRESS_MD = ROOT / "output" / "reports" / "progress" / "20260706_高置信OCR错字补修第五十七批_并入短片段.md"

CHANGES = [
    {
        "old": "盐务局公安科并人盐区公安分局",
        "new": "盐务局公安科并入盐区公安分局",
        "section": "云台公安分局沿革段",
        "evidence": [
            "workbench/ocr/paddle_ocr/下/part01/page_0064.txt:28 作并入盐区公安分局",
            "workbench/ocr/raw/下/part01/page_0064.txt:27 为并人残留",
        ],
    },
    {
        "old": "其中并人成人中专112人，并人成人高校22人",
        "new": "其中并入成人中专112人，并入成人高校22人",
        "section": "农民教育中心校段",
        "evidence": [
            "workbench/ocr/paddle_ocr/下/part01/page_0397.txt:23-24 作并入成人中专、并入成人高校",
            "workbench/ocr/raw/下/part01/page_0397.txt:25 为并人成人高校残留；主阅读版同句有并人成人中专残留",
        ],
    },
    {
        "old": "江苏省立第八师范学校并人江苏省立十中学",
        "new": "江苏省立第八师范学校并入江苏省立十中学",
        "section": "中等师范学校发展概况段",
        "evidence": [
            "workbench/ocr/paddle_ocr/下/part01/page_0387.txt:7 作并入江苏省立十中学",
            "workbench/ocr/raw/下/part01/page_0387.txt:8 为并人残留",
        ],
    },
    {
        "old": "月并人灌云师范学校，成为学校的函授部",
        "new": "月并入灌云师范学校，成为学校的函授部",
        "section": "灌云县教师进修学校段",
        "evidence": [
            "workbench/ocr/paddle_ocr/下/part01/page_0401.txt:18 作并入灌云师范学校",
            "workbench/ocr/raw/下/part01/page_0401.txt:18 为并人残留",
        ],
    },
    {
        "old": "1959年秋，并人赣榆县师范学校设教师进修部",
        "new": "1959年秋，并入赣榆县师范学校设教师进修部",
        "section": "赣榆县教师进修学校段",
        "evidence": [
            "workbench/ocr/paddle_ocr/下/part01/page_0401.txt:33 作并入赣榆县师范学校",
            "workbench/ocr/raw/下/part01/page_0401.txt:33 为并人残留",
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
        "note": "只修 PaddleOCR/raw OCR 对照闭合、旧串唯一命中的并入短片段；未展示、未嵌入页图。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 高置信 OCR 错字补修第五十七批：并入短片段",
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
        "- 劳改队撤销并入徐州第四监狱一处 PaddleOCR 仍作 `并人`，本批不猜改。",
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
