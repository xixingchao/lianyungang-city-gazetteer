# -*- coding: utf-8 -*-
"""Repair high-confidence fixed phrase residues for batch 410."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

LOWER_PART2 = ROOT / "workbench" / "body_chapters" / "第五十二卷至第六十卷及附录（下part02）.md"
FULL_SRC = ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md"
LOWER_HTML = ROOT / "output" / "final_reader" / "连云港市志_下册.html"
FULL_HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"

REPORT = ROOT / "output" / "reports" / "verified_fixed_phrase_batch410_20260708.md"
REPORT_JSON = ROOT / "output" / "reports" / "verified_fixed_phrase_batch410_20260708.json"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260708_固定搭配形近残留补修第四百一十批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"
MARKER = "## 2026-07-08 固定搭配形近残留补修第四百一十批"

CURRENT_TARGETS = [LOWER_PART2, FULL_SRC, LOWER_HTML, FULL_HTML]

REPLACEMENTS: list[tuple[list[Path], str, str, str, str]] = [
    (
        CURRENT_TARGETS,
        "兴举废坠为已任",
        "兴举废坠为己任",
        "固定搭配：以兴举废坠为己任",
        "`以……为己任` 为固定搭配，`已任` 为形近误字。",
    ),
    (
        CURRENT_TARGETS,
        "以修志为已任",
        "以修志为己任",
        "固定搭配：以修志为己任",
        "书末序跋同段两处均为 `以修志为己任` 固定搭配，`已任` 为形近误字。",
    ),
    (
        CURRENT_TARGETS,
        "调整篇自、充实内容、修改定稿",
        "调整篇目、充实内容、修改定稿",
        "OCR 反证：调整篇目",
        "`workbench/ocr/tesseract_check/book_end_20260706/page_0478_tess.txt:28` 作 `调整篇目`。",
    ),
    (
        CURRENT_TARGETS,
        "倪长犀耳闻自赌作《地震记》",
        "倪长犀耳闻目睹作《地震记》",
        "固定搭配：耳闻目睹",
        "人物小传上下文为亲历地震后作《地震记》，`耳闻目睹` 为固定成语，`自赌` 为形近误字。",
    ),
    (
        CURRENT_TARGETS,
        "将所得钱财为已有",
        "将所得钱财攫为己有",
        "OCR 反证：攫为己有",
        "`workbench/ocr/paddle_ocr/下/part02/page_0128.txt:27` 作 `将所得钱财攫为己有`；当前全书 reader 已为同文。",
    ),
]

EVIDENCE_REFS = [
    ("workbench/ocr/paddle_ocr/下/part02/page_0128.txt", [27]),
    ("workbench/ocr/tesseract_check/book_end_20260706/page_0478_tess.txt", [28]),
    ("workbench/body_chapters/第五十二卷至第六十卷及附录（下part02）.md", [4798, 17010, 22808, 23819, 23910, 23915]),
]

RESIDUES = ["为已任", "修志为已任", "调整篇自", "篇自、充实内容", "耳闻自赌", "为已有"]


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def apply_one(path: Path, old: str, new: str, label: str, basis: str) -> dict[str, object]:
    text = read(path)
    old_count = text.count(old)
    if old_count:
        path.write_text(text.replace(old, new), encoding="utf-8")
        status = "fixed"
    elif new in text:
        status = "already_fixed"
    else:
        status = "not_present"
    after = read(path)
    return {
        "path": rel(path),
        "label": label,
        "basis": basis,
        "status": status,
        "fixed": old_count,
        "new_hits": after.count(new),
    }


def evidence_lines() -> list[str]:
    out: list[str] = []
    for rel_path, nums in EVIDENCE_REFS:
        path = ROOT / rel_path
        if not path.exists():
            out.append(f"{rel_path}: missing")
            continue
        lines = read(path).splitlines()
        for num in nums:
            if 1 <= num <= len(lines):
                out.append(f"{rel_path}:{num}: {lines[num - 1].strip()}")
    return out


def residue_counts() -> dict[str, dict[str, int]]:
    out: dict[str, dict[str, int]] = {}
    for path in CURRENT_TARGETS:
        if path.exists():
            text = read(path)
            out[rel(path)] = {needle: text.count(needle) for needle in RESIDUES}
    return out


def write_report(results: list[dict[str, object]], residues: dict[str, dict[str, int]]) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    lines = [
        "# 固定搭配形近残留补修 batch410",
        "",
        f"- 生成时间：{now}",
        "- 范围：下册 part02 现行正文源稿、全书正文汇总、当前下册 reader、当前全书 reader。",
        "- 修复：精确短语级补修 `为已任`、`调整篇自`、`耳闻自赌`、`为已有` 残留。",
        "- 跳过：OCR 原始文件、backup、obsolete、历史交付包；未打开、展示或嵌入图片。",
        "",
        "## 修复明细",
    ]
    for item in results:
        lines.append(
            f"- `{item['path']}`：{item['label']}，状态 {item['status']}，"
            f"本次替换 {item['fixed']} 处，新文本命中 {item['new_hits']}。依据：{item['basis']}"
        )
    lines.extend(["", "## 证据摘录"])
    for hit in evidence_lines():
        lines.append(f"- {hit}")
    lines.extend(["", "## 残留复扫"])
    for path, counts in residues.items():
        shown = ", ".join(f"{key}={value}" for key, value in counts.items())
        lines.append(f"- `{path}`：{shown}")
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    REPORT_JSON.write_text(
        json.dumps({"time": now, "results": results, "evidence": evidence_lines(), "residues": residues}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    PROGRESS.write_text(REPORT.read_text(encoding="utf-8"), encoding="utf-8")


def update_memory() -> None:
    block = f"""{MARKER}

- 补修下册 part02、全书正文汇总、当前下册/全书 reader 中一组精确固定搭配残留：`兴举废坠为已任 -> 兴举废坠为己任`、`以修志为已任 -> 以修志为己任`、`调整篇自 -> 调整篇目`、`耳闻自赌 -> 耳闻目睹`、`将所得钱财为已有 -> 将所得钱财攫为己有`。
- `调整篇目` 依据 `workbench/ocr/tesseract_check/book_end_20260706/page_0478_tess.txt:28`，`攫为己有` 依据 `workbench/ocr/paddle_ocr/下/part02/page_0128.txt:27`；`为己任`、`耳闻目睹` 按固定搭配和上下文精确修复。
- 未处理 OCR 原始文件、backup、obsolete、历史交付包；未打开、展示或嵌入图片。
- 报告：`output/reports/verified_fixed_phrase_batch410_20260708.md`；进度：`output/reports/progress/20260708_固定搭配形近残留补修第四百一十批.md`。
"""
    old = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    start = old.find(MARKER)
    if start < 0:
        MEMORY.write_text(old.rstrip() + "\n\n" + block.strip() + "\n", encoding="utf-8")
        return
    next_start = old.find("\n## ", start + 1)
    if next_start < 0:
        MEMORY.write_text(old[:start].rstrip() + "\n\n" + block.strip() + "\n", encoding="utf-8")
    else:
        MEMORY.write_text(old[:start].rstrip() + "\n\n" + block.strip() + old[next_start:], encoding="utf-8")


def main() -> None:
    results = []
    for paths, old, new, label, basis in REPLACEMENTS:
        for path in paths:
            results.append(apply_one(path, old, new, label, basis))
    residues = residue_counts()
    write_report(results, residues)
    update_memory()
    changed = sum(int(item["fixed"]) for item in results)
    print(json.dumps({"changed": changed, "report": str(REPORT)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
