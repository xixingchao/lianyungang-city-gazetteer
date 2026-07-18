# -*- coding: utf-8 -*-
"""Repair PaddleOCR-proven 准北/淮北 salt-industry phrases."""

from __future__ import annotations

import json
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "output" / "reports" / "verified_huaibei_salt_batch372_20260708.md"
REPORT_JSON = ROOT / "output" / "reports" / "verified_huaibei_salt_batch372_20260708.json"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260708_可证淮北盐业专名补修第三百七十二批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"
MARKER = "## 2026-07-08 可证淮北盐业专名补修第三百七十二批"

PATHS = [
    ROOT / "workbench" / "body_chapters" / "第三十卷至第四十二卷（中part02）.md",
    ROOT / "workbench" / "body_chapters" / "第五十二卷至第六十卷及附录（下part02）.md",
    ROOT / "workbench" / "body_chapters" / "第十七卷至第二十九卷（中part01）.md",
    ROOT / "workbench" / "body_chapters" / "第四十三卷至第五十一卷（下part01）.md",
    ROOT / "workbench" / "body_chapters" / "连云港市志_上册_正文汇总.md",
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
    ROOT / "workbench" / "body_chapters" / "上" / "第十卷至第十六卷（part03）.md",
]

EVIDENCE_FILES = [
    ROOT / "workbench" / "ocr" / "paddle_ocr" / "中" / "part02" / "page_0020.txt",
    ROOT / "workbench" / "ocr" / "paddle_ocr" / "中" / "part02" / "page_0028.txt",
    ROOT / "workbench" / "ocr" / "paddle_ocr" / "中" / "part02" / "page_0081.txt",
    ROOT / "workbench" / "ocr" / "paddle_ocr" / "中" / "part02" / "page_0138.txt",
    ROOT / "workbench" / "ocr" / "paddle_ocr" / "中" / "part02" / "page_0230.txt",
    ROOT / "workbench" / "ocr" / "paddle_ocr" / "中" / "part02" / "page_0288.txt",
    ROOT / "workbench" / "ocr" / "paddle_ocr" / "中" / "part02" / "page_0312.txt",
    ROOT / "workbench" / "ocr" / "paddle_ocr" / "中" / "part02" / "page_0327.txt",
    ROOT / "workbench" / "ocr" / "paddle_ocr" / "中" / "part02" / "page_0335.txt",
    ROOT / "workbench" / "ocr" / "paddle_ocr" / "中" / "part02" / "page_0382.txt",
    ROOT / "workbench" / "ocr" / "paddle_ocr" / "中" / "part02" / "page_0457.txt",
    ROOT / "workbench" / "ocr" / "paddle_ocr" / "中" / "part02" / "page_0497.txt",
    ROOT / "workbench" / "ocr" / "paddle_ocr" / "中" / "part01" / "page_0135.txt",
    ROOT / "workbench" / "ocr" / "paddle_ocr" / "中" / "part01" / "page_0142.txt",
    ROOT / "workbench" / "ocr" / "paddle_ocr" / "中" / "part01" / "page_0456.txt",
    ROOT / "workbench" / "ocr" / "paddle_ocr" / "中" / "part01" / "page_0459.txt",
    ROOT / "workbench" / "ocr" / "paddle_ocr" / "上" / "part03" / "page_0150.txt",
    ROOT / "workbench" / "ocr" / "paddle_ocr" / "上" / "part03" / "page_0155.txt",
    ROOT / "workbench" / "ocr" / "paddle_ocr" / "上" / "part03" / "page_0163.txt",
    ROOT / "workbench" / "ocr" / "paddle_ocr" / "上" / "part03" / "page_0164.txt",
    ROOT / "workbench" / "ocr" / "paddle_ocr" / "上" / "part03" / "page_0165.txt",
    ROOT / "workbench" / "ocr" / "paddle_ocr" / "上" / "part03" / "page_0167.txt",
    ROOT / "workbench" / "ocr" / "paddle_ocr" / "上" / "part03" / "page_0170.txt",
    ROOT / "workbench" / "ocr" / "paddle_ocr" / "上" / "part03" / "page_0171.txt",
    ROOT / "workbench" / "ocr" / "paddle_ocr" / "下" / "part01" / "page_0306.txt",
    ROOT / "workbench" / "ocr" / "paddle_ocr" / "下" / "part01" / "page_0350.txt",
    ROOT / "workbench" / "ocr" / "paddle_ocr" / "下" / "part02" / "page_0136.txt",
    ROOT / "workbench" / "ocr" / "paddle_ocr" / "下" / "part02" / "page_0211.txt",
    ROOT / "workbench" / "ocr" / "paddle_ocr" / "下" / "part02" / "page_0377.txt",
]

