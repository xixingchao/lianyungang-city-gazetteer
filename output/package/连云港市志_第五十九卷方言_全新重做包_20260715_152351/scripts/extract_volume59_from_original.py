from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

import pypdfium2 as pdfium
from pypdf import PdfReader, PdfWriter
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SOURCE_PDF = Path(r"E:\codex_Learing\17_project_数字化工作站\连云港志原件\连云港志下_2.pdf")
START_PAGE = 295
END_PAGE = 342
DPI = 300
JPEG_QUALITY = 92

INPUT_DIR = ROOT / "input" / "source"
ORIGINAL_DIR = ROOT / "workbench" / "page_images" / "original"
CROPPED_DIR = ROOT / "workbench" / "page_images" / "cropped"
REPORT_DIR = ROOT / "output" / "reports"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def ensure_dirs() -> None:
    for path in (INPUT_DIR, ORIGINAL_DIR, CROPPED_DIR, REPORT_DIR):
        path.mkdir(parents=True, exist_ok=True)


def extract_pdf_pages() -> Path:
    reader = PdfReader(str(SOURCE_PDF))
    writer = PdfWriter()
    for source_page in range(START_PAGE, END_PAGE + 1):
        writer.add_page(reader.pages[source_page - 1])
    out_pdf = INPUT_DIR / "连云港市志_第五十九卷方言_源页_全新重做.pdf"
    with out_pdf.open("wb") as f:
        writer.write(f)
    return out_pdf


def crop_body(image: Image.Image) -> Image.Image:
    width, height = image.size
    # Conservative crop: remove only common running header/footer margins.
    left = int(width * 0.035)
    right = int(width * 0.965)
    top = int(height * 0.055)
    bottom = int(height * 0.955)
    return image.crop((left, top, right, bottom))


def render_pages() -> list[dict[str, object]]:
    document = pdfium.PdfDocument(str(SOURCE_PDF))
    rows: list[dict[str, object]] = []
    scale = DPI / 72
    for idx, source_page in enumerate(range(START_PAGE, END_PAGE + 1), start=1):
        page = document[source_page - 1]
        bitmap = page.render(scale=scale)
        image = bitmap.to_pil().convert("RGB")

        original_name = f"page_{source_page:04d}_vol_{idx:03d}_original_{DPI}dpi.jpg"
        cropped_name = f"page_{source_page:04d}_vol_{idx:03d}_cropped_{DPI}dpi.jpg"
        original_path = ORIGINAL_DIR / original_name
        cropped_path = CROPPED_DIR / cropped_name

        image.save(original_path, quality=JPEG_QUALITY, optimize=True)
        crop_body(image).save(cropped_path, quality=JPEG_QUALITY, optimize=True)

        rows.append(
            {
                "volume_page": idx,
                "source_pdf": str(SOURCE_PDF),
                "source_pdf_page": source_page,
                "original_image": str(original_path),
                "cropped_image": str(cropped_path),
                "original_sha256": sha256_file(original_path),
                "cropped_sha256": sha256_file(cropped_path),
                "status": "rendered_from_original",
            }
        )
    return rows


def write_mapping(rows: list[dict[str, object]], source_extract_pdf: Path) -> None:
    mapping_csv = INPUT_DIR / "page_mapping.csv"
    fieldnames = [
        "volume_page",
        "source_pdf",
        "source_pdf_page",
        "original_image",
        "cropped_image",
        "original_sha256",
        "cropped_sha256",
        "status",
    ]
    with mapping_csv.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    metadata = {
        "book": "连云港市志",
        "volume": "第五十九卷 方言",
        "mode": "fresh_redo_from_original_only",
        "source_pdf": str(SOURCE_PDF),
        "source_pdf_sha256": sha256_file(SOURCE_PDF),
        "extracted_pdf": str(source_extract_pdf),
        "extracted_pdf_sha256": sha256_file(source_extract_pdf),
        "source_pdf_pages": [START_PAGE, END_PAGE],
        "volume_pages": [1, len(rows)],
        "page_count": len(rows),
        "dpi": DPI,
        "note": "No old OCR, old redo ledger, or old rearranged text was used to create these source artifacts.",
    }
    (INPUT_DIR / "source_metadata.json").write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    report = REPORT_DIR / "source_extraction_report.md"
    report.write_text(
        "# 第59卷全新重做源页抽取报告\n\n"
        f"- 源 PDF：`{SOURCE_PDF}`\n"
        f"- 抽取页段：PDF 第 {START_PAGE}-{END_PAGE} 页\n"
        f"- 卷内页数：{len(rows)}\n"
        f"- 渲染 DPI：{DPI}\n"
        f"- 源页 PDF：`{source_extract_pdf}`\n"
        f"- 页码映射：`{mapping_csv}`\n"
        "- 说明：本次抽取未使用旧 OCR、旧重排文本或旧双审台账。\n",
        encoding="utf-8",
    )


def main() -> None:
    if not SOURCE_PDF.exists():
        raise FileNotFoundError(SOURCE_PDF)
    ensure_dirs()
    source_extract_pdf = extract_pdf_pages()
    rows = render_pages()
    write_mapping(rows, source_extract_pdf)
    print(f"extracted_pages={len(rows)}")
    print(f"source_extract_pdf={source_extract_pdf}")
    print(f"mapping={INPUT_DIR / 'page_mapping.csv'}")


if __name__ == "__main__":
    main()
