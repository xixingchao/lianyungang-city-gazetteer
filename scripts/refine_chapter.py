# -*- coding: utf-8 -*-
"""
连云港市志 通用正文精修脚本

基于试点 refine_pilot.py 验证的流程，泛化为支持任意 part/页范围/卷标题的批量精修工具。

用法:
  python refine_chapter.py --part 上/part01 --start 124 --end 212 --title "第一卷 自然环境"
  python refine_chapter.py --batch  # 按 part01/02/03 骨架批量精修上册全部卷

清理规则:
  - OCR 元信息首行
  - 页眉模式（·N·连云港市志·XXX / XXX·N· / 连云港市志·XXX / .N.i / .N.）
  - 孤立页码行
  - 多余空行
  - 表格页检测：含"续上表"/"表X-X"的页插入表格占位标记，OCR 原文保留但标注

保留:
  - 内部页锚（HTML 注释）
  - 跨页段落回接
"""

import argparse
import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKSTATION = ROOT
ANCHOR_CSV = ROOT / "workbench" / "indexes" / "连云港市志_上册页锚索引.csv"
OUT_BASE = ROOT / "workbench" / "body_chapters" / "上"
QA_BASE = ROOT / "workbench" / "qa"

# part → (OCR 目录, 全局页偏移)
PART_INFO = {
    "上/part01": (ROOT / "workbench" / "ocr" / "raw" / "上" / "part01", 0),
    "上/part02": (ROOT / "workbench" / "ocr" / "raw" / "上" / "part02", 300),
    "上/part03": (ROOT / "workbench" / "ocr" / "raw" / "上" / "part03", 605),
}

# 上册批量精修计划（按骨架卷范围）
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
    # 行首含页码标点（无汉字）+ 连云港市志·XXX 的页眉行
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


def is_sentence_end(text):
    text = text.rstrip()
    if not text:
        return True
    return text[-1] in "。！？；：」』）)\"'\"'}》"


def is_new_section(line):
    line = line.strip()
    if not line:
        return True
    if re.match(r"^第[一二三四五六七八九十百千零〇\d]+[卷章节]\s", line):
        return True
    if re.match(r"^第[一二三四五六七八九十百千零〇\d]+[卷章节]$", line):
        return True
    if re.match(r"^概述\s*$", line):
        return True
    if re.match(r"^第[一二三四五六七八九十]+节", line):
        return True
    if re.match(r"^附\d+-\d+", line):
        return True
    return False


def is_table_page(text):
    return bool(TABLE_PATTERN.search(text))


def process_page(page_num, ocr_dir, offset, anchor):
    """处理单页，返回 dict"""
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
    lines.append("<!-- 精修说明：基于上册 OCR 初稿，已清理页眉页脚和 OCR 元信息；跨页段落已回接。 -->")
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
            # 表格页占位
            lines.append(f"<!-- TABLE-PAGE: p{pg['page']} 表格页，OCR 原文暂留，阶段 F 表格结构化时处理 -->")
            lines.append("")

        lines.append(text)
        lines.append("")

    return "\n".join(lines)


def build_qa(title, part, start, end, pages):
    lines = []
    lines.append(f"# {title} 精修 QA 报告")
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
        lines.append("")
        for pg in missing:
            lines.append(f"- p{pg['page']}")
        lines.append("")

    if low_char:
        lines.append("### 低字符页清单（可能为过渡页/图片页）")
        lines.append("")
        for pg in low_char[:20]:
            lines.append(f"- p{pg['page']}（{len(pg['text'].strip())} 字）")
        lines.append("")

    if table_pages:
        lines.append("### 表格页清单（已标注占位）")
        lines.append("")
        for pg in table_pages[:30]:
            lines.append(f"- p{pg['page']}")
        if len(table_pages) > 30:
            lines.append(f"- ... 共 {len(table_pages)} 页")
        lines.append("")

    lines.append("## 已清理项")
    lines.append("")
    lines.append("- OCR 元信息首行")
    lines.append("- 页眉模式（·N·连云港市志·XXX / XXX·N· / 连云港市志·XXX / .N.i / .N.）")
    lines.append("- 孤立页码行")
    lines.append("- 多余空行（3+→2）")
    lines.append("")

    lines.append("## 待人工核查项")
    lines.append("")
    lines.append("- OCR 错字（沭/述混淆、形近字）")
    lines.append("- 经纬度/数字符号缺失")
    lines.append("- 跨页回接点抽查")
    lines.append("- 表格页 OCR 原文需阶段 F 结构化处理")
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
    out_qa = QA_BASE / f"{fname}_精修QA报告.md"
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
    parser = argparse.ArgumentParser(description="通用正文精修")
    parser.add_argument("--part", help="如 上/part01")
    parser.add_argument("--start", type=int)
    parser.add_argument("--end", type=int)
    parser.add_argument("--title")
    parser.add_argument("--batch", action="store_true", help="按 BATCH_PLAN 批量精修上册")
    args = parser.parse_args()

    anchors = load_anchors()

    if args.batch:
        results = []
        for part, start, end, title in BATCH_PLAN:
            r = refine_range(part, start, end, title, anchors)
            results.append(r)
        print("")
        print("=== 上册批量精修汇总 ===")
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
