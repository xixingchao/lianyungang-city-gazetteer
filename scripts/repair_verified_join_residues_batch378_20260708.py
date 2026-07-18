# -*- coding: utf-8 -*-
"""Repair verified 加人/加入 residual phrases."""

from __future__ import annotations

import json
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "output" / "reports" / "verified_join_residues_batch378_20260708.md"
REPORT_JSON = ROOT / "output" / "reports" / "verified_join_residues_batch378_20260708.json"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260708_加入残留补修第三百七十八批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"
MARKER = "## 2026-07-08 加入残留补修第三百七十八批"

PATHS = [
    ROOT / "workbench" / "body_chapters" / "上" / "第十卷至第十六卷（part03）.md",
    ROOT / "workbench" / "body_chapters" / "第三十卷至第四十二卷（中part02）.md",
    ROOT / "workbench" / "body_chapters" / "第十七卷至第二十九卷（中part01）.md",
    ROOT / "workbench" / "body_chapters" / "第四十三卷至第五十一卷（下part01）.md",
    ROOT / "workbench" / "body_chapters" / "第五十二卷至第六十卷及附录（下part02）.md",
    ROOT / "workbench" / "body_chapters" / "连云港市志_上册_正文汇总.md",
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
]

EVIDENCE_FILES = [
    ROOT / "output" / "final_reader" / "连云港市志_全书.html",
    ROOT / "workbench" / "body_chapters" / "上" / "第十卷至第十六卷（part03）.md",
    ROOT / "workbench" / "ocr" / "paddle_ocr" / "merged" / "连云港市志_上册_PaddleOCR汇总.md",
]
EVIDENCE_TERMS = {
    "output/final_reader/连云港市志_全书.html": [
        "亚硒酸钠水式加入",
        "加入新浦针织生产合作社",
        "加入公私合营新浦五金车料零售商店",
        "人口加入到初级社、高级社",
        "加入粮谷组合",
        "加入到复合肥生产企业的行列",
        "加入所在国的国籍",
        "加入中国共产党",
    ],
    "workbench/body_chapters/上/第十卷至第十六卷（part03）.md": [
        "亚硒酸钠水式加入",
        "加入新浦针织生产合作社",
    ],
    "workbench/ocr/paddle_ocr/merged/连云港市志_上册_PaddleOCR汇总.md": [
        "亚硒酸钠水式加入",
        "加入新浦针织生产合作社",
    ],
}

PHRASES = [
    ("工艺", "亚硒酸钠水式加人", "亚硒酸钠水式加入"),
    ("合作社", "加人新浦针织生产合作社", "加入新浦针织生产合作社"),
    ("商业", "加人公私合营新浦五金车料零售商店", "加入公私合营新浦五金车料零售商店"),
    ("粮食", "人口加人到初级社", "人口加入到初级社"),
    ("粮食", "加人粮谷组合", "加入粮谷组合"),
    ("化工", "加人到复合肥生产企业", "加入到复合肥生产企业"),
    ("侨务", "加人所在\n国的国籍", "加入所在\n国的国籍"),
    ("入党", "加人中\n国共产党", "加入中\n国共产党"),
    ("入党", "加人\n中国共产党", "加入\n中国共产党"),
    ("入党", "加人\n共产党", "加入\n共产党"),
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
        "# 加入残留补修 batch378",
        "",
        f"- 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"- 修复总数：{total}",
        "- 范围：现行正文源稿与全书正文汇总中已由正式 reader、现行上册源稿或 PaddleOCR 汇总证实的 `加人 -> 加入` 完整短语。",
        "- 原则：只修加入组织、入党、工艺加入等完整语境；保留 `参加人数`、`增加人员`、`参军人员` 等合法词。",
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

- 依据正式 reader、现行上册源稿与 PaddleOCR 汇总证据，补修加入组织、入党、工艺加入语境中的 `加人 -> 加入` 完整短语，共 {total} 处。
- 代表修复：`亚硒酸钠水式加人 -> 亚硒酸钠水式加入`、`加人新浦针织生产合作社 -> 加入新浦针织生产合作社`、`人口加人到初级社 -> 人口加入到初级社`、`加人粮谷组合 -> 加入粮谷组合`、`加人中国共产党 -> 加入中国共产党`。
- 本批后全书正文汇总旧词检查剩余：`亚硒酸钠水式加人` {summary_old.get('亚硒酸钠水式加人', 0)}，`加人新浦针织生产合作社` {summary_old.get('加人新浦针织生产合作社', 0)}，`人口加人到初级社` {summary_old.get('人口加人到初级社', 0)}，`加人中\\n国共产党` {summary_old.get('加人中\\n国共产党', 0)}。
- 未处理 OCR 源文件、backup、obsolete、历史交付包；未作 `人 -> 入` 全局替换；合法 `参加人数`、`增加人员`、`参军人员` 等继续保留；未打开、展示或嵌入图片。
- 报告：`output/reports/verified_join_residues_batch378_20260708.md`；进度：`output/reports/progress/20260708_加入残留补修第三百七十八批.md`。
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
