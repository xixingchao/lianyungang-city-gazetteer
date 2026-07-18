from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAPPING_CSV = ROOT / "input" / "source" / "page_mapping.csv"
REVIEW_DIR = ROOT / "workbench" / "review"
LAYOUT_DIR = ROOT / "workbench" / "layout"
DIALECT_DIR = ROOT / "workbench" / "dialect"
MANUAL_DIR = ROOT / "workbench" / "manual_transcription"
QA_DIR = ROOT / "workbench" / "qa"
REPORT_DIR = ROOT / "output" / "reports"


def read_mapping() -> list[dict[str, str]]:
    with MAPPING_CSV.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def ensure_dirs() -> None:
    for path in (REVIEW_DIR, LAYOUT_DIR, DIALECT_DIR, MANUAL_DIR, QA_DIR, REPORT_DIR):
        path.mkdir(parents=True, exist_ok=True)


def risk_for_page(volume_page: int) -> tuple[str, str]:
    # Initial fresh-routing heuristic from the volume nature only, not from old OCR.
    if 1 <= volume_page <= 2:
        return "高", "卷首概述/章节开端；需确认标题层级和页边界"
    if 3 <= volume_page <= 14:
        return "高", "声母/韵母差异与音标表；重点分流音标、声韵调表、方言例句"
    if 15 <= volume_page <= 26:
        return "高", "语音系统与声韵调材料；重点分流表格、IPA、调值"
    if 27 <= volume_page <= 42:
        return "高", "同音字汇/方言词汇密集区；按字典模式分块"
    if 43 <= volume_page <= 48:
        return "中", "方言词汇/语法与卷末边界；重点确认页末续接"
    return "待定", "需人工确认"


def write_layout(rows: list[dict[str, str]]) -> None:
    out_csv = REVIEW_DIR / "阶段01_全新页级分流台账.csv"
    out_md = REVIEW_DIR / "阶段01_全新页级分流台账.md"
    fields = [
        "volume_page",
        "source_pdf_page",
        "page_id",
        "original_image",
        "cropped_image",
        "fresh_status",
        "initial_risk",
        "initial_route",
        "required_next_step",
    ]
    output_rows = []
    for row in rows:
        volume_page = int(row["volume_page"])
        risk, route = risk_for_page(volume_page)
        output_rows.append(
            {
                "volume_page": row["volume_page"],
                "source_pdf_page": row["source_pdf_page"],
                "page_id": f"page_{int(row['source_pdf_page']):04d}",
                "original_image": row["original_image"],
                "cropped_image": row["cropped_image"],
                "fresh_status": "rendered_from_original_only",
                "initial_risk": risk,
                "initial_route": route,
                "required_next_step": "run_fresh_ocr_then_manual_layout_review",
            }
        )

    with out_csv.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(output_rows)

    lines = [
        "# 阶段01 全新页级分流台账",
        "",
        "说明：本台账只基于原件重新抽取的页图和第59卷内容属性建立；未使用旧 OCR、旧重排文本或旧双审台账。",
        "",
        "| 卷内页 | PDF页 | 页ID | 初始风险 | 初始分流 | 下一步 |",
        "|---:|---:|---|---|---|---|",
    ]
    for row in output_rows:
        lines.append(
            f"| {row['volume_page']} | {row['source_pdf_page']} | {row['page_id']} | "
            f"{row['initial_risk']} | {row['initial_route']} | {row['required_next_step']} |"
        )
    out_md.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_dialect_inventory(rows: list[dict[str, str]]) -> None:
    out_csv = DIALECT_DIR / "dialect_page_inventory_initial.csv"
    fields = ["volume_page", "source_pdf_page", "page_id", "dialect_route", "status", "note"]
    with out_csv.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            volume_page = int(row["volume_page"])
            page_id = f"page_{int(row['source_pdf_page']):04d}"
            if volume_page <= 26:
                route = "phonology_tables_or_prose"
                note = "likely contains phonology discussion, IPA, tone values, or sound correspondence tables"
            elif volume_page <= 42:
                route = "dictionary_mode"
                note = "likely contains homophone dictionary or dialect lexicon blocks; segment before OCR cleanup"
            else:
                route = "mixed_dialect_prose"
                note = "likely contains lexicon/prose/grammar material; confirm by fresh OCR and page view"
            writer.writerow(
                {
                    "volume_page": row["volume_page"],
                    "source_pdf_page": row["source_pdf_page"],
                    "page_id": page_id,
                    "dialect_route": route,
                    "status": "pending_fresh_ocr_and_manual_layout_review",
                    "note": note,
                }
            )


def write_task_list(rows: list[dict[str, str]]) -> None:
    out = REVIEW_DIR / "全新重做执行任务单.md"
    lines = [
        "# 第59卷全新重做执行任务单",
        "",
        "本任务单从原件重新抽页后生成，不继承旧 OCR、旧重排文本或旧验收状态。",
        "",
        "## 执行顺序",
        "",
        "1. 运行全新 OCR：PaddleOCR 为主，RapidOCR 作为疑难对照。",
        "2. 对每页做人工版面分流：正文、表格、音标/声韵调、同音字汇、方言词汇、页眉页脚。",
        "3. 方言/音系页进入 dictionary mode，不并入普通正文清洗。",
        "4. 每页生成新的人工校正文或结构化字典页。",
        "5. 两轮逐字/逐项双审后，才能写通过结论。",
        "",
        "## 第一批建议",
        "",
        "先处理卷内第1-6页，用于验证新 OCR、裁切、音标分流和人工校正文模板。",
        "",
        "| 批次 | 卷内页 | PDF页 | 任务 | 状态 |",
        "|---|---:|---:|---|---|",
    ]
    for row in rows[:6]:
        lines.append(
            f"| pilot | {row['volume_page']} | {row['source_pdf_page']} | fresh OCR + 版面分流 + 人工校正文模板 | 待执行 |"
        )
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_report(rows: list[dict[str, str]]) -> None:
    out = REPORT_DIR / "fresh_project_initial_audit.md"
    out.write_text(
        "# 第59卷全新重做初始化审计\n\n"
        "## 结论\n\n"
        "已建立全新第59卷重做项目，并从原件 PDF 重新抽取 48 页证据材料。\n\n"
        "## 证据\n\n"
        f"- 页码映射：`{MAPPING_CSV}`\n"
        f"- 原始页图数：{len(list((ROOT / 'workbench' / 'page_images' / 'original').glob('*.jpg')))}\n"
        f"- 裁切页图数：{len(list((ROOT / 'workbench' / 'page_images' / 'cropped').glob('*.jpg')))}\n"
        f"- 卷内页数：{len(rows)}\n"
        "- 旧 OCR：未使用。\n"
        "- 旧重排文本：未使用。\n"
        "- 旧双审台账：未使用。\n\n"
        "## 下一步\n\n"
        "运行全新 OCR 小样，先处理卷内第1-6页，确认音标、声韵调表、方言字典块的分流策略。\n",
        encoding="utf-8",
    )


def main() -> None:
    ensure_dirs()
    rows = read_mapping()
    write_layout(rows)
    write_dialect_inventory(rows)
    write_task_list(rows)
    write_report(rows)
    print(f"ledger_pages={len(rows)}")
    print(f"review_dir={REVIEW_DIR}")


if __name__ == "__main__":
    main()
