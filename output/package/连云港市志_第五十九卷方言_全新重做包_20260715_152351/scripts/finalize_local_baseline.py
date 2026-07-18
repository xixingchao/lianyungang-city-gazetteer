from __future__ import annotations

import csv
import json
from collections import Counter
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAPPING_CSV = ROOT / "input" / "source" / "page_mapping.csv"
SOURCE_PDF = ROOT / "input" / "source" / "连云港市志_第五十九卷方言_源页_全新重做.pdf"
OCR_REPORT_CSV = ROOT / "output" / "reports" / "rapidocr_full_report.csv"
DIALECT_CSV = ROOT / "workbench" / "dialect" / "dialect_page_inventory_initial.csv"
READER_HTML = ROOT / "output" / "reader" / "连云港市志_第五十九卷方言_全新OCR草稿.html"
READER_MD = ROOT / "output" / "reader" / "连云港市志_第五十九卷方言_全新OCR草稿.md"
REPORT_DIR = ROOT / "output" / "reports"
QA_DIR = ROOT / "workbench" / "qa"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def existing(path_text: str) -> bool:
    return bool(path_text) and Path(path_text).exists()


def file_size_mb(path: Path) -> float:
    return path.stat().st_size / 1024 / 1024 if path.exists() else 0.0


def classify_delivery_state(missing: list[str], high_risk_pages: list[int]) -> str:
    if missing:
        return "本地证据链不完整"
    if high_risk_pages:
        return "本地维护基线完成；OCR草稿需人工双审后才能作为最终文本"
    return "本地维护基线完成；仍需按抽样规则复核"


def main() -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    QA_DIR.mkdir(parents=True, exist_ok=True)

    mapping = read_csv(MAPPING_CSV)
    ocr_rows = read_csv(OCR_REPORT_CSV)
    dialect_rows = read_csv(DIALECT_CSV)

    missing: list[str] = []
    for required in [MAPPING_CSV, SOURCE_PDF, OCR_REPORT_CSV, DIALECT_CSV, READER_HTML, READER_MD]:
        if not required.exists():
            missing.append(str(required))

    for row in mapping:
        for key in ["original_image", "cropped_image"]:
            if not existing(row.get(key, "")):
                missing.append(f"{key}: {row.get(key, '')}")

    for row in ocr_rows:
        for key in ["txt_path", "json_path"]:
            if not existing(row.get(key, "")):
                missing.append(f"{key}: {row.get(key, '')}")

    route_counts = Counter(row.get("dialect_route", "unknown") for row in dialect_rows)
    risk_counts = Counter(row.get("risk_note", "unknown") for row in ocr_rows)
    high_risk_pages = [int(row["volume_page"]) for row in ocr_rows if row.get("risk_note") == "high_ocr_risk"]
    dialect_layout_pages = [int(row["volume_page"]) for row in ocr_rows if row.get("risk_note") == "dialect_layout_risk"]
    avg_scores = [float(row["avg_score"]) for row in ocr_rows if row.get("avg_score")]
    avg_score = sum(avg_scores) / len(avg_scores) if avg_scores else 0.0

    state = classify_delivery_state(missing, high_risk_pages)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    qa_json = {
        "generated_at": now,
        "project_root": str(ROOT),
        "source_pdf": str(SOURCE_PDF),
        "source_pdf_size_mb": round(file_size_mb(SOURCE_PDF), 2),
        "volume_pages": len(mapping),
        "ocr_pages": len(ocr_rows),
        "dialect_inventory_pages": len(dialect_rows),
        "reader_html_exists": READER_HTML.exists(),
        "reader_md_exists": READER_MD.exists(),
        "missing_count": len(missing),
        "missing": missing,
        "ocr_risk_counts": dict(risk_counts),
        "dialect_route_counts": dict(route_counts),
        "avg_ocr_score": round(avg_score, 4),
        "high_ocr_risk_pages": high_risk_pages,
        "dialect_layout_risk_pages": dialect_layout_pages,
        "delivery_state": state,
        "github_upload_state": "not_uploaded_by_current_user_request",
    }

    (QA_DIR / "本地完成态核验.json").write_text(json.dumps(qa_json, ensure_ascii=False, indent=2), encoding="utf-8")

    risk_lines = [
        "# 第59卷本地完成态核验报告",
        "",
        f"生成时间：{now}",
        "",
        "## 结论",
        "",
        f"{state}。",
        "",
        "本轮第59卷已经在本地统一为全新重做维护基线：重新抽取源页、重新渲染页图、重新生成 OCR 草稿、建立页级分流和方言路由清单，并形成可重打包的本地项目。",
        "",
        "重要边界：当前 OCR 草稿不能冒充最终双审文本。第59卷含大量音标、声韵调表、同音字汇和方言词汇，后续正式正文/字典数据必须回看页图进行人工分块、结构化和双审。",
        "",
        "## 证据链核对",
        "",
        f"- 项目根目录：`{ROOT}`",
        f"- 抽页源 PDF：`{SOURCE_PDF}`（{file_size_mb(SOURCE_PDF):.2f} MB）",
        f"- 卷内页数：{len(mapping)} 页",
        f"- 页图：原图 {len(mapping)} 页，裁切图 {len(mapping)} 页",
        f"- RapidOCR：{len(ocr_rows)} 页",
        f"- 方言分流 inventory：{len(dialect_rows)} 页",
        f"- HTML 草稿：`{READER_HTML}`",
        f"- Markdown 草稿：`{READER_MD}`",
        "",
        "## OCR 风险统计",
        "",
    ]
    for key, count in sorted(risk_counts.items()):
        risk_lines.append(f"- {key}: {count} 页")
    risk_lines.extend([
        "",
        f"- 全卷平均 OCR 置信度：{avg_score:.4f}",
        f"- 高 OCR 风险页：{', '.join(map(str, high_risk_pages)) if high_risk_pages else '无'}",
        f"- 方言版式风险页：{', '.join(map(str, dialect_layout_pages)) if dialect_layout_pages else '无'}",
        "",
        "## 方言路由统计",
        "",
    ])
    for key, count in sorted(route_counts.items()):
        risk_lines.append(f"- {key}: {count} 页")
    risk_lines.extend([
        "",
        "## 本地 QA",
        "",
        f"- 缺失项数量：{len(missing)}",
    ])
    if missing:
        risk_lines.append("- 缺失项：")
        risk_lines.extend(f"  - `{item}`" for item in missing)
    else:
        risk_lines.append("- 源 PDF、页图、OCR、方言清单、读者文件均已核对存在。")
    risk_lines.extend([
        "",
        "## 后续维护口径",
        "",
        "1. 后续上传 GitHub 时，以本项目最新 `output/package/` 里的包作为第59卷维护基线。",
        "2. 不再把旧 OCR、旧 redo 台账、旧验收状态作为本轮第59卷依据。",
        "3. 如果要生成最终正式文本，应从本包继续：先做版面分块，再做 dictionary mode 结构化，再做两轮双审。",
        "",
    ])

    final_report = REPORT_DIR / "volume59_local_baseline_final_report.md"
    final_note = ROOT / "本地维护说明_第59卷全新重做.md"
    final_report.write_text("\n".join(risk_lines), encoding="utf-8")
    final_note.write_text("\n".join(risk_lines), encoding="utf-8")

    print(final_report)
    print(QA_DIR / "本地完成态核验.json")


if __name__ == "__main__":
    main()
