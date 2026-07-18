# -*- coding: utf-8 -*-
"""Synchronize one verified 归入 residue from current reader back to source drafts."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOWER = ROOT / "workbench" / "body_chapters" / "第五十二卷至第六十卷及附录（下part02）.md"
FULL = ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md"
READER = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT = ROOT / "output" / "reports" / "verified_guiru_source_sync_batch391_20260708.md"
REPORT_JSON = ROOT / "output" / "reports" / "verified_guiru_source_sync_batch391_20260708.json"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260708_归入源稿同步第三百九十一批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"
MARKER = "## 2026-07-08 归入源稿同步第三百九十一批"

FIXES = [
    (LOWER, "归人 i韵中", "归入 i韵中"),
    (FULL, "归人i韵中", "归入i韵中"),
]


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def line_hits(path: Path, needles: tuple[str, ...]) -> list[str]:
    hits = []
    for i, line in enumerate(read(path).splitlines(), 1):
        if any(needle in line for needle in needles):
            hits.append(f"{i}: {line.strip()}")
    return hits


def main() -> None:
    results = []
    for path, old, new in FIXES:
        text = read(path)
        count = text.count(old)
        if count != 1:
            raise RuntimeError(f"{rel(path)} expected one `{old}` hit, got {count}")
        path.write_text(text.replace(old, new, 1), encoding="utf-8")
        after = read(path)
        results.append({
            "path": rel(path),
            "old": old,
            "new": new,
            "fixed": count,
            "remaining_old": after.count(old),
        })

    reader_evidence = line_hits(READER, ("归入 i韵中",))
    residues = {
        rel(LOWER): line_hits(LOWER, ("归人 i韵中", "归入 i韵中")),
        rel(FULL): line_hits(FULL, ("归人i韵中", "归入i韵中")),
        rel(READER): reader_evidence,
    }

    lines = [
        "# 归入源稿同步 batch391",
        "",
        f"- 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "- 范围：下册方言章节源稿与全书正文汇总，不处理 OCR 源文件、backup、obsolete 或历史交付包。",
        "- 修复：仅同步 `韵字归人 i韵中/归人i韵中` -> `韵字归入 i韵中/归入i韵中`。",
        "- 图片处理：未打开、展示或嵌入图片。",
        "",
        "## 修复明细",
    ]
    for item in results:
        lines.append(f"- `{item['path']}`：`{item['old']}` -> `{item['new']}`，{item['fixed']} 处；剩余旧词 {item['remaining_old']}。")
    lines.extend(["", "## 证据与复扫"])
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

- 对照当前正式 reader，将下册方言章节源稿与全书正文汇总中的 `韵字归人 i韵中/归人i韵中` 同步为 `韵字归入 i韵中/归入i韵中`，共 2 处；reader 证据位于 `output/final_reader/连云港市志_全书.html` 行 24110。
- 仅处理 `归入` 这一处明确残留，未重写方言音标整段；未处理 OCR 源文件、backup、obsolete、历史交付包；未打开、展示或嵌入图片。
- 报告：`output/reports/verified_guiru_source_sync_batch391_20260708.md`；进度：`output/reports/progress/20260708_归入源稿同步第三百九十一批.md`。
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
