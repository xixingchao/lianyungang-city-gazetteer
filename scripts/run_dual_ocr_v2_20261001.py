# -*- coding: utf-8 -*-
"""
批次3工具：双引擎 OCR 跑批（可重启：按页 JSON，跑过跳过）

用法:
  python run_dual_ocr_v2_20261001.py --part 上_1 --engine paddle --start 124 --end 212
  python run_dual_ocr_v2_20261001.py --part 上_1 --engine rapid  --start 124 --end 212

输出: workbench/ocr_v2/ocr/<engine>/<part>/page_<NNNN>.json
      {page, lines: [{text, score}]}
中文路径规避: np.fromfile + cv2.imdecode 读图，引擎吃 ndarray，不走 cv2.imread。
"""
import argparse
import json
import sys
from pathlib import Path

import cv2
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
PAGES_BASE = ROOT / "workbench" / "ocr_v2" / "pages"
OCR_BASE = ROOT / "workbench" / "ocr_v2" / "ocr"


def imread_cn(path: Path) -> np.ndarray:
    data = np.fromfile(str(path), dtype=np.uint8)
    img = cv2.imdecode(data, cv2.IMREAD_COLOR)
    if img is None:
        raise RuntimeError(f"cannot decode {path}")
    return img


def run_paddle(pages, outdir):
    from paddleocr import PaddleOCR
    ocr = PaddleOCR(
        lang="ch",
        use_doc_orientation_classify=False,
        use_doc_unwarping=False,
        use_textline_orientation=False,
    )
    for p in pages:
        out = outdir / f"page_{p.no:04d}.json"
        if out.exists() and out.stat().st_size > 100:
            continue
        img = imread_cn(p.img_path)
        result = ocr.predict(img)
        lines = []
        for res in result:
            data = res.json["res"] if hasattr(res, "json") else res
            texts = data.get("rec_texts", [])
            scores = data.get("rec_scores", [])
            for t, s in zip(texts, scores):
                lines.append({"text": t, "score": float(s)})
        out.write_text(json.dumps({"page": p.no, "lines": lines}, ensure_ascii=False),
                       encoding="utf-8")
        print(f"paddle page {p.no}: {len(lines)} lines", flush=True)


def run_rapid(pages, outdir):
    from rapidocr_onnxruntime import RapidOCR
    engine = RapidOCR()
    for p in pages:
        out = outdir / f"page_{p.no:04d}.json"
        if out.exists() and out.stat().st_size > 100:
            continue
        img = imread_cn(p.img_path)
        result, _elapse = engine(img)
        lines = []
        if result:
            for box, text, score in result:
                lines.append({"text": text, "score": float(score)})
        out.write_text(json.dumps({"page": p.no, "lines": lines}, ensure_ascii=False),
                       encoding="utf-8")
        print(f"rapid page {p.no}: {len(lines)} lines", flush=True)


class PageRef:
    def __init__(self, no, path):
        self.no = no
        self.img_path = path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--part", required=True)
    ap.add_argument("--engine", required=True, choices=["paddle", "rapid"])
    ap.add_argument("--start", type=int, required=True)
    ap.add_argument("--end", type=int, required=True)
    args = ap.parse_args()

    pages_dir = PAGES_BASE / args.part
    outdir = OCR_BASE / args.engine / args.part
    outdir.mkdir(parents=True, exist_ok=True)
    pages = [PageRef(n, pages_dir / f"page_{n:04d}.png")
             for n in range(args.start, args.end + 1)
             if (pages_dir / f"page_{n:04d}.png").exists()]
    print(f"{args.engine}: {len(pages)} pages, out -> {outdir}", flush=True)

    if args.engine == "paddle":
        run_paddle(pages, outdir)
    else:
        run_rapid(pages, outdir)
    print("DONE", flush=True)


if __name__ == "__main__":
    main()
