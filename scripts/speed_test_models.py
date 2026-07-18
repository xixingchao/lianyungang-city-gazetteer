"""Speed test: PP-OCRv6_small vs medium on one page"""
import sys, time, numpy as np
if sys.stdout.encoding != 'utf-8':
    sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf-8', buffering=1)

from pathlib import Path
from paddleocr import PaddleOCR

IMAGE = Path(r"e:\codex_Learing\09_project_东辛农场\连云港市志_workstation\workbench/conversion/page_images/上/part01/page_0050_180dpi.jpg")

import os
os.environ["PADDLE_PDX_DISABLE_MODEL_SOURCE_CHECK"] = "True"

for model_size in ["small", "medium"]:
    det_name = f"PP-OCRv6_{model_size}_det"
    rec_name = f"PP-OCRv6_{model_size}_rec"
    print(f"\n[Testing {model_size.upper()}] det={det_name}, rec={rec_name}")

    ocr = PaddleOCR(
        use_doc_orientation_classify=False,
        use_doc_unwarping=False,
        use_textline_orientation=False,
        text_detection_model_name=det_name,
        text_recognition_model_name=rec_name,
    )

    t0 = time.time()
    result = ocr.predict(str(IMAGE))
    elapsed = time.time() - t0

    res = result[0]
    texts = res["rec_texts"]
    scores = res["rec_scores"]
    conf = float(np.mean(scores))

    print(f"  Time: {elapsed:.1f}s, Lines: {len(texts)}, Avg Conf: {conf:.4f}")
    print(f"  First 3 lines: {texts[:3]}")
