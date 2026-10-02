# -*- coding: utf-8 -*-
"""批次3：上_1 全册共识 FLAG_A 目视核验后的 v2 修复（2026-10-02）

核验方式：双引擎（PaddleOCR+RapidOCR）一致读数 + 语义唯一（页图区已由两引擎高置信读出）。
逐条留痕，同时改 body_chapters_v2 与 output/final_reader/连云港市志_全书.html。
"""
import io
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = [
    ROOT / "workbench" / "body_chapters_v2" / "总述与大事记.md",
    ROOT / "workbench" / "body_chapters_v2" / "第二卷_建置区划.md",
    ROOT / "workbench" / "body_chapters_v2" / "第三卷_区县概况.md",
    ROOT / "output" / "final_reader" / "连云港市志_全书.html",
]

FIXES = [
    # (旧, 新, 依据)
    ("不淮盐商直接到灶户中购盐", "不准盐商直接到灶户中购盐",
     "p48 双引擎一致「不准」0.918；语义唯一"),
    ("正融和尚重修海州园林寺", "正融和尚重修海州圆林寺",
     "p50 paddle 1.000 / rapid 0.882 均读「圆林寺」"),
    ("国务院批淮江苏省人民政府", "国务院批准江苏省人民政府",
     "p106 双引擎一致「批准」"),
    ("国务院批淮江苏省政府", "国务院批准江苏省政府",
     "p216 双引擎一致「批准」"),
    ("开辟常年莱田6687亩", "开辟常年菜田6687亩",
     "p240 paddle 0.997 / rapid 0.910 均读「菜田」"),
    ("进行良种推广、蔬莱栽培等试验", "进行良种推广、蔬菜栽培等试验",
     "p242 paddle 0.996 / rapid 0.916 均读「蔬菜」"),
]

# 全书系统性同类错字（扫描发现，语义唯一，全库批量修）
GLOBAL_FIXES = [
    ("蔬莱", "蔬菜", "蔬莱=蔬菜 误印，全书扫描 14 处（中/下卷）"),
    ("批淮", "批准", "批淮=批准 误印，全书扫描 6 处"),
]


def main():
    apply = "--apply" in sys.argv
    all_fixes = FIXES + GLOBAL_FIXES
    targets = list(TARGETS) + [p for p in (ROOT / "workbench" / "body_chapters_v2").glob("*.md")
                               if p not in TARGETS]
    for fp in targets:
        if not fp.exists():
            continue
        t = io.open(fp, encoding="utf-8").read()
        n_total = 0
        for old, new, why in all_fixes:
            c = t.count(old)
            if c:
                print(f"{fp.name}: {old!r} -> {new!r} × {c}  ({why})")
                t = t.replace(old, new)
                n_total += c
        if apply and n_total:
            io.open(fp, "w", encoding="utf-8").write(t)
            print(f"  written {fp.name}（{n_total} 处）")
    print("dry-run" if not apply else "applied")


if __name__ == "__main__":
    main()
