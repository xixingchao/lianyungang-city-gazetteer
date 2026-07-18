# -*- coding: utf-8 -*-
"""Repair selected verified 编人/编入 OCR residues in current sources."""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "output" / "reports" / "verified_bianru_batch387_20260708.md"
REPORT_JSON = ROOT / "output" / "reports" / "verified_bianru_batch387_20260708.json"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260708_编入残留补修第三百八十七批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"
READER = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
MARKER = "## 2026-07-08 编入残留补修第三百八十七批"

@dataclass(frozen=True)
class Fix:
    path: Path
    old: str
    new: str
    label: str

FIXES = []
for path in [
    ROOT / "workbench" / "body_chapters" / "第三十卷至第四十二卷（中part02）.md",
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
]:
    FIXES.append(Fix(path, "编人华中第六军分", "编入华中第六军分", "军事编入"))
for path in [
    ROOT / "workbench" / "body_chapters" / "第五十二卷至第六十卷及附录（下part02）.md",
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
]:
    FIXES.append(Fix(path, "编人东海县常备大队", "编入东海县常备大队", "抗日队伍编入"))
for path in [
    ROOT / "workbench" / "body_chapters" / "第四十三卷至第五十一卷（下part01）.md",
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
]:
    FIXES.extend(
        [
            Fix(path, "编人该团", "编入该团", "军事编入"),
            Fix(path, "编人预备役", "编入预备役", "预备役编入"),
            Fix(path, "商团编人县长", "商团编入县长", "商团编入"),
        ]
    )

EVIDENCE_TERMS = [
    "编入华中第六军分区",
    "编入东海县常备大队",
    "编入该团",
    "编入预备役",
    "商团编入县长朱爱周领导的游击队",
]
LEGAL_TERMS = ["采编人员", "在编人员", "扩编人防专业队伍"]


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def line_hits(path: Path, needle: str) -> list[int]:
    return [i for i, line in enumerate(read(path).splitlines(), 1) if needle in line]


def remaining_bianren() -> dict[str, list[str]]:
    paths = [
        ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
        READER,
    ]
    out: dict[str, list[str]] = {}
    for path in paths:
        snippets = []
        for i, line in enumerate(read(path).splitlines(), 1):
            if "编人" in line:
                idx = line.find("编人")
                snippets.append(f"{i}: {line[max(0, idx - 45):idx + 95]}")
        out[rel(path)] = snippets
    return out


def apply_fixes() -> list[dict[str, object]]:
    results = []
    for fix in FIXES:
        text = read(fix.path)
        count = text.count(fix.old)
        if count:
            fix.path.write_text(text.replace(fix.old, fix.new), encoding="utf-8")
        after = read(fix.path)
        results.append(
            {
                "path": rel(fix.path),
                "label": fix.label,
                "old": fix.old,
                "new": fix.new,
                "old_count": count,
                "old_count_after": after.count(fix.old),
                "new_count_after": after.count(fix.new),
            }
        )
    return results


def render(results: list[dict[str, object]], evidence: dict[str, list[int]], residues: dict[str, list[str]]) -> str:
    total = sum(int(item["old_count"]) for item in results)
    lines = [
        "# 编入残留补修 batch387",
        "",
        f"- 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"- 修复总数：{total}",
        "- 范围：现行分册源稿与全书汇总中军事、预备役、商团语境的 `编人 -> 编入` 完整短语。",
        "- 原则：保留 `采编人员`、`在编人员`、`扩编人防专业队伍` 等合法词。",
        "- 图片处理：未打开、展示或嵌入图片。",
        "",
        "## 修复明细",
    ]
    for item in results:
        if int(item["old_count"]):
            lines.append(f"- `{item['path']}`：`{item['old']}` -> `{item['new']}`，{item['old_count']} 处。")
    lines.extend(["", "## reader 证据"])
    for term, hits in evidence.items():
        compact = "，".join(str(i) for i in hits) or "未命中"
        lines.append(f"- `output/final_reader/连云港市志_全书.html` 行 {compact}：`{term}`")
    lines.extend(["", "## 剩余 `编人` 片段"])
    for path, snippets in residues.items():
        lines.append(f"### {path}")
        if not snippets:
            lines.append("- 无。")
            continue
        for snippet in snippets:
            legal = "；合法词" if any(term in snippet for term in LEGAL_TERMS) else ""
            lines.append(f"- {snippet}{legal}")
    return "\n".join(lines) + "\n"


def upsert_memory(total: int) -> None:
    block = f"""{MARKER}

- 依据正式 reader 对证，补修军事、预备役、商团语境中的 `编人 -> 编入` 完整短语，共 {total} 处。
- 代表修复：`编人华中第六军分区 -> 编入华中第六军分区`、`编人东海县常备大队 -> 编入东海县常备大队`、`编人该团 -> 编入该团`、`编人预备役 -> 编入预备役`、`商团编人县长朱爱周领导的游击队 -> 商团编入...`。
- 合法 `采编人员`、`在编人员`、`扩编人防专业队伍` 保留；未处理 OCR 源文件、backup、obsolete、历史交付包；未打开、展示或嵌入图片。
- 报告：`output/reports/verified_bianru_batch387_20260708.md`；进度：`output/reports/progress/20260708_编入残留补修第三百八十七批.md`。
"""
    old = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    start = old.find(MARKER)
    if start < 0:
        MEMORY.write_text(old.rstrip() + "\n\n" + block.strip() + "\n", encoding="utf-8")
        return
    next_start = old.find("\n## ", start + 1)
    MEMORY.write_text(old[:start].rstrip() + "\n\n" + block.strip() + ("\n" if next_start < 0 else old[next_start:]), encoding="utf-8")


def main() -> None:
    results = apply_fixes()
    evidence = {term: line_hits(READER, term) for term in EVIDENCE_TERMS}
    residues = remaining_bianren()
    total = sum(int(item["old_count"]) for item in results)
    report = render(results, evidence, residues)
    data = {
        "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "total": total,
        "results": results,
        "evidence": evidence,
        "remaining_bianren": residues,
    }
    REPORT.write_text(report, encoding="utf-8")
    REPORT_JSON.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    PROGRESS.write_text(report, encoding="utf-8")
    upsert_memory(total)
    print(f"total={total}")
    print(f"report={REPORT}")


if __name__ == "__main__":
    main()
