# -*- coding: utf-8 -*-
"""Repair PaddleOCR-proven 人海/入海 and related 入海州 residues."""

from __future__ import annotations

import json
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "output" / "reports" / "verified_renhai_residues_batch374_20260708.md"
REPORT_JSON = ROOT / "output" / "reports" / "verified_renhai_residues_batch374_20260708.json"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260708_可证人海入海残留补修第三百七十四批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"
MARKER = "## 2026-07-08 可证人海入海残留补修第三百七十四批"

PATHS = [
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
    ROOT / "workbench" / "body_chapters" / "第四十三卷至第五十一卷（下part01）.md",
    ROOT / "workbench" / "body_chapters" / "第五十二卷至第六十卷及附录（下part02）.md",
    ROOT / "workbench" / "body_chapters" / "第十七卷至第二十九卷（中part01）.md",
]

EVIDENCE_FILES = [
    ROOT / "workbench" / "ocr" / "paddle_ocr" / "上" / "part01" / "page_0146.txt",
    ROOT / "workbench" / "ocr" / "paddle_ocr" / "上" / "part01" / "page_0167.txt",
    ROOT / "workbench" / "ocr" / "paddle_ocr" / "上" / "part01" / "page_0168.txt",
    ROOT / "workbench" / "ocr" / "paddle_ocr" / "上" / "part01" / "page_0169.txt",
    ROOT / "workbench" / "ocr" / "paddle_ocr" / "上" / "part01" / "page_0170.txt",
    ROOT / "workbench" / "ocr" / "paddle_ocr" / "上" / "part01" / "page_0190.txt",
    ROOT / "workbench" / "ocr" / "paddle_ocr" / "上" / "part01" / "page_0208.txt",
    ROOT / "workbench" / "ocr" / "paddle_ocr" / "上" / "part01" / "page_0245.txt",
    ROOT / "workbench" / "ocr" / "paddle_ocr" / "上" / "part01" / "page_0273.txt",
    ROOT / "workbench" / "ocr" / "paddle_ocr" / "上" / "part02" / "page_0098.txt",
    ROOT / "workbench" / "ocr" / "paddle_ocr" / "上" / "part02" / "page_0267.txt",
    ROOT / "workbench" / "ocr" / "paddle_ocr" / "上" / "part02" / "page_0268.txt",
    ROOT / "workbench" / "ocr" / "paddle_ocr" / "上" / "part02" / "page_0288.txt",
    ROOT / "workbench" / "ocr" / "paddle_ocr" / "上" / "part02" / "page_0293.txt",
    ROOT / "workbench" / "ocr" / "paddle_ocr" / "上" / "part02" / "page_0126.txt",
    ROOT / "workbench" / "ocr" / "paddle_ocr" / "上" / "part03" / "page_0088.txt",
    ROOT / "workbench" / "ocr" / "paddle_ocr" / "中" / "part01" / "page_0493.txt",
    ROOT / "workbench" / "ocr" / "paddle_ocr" / "下" / "part01" / "page_0161.txt",
    ROOT / "workbench" / "ocr" / "paddle_ocr" / "下" / "part01" / "page_0169.txt",
    ROOT / "workbench" / "ocr" / "paddle_ocr" / "下" / "part01" / "page_0172.txt",
    ROOT / "workbench" / "ocr" / "paddle_ocr" / "下" / "part01" / "page_0374.txt",
    ROOT / "workbench" / "ocr" / "paddle_ocr" / "下" / "part02" / "page_0351.txt",
]

EVIDENCE_TERMS = {
    "workbench/ocr/paddle_ocr/上/part01/page_0146.txt": ["经苏北入海"],
    "workbench/ocr/paddle_ocr/上/part01/page_0167.txt": ["争道入海", "新开掘入海河道"],
    "workbench/ocr/paddle_ocr/上/part01/page_0168.txt": ["荻水口入海", "柳树村东北入海", "潮河口入海", "朱蓬口入海", "下口入海"],
    "workbench/ocr/paddle_ocr/上/part01/page_0169.txt": ["子口入海"],
    "workbench/ocr/paddle_ocr/上/part01/page_0170.txt": ["洋桥镇入海", "燕尾闸入海"],
    "workbench/ocr/paddle_ocr/上/part01/page_0190.txt": ["排泄入海"],
    "workbench/ocr/paddle_ocr/上/part01/page_0208.txt": ["向东入海"],
    "workbench/ocr/paddle_ocr/上/part01/page_0245.txt": ["穿境入海"],
    "workbench/ocr/paddle_ocr/上/part01/page_0273.txt": ["子口入海"],
    "workbench/ocr/paddle_ocr/上/part02/page_0098.txt": ["废水排入海域"],
    "workbench/ocr/paddle_ocr/上/part02/page_0267.txt": ["下泄入海"],
    "workbench/ocr/paddle_ocr/上/part02/page_0268.txt": ["海州入海"],
    "workbench/ocr/paddle_ocr/上/part02/page_0288.txt": ["海州入海"],
    "workbench/ocr/paddle_ocr/上/part02/page_0293.txt": ["泄水入海干河"],
    "workbench/ocr/paddle_ocr/上/part02/page_0126.txt": ["污水入海量"],
    "workbench/ocr/paddle_ocr/上/part03/page_0088.txt": ["进入海州湾"],
    "workbench/ocr/paddle_ocr/中/part01/page_0493.txt": ["污水入海量"],
    "workbench/ocr/paddle_ocr/下/part01/page_0161.txt": ["攻入海州"],
    "workbench/ocr/paddle_ocr/下/part01/page_0169.txt": ["攻入海州"],
    "workbench/ocr/paddle_ocr/下/part01/page_0172.txt": ["编入海赣独立团"],
    "workbench/ocr/paddle_ocr/下/part01/page_0374.txt": ["并入海州十一中学"],
    "workbench/ocr/paddle_ocr/下/part02/page_0351.txt": ["攻入海州"],
}

