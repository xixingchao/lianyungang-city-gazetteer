# -*- coding: utf-8 -*-
"""
v2 字符规范化（可重复执行）：完成 7-06 阅读版只覆盖中下册的字符修复
- 馀 → 余（异体字规范化；阅读版 yu 修复漏了上册）
- %o → ‰（千分号 OCR 误识）
- 标淮 → 标准（高置信双字纠错）
替换留痕到 output/reports/progress/。
"""
import io
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
V2 = ROOT / "workbench" / "body_chapters_v2"
REPORT = ROOT / "output" / "reports" / "progress"

RULES = [("馀", "余"), ("%o", "‰"), ("标淮", "标准")]

total = Counter()
for p in sorted(V2.glob("*.md")):
    t = io.open(p, encoding="utf-8").read()
    counts = Counter()
    for old, new in RULES:
        c = t.count(old)
        if c:
            t = t.replace(old, new)
            counts[f"{old}->{new}"] += c
    if counts:
        io.open(p, "w", encoding="utf-8", newline="\n").write(t)
        total += counts

lines = ["# v2 字符规范化（馀→余 / %o→‰ / 标淮→标准）", "", f"- 合计：{dict(total)}"]
REPORT.mkdir(parents=True, exist_ok=True)
io.open(REPORT / "20261001_v2字符规范化.md", "w", encoding="utf-8", newline="\n").write(
    "\n".join(lines) + "\n")
print(dict(total))
