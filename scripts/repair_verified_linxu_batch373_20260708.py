# -*- coding: utf-8 -*-
"""Repair PaddleOCR-proven 山东临沐 -> 山东临沭 residues."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "output" / "reports" / "verified_linxu_batch373_20260708.md"
REPORT_JSON = ROOT / "output" / "reports" / "verified_linxu_batch373_20260708.json"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260708_山东临沭地名补修第三百七十三批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"
MARKER = "## 2026-07-08 山东临沭地名补修第三百七十三批"
PATHS = [
    ROOT / "workbench" / "body_chapters" / "上" / "第一卷_自然环境.md",
    ROOT / "workbench" / "body_chapters" / "连云港市志_上册_正文汇总.md",
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
]
EVIDENCE = {
    ROOT / "workbench" / "ocr" / "paddle_ocr" / "上" / "part01" / "page_0135.txt": ["县西北部与山东临沭、郯城以及省内与新沂"],
    ROOT / "workbench" / "ocr" / "paddle_ocr" / "中" / "part01" / "page_0118.txt": ["山东临沭"],
    ROOT / "workbench" / "ocr" / "paddle_ocr" / "中" / "part01" / "page_0119.txt": ["山东临沭"],
}
OLD = "山东临沐"
NEW = "山东临沭"


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def line_hits(path: Path, needle: str) -> list[int]:
    return [i for i, line in enumerate(read(path).splitlines(), 1) if needle in line]


def main() -> None:
    results = []
    for path in PATHS:
        text = read(path)
        count = text.count(OLD)
        if count:
            path.write_text(text.replace(OLD, NEW), encoding="utf-8")
        results.append({"path": rel(path), "old_count": count, "new_count_after": read(path).count(NEW)})
    evidence = {rel(path): {term: line_hits(path, term) for term in terms} for path, terms in EVIDENCE.items()}
    residuals = {rel(path): read(path).count(OLD) for path in PATHS if read(path).count(OLD)}
    total = sum(item["old_count"] for item in results)
    lines = [
        "# 山东临沭地名补修 batch373",
        "",
        f"- 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"- 修复总数：{total}",
        "- 范围：上册自然环境源稿、上册正文汇总、全书正文汇总。",
        "- 原则：只修完整地名 `山东临沐 -> 山东临沭`；不处理 `沐阳` 等历史条目。",
        "- 图片处理：未打开、展示或嵌入图片。",
        "",
        "## 证据位置",
    ]
    for path, terms in evidence.items():
        lines.append(f"- `{path}`")
        for term, hits in terms.items():
            compact = "，".join(str(i) for i in hits) or "未命中"
            lines.append(f"  - 行 {compact}：`{term}`")
    lines.extend(["", "## 替换明细"])
    for item in results:
        lines.append(f"- `{item['path']}`：替换 {item['old_count']} 处；修后 `{NEW}` {item['new_count_after']} 处。")
    lines.extend(["", "## 残留检查"])
    if residuals:
        for path, count in residuals.items():
            lines.append(f"- `{path}`：`{OLD}` {count}")
    else:
        lines.append("- 检查范围未见本批旧词残留。")
    report = "\n".join(lines) + "\n"
    data = {"time": datetime.now().strftime("%Y-%m-%d %H:%M"), "total": total, "results": results, "evidence": evidence, "residuals": residuals}
    REPORT_JSON.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    REPORT.write_text(report, encoding="utf-8")
    PROGRESS.write_text(report, encoding="utf-8")
    block = f"""{MARKER}

- 依据 `workbench/ocr/paddle_ocr/上/part01/page_0135.txt`、`workbench/ocr/paddle_ocr/中/part01/page_0118.txt`、`workbench/ocr/paddle_ocr/中/part01/page_0119.txt`，补修现行源稿中的 `山东临沐 -> 山东临沭`，共 {total} 处。
- 本批只修完整地名，不处理 `沐阳` 等历史行政区划或古地名条目；未处理 OCR 源文件、backup、obsolete、历史交付包；未打开、展示或嵌入图片。
- 报告：`output/reports/verified_linxu_batch373_20260708.md`；进度：`output/reports/progress/20260708_山东临沭地名补修第三百七十三批.md`。
"""
    old_memory = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    start = old_memory.find(MARKER)
    if start < 0:
        MEMORY.write_text(old_memory.rstrip() + "\n\n" + block.strip() + "\n", encoding="utf-8")
    else:
        next_start = old_memory.find("\n## ", start + 1)
        MEMORY.write_text(old_memory[:start].rstrip() + "\n\n" + block.strip() + ("\n" if next_start < 0 else old_memory[next_start:]), encoding="utf-8")
    print(f"total={total}")
    print(json.dumps(residuals, ensure_ascii=False, indent=2))
    print(f"report={REPORT}")


if __name__ == "__main__":
    main()
