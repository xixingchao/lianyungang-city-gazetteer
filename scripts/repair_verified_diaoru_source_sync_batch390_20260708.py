# -*- coding: utf-8 -*-
"""Synchronize verified 调入 residues from current reader back to source drafts."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MID = ROOT / "workbench" / "body_chapters" / "第三十卷至第四十二卷（中part02）.md"
FULL = ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md"
READER = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT = ROOT / "output" / "reports" / "verified_diaoru_source_sync_batch390_20260708.md"
REPORT_JSON = ROOT / "output" / "reports" / "verified_diaoru_source_sync_batch390_20260708.json"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260708_调入源稿同步第三百九十批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"
MARKER = "## 2026-07-08 调入源稿同步第三百九十批"

PHRASE_OLD = "招工、调人等方式"
PHRASE_NEW = "招工、调入等方式"
EXPECTED_HEADER_LINES = 7


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def line_hits(path: Path, needle: str) -> list[str]:
    hits = []
    for i, line in enumerate(read(path).splitlines(), 1):
        if needle in line:
            hits.append(f"{i}: {line.strip()}")
    return hits


def sync_file(path: Path) -> dict[str, object]:
    text = read(path)
    phrase_count = text.count(PHRASE_OLD)
    if phrase_count != 1:
        raise RuntimeError(f"{rel(path)} expected one phrase hit, got {phrase_count}")

    lines = text.splitlines()
    header_lines = [i for i, line in enumerate(lines) if line == "调人"]
    if len(header_lines) != EXPECTED_HEADER_LINES:
        raise RuntimeError(f"{rel(path)} expected {EXPECTED_HEADER_LINES} standalone table headers, got {len(header_lines)}")

    text = text.replace(PHRASE_OLD, PHRASE_NEW, 1)
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if line == "调人":
            lines[i] = "调入"
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    after = read(path)
    return {
        "path": rel(path),
        "phrase_fixed": phrase_count,
        "header_lines_fixed": len(header_lines),
        "remaining_phrase_old": after.count(PHRASE_OLD),
        "remaining_standalone_headers": sum(1 for line in after.splitlines() if line == "调人"),
    }


def collect_residues() -> dict[str, list[str]]:
    paths = [MID, FULL, READER]
    return {rel(path): line_hits(path, "调人") for path in paths}


def main() -> None:
    results = [sync_file(MID), sync_file(FULL)]
    residues = collect_residues()
    reader_evidence = line_hits(READER, PHRASE_NEW)

    lines = [
        "# 调入源稿同步 batch390",
        "",
        f"- 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "- 范围：现行正文源稿与全书正文汇总，不处理 OCR 源文件、backup、obsolete 或历史交付包。",
        f"- 成句同步：`{PHRASE_OLD}` -> `{PHRASE_NEW}`，每个源文件 1 处。",
        "- 表头同步：仅将粮食/油脂调运统计表中独立成行的 `调人` 表头改为 `调入`，每个源文件 7 行。",
        "- 图片处理：未打开、展示或嵌入图片。",
        "",
        "## 修复明细",
    ]
    for item in results:
        lines.append(
            f"- `{item['path']}`：成句 {item['phrase_fixed']} 处，独立表头 {item['header_lines_fixed']} 行；"
            f"剩余成句旧词 {item['remaining_phrase_old']}，剩余独立 `调人` 行 {item['remaining_standalone_headers']}。"
        )

    lines.extend(["", "## reader 证据"])
    for hit in reader_evidence:
        lines.append(f"- `output/final_reader/连云港市志_全书.html` {hit}")

    lines.extend(["", "## 剩余 `调人`"])
    for path, hits in residues.items():
        lines.append(f"### {path}")
        if not hits:
            lines.append("- 无。")
        else:
            for hit in hits:
                lines.append(f"- {hit}")

    report = "\n".join(lines) + "\n"
    REPORT.write_text(report, encoding="utf-8")
    REPORT_JSON.write_text(
        json.dumps({"time": datetime.now().strftime("%Y-%m-%d %H:%M"), "results": results, "reader_evidence": reader_evidence, "residues": residues}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    PROGRESS.write_text(report, encoding="utf-8")

    block = f"""{MARKER}

- 对照当前正式 reader，将中册源稿和全书正文汇总中的 `招工、调人等方式` 同步为 `招工、调入等方式`，共 2 处；reader 证据位于 `output/final_reader/连云港市志_全书.html` 行 13297。
- 同步粮食/油脂调运统计表表头：仅修正独立成行的 `调人 -> 调入`，覆盖 `1953～1990年连云港市粮食调入、调出统计表` 与 `1957~1990年连云港市油脂调入、调出统计表` 表头，共 14 行。
- 修后当前源稿剩余 `调人` 均为 `催调人员`、`治调人员`、`抽调人员/抽调人事` 等合法跨词命中；未处理 OCR 源文件、backup、obsolete、历史交付包；未打开、展示或嵌入图片。
- 报告：`output/reports/verified_diaoru_source_sync_batch390_20260708.md`；进度：`output/reports/progress/20260708_调入源稿同步第三百九十批.md`。
"""
    old_mem = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    start = old_mem.find(MARKER)
    if start < 0:
        MEMORY.write_text(old_mem.rstrip() + "\n\n" + block.strip() + "\n", encoding="utf-8")
    else:
        next_start = old_mem.find("\n## ", start + 1)
        MEMORY.write_text(old_mem[:start].rstrip() + "\n\n" + block.strip() + ("\n" if next_start < 0 else old_mem[next_start:]), encoding="utf-8")

    print("results=" + json.dumps(results, ensure_ascii=False))
    print(f"report={REPORT}")


if __name__ == "__main__":
    main()
