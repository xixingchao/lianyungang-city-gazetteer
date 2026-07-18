# -*- coding: utf-8 -*-
"""Repair source-backed Huaiyin/Huaihai OCR residues in middle power chapter, batch 228."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = [
    ROOT / "output" / "final_reader" / "连云港市志_全书.html",
    ROOT / "output" / "final_reader" / "连云港市志_中册.html",
    ROOT / "workbench" / "body_chapters" / "第十七卷至第二十九卷（中part01）.md",
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
]
REPORT_JSON = ROOT / "output" / "reports" / "middle_power_huaihai_names_batch228_20260707.json"
REPORT_MD = ROOT / "output" / "reports" / "middle_power_huaihai_names_batch228_20260707.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260707_中册电力淮阴淮海盐专名残留补修第二百二十八批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    (
        "110千伏淮海输变电工程，准阴、连云港、盐城组成了以110千伏设备为主要骨架的准海盐",
        "110千伏淮海输变电工程，淮阴、连云港、盐城组成了以110千伏设备为主要骨架的淮海盐",
        "workbench/ocr/paddle_ocr/中/part01/page_0330.txt",
    ),
    (
        "设备为主要骨架的准海盐电网。此时，连云港地区电网拥有110千伏变电所1座",
        "设备为主要骨架的淮海盐电网。此时，连云港地区电网拥有110千伏变电所1座",
        "workbench/ocr/paddle_ocr/中/part01/page_0346.txt",
    ),
    (
        "统一分配，连云港地区负荷分配比例占淮海盐电网总负荷的30.7%。1979年，准海盐电",
        "统一分配，连云港地区负荷分配比例占淮海盐电网总负荷的30.7%。1979年，淮海盐电",
        "workbench/ocr/paddle_ocr/中/part01/page_0371.txt",
    ),
]
EVIDENCE = {
    "workbench/ocr/paddle_ocr/中/part01/page_0330.txt": ["淮阴、连云港、盐城组成了以110千伏设备为主要骨架的淮海盐"],
    "workbench/ocr/paddle_ocr/中/part01/page_0346.txt": ["设备为主要骨架的淮海盐电网"],
    "workbench/ocr/paddle_ocr/中/part01/page_0371.txt": ["淮海盐电网中心调度所", "1979年，淮海盐电"],
}


def ensure_evidence() -> None:
    missing = []
    for rel, snippets in EVIDENCE.items():
        text = (ROOT / rel).read_text(encoding="utf-8", errors="ignore")
        for snippet in snippets:
            if snippet not in text:
                missing.append(f"{rel}: {snippet}")
    if missing:
        raise SystemExit("missing evidence: " + "; ".join(missing))


def main() -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    ensure_evidence()

    changes = []
    for path in TARGETS:
        text = path.read_text(encoding="utf-8", errors="ignore")
        original = text
        file_changes = []
        for old, new, evidence in REPLACEMENTS:
            count = text.count(old)
            if count:
                text = text.replace(old, new)
                file_changes.append({"old": old, "new": new, "count": count, "evidence": evidence})
        if text != original:
            path.write_text(text, encoding="utf-8")
        changes.append({"file": str(path.relative_to(ROOT)), "changes": file_changes})

    residuals = {}
    for old, _, _ in REPLACEMENTS:
        residuals[old] = {str(path.relative_to(ROOT)): path.read_text(encoding="utf-8", errors="ignore").count(old) for path in TARGETS}

    payload = {"time": now, "changes": changes, "residuals": residuals, "evidence": EVIDENCE}
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 中册电力淮阴淮海盐专名残留补修第二百二十八批",
        "",
        f"> 生成时间：{now}",
        "",
        "## 范围",
        "",
        "- 当前中册阅读稿、全书阅读稿、中册正文源稿、全书正文汇总。",
        "- 依据 PaddleOCR 页级文字证据，修复电力工业卷 `准阴/准海盐` 专名残留。",
        "- 未打开、展示或嵌入图片。",
        "",
        "## 修改统计",
        "",
        "| 文件 | 原文 | 新文 | 次数 | 证据 |",
        "|---|---|---|---:|---|",
    ]
    for item in changes:
        for change in item["changes"]:
            lines.append(f"| `{item['file']}` | `{change['old']}` | `{change['new']}` | {change['count']} | `{change['evidence']}` |")
    lines.extend(["", "## 残留计数", ""])
    for pattern, files in residuals.items():
        lines.append(f"- `{pattern}`：{sum(files.values())}")
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    PROGRESS.write_text(REPORT_MD.read_text(encoding="utf-8"), encoding="utf-8")

    memory = MEMORY.read_text(encoding="utf-8", errors="ignore").rstrip()
    memory += "\n\n## 2026-07-07 中册电力淮阴淮海盐专名残留补修第二百二十八批\n\n"
    memory += "- 依据 `workbench/ocr/paddle_ocr/中/part01/page_0330.txt`、`page_0346.txt`、`page_0371.txt`，修复电力工业卷 `准阴/准海盐 -> 淮阴/淮海盐` 专名残留。\n"
    memory += "- 同步范围：中册/全书阅读稿、中册正文源稿、全书正文汇总；报告：`output/reports/middle_power_huaihai_names_batch228_20260707.md`。\n"
    memory += "- `客房资信` 等语义可疑但 OCR 仍不支持的项未猜改；未打开、展示或嵌入图片。\n"
    MEMORY.write_text(memory + "\n", encoding="utf-8")

    print(json.dumps({
        "changed_files": sum(1 for item in changes if item["changes"]),
        "changed_items": sum(change["count"] for item in changes for change in item["changes"]),
        "residual_total": sum(sum(files.values()) for files in residuals.values()),
        "report": str(REPORT_MD),
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
