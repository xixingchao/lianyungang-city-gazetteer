# -*- coding: utf-8 -*-
"""Repair three PaddleOCR-proven reader/source residues."""

from __future__ import annotations

import json
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "output" / "reports" / "paddle_proven_residues_batch369_20260708.md"
REPORT_JSON = ROOT / "output" / "reports" / "paddle_proven_residues_batch369_20260708.json"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260708_PaddleOCR可证句段残留补修第三百六十九批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"
MARKER = "## 2026-07-08 PaddleOCR可证句段残留补修第三百六十九批"

EVIDENCE_FILES = [
    ROOT / "workbench" / "ocr" / "paddle_ocr" / "中" / "part02" / "page_0349.txt",
    ROOT / "workbench" / "ocr" / "paddle_ocr" / "下" / "part01" / "page_0016.txt",
    ROOT / "workbench" / "ocr" / "paddle_ocr" / "下" / "part01" / "page_0017.txt",
    ROOT / "workbench" / "ocr" / "paddle_ocr" / "下" / "part01" / "page_0095.txt",
]

SOURCE_MID = ROOT / "workbench" / "body_chapters" / "第三十卷至第四十二卷（中part02）.md"
SOURCE_LOW = ROOT / "workbench" / "body_chapters" / "第四十三卷至第五十一卷（下part01）.md"
SUMMARY = ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md"
READER_ALL = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
READER_MID = ROOT / "output" / "final_reader" / "连云港市志_中册.html"
READER_LOW = ROOT / "output" / "final_reader" / "连云港市志_下册.html"


@dataclass(frozen=True)
class Replacement:
    label: str
    path: Path
    old: str
    new: str


SOURCE_CREDIT_OLD = "农村信用社董新纳入人民银行管理体制"
SOURCE_CREDIT_NEW = "农村信用社重新纳入人民银行管理体制"

SOURCE_CIVIL_OLD = """政部门在拥军优属、推行火葬、生产救灾等方面都落实了一些措施。以上工作对巩固国

<!-- page-anchor: LYG-1988 -->

工作未能正常运转。"""
SOURCE_CIVIL_NEW = """政部门在拥军优属、推行火葬、生产救灾等方面都落实了一些措施。以上工作对巩固国
防、稳定社会、树立良好的社会风尚方面都取得成效。“文化大革命”期间，全市民政部门

<!-- page-anchor: LYG-1988 -->

工作未能正常运转。"""

READER_CIVIL_ALL_OLD = "以上工作对巩固国工作未能正常运转。"
READER_CIVIL_ALL_NEW = "以上工作对巩固国防、稳定社会、树立良好的社会风尚方面都取得成效。“文化大革命”期间，全市民政部门工作未能正常运转。"
READER_CIVIL_LOW_OLD = "<p>政部门在拥军优属、推行火葬、生产救灾等方面都落实了一些措施。以上工作对巩固国</p><p>工作未能正常运转。</p>"
READER_CIVIL_LOW_NEW = "<p>政部门在拥军优属、推行火葬、生产救灾等方面都落实了一些措施。以上工作对巩固国</p><p>防、稳定社会、树立良好的社会风尚方面都取得成效。“文化大革命”期间，全市民政部门</p><p>工作未能正常运转。</p>"

SOURCE_PORT_OLD = """点停泊、船只看管、查岗查船、验滩等制度。1977年，市公安局边防科会同港务监督部门
精神，制订港口管理规则并公布实施。"""
SOURCE_PORT_NEW = """点停泊、船只看管、查岗查船、验滩等制度。1977年，市公安局边防科会同港务监督部门
制订《关于加强港口管理、整顿水上交通秩序的联合通告》，各边防派出所根据《联合通告》
精神，制订港口管理规则并公布实施。"""

READER_PORT_ALL_OLD = "1977年，市公安局边防科会同港务监督部门精神，制订港口管理规则并公布实施。"
READER_PORT_ALL_NEW = "1977年，市公安局边防科会同港务监督部门制订《关于加强港口管理、整顿水上交通秩序的联合通告》，各边防派出所根据《联合通告》精神，制订港口管理规则并公布实施。"
READER_PORT_LOW_OLD = "1977年，市公安局边防科会同港务监督部门</p><p>精神，制订港口管理规则并公布实施。"
READER_PORT_LOW_NEW = "1977年，市公安局边防科会同港务监督部门</p><p>制订《关于加强港口管理、整顿水上交通秩序的联合通告》，各边防派出所根据《联合通告》</p><p>精神，制订港口管理规则并公布实施。"

