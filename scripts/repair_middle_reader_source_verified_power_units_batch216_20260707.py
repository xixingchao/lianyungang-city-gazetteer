# -*- coding: utf-8 -*-
"""Repair source-verified middle-volume power unit OCR residues."""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT_JSON = ROOT / "output" / "reports" / "middle_reader_source_verified_power_units_batch216_20260707.json"
REPORT_MD = ROOT / "output" / "reports" / "middle_reader_source_verified_power_units_batch216_20260707.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260707_中册电力单位残留回源补修第二百一十六批.md"

COMMON_REPLACEMENTS = [
    ("1990年生产Y系列电机61826于瓦", "1990年生产Y系列电机61826千瓦"),
    ("1.18亿于瓦时", "1.18亿千瓦时"),
    ("1号1600于瓦汽轮发电机", "1号1600千瓦汽轮发电机"),
    ("两台2.5万于瓦机组", "两台2.5万千瓦机组"),
    ("1026(5×200+1×26)于瓦", "1026(5×200+1×26)千瓦"),
    ("初建时投产1台6000于瓦发电机组", "初建时投产1台6000千瓦发电机组"),
    ("初建时投产1台6000</p><p>于瓦发电机组", "初建时投产1台6000千瓦发电机组"),
    ("初建时投产1台6000于</p><p>瓦发电机组", "初建时投产1台6000千瓦发电机组"),
    ("海州发电所1600于瓦发电机组", "海州发电所1600千瓦发电机组"),
    ("年用电475万于瓦", "年用电475万千瓦"),
    ("人均用电212于瓦时", "人均用电212千瓦时"),
    ("装接容量为22652于瓦", "装接容量为22652千瓦"),
    ("每于瓦线路工程贴", "每千瓦线路工程贴"),
    ("容量为2287.18于瓦", "容量为2287.18千瓦"),
    ("容</p><p>量为2287.18于瓦", "容量为2287.18千瓦"),
    ("容\n量为2287.18于瓦", "容\n量为2287.18千瓦"),
    ("每于瓦时0.14元", "每千瓦时0.14元"),
    ("每月每于瓦7.63元", "每月每千瓦7.63元"),
]

SOURCE_ONLY_REPLACEMENTS = [
    ("两组35方于瓦的热电站", "两组35万千瓦的热电站"),
    ("农网损失电量3732方于瓦时", "农网损失电量3732万千瓦时"),
]

TARGETS = [
    {
        "path": ROOT / "output" / "final_reader" / "连云港市志_中册.html",
        "label": "middle_reader",
        "replacements": COMMON_REPLACEMENTS,
    },
    {
        "path": ROOT / "workbench" / "body_chapters" / "第十七卷至第二十九卷（中part01）.md",
        "label": "middle_part01_source",
        "replacements": COMMON_REPLACEMENTS + SOURCE_ONLY_REPLACEMENTS,
    },
    {
        "path": ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
        "label": "full_body_source",
        "replacements": COMMON_REPLACEMENTS + SOURCE_ONLY_REPLACEMENTS,
    },
]

EVIDENCE = [
    (ROOT / "workbench" / "ocr" / "paddle_ocr" / "中" / "part01" / "page_0221.txt", "61826千瓦"),
    (ROOT / "workbench" / "ocr" / "paddle_ocr" / "中" / "part01" / "page_0321.txt", "两组35万千瓦的热电站"),
    (ROOT / "workbench" / "ocr" / "paddle_ocr" / "中" / "part01" / "page_0332.txt", "1.18亿千瓦时"),
    (ROOT / "workbench" / "ocr" / "paddle_ocr" / "中" / "part01" / "page_0334.txt", "1号1600千瓦汽轮发电机"),
    (ROOT / "workbench" / "ocr" / "paddle_ocr" / "中" / "part01" / "page_0334.txt", "两台2.5万千瓦机组"),
    (ROOT / "workbench" / "ocr" / "paddle_ocr" / "中" / "part01" / "page_0342.txt", "1026(5×200+1×26)千瓦"),
    (ROOT / "workbench" / "ocr" / "paddle_ocr" / "中" / "part01" / "page_0343.txt", "初建时投产1台6000千"),
    (ROOT / "workbench" / "ocr" / "paddle_ocr" / "中" / "part01" / "page_0362.txt", "农网损失电量3732万千瓦时"),
    (ROOT / "workbench" / "ocr" / "paddle_ocr" / "中" / "part01" / "page_0365.txt", "海州发电所1600千瓦发电机组"),
    (ROOT / "workbench" / "ocr" / "paddle_ocr" / "中" / "part01" / "page_0365.txt", "年用电475万千瓦"),
    (ROOT / "workbench" / "ocr" / "paddle_ocr" / "中" / "part01" / "page_0365.txt", "人均用电212千瓦时"),
    (ROOT / "workbench" / "ocr" / "paddle_ocr" / "中" / "part01" / "page_0370.txt", "装接容量为22652千瓦"),
    (ROOT / "workbench" / "ocr" / "paddle_ocr" / "中" / "part01" / "page_0375.txt", "每千瓦线路工程贴"),
    (ROOT / "workbench" / "ocr" / "paddle_ocr" / "中" / "part01" / "page_0376.txt", "量为2287.18千瓦"),
    (ROOT / "workbench" / "ocr" / "paddle_ocr" / "中" / "part01" / "page_0377.txt", "每千瓦时0.14元"),
    (ROOT / "workbench" / "ocr" / "paddle_ocr" / "中" / "part01" / "page_0377.txt", "每月每千瓦7.63元"),
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
        residuals[target["label"]] = {
            "于瓦": text.count("于瓦"),
            "方于瓦": text.count("方于瓦"),
            **{old: text.count(old) for old, _ in target["replacements"]},
        }

    payload = {"time": now, "changes": changes, "residuals": residuals}
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 中册电力单位残留回源补修第二百一十六批",
        "",
        f"> 生成时间：{now}",
        "",
        "## 范围",
        "",
        "- 当前中册阅读稿、对应中册正文源稿、全书正文汇总中的电力单位 OCR 残留。",
        "- 仅替换 PaddleOCR 同页可证的完整短语，不做 `于 -> 千` 或 `方 -> 万` 全局替换。",
        "- 当前正式 `连云港市志_全书.html` 已无本批 `于瓦` 残留，未改动该文件。",
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
    ])
    for path, needle in EVIDENCE:
        lines.append(f"- `{path.relative_to(ROOT)}`：`{needle}`。")
    lines.extend(["", "## 残留", ""])
    for label, values in residuals.items():
        lines.append(f"- {label}: " + "；".join(f"`{k}`={v}" for k, v in values.items()))
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    PROGRESS.write_text(REPORT_MD.read_text(encoding="utf-8"), encoding="utf-8")
    print(json.dumps({"changed": sum(i["count"] for i in changes), "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
