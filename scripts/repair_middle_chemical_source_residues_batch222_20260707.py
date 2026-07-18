# -*- coding: utf-8 -*-
"""Repair source-backed middle-volume chemical OCR residues, batch 222."""

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
REPORT_JSON = ROOT / "output" / "reports" / "middle_chemical_source_residues_batch222_20260707.json"
REPORT_MD = ROOT / "output" / "reports" / "middle_chemical_source_residues_batch222_20260707.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260707_中册化工专业名词源稿残留补修第二百二十二批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    ("二氯异氟尿酸钠", "二氯异氰尿酸钠", "conversion_source_risk_20260703.json:52632"),
    ("游离漠含量", "游离溴含量", "conversion_source_risk_20260703.json:36284"),
    ("游离漠\n含量", "游离溴\n含量", "conversion_source_risk_20260703.json:36284"),
    ("游离漠</p><p>含量", "游离溴</p><p>含量", "conversion_source_risk_20260703.json:36284"),
    ("八漠醚", "八溴醚", "workbench/table_entries/中/data/LYG-中-T130.json"),
    ("二漠丙基", "二溴丙基", "conversion_source_risk_20260703.json:36284"),
    ("炭砖年生能力达到5000饨", "炭砖年生产能力达到5000吨", "conversion_source_risk_20260703.json:52704"),
    ("第七节市化治制品", "第七节化冶制品", "workbench/indexes/连云港市志_全书_章节骨架.md:559"),
    ("市化治制品", "化冶制品", "workbench/indexes/连云港市志_全书_章节骨架.md:559"),
]

EVIDENCE_SNIPPETS = [
    "二氯异氰尿酸钠生产装置",
    "游离溴含量降至50PPM以下",
    "八溴醚",
    "炭砖年生产能力达到5000吨",
    "化冶制品",
]


def plain(html: str) -> str:
    return re.sub(r"<[^>]+>", "", html)


def main() -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    evidence_text = (ROOT / "output" / "reports" / "conversion_source_risk_20260703.json").read_text(encoding="utf-8", errors="ignore")
    evidence_text += "\n" + (ROOT / "workbench" / "table_entries" / "中" / "data" / "LYG-中-T130.json").read_text(encoding="utf-8", errors="ignore")
    evidence_text += "\n" + (ROOT / "workbench" / "indexes" / "连云港市志_全书_章节骨架.md").read_text(encoding="utf-8", errors="ignore")
    missing = [s for s in EVIDENCE_SNIPPETS if s not in evidence_text]
    if missing:
        raise SystemExit("missing evidence: " + "; ".join(missing))

    changes: list[dict[str, object]] = []
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
    for old, _new, _source in REPLACEMENTS:
        residuals[old] = {}
        for path in TARGETS:
            text = path.read_text(encoding="utf-8", errors="ignore")
            if path.suffix.lower() == ".html":
                text = plain(text)
            residuals[old][str(path.relative_to(ROOT))] = text.count(old)

    payload = {"time": now, "changes": changes, "residuals": residuals, "replacements": REPLACEMENTS}
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 中册化工专业名词源稿残留补修第二百二十二批",
        "",
        f"> 生成时间：{now}",
        "",
        "## 范围",
        "",
        "- 当前中册阅读稿、全书阅读稿、中册正文源稿、全书正文汇总。",
        "- 依据 `output/reports/conversion_source_risk_20260703.json`、`workbench/table_entries/中/data/LYG-中-T130.json` 和章节骨架中的正确摘录修复专业名词残留。",
        "- 未打开、展示或嵌入图片。",
        "",
        "## 修改统计",
        "",
        "| 文件 | 原文 | 新文 | 次数 | 证据 |",
        "|---|---|---|---:|---|",
    ]
    for item in changes:
        for change in item["changes"]:
            lines.append(f"| `{item['file']}` | `{change['old']}` | `{change['new']}` | {change['count']} | `{change['source']}` |")
    lines.extend(["", "## 残留计数", ""])
    for old, files in residuals.items():
        total = sum(files.values())
        lines.append(f"- `{old}`：{total}")
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    PROGRESS.write_text(REPORT_MD.read_text(encoding="utf-8"), encoding="utf-8")

    memory = MEMORY.read_text(encoding="utf-8", errors="ignore").rstrip()
    memory += "\n\n## 2026-07-07 中册化工专业名词源稿残留补修第二百二十二批\n\n"
    memory += "- 依据 `output/reports/conversion_source_risk_20260703.json`、`workbench/table_entries/中/data/LYG-中-T130.json`、章节骨架，修复中册化工段 `二氯异氟尿酸钠`、`游离漠含量/跨段变体`、`八漠醚`、`二漠丙基`、`炭砖年生能力达到5000饨`、`市化治制品` 等残留。\n"
    memory += "- 同步范围：中册/全书阅读稿、中册正文源稿、全书正文汇总；报告：`output/reports/middle_chemical_source_residues_batch222_20260707.md`。\n"
    memory += "- 未打开、展示或嵌入图片。\n"
    MEMORY.write_text(memory + "\n", encoding="utf-8")
    print(json.dumps({"changed_files": sum(1 for c in changes if c["changes"]), "report": str(REPORT_MD), "residuals": residuals}, ensure_ascii=False))


if __name__ == "__main__":
    main()
