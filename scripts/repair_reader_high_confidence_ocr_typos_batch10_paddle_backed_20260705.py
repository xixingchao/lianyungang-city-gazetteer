# -*- coding: utf-8 -*-
"""Tenth batch of high-confidence OCR repairs backed by page-level PaddleOCR."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_MD = ROOT / "output" / "reports" / "reader_high_confidence_ocr_typos_batch10_paddle_backed_20260705.md"
REPORT_JSON = ROOT / "output" / "reports" / "reader_high_confidence_ocr_typos_batch10_paddle_backed_20260705.json"

CHANGES = [
    ("内容的新编书自", "内容的新编书目", "文化曲艺", "workbench/ocr/paddle_ocr/下/part02/page_0032.txt"),
    ("杀县令，攻人会稽", "杀县令，攻入会稽", "起义起事", "workbench/ocr/paddle_ocr/下/part01/page_0154.txt"),
    ("领兵万余攻海州。巍胜在海州北二十里", "领兵万余攻海州。魏胜在海州北二十里", "魏胜抗金", "workbench/ocr/paddle_ocr/下/part01/page_0158.txt"),
    ("孙佳讯对《镜花缘》研究造谐较深", "孙佳讯对《镜花缘》研究造诣较深", "孙佳讯传", "workbench/ocr/paddle_ocr/下/part02/page_0366.txt"),
    ("《镜花缘海属传说辨辩证》", "《镜花缘海属传说辨证》", "孙佳讯传", "workbench/ocr/paddle_ocr/下/part02/page_0366.txt"),
]

DEFERRED = [
    "`战船干余艘` 疑似 `战船千余艘`，但暂未找到直接页级 OCR 证据，本批不改。",
    "`金兵主师蒙恬镇国` 页级 OCR 仍为 `主师`，不按常识改。",
    "`宋军人，金兵拒战` 页级 OCR 仍为 `宋军人`，不猜补谓语。",
    "`阁门抵侯` 暂未找到明确页级 OCR 证据，本批不改。",
]


def main() -> None:
    html = HTML.read_text(encoding="utf-8")
    applied = []
    for old, new, section, evidence in CHANGES:
        count = html.count(old)
        if count < 1:
            raise RuntimeError(f"missing expected text: {old!r}")
        html = html.replace(old, new)
        applied.append({"old": old, "new": new, "section": section, "evidence": evidence, "count": count})
    HTML.write_text(html, encoding="utf-8")

    payload = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "reader": str(HTML.relative_to(ROOT)).replace("\\", "/"),
        "changes": applied,
        "deferred": DEFERRED,
        "note": "只修页级 PaddleOCR 明确支持的短片段。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 高置信 OCR 错字补修第十批：PaddleOCR 对照短片段",
        "",
        f"> 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "## 修复项",
        "",
    ]
    for item in applied:
        lines.append(f"- `{item['old']}` -> `{item['new']}`（{item['section']}；命中 {item['count']} 处；证据：`{item['evidence']}`）")
    lines += ["", "## 暂缓项", ""]
    for item in DEFERRED:
        lines.append(f"- {item}")
    lines += ["", "## 边界", "", "- 不扩展为全局 `人/入`、`自/目`、`谐/诣` 替换。", "- OCR 未给出强证据的古文、官名和地名继续保留。", ""]
    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(f"changed={sum(item['count'] for item in applied)}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()
