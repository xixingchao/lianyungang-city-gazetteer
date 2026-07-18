# -*- coding: utf-8 -*-
"""Repair source-verified lower-reader 印刷广->印刷厂 residue."""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOWER = ROOT / "output" / "final_reader" / "连云港市志_下册.html"
FULL = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
SOURCE = ROOT / "workbench" / "ocr" / "paddle_ocr" / "下" / "part02" / "page_0067.txt"
REPORT_JSON = ROOT / "output" / "reports" / "reader_source_verified_print_factory_batch214_20260707.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_source_verified_print_factory_batch214_20260707.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260707_源页核验印刷厂残留补修第二百一十四批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

OLD = "送印刷广切边"
NEW = "送印刷厂切边"
EVIDENCE = "年终装订好送印刷厂切边，然后直接入库收藏。"


def plain(html: str) -> str:
    return re.sub(r"<[^>]+>", "", html)


def main() -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    source_text = SOURCE.read_text(encoding="utf-8", errors="ignore")
    if EVIDENCE not in source_text:
        raise SystemExit("missing source evidence in page_0067.txt")
    counts = {}
    for label, path in [("lower", LOWER), ("full", FULL)]:
        html = path.read_text(encoding="utf-8")
        count = html.count(OLD)
        if count:
            html = html.replace(OLD, NEW)
            path.write_text(html, encoding="utf-8")
        counts[label] = count
    residual_counts = {}
    for label, path in [("lower", LOWER), ("full", FULL)]:
        text = plain(path.read_text(encoding="utf-8"))
        residual_counts[label] = {OLD: text.count(OLD), NEW: text.count(NEW)}
    payload = {"time": now, "changed": counts, "source": "workbench/ocr/paddle_ocr/下/part02/page_0067.txt:7", "old": OLD, "new": NEW, "residual_counts": residual_counts}
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# 源页核验印刷厂残留补修第二百一十四批",
        "",
        f"> 生成时间：{now}",
        "",
        "## 范围",
        "",
        "- 当前下册阅读稿和全书阅读稿。",
        "- 依据 PaddleOCR 页级文字证据修复 `送印刷广切边 -> 送印刷厂切边`。",
        "- 未打开、展示或嵌入图片。",
        "",
        "## 统计",
        "",
        f"- 下册修复：{counts['lower']} 处",
        f"- 全书同步修复：{counts['full']} 处",
        "",
        "## 证据",
        "",
        "- `workbench/ocr/paddle_ocr/下/part02/page_0067.txt:7`：`年终装订好送印刷厂切边，然后直接入库收藏。`",
        "",
        "## 残留计数",
        "",
    ]
    for label, values in residual_counts.items():
        lines.append(f"- {label} `{OLD}`: {values[OLD]}；`{NEW}`: {values[NEW]}")
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    PROGRESS.write_text(REPORT_MD.read_text(encoding="utf-8"), encoding="utf-8")
    MEMORY.write_text(MEMORY.read_text(encoding="utf-8").rstrip() + "\n\n## 2026-07-07 源页核验印刷厂残留补修第二百一十四批\n\n- 依据 `workbench/ocr/paddle_ocr/下/part02/page_0067.txt:7`，修复下册/全书 `送印刷广切边 -> 送印刷厂切边`。\n- 修后原先 6 个待源页核验 reader 残留均已处理；报告：`output/reports/reader_source_verified_print_factory_batch214_20260707.md`。\n- 未打开、展示或嵌入图片。\n", encoding="utf-8")
    print(json.dumps({"changed": counts, "residual_counts": residual_counts, "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
