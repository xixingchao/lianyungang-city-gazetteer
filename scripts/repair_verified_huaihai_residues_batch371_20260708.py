# -*- coding: utf-8 -*-
"""Repair PaddleOCR-proven 准海/淮海 residual phrases."""

from __future__ import annotations

import json
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "output" / "reports" / "verified_huaihai_residues_batch371_20260708.md"
REPORT_JSON = ROOT / "output" / "reports" / "verified_huaihai_residues_batch371_20260708.json"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260708_可证准海淮海残留补修第三百七十一批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"
MARKER = "## 2026-07-08 可证准海淮海残留补修第三百七十一批"

MID = ROOT / "workbench" / "body_chapters" / "第三十卷至第四十二卷（中part02）.md"
LOW1 = ROOT / "workbench" / "body_chapters" / "第四十三卷至第五十一卷（下part01）.md"
LOW2 = ROOT / "workbench" / "body_chapters" / "第五十二卷至第六十卷及附录（下part02）.md"
SUMMARY = ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md"

EVIDENCE_FILES = [
    ROOT / "workbench" / "ocr" / "paddle_ocr" / "中" / "part02" / "page_0222.txt",
    ROOT / "workbench" / "ocr" / "paddle_ocr" / "中" / "part02" / "page_0330.txt",
    ROOT / "workbench" / "ocr" / "paddle_ocr" / "中" / "part02" / "page_0406.txt",
    ROOT / "workbench" / "ocr" / "paddle_ocr" / "中" / "part02" / "page_0408.txt",
    ROOT / "workbench" / "ocr" / "paddle_ocr" / "中" / "part02" / "page_0409.txt",
    ROOT / "workbench" / "ocr" / "paddle_ocr" / "中" / "part02" / "page_0500.txt",
    ROOT / "workbench" / "ocr" / "paddle_ocr" / "下" / "part01" / "page_0163.txt",
    ROOT / "workbench" / "ocr" / "paddle_ocr" / "下" / "part01" / "page_0174.txt",
    ROOT / "workbench" / "ocr" / "paddle_ocr" / "下" / "part02" / "page_0020.txt",
    ROOT / "workbench" / "ocr" / "paddle_ocr" / "下" / "part02" / "page_0157.txt",
    ROOT / "workbench" / "ocr" / "paddle_ocr" / "下" / "part02" / "page_0348.txt",
    ROOT / "workbench" / "ocr" / "paddle_ocr" / "下" / "part02" / "page_0350.txt",
    ROOT / "workbench" / "ocr" / "paddle_ocr" / "下" / "part02" / "page_0374.txt",
]

EVIDENCE_TERMS = {
    "workbench/ocr/paddle_ocr/中/part02/page_0222.txt": ["中共淮海地委、行署、军分区"],
    "workbench/ocr/paddle_ocr/中/part02/page_0330.txt": ["《淮海报》载"],
    "workbench/ocr/paddle_ocr/中/part02/page_0406.txt": ["淮海区党委"],
    "workbench/ocr/paddle_ocr/中/part02/page_0408.txt": ["淮海、滨海两区"],
    "workbench/ocr/paddle_ocr/中/part02/page_0409.txt": ["开辟淮海抗日民主根据"],
    "workbench/ocr/paddle_ocr/中/part02/page_0500.txt": ["淮海区第二届参议会"],
    "workbench/ocr/paddle_ocr/下/part01/page_0163.txt": ["进犯淮海地区"],
    "workbench/ocr/paddle_ocr/下/part01/page_0174.txt": ["淮海军分区一支队"],
    "workbench/ocr/paddle_ocr/下/part02/page_0020.txt": ["《淮海浪士》"],
    "workbench/ocr/paddle_ocr/下/part02/page_0157.txt": ["淮海之窗", "淮海经济区"],
    "workbench/ocr/paddle_ocr/下/part02/page_0348.txt": ["参加淮海按试"],
    "workbench/ocr/paddle_ocr/下/part02/page_0350.txt": ["借淮海水师巡逻船"],
    "workbench/ocr/paddle_ocr/下/part02/page_0374.txt": ["入淮海干校", "任淮海第三中学"],
}


