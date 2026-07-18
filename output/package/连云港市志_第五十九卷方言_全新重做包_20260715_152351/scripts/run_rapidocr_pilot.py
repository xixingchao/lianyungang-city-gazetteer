from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

from rapidocr_onnxruntime import RapidOCR

ROOT = Path(__file__).resolve().parents[1]
MAPPING_CSV = ROOT / "input" / "source" / "page_mapping.csv"
OCR_DIR = ROOT / "workbench" / "ocr" / "rapidocr"
REPORT_DIR = ROOT / "output" / "reports"
PILOT_PAGES = set(range(1, 7))


def read_mapping() -> list[dict[str, str]]:
    with MAPPING_CSV.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def normalize(result: Any) -> list[dict[str, Any]]:
    lines: list[dict[str, Any]] = []
    if not result:
        return lines
    if isinstance(result, tuple):
        result = result[0]
    for item in result or []:
        if not item or len(item) < 2:
            continue
        box = item[0]
        text = item[1]
        score = item[2] if len(item) > 2 else None
        lines.append({"text": text, "score": score, "box": box})
    return lines


def main() -> None:
    OCR_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    rows = [row for row in read_mapping() if int(row["volume_page"]) in PILOT_PAGES]
    engine = RapidOCR()
    report_rows = []
    for row in rows:
        volume_page = int(row["volume_page"])
        source_pdf_page = int(row["source_pdf_page"])
        image_path = Path(row["cropped_image"])
        result, elapsed = engine(str(image_path))
        lines = normalize(result)
        page_id = f"page_{source_pdf_page:04d}_vol_{volume_page:03d}"
        json_path = OCR_DIR / f"{page_id}_rapidocr.json"
        txt_path = OCR_DIR / f"{page_id}_rapidocr.txt"
        json_path.write_text(json.dumps({"source": str(image_path), "elapsed": elapsed, "lines": lines}, ensure_ascii=False, indent=2), encoding="utf-8")
        txt_path.write_text("\n".join(line["text"] for line in lines), encoding="utf-8")
        scores = [float(line["score"]) for line in lines if line.get("score") is not None]
        avg = sum(scores) / len(scores) if scores else 0.0
        report_rows.append({
            "volume_page": volume_page,
            "source_pdf_page": source_pdf_page,
            "line_count": len(lines),
            "avg_score": f"{avg:.4f}",
            "elapsed": str(elapsed),
            "txt_path": str(txt_path),
        })
        print(f"page={volume_page} pdf={source_pdf_page} lines={len(lines)} avg={avg:.4f} elapsed={elapsed}")

    if report_rows:
        out_csv = REPORT_DIR / "rapidocr_pilot_report.csv"
        with out_csv.open("w", encoding="utf-8-sig", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=list(report_rows[0].keys()))
            writer.writeheader()
            writer.writerows(report_rows)
        out_md = REPORT_DIR / "rapidocr_pilot_report.md"
        out_md.write_text(
            "# 第59卷 RapidOCR Pilot 报告\n\n"
            "说明：本报告由 fresh 项目页图直接生成，未使用旧 OCR。\n\n"
            "| 卷内页 | PDF页 | 行数 | 平均置信度 | 耗时 | 文本 |\n"
            "|---:|---:|---:|---:|---|---|\n"
            + "\n".join(
                f"| {r['volume_page']} | {r['source_pdf_page']} | {r['line_count']} | {r['avg_score']} | {r['elapsed']} | `{r['txt_path']}` |"
                for r in report_rows
            )
            + "\n",
            encoding="utf-8",
        )
        print(f"report={out_md}")


if __name__ == "__main__":
    main()
