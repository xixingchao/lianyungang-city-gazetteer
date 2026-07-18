"""PaddleOCR 引擎适配 — 对上册903页用 PP-OCRv6 重新识别

基于现有 run_pdf_ocr.py 管道，新增 --engine paddleocr 选项。
输出与 RapidOCR 格式兼容（.txt + .json），存放于独立目录避免覆盖原结果。

用法:
  python scripts/run_paddleocr_up.py --dry-run          # 预览计划
  python scripts/run_paddleocr_up.py                     # 执行全量
  python scripts/run_paddleocr_up.py --start 1 --end 10  # 指定范围
  python scripts/run_paddleocr_up.py --limit 5            # 限制页数
"""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
WORKSTATION = ROOT / "连云港市志_workstation"

# 上册三个分册
UPPER_PARTS = [
    ("上", "part01", ROOT / "连云港志上_1.pdf", 300),
    ("上", "part02", ROOT / "连云港志上_2.pdf", 305),
    ("上", "part03", ROOT / "连云港志上_3.pdf", 298),
]


def parse_args():
    parser = argparse.ArgumentParser(description="PaddleOCR re-OCR for upper volume")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--start", type=int, default=1, help="1-based global page")
    parser.add_argument("--end", type=int, default=903, help="1-based global page (inclusive)")
    parser.add_argument("--limit", type=int, help="max pages")
    parser.add_argument("--force", action="store_true", help="overwrite existing outputs")
    parser.add_argument("--dpi", type=int, default=180)
    return parser.parse_args()


def global_to_part(global_page: int):
    """将全局页码(1-903)映射到(分册, 分册内页码)"""
    offset = 0
    for volume, part, pdf_path, total in UPPER_PARTS:
        if global_page <= offset + total:
            return volume, part, pdf_path, global_page - offset, total
        offset += total
    raise ValueError(f"Page {global_page} out of range (1-903)")


def output_paths(volume, part, page_num, dpi):
    """PaddleOCR 输出到独立目录 paddle_ocr/ 避免覆盖原 RapidOCR 结果"""
    base = WORKSTATION / "workbench" / "ocr" / "paddle_ocr" / volume / part
    page_id = f"page_{page_num:04d}"
    return {
        "image": WORKSTATION / "workbench/conversion/page_images" / volume / part / f"{page_id}_{dpi}dpi.jpg",
        "text": base / f"{page_id}.txt",
        "json": base / f"{page_id}.json",
    }


def init_paddleocr():
    from paddleocr import PaddleOCR
    import os
    os.environ["PADDLE_PDX_DISABLE_MODEL_SOURCE_CHECK"] = "True"
    return PaddleOCR(
        use_doc_orientation_classify=False,
        use_doc_unwarping=False,
        use_textline_orientation=False,
        text_detection_model_name="PP-OCRv6_small_det",
        text_recognition_model_name="PP-OCRv6_small_rec",
        lang="ch",
    )


def paddleocr_page(ocr, image_path: Path) -> tuple[str, list[dict], float]:
    """对单张页面图片执行 PaddleOCR 识别"""
    result = ocr.predict(str(image_path))
    res = result[0]

    texts = res["rec_texts"]
    scores = res["rec_scores"]
    polys = res.get("dt_polys", res.get("rec_polys", []))

    lines = []
    for i, (text, score) in enumerate(zip(texts, scores)):
        box = polys[i].tolist() if i < len(polys) else []
        lines.append({
            "text": text,
            "score": float(score),
            "box": box,
        })

    text = "\n".join(texts)
    avg_conf = float(np.mean(scores)) if len(scores) > 0 else 0.0
    return text, lines, avg_conf


def write_outputs(volume, part, page_num, total_pages, image_path, text_path, json_path,
                  text, lines, avg_conf, time_s, image_size):
    text_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.parent.mkdir(parents=True, exist_ok=True)

    label = f"连云港市志_{volume}_{part}"
    header = f"# {label} 第 {page_num}/{total_pages} 页\n\n"
    text_path.write_text(header + text.strip() + "\n", encoding="utf-8")

    payload = {
        "book": "连云港市志",
        "volume": volume,
        "part": part,
        "page": page_num,
        "total_pages": total_pages,
        "engine": "paddleocr_ppocrv6",
        "image": str(image_path),
        "image_size": image_size,
        "text_chars": len(text.strip()),
        "line_count": len(lines),
        "avg_confidence": round(avg_conf, 4),
        "time_s": round(time_s, 2),
        "lines": lines,
    }
    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def main():
    args = parse_args()
    ocr = None if args.dry_run else init_paddleocr()

    pages = list(range(args.start, args.end + 1))
    if args.limit:
        pages = pages[:args.limit]

    print(f"[PLAN] PaddleOCR (PP-OCRv6) re-OCR for upper volume")
    print(f"  Pages: {pages[0]}-{pages[-1]} ({len(pages)} total)")
    print(f"  Dry-run: {args.dry_run}")
    print(f"  Force: {args.force}")
    print()

    total_chars = 0
    total_time = 0.0
    success = 0
    skipped = 0

    for global_page in pages:
        volume, part, pdf_path, part_page, part_total = global_to_part(global_page)
        paths = output_paths(volume, part, part_page, args.dpi)

        if not paths["image"].exists():
            print(f"  [SKIP] p{global_page:04d}: image not found: {paths['image']}")
            continue

        if paths["text"].exists() and paths["json"].exists() and not args.force:
            print(f"  p{global_page:04d}: cached ({paths['text'].stat().st_size} bytes)")
            skipped += 1
            continue

        if args.dry_run:
            print(f"  p{global_page:04d}: would OCR ({volume}/{part} p{part_page}/{part_total})")
            continue

        try:
            with Image.open(paths["image"]) as img:
                image_size = list(img.size)

            t0 = time.time()
            text, lines, avg_conf = paddleocr_page(ocr, paths["image"])
            elapsed = time.time() - t0

            write_outputs(
                volume, part, part_page, part_total,
                paths["image"], paths["text"], paths["json"],
                text, lines, avg_conf, elapsed, image_size,
            )

            total_chars += len(text.strip())
            total_time += elapsed
            success += 1
            print(f"  p{global_page:04d}: OK  chars={len(text.strip())}, lines={len(lines)}, "
                  f"conf={avg_conf:.4f}, time={elapsed:.1f}s")
        except Exception as e:
            print(f"  p{global_page:04d}: FAILED  {type(e).__name__}: {e}")

    print()
    print(f"[DONE] Success: {success}, Skipped: {skipped}, Failed: {len(pages) - success - skipped}")
    if success:
        print(f"  Total chars: {total_chars}, Avg conf: N/A")
        print(f"  Total time: {total_time:.1f}s, Avg per page: {total_time/success:.1f}s")


if __name__ == "__main__":
    main()
