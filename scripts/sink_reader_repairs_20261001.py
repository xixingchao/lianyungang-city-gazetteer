# -*- coding: utf-8 -*-
"""
重启批次1(2)：把 7-06 阅读版已做的全局字符规范化沉回重排源文件

依据 assess_text_identity 的差异清单，规则为高置信全局替换：
- 馀 → 余（异体字规范化，阅读版 batch1-6 yu 修复）
- %o → ‰（千分号 OCR 误识）
- 标淮 → 标准（高置信双字纠错；淮 单字合法不动）
- 纯拉丁垃圾串（连续≥5 个 a/b 的 OCR 噪声）→ 删除
其余差异（真实改写、表格嵌回）不在本批处理，留批次2。

替换全部计数留痕，输出到 output/reports/progress/。
"""
import io
import re
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "workbench" / "body_chapters_reflowed"

RULES = [
    ("馀", "余"),
    ("%o", "‰"),
    ("标淮", "标准"),
]
JUNK = re.compile(r"(?<![\u4e00-\u9fffA-Za-z])[abAB]{5,}(?![\u4e00-\u9fffA-Za-z])")

total = Counter()
per_file = []
for p in sorted(SRC.rglob("*.md")):
    t = io.open(p, encoding="utf-8").read()
    counts = Counter()
    for old, new in RULES:
        c = t.count(old)
        if c:
            t = t.replace(old, new)
            counts[f"{old}->{new}"] = c
            total[f"{old}->{new}"] += c
    junk = JUNK.findall(t)
    if junk:
        t = JUNK.sub("", t)
        counts["junk_removed"] = len(junk)
        total["junk_removed"] += len(junk)
    if sum(counts.values()):
        io.open(p, "w", encoding="utf-8", newline="\n").write(t)
        per_file.append((p.name, dict(counts)))

lines = ["# 2026-10-01 批次1(2)：阅读版字符规范化沉回重排源", "",
         "| 文件 | 替换 | 次数 |", "|---|---|---:|"]
for name, counts in per_file:
    for k, v in counts.items():
        lines.append(f"| {name} | {k} | {v} |")
lines += ["", f"## 合计", ""]
for k, v in total.most_common():
    lines.append(f"- {k}: {v}")

out = ROOT / "output" / "reports" / "progress" / "20261001_批次1之2_字符规范化沉回.md"
io.open(out, "w", encoding="utf-8", newline="\n").write("\n".join(lines) + "\n")
print(json.dumps(dict(total), ensure_ascii=False, indent=1))
print("files changed:", len(per_file))
