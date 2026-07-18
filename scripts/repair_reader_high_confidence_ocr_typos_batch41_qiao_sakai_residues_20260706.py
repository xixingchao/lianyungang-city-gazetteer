# -*- coding: utf-8 -*-
"""Batch 41: remaining verified qiaojuan/Sakai short fixes."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_MD = ROOT / "output" / "reports" / "reader_high_confidence_ocr_typos_batch41_qiao_sakai_residues_20260706.md"
REPORT_JSON = ROOT / "output" / "reports" / "reader_high_confidence_ocr_typos_batch41_qiao_sakai_residues_20260706.json"

CHANGES = [
    {
        "old": "侨券中担任县、局级以上职务的10人、高级专业技术职务32人",
        "new": "侨眷中担任县、局级以上职务的10人、高级专业技术职务32人",
        "section": "中共地方组织侨务工作概述",
        "evidence": [
            "workbench/ocr/paddle_ocr/中/part02/page_0455.txt:11 作侨眷中担任县、局级以上职务",
        ],
    },
    {
        "old": "被连云港市政府作为馈赠礼品送日本市政府。",
        "new": "被连云港市政府作为馈赠礼品送日本堺市政府。",
        "section": "刺绣厂中日友好双面绣台",
        "evidence": [
            "workbench/ocr/paddle_ocr/中/part01/page_0042.txt:41 作日本堺市政府",
        ],
    },
    {
        "old": "落实侨胞、侨着政策案3件、3人",
        "new": "落实侨胞、侨眷政策案3件、3人",
        "section": "法院统战案件复查",
        "evidence": [
            "workbench/ocr/paddle_ocr/下/part01/page_0139.txt:16 作侨胞、侨眷政策案",
        ],
    },
    {
        "old": "归侨、侨在“文革”中被查抄遗留问题的通知",
        "new": "归侨、侨眷在“文革”中被查抄遗留问题的通知",
        "section": "侨务政策查抄遗留问题通知",
        "evidence": [
            "workbench/ocr/paddle_ocr/下/part01/page_0300.txt:12 作归侨、侨眷在文革中被查抄",
        ],
    },
    {
        "old": "作品在日本市”少儿书画展。",
        "new": "作品在日本堺市”少儿书画展。",
        "section": "东海县实验小学少儿书画展",
        "evidence": [
            "workbench/ocr/paddle_ocr/下/part01/page_0356.txt:32 作日本堺市少儿书画展",
        ],
    },
    {
        "old": "吕布偷袭下邸掳去刘备着属",
        "new": "吕布偷袭下邳掳去刘备眷属",
        "section": "糜竺传刘备眷属",
        "evidence": [
            "workbench/ocr/paddle_ocr/下/part02/page_0343.txt:18 作吕布偷袭下邳掳去刘备眷属",
        ],
    },
    {
        "old": "作品还赴日本市展出。",
        "new": "作品还赴日本堺市展出。",
        "section": "摄影艺术展赴日展出",
        "evidence": [
            "workbench/ocr/paddle_ocr/下/part02/page_0024.txt:18 作作品还赴日本堺市展出",
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
        "note": "只修已由 PaddleOCR 闭合的侨眷、眷属、堺市短片段；未展示、未嵌入页图。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 高置信 OCR 错字补修第四十一批：侨眷与堺市短片段",
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
