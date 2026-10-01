# -*- coding: utf-8 -*-
"""
批次5工具：渲染第五十九卷方言 48 页页图（300 DPI，卷内页号命名）

卷内页 1-48 = 连云港志下_2.pdf 第 295-342 页（与 7-15 全新重做包 page_mapping.csv 一致）
输出: workbench/volume59/pages/page_001.png .. page_048.png
"""
from pathlib import Path

import pypdfium2 as pdfium

ROOT = Path(__file__).resolve().parents[1]
PDF = Path(r"E:\codex_Learing\_archive_20260927\batch2\17_keeps\连云港志原件\连云港志下_2.pdf")
OUT = ROOT / "workbench" / "volume59" / "pages"
START, END, DPI = 295, 342, 300


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    doc = pdfium.PdfDocument(str(PDF))
    scale = DPI / 72.0
    done = skipped = 0
    for pdf_page in range(START, END + 1):
        vol_page = pdf_page - START + 1
        out = OUT / f"page_{vol_page:03d}.png"
        if out.exists() and out.stat().st_size > 10000:
            skipped += 1
            continue
        page = doc[pdf_page - 1]
        bmp = page.render(scale=scale)
        bmp.to_pil().save(out)
        page.close()
        done += 1
        if done % 12 == 0:
            print(f"rendered {done}...", flush=True)
    doc.close()
    print(f"vol59 pages: rendered={done} skipped={skipped} -> {OUT}", flush=True)


if __name__ == "__main__":
    main()
