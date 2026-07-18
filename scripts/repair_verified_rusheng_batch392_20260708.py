# -*- coding: utf-8 -*-
"""Repair verified 入声 OCR residues in the dialect chapter."""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOWER_SRC = ROOT / "workbench" / "body_chapters" / "第五十二卷至第六十卷及附录（下part02）.md"
FULL_SRC = ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md"
LOWER_READER = ROOT / "output" / "final_reader" / "连云港市志_下册.html"
FULL_READER = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT = ROOT / "output" / "reports" / "verified_rusheng_batch392_20260708.md"
REPORT_JSON = ROOT / "output" / "reports" / "verified_rusheng_batch392_20260708.json"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260708_入声残留补修第三百九十二批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"
MARKER = "## 2026-07-08 入声残留补修第三百九十二批"


@dataclass(frozen=True)
class Replacement:
    path: Path
    old: str
    new: str
    expected: int
    label: str


REPLACEMENTS = [
    Replacement(LOWER_SRC, "村庄人声字越少", "村庄入声字越少", 1, "方言过渡带入声字"),
    Replacement(FULL_SRC, "古人声清音字", "古入声清音字", 1, "古入声清音字"),
    Replacement(FULL_SRC, "除少数人\n声字变成舒声外，人声自成一类", "除少数入\n声字变成舒声外，入声自成一类", 1, "少数入声字/入声自成一类"),
    Replacement(FULL_SRC, "村庄人声字越少", "村庄入声字越少", 1, "方言过渡带入声字"),
    Replacement(FULL_SRC, "5.人声。分布", "5.入声。分布", 1, "入声分布小节"),
    Replacement(FULL_SRC, "上声、去声、人声。两字组", "上声、去声、入声。两字组", 1, "调类代码说明"),
    Replacement(LOWER_READER, "<tr><td>5</td><td>人声</td><td>13</td><td>急职一出匹黑惜桌接说发岳纳物局食白</td></tr>", "<tr><td>5</td><td>入声</td><td>13</td><td>急职一出匹黑惜桌接说发岳纳物局食白</td></tr>", 1, "reader 声调表"),
    Replacement(FULL_READER, "<tr><td>5</td><td>人声</td><td>13</td><td>急职一出匹黑惜桌接说发岳纳物局食白</td></tr>", "<tr><td>5</td><td>入声</td><td>13</td><td>急职一出匹黑惜桌接说发岳纳物局食白</td></tr>", 1, "reader 声调表"),
]

STANDALONE_TARGETS = [LOWER_SRC, FULL_SRC]
LEGAL_RESIDUES = ["人声、唢呐声", "人声誉"]


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def replace_standalone_rusheng(path: Path) -> dict[str, object]:
    text = read(path)
    lines = text.splitlines()
    hits = [i for i, line in enumerate(lines) if line == "人声"]
    if len(hits) != 2:
        raise RuntimeError(f"{rel(path)} expected two standalone 人声 lines, got {len(hits)}")
    for i in hits:
        lines[i] = "入声"
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return {"path": rel(path), "old": "standalone 人声", "new": "standalone 入声", "fixed": len(hits), "lines": [i + 1 for i in hits]}


def line_hits(path: Path, needles: tuple[str, ...]) -> list[str]:
    hits = []
    for i, line in enumerate(read(path).splitlines(), 1):
        if any(needle in line for needle in needles):
            hits.append(f"{i}: {line.strip()}")
    return hits


def main() -> None:
    results: list[dict[str, object]] = []
    by_path: dict[Path, str] = {}
    for replacement in REPLACEMENTS:
        text = by_path.setdefault(replacement.path, read(replacement.path))
        count = text.count(replacement.old)
        if count != replacement.expected:
            raise RuntimeError(f"{rel(replacement.path)} `{replacement.old}` expected {replacement.expected}, got {count}")
        by_path[replacement.path] = text.replace(replacement.old, replacement.new, replacement.expected)
        results.append({"path": rel(replacement.path), "label": replacement.label, "old": replacement.old, "new": replacement.new, "fixed": count})

    for path, text in by_path.items():
        path.write_text(text, encoding="utf-8")

    for path in STANDALONE_TARGETS:
        results.append(replace_standalone_rusheng(path))

    residue_needles = ("人声", "入声")
    residues = {
        rel(LOWER_SRC): line_hits(LOWER_SRC, residue_needles),
        rel(FULL_SRC): line_hits(FULL_SRC, residue_needles),
        rel(LOWER_READER): line_hits(LOWER_READER, ("<td>人声</td>", "<td>入声</td>", "人声、唢呐声")),
        rel(FULL_READER): line_hits(FULL_READER, ("<td>人声</td>", "<td>入声</td>", "人声、唢呐声")),
    }

    lines = [
        "# 入声残留补修 batch392",
        "",
        f"- 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "- 范围：下册方言章节源稿、全书正文汇总、当前下册 reader、当前全书 reader。",
        "- 原则：只修方言术语 `入声` 被 OCR 为 `人声` 的完整语境；保留戏曲 `人声、唢呐声` 等合法词。",
        "- 图片处理：未打开、展示或嵌入图片。",
        "",
        "## 修复明细",
    ]
    for item in results:
        lines.append(f"- `{item['path']}`：{item.get('label', item['old'])}，{item['fixed']} 处。")

    lines.extend(["", "## 复扫摘录"])
    for path, hits in residues.items():
        lines.append(f"### {path}")
        if not hits:
            lines.append("- 无。")
        else:
            for hit in hits:
                mark = "；合法保留" if any(term in hit for term in LEGAL_RESIDUES) else ""
                lines.append(f"- {hit}{mark}")

    report = "\n".join(lines) + "\n"
    REPORT.write_text(report, encoding="utf-8")
    REPORT_JSON.write_text(
        json.dumps({"time": datetime.now().strftime("%Y-%m-%d %H:%M"), "results": results, "residues": residues}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    PROGRESS.write_text(report, encoding="utf-8")

    total = sum(int(item["fixed"]) for item in results)
    block = f"""{MARKER}

- 补修方言章节 `入声` 术语被 OCR 为 `人声` 的残留 {total} 处，覆盖概述、入声分布、声调表、连读变调说明，以及当前下册/全书 reader 声调表。
- 保留戏曲段落 `人声、唢呐声` 与其它非方言术语合法命中；未作 `人 -> 入` 全局替换；未处理 OCR 源文件、backup、obsolete、历史交付包；未打开、展示或嵌入图片。
- 报告：`output/reports/verified_rusheng_batch392_20260708.md`；进度：`output/reports/progress/20260708_入声残留补修第三百九十二批.md`。
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