EVIDENCE_TERMS = {
    "workbench/ocr/paddle_ocr/中/part02/page_0020.txt": ["淮北盐务稽核分所"],
    "workbench/ocr/paddle_ocr/中/part02/page_0028.txt": ["淮北盐务机关"],
    "workbench/ocr/paddle_ocr/中/part02/page_0081.txt": ["淮北建坨委员会"],
    "workbench/ocr/paddle_ocr/中/part02/page_0138.txt": ["淮北盐场增产原盐"],
    "workbench/ocr/paddle_ocr/中/part02/page_0230.txt": ["淮北盐业兴旺"],
    "workbench/ocr/paddle_ocr/中/part02/page_0288.txt": ["淮北盐税收入统计表"],
    "workbench/ocr/paddle_ocr/中/part02/page_0312.txt": ["淮北盐务管理局"],
    "workbench/ocr/paddle_ocr/中/part02/page_0327.txt": ["淮北盐区税率", "淮北盐区征收盐税"],
    "workbench/ocr/paddle_ocr/中/part02/page_0335.txt": ["淮北盐务管理局征收管理"],
    "workbench/ocr/paddle_ocr/中/part02/page_0382.txt": ["淮北盐场办事处"],
    "workbench/ocr/paddle_ocr/中/part02/page_0457.txt": ["淮北盐特委撤销"],
    "workbench/ocr/paddle_ocr/中/part02/page_0497.txt": ["淮北盐特区"],
    "workbench/ocr/paddle_ocr/中/part01/page_0135.txt": ["淮北盐务局协调", "淮北盐场运销"],
    "workbench/ocr/paddle_ocr/中/part01/page_0142.txt": ["淮北盐场生产"],
    "workbench/ocr/paddle_ocr/中/part01/page_0456.txt": ["淮北盐为主要物资"],
    "workbench/ocr/paddle_ocr/中/part01/page_0459.txt": ["淮北海盐"],
    "workbench/ocr/paddle_ocr/上/part03/page_0150.txt": ["淮北盐务局和各制盐场", "淮北盐务局在海州"],
    "workbench/ocr/paddle_ocr/上/part03/page_0155.txt": ["淮北场办事处"],
    "workbench/ocr/paddle_ocr/上/part03/page_0163.txt": ["淮北供应加碘盐"],
    "workbench/ocr/paddle_ocr/上/part03/page_0164.txt": ["淮北盐价", "淮北各场盐价"],
    "workbench/ocr/paddle_ocr/上/part03/page_0165.txt": ["淮北地区食盐"],
    "workbench/ocr/paddle_ocr/上/part03/page_0167.txt": ["淮北五、六岸"],
    "workbench/ocr/paddle_ocr/上/part03/page_0170.txt": ["淮北共设6个区", "淮北各制盐场"],
    "workbench/ocr/paddle_ocr/上/part03/page_0171.txt": ["淮北各场登记"],
    "workbench/ocr/paddle_ocr/下/part01/page_0306.txt": ["淮北盐特委"],
    "workbench/ocr/paddle_ocr/下/part01/page_0350.txt": ["淮北盐运使司"],
    "workbench/ocr/paddle_ocr/下/part02/page_0136.txt": ["《淮北盐工报》"],
    "workbench/ocr/paddle_ocr/下/part02/page_0211.txt": ["淮北盐业医院"],
    "workbench/ocr/paddle_ocr/下/part02/page_0377.txt": ["淮北盐业生产"],
}

