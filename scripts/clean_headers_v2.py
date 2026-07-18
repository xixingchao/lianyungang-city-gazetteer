# -*- coding: utf-8 -*-
"""
页眉页脚彻底清理 V2 — 覆盖 PaddleOCR 所有残留模式

基于东辛农场志成品标准：最终阅读版不应有任何页眉、页码、书名行。
"""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# ── 需要清理的行级模式（按行匹配） ──

# 1. OCR 元信息首行
OCR_META = re.compile(r"^# 连云港市志_.*$")

# 2. 标准页眉：·N·连云港市志·XXX
STD_HEADER = re.compile(
    r"^·\s*\d+\s*·\s*连云港市志\s*·\s*[\u4e00-\u9fff（）()\w]{1,30}\s*$"
)

# 3. 反向页眉：XXX·N· 或 XXX·N  (章节名+页码)
REV_HEADER = re.compile(
    r"^[\u4e00-\u9fff（）()\w]{2,25}\s*·\s*\d+\s*·?\s*$"
)

# 4. 书名页眉：单独一行的"连云港市志"
BOOK_TITLE_LINE = re.compile(r"^\s*连云港市志\s*$")

# 5. 孤立页码行（纯数字，1-4位）
ISOLATED_PAGE_NUM = re.compile(r"^\s*\d{1,4}\s*$")

# 6. 目录页页码引用：· (N) 或 …(N)
TOC_PAGE_REF = re.compile(r"^\s*[·….]+\s*\(\d+\)\s*$")

# 7. 乱码装饰线（OCR把装饰线识别成数字字母串）
DECORATION_NOISE = re.compile(r"^\s*[\dA-Za-z]{8,}\s*$")

# 8. 单行书名行（非段落）
SHORT_TITLE = re.compile(r"^\s*《[\u4e00-\u9fff（）()\w]+》\s*$")

# 9. 纯空白/标点行
BLANK_LIKE = re.compile(r"^\s*[·…\.,;:!?、，。；：！？\-\—\s]*\s*$")


def is_page_header_line(line: str, prev_line: str, next_line: str) -> bool:
    """
    判断一行是否是页眉/页码干扰。
    页眉/页码通常特征：行短、位于每页开头、不构成连续段落。
    """
    s = line.strip()
    if not s:
        return False

    # OCR 元信息
    if OCR_META.match(s):
        return True

    # 标准页眉
    if STD_HEADER.match(s):
        return True

    # 反向页眉（章节·页码）
    if REV_HEADER.match(s):
        return True

    # 书名行（单独的"连云港市志"）
    if BOOK_TITLE_LINE.match(s):
        return True

    # 目录页页码引用：· (650)
    if TOC_PAGE_REF.match(s):
        return True

    # 乱码装饰线（10个以上数字字母）
    if DECORATION_NOISE.match(s):
        return True

    # 孤立页码：1-4位纯数字，且前后行都不像正文
    if ISOLATED_PAGE_NUM.match(s):
        # 仅当它是孤立的（前后行至少有一个空行）
        if not prev_line.strip() or not next_line.strip():
            return True

    # 纯标点/空格
    if BLANK_LIKE.match(s):
        return True

    return False


def clean_page_text(text: str) -> str:
    """
    清理单页 OCR 文本中的页眉页脚。
    输入：单页原始 OCR 文本
    输出：清理后的文本
    """
    lines = text.split("\n")

    # Step 1: 移除 OCR 元信息行
    lines = [ln for ln in lines if not OCR_META.match(ln)]

    # Step 2: 逐行检查，移除页眉/页码
    cleaned = []
    for i, line in enumerate(lines):
        prev_line = lines[i - 1] if i > 0 else ""
        next_line = lines[i + 1] if i < len(lines) - 1 else ""

        if is_page_header_line(line, prev_line, next_line):
            continue

        cleaned.append(line)

    # Step 3: 压缩多余空行（3+ → 2）
    result = "\n".join(cleaned)
    result = re.sub(r"\n{3,}", "\n\n", result)
    result = re.sub(r"^\n+", "", result)
    result = re.sub(r"\n+$", "\n", result)

    return result


def process_chapter_file(filepath: Path) -> tuple[int, int]:
    """
    处理单个分章 MD 文件，逐页清理页眉页码。
    返回：(清理的行数, 剩余可疑行数)
    """
    text = filepath.read_text(encoding="utf-8")
    lines = text.split("\n")

    # 统计清理前
    removed_count = 0
    new_lines = []
    i = 0
    while i < len(lines):
        line = lines[i]
        prev_line = lines[i - 1] if i > 0 else ""
        next_line = lines[i + 1] if i < len(new_lines) - 1 else ""

        # 不处理注释行、标题行
        stripped = line.strip()
        if stripped.startswith("#") or stripped.startswith("<!--"):
            new_lines.append(line)
            i += 1
            continue

        if is_page_header_line(line, prev_line, next_line):
            removed_count += 1
            i += 1
            continue

        new_lines.append(line)
        i += 1

    new_text = "\n".join(new_lines)
    # 再次压缩空行
    new_text = re.sub(r"\n{3,}", "\n\n", new_text)

    # 统计剩余可疑行
    remaining = 0
    for line in new_text.split("\n"):
        s = line.strip()
        if s and not s.startswith("#") and not s.startswith("<!--"):
            if REV_HEADER.match(s) or STD_HEADER.match(s) or TOC_PAGE_REF.match(s):
                remaining += 1
            # 也检查短行（3-8字符）含 · 且非正文
            elif len(s) <= 10 and "·" in s:
                remaining += 1

    filepath.write_text(new_text, encoding="utf-8")
    return removed_count, remaining


def main():
    chapter_dir = ROOT / "workbench" / "body_chapters" / "paddle_上"
    md_files = sorted(chapter_dir.glob("*.md"))

    total_removed = 0
    total_remaining = 0

    for fp in md_files:
        removed, remaining = process_chapter_file(fp)
        total_removed += removed
        total_remaining += remaining
        print(f"  {fp.name}: 移除 {removed} 行, 残留 {remaining} 行")

    print(f"\n总计: 移除 {total_removed} 行, 残留 {total_remaining} 行")


if __name__ == "__main__":
    main()