@dataclass(frozen=True)
class Replacement:
    label: str
    path: Path
    old: str
    new: str


PHRASES = [
    ("淮海地委", "中共准海地委", "中共淮海地委"),
    ("淮海报", "《准海报》", "《淮海报》"),
    ("淮海滨海", "准海、滨海两区", "淮海、滨海两区"),
    ("淮海根据地", "开辟准海抗日民主根据", "开辟淮海抗日民主根据"),
    ("淮海区党委", "准海区党委", "淮海区党委"),
    ("淮海参议会", "准海区第二届参议会", "淮海区第二届参议会"),
    ("淮海浪士", "《准海浪士》", "《淮海浪士》"),
    ("淮海之窗", "准海之窗", "淮海之窗"),
    ("淮海经济区", "准海经济区", "淮海经济区"),
    ("淮海按试", "准海按试", "淮海按试"),
    ("淮海水师", "准海水师巡逻船", "淮海水师巡逻船"),
    ("淮海干校", "入准海干校", "入淮海干校"),
    ("淮海第三中学", "任准海第三中学", "任淮海第三中学"),
    ("淮海军分区", "准海军分区一支队", "淮海军分区一支队"),
    ("淮海地区", "进犯准海地区", "进犯淮海地区"),
]

REPLACEMENTS = [Replacement(label, path, old, new) for path in [MID, LOW1, LOW2, SUMMARY] for label, old, new in PHRASES]
OLD_TERMS = [old for _, old, _ in PHRASES]
NEW_TERMS = [new for _, _, new in PHRASES]


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def line_hits(path: Path, needle: str) -> list[int]:
    return [i for i, line in enumerate(read(path).splitlines(), 1) if needle in line]


def apply_replacements() -> list[dict[str, object]]:
    results: list[dict[str, object]] = []
    for item in REPLACEMENTS:
        text = read(item.path)
        count = text.count(item.old)
        if count:
            item.path.write_text(text.replace(item.old, item.new), encoding="utf-8")
        results.append({
            "label": item.label,
            "path": rel(item.path),
            "old": item.old,
            "new": item.new,
            "old_count": count,
            "new_count_after": read(item.path).count(item.new),
        })
    return results


def collect_evidence() -> dict[str, dict[str, list[int]]]:
    evidence: dict[str, dict[str, list[int]]] = {}
    for path in EVIDENCE_FILES:
        key = rel(path)
        evidence[key] = {}
        for term in EVIDENCE_TERMS.get(key, []):
            evidence[key][term] = line_hits(path, term)
    return evidence


def collect_counts(paths: list[Path], terms: list[str]) -> dict[str, dict[str, int]]:
    counts: dict[str, dict[str, int]] = {}
    for path in paths:
        text = read(path)
        hits = {term: text.count(term) for term in terms if text.count(term)}
        if hits:
            counts[rel(path)] = hits
    return counts


def render(results: list[dict[str, object]], evidence: dict[str, dict[str, list[int]]], old_counts: dict[str, dict[str, int]], new_counts: dict[str, dict[str, int]]) -> str:
    total = sum(int(item["old_count"]) for item in results)
    by_label: dict[str, int] = defaultdict(int)
    for item in results:
        by_label[str(item["label"])] += int(item["old_count"])

    lines = [
        "# 可证准海淮海残留补修 batch371",
        "",
        f"- 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"- 修复总数：{total}",
        "- 范围：中册财政/党政段、下册军事与文化人物段、全书正文汇总中已由 PaddleOCR 证实的完整短语。",
        "- 原则：只修完整短语；不作 `准 -> 淮` 全局替换，保留未证的 `准海线` 等专名。",
        "- 图片处理：未打开、展示或嵌入图片。",
        "",
        "## 分项统计",
    ]
    for label in sorted(by_label):
        lines.append(f"- {label}：{by_label[label]} 处。")

    lines.extend(["", "## 证据位置"])
    for path, terms in evidence.items():
        lines.append(f"- `{path}`")
        for term, hits in terms.items():
            compact = "，".join(str(i) for i in hits) or "未命中"
            lines.append(f"  - 行 {compact}：`{term}`")

    lines.extend(["", "## 替换明细"])
    for item in results:
        if int(item["old_count"]):
            lines.append(f"- `{item['path']}`：{item['label']}，替换 {item['old_count']} 处；`{item['old']}` -> `{item['new']}`。")

    lines.extend(["", "## 旧词残留检查"])
    if old_counts:
        for path, hits in old_counts.items():
            compact = "，".join(f"`{term}` {count}" for term, count in hits.items())
            lines.append(f"- `{path}`：{compact}")
    else:
        lines.append("- 检查范围未见本批旧词残留。")

    lines.extend(["", "## 新词命中"])
    for path, hits in new_counts.items():
        compact = "，".join(f"`{term}` {count}" for term, count in hits.items())
        lines.append(f"- `{path}`：{compact}")
    return "\n".join(lines) + "\n"


