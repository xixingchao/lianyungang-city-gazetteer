# -*- coding: utf-8 -*-
"""Repair cross-line 编人/编入 residues verified against final reader."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "output" / "reports" / "verified_bianru_crossline_batch388_20260708.md"
REPORT_JSON = ROOT / "output" / "reports" / "verified_bianru_crossline_batch388_20260708.json"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260708_编入跨行残留补修第三百八十八批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"
READER = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
MARKER = "## 2026-07-08 编入跨行残留补修第三百八十八批"

FIXES = [
    (
        ROOT / "workbench" / "body_chapters" / "第五十二卷至第六十卷及附录（下part02）.md",
        "编人东海\n县常备大队",
        "编入东海\n县常备大队",
        "抗日队伍编入",
    ),
    (
        ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
        "编人东海\n县常备大队",
        "编入东海\n县常备大队",
        "抗日队伍编入",
    ),
    (
        ROOT / "workbench" / "body_chapters" / "第四十三卷至第五十一卷（下part01）.md",
        "登记编人预备\n役",
        "登记编入预备\n役",
        "预备役编入",
    ),
    (
        ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
        "登记编人预备\n役",
        "登记编入预备\n役",
        "预备役编入",
    ),
]
EVIDENCE_TERMS = [
    "抗日铁血锄奸大队被东海县政府编入东海县常备大队",
    "登记编入预备役",
]
LEGAL_TERMS = ["采编人员", "在编人员", "扩编人防专业队伍"]


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def line_hits(path: Path, needle: str) -> list[int]:
    return [i for i, line in enumerate(read(path).splitlines(), 1) if needle in line]


def remaining() -> dict[str, list[str]]:
    out = {}
    for path in [ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md", READER]:
        snippets = []
        for i, line in enumerate(read(path).splitlines(), 1):
            if "编人" in line:
                idx = line.find("编人")
                snippets.append(f"{i}: {line[max(0, idx - 45):idx + 95]}")
        out[rel(path)] = snippets
    return out


def main() -> None:
    results = []
    for path, old, new, label in FIXES:
        text = read(path)
        count = text.count(old)
        if count:
            path.write_text(text.replace(old, new), encoding="utf-8")
        after = read(path)
        results.append(
            {
                "path": rel(path),
                "label": label,
                "old": old.replace("\n", "\\n"),
                "new": new.replace("\n", "\\n"),
                "old_count": count,
                "old_count_after": after.count(old),
                "new_count_after": after.count(new),
            }
        )
    evidence = {term: line_hits(READER, term) for term in EVIDENCE_TERMS}
    residues = remaining()
    total = sum(item["old_count"] for item in results)

    lines = [
        "# 编入跨行残留补修 batch388",
        "",
        f"- 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"- 修复总数：{total}",
        "- 范围：只处理 `编人` 被换行拆开的 `编人东海/县常备大队` 与 `登记编人预备/役`。",
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
    lines.extend(["", "## 剩余 `编人` 片段"])
    for path, snippets in residues.items():
        lines.append(f"### {path}")
        if not snippets:
            lines.append("- 无。")
            continue
        for snippet in snippets:
            legal = "；合法词" if any(term in snippet for term in LEGAL_TERMS) else ""
            lines.append(f"- {snippet}{legal}")
    report = "\n".join(lines) + "\n"
    data = {"time": datetime.now().strftime("%Y-%m-%d %H:%M"), "total": total, "results": results, "evidence": evidence, "remaining_bianren": residues}
    REPORT.write_text(report, encoding="utf-8")
    REPORT_JSON.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    PROGRESS.write_text(report, encoding="utf-8")

    block = f"""{MARKER}

- 依据正式 reader 对证，补修 `编人` 跨行残留 {total} 处：`编人东海/县常备大队 -> 编入东海/县常备大队`、`登记编人预备/役 -> 登记编入预备/役`。
- 合法 `采编人员`、`在编人员`、`扩编人防专业队伍` 保留；未处理 OCR 源文件、backup、obsolete、历史交付包；未打开、展示或嵌入图片。
- 报告：`output/reports/verified_bianru_crossline_batch388_20260708.md`；进度：`output/reports/progress/20260708_编入跨行残留补修第三百八十八批.md`。
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
