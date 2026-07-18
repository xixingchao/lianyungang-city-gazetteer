# -*- coding: utf-8 -*-
"""Remove proven page-header residues inside Volume 59 Dialect."""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = [
    ROOT / "workbench" / "body_chapters" / "第五十二卷至第六十卷及附录（下part02）.md",
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
]
REPORT_MD = ROOT / "output" / "reports" / "dialect_volume59_headers_removed_20260709.md"
REPORT_JSON = ROOT / "output" / "reports" / "dialect_volume59_headers_removed_20260709.json"
MEMORY = ROOT / "PROJECT_MEMORY.md"

START_RE = re.compile(r"^第五十九卷(?:\s*方言)?\s*$", re.M)
END_RE = re.compile(r"^第六十卷(?:\s*人物)?\s*$", re.M)
HEADER_RE = re.compile(
    r"^(?:第一章\s*方言差别|第二章\s*语音系统|第三章\s*同音字汇|第四章\s*方言词汇|第五章\s*语法特点|第章)"
    r"\s*·\s*\d{4}\s*·?\s*[:：]?\s*$"
)


def line_no(text: str, pos: int) -> int:
    return text.count("\n", 0, pos) + 1


def find_range(text: str) -> tuple[int, int]:
    candidates = []
    for start in START_RE.finditer(text):
        end = END_RE.search(text[start.end() :])
        if not end:
            continue
        s, e = start.start(), start.end() + end.start()
        volume = text[s:e]
        if "同音字汇" in volume and "语法特点" in volume:
            candidates.append((s, e))
    if not candidates:
        raise RuntimeError("Volume 59 body range not found")
    return candidates[-1]


def clean_file(path: Path) -> dict:
    original = path.read_text(encoding="utf-8", errors="ignore")
    start, end = find_range(original)
    prefix, volume, suffix = original[:start], original[start:end], original[end:]
    removed = []
    kept = []
    base_line = line_no(original, start)
    for offset, line in enumerate(volume.splitlines()):
        if HEADER_RE.match(line.strip()):
            removed.append({"line": base_line + offset, "text": line.strip()})
        else:
            kept.append(line)
    new_volume = "\n".join(kept)
    if volume.endswith("\n"):
        new_volume += "\n"
    changed = bool(removed)
    if changed:
        path.write_text(prefix + new_volume + suffix, encoding="utf-8")
    return {
        "path": str(path.relative_to(ROOT)),
        "changed": changed,
        "removed_count": len(removed),
        "removed": removed,
    }


def update_memory(results: list[dict]) -> None:
    total = sum(r["removed_count"] for r in results)
    entry = f"""

## 2026-07-09 第五十九卷方言页眉残留清理

- 范围：仅限 `第五十九卷 方言` 至 `第六十卷 人物` 之间。
- 动作：删除可证页眉残留行，如 `第三章 同音字汇·2589·`、`第四章 方言词汇·2597·`。
- 结果：共删除 {total} 行；详见 `output/reports/dialect_volume59_headers_removed_20260709.md`。
- 说明：本批不改音标、同音字、方言词条正文，只清理页眉噪声，为后续词汇块重建做准备。
"""
    text = MEMORY.read_text(encoding="utf-8", errors="ignore") if MEMORY.exists() else ""
    if "## 2026-07-09 第五十九卷方言页眉残留清理" not in text:
        MEMORY.write_text(text.rstrip() + entry + "\n", encoding="utf-8")


def main() -> None:
    results = [clean_file(path) for path in TARGETS]
    data = {"generated_at": datetime.now().strftime("%Y-%m-%d %H:%M"), "results": results}
    REPORT_JSON.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# 第五十九卷方言页眉残留清理报告",
        "",
        f"> 生成时间：{data['generated_at']}",
        "",
        "## 范围",
        "",
        "仅处理 `第五十九卷 方言` 至 `第六十卷 人物` 之间的页眉式残留，不改正文词条。",
        "",
        "## 结果",
        "",
        "| 文件 | 删除行数 |",
        "|---|---:|",
    ]
    for result in results:
        lines.append(f"| `{result['path']}` | {result['removed_count']} |")
    lines.extend(["", "## 删除明细", "", "| 文件 | 行号 | 文本 |", "|---|---:|---|"])
    for result in results:
        for row in result["removed"]:
            lines.append(f"| `{result['path']}` | {row['line']} | `{row['text']}` |")
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    update_memory(results)
    print("removed=" + str(sum(r["removed_count"] for r in results)))
    for result in results:
        print(f"{result['path']}: {result['removed_count']}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()
