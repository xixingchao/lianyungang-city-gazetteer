# -*- coding: utf-8 -*-
"""精修脚本：标点符号规范化 + PaddleOCR残留错字修正
读取 pace_上 分章MD文件，应用修正后写回。
保留备份为 .bak 文件。
"""

import re, json, shutil
from pathlib import Path

ROOT = Path(r"E:\codex_learing\09_project_东辛农场\连云港市志_workstation")
CH_DIR = ROOT / "workbench" / "body_chapters" / "paddle_上"
CHAPTER_ORDER = [
    "序与凡例.md", "总述与大事记.md", "第一卷_自然环境.md",
    "第二卷_建置区划.md", "第三卷_区县概况.md",
    "第四卷_人口（part01部分）.md",
    "第四卷至第十卷（part02）.md", "第十卷至第十六卷（part03）.md",
]

# ── 标点规范映射（半角→全角） ──
PUNCT_MAP = {
    ",": "，", ".": "。", ":": "：", ";": "；", "~": "～",
    "?": "？", "!": "！", "(": "（", ")": "）",
    "[": "【", "]": "【", '"': "\u201c", "'": "\u2018",
}

# ── OCR 错字修正映射（基于PaddleOCR常见错误模式） ──
OCR_FIXES = {
    # 形近字
    "准": "淮",  # 准河→淮河
    "辛": "幸",  # 辛福→幸福  (但东辛农场中的辛不应改,加下文限制)
    "辛": "辛",  # 保留
    "沭": "沭",  # 沭阳/沭河
    "述": "沭",  # 述阳→沭阳
    "糟": "漕",  # 糟运→漕运
    "尽": "昼",  # 尽夜→昼夜  (谨慎)
    "肓": "育",  # 教肓→教育
    "己": "已",  # 己经→已经
    "未": "末",  # 期未→期末 (谨慎)
    "井": "开",  # 井始→开始  (谨慎)
    "干": "于",  # 由干→由于
    "大": "太",  # 大平→太平
    "代": "伐",  # 年代→年伐? 反过来: 伐→代 (年代)
    "份": "分",  # 部份→部分  (但年份不改)
    "令": "今",  # 令天→今天
    "厂": "广",  # 厂大→广大
    "午": "年",  # 午份→年份 (谨慎)
}

# ── 带上下文限制的修正（避免误伤） ──
CONTEXT_FIXES = [
    # (错误模式, 上下文限制, 替换为)
    (r"准[河海江]", lambda m: "淮" + m.group(0)[1:]),  # 准河→淮河 准海→淮海
    (r"糟运", "漕运"),
    (r"尽夜", "昼夜"),
    (r"教肓", "教育"),
    (r"已[经将]", lambda m: "已" + m.group(0)[1:]),  # 已是正确,不改
    (r"由干", "由于"),
    (r"期未", "期末"),
]

# ── 上下文修正（复合模式，多字） ──
COMPOUND_FIXES = {
    "东辛农场": "东辛农场",  # 确认保留
    "公斤": "公斤", 
    "公顷": "公顷",
    "万亩": "万亩",
    "": "",
}


def fix_ocr_errors(text):
    """修正OCR残留错字"""
    # 上下文修正
    for pat, repl in CONTEXT_FIXES:
        text = re.sub(pat, repl if callable(repl) else repl, text)
    return text


def fix_punctuation(text):
    """标点符号半角→全角（正文内容，不含代码/标记）"""
    # 不处理 HTML 注释和模板标记
    def replace_in_text(segment):
        for half, full in PUNCT_MAP.items():
            segment = segment.replace(half, full)
        return segment

    # 分割: 保留注释和标记不被处理
    parts = re.split(r'(<!--.*?-->)', text, flags=re.DOTALL)
    result = []
    for part in parts:
        if part.startswith('<!--'):
            result.append(part)  # 跳过注释
        else:
            result.append(replace_in_text(part))
    return ''.join(result)


def process_file(fpath):
    """处理单个文件"""
    orig = fpath.read_text('utf-8')
    text = orig

    # 1. 标点规范化
    text = fix_punctuation(text)

    # 2. OCR错字修正
    text = fix_ocr_errors(text)

    if text == orig:
        print(f'  [不变] {fpath.name}')
        return False

    # 3. 备份
    bak = fpath.with_suffix(fpath.suffix + '.bak')
    if not bak.exists():
        shutil.copy2(fpath, bak)

    # 4. 写回
    fpath.write_text(text, 'utf-8')
    print(f'  [修正] {fpath.name}')
    return True


def main():
    total_fixed = 0
    for fname in CHAPTER_ORDER:
        fp = CH_DIR / fname
        if not fp.exists():
            alt = CH_DIR / fname.replace('(', '（').replace(')', '）')
            if alt.exists():
                fp = alt
            else:
                print(f'  [跳过] {fname}')
                continue
        if process_file(fp):
            total_fixed += 1
    print(f'\n完成！共处理 {total_fixed} 个文件')

    # 统计修正信息
    print()
    print('=== 标点规范化说明 ===')
    print('- 逗号: , → ，')
    print('- 句号: . → 。')
    print('- 冒号: : → ：')
    print('- 分号: ; → ；')
    print('- 问号: ? → ？')
    print('- 感叹号: ! → ！')
    print('- 括号: () → （）')
    print()
    print('=== OCR错字修正说明 ===')
    print('- 糟运→漕运, 尽夜→昼夜')
    print('- 教肓→教育, 由干→由于')
    print('- 准河→淮河, 期未→期末')
    print()
    print('注意：备份文件已保存为 .bak 后缀')


if __name__ == '__main__':
    main()
