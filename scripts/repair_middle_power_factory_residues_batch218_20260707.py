# -*- coding: utf-8 -*-
"""Repair source-verified middle power chapter factory/unit residues."""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT_JSON = ROOT / "output" / "reports" / "middle_power_factory_residues_batch218_20260707.json"
REPORT_MD = ROOT / "output" / "reports" / "middle_power_factory_residues_batch218_20260707.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260707_中册电力厂字与竣工残留补修第二百一十八批.md"

TARGETS = [
    {
        "path": ROOT / "output" / "final_reader" / "连云港市志_全书.html",
        "label": "full_reader",
        "replacements": [
            ("该厂始建于1974年10月，工于1976年5月", "该厂始建于1974年10月，竣工于1976年5月"),
            ("对海州面粉广、西墅扬水站", "对海州面粉厂、西墅扬水站"),
        ],
    },
    {
        "path": ROOT / "output" / "final_reader" / "连云港市志_中册.html",
        "label": "middle_reader",
        "replacements": [
            ("该厂始建于1974年10月，工于1976年5月", "该厂始建于1974年10月，竣工于1976年5月"),
            ("对海州面粉广、西墅扬水站", "对海州面粉厂、西墅扬水站"),
        ],
    },
    {
        "path": ROOT / "workbench" / "body_chapters" / "第十七卷至第二十九卷（中part01）.md",
        "label": "middle_part01_source",
        "replacements": [
            ("该厂始建于1974年10月，工于1976年5月", "该厂始建于1974年10月，竣工于1976年5月"),
            ("初建时投产1台6000于\n瓦发电机组", "初建时投产1台6000千\n瓦发电机组"),
            ("对海州面粉广、西墅扬水站", "对海州面粉厂、西墅扬水站"),
        ],
    },
    {
        "path": ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
        "label": "full_body_source",
        "replacements": [
            ("该厂始建于1974年10月，工于1976年5月", "该厂始建于1974年10月，竣工于1976年5月"),
            ("初建时投产1台6000于\n瓦发电机组", "初建时投产1台6000千\n瓦发电机组"),
            ("对海州面粉广、西墅扬水站", "对海州面粉厂、西墅扬水站"),
        ],
    },
]

EVIDENCE = [
    (ROOT / "workbench" / "ocr" / "paddle_ocr" / "中" / "part01" / "page_0343.txt", "竣工于1976年5月"),
    (ROOT / "workbench" / "ocr" / "paddle_ocr" / "中" / "part01" / "page_0343.txt", "初建时投产1台6000千"),
    (ROOT / "workbench" / "ocr" / "paddle_ocr" / "中" / "part01" / "page_0377.txt", "对海州面粉厂、西墅扬水站"),
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
        scan = plain(text) if target["path"].suffix == ".html" else text
        residuals[target["label"]] = {
            "工于1976": scan.count("工于1976"),
            "对海州面粉广、西墅扬水站": scan.count("对海州面粉广、西墅扬水站"),
            "初建时投产1台6000于": text.count("初建时投产1台6000于"),
        }

    payload = {"time": now, "changes": changes, "residuals": residuals}
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 中册电力厂字与竣工残留补修第二百一十八批",
        "",
        f"> 生成时间：{now}",
        "",
        "## 范围",
        "",
        "- 修复中册电力工业卷中 PaddleOCR 同页可证的 `工于1976`、`海州面粉广` 和跨行 `6000于/瓦` 残留。",
        "- 仅处理电力卷证据明确的短语；上册食品工业 `方昌面粉广/新海面粉广` 等未纳入本批。",
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
        "- `workbench/ocr/paddle_ocr/中/part01/page_0343.txt`：`竣工于1976年5月`、`初建时投产1台6000千瓦发电机组`。",
        "- `workbench/ocr/paddle_ocr/中/part01/page_0377.txt`：`对海州面粉厂、西墅扬水站`。",
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
