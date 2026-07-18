# -*- coding: utf-8 -*-
"""Patch batch 86 replacement count in project memory."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MEMORY = ROOT / "PROJECT_MEMORY.md"
old = "- 本批证据短语 10 项，实际替换 3 处；报告：`output/reports/reader_paddle_backed_residues_batch86_20260706.md`。"
new = "- 本批证据短语 10 项，首跑替换 16 处，续补源稿/汇总断行残留 3 处，累计替换 19 处；报告：`output/reports/reader_paddle_backed_residues_batch86_20260706.md`。"
text = MEMORY.read_text(encoding="utf-8")
if old not in text:
    raise SystemExit("target line not found")
MEMORY.write_text(text.replace(old, new, 1), encoding="utf-8")
print("memory_batch86_count_patched")
