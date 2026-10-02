# -*- coding: utf-8 -*-
"""批次4前置：v2 中「一X一Y」汉字链的逐token分类（连接号 一→— 候选）。

背景：批次1 已把数字位「一」→「~」修掉 13 处，但路线/序列/地层等连接位上的
「一」（原书应为连接号「—」）未处理，共 259 处进待核清单（dash_chain.json）。
本脚本对 v2 逐 token 判定：连接号（应改「—」）还是真汉字「一」（保留）。

用法：python classify_v2_dash_chains_20261002.py [--apply]
默认 dry-run，只输出分类结果；--apply 才写回 v2 + 阅读版 HTML。
"""
from __future__ import annotations

import argparse
import io
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
V2 = ROOT / "workbench" / "body_chapters_v2"
READER = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT = ROOT / "output" / "reports" / "progress" / "20261002_批次4_连接号一X一Y核定.md"

DASH_CHAIN = re.compile(r"[\u4e00-\u9fff]一[\u4e00-\u9fff]{1,}一[\u4e00-\u9fff]")
ANCH = re.compile(r"<!--\s*page-anchor:\s*([A-Za-z0-9\-]+)\s*-->")

# 真汉字「一」词表（词首）
W_HEAD = (
    "进一步", "一个", "一次", "一般", "一切", "一直", "一样", "一边", "一带", "一行", "一支", "一名",
    "一对", "一系列", "一致", "一共", "一齐", "一同", "一律", "一旦", "一层", "一片", "一线", "一日",
    "一年", "一月", "一起", "一再", "一贯", "一定", "一流", "一体", "一并", "一览", "一经", "一心",
    "一手", "一头", "一批", "一类", "一种", "一条", "一座", "一道", "一时", "一所", "一格", "一页",
    "一号", "一节", "一班", "一组", "一队", "一例", "一色", "一揽子", "一回事", "一览表", "一应",
    "一隅", "一斑", "一脉", "一席", "一端", "一侧", "一转", "一瞬", "一准", "一总", "一...", "一系列",
    "一五", "一化", "一平", "一期", "一号", "一村", "一区", "一线", "一校", "一厂", "一站", "一军",
    "一营", "一连", "一团", "一族", "一科", "一属", "一系",
    # 补（2026-10-02 逐行核对后新增）
    "一夜", "一块", "一届", "一路", "一番", "一栋", "一棵", "一孔", "一张", "一幅", "一帧", "一册",
    "一本", "一卷", "一部", "一处", "一局", "一县", "一市", "一省", "一国", "一乡", "一镇", "一街",
    "一型", "一式", "一级", "一等", "一波", "一阵", "一场", "一趟", "一回", "一顿", "一口", "一户",
    "一家", "一间", "一室", "一厅", "一楼", "一桥", "一坝", "一渠", "一塘", "一井", "一库", "一院",
    "一版", "一台", "一套", "一宗", "一轴", "一柱", "一节", "一支", "一旅", "一师", "一排", "一班",
    "一壁", "一则", "一者", "一斑", "一色", "一统", "一任", "一似", "一霎", "一晌", "一早", "一晚",
    "一夕", "一朝", "一翼", "一环", "一层", "一道", "一线", "一例", "一隅", "一席", "一端", "一侧",
)
# 真汉字「一」词表（词尾：前面那个字 + 一 构成词）
W_TAIL = (
    "十一", "第一", "统一", "同一", "唯一", "之一", "其一", "单一", "不一", "万一", "划一", "均一",
    "专一", "纯一", "如一", "数十", "百一", "千一", "数一", "二一", "三一", "四一", "五一", "六一",
    "七一", "八一", "九一", "十一", "二十一", "三十一", "四十一", "五十一", "六十一", "七十一",
    "八十一", "九十一", "一百一", "千一", "万一",
)
# 真汉字「一」的固定结构
W_MID = ("一一", "一五一十", "数一数二", "说一不二", "一分为二", "合二为一", "三位一体")


def classify(line: str, start: int, end: int):
    """对 [start,end) 区间内的每个「一」判定：True=真汉字，False=连接号候选。

    词表按「token 位于词的任意位置」匹配：一在词中（进一步/单一/一行/第一…）都算真汉字。
    """
    words = tuple(dict.fromkeys(W_HEAD + W_TAIL))
    verdicts = []
    for i in range(start, end):
        if line[i] != "一":
            continue
        contained = False
        for w in words:
            for off in range(len(w)):
                if w[off] == "一" and i - off >= 0 and line[i - off:i - off + len(w)] == w:
                    contained = True
                    break
            if contained:
                break
        # 固定结构（一一 / 一五一十 / 数一数二 …）
        mid = any(w in line[max(0, i - 4):i + 5] for w in W_MID)
        dup = (i > 0 and line[i - 1] == "一") or (i + 1 < len(line) and line[i + 1] == "一")
        verdicts.append((i, not (contained or mid or dup),
                         line[max(0, i - 3):i], line[i + 1:i + 5]))
    return verdicts


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    cases = []          # (file, line_no, anchor, line, [connector positions])
    genuine = []
    for f in sorted(V2.glob("*.md")):
        anchor = None
        for ln, line in enumerate(io.open(f, encoding="utf-8").read().splitlines(), 1):
            m = ANCH.search(line)
            if m:
                anchor = m.group(1)
                continue
            for mm in DASH_CHAIN.finditer(line):
                vs = classify(line, mm.start(), mm.end())
                conn = [v[0] for v in vs if v[1]]
                if conn:
                    cases.append((f.name, ln, anchor, line, conn))
                if any(not v[1] for v in vs):
                    genuine.append((f.name, ln, [v for v in vs if not v[1]], line))

    print(f"含「一X一Y」链的行: {len(cases) + 0} 行（其中连接号候选 {sum(len(c[4]) for c in cases)} 个 token）")
    print(f"判定为真汉字「一」的 token: {sum(len(g[2]) for g in genuine)} 个")
    print()
    for name, ln, anchor, line, conn in cases:
        marks = []
        for pos in conn:
            marks.append(f"…{line[max(0,pos-6):pos]}【一】{line[pos+1:pos+7]}…")
        print(f"{name[:16]:16} L{ln:5d} {anchor or '?':11} " + " | ".join(marks))

    if args.apply:
        print("\n--apply：本轮不自动写回（先人工复核分类结果）")


if __name__ == "__main__":
    main()
