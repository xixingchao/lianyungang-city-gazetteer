from __future__ import annotations

import csv
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAPPING_CSV = ROOT / "input" / "source" / "page_mapping.csv"
OCR_DIR = ROOT / "workbench" / "ocr" / "rapidocr"
OUTPUT_READER = ROOT / "output" / "reader"
REPORT_DIR = ROOT / "output" / "reports"


def read_mapping() -> list[dict[str, str]]:
    with MAPPING_CSV.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def read_ocr(source_pdf_page: int, volume_page: int) -> tuple[str, int, float]:
    page_id = f"page_{source_pdf_page:04d}_vol_{volume_page:03d}"
    txt_path = OCR_DIR / f"{page_id}_rapidocr.txt"
    json_path = OCR_DIR / f"{page_id}_rapidocr.json"
    text = txt_path.read_text(encoding="utf-8") if txt_path.exists() else ""
    avg = 0.0
    line_count = 0
    if json_path.exists():
        data = json.loads(json_path.read_text(encoding="utf-8"))
        lines = data.get("lines", [])
        line_count = len(lines)
        scores = [float(line["score"]) for line in lines if line.get("score") is not None]
        avg = sum(scores) / len(scores) if scores else 0.0
    return text, line_count, avg


def main() -> None:
    OUTPUT_READER.mkdir(parents=True, exist_ok=True)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    rows = read_mapping()
    md_lines = [
        "# 连云港市志 第五十九卷《方言》全新 OCR 草稿",
        "",
        "> 说明：本稿由原件重新抽页后运行 RapidOCR 生成，只作为人工校对线索；不得作为最终文字交付。音标、表格、同音字汇、方言词汇必须回看页图并结构化/双审。",
        "",
    ]
    html_parts = [
        "<!doctype html><html lang=\"zh-CN\"><head><meta charset=\"utf-8\">",
        "<title>连云港市志 第五十九卷 方言 全新OCR草稿</title>",
        "<style>body{font-family:SimSun,'Noto Serif SC',serif;line-height:1.7;margin:32px auto;max-width:980px;color:#191919}pre{white-space:pre-wrap;border-left:3px solid #999;padding-left:12px} .warn{background:#fff3cd;padding:12px;border:1px solid #e6c96d}</style>",
        "</head><body><h1>连云港市志 第五十九卷《方言》全新 OCR 草稿</h1>",
        "<p class=\"warn\">本稿仅供人工校对使用，不是最终交付文本。音标、表格、同音字汇、方言词汇必须回看页图并双审。</p>",
    ]
    summary_rows = []
    for row in rows:
        volume_page = int(row["volume_page"])
        source_pdf_page = int(row["source_pdf_page"])
        text, line_count, avg = read_ocr(source_pdf_page, volume_page)
        original_rel = Path(row["original_image"]).relative_to(ROOT).as_posix()
        cropped_rel = Path(row["cropped_image"]).relative_to(ROOT).as_posix()
        risk = "高风险" if avg < 0.72 or volume_page <= 45 else "待复核"
        md_lines.extend([
            f"## 卷内第{volume_page:03d}页（PDF页 {source_pdf_page}，{risk}）",
            "",
            f"- 原图：`{original_rel}`",
            f"- 裁切图：`{cropped_rel}`",
            f"- OCR行数：{line_count}",
            f"- 平均置信度：{avg:.4f}",
            "",
            "```text",
            text,
            "```",
            "",
        ])
        html_parts.extend([
            f"<section id=\"vol-{volume_page:03d}\"><h2>卷内第{volume_page:03d}页（PDF页 {source_pdf_page}，{html.escape(risk)}）</h2>",
            f"<p>原图：<a href=\"../{html.escape(original_rel)}\">original</a>；裁切图：<a href=\"../{html.escape(cropped_rel)}\">cropped</a>；OCR行数：{line_count}；平均置信度：{avg:.4f}</p>",
            f"<pre>{html.escape(text)}</pre></section>",
        ])
        summary_rows.append({
            "volume_page": volume_page,
            "source_pdf_page": source_pdf_page,
            "line_count": line_count,
            "avg_score": f"{avg:.4f}",
            "risk": risk,
        })
    html_parts.append("</body></html>")
    (OUTPUT_READER / "连云港市志_第五十九卷方言_全新OCR草稿.md").write_text("\n".join(md_lines), encoding="utf-8")
    (OUTPUT_READER / "连云港市志_第五十九卷方言_全新OCR草稿.html").write_text("\n".join(html_parts), encoding="utf-8")
    with (REPORT_DIR / "ocr_draft_reader_summary.csv").open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["volume_page", "source_pdf_page", "line_count", "avg_score", "risk"])
        writer.writeheader()
        writer.writerows(summary_rows)
    print(OUTPUT_READER / "连云港市志_第五十九卷方言_全新OCR草稿.html")


if __name__ == "__main__":
    main()
