# -*- coding: utf-8 -*-
"""Repair source-backed unit residues in body source files, batch 233."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = [
    ROOT / "workbench" / "body_chapters" / "第三十卷至第四十二卷（中part02）.md",
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
]
REPORT_JSON = ROOT / "output" / "reports" / "body_source_units_batch233_20260707.json"
REPORT_MD = ROOT / "output" / "reports" / "body_source_units_batch233_20260707.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260707_正文源稿单位残留补修第二百三十三批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"
ITEMS = [
    {
        "old": "食盐积压5方吨",
        "new": "食盐积压5万吨",
        "evidence": ROOT / "workbench" / "ocr" / "paddle_ocr" / "中" / "part02" / "page_0055.txt",
        "snippet": "现象，仅食盐积压5万吨。因此于1959年成立了赣榆县航运公司",
    },
    {
        "old": "煤炭64.19方吨",
        "new": "煤炭64.19万吨",
        "evidence": ROOT / "workbench" / "ocr" / "paddle_ocr" / "中" / "part02" / "page_0260.txt",
        "snippet": "全年还组织计划外煤炭64.19万吨、钢材1.35万吨",
    },
    {
        "old": "生猪存栏101方头，水产品9.1方吨",
        "new": "生猪存栏101万头，水产品9.1万吨",
        "evidence": ROOT / "workbench" / "ocr" / "paddle_ocr" / "中" / "part02" / "page_0494.txt",
        "snippet": "生猪存栏101万头，水产品9.1万吨",
    },
]


def ensure_evidence() -> None:
    for item in ITEMS:
        text = item["evidence"].read_text(encoding="utf-8", errors="ignore")
        if item["snippet"] not in text:
            raise SystemExit(f"missing evidence: {item['evidence'].relative_to(ROOT)}: {item['snippet']}")


def main() -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    ensure_evidence()
    changes = []
    for path in TARGETS:
        text = path.read_text(encoding="utf-8", errors="ignore")
        file_items = []
        for item in ITEMS:
            count = text.count(item["old"])
            if count:
                text = text.replace(item["old"], item["new"])
                file_items.append({
                    "old": item["old"],
                    "new": item["new"],
                    "count": count,
                    "evidence": str(item["evidence"].relative_to(ROOT)),
                })
        if file_items:
            path.write_text(text, encoding="utf-8")
        changes.append({"file": str(path.relative_to(ROOT)), "items": file_items})

    residuals = {
        item["old"]: {
            str(path.relative_to(ROOT)): path.read_text(encoding="utf-8", errors="ignore").count(item["old"])
            for path in TARGETS
        }
        for item in ITEMS
    }
    payload = {"time": now, "changes": changes, "residuals": residuals}
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 正文源稿单位残留补修第二百三十三批",
        "",
        f"> 生成时间：{now}",
        "",
        "## 范围",
        "",
        "- 修复中册正文源稿和全书正文汇总中已由页级 PaddleOCR 证实的单位残留。",
        "- 当前正式阅读稿对应位置已正确，本批只补源稿同步。",
        "- 未做全局替换，未打开、展示或嵌入图片。",
        "",
        "## 修改统计",
        "",
        "| 文件 | 原文 | 新文 | 次数 | 证据 |",
        "|---|---|---|---:|---|",
    ]
    for item in changes:
        for change in item["items"]:
            lines.append(
                f"| `{item['file']}` | `{change['old']}` | `{change['new']}` | {change['count']} | `{change['evidence']}` |"
            )
    lines.extend(["", "## 残留计数", ""])
    for old, files in residuals.items():
        lines.append(f"- `{old}`：{sum(files.values())}")
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    PROGRESS.write_text(REPORT_MD.read_text(encoding="utf-8"), encoding="utf-8")

    memory = MEMORY.read_text(encoding="utf-8", errors="ignore").rstrip()
    memory += "\n\n## 2026-07-07 正文源稿单位残留补修第二百三十三批\n\n"
    memory += "- 依据 `workbench/ocr/paddle_ocr/中/part02/page_0055.txt`、`page_0260.txt`、`page_0494.txt`，修复源稿 `5方吨/64.19方吨/101方头、9.1方吨` 为 `5万吨/64.19万吨/101万头、9.1万吨`。\n"
    memory += "- 当前正式阅读稿对应位置已正确，本批只补 `workbench/body_chapters` 源稿同步；报告：`output/reports/body_source_units_batch233_20260707.md`。\n"
    memory += "- 未做全局替换，未打开、展示或嵌入图片。\n"
    MEMORY.write_text(memory + "\n", encoding="utf-8")

    print(json.dumps({
        "changed_files": sum(1 for item in changes if item["items"]),
        "changed_items": sum(change["count"] for item in changes for change in item["items"]),
        "residual_total": sum(sum(files.values()) for files in residuals.values()),
        "report": str(REPORT_MD),
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
