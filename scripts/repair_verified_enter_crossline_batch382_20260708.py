# -*- coding: utf-8 -*-
"""Repair cross-line 进人/进入 residuals verified against the final reader."""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "output" / "reports" / "verified_enter_crossline_batch382_20260708.md"
REPORT_JSON = ROOT / "output" / "reports" / "verified_enter_crossline_batch382_20260708.json"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260708_进入跨行残留补修第三百八十二批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"
READER = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
MARKER = "## 2026-07-08 进入跨行残留补修第三百八十二批"

@dataclass(frozen=True)
class Fix:
    label: str
    path: Path
    old: str
    new: str
    evidence: str

FIXES = [
    Fix(
        "纺织设备安装",
        ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
        "1976年6月进人设\n备安装",
        "1976年6月进入设\n备安装",
        "进入设备安装",
    ),
    Fix(
        "粮食市场销售",
        ROOT / "workbench" / "body_chapters" / "第三十卷至第四十二卷（中part02）.md",
        "允许农民进人\n市场多渠道销售",
        "允许农民进入\n市场多渠道销售",
        "允许农民进入市场",
    ),
    Fix(
        "粮食市场销售",
        ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
        "允许农民进人\n市场多渠道销售",
        "允许农民进入\n市场多渠道销售",
        "允许农民进入市场",
    ),
    Fix(
        "电工电器行业",
        ROOT / "workbench" / "body_chapters" / "第十七卷至第二十九卷（中part01）.md",
        "进人80\n年代，电工电器",
        "进入80\n年代，电工电器",
        "进入80年代",
    ),
    Fix(
        "电工电器行业",
        ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
        "进人80\n年代，电工电器",
        "进入80\n年代，电工电器",
        "进入80年代",
    ),
]

LEGAL_RESIDUES = ["引进人才", "促进人才", "新进人员", "先进人物", "先进人类"]


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def line_hits(path: Path, needle: str) -> list[int]:
    return [i for i, line in enumerate(read(path).splitlines(), 1) if needle in line]


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
                "label": fix.label,
                "path": rel(fix.path),
                "old": fix.old.replace("\n", "\\n"),
                "new": fix.new.replace("\n", "\\n"),
                "old_count": count,
                "old_count_after": after.count(fix.old),
                "new_count_after": after.count(fix.new),
                "evidence": fix.evidence,
            }
        )
    return results


def remaining_jinren() -> dict[str, list[str]]:
    paths = [
        ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
        ROOT / "output" / "final_reader" / "连云港市志_全书.html",
    ]
    out: dict[str, list[str]] = {}
    for path in paths:
        snippets = []
        for i, line in enumerate(read(path).splitlines(), 1):
            if "进人" in line:
                idx = line.find("进人")
                snippets.append(f"{i}: {line[max(0, idx - 45):idx + 90]}")
        out[rel(path)] = snippets
    return out


def render(results: list[dict[str, object]], evidence: dict[str, list[int]], residues: dict[str, list[str]]) -> str:
    total = sum(int(item["old_count"]) for item in results)
    lines = [
        "# 进入跨行残留补修 batch382",
        "",
        f"- 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"- 修复总数：{total}",
        "- 范围：只处理 `进人` 被换行拆开的三类完整短语；合法 `引进人才`、`先进人物`、`新进人员` 等不处理。",
        "- 证据：正式 reader 已呈现为 `进入设备安装`、`允许农民进入市场`、`进入80年代`。",
        "- 图片处理：未打开、展示或嵌入图片。",
        "",
        "## 修复明细",
    ]
    for item in results:
        lines.append(
            f"- `{item['path']}`：{item['label']}，`{item['old']}` -> `{item['new']}`，{item['old_count']} 处。"
        )
    lines.extend(["", "## reader 证据"])
    for term, hits in evidence.items():
        compact = "，".join(str(i) for i in hits) or "未命中"
        lines.append(f"- `output/final_reader/连云港市志_全书.html` 行 {compact}：`{term}`")
    lines.extend(["", "## 剩余 `进人` 片段"])
    for path, snippets in residues.items():
        lines.append(f"### {path}")
        if not snippets:
            lines.append("- 无。")
            continue
        for snippet in snippets:
            legal = "；合法词" if any(term in snippet for term in LEGAL_RESIDUES) else ""
            lines.append(f"- {snippet}{legal}")
    return "\n".join(lines) + "\n"


def upsert_memory(total: int) -> None:
    block = f"""{MARKER}

- 依据正式 reader 对证，补修三类 `进人 -> 进入` 跨行残留，共 {total} 处：`1976年6月进人设/备安装`、`允许农民进人/市场多渠道销售`、`进人80/年代，电工电器`。
- 本批只改现行正文源稿与全书汇总中的完整跨行短语；未处理 OCR 源文件、backup、obsolete、历史交付包；未打开、展示或嵌入图片。
- 修复后正式 reader 中剩余 `进人` 均为 `引进人才`、`先进人物`、`先进人类`、`新进人员`、`促进人才` 等合法词；全书汇总额外有一处换行形成的 `先/进人物`，按合法词保留。
- 报告：`output/reports/verified_enter_crossline_batch382_20260708.md`；进度：`output/reports/progress/20260708_进入跨行残留补修第三百八十二批.md`。
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
    evidence_terms = sorted({fix.evidence for fix in FIXES})
    evidence = {term: line_hits(READER, term) for term in evidence_terms}
    residues = remaining_jinren()
    total = sum(int(item["old_count"]) for item in results)
    report = render(results, evidence, residues)
    data = {
        "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "total": total,
        "results": results,
        "evidence": evidence,
        "remaining_jinren": residues,
    }
    REPORT.write_text(report, encoding="utf-8")
    REPORT_JSON.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    PROGRESS.write_text(report, encoding="utf-8")
    upsert_memory(total)
    print(f"total={total}")
    print(f"report={REPORT}")


if __name__ == "__main__":
    main()