REPLACEMENTS = [
    Replacement("农村信用社误识", SOURCE_MID, SOURCE_CREDIT_OLD, SOURCE_CREDIT_NEW),
    Replacement("农村信用社误识", SUMMARY, SOURCE_CREDIT_OLD, SOURCE_CREDIT_NEW),
    Replacement("农村信用社误识", READER_ALL, SOURCE_CREDIT_OLD, SOURCE_CREDIT_NEW),
    Replacement("农村信用社误识", READER_MID, SOURCE_CREDIT_OLD, SOURCE_CREDIT_NEW),
    Replacement("民政概述跨页漏句", SOURCE_LOW, SOURCE_CIVIL_OLD, SOURCE_CIVIL_NEW),
    Replacement("民政概述跨页漏句", SUMMARY, SOURCE_CIVIL_OLD, SOURCE_CIVIL_NEW),
    Replacement("民政概述跨页漏句", READER_ALL, READER_CIVIL_ALL_OLD, READER_CIVIL_ALL_NEW),
    Replacement("民政概述跨页漏句", READER_LOW, READER_CIVIL_LOW_OLD, READER_CIVIL_LOW_NEW),
    Replacement("边防管理漏句", SOURCE_LOW, SOURCE_PORT_OLD, SOURCE_PORT_NEW),
    Replacement("边防管理漏句", SUMMARY, SOURCE_PORT_OLD, SOURCE_PORT_NEW),
    Replacement("边防管理漏句", READER_ALL, READER_PORT_ALL_OLD, READER_PORT_ALL_NEW),
    Replacement("边防管理漏句", READER_LOW, READER_PORT_LOW_OLD, READER_PORT_LOW_NEW),
]

CHECK_TERMS = [
    "董新纳入",
    "农村信用社重新纳入",
    "以上工作对巩固国工作未能正常运转",
    "以上工作对巩固国防",
    "港务监督部门精神",
    "联合通告",
]

