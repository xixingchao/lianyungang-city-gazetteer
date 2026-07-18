# -*- coding: utf-8 -*-
"""Remove reader-visible internal notes from restored volume 5 tables."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
PROGRESS_PATH = ROOT / "output" / "reports" / "progress" / "20260629_第二批_第五卷已核表恢复.md"
MEMORY_PATH = ROOT / "PROJECT_MEMORY.md"

NOTES = [
    "\n<p>注：已精修，对照原图确认</p>",
    "\n<p>注：表格分两栏排列，数据待核对</p>",
]


def main() -> None:
    text = HTML_PATH.read_text(encoding="utf-8")
    counts = {note: text.count(note) for note in NOTES}
    fixed = text
    for note in NOTES:
        fixed = fixed.replace(note, "")
    if fixed != text:
        HTML_PATH.write_text(fixed, encoding="utf-8")

    progress = PROGRESS_PATH.read_text(encoding="utf-8")
    line = "- 已清除恢复表后随带的内部 notes 段落，避免工作说明暴露在主阅读版。"
    if line not in progress:
        progress = progress.replace("## 下一步计划", f"{line}\n\n## 下一步计划")
        PROGRESS_PATH.write_text(progress, encoding="utf-8")

    memory = MEMORY_PATH.read_text(encoding="utf-8")
    mem_line = "- 已补清第五卷恢复表后随带的内部 notes 段落，保持主阅读版不显示工作说明。"
    marker = "## 2026-06-29 第二批第五卷已核表恢复"
    if marker in memory and mem_line not in memory:
        idx = memory.find(marker)
        next_idx = memory.find("\n## ", idx + 1)
        if next_idx == -1:
            next_idx = len(memory)
        section = memory[idx:next_idx].rstrip() + "\n" + mem_line + "\n"
        memory = memory[:idx] + section + memory[next_idx:]
        MEMORY_PATH.write_text(memory, encoding="utf-8")

    print("removed internal notes")
    for note, count in counts.items():
        print(f"- {note.strip()}: {count}")


if __name__ == "__main__":
    main()
