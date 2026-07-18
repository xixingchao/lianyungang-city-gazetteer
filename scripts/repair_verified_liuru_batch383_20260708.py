# -*- coding: utf-8 -*-
"""Repair verified 流人/流入 OCR residues in current sources."""

from __future__ import annotations

import json
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "output" / "reports" / "verified_liuru_batch383_20260708.md"
REPORT_JSON = ROOT / "output" / "reports" / "verified_liuru_batch383_20260708.json"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260708_流入残留补修第三百八十三批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"
READER = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
MARKER = "## 2026-07-08 流入残留补修第三百八十三批"

@dataclass(frozen=True)
class Phrase:
    label: str
    old: str
    new: str

PHRASES = [
    Phrase("海岸变迁", "北流人渤海", "北流入渤海"),
    Phrase("海岸变迁", "水流人黄海", "水流入黄海"),
    Phrase("盐业工艺", "流人卤池", "流入卤池"),
    Phrase("盐业工艺", "汛潮流人圩河", "汛潮流入圩河"),
    Phrase("盐业工艺", "流人盐浆", "流入盐浆"),
    Phrase("河流航运", "东流人海", "东流入海"),
    Phrase("景区水系", "流人山下农田", "流入山下农田"),
    Phrase("外贸货源", "大量流人", "大量流入"),
    Phrase("戏曲传播", "京剧的流人", "京剧的流入"),
    Phrase("戏曲传播", "南下流人海州", "南下流入海州"),
    Phrase("戏曲传播", "吕剧流人后", "吕剧流入后"),
    Phrase("劳动力管理", "盲目流人城市", "盲目流入城市"),
]

PATHS = [
    ROOT / "workbench" / "body_chapters" / "第三十卷至第四十二卷（中part02）.md",
    ROOT / "workbench" / "body_chapters" / "第四十三卷至第五十一卷（下part01）.md",
    ROOT / "workbench" / "body_chapters" / "第五十二卷至第六十卷及附录（下part02）.md",
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
]

EVIDENCE_TERMS = [phrase.new for phrase in PHRASES]
LEGAL_READER_TERMS = ["外流人口", "内外流人员", "市内流人员", "外流人员"]


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def line_hits(path: Path, needle: str) -> list[int]:
    return [i for i, line in enumerate(read(path).splitlines(), 1) if needle in line]


def apply_fixes() -> list[dict[str, object]]:
    results = []
    for path in PATHS:
        text = read(path)
        changed = text
        for phrase in PHRASES:
            count = changed.count(phrase.old)
            if count:
                changed = changed.replace(phrase.old, phrase.new)
            results.append(
                {
                    "label": phrase.label,
                    "path": rel(path),
                    "old": phrase.old,
                    "new": phrase.new,
                    "old_count": count,
                }
            )
        if changed != text:
            path.write_text(changed, encoding="utf-8")
    for item in results:
        path = ROOT / item["path"]
        after = read(path)
        item["old_count_after"] = after.count(str(item["old"]))
        item["new_count_after"] = after.count(str(item["new"]))
    return results


def remaining_liuren() -> dict[str, list[str]]:
    paths = [ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md", READER]
    out: dict[str, list[str]] = {}
    for path in paths:
        snippets = []
        for i, line in enumerate(read(path).splitlines(), 1):
            if "流人" in line:
                idx = line.find("流人")
                snippets.append(f"{i}: {line[max(0, idx - 45):idx + 95]}")
        out[rel(path)] = snippets
    return out


def render(results: list[dict[str, object]], evidence: dict[str, list[int]], residues: dict[str, list[str]]) -> str:
    total = sum(int(item["old_count"]) for item in results)
    by_label = defaultdict(int)
    for item in results:
        by_label[str(item["label"])] += int(item["old_count"])
    lines = [
        "# 流入残留补修 batch383",
        "",
        f"- 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"- 修复总数：{total}",
        "- 范围：现行分册源稿与全书汇总中由正式 reader 对证的 `流人 -> 流入` 完整短语。",
        "- 原则：只修水流、货物流向、剧种流布、劳动力流动等明确语境；不处理 backup、obsolete、历史交付包。",
        "- 图片处理：未打开、展示或嵌入图片。",
        "",
        "## 分项统计",
    ]
    for label in sorted(by_label):
        lines.append(f"- {label}：{by_label[label]} 处。")
    lines.extend(["", "## 修复明细"])
    for item in results:
        if int(item["old_count"]):
            lines.append(f"- `{item['path']}`：`{item['old']}` -> `{item['new']}`，{item['old_count']} 处。")
    lines.extend(["", "## reader 证据"])
    for term, hits in evidence.items():
        compact = "，".join(str(i) for i in hits) or "未命中"
        lines.append(f"- `output/final_reader/连云港市志_全书.html` 行 {compact}：`{term}`")
    lines.extend(["", "## 剩余 `流人` 片段"])
    for path, snippets in residues.items():
        lines.append(f"### {path}")
        if not snippets:
            lines.append("- 无。")
            continue
        for snippet in snippets:
            legal = "；未纳入本批" if any(term in snippet for term in LEGAL_READER_TERMS) else ""
            lines.append(f"- {snippet}{legal}")
    return "\n".join(lines) + "\n"


def upsert_memory(total: int) -> None:
    block = f"""{MARKER}

- 依据正式 reader 对证，补修 `流人 -> 流入` 完整短语 {total} 处，覆盖海岸变迁、盐业工艺、河流航运、景区水系、外贸货源、戏曲传播、劳动力管理等明确语境。
- 代表修复：`北流人渤海 -> 北流入渤海`、`流人卤池 -> 流入卤池`、`东流人海 -> 东流入海`、`京剧的流人 -> 京剧的流入`、`盲目流人城市 -> 盲目流入城市`。
- 未处理 OCR 源文件、backup、obsolete、历史交付包；未打开、展示或嵌入图片；未扩大为 `人 -> 入` 全局替换。
- 报告：`output/reports/verified_liuru_batch383_20260708.md`；进度：`output/reports/progress/20260708_流入残留补修第三百八十三批.md`。
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
    residues = remaining_liuren()
    total = sum(int(item["old_count"]) for item in results)
    report = render(results, evidence, residues)
    data = {
        "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "total": total,
        "results": results,
        "evidence": evidence,
        "remaining_liuren": residues,
    }
    REPORT.write_text(report, encoding="utf-8")
    REPORT_JSON.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    PROGRESS.write_text(report, encoding="utf-8")
    upsert_memory(total)
    print(f"total={total}")
    print(f"report={REPORT}")


if __name__ == "__main__":
    main()
