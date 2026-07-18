# -*- coding: utf-8 -*-
"""Repair PaddleOCR-proven 加人/编人 residual phrases."""

from __future__ import annotations

import json
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "output" / "reports" / "verified_join_compile_batch375_20260708.md"
REPORT_JSON = ROOT / "output" / "reports" / "verified_join_compile_batch375_20260708.json"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260708_加入编入残留补修第三百七十五批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"
MARKER = "## 2026-07-08 加入编入残留补修第三百七十五批"

PATHS = [
    ROOT / "workbench" / "body_chapters" / "第三十卷至第四十二卷（中part02）.md",
    ROOT / "workbench" / "body_chapters" / "第四十三卷至第五十一卷（下part01）.md",
    ROOT / "workbench" / "body_chapters" / "第五十二卷至第六十卷及附录（下part02）.md",
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
]

EVIDENCE_FILES = [
    ROOT / "workbench" / "ocr" / "paddle_ocr" / "中" / "part02" / "page_0400.txt",
    ROOT / "workbench" / "ocr" / "paddle_ocr" / "下" / "part01" / "page_0157.txt",
    ROOT / "workbench" / "ocr" / "paddle_ocr" / "下" / "part01" / "page_0170.txt",
    ROOT / "workbench" / "ocr" / "paddle_ocr" / "下" / "part01" / "page_0172.txt",
    ROOT / "workbench" / "ocr" / "paddle_ocr" / "下" / "part01" / "page_0174.txt",
    ROOT / "workbench" / "ocr" / "paddle_ocr" / "下" / "part02" / "page_0361.txt",
    ROOT / "workbench" / "ocr" / "paddle_ocr" / "下" / "part02" / "page_0369.txt",
    ROOT / "workbench" / "ocr" / "paddle_ocr" / "下" / "part02" / "page_0376.txt",
    ROOT / "workbench" / "ocr" / "paddle_ocr" / "下" / "part02" / "page_0379.txt",
    ROOT / "workbench" / "ocr" / "paddle_ocr" / "下" / "part02" / "page_0391.txt",
]

EVIDENCE_TERMS = {
    "workbench/ocr/paddle_ocr/中/part02/page_0400.txt": ["并加入共产党的"],
    "workbench/ocr/paddle_ocr/下/part01/page_0157.txt": ["编入现役"],
    "workbench/ocr/paddle_ocr/下/part01/page_0170.txt": ["编入主力"],
    "workbench/ocr/paddle_ocr/下/part01/page_0172.txt": ["被编入九十八军", "被编入八路军苏皖纵队"],
    "workbench/ocr/paddle_ocr/下/part01/page_0174.txt": ["编入灌云县警卫团", "编入华东野"],
    "workbench/ocr/paddle_ocr/下/part02/page_0361.txt": ["加入抗日队伍"],
    "workbench/ocr/paddle_ocr/下/part02/page_0369.txt": ["编入新四军三师九旅二十六团"],
    "workbench/ocr/paddle_ocr/下/part02/page_0376.txt": ["编入滨海军区二十三团"],
    "workbench/ocr/paddle_ocr/下/part02/page_0379.txt": ["编入主攻团", "加入共青团"],
    "workbench/ocr/paddle_ocr/下/part02/page_0391.txt": ["加入北京人民艺术剧院"],
}

PHRASES = [
    ("加入", "并加人共产党的", "并加入共产党的"),
    ("加入", "加人共青团", "加入共青团"),
    ("加入", "加人抗日队伍", "加入抗日队伍"),
    ("加入", "加人北京人民艺术剧院", "加入北京人民艺术剧院"),
    ("编入", "编人新四军三师九旅二十六团", "编入新四军三师九旅二十六团"),
    ("编入", "编人滨海军区二十三团", "编入滨海军区二十三团"),
    ("编入", "编人主攻团", "编入主攻团"),
    ("编入", "编人现役", "编入现役"),
    ("编入", "编人主力", "编入主力"),
    ("编入", "被编人九十八军", "被编入九十八军"),
    ("编入", "被编人八路军苏皖纵队", "被编入八路军苏皖纵队"),
    ("编入", "编人灌云县警卫团", "编入灌云县警卫团"),
    ("编入", "编人华东野", "编入华东野"),
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
        results.append({"label": item.label, "path": rel(item.path), "old": item.old, "new": item.new, "old_count": count, "new_count_after": read(item.path).count(item.new)})
    return results


def collect_evidence() -> dict[str, dict[str, list[int]]]:
    return {rel(path): {term: line_hits(path, term) for term in EVIDENCE_TERMS.get(rel(path), [])} for path in EVIDENCE_FILES}


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
        "# 加入编入残留补修 batch375",
        "",
        f"- 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"- 修复总数：{total}",
        "- 范围：现行正文源稿与全书正文汇总中已由 PaddleOCR 证实的人物/军事 `加入/编入` 完整短语。",
        "- 原则：只修完整短语；不处理 `采编人员`、`在编人员`、`参加人数` 等合法词。",
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


def upsert_memory(results, old_counts) -> None:
    total = sum(int(item["old_count"]) for item in results)
    summary_old = old_counts.get("workbench/body_chapters/连云港市志_全书_正文汇总.md", {})
    block = f"""{MARKER}

- 依据中册 part02/page_0400，下册 part01/page_0157、0170、0172、0174，下册 part02/page_0361、0369、0376、0379、0391 页级 PaddleOCR 成句证据，补修人物/军事类 `加人/编人 -> 加入/编入` 完整短语，共 {total} 处。
- 代表修复：`并加人共产党的 -> 并加入共产党的`、`加人共青团/抗日队伍/北京人民艺术剧院 -> 加入...`、`编人现役/主力/主攻团/新四军三师九旅二十六团/滨海军区二十三团/灌云县警卫团/华东野... -> 编入...`、`被编人九十八军/八路军苏皖纵队 -> 被编入...`。
- 本批后全书正文汇总旧词检查剩余：`并加人共产党的` {summary_old.get('并加人共产党的', 0)}，`加人共青团` {summary_old.get('加人共青团', 0)}，`编人现役` {summary_old.get('编人现役', 0)}，`被编人九十八军` {summary_old.get('被编人九十八军', 0)}。
- 未处理 OCR 源文件、backup、obsolete、历史交付包；未作危险全局替换；未打开、展示或嵌入图片。
- 报告：`output/reports/verified_join_compile_batch375_20260708.md`；进度：`output/reports/progress/20260708_加入编入残留补修第三百七十五批.md`。
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
    data = {"time": datetime.now().strftime("%Y-%m-%d %H:%M"), "total": sum(int(item["old_count"]) for item in results), "results": results, "evidence": evidence, "old_counts": old_counts, "new_counts": new_counts}
    REPORT_JSON.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    REPORT.write_text(report, encoding="utf-8")
    PROGRESS.write_text(report, encoding="utf-8")
    upsert_memory(results, old_counts)
    print(f"total={data['total']}")
    print(json.dumps(old_counts, ensure_ascii=False, indent=2))
    print(f"report={REPORT}")


if __name__ == "__main__":
    main()
