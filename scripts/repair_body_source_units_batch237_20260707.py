# -*- coding: utf-8 -*-
"""Repair source-backed follow-up unit residues, batch 237."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = [
    ROOT / "workbench" / "body_chapters" / "上" / "第四卷至第十卷（part02）.md",
    ROOT / "workbench" / "body_chapters" / "上" / "第十卷至第十六卷（part03）.md",
    ROOT / "workbench" / "body_chapters" / "第十七卷至第二十九卷（中part01）.md",
    ROOT / "workbench" / "body_chapters" / "连云港市志_上册_正文汇总.md",
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
]
REPORT_JSON = ROOT / "output" / "reports" / "body_source_units_followup_batch237_20260707.json"
REPORT_MD = ROOT / "output" / "reports" / "body_source_units_followup_batch237_20260707.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260707_正文源稿单位残留补修第二百三十七批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"
ITEMS = [
    (
        "年吞吐量纳3500～4000方吨",
        "年吞吐量约3500～4000万吨",
        "上/part02/page_0034.txt",
        "年吞吐量约3500~4000万吨",
    ),
    (
        "从两掠夺淮盐（主要是淮北盐）至少110多方吨",
        "从两淮掠夺淮盐（主要是淮北盐）至少110多万吨",
        "上/part02/page_0132.txt",
        "从两淮掠夺淮盐(主要是淮北盐)至少110多万吨",
    ),
    (
        "粮食产量从18方吨提高到31万吨",
        "粮食产量从18万吨提高到31万吨",
        "上/part03/page_0045.txt",
        "粮食产量从18万吨提高到31万吨",
    ),
    (
        "实产合成氨3.64方吨",
        "实产合成氨3.64万吨",
        "中/part01/page_0167.txt",
        "实产合成氨3.64万吨",
    ),
]


def evidence_path(rel: str) -> Path:
    volume, part, page = rel.split("/")
    return ROOT / "workbench" / "ocr" / "paddle_ocr" / volume / part / page


def normalize(text: str) -> str:
    return text.replace("（", "(").replace("）", ")").replace("～", "~")


def ensure_evidence() -> None:
    for _, _, rel, snippet in ITEMS:
        path = evidence_path(rel)
        text = normalize(path.read_text(encoding="utf-8", errors="ignore"))
        if normalize(snippet) not in text:
            raise SystemExit(f"missing evidence: {path.relative_to(ROOT)}: {snippet}")


def main() -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    ensure_evidence()
    changes = []
    for path in TARGETS:
        text = path.read_text(encoding="utf-8", errors="ignore")
        file_items = []
        for old, new, rel, _ in ITEMS:
            count = text.count(old)
            if count:
                text = text.replace(old, new)
                file_items.append({"old": old, "new": new, "count": count, "evidence": str(evidence_path(rel).relative_to(ROOT))})
        if file_items:
            path.write_text(text, encoding="utf-8")
        changes.append({"file": str(path.relative_to(ROOT)), "items": file_items})

    residuals = {
        old: {str(path.relative_to(ROOT)): path.read_text(encoding="utf-8", errors="ignore").count(old) for path in TARGETS}
        for old, _, _, _ in ITEMS
    }
    payload = {"time": now, "changes": changes, "residuals": residuals}
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 正文源稿单位残留补修第二百三十七批",
        "",
        f"> 生成时间：{now}",
        "",
        "## 范围",
        "",
        "- 修复 Batch 236 后漏网的同页单位残留，并补正同句中页级 OCR 已明确的 `约`、`两淮`。",
        "- 同步正常命名正文源稿和汇总稿；未处理旧交付包、obsolete 或乱码副本。",
        "- 未做全局替换，未打开、展示或嵌入图片。",
        "",
        "## 修改统计",
        "",
        "| 文件 | 原文 | 新文 | 次数 | 证据 |",
        "|---|---|---|---:|---|",
    ]
    for item in changes:
        for change in item["items"]:
            lines.append(f"| `{item['file']}` | `{change['old']}` | `{change['new']}` | {change['count']} | `{change['evidence']}` |")
    lines.extend(["", "## 残留计数", ""])
    for old, files in residuals.items():
        lines.append(f"- `{old}`：{sum(files.values())}")
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    PROGRESS.write_text(REPORT_MD.read_text(encoding="utf-8"), encoding="utf-8")

    memory = MEMORY.read_text(encoding="utf-8", errors="ignore").rstrip()
    memory += "\n\n## 2026-07-07 正文源稿单位残留补修第二百三十七批\n\n"
    memory += "- 依据上册 `part02/page_0034.txt`、`part02/page_0132.txt`、`part03/page_0045.txt` 和中册 `part01/page_0167.txt`，修复 `3500～4000方吨/110多方吨/18方吨/3.64方吨` 残留。\n"
    memory += "- 同步补正同句 `吞吐量纳 -> 吞吐量约`、`从两掠夺 -> 从两淮掠夺`；报告：`output/reports/body_source_units_followup_batch237_20260707.md`。\n"
    memory += "- 未处理旧交付包、obsolete 或乱码副本；未做全局替换，未打开、展示或嵌入图片。\n"
    MEMORY.write_text(memory + "\n", encoding="utf-8")

    print(json.dumps({
        "changed_files": sum(1 for item in changes if item["items"]),
        "changed_items": sum(change["count"] for item in changes for change in item["items"]),
        "residual_total": sum(sum(files.values()) for files in residuals.values()),
        "report": str(REPORT_MD),
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
