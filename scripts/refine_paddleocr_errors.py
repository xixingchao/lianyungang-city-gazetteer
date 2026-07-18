#!/usr/bin/env python3
"""PaddleOCR 残留错误自动修正 — 针对 PaddleOCR 未能纠正的少量错误"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHAPTER_DIR = ROOT / "workbench" / "body_chapters" / "paddle_上"

CORRECTIONS = [
    # ── PaddleOCR 未能修正的残余错误 ──
    # 准→淮（PaddleOCR 还残留少量）
    (r"准海", "淮海"),
    (r"准河", "淮河"),
    (r"准阴", "淮阴"),
    (r"准安", "淮安"),
    (r"准盐", "淮盐"),
    (r"准沭", "淮沭"),
    (r"治准", "治淮"),
    (r"江准", "江淮"),
    (r"导准", "导淮"),
    (r"徐准", "徐淮"),
    # 糟运→漕运
    (r"糟运", "漕运"),
    # 尽夜→昼夜
    (r"尽夜", "昼夜"),
    # 圆林寺→园林寺
    (r"圆林寺", "园林寺"),
    # 同治→同知（但"同治"也可能是年号，需谨慎：仅在"海州同治"中替换）
    (r"海州同治", "海州同知"),
    # 收人→收入（PaddleOCR 残留极少量）
    (r"收人(?!员|数|口|手)", "收入"),
    # 窜人→窜入
    (r"窜人", "窜入"),
    # 干→千（数字）
    (r"干瓦", "千瓦"),
    (r"干字", "千字"),
    (r"干米", "千米"),
    (r"干克", "千克"),
    (r"干吨", "千吨"),
    (r"干元", "千元"),
    (r"干亩", "千亩"),
    (r"干升", "千升"),
    (r"干克", "千克"),
    # 帐→账
    (r"台帐", "台账"),
    (r"记帐", "记账"),
    (r"转帐", "转账"),
    (r"帐簿", "账簿"),
    (r"帐单", "账单"),
    (r"帐目", "账目"),
    (r"欠帐", "欠账"),
    (r"帐号", "账号"),
    (r"帐务", "账务"),
    (r"算帐", "算账"),
    (r"呆帐", "呆账"),
    # 座标系→坐标系
    (r"座标系", "坐标系"),
    # 复盖→覆盖
    (r"复盖(?!率|面|层)", "覆盖"),
    # 高梁→高粱
    (r"高梁(?!桥|庄|乡|镇|村|路|街|巷)", "高粱"),
    # 辨/辩
    (r"辩别", "辨别"),
    # 拔/拨
    (r"拔款", "拨款"),
    # 叠夜→昼夜
    (r"叠夜", "昼夜"),
    # 兰→蓝
    (r"兰色", "蓝色"),
    (r"兰天", "蓝天"),
    # 即/既
    (r"既使", "即使"),
    (r"即然", "既然"),
    # 象/像
    (r"好象", "好像"),
    # 州/洲
    (r"沙州(?!市|县|区|镇)", "沙洲"),
    (r"绿州", "绿洲"),
    # 做/作
    (r"做工(?!厂|具|艺|程|人)", "作工"),
    # 余/馀
    (r"余(?!额|款|粮|钱|利|波|热|震|光|地|力|姚|杭|杭)", "馀"),
]

CHAPTER_FILES = [
    "序与凡例.md",
    "总述与大事记.md",
    "第一卷_自然环境.md",
    "第二卷_建置区划.md",
    "第三卷_区县概况.md",
    "第四卷_人口（part01_部分）.md",
    "第四卷至第十卷（part02）.md",
    "第十卷至第十六卷（part03）.md",
]


def main():
    total_fixes = 0
    for fname in CHAPTER_FILES:
        fpath = CHAPTER_DIR / fname
        if not fpath.exists():
            continue
        text = fpath.read_text(encoding="utf-8")
        original = text
        fixes = 0
        for pattern, replacement in CORRECTIONS:
            new_text, count = re.subn(pattern, replacement, text)
            if count > 0:
                fixes += count
                text = new_text

        if fixes > 0:
            # 备份
            backup = fpath.with_suffix(fpath.suffix + ".paddle_backup")
            backup.write_text(original, encoding="utf-8")
            fpath.write_text(text, encoding="utf-8")
            print(f"[{fname}] {fixes} 处修正")
            total_fixes += fixes
        else:
            print(f"[{fname}] 无需修正")

    print(f"\n总计修正: {total_fixes} 处")


if __name__ == "__main__":
    main()
