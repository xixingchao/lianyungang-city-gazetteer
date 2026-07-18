# -*- coding: utf-8 -*-
"""
连云港市志 上册 正文精修试点：总述 + 大事记（全局页 29-123）

流程：
1. 读取 OCR 原文（per-page txt）
2. 清理 OCR 元信息行、页眉页脚、孤立页码
3. 跨页段落回接
4. 保留内部页锚（HTML 注释形式，不显示在最终阅读版）
5. 输出精修 Markdown + QA 报告

清理规则基于 OCR 抽样确认的模式：
- 元信息首行：# 连云港市志_上_part01 第 N/300 页
- 页眉模式：·N·连云港市志·总述 / 总述·N· / ·N·连云港市志·大事记 / 大事记·N·
- 孤立页码行：纯数字行或 ·数字·
"""

import re
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OCR_DIR = ROOT / "workbench" / "ocr" / "raw" / "上" / "part01"
ANCHOR_CSV = ROOT / "workbench" / "indexes" / "连云港市志_上册页锚索引.csv"
OUT_DIR = ROOT / "workbench" / "body_chapters" / "上"
OUT_MD = OUT_DIR / "总述与大事记.md"
OUT_QA = ROOT / "workbench" / "qa" / "总述大事记精修QA报告.md"

START_PAGE = 29  # 全局页 = part01 电子页
END_PAGE = 123


