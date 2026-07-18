# -*- coding: utf-8 -*-
"""Repair source-backed bromine/factory residues in middle volume, batch 223."""

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
REPORT_JSON = ROOT / "output" / "reports" / "middle_bromine_factory_residues_batch223_20260707.json"
REPORT_MD = ROOT / "output" / "reports" / "middle_bromine_factory_residues_batch223_20260707.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260707_中册海水化工溴字厂字残留补修第二百二十三批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    ("海水提漠", "海水提溴", "same paragraph uses `海水提溴项目`"),
    ("苦卤提漠", "苦卤提溴", "same paragraph uses `海水提溴项目`"),
    ("漠化工产品", "溴化工产品", "bromine chemical context"),
    ("漠</p><p>化工产品", "溴</p><p>化工产品", "bromine chemical context"),
    ("漠化</p><p>工产品", "溴化</p><p>工产品", "bromine chemical context"),
    ("漠素", "溴素", "conversion_source_risk_20260703.json and current paragraph"),
    ("漠</p><p>素", "溴</p><p>素", "conversion_source_risk_20260703.json and current paragraph"),
    ("该广生产的溴系列产品", "该厂生产的溴系列产品", "factory context"),
    ("工业漠乙烷", "工业溴乙烷", "bromine product list"),
    ("漠甲烷", "溴甲烷", "workbench/table_entries/中/data/LYG-中-T130.json"),
    ("漠</p><p>甲烷", "溴</p><p>甲烷", "workbench/table_entries/中/data/LYG-中-T130.json"),
    ("四漠苯酐", "四溴苯酐", "bromine product list"),
    ("除漠乙烷外", "除溴乙烷外", "bromine product list"),
    ("十漠联苯醚", "十溴联苯醚", "conversion_source_risk_20260703.json:36284"),
]

EVIDENCE_FILES = [
    ROOT / "output" / "reports" / "conversion_source_risk_20260703.json",
    ROOT / "workbench" / "table_entries" / "中" / "data" / "LYG-中-T130.json",
    ROOT / "output" / "reports" / "reader_readability_chemical_batch2_20260704.json",
]
EVIDENCE_SNIPPETS = ["溴甲烷", "溴乙烷", "溴素", "十溴联苯醚", "八溴醚"]


def plain(html: str) -> str:
    return re.sub(r"<[^>]+>", "", html)


def main() -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    evidence = "\n".join(p.read_text(encoding="utf-8", errors="ignore") for p in EVIDENCE_FILES)
    missing = [s for s in EVIDENCE_SNIPPETS if s not in evidence]
    if missing:
        raise SystemExit("missing evidence: " + "; ".join(missing))

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
        "# 中册海水化工溴字厂字残留补修第二百二十三批",
        "",
        f"> 生成时间：{now}",
        "",
        "## 范围",
        "",
        "- 当前中册阅读稿、全书阅读稿、中册正文源稿、全书正文汇总。",
        "- 依据既有化工页回源摘录、结构化表 `LYG-中-T130` 和同段上下文，修复海水化工一厂/黄海化工厂段溴字与厂字残留。",
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
        lines.append(f"- `{old}`：{sum(files.values())}")
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    PROGRESS.write_text(REPORT_MD.read_text(encoding="utf-8"), encoding="utf-8")

    memory = MEMORY.read_text(encoding="utf-8", errors="ignore").rstrip()
    memory += "\n\n## 2026-07-07 中册海水化工溴字厂字残留补修第二百二十三批\n\n"
    memory += "- 依据既有化工页回源摘录与 `workbench/table_entries/中/data/LYG-中-T130.json`，修复海水化工一厂/黄海化工厂段 `海水提漠`、`漠素`、`该广生产的溴系列产品`、`漠甲烷`、`四漠苯酐`、`除漠乙烷外`、`十漠联苯醚` 等残留。\n"
    memory += "- 同步范围：中册/全书阅读稿、中册正文源稿、全书正文汇总；报告：`output/reports/middle_bromine_factory_residues_batch223_20260707.md`。\n"
    memory += "- 未打开、展示或嵌入图片。\n"
    MEMORY.write_text(memory + "\n", encoding="utf-8")
    print(json.dumps({"changed_files": sum(1 for c in changes if c["changes"]), "report": str(REPORT_MD), "residuals": residuals}, ensure_ascii=False))


if __name__ == "__main__":
    main()
