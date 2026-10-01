# -*- coding: utf-8 -*-
"""
上册三册 OCR 流水线（空闲优先级版）

- 进程自身 + 全部子进程降为 IDLE_PRIORITY_CLASS：打游戏时自动让路，
  机器空闲时全速跑
- 子步骤与直接跑等价（断点可续：渲染/OCR 均跳过已有产物）
"""
import ctypes
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IDLE_PRIORITY = 0x00000040

handle = ctypes.windll.kernel32.GetCurrentProcess()
ctypes.windll.kernel32.SetPriorityClass(handle, IDLE_PRIORITY)

# 限制线程数留出余量（与空闲优先级叠加，双保险）
env = dict(os.environ)
env.setdefault("OMP_NUM_THREADS", "3")
env.setdefault("MKL_NUM_THREADS", "3")

STEPS = [
    # 渲染
    ["scripts/render_pages_v2_20261001.py", "--part", "上_1", "--start", "1", "--end", "300", "--offset", "0"],
    ["scripts/render_pages_v2_20261001.py", "--part", "上_2", "--start", "1", "--end", "305", "--offset", "300"],
    ["scripts/render_pages_v2_20261001.py", "--part", "上_3", "--start", "1", "--end", "298", "--offset", "605"],
    # RapidOCR（快，先出全量）
    ["scripts/run_dual_ocr_v2_20261001.py", "--part", "上_1", "--engine", "rapid", "--start", "1", "--end", "300", "--offset", "0"],
    ["scripts/run_dual_ocr_v2_20261001.py", "--part", "上_2", "--engine", "rapid", "--start", "1", "--end", "305", "--offset", "300"],
    ["scripts/run_dual_ocr_v2_20261001.py", "--part", "上_3", "--engine", "rapid", "--start", "1", "--end", "298", "--offset", "605"],
    # PaddleOCR（慢，大头）
    ["scripts/run_dual_ocr_v2_20261001.py", "--part", "上_1", "--engine", "paddle", "--start", "1", "--end", "300", "--offset", "0"],
    ["scripts/run_dual_ocr_v2_20261001.py", "--part", "上_2", "--engine", "paddle", "--start", "1", "--end", "305", "--offset", "300"],
    ["scripts/run_dual_ocr_v2_20261001.py", "--part", "上_3", "--engine", "paddle", "--start", "1", "--end", "298", "--offset", "605"],
]


def main():
    for i, step in enumerate(STEPS, 1):
        script = step[0]
        print(f"[pipeline] ({i}/{len(STEPS)}) {script} {' '.join(step[1:])}", flush=True)
        r = subprocess.run([sys.executable, "-X", "utf8", str(ROOT / step[0])] + step[1:],
                           cwd=str(ROOT), env=env)
        if r.returncode != 0:
            print(f"[pipeline] STEP FAILED rc={r.returncode}: {step}", flush=True)
            sys.exit(r.returncode)
    print("PIPELINE_ALL_DONE", flush=True)


if __name__ == "__main__":
    main()
