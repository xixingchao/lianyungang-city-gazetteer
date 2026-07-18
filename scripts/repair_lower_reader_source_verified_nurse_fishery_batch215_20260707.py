# -*- coding: utf-8 -*-
"""Repair source-verified lower-reader nurse/fishery residues."""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT_JSON = ROOT / "output" / "reports" / "lower_reader_source_verified_nurse_fishery_batch215_20260707.json"
REPORT_MD = ROOT / "output" / "reports" / "lower_reader_source_verified_nurse_fishery_batch215_20260707.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260707_下册护士与工厂化养鱼残留回源补修第二百一十五批.md"

TARGETS = [
    {
        "path": ROOT / "output" / "final_reader" / "连云港市志_下册.html",
        "label": "lower_reader",
        "replacements": [
            ("护土长", "护士长"),
            ("护土学校", "护士学校"),
            ("曾设</p><p>：置港机维修、港电维修、外语和护土等专业。至1990年未", "曾设置港机维修、港电维修、外语和护士等专业。至1990年末"),
            ("曾设：置港机维修、港电维修、外语和护土等专业。至1990年未", "曾设置港机维修、港电维修、外语和护士等专业。至1990年末"),
            ("担任护土", "担任护士"),
            ("任护土、医土、医生", "任护士、医士、医生"),
            ("护土待遇", "护士待遇"),
            ("工广化养鱼", "工厂化养鱼"),
        ],
    },
    {
        "path": ROOT / "workbench" / "body_chapters" / "第四十三卷至第五十一卷（下part01）.md",
        "label": "lower_part01_source",
        "replacements": [
            ("护土学校", "护士学校"),
            ("护土待遇", "护士待遇"),
            ("曾设\n：置港机维修、港电维修、外语和护土等专业。至1990年未", "曾设置\n港机维修、港电维修、外语和护士等专业。至1990年末"),
            ("曾设 ：置港机维修、港电维修、外语和护土等专业。至1990年未", "曾设置港机维修、港电维修、外语和护士等专业。至1990年末"),
            ("工广化养鱼", "工厂化养鱼"),
        ],
    },
    {
        "path": ROOT / "workbench" / "body_chapters" / "第五十二卷至第六十卷及附录（下part02）.md",
        "label": "lower_part02_source",
        "replacements": [
            ("护土长", "护士长"),
            ("担任护土", "担任护士"),
            ("任护土、医土、医生", "任护士、医士、医生"),
        ],
    },
    {
        "path": ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
        "label": "full_body_source",
        "replacements": [
            ("护土长", "护士长"),
            ("护土待遇", "护士待遇"),
            ("曾设\n：置港机维修、港电维修、外语和护土等专业。至1990年未", "曾设置\n港机维修、港电维修、外语和护士等专业。至1990年末"),
            ("曾设 ：置港机维修、港电维修、外语和护土等专业。至1990年未", "曾设置港机维修、港电维修、外语和护士等专业。至1990年末"),
            ("工广化养鱼", "工厂化养鱼"),
        ],
    },
]

EVIDENCE = [
    (ROOT / "workbench" / "ocr" / "paddle_ocr" / "下" / "part02" / "page_0191.txt", "护士长"),
    (ROOT / "workbench" / "ocr" / "paddle_ocr" / "下" / "part01" / "page_0252.txt", "外语和护士等专业。至1990年末"),
    (ROOT / "workbench" / "ocr" / "paddle_ocr" / "下" / "part01" / "page_0393.txt", "护士学校"),
    (ROOT / "workbench" / "ocr" / "paddle_ocr" / "下" / "part02" / "page_0393.txt", "担任护士"),
    (ROOT / "workbench" / "ocr" / "paddle_ocr" / "下" / "part02" / "page_0395.txt", "任护士、医士、医生"),
    (ROOT / "workbench" / "ocr" / "paddle_ocr" / "下" / "part01" / "page_0304.txt", "改善护士待遇"),
    (ROOT / "workbench" / "ocr" / "paddle_ocr" / "下" / "part01" / "page_0438.txt", "工厂化养鱼"),
]


def plain(html: str) -> str:
    return re.sub(r"<[^>]+>", "", html)


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
        if target["path"].suffix == ".html":
            text = plain(text)
        residuals[target["label"]] = {old: text.count(old) for old, _ in target["replacements"]}

    payload = {"time": now, "changes": changes, "residuals": residuals}
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 下册护士与工厂化养鱼残留回源补修第二百一十五批",
        "",
        f"> 生成时间：{now}",
        "",
        "## 范围",
        "",
        "- 当前下册阅读稿及对应下册正文源稿、全书正文汇总。",
        "- 仅替换 PaddleOCR 同页可证的短语，不处理 `护土植物`、`养护土面公路` 等合法跨词语境。",
        "- 未打开、展示或嵌入图片。",
        "",
        "## 修改统计",
        "",
        "| 文件 | 原文 | 新文 | 次数 |",
        "|---|---|---|---:|",
    ]
    for item in changes:
        if item["count"]:
            lines.append(f"| `{item['path']}` | `{item['old']}` | `{item['new']}` | {item['count']} |")
    lines.extend([
        "",
        "## 证据",
        "",
        "- `workbench/ocr/paddle_ocr/下/part02/page_0191.txt`：`护士长`。",
        "- `workbench/ocr/paddle_ocr/下/part01/page_0252.txt`：`设置港机维修、港电维修、外语和护士等专业。至1990年末`。",
        "- `workbench/ocr/paddle_ocr/下/part01/page_0393.txt`：`护士学校`。",
        "- `workbench/ocr/paddle_ocr/下/part02/page_0393.txt`：`担任护士`。",
        "- `workbench/ocr/paddle_ocr/下/part02/page_0395.txt`：`任护士、医士、医生`。",
        "- `workbench/ocr/paddle_ocr/下/part01/page_0304.txt`：`改善护士待遇`。",
        "- `workbench/ocr/paddle_ocr/下/part01/page_0438.txt`：`工厂化养鱼`。",
        "",
        "## 残留",
        "",
    ])
    for label, values in residuals.items():
        lines.append(f"- {label}: " + "；".join(f"`{k}`={v}" for k, v in values.items()))
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    PROGRESS.write_text(REPORT_MD.read_text(encoding="utf-8"), encoding="utf-8")
    print(json.dumps({"changed": sum(i["count"] for i in changes), "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