PHRASES = [
    ("入海", "经苏北人海", "经苏北入海"),
    ("入海", "争道人海", "争道入海"),
    ("入海", "新开掘人海河道", "新开掘入海河道"),
    ("入海", "荻水口人海", "荻水口入海"),
    ("入海", "柳树村东北人海", "柳树村东北入海"),
    ("入海", "潮河口人海", "潮河口入海"),
    ("入海", "朱蓬口人海", "朱蓬口入海"),
    ("入海", "下口人海", "下口入海"),
    ("入海", "三洋港（旧称唐生口）人海", "三洋港（旧称唐生口）入海"),
    ("入海", "子口人海", "子口入海"),
    ("入海", "洋桥镇人海", "洋桥镇入海"),
    ("入海", "燕尾闸人海", "燕尾闸入海"),
    ("入海", "排泄人海", "排泄入海"),
    ("入海", "向东人海", "向东入海"),
    ("入海", "穿境人海", "穿境入海"),
    ("入海", "下泄人海", "下泄入海"),
    ("入海", "海州人海", "海州入海"),
    ("入海", "烧香河口人海", "烧香河口入海"),
    ("入海", "泄水人海干河", "泄水入海干河"),
    ("入海", "废水排人海域", "废水排入海域"),
    ("入海量", "污水人海量", "污水入海量"),
    ("进入海州湾", "进人海州湾", "进入海州湾"),
    ("攻入海州", "攻人海州", "攻入海州"),
    ("编入海赣", "编人海赣独立团", "编入海赣独立团"),
    ("并入海州十一中", "并人海州十一中学", "并入海州十一中学"),
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
        "# 可证人海入海残留补修 batch374",
        "",
        f"- 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"- 修复总数：{total}",
        "- 范围：现行正文源稿与全书正文汇总中已由 PaddleOCR 证实的完整短语。",
        "- 原则：只修完整短语；不作 `人 -> 入` 全局替换，保留未证古文、书名和人物经历残留。",
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


def upsert_memory(results: list[dict[str, object]], old_counts: dict[str, dict[str, int]]) -> None:
    total = sum(int(item["old_count"]) for item in results)
    summary_old = old_counts.get("workbench/body_chapters/连云港市志_全书_正文汇总.md", {})
    block = f"""{MARKER}

- 依据上册 part01/page_0146、0167、0168、0169、0170、0190、0208、0245、0273，上册 part02/page_0098、0126、0267、0268、0288、0293，上册 part03/page_0088，中册 part01/page_0493，下册 part01/page_0161、0169、0172、0374，下册 part02/page_0351 页级 PaddleOCR 成句证据，补修 `人海/进人海州湾/攻人海州/编人海赣/并人海州十一中学` 可证残留，共 {total} 处。
- 代表修复：`经苏北人海 -> 经苏北入海`、`新开掘人海河道 -> 新开掘入海河道`、`荻水口/柳树村东北/潮河口/朱蓬口/下口/子口/洋桥镇/燕尾闸人海 -> ...入海`、`废水排人海域 -> 废水排入海域`、`污水人海量 -> 污水入海量`、`进人海州湾 -> 进入海州湾`、`攻人海州 -> 攻入海州`、`编人海赣独立团 -> 编入海赣独立团`、`并人海州十一中学 -> 并入海州十一中学`。
- 本批后全书正文汇总旧词检查剩余：`经苏北人海` {summary_old.get('经苏北人海', 0)}，`子口人海` {summary_old.get('子口人海', 0)}，`污水人海量` {summary_old.get('污水人海量', 0)}，`进人海州湾` {summary_old.get('进人海州湾', 0)}，`攻人海州` {summary_old.get('攻人海州', 0)}。
- 未处理 OCR 源文件、backup、obsolete、历史交付包；未作危险全局替换，未证古文/书名/人物经历保留待核；未打开、展示或嵌入图片。
- 报告：`output/reports/verified_renhai_residues_batch374_20260708.md`；进度：`output/reports/progress/20260708_可证人海入海残留补修第三百七十四批.md`。
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
