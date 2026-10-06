# -*- coding: utf-8 -*-
"""Detect ruled-table pages in the 中/下 volumes and check them against the table library.

Method: render each page small, binarize, count long horizontal/vertical dark runs
(table rules). Ruled-table pages are then matched against the page numbers recorded
in the structured-table library (under the known page-number conventions).
"""
from __future__ import annotations

import glob
import json
import sys
from pathlib import Path

import fitz
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
SRC = Path(r"E:\codex_Learing\_archive_20260927\batch2\17_keeps\连云港志原件")
PARTS = [
    ("连云港志中_1.pdf", 124, "中"),   # 印刷 = idx + 103 + 21? -> calibrated below
    ("连云港志中_2.pdf", 124, "中"),
    ("连云港志下_1.pdf", 136, "下"),
    ("连云港志下_2.pdf", 148, "下"),
]
# 印刷 = idx + PRINT_OFF[file]
PRINT_OFF = {
    "连云港志中_1.pdf": 803,   # placeholder, calibrated at runtime
    "连云港志中_2.pdf": 1303,
    "连云港志下_1.pdf": 1838,
    "连云港志下_2.pdf": 2285,
}
ANCHOR_OFF = {"中": (103, 119), "下": (136, 148)}  # 锚偏移(印刷→锚) 两个册


def load_library_pages() -> dict[str, set[int]]:
    """printed-page -> {table_id} using page/pages fields under both conventions."""
    by_part = {"中": set(), "下": set(), "上": set()}
    for f in glob.glob(str(ROOT / "workbench" / "table_entries" / "*" / "data" / "*.json")):
        try:
            d = json.loads(Path(f).read_text(encoding="utf-8"))
        except Exception:
            continue
        part = d.get("table_id", "").split("-")[1]
        vals = set()
        for key in ("page", "pages"):
            v = d.get(key)
            if isinstance(v, int):
                vals.add(v)
            elif isinstance(v, list):
                vals.update(x for x in v if isinstance(x, int))
        by_part.setdefault(part, set()).update(vals)
    return by_part


def analyze(page) -> tuple[int, int]:
    pix = page.get_pixmap(dpi=72, colorspace=fitz.csGRAY)
    arr = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width)
    dark = arr < 150
    # 横线：每行找最长连续暗段
    h_count = 0
    for row in dark:
        idx = np.flatnonzero(row)
        if idx.size == 0:
            continue
        runs = np.split(idx, np.flatnonzero(np.diff(idx) > 2) + 1)
        longest = max(len(r) for r in runs)
        if longest >= pix.width * 0.45:
            h_count += 1
    darkT = dark.T
    v_count = 0
    for col in darkT:
        idx = np.flatnonzero(col)
        if idx.size == 0:
            continue
        runs = np.split(idx, np.flatnonzero(np.diff(idx) > 2) + 1)
        longest = max(len(r) for r in runs)
        if longest >= pix.height * 0.18:
            v_count += 1
    return h_count, v_count


def main() -> None:
    lib = load_library_pages()
    print("库中登记页数:", {k: len(v) for k, v in lib.items()})
    out = []
    for fname, _off, part in PARTS:
        path = SRC / fname
        doc = fitz.open(str(path))
        off = PRINT_OFF[fname]
        for idx in range(len(doc)):
            printed = idx + off
            h, v = analyze(doc[idx])
            if h >= 4 and v >= 3:
                # 该印刷页是否已被某表登记
                found = False
                for cand in (printed, printed + ANCHOR_OFF["中"][0], printed + ANCHOR_OFF["中"][1],
                             printed + ANCHOR_OFF["下"][0], printed + ANCHOR_OFF["下"][1]):
                    if cand in lib.get(part, set()):
                        found = True
                        break
                out.append((fname, idx, printed, h, v, found))
        doc.close()
        print(f"{fname} 扫描完成，累计表格样页 {len(out)}", flush=True)
    Path(ROOT / "output" / "reports" / "表格线扫描_20261006.tsv").write_text(
        "file\tidx\tprinted\th_lines\tv_lines\tin_library\n"
        + "\n".join("%s\t%d\t%d\t%d\t%d\t%s" % (a, b, c, h, v, found) for a, b, c, h, v, found in out),
        encoding="utf-8",
    )
    miss = [r for r in out if not r[5]]
    print("总表格样页:", len(out), "| 未在库登记:", len(miss))
    for r in miss[:80]:
        print("   MISS", r)


if __name__ == "__main__":
    main()
