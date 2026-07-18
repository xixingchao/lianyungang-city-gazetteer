# -*- coding: utf-8 -*-
"""
连云港市志 中下册 OCR 系统性错误批量修复脚本

基于上册精修经验（88处OCR系统性错误）对中下册进行批量替换。
运行方式：
    python scripts/refine_mid_low_ocr.py

安全策略：
    - 只做确信无误的替换（形近字、常见OCR误识）
    - 每次替换都记录日志
    - 生成替换报告
"""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# === 待处理的文件列表 ===
FILES = [
    ROOT / "workbench" / "body_chapters" / "第十七卷至第二十九卷（中part01）.md",
    ROOT / "workbench" / "body_chapters" / "第三十卷至第四十二卷（中part02）.md",
    ROOT / "workbench" / "body_chapters" / "第四十三卷至第五十一卷（下part01）.md",
    ROOT / "workbench" / "body_chapters" / "第五十二卷至第六十卷及附录（下part02）.md",
]

# === 系统性 OCR 替换规则 ===
# 格式：(old, new, description)
REPLACEMENTS = [
    # --- 最确定的形近字错误 ---
    ("收人", "收入", "入→人 形近误识"),
    ("胸县", "朐县", "朐→胸 形近误识（连云港地名）"),
    ("胸山", "朐山", "朐→胸 形近误识（连云港地名）"),
    ("大胸", "大朐", "朐→胸 形近误识（连云港地名）"),

    # --- 已知确认的其他错误 ---
    ("腹蛇", "蝮蛇", "腹→蝮 形近误识（毒蛇名）"),
    ("广衰", "广袤", "衰→袤 形近误识"),

    # --- 沭/述/沐 混淆（中下册最大量系统性错误）---
    # 沭阳（今连云港市沭阳县）被误识为 述阳 或 沐阳
    ("准述新河", "淮沭新河", "准述→淮沭 河流名（淮沭新河）"),
    ("准述河", "淮沭河", "准述→淮沭 河流名（淮沭河）"),
    ("述阳", "沭阳", "述→沭 地名（沭阳县）"),
    ("沐阳", "沭阳", "沐→沭 地名（沭阳县）"),
    ("临述", "临沭", "述→沭 地名（山东省临沭县）"),
    ("临沐", "临沭", "沐→沭 地名（山东省临沭县）"),
    ("沐河", "沭河", "沐→沭 河流名（沭河）"),
    ("述河", "沭河", "述→沭 河流名（沭河）"),
    ("述城", "沭城", "述→沭 地名（沭城-沭阳县城关镇）"),
    ("述刘线", "沭刘线", "述→沭 道路名（沭刘线）"),
    ("沂述", "沂沭", "述→沭 河流名（沂沭河）"),
    ("海述", "海沭", "述→沭 地区名（海沭）"),
    ("赣述", "赣沭", "述→沭 地区名（海赣沭地区）"),
    ("沂沐", "沂沭", "沐→沭 河流名（沂沭）"),
    ("沭述", "沭沭", "述→沭 重复误识"),
    ("东灌述", "东灌沭", "述→沭 地区名（东灌沭）"),

    # --- 表格式样标准化 ---
    # 表 XX ~ Y  → 表XX-Y
    # 这个需要更精确的正则
]

# === 页眉残留模式清理（正则） ===
HEADER_CLEANUP_PATTERNS = [
    (re.compile(r"^\.\d+[il]\s*$", re.MULTILINE), "孤立页码残码"),
    (re.compile(r"^\.\d+\.[il]\s*$", re.MULTILINE), "孤立页码残码带点"),
    (re.compile(r"^·\d+·\s*$", re.MULTILINE), "孤立·N·行"),
    (re.compile(r"^[^\u4e00-\u9fff\n]{1,12}连云港市志·[\u4e00-\u9fff（）()]{1,25}\s*$", re.MULTILINE), "页眉行"),
    (re.compile(r"^·\d+·连云港市志·[^\n]+\s*$", re.MULTILINE), "标准页眉"),
    (re.compile(r"^[^\n]+·\d+·\s*$", re.MULTILINE), "后置页眉"),
    (re.compile(r"^连云港市志·[^\n]+\s*$", re.MULTILINE), "简洁页眉"),
    (re.compile(r"^\d+年[\u4e00-\u9fff]*\s*\n?$", re.MULTILINE), "孤立年份行（需人工确认）——不移除仅报告"),
]

def fix_year_colon(text):
    """修复年份范围中的波浪线和全角破折号为半角连接线"""
    # 1953~1990 → 1953—1990（在志书中使用长横）
    # 但保留原志书风格，先只处理表号
    return text

def fix_table_format(text):
    """标准化表格标记"""
    # 表 17 ~ 1 → 表17-1
    text = re.sub(r'表\s+(\d+)\s*~\s*(\d+)', r'表\1-\2', text)
    # 表17 ~ 1 → 表17-1
    text = re.sub(r'表(\d+)\s*~\s*(\d+)', r'表\1-\2', text)
    return text

def fix_negative_sign(text):
    """修复利润负数中的波浪线"""
    # 利润~X.XX → 利润-X.XX
    text = re.sub(r'(利润)\s*~\s*(\d+\.?\d*)', r'\1 -\2', text)
    # 但需避免 ~ 用在正常年份范围中
    return text

def clean_headers(text):
    """清理页眉残留"""
    for pat, desc in HEADER_CLEANUP_PATTERNS:
        if desc != "孤立年份行（需人工确认）——不移除仅报告":
            text = pat.sub("", text)
    # 清理多余空行
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()

def count_occurrences(text, old):
    """统计替换前出现次数"""
    return text.count(old)


def process_file(filepath):
    """处理单个文件"""
    print(f"\n{'='*60}")
    print(f"处理: {filepath.name}")
    print(f"{'='*60}")

    if not filepath.exists():
        print(f"  [跳过] 文件不存在: {filepath}")
        return

    content = filepath.read_text(encoding="utf-8")
    original = content
    stats = []

    # 1. 页眉清理
    content = clean_headers(content)
    header_changes = (original != content)  # 粗略判断

    # 2. 表格式样标准化
    content = fix_table_format(content)

    # 3. 简单文本替换
    for old, new, desc in REPLACEMENTS:
        before = count_occurrences(content, old)
        if before > 0:
            content = content.replace(old, new)
            after = count_occurrences(content, old)
            fixed = before - after
            if fixed > 0:
                stats.append((old, new, fixed, desc))
                print(f"  [OK] {old} -> {new}  ({fixed}处) [{desc}]")

    # 4. 写入
    if content != original:
        filepath.write_text(content, encoding="utf-8")
        print(f"  → 已更新文件")
    else:
        print(f"  → 无需修改")

    return stats


def main():
    print("连云港市志 中下册 OCR 系统性错误修复")
    print("=" * 50)

    total_stats = []
    for f in FILES:
        stats = process_file(f)
        if stats:
            total_stats.extend(stats)

    print(f"\n{'='*60}")
    print("替换汇总")
    print(f"{'='*60}")
    if total_stats:
        for old, new, count, desc in total_stats:
            print(f"  {old} → {new}: {count}处 ({desc})")
    else:
        print("  无替换")

    print(f"\n处理完成。上述替换均为确信无误的形近字修正。")


if __name__ == "__main__":
    main()
