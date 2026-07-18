# -*- coding: utf-8 -*-
"""Repair evidence-backed source/reader residues, batch 241."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT_JSON = ROOT / "output" / "reports" / "source_reader_residues_batch241_20260707.json"
REPORT_MD = ROOT / "output" / "reports" / "source_reader_residues_batch241_20260707.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260707_源稿阅读稿残留补修第二百四十一批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

ITEMS = [
    {
        "old": "汽车运输公可",
        "new": "汽车运输公司",
        "evidence": "workbench/ocr/paddle_ocr/merged/连云港市志_上册_PaddleOCR汇总.md",
        "snippet": "汽车运输公司",
        "targets": [
            "workbench/body_chapters/上/第三卷_区县概况.md",
            "workbench/body_chapters/连云港市志_上册_正文汇总.md",
            "workbench/body_chapters/连云港市志_全书_正文汇总.md",
        ],
    },
    {
        "old": "充许个人经商",
        "new": "允许个人经商",
        "evidence": "workbench/ocr/paddle_ocr/merged/连云港市志_上_part02_PaddleOCR汇总.md",
        "snippet": "允许个人经商",
        "targets": [
            "workbench/body_chapters/上/第四卷至第十卷（part02）.md",
            "workbench/body_chapters/连云港市志_上册_正文汇总.md",
            "workbench/body_chapters/连云港市志_全书_正文汇总.md",
        ],
    },
    {
        "old": "充许-\n部分地区、一部分农民勤劳致富",
        "new": "允许一\n部分地区、一部分农民勤劳致富",
        "evidence": "workbench/ocr/paddle_ocr/merged/连云港市志_上_part02_PaddleOCR汇总.md",
        "snippet": "允许一\n部分地区、一部分农民勤劳致富",
        "targets": [
            "workbench/body_chapters/上/第四卷至第十卷（part02）.md",
            "workbench/body_chapters/连云港市志_上册_正文汇总.md",
            "workbench/body_chapters/连云港市志_全书_正文汇总.md",
        ],
    },
    {
        "old": "西湘幸存",
        "new": "西厢幸存",
        "evidence": "workbench/ocr/paddle_ocr/中/part02/page_0103.txt",
        "snippet": "西厢幸存",
        "targets": [
            "workbench/body_chapters/第三十卷至第四十二卷（中part02）.md",
            "workbench/body_chapters/连云港市志_全书_正文汇总.md",
            "output/final_reader/连云港市志_中册.html",
            "output/final_reader/连云港市志_全书.html",
        ],
    },
    {
        "old": "赐护国延福观",
        "new": "敕赐护国延福观",
        "evidence": "workbench/ocr/paddle_ocr/中/part02/page_0103.txt",
        "snippet": "敕赐护国延福观",
        "targets": [
            "workbench/body_chapters/第三十卷至第四十二卷（中part02）.md",
            "workbench/body_chapters/连云港市志_全书_正文汇总.md",
            "output/final_reader/连云港市志_中册.html",
            "output/final_reader/连云港市志_全书.html",
        ],
    },
    {
        "old": "注洋一片",
        "new": "汪洋一片",
        "evidence": "workbench/ocr/paddle_ocr/中/part02/page_0103.txt",
        "snippet": "汪洋一片",
        "targets": [
            "workbench/body_chapters/第三十卷至第四十二卷（中part02）.md",
            "workbench/body_chapters/连云港市志_全书_正文汇总.md",
            "output/final_reader/连云港市志_中册.html",
            "output/final_reader/连云港市志_全书.html",
        ],
    },
    {
        "old": "花枝摇电",
        "new": "花枝摇曳",
        "evidence": "workbench/ocr/paddle_ocr/中/part02/page_0103.txt",
        "snippet": "花枝摇曳",
        "targets": [
            "workbench/body_chapters/第三十卷至第四十二卷（中part02）.md",
            "workbench/body_chapters/连云港市志_全书_正文汇总.md",
            "output/final_reader/连云港市志_中册.html",
            "output/final_reader/连云港市志_全书.html",
        ],
    },
    {
        "old": "鸟语调嗽",
        "new": "鸟语啁啾",
        "evidence": "workbench/ocr/paddle_ocr/中/part02/page_0103.txt",
        "snippet": "鸟语啁啾",
        "targets": [
            "workbench/body_chapters/第三十卷至第四十二卷（中part02）.md",
            "workbench/body_chapters/连云港市志_全书_正文汇总.md",
            "output/final_reader/连云港市志_中册.html",
            "output/final_reader/连云港市志_全书.html",
        ],
    },
    {
        "old": "虎豹尽高尊",
        "new": "虎豹尽高蹲",
        "evidence": "workbench/ocr/paddle_ocr/中/part02/page_0104.txt",
        "snippet": "虎豹尽高蹲",
        "targets": [
            "workbench/body_chapters/第三十卷至第四十二卷（中part02）.md",
            "workbench/body_chapters/连云港市志_全书_正文汇总.md",
            "output/final_reader/连云港市志_中册.html",
            "output/final_reader/连云港市志_全书.html",
        ],
    },
    {
        "old": "肤寸氮盒",
        "new": "肤寸氤氲",
        "evidence": "workbench/ocr/paddle_ocr/中/part02/page_0104.txt",
        "snippet": "肤寸氤氲",
        "targets": [
            "workbench/body_chapters/第三十卷至第四十二卷（中part02）.md",
            "workbench/body_chapters/连云港市志_全书_正文汇总.md",
            "output/final_reader/连云港市志_中册.html",
            "output/final_reader/连云港市志_全书.html",
        ],
    },
    {
        "old": "山势崔鬼",
        "new": "山势崔嵬",
        "evidence": "workbench/ocr/paddle_ocr/中/part02/page_0104.txt",
        "snippet": "山势崔嵬",
        "targets": [
            "workbench/body_chapters/第三十卷至第四十二卷（中part02）.md",
            "workbench/body_chapters/连云港市志_全书_正文汇总.md",
            "output/final_reader/连云港市志_中册.html",
            "output/final_reader/连云港市志_全书.html",
        ],
    },
    {
        "old": "山麓杂脊堆砌",
        "new": "山麓杂沓堆砌",
        "evidence": "workbench/ocr/paddle_ocr/中/part02/page_0104.txt",
        "snippet": "山麓杂沓堆砌",
        "targets": [
            "workbench/body_chapters/第三十卷至第四十二卷（中part02）.md",
            "workbench/body_chapters/连云港市志_全书_正文汇总.md",
            "output/final_reader/连云港市志_中册.html",
            "output/final_reader/连云港市志_全书.html",
        ],
    },
]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8", errors="ignore")


def write(rel: str, text: str) -> None:
    (ROOT / rel).write_text(text, encoding="utf-8")


def main() -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    for item in ITEMS:
        evidence_text = read(item["evidence"])
        if item["snippet"] not in evidence_text:
            raise SystemExit(f"missing evidence: {item['evidence']} -> {item['snippet']}")

    changes = []
    for item in ITEMS:
        item_changes = []
        for rel in item["targets"]:
            text = read(rel)
            count = text.count(item["old"])
            if count:
                write(rel, text.replace(item["old"], item["new"]))
            item_changes.append({"file": rel, "count": count})
        changes.append({
            "old": item["old"],
            "new": item["new"],
            "evidence": item["evidence"],
            "changes": item_changes,
            "residual": sum(read(rel).count(item["old"]) for rel in item["targets"]),
        })

    payload = {"time": now, "changes": changes}
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 源稿阅读稿残留补修第二百四十一批",
        "",
        f"> 生成时间：{now}",
        "",
        "## 范围",
        "",
        "- 修复当前源稿/阅读稿中有页级 OCR 或 PaddleOCR 汇总明确支持的残留。",
        "- 本批不处理 `观盾珠落洗头盆`、`万头乳鸽` 等源 OCR 仍不充分的疑点。",
        "- 未做全局替换，未打开、展示或嵌入图片。",
        "",
        "## 修改统计",
        "",
        "| 原文 | 新文 | 文件 | 次数 | 证据 |",
        "|---|---|---|---:|---|",
    ]
    for item in changes:
        for change in item["changes"]:
            if change["count"]:
                lines.append(f"| `{item['old']}` | `{item['new']}` | `{change['file']}` | {change['count']} | `{item['evidence']}` |")
    lines.extend(["", "## 残留计数", ""])
    for item in changes:
        lines.append(f"- `{item['old']}`：{item['residual']}")
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    PROGRESS.write_text(REPORT_MD.read_text(encoding="utf-8"), encoding="utf-8")

    memory = MEMORY.read_text(encoding="utf-8", errors="ignore").rstrip()
    memory += "\n\n## 2026-07-07 源稿阅读稿残留补修第二百四十一批\n\n"
    memory += "- 依据页级 OCR/PaddleOCR 汇总，修复 `汽车运输公可`、`充许个人经商`、`充许-部分` 以及东磊名胜旅游段 `西湘/赐护国/注洋/摇电/调嗽/高尊/氮盒/崔鬼/杂脊` 等残留。\n"
    memory += "- 同步范围覆盖相关正文源稿、上册/全书汇总及中册/全书阅读稿；报告：`output/reports/source_reader_residues_batch241_20260707.md`。\n"
    memory += "- `观盾珠落洗头盆`、`万头乳鸽` 等 OCR 仍不充分项未猜改；未做全局替换，未打开、展示或嵌入图片。\n"
    MEMORY.write_text(memory + "\n", encoding="utf-8")

    print(json.dumps({
        "changed_items": sum(c["count"] for item in changes for c in item["changes"]),
        "changed_files": len({c["file"] for item in changes for c in item["changes"] if c["count"]}),
        "residual_total": sum(item["residual"] for item in changes),
        "report": str(REPORT_MD),
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
