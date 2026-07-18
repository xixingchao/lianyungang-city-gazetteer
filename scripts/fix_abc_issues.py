#!/usr/bin/env python3
"""
修复上册 A/B 类格式问题：

A. 标题缺少空格
   - "第一章建置" → "第一章 建置"
   - "第一节地质" → "第一节 地质"
   - "第一章#" → "第一章"（去除垃圾字符）
   - "第一节•水系" → "第一节 水系"（点号替换为空格）

B. OCR残留错字（第二轮遗漏的）
   - 两干→两千, 戊成→戊戌
   - 盲自→盲目, 稀蔬→稀疏
   - 农車业→农副业

C. 暂不自动处理（需人工判断哪些是合法的总目录内容）
"""

import os
import re
import glob
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

BODY_DIR = Path(__file__).resolve().parent.parent / "workbench" / "body_chapters" / "上"
files = sorted(glob.glob(os.path.join(BODY_DIR, '*.md')))
files = [f for f in files if '汇总' not in f and '.backup' not in f]


# ============================================================
# A 修复：标题缺少空格
# ============================================================

def fix_title_spacing(text):
    """修复标题中缺少的空格"""
    fixes = []
    lines = text.split('\n')
    new_lines = []
    for line in lines:
        stripped = line.strip()
        # 跳过 markdown 标题行
        if stripped.startswith('#'):
            new_lines.append(line)
            continue

        original = line
        count = 0

        # A1: "第一章建置" → "第一章 建置"（卷/章/节后紧跟汉字）
        new_line = re.sub(
            r'(第[一二三四五六七八九十\d]+)卷([^\s）\)\)\]\-\—\~～\d\ni])',
            r'\1卷 \2', line
        )
        if new_line != line:
            count += 1
            line = new_line

        new_line = re.sub(
            r'(第[一二三四五六七八九十\d]+)章([^\s\#\·])',
            r'\1章 \2', line
        )
        if new_line != line:
            count += 1
            line = new_line

        new_line = re.sub(
            r'(第[一二三四五六七八九十\d]+)节([^\s\#\·\d])',
            r'\1节 \2', line
        )
        if new_line != line:
            count += 1
            line = new_line

        # A2: "第一节•水系" "第四章气候·" → "第一节 水系" "第四章 气候"
        new_line = re.sub(
            r'(第[一二三四五六七八九十\d]+[章节])[·‧•]',
            r'\1 ', line
        )
        if new_line != line:
            count += 1
            line = new_line

        # A3: "第一章#" → "第一章"（去掉垃圾字符）
        new_line = re.sub(
            r'(第[一二三四五六七八九十\d]+[章节])#',
            r'\1', line
        )
        if new_line != line:
            count += 1
            line = new_line

        # A4: "第一章建 置" → "第一章 建置"（章/节后多余空格规范化为一个空格）
        new_line = re.sub(
            r'(第[一二三四五六七八九十\d]+[章节])\s+([^\s])',
            r'\1 \2', line
        )
        if new_line != line:
            count += 1
            line = new_line

        # A5: 节后跟明显 OCR 残字（单字且非正常章节名成分）
        new_line = re.sub(
            r'(第[一二三四五六七八九十\d]+节)[垒角]',
            r'\1 ', line
        )
        if new_line != line:
            count += 1
            line = new_line

        if count > 0:
            before = original.strip()[:70]
            after = line.strip()[:70]
            fixes.append(f"  {before} → {after}")
        new_lines.append(line)

    return '\n'.join(new_lines), fixes


# ============================================================
# B 修复：OCR残留错字
# ============================================================

OCR_FIXES = [
    ('两干', '两千', '两干→两千'),
    ('戊成', '戊戌', '戊成→戊戌'),
    ('盲自', '盲目', '盲自→盲目'),
    ('稀蔬', '稀疏', '稀蔬→稀疏'),
    ('农車业', '农副业', '农車业→农副业'),
    ('农車', '农副', '农車→农副'),
]


def fix_ocr_errors(text):
    fixes = []
    for old, new, desc in OCR_FIXES:
        count = text.count(old)
        if count > 0:
            text = text.replace(old, new)
            fixes.append(f"  [{desc}] x{count}")
    return text, fixes


# ============================================================
# 主流程
# ============================================================

def main():
    dry_run = '--dry-run' in sys.argv
    mode = "预览" if dry_run else "执行"

    print(f"{'='*60}")
    print(f"[{mode}] 上册 A/B 格式问题修复")
    print(f"{'='*60}")

    total_a = 0
    total_b = 0

    for fp in files:
        basename = os.path.basename(fp)
        print(f"\n--- {basename} ---")

        with open(fp, 'r', encoding='utf-8') as f:
            original = f.read()

        text = original
        a_fixes = []
        b_fixes = []

        # A. 标题缺少空格
        text, a_fixes = fix_title_spacing(text)

        # B. OCR 错字
        text, b_fixes = fix_ocr_errors(text)

        if a_fixes:
            print(f"  A. 标题缺少空格: {len(a_fixes)}处")
            for f in a_fixes[:15]:
                print(f"    {f}")
            if len(a_fixes) > 15:
                print(f"    ... 还有{len(a_fixes)-15}处")
        else:
            print(f"  A. 标题缺少空格: 无")

        if b_fixes:
            print(f"  B. OCR残留错字: {len(b_fixes)}处")
            for f in b_fixes:
                print(f"    {f}")
        else:
            print(f"  B. OCR残留错字: 无")

        total_a += len(a_fixes)
        total_b += len(b_fixes)

        if not dry_run and text != original:
            backup_path = fp + '.abc_backup'
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(original)
            with open(fp, 'w', encoding='utf-8') as f:
                f.write(text)

    print(f"\n{'='*60}")
    print(f"总计:")
    print(f"  A. 标题空格修复: {total_a}处")
    print(f"  B. OCR错字修复: {total_b}处")
    if dry_run:
        print(f"** 预览模式，未实际修改文件 **")
        print(f"** 运行不带 --dry-run 参数以执行修复 **")
    else:
        print(f"** 修复已执行，备份以 .abc_backup 后缀保存 **")
    print(f"{'='*60}")


if __name__ == '__main__':
    main()
