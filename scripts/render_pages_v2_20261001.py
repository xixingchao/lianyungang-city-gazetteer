# -*- coding: utf-8 -*-
"""
批次3工具：按卷渲染原件 PDF 页图（可重启、按需范围）

用法:
  python render_pages_v2_20261001.py --part 上_1 --start 124 --end 212

输出: workbench/ocr_v2/pages/<part>/page_<NNNN>.png
锚号约定: 上册 part01 的 image_page == PDF 页码（已实测核对）
"""
import argparse
from pathlib import Path

import pypdfium2 as pdfium

ROOT = Path(__file__).resolve().parents[1]
PDF_BASE = Path(r"E:\codex_Learing\_archive_20260927\batch2\17_keeps\连云港志原件")
OUT_BASE = ROOT / "workbench" / "ocr_v2" / "pages"
DPI = 200

PDF_NAMES = {
    "上_1": "连云港志上_1.pdf", "上_2": "连云港志上_2.pdf", "上_3": "连云港志上_3.pdf",
    "中_1": "连云港志中_1.pdf", "中_2": "连云港志中_2.pdf",
    "下_1": "连云港志下_1.pdf", "下_2": "连云港志下_2.pdf",
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--part", required=True, choices=PDF_NAMES.keys())
    ap.add_argument("--start", type=int, required=True)
    ap.add_argument("--end", type=int, required=True)
    ap.add_argument("--dpi", type=int, default=DPI)
    args = ap.parse_args()

    pdf = PDF_BASE / PDF_NAMES[args.part]
    outdir = OUT_BASE / args.part
    outdir.mkdir(parents=True, exist_ok=True)

    doc = pdfium.PdfDocument(str(pdf))
    scale = args.dpi / 72.0
    done = skipped = 0
    for page_no in range(args.start, args.end + 1):
        out = outdir / f"page_{page_no:04d}.png"
        if out.exists() and out.stat().st_size > 10000:
            skipped += 1
            continue
        page = doc[page_no - 1]
        bmp = page.render(scale=scale)
        img = bmp.to_pil()
        img.save(out)
        done += 1
        page.close()
        if (done % 20) == 0:
            print(f"rendered {done} ...")
    doc.close()
    print(f"part={args.part} range={args.start}-{args.end} rendered={done} skipped={skipped} -> {outdir}")


if __name__ == "__main__":
    main()