PHRASES = [
    ("淮北盐务管理局", "准北盐务管理局", "淮北盐务管理局"),
    ("淮北盐工报", "《准北盐工报》", "《淮北盐工报》"),
    ("淮北盐务稽核分所", "准北盐务稽核分所", "淮北盐务稽核分所"),
    ("淮北盐场", "准北盐场", "淮北盐场"),
    ("淮北盐区", "准北盐区", "淮北盐区"),
    ("淮北盐务局", "准北盐务局", "淮北盐务局"),
    ("淮北场办事处", "准北场办事处", "淮北场办事处"),
    ("淮北盐务机关", "准北盐务机关", "淮北盐务机关"),
    ("淮北盐特委", "准北盐特委", "淮北盐特委"),
    ("淮北盐特区", "准北盐特区", "淮北盐特区"),
    ("淮北盐运使司", "准北盐运使司", "淮北盐运使司"),
    ("淮北盐业", "准北盐业", "淮北盐业"),
    ("淮北盐税", "准北盐税", "淮北盐税"),
    ("淮北各制盐场", "准北各制盐场", "淮北各制盐场"),
    ("淮北各场", "准北各场", "淮北各场"),
    ("淮北运署", "准北运署", "淮北运署"),
    ("淮北供应加碘盐", "准北供应加碘盐", "淮北供应加碘盐"),
    ("淮北盐价", "准北盐价", "淮北盐价"),
    ("淮北五六岸", "准北五、六岸", "淮北五、六岸"),
    ("淮北分区", "准北共设6个区", "淮北共设6个区"),
    ("淮北建坨委员会", "准北建坨委员会", "淮北建坨委员会"),
    ("淮北盐物资", "准北盐为主要物资", "淮北盐为主要物资"),
    ("淮北海盐", "准北海盐", "淮北海盐"),
    ("淮北地区食盐", "准北地区食盐", "淮北地区食盐"),
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
        "# 可证淮北盐业专名补修 batch372",
        "",
        f"- 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"- 修复总数：{total}",
        "- 范围：现行正文源稿与正文汇总中已由 PaddleOCR 证实的淮北盐业专名。",
        "- 原则：只修完整盐业专名；不作 `准 -> 淮` 全局替换，保留 `准北2BG-6A` 等未证残留。",
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

- 依据中册 part01/0135、0142、0456、0459，中册 part02/0020、0028、0081、0138、0230、0288、0312、0327、0335、0382、0457、0497，上册 part03/0150、0155、0163、0164、0165、0167、0170、0171，下册 part01/0306、0350，下册 part02/0136、0211、0377 页级 PaddleOCR 成句证据，补修现行源稿和全书汇总中的淮北盐业专名，共 {total} 处。
- 代表修复：`准北盐务管理局/盐务局/盐务稽核分所/盐务机关 -> 淮北...`，`《准北盐工报》 -> 《淮北盐工报》`，`准北盐场/盐区/盐业/盐税/盐价 -> 淮北...`，`准北各制盐场/各场/运署/五、六岸/共设6个区 -> 淮北...`，`准北建坨委员会/准北海盐/准北地区食盐 -> 淮北...`。
- 本批后全书正文汇总旧词检查剩余：`准北盐务管理局` {summary_old.get('准北盐务管理局', 0)}，`《准北盐工报》` {summary_old.get('《准北盐工报》', 0)}，`准北盐场` {summary_old.get('准北盐场', 0)}，`准北盐务局` {summary_old.get('准北盐务局', 0)}，`准北盐区` {summary_old.get('准北盐区', 0)}。
- 未处理 OCR 源文件、backup、obsolete、历史交付包；未作 `准 -> 淮` 全局替换，未证的型号、地名和零散残留继续保留待核；未打开、展示或嵌入图片。
- 报告：`output/reports/verified_huaibei_salt_batch372_20260708.md`；进度：`output/reports/progress/20260708_可证淮北盐业专名补修第三百七十二批.md`。
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
