# -*- coding: utf-8 -*-
"""Repair verified 调人/调入 OCR residues in sentence contexts."""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "output" / "reports" / "verified_diaoru_batch389_20260708.md"
REPORT_JSON = ROOT / "output" / "reports" / "verified_diaoru_batch389_20260708.json"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260708_调入残留补修第三百八十九批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"
READER = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
MARKER = "## 2026-07-08 调入残留补修第三百八十九批"

@dataclass(frozen=True)
class Fix:
    old: str
    new: str
    paths: tuple[Path, ...]
    label: str

FIXES = [
    Fix("调人1511", "调入1511", (ROOT / "workbench/body_chapters/上/第十卷至第十六卷（part03）.md", ROOT / "workbench/body_chapters/连云港市志_上册_正文汇总.md", ROOT / "workbench/body_chapters/连云港市志_全书_正文汇总.md"), "工业设备调入"),
    Fix("调人大批救济粮", "调入大批救济粮", (ROOT / "workbench/body_chapters/第三十卷至第四十二卷（中part02）.md", ROOT / "workbench/body_chapters/连云港市志_全书_正文汇总.md"), "救济粮调入"),
    Fix("调人75吨", "调入75吨", (ROOT / "workbench/body_chapters/第三十卷至第四十二卷（中part02）.md", ROOT / "workbench/body_chapters/连云港市志_全书_正文汇总.md"), "生油调入"),
    Fix("调人各粮", "调入各粮", (ROOT / "workbench/body_chapters/第三十卷至第四十二卷（中part02）.md", ROOT / "workbench/body_chapters/连云港市志_全书_正文汇总.md"), "粮食调入"),
    Fix("调人山东的生油", "调入山东的生油", (ROOT / "workbench/body_chapters/第三十卷至第四十二卷（中part02）.md", ROOT / "workbench/body_chapters/连云港市志_全书_正文汇总.md"), "生油调入"),
    Fix("陈雨清调人省男子篮球队", "陈雨清调入省男子篮球队", (ROOT / "workbench/body_chapters/第五十二卷至第六十卷及附录（下part02）.md", ROOT / "workbench/body_chapters/连云港市志_全书_正文汇总.md"), "运动员调入"),
    Fix("李正巧、徐廷英调人省", "李正巧、徐廷英调入省", (ROOT / "workbench/body_chapters/第五十二卷至第六十卷及附录（下part02）.md", ROOT / "workbench/body_chapters/连云港市志_全书_正文汇总.md"), "运动员调入"),
    Fix("调人千余名干部", "调入千余名干部", (ROOT / "workbench/body_chapters/第四十三卷至第五十一卷（下part01）.md", ROOT / "workbench/body_chapters/连云港市志_全书_正文汇总.md"), "干部调入"),
    Fix("引进调人", "引进调入", (ROOT / "workbench/body_chapters/第四十三卷至第五十一卷（下part01）.md", ROOT / "workbench/body_chapters/连云港市志_全书_正文汇总.md"), "人才调入"),
]

EVIDENCE_TERMS = [
    "调入1511",
    "调入大批救济粮",
    "调入75吨",
    "调入各粮",
    "调入山东的生油",
    "陈雨清调入省男子篮球队",
    "李正巧、徐廷英调入省",
    "调入千余名干部",
    "引进调入",
]
LEGAL_TERMS = ["催调人员", "治调人员", "抽调人员", "招工、调人等方式"]


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def line_hits(path: Path, needle: str) -> list[int]:
    return [i for i, line in enumerate(read(path).splitlines(), 1) if needle in line]


def remaining() -> dict[str, list[str]]:
    out = {}
    for path in [ROOT / "workbench/body_chapters/连云港市志_全书_正文汇总.md", READER]:
        snippets = []
        for i, line in enumerate(read(path).splitlines(), 1):
            if "调人" in line:
                idx = line.find("调人")
                snippets.append(f"{i}: {line[max(0, idx - 45):idx + 95]}")
        out[rel(path)] = snippets
    return out


