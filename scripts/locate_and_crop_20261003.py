# -*- coding: utf-8 -*-
"""通读定位工具：给「书页号 + 待核字符串」，渲染该页 300dpi 并裁出目标行（2026-10-03）。

原理：v2 里每个页锚（<!-- page-anchor: LYG-XXXX -->）标出该页起点；
该页内的字符偏移 ÷ 每行字数 ≈ 行号，再按页高换算 y 坐标裁切。
定位只是**估算**，裁出来先看一眼，不中就把 --dy 微调。

用法：
  python locate_and_crop_20261003.py 1818 "如火如茶"
  python locate_and_crop_20261003.py 1583 "磨菇" --dy -60
"""
from __future__ import annotations

import argparse
import io
import glob
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
V2 = ROOT / "workbench" / "body_chapters_v2"
ORIG = Path(r"E:\codex_Learing\_archive_20260927\batch2\17_keeps\连云港志原件")
OUT = Path(r"C:\Users\52744\_scratch\readthrough")
OUT.mkdir(parents=True, exist_ok=True)

# 绝对页 → PDF 分卷与卷内起始页
PARTS = [
    ("连云港志上_1.pdf", 1, 300), ("连云港志上_2.pdf", 301, 605), ("连云港志上_3.pdf", 606, 903),
    ("连云港志中_1.pdf", 904, 1420), ("连云港志中_2.pdf", 1421, 1971),
    ("连云港志下_1.pdf", 1972, 2432), ("连云港志下_2.pdf", 2433, 2911),
]
ANCH = re.compile(r"<!--\s*page-anchor:\s*LYG-(?:S-)?(\d+)\s*-->")


def pdf_of(page: int) -> tuple[str, int]:
    for name, a, b in PARTS:
        if a <= page <= b:
            return name, page - a + 1
    raise SystemExit(f"页 {page} 不在任何分卷范围")


def locate_in_v2(page: int, needle: str) -> tuple[str, int, int]:
    """返回 (命中文件, 行号, 该页内字符偏移)。"""
    for f in sorted(glob.glob(str(V2 / "*.md"))):
        t = io.open(f, encoding="utf-8").read()
        pos = t.find(needle)
        if pos < 0:
            continue
        # 向前找最近的页锚，取其页号
        best = None
        for m in ANCH.finditer(t, 0, pos):
            best = (int(m.group(1)), m.end())
        if not best:
            continue
        anchor_page, anchor_end = best
        if anchor_page != page:
            # 命中页与锚不符时仍报告，方便人工判断
            print(f"注意：字符串在 {Path(f).name} 中最近锚为 {anchor_page}，与请求的 {page} 不一致", file=sys.stderr)
        offset = pos - anchor_end
        ln = t.count("\n", 0, pos) + 1
        return Path(f).name, ln, offset
    raise SystemExit(f"v2 中未找到：{needle}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("page", type=int)
    ap.add_argument("needle")
    ap.add_argument("--chars-per-line", type=int, default=44)
    ap.add_argument("--dy", type=int, default=0, help="微调像素（负=上移）")
    ap.add_argument("--band", type=int, default=90, help="裁切半高")
    args = ap.parse_args()

    fname, ln, offset = locate_in_v2(args.page, args.needle)
    line_no = offset / args.chars_per_line
    pdf, local = pdf_of(args.page)
    import fitz
    from PIL import Image
    doc = fitz.open(os.path.join(str(ORIG), pdf))
    pix = doc[local - 1].get_pixmap(dpi=300)
    img_path = OUT / f"p{args.page}_300.png"
    pix.save(str(img_path))
    doc.close()
    step = (3508 - 320) / 39.0
    y = 320 + line_no * step + args.dy
    im = Image.open(str(img_path))
    band = im.crop((200, max(0, int(y) - args.band), 2340, min(im.height, int(y) + args.band)))
    out = OUT / f"crop_p{args.page}.png"
    band.save(str(out))
    print(f"{fname} L{ln} 偏移 {offset} → 估行 {line_no:.1f} y≈{int(y)}  → {out}")


if __name__ == "__main__":
    main()
