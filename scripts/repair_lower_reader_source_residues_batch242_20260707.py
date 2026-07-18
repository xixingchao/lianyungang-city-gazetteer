# -*- coding: utf-8 -*-
"""Repair evidence-backed lower-volume residues, batch 242."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT_JSON = ROOT / "output" / "reports" / "lower_reader_source_residues_batch242_20260707.json"
REPORT_MD = ROOT / "output" / "reports" / "lower_reader_source_residues_batch242_20260707.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260707_下册阅读稿源稿残留补修第二百四十二批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

ITEMS = [
    {
        "old": "優华日军",
        "new": "侵华日军",
        "evidence": "workbench/ocr/paddle_ocr/下/part01/page_0175.txt",
        "snippet": "侵华日军在连部分罪行",
        "targets": [
            "workbench/body_chapters/第四十三卷至第五十一卷（下part01）.md",
            "workbench/body_chapters/连云港市志_全书_正文汇总.md",
            "output/final_reader/连云港市志_下册.html",
            "output/final_reader/连云港市志_全书.html",
        ],
    },
    {
        "old": "踩蹦人民",
        "new": "蹂躏人民",
        "evidence": "workbench/ocr/paddle_ocr/下/part01/page_0175.txt",
        "snippet": "蹂躏人民",
        "targets": [
            "workbench/body_chapters/第四十三卷至第五十一卷（下part01）.md",
            "workbench/body_chapters/连云港市志_全书_正文汇总.md",
            "output/final_reader/连云港市志_下册.html",
            "output/final_reader/连云港市志_全书.html",
        ],
    },
    {
        "old": "元且文艺晚会",
        "new": "元旦文艺晚会",
        "evidence": "workbench/ocr/paddle_ocr/下/part02/page_0050.txt",
        "snippet": "元旦文艺晚会",
        "targets": [
            "workbench/body_chapters/第五十二卷至第六十卷及附录（下part02）.md",
            "output/final_reader/连云港市志_下册.html",
        ],
    },
    {
        "old": "发现隐惠1170处",
        "new": "发现隐患1170处",
        "evidence": "workbench/ocr/paddle_ocr/下/part01/page_0082.txt",
        "snippet": "发现隐患1170处",
        "targets": [
            "workbench/body_chapters/第四十三卷至第五十一卷（下part01）.md",
            "workbench/body_chapters/连云港市志_全书_正文汇总.md",
            "output/final_reader/连云港市志_下册.html",
        ],
    },
    {
        "old": "查出隐惠1916处",
        "new": "查出隐患1916处",
        "evidence": "workbench/ocr/paddle_ocr/下/part01/page_0092.txt",
        "snippet": "查出隐患1916处",
        "targets": [
            "workbench/body_chapters/第四十三卷至第五十一卷（下part01）.md",
            "workbench/body_chapters/连云港市志_全书_正文汇总.md",
            "output/final_reader/连云港市志_下册.html",
        ],
    },
    {
        "old": "事故隐惠987起",
        "new": "事故隐患987起",
        "evidence": "workbench/ocr/paddle_ocr/下/part01/page_0099.txt",
        "snippet": "事故隐患987起",
        "targets": [
            "workbench/body_chapters/第四十三卷至第五十一卷（下part01）.md",
            "workbench/body_chapters/连云港市志_全书_正文汇总.md",
            "output/final_reader/连云港市志_下册.html",
        ],
    },
    {
        "old": "事故隐惠934处",
        "new": "事故隐患934处",
        "evidence": "workbench/ocr/paddle_ocr/下/part01/page_0274.txt",
        "snippet": "事故隐患934处",
        "targets": [
            "workbench/body_chapters/第四十三卷至第五十一卷（下part01）.md",
            "workbench/body_chapters/连云港市志_全书_正文汇总.md",
            "output/final_reader/连云港市志_下册.html",
        ],
    },
    {
        "old": "较大隐惠120处",
        "new": "较大隐患120处",
        "evidence": "workbench/ocr/paddle_ocr/下/part01/page_0274.txt",
        "snippet": "较大隐患120处",
        "targets": [
            "workbench/body_chapters/第四十三卷至第五十一卷（下part01）.md",
            "workbench/body_chapters/连云港市志_全书_正文汇总.md",
            "output/final_reader/连云港市志_下册.html",
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
        if item["snippet"] not in read(item["evidence"]):
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
        "# 下册阅读稿源稿残留补修第二百四十二批",
        "",
        f"> 生成时间：{now}",
        "",
        "## 范围",
        "",
        "- 修复下册源稿/阅读稿中页级 OCR 明确支持的 `蹂躏/元旦/隐患` 等残留。",
        "- 本批不处理 `撤消`、`进人`、`输人` 等需要逐条语境复核的项。",
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
    memory += "\n\n## 2026-07-07 下册阅读稿源稿残留补修第二百四十二批\n\n"
    memory += "- 依据下册页级 PaddleOCR，修复 `優华日军/踩蹦人民/元且文艺晚会/隐惠` 等明确 OCR 残留。\n"
    memory += "- 同步范围覆盖相关下册正文源稿、全书汇总及下册/全书阅读稿；报告：`output/reports/lower_reader_source_residues_batch242_20260707.md`。\n"
    memory += "- `撤消`、`进人`、`输人` 等需逐条语境复核项未猜改；未做全局替换，未打开、展示或嵌入图片。\n"
    MEMORY.write_text(memory + "\n", encoding="utf-8")

    print(json.dumps({
        "changed_items": sum(c["count"] for item in changes for c in item["changes"]),
        "changed_files": len({c["file"] for item in changes for c in item["changes"] if c["count"]}),
        "residual_total": sum(item["residual"] for item in changes),
        "report": str(REPORT_MD),
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
