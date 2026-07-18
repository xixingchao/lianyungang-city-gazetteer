"""Render exported PDF pages and build OCR drafts for Lianyungang Shizhi.

The script treats exported PDFs as immutable inputs. It writes page images,
per-page OCR text/JSON, merged text, and a CSV report under the workstation.
It is intentionally checkpoint-friendly: existing page images and OCR files are
skipped unless --force-render or --force-ocr is passed.
"""

from __future__ import annotations

import argparse
import csv
import json
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import numpy as np
import pypdfium2 as pdfium
from PIL import Image, ImageFilter


ROOT = Path(__file__).resolve().parents[2]
WORKSTATION = ROOT / "连云港市志_workstation"
TESSERACT_EXE = Path(r"C:\Tesseract-OCR\tesseract.exe")


@dataclass(frozen=True)
class PartSpec:
    volume: str
    part: str
    source_pdf: Path

    @property
    def slug(self) -> str:
        return f"{self.volume}_{self.part}"

    @property
    def label(self) -> str:
        return f"连云港市志_{self.volume}_{self.part}"


PARTS = [
    PartSpec("上", "part01", ROOT / "连云港志上_1.pdf"),
    PartSpec("上", "part02", ROOT / "连云港志上_2.pdf"),
    PartSpec("上", "part03", ROOT / "连云港志上_3.pdf"),
    PartSpec("中", "part01", ROOT / "连云港志中_1.pdf"),
    PartSpec("中", "part02", ROOT / "连云港志中_2.pdf"),
    PartSpec("下", "part01", ROOT / "连云港志下_1.pdf"),
    PartSpec("下", "part02", ROOT / "连云港志下_2.pdf"),
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Render PDF pages and run OCR.")
    parser.add_argument("--parts", default="all", help="all, or comma-separated part ids: part01,part02,part03")
    parser.add_argument("--sample", action="store_true", help="run a representative sample per part")
    parser.add_argument("--pages", help="1-based pages, e.g. 1,10,100,-1. Overrides --sample")
    parser.add_argument("--start-page", type=int, help="1-based first page for range mode")
    parser.add_argument("--end-page", type=int, help="1-based last page for range mode")
    parser.add_argument("--limit", type=int, help="maximum number of pages per selected part")
    parser.add_argument("--dpi", type=int, default=180, help="render DPI; 180 is a good first-pass default")
    parser.add_argument("--engine", choices=["rapidocr", "tesseract"], default="rapidocr")
    parser.add_argument("--render-only", action="store_true")
    parser.add_argument("--ocr-only", action="store_true")
    parser.add_argument("--force-render", action="store_true")
    parser.add_argument("--force-ocr", action="store_true")
    return parser.parse_args()


def selected_parts(spec: str) -> list[PartSpec]:
    if spec == "all":
        return PARTS
    wanted = {item.strip() for item in spec.split(",") if item.strip()}
    parts = [part for part in PARTS if part.part in wanted or part.slug in wanted]
    missing = wanted - {part.part for part in parts} - {part.slug for part in parts}
    if missing:
        raise SystemExit(f"Unknown part id(s): {', '.join(sorted(missing))}")
    return parts


def page_count(pdf_path: Path) -> int:
    pdf = pdfium.PdfDocument(str(pdf_path))
    try:
        return len(pdf)
    finally:
        pdf.close()


def page_numbers(args: argparse.Namespace, total_pages: int) -> list[int]:
    if args.pages:
        pages: list[int] = []
        for raw in args.pages.split(","):
            raw = raw.strip()
            if not raw:
                continue
            value = int(raw)
            page = total_pages if value == -1 else value
            if page < 1 or page > total_pages:
                raise SystemExit(f"Page {value} is out of range 1-{total_pages}")
            pages.append(page)
    elif args.sample:
        candidates = [1, 2, 10, 50, 100, total_pages]
        pages = [page for page in candidates if 1 <= page <= total_pages]
    else:
        start = args.start_page or 1
        end = args.end_page or total_pages
        if start < 1 or end > total_pages or start > end:
            raise SystemExit(f"Invalid page range {start}-{end}; total pages={total_pages}")
        pages = list(range(start, end + 1))

    unique_pages = list(dict.fromkeys(pages))
    if args.limit:
        unique_pages = unique_pages[: args.limit]
    return unique_pages


def paths_for(part: PartSpec, page_num: int, dpi: int) -> dict[str, Path]:
    page_id = f"page_{page_num:04d}"
    image_dir = WORKSTATION / "workbench" / "conversion" / "page_images" / part.volume / part.part
    raw_dir = WORKSTATION / "workbench" / "ocr" / "raw" / part.volume / part.part
    return {
        "image": image_dir / f"{page_id}_{dpi}dpi.jpg",
        "text": raw_dir / f"{page_id}.txt",
        "json": raw_dir / f"{page_id}.json",
    }


def ensure_dirs() -> None:
    for path in [
        WORKSTATION / "workbench" / "conversion" / "page_images",
        WORKSTATION / "workbench" / "ocr" / "raw",
        WORKSTATION / "workbench" / "ocr" / "merged",
        WORKSTATION / "workbench" / "ocr" / "confidence",
        WORKSTATION / "workbench" / "qa",
    ]:
        path.mkdir(parents=True, exist_ok=True)


def render_page(pdf_path: Path, page_num: int, image_path: Path, dpi: int, force: bool) -> tuple[int, int]:
    if image_path.exists() and image_path.stat().st_size > 0 and not force:
        with Image.open(image_path) as img:
            return img.size

    image_path.parent.mkdir(parents=True, exist_ok=True)
    pdf = pdfium.PdfDocument(str(pdf_path))
    try:
        page = pdf[page_num - 1]
        try:
            bitmap = page.render(scale=dpi / 72)
            image = bitmap.to_pil().convert("RGB")
        finally:
            page.close()
    finally:
        pdf.close()

    image.save(image_path, "JPEG", quality=92, optimize=True)
    return image.size


def load_image_for_ocr(image_path: Path) -> Image.Image:
    image = Image.open(image_path).convert("RGB")
    return image.filter(ImageFilter.SHARPEN)


def rapidocr_engine():
    from rapidocr_onnxruntime import RapidOCR

    return RapidOCR()


def rapidocr_lines(engine, image: Image.Image) -> tuple[str, list[dict], float | None]:
    result, elapse = engine(np.array(image))
    if result is None:
        return "", [], None

    def sort_key(item) -> tuple[float, float]:
        box = item[0]
        xs = [point[0] for point in box]
        ys = [point[1] for point in box]
        return (min(ys), min(xs))

    rows = []
    for item in sorted(result, key=sort_key):
        box, text, score = item[0], item[1], float(item[2])
        rows.append({"text": text, "score": score, "box": box})

    text = "\n".join(row["text"] for row in rows)
    avg_conf = sum(row["score"] for row in rows) / len(rows) if rows else None
    return text, rows, avg_conf


def tesseract_text(image: Image.Image) -> tuple[str, list[dict], float | None]:
    import pytesseract

    if TESSERACT_EXE.exists():
        pytesseract.pytesseract.tesseract_cmd = str(TESSERACT_EXE)
    text = pytesseract.image_to_string(image, lang="chi_sim", config="--psm 6")
    return text.strip(), [], None


def ocr_page(engine_name: str, engine, image_path: Path) -> tuple[str, list[dict], float | None]:
    with load_image_for_ocr(image_path) as image:
        if engine_name == "rapidocr":
            return rapidocr_lines(engine, image)
        return tesseract_text(image)


def write_page_outputs(
    part: PartSpec,
    page_num: int,
    total_pages: int,
    engine_name: str,
    image_path: Path,
    text_path: Path,
    json_path: Path,
    text: str,
    lines: list[dict],
    avg_conf: float | None,
    time_s: float,
    image_size: tuple[int, int],
) -> None:
    text_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    header = f"# {part.label} 第 {page_num}/{total_pages} 页\n\n"
    text_path.write_text(header + text.strip() + "\n", encoding="utf-8")
    payload = {
        "book": "连云港市志",
        "volume": part.volume,
        "part": part.part,
        "source_pdf": str(part.source_pdf),
        "page": page_num,
        "total_pages": total_pages,
        "engine": engine_name,
        "image": str(image_path),
        "image_size": image_size,
        "text_chars": len(text.strip()),
        "line_count": len(lines),
        "avg_confidence": avg_conf,
        "time_s": round(time_s, 2),
        "lines": lines,
    }
    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def read_existing_text(text_path: Path) -> str:
    if not text_path.exists():
        return ""
    text = text_path.read_text(encoding="utf-8", errors="replace")
    parts = text.split("\n\n", 1)
    return parts[1].strip() if len(parts) == 2 else text.strip()


def merge_part_text(part: PartSpec, pages: Iterable[int]) -> Path:
    merged_dir = WORKSTATION / "workbench" / "ocr" / "merged"
    merged_dir.mkdir(parents=True, exist_ok=True)
    merged_path = merged_dir / f"{part.label}_OCR汇总.md"
    chunks = [f"# {part.label} OCR汇总\n"]
    for page_num in pages:
        text_path = paths_for(part, page_num, 180)["text"]
        if not text_path.exists():
            matches = sorted(text_path.parent.glob(f"page_{page_num:04d}.txt"))
            if matches:
                text_path = matches[0]
        if not text_path.exists():
            continue
        chunks.append(f"\n\n## 第 {page_num} 页\n\n")
        chunks.append(read_existing_text(text_path))
    merged_path.write_text("".join(chunks).rstrip() + "\n", encoding="utf-8")
    return merged_path


def write_report(records: list[dict], engine_name: str, dpi: int) -> Path:
    report_dir = WORKSTATION / "workbench" / "ocr" / "confidence"
    report_dir.mkdir(parents=True, exist_ok=True)
    csv_path = report_dir / f"连云港市志_上册_{engine_name}_{dpi}dpi_OCR统计.csv"
    fields = [
        "volume",
        "part",
        "page",
        "status",
        "engine",
        "dpi",
        "chars",
        "lines",
        "avg_confidence",
        "time_s",
        "image_size",
        "source_pdf",
        "image_path",
        "text_path",
        "json_path",
        "error",
    ]
    with csv_path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for record in records:
            writer.writerow({field: record.get(field, "") for field in fields})
    return csv_path


def main() -> int:
    args = parse_args()
    ensure_dirs()
    parts = selected_parts(args.parts)
    engine = rapidocr_engine() if args.engine == "rapidocr" and not args.render_only else None
    all_records: list[dict] = []

    for part in parts:
        if not part.source_pdf.exists() or part.source_pdf.stat().st_size == 0:
            print(f"[SKIP] Missing or empty PDF: {part.source_pdf}")
            continue
        total = page_count(part.source_pdf)
        pages = page_numbers(args, total)
        print(f"[PART] {part.label}: {len(pages)} page(s), source pages={total}")

        completed_pages: list[int] = []
        for page_num in pages:
            out = paths_for(part, page_num, args.dpi)
            t0 = time.time()
            status = "ok"
            error = ""
            text = ""
            lines: list[dict] = []
            avg_conf: float | None = None
            try:
                image_size = render_page(part.source_pdf, page_num, out["image"], args.dpi, args.force_render)
                if args.render_only:
                    print(f"  page {page_num:04d}: rendered {image_size[0]}x{image_size[1]}")
                elif out["text"].exists() and out["json"].exists() and not args.force_ocr:
                    text = read_existing_text(out["text"])
                    print(f"  page {page_num:04d}: skip OCR ({len(text)} chars cached)")
                else:
                    text, lines, avg_conf = ocr_page(args.engine, engine, out["image"])
                    write_page_outputs(
                        part,
                        page_num,
                        total,
                        args.engine,
                        out["image"],
                        out["text"],
                        out["json"],
                        text,
                        lines,
                        avg_conf,
                        time.time() - t0,
                        image_size,
                    )
                    conf_text = "" if avg_conf is None else f", conf={avg_conf:.3f}"
                    print(f"  page {page_num:04d}: OCR {len(text.strip())} chars, lines={len(lines)}{conf_text}")
                completed_pages.append(page_num)
            except Exception as exc:  # Keep long jobs moving and report exact failures.
                status = "failed"
                error = f"{type(exc).__name__}: {exc}"
                image_size = (0, 0)
                print(f"  page {page_num:04d}: FAILED {error}")

            all_records.append(
                {
                    "volume": part.volume,
                    "part": part.part,
                    "page": page_num,
                    "status": status,
                    "engine": args.engine,
                    "dpi": args.dpi,
                    "chars": len(text.strip()),
                    "lines": len(lines),
                    "avg_confidence": "" if avg_conf is None else round(avg_conf, 4),
                    "time_s": round(time.time() - t0, 2),
                    "image_size": f"{image_size[0]}x{image_size[1]}",
                    "source_pdf": str(part.source_pdf),
                    "image_path": str(out["image"]),
                    "text_path": str(out["text"]),
                    "json_path": str(out["json"]),
                    "error": error,
                }
            )

        if not args.render_only and completed_pages:
            merged = merge_part_text(part, completed_pages)
            print(f"[MERGED] {merged}")

    if all_records:
        csv_path = write_report(all_records, args.engine, args.dpi)
        print(f"[REPORT] {csv_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
