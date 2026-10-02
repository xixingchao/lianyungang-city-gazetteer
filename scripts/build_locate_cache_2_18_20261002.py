# -*- coding: utf-8 -*-
"""vol59 字汇/音系页（2-18）RapidOCR 带坐标缓存（用于批量裁图裁定）

输出: workbench/volume59/locate_ocr/page_0XX.json
"""
import json
import sys
from pathlib import Path

import cv2
import numpy as np

BASE = Path(r"E:\codex_Learing\project_连云港市志\repo\workbench\volume59")
OUT = BASE / "locate_ocr"
OUT.mkdir(exist_ok=True)


def main():
    from rapidocr_onnxruntime import RapidOCR
    eng = RapidOCR()
    for pno in range(2, 19):
        out = OUT / f"page_{pno:03d}.json"
        if out.exists() and out.stat().st_size > 200:
            print(f"p{pno} cached", flush=True)
            continue
        data = np.fromfile(str(BASE / "pages" / f"page_{pno:03d}.png"), dtype=np.uint8)
        img = cv2.imdecode(data, cv2.IMREAD_COLOR)
        res, _ = eng(img)
        lines = []
        if res:
            for box, text, score in res:
                xs = [p[0] for p in box]
                ys = [p[1] for p in box]
                lines.append({"x0": int(min(xs)), "y0": int(min(ys)),
                              "x1": int(max(xs)), "y1": int(max(ys)),
                              "text": text, "score": float(score)})
        out.write_text(json.dumps({"page": pno, "lines": lines}, ensure_ascii=False),
                       encoding="utf-8")
        print(f"p{pno} {len(lines)} lines", flush=True)


if __name__ == "__main__":
    main()
