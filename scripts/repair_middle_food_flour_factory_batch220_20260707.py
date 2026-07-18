# -*- coding: utf-8 -*-
"""Repair source-verified flour factory OCR residues."""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT_JSON = ROOT / "output" / "reports" / "middle_food_flour_factory_batch220_20260707.json"
REPORT_MD = ROOT / "output" / "reports" / "middle_food_flour_factory_batch220_20260707.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260707_中册食品面粉厂残留补修第二百二十批.md"

REPLACEMENTS = [
    ("将方昌面粉广并入成立新海面粉广", "将万昌面粉厂并入成立新海面粉厂"),
    ("以上三广均停止生产", "以上三厂均停止生产"),
    ("二广设备调给灌云五图河农场", "二厂设备调给灌云五图河农场"),
    ("隆丰面粉厂广因经理韩福全", "隆丰面粉厂因经理韩福全"),
]

TARGETS = [
    ROOT / "output" / "final_reader" / "连云港市志_全书.html",
    ROOT / "output" / "final_reader" / "连云港市志_中册.html",
    ROOT / "workbench" / "body_chapters" / "第三十卷至第四十二卷（中part02）.md",
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
]

EVIDENCE = [
    (ROOT / "workbench" / "ocr" / "paddle_ocr" / "中" / "part02" / "page_0253.txt", "将万昌面粉厂并入成立新海面粉厂"),
    (ROOT / "workbench" / "ocr" / "paddle_ocr" / "中" / "part02" / "page_0253.txt", "以上三厂均停止生产"),
    (ROOT / "workbench" / "ocr" / "paddle_ocr" / "中" / "part02" / "page_0253.txt", "二厂设备调给灌云五图河农场"),
    (ROOT / "workbench" / "ocr" / "paddle_ocr" / "中" / "part02" / "page_0253.txt", "隆丰面粉厂因经理韩福全"),
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
    for path in TARGETS:
        text = path.read_text(encoding="utf-8")
        before = text
        for old, new in REPLACEMENTS:
            count = text.count(old)
            if count:
                text = text.replace(old, new)
            changes.append({"path": str(path.relative_to(ROOT)), "old": old, "new": new, "count": count})
        if text != before:
            path.write_text(text, encoding="utf-8")

    residuals = {}
    for path in TARGETS:
        text = path.read_text(encoding="utf-8")
        scan = plain(text) if path.suffix == ".html" else text
        residuals[str(path.relative_to(ROOT))] = {
            "方昌面粉广": scan.count("方昌面粉广"),
            "新海面粉广": scan.count("新海面粉广"),
            "以上三广": scan.count("以上三广"),
            "二广设备": scan.count("二广设备"),
            "隆丰面粉厂广": scan.count("隆丰面粉厂广"),
        }

    payload = {"time": now, "changes": changes, "residuals": residuals}
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 中册食品面粉厂残留补修第二百二十批",
        "",
        f"> 生成时间：{now}",
        "",
        "## 范围",
        "",
        "- 依据 `workbench/ocr/paddle_ocr/中/part02/page_0253.txt` 修复食品工业加工章面粉厂段 OCR 残留。",
        "- 只替换整句短语，不做单字 `广 -> 厂`。",
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
        "- `workbench/ocr/paddle_ocr/中/part02/page_0253.txt`：`将万昌面粉厂并入成立新海面粉厂`、`以上三厂均停止生产`、`二厂设备调给灌云五图河农场`、`隆丰面粉厂因经理韩福全`。",
        "",
        "## 残留",
        "",
    ])
    for label, values in residuals.items():
        lines.append(f"- `{label}`: " + "；".join(f"`{k}`={v}" for k, v in values.items()))
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    PROGRESS.write_text(REPORT_MD.read_text(encoding="utf-8"), encoding="utf-8")
    print(json.dumps({"changed": sum(i["count"] for i in changes), "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
