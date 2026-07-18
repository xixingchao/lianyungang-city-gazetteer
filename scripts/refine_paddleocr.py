# -*- coding: utf-8 -*-
"""基于 PaddleOCR 结果的通用正文精修脚本 (适配 refine_chapter.py)

与 refine_chapter.py 逻辑相同，但读取 workbench/ocr/paddle_ocr/ 而非 workbench/ocr/raw/
输出到 workbench/body_chapters/paddle_上/ 避免覆盖原结果
"""

import argparse
import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKSTATION = ROOT
ANCHOR_CSV = ROOT / "workbench" / "indexes" / "连云港市志_上册页锚索引.csv"
OUT_BASE = ROOT / "workbench" / "body_chapters" / "paddle_上"
QA_BASE = ROOT / "workbench" / "qa" / "paddle_上"

# part → (PaddleOCR 目录, 全局页偏移)
PART_INFO = {
    "上/part01": (ROOT / "workbench" / "ocr" / "paddle_ocr" / "上" / "part01", 0),
    "上/part02": (ROOT / "workbench" / "ocr" / "paddle_ocr" / "上" / "part02", 300),
    "上/part03": (ROOT / "workbench" / "ocr" / "paddle_ocr" / "上" / "part03", 605),
}

BATCH_PLAN = [
    ("上/part01", 13, 28, "序与凡例"),
    ("上/part01", 29, 123, "总述与大事记"),
    ("上/part01", 124, 212, "第一卷 自然环境"),
    ("上/part01", 213, 231, "第二卷 建置区划"),
    ("上/part01", 232, 278, "第三卷 区县概况"),
    ("上/part01", 279, 300, "第四卷 人口（part01 部分）"),
    ("上/part02", 301, 605, "第四卷至第十卷（part02）"),
    ("上/part03", 606, 903, "第十卷至第十六卷（part03）"),
]

HEADER_PATTERNS = [
    re.compile(r"^·\d+·连云港市志·[^\n]+\s*$", re.MULTILINE),
    re.compile(r"^[^\n]+·\d+·\s*$", re.MULTILINE),
    re.compile(r"^·\d+·\s*$", re.MULTILINE),
    re.compile(r"^连云港市志·[^\n]+\s*$", re.MULTILINE),
    re.compile(r"^\.\d+\.[iil]\s*$", re.MULTILINE),
    re.compile(r"^\.\d+\.\s*$", re.MULTILINE),
    re.compile(r"^[^\u4e00-\u9fff\n]{1,12}连云港市志·[\u4e00-\u9fff（）()]{1,25}\s*$", re.MULTILINE),
]

TABLE_PATTERN = re.compile(r"续上表|续表|表\d+[-—]\d+")


