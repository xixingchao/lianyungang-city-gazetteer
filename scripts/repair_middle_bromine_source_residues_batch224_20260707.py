# -*- coding: utf-8 -*-
"""Repair source-backed bromine residues in middle volume, batch 224."""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = [
    ROOT / "output" / "final_reader" / "连云港市志_全书.html",
    ROOT / "output" / "final_reader" / "连云港市志_中册.html",
    ROOT / "workbench" / "body_chapters" / "第十七卷至第二十九卷（中part01）.md",
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
]
REPORT_JSON = ROOT / "output" / "reports" / "middle_bromine_source_residues_batch224_20260707.json"
REPORT_MD = ROOT / "output" / "reports" / "middle_bromine_source_residues_batch224_20260707.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260707_中册海水化工溴字源稿残留补修第二百二十四批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    ("市海水化工-厂", "市海水化工一厂", "workbench/ocr/paddle_ocr/中/part01/page_0154.txt"),
    ("使漠\n素年生产能力", "使溴\n素年生产能力", "workbench/ocr/paddle_ocr/中/part01/page_0154.txt"),
    ("使漠</p><p>素年生产能力", "使溴</p><p>素年生产能力", "workbench/ocr/paddle_ocr/中/part01/page_0154.txt"),
    ("四澳乙烷、澳乙烷", "四溴乙烷、溴乙烷", "workbench/ocr/paddle_ocr/中/part01/page_0159.txt"),
    ("四溴乙浣100吨", "四溴乙烷100吨", "workbench/ocr/paddle_ocr/中/part01/page_0159.txt"),
    ("海水化工~厂", "海水化工一厂", "workbench/ocr/paddle_ocr/中/part01/page_0159.txt"),
    ("除溴乙烷外，其余均为国内独家生产。漠\n甲烷", "除溴乙烷外，其余均为国内独家生产。溴\n甲烷", "workbench/ocr/paddle_ocr/中/part01/page_0162.txt"),
    ("除溴乙烷外，其余均为国内独家生产。漠</p><p>甲烷", "除溴乙烷外，其余均为国内独家生产。溴</p><p>甲烷", "workbench/ocr/paddle_ocr/中/part01/page_0162.txt"),
]

EVIDENCE = {
    "workbench/ocr/paddle_ocr/中/part01/page_0154.txt": ["市海水化工一厂", "使溴\n素年生产能力"],
    "workbench/ocr/paddle_ocr/中/part01/page_0159.txt": ["四溴乙烷、溴乙烷", "海水化工一厂采用无后处理法"],
    "workbench/ocr/paddle_ocr/中/part01/page_0162.txt": ["除溴乙烷外，其余均为国内独家生产。溴\n甲烷"],
}

RESIDUE_PATTERNS = [
    "市海水化工-厂",
    "使漠\n素年生产能力",
    "使漠</p><p>素年生产能力",
    "四澳乙烷",
    "澳乙烷",
    "四溴乙浣",
    "海水化工~厂",
    "除溴乙烷外，其余均为国内独家生产。漠\n甲烷",
    "除溴乙烷外，其余均为国内独家生产。漠</p><p>甲烷",
]


def plain(html: str) -> str:
    return re.sub(r"<[^>]+>", "", html)


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
        for old, new, source in REPLACEMENTS:
            count = text.count(old)
            if count:
                text = text.replace(old, new)
                file_changes.append({"old": old, "new": new, "count": count, "source": source})
        if text != original:
            path.write_text(text, encoding="utf-8")
        changes.append({"file": str(path.relative_to(ROOT)), "changes": file_changes})

    residuals = {}
    for pattern in RESIDUE_PATTERNS:
        residuals[pattern] = {}
        for path in TARGETS:
            text = path.read_text(encoding="utf-8", errors="ignore")
            residuals[pattern][str(path.relative_to(ROOT))] = text.count(pattern)

    payload = {"time": now, "changes": changes, "residuals": residuals, "evidence": EVIDENCE}
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 中册海水化工溴字源稿残留补修第二百二十四批",
        "",
        f"> 生成时间：{now}",
        "",
        "## 范围",
        "",
        "- 当前中册阅读稿、全书阅读稿、中册正文源稿、全书正文汇总。",
        "- 依据 PaddleOCR 页级文字证据，补修 223 批后残留的跨行溴字、乙烷名词和厂名残留。",
        "- 未打开、展示或嵌入图片。",
        "",
        "## 修改统计",
        "",
        "| 文件 | 原文 | 新文 | 次数 | 证据 |",
        "|---|---|---|---:|---|",
    ]
    for item in changes:
        for change in item["changes"]:
            old = change["old"].replace("\n", "\\n")
            new = change["new"].replace("\n", "\\n")
            lines.append(f"| `{item['file']}` | `{old}` | `{new}` | {change['count']} | `{change['source']}` |")
    lines.extend(["", "## 残留计数", ""])
    for pattern, files in residuals.items():
        display = pattern.replace("\n", "\\n")
        lines.append(f"- `{display}`：{sum(files.values())}")
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    PROGRESS.write_text(REPORT_MD.read_text(encoding="utf-8"), encoding="utf-8")

    memory = MEMORY.read_text(encoding="utf-8", errors="ignore").rstrip()
    memory += "\n\n## 2026-07-07 中册海水化工溴字源稿残留补修第二百二十四批\n\n"
    memory += "- 依据 `workbench/ocr/paddle_ocr/中/part01/page_0154.txt`、`page_0159.txt`、`page_0162.txt`，补修 223 批后残留的 `使漠/素年生产能力`、`四澳乙烷/澳乙烷`、`四溴乙浣`、`海水化工~厂`、`除溴乙烷外...漠/甲烷` 等。\n"
    memory += "- 同步范围：中册/全书阅读稿、中册正文源稿、全书正文汇总；报告：`output/reports/middle_bromine_source_residues_batch224_20260707.md`。\n"
    memory += "- 未打开、展示或嵌入图片。\n"
    MEMORY.write_text(memory + "\n", encoding="utf-8")

    print(json.dumps({"changed_files": sum(1 for c in changes if c["changes"]), "report": str(REPORT_MD), "residual_total": sum(sum(v.values()) for v in residuals.values())}, ensure_ascii=False))


if __name__ == "__main__":
    main()
