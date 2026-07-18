# -*- coding: utf-8 -*-
"""Repair remaining verified 人选/入选 residual phrases."""

from __future__ import annotations

import json
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "output" / "reports" / "verified_rxuan_batch377_20260708.md"
REPORT_JSON = ROOT / "output" / "reports" / "verified_rxuan_batch377_20260708.json"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260708_剩余入选残留补修第三百七十七批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"
MARKER = "## 2026-07-08 剩余入选残留补修第三百七十七批"

LOWER = ROOT / "workbench" / "body_chapters" / "第五十二卷至第六十卷及附录（下part02）.md"
MIDDLE = ROOT / "workbench" / "body_chapters" / "第十七卷至第二十九卷（中part01）.md"
SUMMARY = ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md"
PATHS = [LOWER, MIDDLE, SUMMARY]

EVIDENCE_FILES = [ROOT / "output" / "final_reader" / "连云港市志_全书.html"]
EVIDENCE_TERMS = {
    "output/final_reader/连云港市志_全书.html": [
        "张理的《渔归》入选参展",
        "张理的《劈山建海港》入选参展",
        "都入选江苏省美术展览",
        "10名老人入选",
        "王振东入选江苏公安篮球队",
        "入选江苏银行系统篮球代表队",
        "分别入选省商业系统和全国盐业队",
        "入选江苏省首届民间美术博览会",
    ]
}

PHRASES = [
    ("美术", "张理的《渔归》人选参展", "张理的《渔归》入选参展"),
    ("美术", "张理的《劈山建海港》人选参展", "张理的《劈山建海港》入选参展"),
    ("雕塑", "都人选江苏省美术\n展览", "都入选江苏省美术\n展览"),
    ("老年体育", "10名老人人选", "10名老人入选"),
    ("篮球", "陈爱民王振东人选江苏公安篮球队", "陈爱民王振东入选江苏公安篮球队"),
    ("篮球", "周长仁）人选江苏银行系统篮球", "周长仁）入选江苏银行系统篮球"),
    ("足球", "沈文睿、陈猛醒还分别人选省商业系统和全国盐业队", "沈文睿、陈猛醒还分别入选省商业系统和全国盐业队"),
    ("民间美术", "人选江苏省首届民间美术博览会", "入选江苏省首届民间美术博览会"),
]

@dataclass(frozen=True)
class Replacement:
    label: str
    path: Path
    old: str
    new: str

REPLACEMENTS = [Replacement(label, path, old, new) for path in PATHS for label, old, new in PHRASES]
OLD_TERMS = [old for _, old, _ in PHRASES]
NEW_TERMS = [new for _, _, new in PHRASES]


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def line_hits(path: Path, needle: str) -> list[int]:
    return [i for i, line in enumerate(read(path).splitlines(), 1) if needle in line]


def apply_replacements() -> list[dict[str, object]]:
    results = []
    for item in REPLACEMENTS:
        text = read(item.path)
        count = text.count(item.old)
        if count:
            item.path.write_text(text.replace(item.old, item.new), encoding="utf-8")
        after = read(item.path)
        results.append({"label": item.label, "path": rel(item.path), "old": item.old, "new": item.new, "old_count": count, "new_count_after": after.count(item.new)})
    return results


def collect_evidence() -> dict[str, dict[str, list[int]]]:
    return {rel(path): {term: line_hits(path, term) for term in EVIDENCE_TERMS[rel(path)]} for path in EVIDENCE_FILES}


def collect_counts(paths: list[Path], terms: list[str]) -> dict[str, dict[str, int]]:
    counts = {}
    for path in paths:
        text = read(path)
        hits = {term: text.count(term) for term in terms if text.count(term)}
        if hits:
            counts[rel(path)] = hits
    return counts


def render(results, evidence, old_counts, new_counts) -> str:
    total = sum(int(item["old_count"]) for item in results)
    by_label = defaultdict(int)
    for item in results:
        by_label[item["label"]] += int(item["old_count"])
    lines = [
        "# 剩余入选残留补修 batch377",
        "",
        f"- 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"- 修复总数：{total}",
        "- 范围：现行正文源稿与全书正文汇总中可由正式 reader 对证的剩余 `人选 -> 入选` 完整短语。",
        "- 原则：只修艺术、体育、获展语境；保留政治人事语境中的合法 `人选`。",
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


def upsert_memory(total: int, old_counts: dict[str, dict[str, int]]) -> None:
    summary_old = old_counts.get("workbench/body_chapters/连云港市志_全书_正文汇总.md", {})
    block = f"""{MARKER}

- 依据正式 reader 对证，补修当前源稿和全书汇总中剩余艺术、体育、获展语境 `人选 -> 入选` 完整短语，共 {total} 处。
- 代表修复：`张理的《渔归》人选参展 -> 张理的《渔归》入选参展`、`都人选江苏省美术展览 -> 都入选江苏省美术展览`、`10名老人人选 -> 10名老人入选`、`王振东人选江苏公安篮球队 -> 王振东入选江苏公安篮球队`、`人选江苏省首届民间美术博览会 -> 入选江苏省首届民间美术博览会`。
- 本批后全书正文汇总旧词检查剩余：`张理的《渔归》人选参展` {summary_old.get('张理的《渔归》人选参展', 0)}，`10名老人人选` {summary_old.get('10名老人人选', 0)}，`人选江苏省首届民间美术博览会` {summary_old.get('人选江苏省首届民间美术博览会', 0)}。
- 未处理 OCR 源文件、backup、obsolete、历史交付包；未作 `人 -> 入` 全局替换；合法 `代表人选`、`副市长人选` 等继续保留；未打开、展示或嵌入图片。
- 报告：`output/reports/verified_rxuan_batch377_20260708.md`；进度：`output/reports/progress/20260708_剩余入选残留补修第三百七十七批.md`。
"""
    old = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    start = old.find(MARKER)
    if start < 0:
        MEMORY.write_text(old.rstrip() + "\n\n" + block.strip() + "\n", encoding="utf-8")
        return
    next_start = old.find("\n## ", start + 1)
    MEMORY.write_text(old[:start].rstrip() + "\n\n" + block.strip() + ("\n" if next_start < 0 else old[next_start:]), encoding="utf-8")


def main() -> None:
    results = apply_replacements()
    evidence = collect_evidence()
    old_counts = collect_counts(PATHS, OLD_TERMS)
    new_counts = collect_counts(PATHS, NEW_TERMS)
    total = sum(int(item["old_count"]) for item in results)
    report = render(results, evidence, old_counts, new_counts)
    data = {"time": datetime.now().strftime("%Y-%m-%d %H:%M"), "total": total, "results": results, "evidence": evidence, "old_counts": old_counts, "new_counts": new_counts}
    REPORT_JSON.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    REPORT.write_text(report, encoding="utf-8")
    PROGRESS.write_text(report, encoding="utf-8")
    upsert_memory(total, old_counts)
    print(f"total={total}")
    print(json.dumps(old_counts, ensure_ascii=False, indent=2))
    print(f"report={REPORT}")


if __name__ == "__main__":
    main()
