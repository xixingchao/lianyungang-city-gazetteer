# -*- coding: utf-8 -*-
"""Repair source-backed dacron factory residue in middle finance chapter, batch 227."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = [
    ROOT / "output" / "final_reader" / "连云港市志_全书.html",
    ROOT / "output" / "final_reader" / "连云港市志_中册.html",
    ROOT / "workbench" / "body_chapters" / "第三十卷至第四十二卷（中part02）.md",
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
]
REPORT_JSON = ROOT / "output" / "reports" / "middle_finance_dacron_factory_batch227_20260707.json"
REPORT_MD = ROOT / "output" / "reports" / "middle_finance_dacron_factory_batch227_20260707.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260707_中册金融贷款涤纶厂残留补修第二百二十七批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"
EVIDENCE = ROOT / "workbench" / "ocr" / "paddle_ocr" / "中" / "part02" / "page_0371.txt"

OLD = "涤纶广涤纶长丝项目"
NEW = "涤纶厂涤纶长丝项目"


def ensure_evidence() -> None:
    text = EVIDENCE.read_text(encoding="utf-8", errors="ignore")
    if NEW not in text:
        raise SystemExit(f"missing evidence: {NEW}")


def main() -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    ensure_evidence()

    changes = []
    for path in TARGETS:
        text = path.read_text(encoding="utf-8", errors="ignore")
        count = text.count(OLD)
        if count:
            path.write_text(text.replace(OLD, NEW), encoding="utf-8")
        changes.append({"file": str(path.relative_to(ROOT)), "count": count})

    residuals = {
        str(path.relative_to(ROOT)): path.read_text(encoding="utf-8", errors="ignore").count(OLD)
        for path in TARGETS
    }
    payload = {
        "time": now,
        "old": OLD,
        "new": NEW,
        "changes": changes,
        "residuals": residuals,
        "evidence": str(EVIDENCE.relative_to(ROOT)),
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 中册金融贷款涤纶厂残留补修第二百二十七批",
        "",
        f"> 生成时间：{now}",
        "",
        "## 范围",
        "",
        "- 当前中册阅读稿、全书阅读稿、中册正文源稿、全书正文汇总。",
        "- 依据 PaddleOCR 页级文字证据，修复金融贷款章项目名称 `涤纶广涤纶长丝项目` 残留。",
        "- 未打开、展示或嵌入图片。",
        "",
        "## 修改统计",
        "",
        "| 文件 | 原文 | 新文 | 次数 | 证据 |",
        "|---|---|---|---:|---|",
    ]
    for item in changes:
        lines.append(f"| `{item['file']}` | `{OLD}` | `{NEW}` | {item['count']} | `{EVIDENCE.relative_to(ROOT)}` |")
    lines.extend(["", "## 残留计数", ""])
    for file, count in residuals.items():
        lines.append(f"- `{file}`：{count}")
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    PROGRESS.write_text(REPORT_MD.read_text(encoding="utf-8"), encoding="utf-8")

    memory = MEMORY.read_text(encoding="utf-8", errors="ignore").rstrip()
    memory += "\n\n## 2026-07-07 中册金融贷款涤纶厂残留补修第二百二十七批\n\n"
    memory += "- 依据 `workbench/ocr/paddle_ocr/中/part02/page_0371.txt`，修复金融贷款章项目名称 `涤纶广涤纶长丝项目 -> 涤纶厂涤纶长丝项目`。\n"
    memory += "- 同步范围：中册/全书阅读稿、中册正文源稿、全书正文汇总；报告：`output/reports/middle_finance_dacron_factory_batch227_20260707.md`。\n"
    memory += "- 本批未处理历史 `output/package` 旧交付包副本；未打开、展示或嵌入图片。\n"
    MEMORY.write_text(memory + "\n", encoding="utf-8")

    print(json.dumps({
        "changed_files": sum(1 for item in changes if item["count"]),
        "residual_total": sum(residuals.values()),
        "report": str(REPORT_MD),
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