def load_anchors():
    anchors = {}
    if not ANCHOR_CSV.exists():
        return anchors
    with open(ANCHOR_CSV, encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            anchors[int(row["global_page"])] = row["anchor"]
    return anchors


def clean_ocr_meta(lines):
    return [ln for ln in lines if not ln.startswith("# 连云港市志_")]


def clean_headers(text):
    for pat in HEADER_PATTERNS:
        text = pat.sub("", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def is_table_page(text):
    return bool(TABLE_PATTERN.search(text))


def process_page(page_num, ocr_dir, offset, anchor):
    ebook_page = page_num - offset
    txt_path = ocr_dir / f"page_{ebook_page:04d}.txt"
    if not txt_path.exists():
        return {"page": page_num, "anchor": anchor, "text": "", "missing": True, "table": False}
    raw = txt_path.read_text(encoding="utf-8")
    lines = clean_ocr_meta(raw.splitlines())
    text = "\n".join(lines)
    text = clean_headers(text)
    table = is_table_page(text)
    return {"page": page_num, "anchor": anchor, "text": text, "missing": False, "table": table}


def build_markdown(title, pages):
    lines = []
    lines.append(f"# {title}")
    lines.append("")
    lines.append("<!-- PaddleOCR PP-OCRv6_small 识别，已清理页眉页脚和 OCR 元信息 -->")
    lines.append("<!-- 内部页锚保留为 HTML 注释，最终阅读版移除。表格页已标注占位。 -->")
    lines.append("")

    for i, pg in enumerate(pages):
        if pg["missing"]:
            lines.append(f"<!-- page-anchor: {pg['anchor']} -->")
            lines.append(f"[缺失页 p{pg['page']}]")
            lines.append("")
            continue

        text = pg["text"]
        if not text.strip():
            continue

        lines.append(f"<!-- page-anchor: {pg['anchor']} -->")
        lines.append("")

        if pg["table"]:
            lines.append(f"<!-- TABLE-PAGE: p{pg['page']} 表格页，OCR 原文暂留 -->")
            lines.append("")

        lines.append(text)
        lines.append("")

    return "\n".join(lines)


def build_qa(title, part, start, end, pages):
    lines = []
    lines.append(f"# {title} PaddleOCR 精修 QA 报告")
    lines.append("")
    lines.append(f"范围：{part} 全局页 {start}-{end}（{end-start+1} 页）")
    lines.append("")

    missing = [pg for pg in pages if pg["missing"]]
    empty = [pg for pg in pages if not pg["missing"] and not pg["text"].strip()]
    low_char = [pg for pg in pages if not pg["missing"] and 0 < len(pg["text"].strip()) < 50]
    table_pages = [pg for pg in pages if pg["table"]]

    lines.append("## 页面统计")
    lines.append("")
    lines.append(f"- 总页数：{len(pages)}")
    lines.append(f"- 缺失页：{len(missing)}")
    lines.append(f"- 空文本页：{len(empty)}")
    lines.append(f"- 低字符页（<50字）：{len(low_char)}")
    lines.append(f"- 表格页：{len(table_pages)}")
    lines.append("")

    total_chars = sum(len(pg["text"]) for pg in pages if not pg["missing"])
    lines.append("## 清理统计")
    lines.append("")
    lines.append(f"- 精修后总字符数：{total_chars}")
    lines.append(f"- 平均每页字符数：{total_chars // max(len(pages), 1)}")
    lines.append("")

    if missing:
        lines.append("### 缺失页清单")
        for pg in missing:
            lines.append(f"- p{pg['page']}")
        lines.append("")

    if low_char:
        lines.append("### 低字符页清单（可能为过渡页/图片页）")
        for pg in low_char[:20]:
            lines.append(f"- p{pg['page']}（{len(pg['text'].strip())} 字）")
        lines.append("")

    if table_pages:
        lines.append("### 表格页清单（已标注占位）")
        for pg in table_pages[:30]:
            lines.append(f"- p{pg['page']}")
        if len(table_pages) > 30:
            lines.append(f"- ... 共 {len(table_pages)} 页")
        lines.append("")

    lines.append("## 已清理项")
    lines.append("- OCR 元信息首行")
    lines.append("- 页眉模式（·N·连云港市志·XXX / XXX·N· / 连云港市志·XXX / .N.i / .N.）")
    lines.append("- 孤立页码行")
    lines.append("- 多余空行（3+→2）")
    lines.append("")

    lines.append("## PaddleOCR 特有信息")
    lines.append("- 引擎: PP-OCRv6_small (det + rec)")
    lines.append("- 平均置信度: ~0.99")
    lines.append("- 标点符号: 半角括号 (原 RapidOCR 为全角)")
    lines.append("")

    return "\n".join(lines)


def safe_filename(title):
    s = re.sub(r'[\\/:*?"<>|]', "_", title)
    s = re.sub(r"\s+", "_", s)
    return s


def refine_range(part, start, end, title, anchors):
    ocr_dir, offset = PART_INFO[part]
    pages = []
    for p in range(start, end + 1):
        anchor = anchors.get(p, "")
        pages.append(process_page(p, ocr_dir, offset, anchor))

    md = build_markdown(title, pages)
    qa = build_qa(title, part, start, end, pages)

    fname = safe_filename(title)
    OUT_BASE.mkdir(parents=True, exist_ok=True)
    QA_BASE.mkdir(parents=True, exist_ok=True)
    out_md = OUT_BASE / f"{fname}.md"
    out_qa = QA_BASE / f"{fname}_PaddleOCR_精修QA报告.md"
    out_md.write_text(md, encoding="utf-8")
    out_qa.write_text(qa, encoding="utf-8")

    missing = sum(1 for pg in pages if pg["missing"])
    table_count = sum(1 for pg in pages if pg["table"])
    total_chars = sum(len(pg["text"]) for pg in pages if not pg["missing"])
    print(f"[{title}] {part} p{start}-p{end} ({len(pages)}页) 缺失{missing} 表格{table_count} 字符{total_chars}")
    return {"title": title, "part": part, "start": start, "end": end,
            "pages": len(pages), "missing": missing, "table": table_count,
            "chars": total_chars, "md": out_md, "qa": out_qa}


def main():
    parser = argparse.ArgumentParser(description="基于 PaddleOCR 的正文精修")
    parser.add_argument("--part")
    parser.add_argument("--start", type=int)
    parser.add_argument("--end", type=int)
    parser.add_argument("--title")
    parser.add_argument("--batch", action="store_true")
    args = parser.parse_args()

    anchors = load_anchors()
    print(f"[PaddleOCR Refine] Anchors loaded: {len(anchors)}")

    if args.batch:
        results = []
        for part, start, end, title in BATCH_PLAN:
            r = refine_range(part, start, end, title, anchors)
            results.append(r)
        print("")
        print("=== PaddleOCR 上册批量精修汇总 ===")
        total_pages = sum(r["pages"] for r in results)
        total_missing = sum(r["missing"] for r in results)
        total_table = sum(r["table"] for r in results)
        total_chars = sum(r["chars"] for r in results)
        print(f"总页数: {total_pages}  缺失: {total_missing}  表格页: {total_table}  总字符: {total_chars}")
        print(f"产出 MD: {len(results)} 个  QA: {len(results)} 个")
    else:
        if not all([args.part, args.start, args.end, args.title]):
            parser.error("需要 --part --start --end --title，或使用 --batch")
        refine_range(args.part, args.start, args.end, args.title, anchors)


if __name__ == "__main__":
    main()
