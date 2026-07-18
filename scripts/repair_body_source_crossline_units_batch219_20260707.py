# -*- coding: utf-8 -*-
"""Repair source-only cross-line power-unit OCR residues."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT_JSON = ROOT / "output" / "reports" / "body_source_crossline_units_batch219_20260707.json"
REPORT_MD = ROOT / "output" / "reports" / "body_source_crossline_units_batch219_20260707.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260707_正文源稿跨行单位残留补修第二百一十九批.md"

TARGETS = [
    {
        "path": ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
        "label": "full_body_source",
        "replacements": [
            ("37708吨71977于\n瓦", "37708吨71977千\n瓦"),
            ("10万于\n瓦时及以上半年1次", "10万千\n瓦时及以上半年1次"),
        ],
    },
    {
        "path": ROOT / "workbench" / "body_chapters" / "连云港市志_上册_正文汇总.md",
        "label": "upper_body_source",
        "replacements": [
            ("37708吨71977于\n瓦", "37708吨71977千\n瓦"),
        ],
    },
    {
        "path": ROOT / "workbench" / "body_chapters" / "第十七卷至第二十九卷（中part01）.md",
        "label": "middle_part01_source",
        "replacements": [
            ("10万于\n瓦时及以上半年1次", "10万千\n瓦时及以上半年1次"),
        ],
    },
]

EVIDENCE = [
    (ROOT / "workbench" / "ocr" / "paddle_ocr" / "上" / "part03" / "page_0096.txt", "71977千"),
    (ROOT / "workbench" / "ocr" / "paddle_ocr" / "中" / "part01" / "page_0376.txt", "10万千"),
    (ROOT / "output" / "final_reader" / "连云港市志_全书.html", "71977千瓦"),
    (ROOT / "output" / "final_reader" / "连云港市志_全书.html", "10万千瓦时及以上半年1次"),
]


def main() -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    for path, needle in EVIDENCE:
        text = path.read_text(encoding="utf-8", errors="ignore")
        if needle not in text:
            raise SystemExit(f"missing evidence {needle} in {path}")

    changes = []
    for target in TARGETS:
        path = target["path"]
        text = path.read_text(encoding="utf-8")
        before = text
        for old, new in target["replacements"]:
            count = text.count(old)
            if count:
                text = text.replace(old, new)
            changes.append({"label": target["label"], "path": str(path.relative_to(ROOT)), "old": old, "new": new, "count": count})
        if text != before:
            path.write_text(text, encoding="utf-8")

    residuals = {}
    for target in TARGETS:
        text = target["path"].read_text(encoding="utf-8")
        residuals[target["label"]] = {old: text.count(old) for old, _ in target["replacements"]}

    payload = {"time": now, "changes": changes, "residuals": residuals}
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 正文源稿跨行单位残留补修第二百一十九批",
        "",
        f"> 生成时间：{now}",
        "",
        "## 范围",
        "",
        "- 修复正文源稿中 2 类跨行 `于/瓦` 单位残留；正式阅读稿已为正确文本。",
        "- 仅替换 PaddleOCR/正式阅读稿可证的完整短语，不做全局替换。",
        "- 未打开、展示或嵌入图片。",
        "",
        "## 修改统计",
        "",
        "| 文件 | 原文 | 新文 | 次数 |",
        "|---|---|---|---:|",
    ]
    for item in changes:
        if item["count"]:
            old = item["old"].replace("\n", "\\n")
            new = item["new"].replace("\n", "\\n")
            lines.append(f"| `{item['path']}` | `{old}` | `{new}` | {item['count']} |")
    lines.extend([
        "",
        "## 证据",
        "",
        "- `workbench/ocr/paddle_ocr/上/part03/page_0096.txt`：`71977千瓦`。",
        "- `workbench/ocr/paddle_ocr/中/part01/page_0376.txt`：`10万千瓦时及以上半年1次`。",
        "- `output/final_reader/连云港市志_全书.html`：对应两处均已为正确文本。",
        "",
        "## 残留",
        "",
    ])
    for label, values in residuals.items():
        lines.append(f"- {label}: " + "；".join(f"`{k.replace(chr(10), '\\n')}`={v}" for k, v in values.items()))
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    PROGRESS.write_text(REPORT_MD.read_text(encoding="utf-8"), encoding="utf-8")
    print(json.dumps({"changed": sum(i["count"] for i in changes), "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