def main() -> None:
    results = []
    for fix in FIXES:
        for path in fix.paths:
            text = read(path)
            count = text.count(fix.old)
            if count:
                path.write_text(text.replace(fix.old, fix.new), encoding="utf-8")
            after = read(path)
            results.append({"path": rel(path), "label": fix.label, "old": fix.old, "new": fix.new, "old_count": count, "old_count_after": after.count(fix.old), "new_count_after": after.count(fix.new)})
    evidence = {term: line_hits(READER, term) for term in EVIDENCE_TERMS}
    residues = remaining()
    total = sum(item["old_count"] for item in results)

    lines = [
        "# 调入残留补修 batch389",
        "",
        f"- 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"- 修复总数：{total}",
        "- 范围：现行源稿与汇总中由正式 reader 对证的成句 `调人 -> 调入` 残留。",
        "- 原则：保留 `催调人员`、`治调人员`、`抽调人员`、`招工、调人等方式` 等合法词；表格孤立 `调人` 表头另行待核。",
        "- 图片处理：未打开、展示或嵌入图片。",
        "",
        "## 修复明细",
    ]
    for item in results:
        if item["old_count"]:
            lines.append(f"- `{item['path']}`：`{item['old']}` -> `{item['new']}`，{item['old_count']} 处。")
    lines.extend(["", "## reader 证据"])
    for term, hits in evidence.items():
        compact = "，".join(str(i) for i in hits) or "未命中"
        lines.append(f"- `output/final_reader/连云港市志_全书.html` 行 {compact}：`{term}`")
    lines.extend(["", "## 剩余 `调人` 片段"])
    for path, snippets in residues.items():
        lines.append(f"### {path}")
        if not snippets:
            lines.append("- 无。")
            continue
        for snippet in snippets:
            legal = "；合法词/待表格核" if any(term in snippet for term in LEGAL_TERMS) or snippet.strip().endswith("调人") else ""
            lines.append(f"- {snippet}{legal}")
    report = "\n".join(lines) + "\n"
    data = {"time": datetime.now().strftime("%Y-%m-%d %H:%M"), "total": total, "results": results, "evidence": evidence, "remaining_diaoren": residues}
    REPORT.write_text(report, encoding="utf-8")
    REPORT_JSON.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    PROGRESS.write_text(report, encoding="utf-8")

    block = f"""{MARKER}

- 依据正式 reader 对证，补修成句 `调人 -> 调入` 残留 {total} 处，覆盖设备、救济粮/粮油、运动员、干部和人才引进等语境。
- 代表修复：`调人1511 -> 调入1511`、`调人大批救济粮 -> 调入大批救济粮`、`陈雨清调人省男子篮球队 -> 陈雨清调入省男子篮球队`、`调人千余名干部 -> 调入千余名干部`、`引进调人 -> 引进调入`。
- 保留 `催调人员`、`治调人员`、`抽调人员`、`招工、调人等方式` 等合法词；表格孤立 `调人` 表头另行待核；未处理 OCR 源文件、backup、obsolete、历史交付包；未打开、展示或嵌入图片。
- 报告：`output/reports/verified_diaoru_batch389_20260708.md`；进度：`output/reports/progress/20260708_调入残留补修第三百八十九批.md`。
"""
    old_mem = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    start = old_mem.find(MARKER)
    if start < 0:
        MEMORY.write_text(old_mem.rstrip() + "\n\n" + block.strip() + "\n", encoding="utf-8")
    else:
        next_start = old_mem.find("\n## ", start + 1)
        MEMORY.write_text(old_mem[:start].rstrip() + "\n\n" + block.strip() + ("\n" if next_start < 0 else old_mem[next_start:]), encoding="utf-8")

    print(f"total={total}")
    print(f"report={REPORT}")


if __name__ == "__main__":
    main()