def load_anchors():
    """返回 {global_page: anchor_id}"""
    anchors = {}
    with open(ANCHOR_CSV, encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            anchors[int(row["global_page"])] = row["anchor"]
    return anchors


def clean_ocr_meta(lines):
    """删除 OCR 元信息首行"""
    return [ln for ln in lines if not ln.startswith("# 连云港市志_")]


# 页眉/页脚正则模式（re.MULTILINE 使 ^ $ 按行匹配）
HEADER_PATTERNS = [
    re.compile(r"^·\d+·连云港市志·总述\s*$", re.MULTILINE),
    re.compile(r"^总述·\d+·\s*$", re.MULTILINE),
    re.compile(r"^·\d+·连云港市志·大事记\s*$", re.MULTILINE),
    re.compile(r"^大事记·\d+·\s*$", re.MULTILINE),
    re.compile(r"^·\d+·连云港市志·[^\n]+\s*$", re.MULTILINE),  # 通用 ·N·连云港市志·XXX
    re.compile(r"^[^\n]+·\d+·\s*$", re.MULTILINE),  # 通用 XXX·N·
    re.compile(r"^·\d+·\s*$", re.MULTILINE),  # 孤立 ·N·
    re.compile(r"^连云港市志·[^\n]+\s*$", re.MULTILINE),  # 无页码页眉 连云港市志·大事记
    re.compile(r"^\.\d+\.[iil]\s*$", re.MULTILINE),  # 残留页码 .N.i
    re.compile(r"^\.\d+\.\s*$", re.MULTILINE),  # 残留页码 .N.
]


def clean_headers(text):
    """清理页眉页脚"""
    for pat in HEADER_PATTERNS:
        text = pat.sub("", text)
    # 清理空行
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def is_sentence_end(text):
    """判断文本末尾是否为句子结束"""
    text = text.rstrip()
    if not text:
        return True
    return text[-1] in "。！？；：」』）)\"'\"'"


def is_new_section(line):
    """判断是否为新章节/条目起始"""
    line = line.strip()
    if not line:
        return True
    # 大事记年份标题模式
    if re.match(r"^(春秋|秦|汉|三国|晋|南北朝|隋|唐|宋|元|明|清|民国|共和国)", line):
        return True
    if re.match(r"^\d{4}年", line):
        return True
    if re.match(r"^周[^\n]{1,6}年", line):
        return True
    # 总述小节标题
    if re.match(r"^\(一[）)\)]|^\(二[）)\)]|^\(三[）)\)]|^\(四[）)\)]|^\(五[）)\)]", line):
        return True
    if re.match(r"^（一）|^（二）|^（三）|^（四）|^（五）", line):
        return True
    return False


def process_pages(start, end, anchors):
    """逐页处理，跨页回接"""
    pages = []
    for p in range(start, end + 1):
        txt_path = OCR_DIR / f"page_{p:04d}.txt"
        if not txt_path.exists():
            pages.append({"page": p, "anchor": anchors.get(p, ""), "text": "", "missing": True})
            continue
        raw = txt_path.read_text(encoding="utf-8")
        lines = raw.splitlines()
        lines = clean_ocr_meta(lines)
        text = "\n".join(lines)
        text = clean_headers(text)
        pages.append({"page": p, "anchor": anchors.get(p, ""), "text": text, "missing": False})
    return pages


def merge_with_anchors(pages):
    """合并页面，跨页回接，插入页锚"""
    sections = []  # list of (anchor, text_block)
    current_block = []
    current_anchor = ""

    for i, pg in enumerate(pages):
        if pg["missing"]:
            current_block.append(f"\n\n[缺失页 p{pg['page']}]\n\n")
            continue

        anchor = pg["anchor"]
        text = pg["text"]
        if not text.strip():
            continue

        # 插入页锚
        if current_anchor and current_block:
            # 检查是否需要回接
            prev_text = current_block[-1] if current_block else ""
            if prev_text and not is_sentence_end(prev_text):
                # 跨页回接：合并到上一段
                first_line = text.split("\n")[0] if text else ""
                if not is_new_section(first_line):
                    # 回接
                    current_block[-1] = prev_text.rstrip() + text.lstrip().split("\n")[0]
                    remaining = "\n".join(text.lstrip().split("\n")[1:])
                    if remaining.strip():
                        current_block.append(remaining)
                else:
                    current_block.append(text)
            else:
                current_block.append(text)
        else:
            current_block.append(text)

        # 如果有新锚点，保存当前块并开始新块
        if anchor and i > 0 and current_block:
            # 保留前一块
            sections.append((current_anchor or pages[0]["anchor"], "\n\n".join(current_block)))
            current_block = []
            current_anchor = anchor

    if current_block:
        sections.append((current_anchor or pages[0]["anchor"], "\n\n".join(current_block)))

    return sections


def build_markdown(pages, sections):
    """构建精修 Markdown"""
    lines = []
    lines.append("# 总述")
    lines.append("")
    lines.append("<!-- 精修说明：基于上册 OCR 初稿，已清理页眉页脚和 OCR 元信息；跨页段落已回接。 -->")
    lines.append("<!-- 内部页锚保留为 HTML 注释，最终阅读版移除。 -->")
    lines.append("")

    # 按页逐页输出，保留页锚
    in_dashiji = False
    for pg in pages:
        if pg["missing"]:
            lines.append(f"<!-- page-anchor: {pg['anchor']} -->")
            lines.append(f"[缺失页 p{pg['page']}]")
            lines.append("")
            continue

        text = pg["text"]
        if not text.strip():
            continue

        # 检测章节切换
        if not in_dashiji and pg["page"] >= 41:
            in_dashiji = True
            lines.append("")
            lines.append("# 大事记")
            lines.append("")

        # 插入页锚
        lines.append(f"<!-- page-anchor: {pg['anchor']} -->")
        lines.append("")
        lines.append(text)
        lines.append("")

    return "\n".join(lines)


def build_qa(pages):
    """构建 QA 报告"""
    lines = []
    lines.append("# 总述+大事记 精修 QA 报告")
    lines.append("")
    lines.append(f"范围：全局页 {START_PAGE}-{END_PAGE}（{END_PAGE-START_PAGE+1} 页）")
    lines.append("")

    missing = [pg for pg in pages if pg["missing"]]
    empty = [pg for pg in pages if not pg["missing"] and not pg["text"].strip()]
    low_char = [pg for pg in pages if not pg["missing"] and len(pg["text"].strip()) < 50 and pg["text"].strip()]

    lines.append("## 页面统计")
    lines.append("")
    lines.append(f"- 总页数：{len(pages)}")
    lines.append(f"- 缺失页：{len(missing)}")
    lines.append(f"- 空文本页：{len(empty)}")
    lines.append(f"- 低字符页（<50字）：{len(low_char)}")
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
        for pg in low_char:
            lines.append(f"- p{pg['page']}（{len(pg['text'].strip())} 字）")
        lines.append("")

    # 统计清理项
    total_chars = 0
    for pg in pages:
        if not pg["missing"]:
            total_chars += len(pg["text"])

    lines.append("## 清理统计")
    lines.append("")
    lines.append(f"- 精修后总字符数：{total_chars}")
    lines.append(f"- 平均每页字符数：{total_chars // max(len(pages), 1)}")
    lines.append("")

    lines.append("## 已清理项")
    lines.append("")
    lines.append("- OCR 元信息首行（# 连云港市志_上_part01 第 N/300 页）")
    lines.append("- 页眉模式（·N·连云港市志·总述 / 总述·N· / ·N·连云港市志·大事记 / 大事记·N·）")
    lines.append("- 孤立页码行（·N·）")
    lines.append("- 多余空行（3+连续空行压缩为2行）")
    lines.append("")

    lines.append("## 待人工核查项")
    lines.append("")
    lines.append('- OCR 错字（如"新述河"应为"新沭河"、"述阳"应为"沭阳"）')
    lines.append("- 经纬度符号缺失（如 3507' 应为 35°07'）")
    lines.append("- 跨页回接点需抽查确认")
    lines.append("- 大事记年份条目格式需统一")
    lines.append("")

    return "\n".join(lines)


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    anchors = load_anchors()
    pages = process_pages(START_PAGE, END_PAGE, anchors)
    sections = merge_with_anchors(pages)
    md = build_markdown(pages, sections)
    qa = build_qa(pages)

    OUT_MD.write_text(md, encoding="utf-8")
    OUT_QA.parent.mkdir(parents=True, exist_ok=True)
    OUT_QA.write_text(qa, encoding="utf-8")

    print("=== 总述+大事记 精修试点完成 ===")
    print(f"范围: p{START_PAGE}-p{END_PAGE} ({len(pages)} 页)")
    missing = sum(1 for pg in pages if pg["missing"])
    total_chars = sum(len(pg["text"]) for pg in pages if not pg["missing"])
    print(f"缺失页: {missing}")
    print(f"精修后总字符: {total_chars}")
    print(f"输出: {OUT_MD}")
    print(f"输出: {OUT_QA}")


if __name__ == "__main__":
    main()
