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


def write_page(row: dict[str, str], engine: RapidOCR) -> dict[str, str | int | float]:
    volume_page = int(row["volume_page"])
    source_pdf_page = int(row["source_pdf_page"])
    image_path = Path(row["cropped_image"])
    page_id = f"page_{source_pdf_page:04d}_vol_{volume_page:03d}"
    json_path = OCR_DIR / f"{page_id}_rapidocr.json"
    txt_path = OCR_DIR / f"{page_id}_rapidocr.txt"

    if json_path.exists() and txt_path.exists():
        data = json.loads(json_path.read_text(encoding="utf-8"))
        lines = data.get("lines", [])
        scores = [float(line["score"]) for line in lines if line.get("score") is not None]
        avg = sum(scores) / len(scores) if scores else 0.0
        return {
            "volume_page": volume_page,
            "source_pdf_page": source_pdf_page,
            "line_count": len(lines),
            "avg_score": avg,
            "status": "existing",
            "txt_path": str(txt_path),
            "json_path": str(json_path),
        }

    result, elapsed = engine(str(image_path))
    lines = normalize(result)
    json_path.write_text(
        json.dumps({"source": str(image_path), "elapsed": elapsed, "lines": lines}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    txt_path.write_text("\n".join(line["text"] for line in lines), encoding="utf-8")
    scores = [float(line["score"]) for line in lines if line.get("score") is not None]
    avg = sum(scores) / len(scores) if scores else 0.0
    return {
        "volume_page": volume_page,
        "source_pdf_page": source_pdf_page,
        "line_count": len(lines),
        "avg_score": avg,
        "status": "new",
        "txt_path": str(txt_path),
        "json_path": str(json_path),
    }


def risk_note(avg_score: float, volume_page: int) -> str:
    if avg_score < 0.72:
        return "high_ocr_risk"
    if 2 <= volume_page <= 42:
        return "dialect_layout_risk"
    return "review_required"


def main() -> None:
    OCR_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    rows = read_mapping()
    engine = RapidOCR()
    report_rows = []
    for row in rows:
        record = write_page(row, engine)
        avg = float(record["avg_score"])
        record["risk_note"] = risk_note(avg, int(record["volume_page"]))
        report_rows.append(record)
        print(
            f"page={record['volume_page']} pdf={record['source_pdf_page']} "
            f"lines={record['line_count']} avg={avg:.4f} status={record['status']} risk={record['risk_note']}"
        )

    out_csv = REPORT_DIR / "rapidocr_full_report.csv"
    fields = ["volume_page", "source_pdf_page", "line_count", "avg_score", "status", "risk_note", "txt_path", "json_path"]
    with out_csv.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(report_rows)

    out_md = REPORT_DIR / "rapidocr_full_report.md"
    lines = [
        "# 第59卷全卷 RapidOCR 报告",
        "",
        "说明：本报告由 fresh 项目页图直接生成，未使用旧 OCR。RapidOCR 输出仅作线索，音标/表格/同音字汇需人工或结构化处理。",
        "",
        "| 卷内页 | PDF页 | 行数 | 平均置信度 | 状态 | 风险 | 文本 |",
        "|---:|---:|---:|---:|---|---|---|",
    ]
    for r in report_rows:
        lines.append(
            f"| {r['volume_page']} | {r['source_pdf_page']} | {r['line_count']} | {float(r['avg_score']):.4f} | "
            f"{r['status']} | {r['risk_note']} | `{r['txt_path']}` |"
        )
    out_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"report={out_md}")


if __name__ == "__main__":
    main()
