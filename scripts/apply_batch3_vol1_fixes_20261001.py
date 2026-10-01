# -*- coding: utf-8 -*-
"""
批次3-Pilot：第一卷经目视核验的错字修复（全部带出现次数断言，防误伤）

依据：output/reports/batch3/上_1_consensus.json + 页图目视核验
（page_0127/0138/0198/0200 已人工读图确认）。
"""
import io
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
V2 = ROOT / "workbench" / "body_chapters_v2" / "第一卷_自然环境.md"
REPORT = ROOT / "output" / "reports" / "progress"

# (旧, 新, 期望次数, 依据)
FIXES = [
    ("自浆化棕壤", "白浆化棕壤", 1, "FLAG_A+术语：白浆化棕壤为标准土壤名"),
    ("棟树", "楝树", 1, "FLAG_A：楝树正字"),
    ("预针鱼", "颚针鱼", 1, "FLAG_A+目视图p198：颚针鱼"),
    ("虹科赤鱼、尖嘴虹、燕子鱼", "魟科赤魟、尖嘴魟、燕子魟", 1, "目视图p198：魟科"),
    ("鮐", "鲐", None, "编码变体归一（次数不设限，报告中记录）"),
    ("鲂科短鳍红娘鱼", "鲂鮄科短鳍红娘鱼", 1, "目视图p198：鲂鮄科"),
    ("黄鞍鲸", "黄鮟鱇", 1, "目视图p198：鮟鱇科黄鮟鱇"),
    ("小刀蛭", "小刀蛏", 1, "目视图p200：竹蛏科小刀蛏"),
    ("起珑种植", "起垄种植", 1, "农艺术语：起垄（三方全误，语义确定）"),
    ("黄蟮（", "黄鳝（", 1, "FLAG_B：鳝正字"),
]

t = io.open(V2, encoding="utf-8").read()
applied = []
for old, new, expect, why in FIXES:
    c = t.count(old)
    if expect is not None and c != expect:
        applied.append({"old": old, "new": new, "found": c, "expected": expect,
                        "status": "SKIP(次数不符)"})
        continue
    t = t.replace(old, new)
    applied.append({"old": old, "new": new, "found": c, "why": why, "status": "APPLIED"})

io.open(V2, "w", encoding="utf-8", newline="\n").write(t)

lines = ["# 2026-10-01 批次3-Pilot：第一卷目视核验错字修复", "",
         "| 旧 | 新 | 次数 | 状态 | 依据 |", "|---|---|---:|---|---|"]
for a in applied:
    lines.append(f"| {a['old']} | {a['new']} | {a['found']} | {a['status']} | {a.get('why','')} |")
REPORT.mkdir(parents=True, exist_ok=True)
io.open(REPORT / "20261001_批次3Pilot_第一卷目视核验修复.md", "w", encoding="utf-8",
        newline="\n").write("\n".join(lines) + "\n")
print(json.dumps(applied, ensure_ascii=False, indent=1))