def upsert_memory(results: list[dict[str, object]], old_counts: dict[str, dict[str, int]]) -> None:
    total = sum(int(item["old_count"]) for item in results)
    summary_old = old_counts.get("workbench/body_chapters/连云港市志_全书_正文汇总.md", {})
    block = f"""{MARKER}

- 依据中册 part02/page_0222、0330、0406、0408、0409、0500，以及下册 part01/page_0163、0174、下册 part02/page_0020、0157、0348、0350、0374 页级 PaddleOCR 成句证据，补修 `准海 -> 淮海` 可证完整短语，共 {total} 处。
- 代表修复：`中共准海地委 -> 中共淮海地委`、`《准海报》 -> 《淮海报》`、`准海、滨海两区 -> 淮海、滨海两区`、`开辟准海抗日民主根据 -> 开辟淮海抗日民主根据`、`准海区党委/参议会 -> 淮海区党委/参议会`、`《准海浪士》 -> 《淮海浪士》`、`准海之窗/准海经济区 -> 淮海之窗/淮海经济区`、`准海按试/水师/干校/第三中学/军分区/地区 -> 淮海...`。
- 本批后全书正文汇总旧词检查剩余：`中共准海地委` {summary_old.get('中共准海地委', 0)}，`《准海报》` {summary_old.get('《准海报》', 0)}，`准海之窗` {summary_old.get('准海之窗', 0)}，`准海经济区` {summary_old.get('准海经济区', 0)}，`准海按试` {summary_old.get('准海按试', 0)}，`准海水师巡逻船` {summary_old.get('准海水师巡逻船', 0)}。
- 未处理 OCR 源文件、backup、obsolete、历史交付包；未作 `准 -> 淮` 全局替换，未证的 `准海线`、伪政权税务表述等继续保留待核；未打开、展示或嵌入图片。
- 报告：`output/reports/verified_huaihai_residues_batch371_20260708.md`；进度：`output/reports/progress/20260708_可证准海淮海残留补修第三百七十一批.md`。
"""
    old = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    start = old.find(MARKER)
    if start < 0:
        MEMORY.write_text(old.rstrip() + "\n\n" + block.strip() + "\n", encoding="utf-8")
        return
    next_start = old.find("\n## ", start + 1)
    new_text = old[:start].rstrip() + "\n\n" + block.strip() + ("\n" if next_start < 0 else old[next_start:])
    MEMORY.write_text(new_text, encoding="utf-8")


def main() -> None:
    results = apply_replacements()
    touched = [MID, LOW1, LOW2, SUMMARY]
    evidence = collect_evidence()
    old_counts = collect_counts(touched, OLD_TERMS)
    new_counts = collect_counts(touched, NEW_TERMS)
    report = render(results, evidence, old_counts, new_counts)
    data = {
        "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "total": sum(int(item["old_count"]) for item in results),
        "results": results,
        "evidence": evidence,
        "old_counts": old_counts,
        "new_counts": new_counts,
    }
    REPORT_JSON.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    REPORT.write_text(report, encoding="utf-8")
    PROGRESS.write_text(report, encoding="utf-8")
    upsert_memory(results, old_counts)
    print(f"total={data['total']}")
    print(json.dumps(old_counts, ensure_ascii=False, indent=2))
    print(f"report={REPORT}")


if __name__ == "__main__":
    main()
