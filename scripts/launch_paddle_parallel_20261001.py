# -*- coding: utf-8 -*-
"""并行加速：起 3 个 paddle OCR worker（IDLE 优先级，2 线程/个），与原有 worker 并行。
分片互不重叠；已跑过的页自动跳过（可重启）。日志写 workbench/ocr_v2/logs/。"""
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IDLE_PRIORITY_CLASS = 0x00000040

env = dict(os.environ)
env["OMP_NUM_THREADS"] = "2"
env["MKL_NUM_THREADS"] = "2"

JOBS = [
    ("上_1", 250, 300, 0),
    ("上_2", 1, 305, 300),
    ("上_3", 1, 298, 605),
]

logdir = ROOT / "workbench" / "ocr_v2" / "logs"
logdir.mkdir(parents=True, exist_ok=True)

for part, a, b, off in JOBS:
    log = open(logdir / ("paddle_%s_%d_%d.log" % (part, a, b)), "w", encoding="utf-8")
    p = subprocess.Popen(
        [sys.executable, "-X", "utf8", "scripts/run_dual_ocr_v2_20261001.py",
         "--part", part, "--engine", "paddle", "--start", str(a), "--end", str(b), "--offset", str(off)],
        cwd=str(ROOT), env=env, creationflags=IDLE_PRIORITY_CLASS,
        stdout=log, stderr=subprocess.STDOUT)
    print("launched", part, a, b, "pid", p.pid, flush=True)
print("done")