EVIDENCE_TERMS = {
    "workbench/ocr/paddle_ocr/中/part02/page_0349.txt": ["农村信用社重新纳入人民银行管理体制"],
    "workbench/ocr/paddle_ocr/下/part01/page_0016.txt": ["以上工作对巩固国", "防、稳定社会、树立良好的社会风尚方面都取得成效"],
    "workbench/ocr/paddle_ocr/下/part01/page_0017.txt": ["工作未能正常运转"],
    "workbench/ocr/paddle_ocr/下/part01/page_0095.txt": ["制订《关于加强港口管理、整顿水上交通秩序的联合通告》", "根据《联合通告》"],
}


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def write(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8")


def line_hits(path: Path, needle: str) -> list[int]:
    return [i for i, line in enumerate(read(path).splitlines(), 1) if needle in line]


def apply_replacements() -> list[dict[str, object]]:
    results: list[dict[str, object]] = []
    for item in REPLACEMENTS:
        text = read(item.path)
        before = text.count(item.old)
        after_present = text.count(item.new)
        if before:
            text = text.replace(item.old, item.new)
            write(item.path, text)
        results.append({
            "label": item.label,
            "path": rel(item.path),
            "old_count": before,
            "new_count_before": after_present,
            "new_count_after": read(item.path).count(item.new),
            "old_preview": item.old[:80],
            "new_preview": item.new[:120],
        })
    return results


def collect_residuals(paths: list[Path]) -> dict[str, dict[str, int]]:
    residuals: dict[str, dict[str, int]] = {}
    for path in paths:
        if not path.exists():
            continue
        text = read(path)
        hits = {term: text.count(term) for term in CHECK_TERMS if text.count(term)}
        if hits:
            residuals[rel(path)] = hits
    return residuals


def collect_evidence() -> dict[str, dict[str, list[int]]]:
    evidence: dict[str, dict[str, list[int]]] = {}
    for path in EVIDENCE_FILES:
        path_key = rel(path)
        evidence[path_key] = {}
        for term in EVIDENCE_TERMS.get(path_key, []):
            evidence[path_key][term] = line_hits(path, term)
    return evidence


def render(results: list[dict[str, object]], residuals: dict[str, dict[str, int]], evidence: dict[str, dict[str, list[int]]]) -> str:
    by_label: dict[str, int] = defaultdict(int)
    for item in results:
        by_label[str(item["label"])] += int(item["old_count"])
    total = sum(int(item["old_count"]) for item in results)

    lines = [
        "# PaddleOCR可证句段残留补修 batch369",
        "",
        f"- 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"- 修复总数：{total}",
        "- 范围：中册金融、下册民政概述、下册治安司法边防管理三处可证句段，以及对应正式阅读器。",
        "- 依据：页级 PaddleOCR 成句证据；只修完整句段，不作危险全局替换。",
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
        lines.append(
            f"- `{item['path']}`：{item['label']}，替换 {item['old_count']} 处；"
            f"修后目标短语 {item['new_count_after']} 处。"
        )

    lines.extend(["", "## 残留检查"])
    if residuals:
        for path, hits in residuals.items():
            compact = "，".join(f"`{term}` {value}" for term, value in hits.items())
            lines.append(f"- `{path}`：{compact}")
    else:
        lines.append("- 检查范围未见目标残留词。")
    return "\n".join(lines) + "\n"


def upsert_memory(results: list[dict[str, object]], residuals: dict[str, dict[str, int]]) -> None:
    total = sum(int(item["old_count"]) for item in results)
    all_hits = residuals.get("workbench/body_chapters/连云港市志_全书_正文汇总.md", {})
    reader_hits = residuals.get("output/final_reader/连云港市志_全书.html", {})
    block = f"""{MARKER}

- 依据 `workbench/ocr/paddle_ocr/中/part02/page_0349.txt`、`workbench/ocr/paddle_ocr/下/part01/page_0016.txt`、`workbench/ocr/paddle_ocr/下/part01/page_0017.txt`、`workbench/ocr/paddle_ocr/下/part01/page_0095.txt`，补修农村信用社、民政概述跨页漏句、边防管理漏句三处可证残留，共 {total} 处。
- 代表修复：`农村信用社董新纳入人民银行管理体制 -> 农村信用社重新纳入人民银行管理体制`；`以上工作对巩固国工作未能正常运转 -> 以上工作对巩固国防、稳定社会、树立良好的社会风尚方面都取得成效。“文化大革命”期间，全市民政部门工作未能正常运转`；补入 `制订《关于加强港口管理、整顿水上交通秩序的联合通告》，各边防派出所根据《联合通告》`。
- 本批后全书正文汇总检查范围：`董新纳入` {all_hits.get('董新纳入', 0)}，`以上工作对巩固国工作未能正常运转` {all_hits.get('以上工作对巩固国工作未能正常运转', 0)}，`港务监督部门精神` {all_hits.get('港务监督部门精神', 0)}，`联合通告` {all_hits.get('联合通告', 0)}。
- 本批后全书 reader 检查范围：`董新纳入` {reader_hits.get('董新纳入', 0)}，`以上工作对巩固国工作未能正常运转` {reader_hits.get('以上工作对巩固国工作未能正常运转', 0)}，`港务监督部门精神` {reader_hits.get('港务监督部门精神', 0)}，`联合通告` {reader_hits.get('联合通告', 0)}。
- 未作 `人 -> 入`、`述 -> 沭`、`沐 -> 沭`、`准 -> 淮` 等全局替换；未处理 OCR 源文件、backup、obsolete、历史交付包；未打开、展示或嵌入图片。
- 报告：`output/reports/paddle_proven_residues_batch369_20260708.md`；进度：`output/reports/progress/20260708_PaddleOCR可证句段残留补修第三百六十九批.md`。
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
    touched = sorted({item.path for item in REPLACEMENTS})
    residuals = collect_residuals(touched)
    evidence = collect_evidence()
    report = render(results, residuals, evidence)
    data = {
        "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "total": sum(int(item["old_count"]) for item in results),
        "results": results,
        "evidence": evidence,
        "residuals": residuals,
    }
    REPORT_JSON.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    REPORT.write_text(report, encoding="utf-8")
    PROGRESS.write_text(report, encoding="utf-8")
    upsert_memory(results, residuals)
    print(f"total={data['total']}")
    print(json.dumps(residuals, ensure_ascii=False, indent=2))
    print(f"report={REPORT}")


if __name__ == "__main__":
    main()
