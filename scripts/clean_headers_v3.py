# -*- coding: utf-8 -*-
"""
页眉页脚彻底清理 V3 — 精细模式，区分正文中合法的·与页眉中的·

核心思路：页眉/页码行出现在每页开头，行短（通常<20字符），
且不含引号、括号等正文标点。
"""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def is_header_or_page_num(line: str) -> bool:
    """
    判断单独一行是否是页眉或页码（应被移除）。
    """
    s = line.strip()
    if not s:
        return False

    # 乱码装饰线（OCR 错误，可能很长）优先检测
    if re.match(r"^[\dA-Za-z]{10,}$", s):
        return True

    # 行太长的不太可能是页眉
    if len(s) > 50:
        return False

    # ── 明确是页眉的模式 ──

    # ·N·连云港市志·XXX
    if re.match(r"^·\s*\d+\s*·\s*连云港市志", s):
        return True

    # XXX·N· 或 XXX·N （章节页眉，如"序·1"、"总述·3"、"第一章地质地貌·97"、"大事记·"、"总篇目·1·"）
    # 也匹配"第一章 地质地貌·101"、"第二章 海洋捕捞·615"、"溉·557"、"产·667"
    # 也匹配"第四章麻、毛、丝织·779"（含顿号/逗号）
    # 特征：含汉字/中文标点 + · + 数字（或数字+·/.结尾）
    # 排除：含括号的（如"日期(月·日)"）、含书名号的正文引用
    if re.match(r"^[\u4e00-\u9fff\w\s\u3001\uff0c]{1,50}\s*·\s*\d+\s*\.?\s*·?\s*$", s):
        if "(" not in s and ")" not in s and "\u300a" not in s:
            return True

    # "大事记·"（章节页眉，后面跟数字但不在这行）
    if re.match(r"^[\u4e00-\u9fff]{2,10}\s*·\s*$", s):
        return True

    # 页码后置：144·、292· 等
    if re.match(r"^\d{1,4}\s*·\s*$", s):
        return True

    # · N·连云港市志·XXX（带空格版）
    if re.match(r"^·\s*\d+\s*·\s*连云港市志", s):
        return True

    # ── 书名行 ──
    if s == "连云港市志":
        return True

    # ── 目录页页码引用：…(595) 或 · (281) ──
    if re.match(r"^[·….]*\s*\(\d+\)\s*$", s):
        return True

    # ── 孤立页码：1-4位数字，非年份 ──
    # 排除年份（如"1949"），只清理孤立的小页码
    if re.match(r"^\d{1,3}$", s):
        return True

    # ── 乱码装饰线（OCR 错误识别为数字字母串，如 3111111111118111111111111111111111114） ──
    if re.match(r"^[\dA-Za-z]{10,}$", s):
        return True

    # ── 纯标点/空格/· ──
    if re.match(r"^[\s·….,;:!?、，。；：！？\-\—]*$", s):
        return True

    return False


def clean_chapter_text(text: str) -> str:
    """
    清理分章 MD 文本中的页眉页码行。
    逐行处理，保留标题和注释。
    """
    lines = text.split("\n")
    cleaned = []

    for line in lines:
        stripped = line.strip()

        # 保留标题、注释、分隔线
        if stripped.startswith("#") or stripped.startswith("<!--") or stripped == "---":
            cleaned.append(line)
            continue

        # 空行保留
        if not stripped:
            cleaned.append(line)
            continue

        # 检测页眉/页码
        if is_header_or_page_num(line):
            continue

        cleaned.append(line)

    result = "\n".join(cleaned)
    # 压缩多余空行
    result = re.sub(r"\n{3,}", "\n\n", result)
    result = re.sub(r"^\n+", "", result)
    result = re.sub(r"\n+$", "\n", result)
    return result


def main():
    chapter_dir = ROOT / "workbench" / "body_chapters" / "paddle_上"
    md_files = sorted(chapter_dir.glob("*.md"))

    total_removed = 0

    for fp in md_files:
        original = fp.read_text(encoding="utf-8")
        cleaned_text = clean_chapter_text(original)

        # 统计移除行数
        orig_lines = len(original.split("\n"))
        new_lines = len(cleaned_text.split("\n"))
        removed = orig_lines - new_lines

        fp.write_text(cleaned_text, encoding="utf-8")
        total_removed += removed
        print(f"  {fp.name}: -{removed} 行")

    print(f"\n总计移除: {total_removed} 行")

    # 最终验证
    print("\n=== 最终残留验证 ===")
    for fp in md_files:
        text = fp.read_text(encoding="utf-8")
        lines = text.split("\n")
        suspects = []
        for i, line in enumerate(lines):
            s = line.strip()
            if not s or s.startswith("#") or s.startswith("<!--"):
                continue
            if is_header_or_page_num(line):
                suspects.append((i + 1, s))
        if suspects:
            print(f"  {fp.name}: {len(suspects)} 残留")
            for ln, content in suspects[:5]:
                print(f"    L{ln}: [{content}]")


if __name__ == "__main__":
    main()
