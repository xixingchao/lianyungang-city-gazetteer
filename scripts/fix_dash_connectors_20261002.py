# -*- coding: utf-8 -*-
"""连接号专项：v2/阅读版「一」→「—」批量核定与写回（2026-10-02）。

两类判据（均要求 token 不落在词表/人名内）：
- A 链式：同一行内出现「一X一Y」链（路线、序列、地层、孢粉组合等）
- B 邻证：同一行内已有连接号「—」，则孤立的「一」（两侧汉字）亦判为误读的连接号
写回：body_chapters_v2 与 output/final_reader/连云港市志_全书.html 同步，逐条留痕。
用法：python fix_dash_connectors_20261002.py [--apply]
"""
from __future__ import annotations

import argparse
import glob
import io
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
V2 = ROOT / "workbench" / "body_chapters_v2"
READER = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
ANCH = re.compile(r"<!--\s*page-anchor:\s*([A-Za-z0-9\-]+)\s*-->")
NL = "\n"
DASH_CHAIN = re.compile(r"[\u4e00-\u9fff]一[\u4e00-\u9fff]{1,}一[\u4e00-\u9fff]")
LONE = re.compile(r"[\u4e00-\u9fff]一[\u4e00-\u9fff]")

# 真汉字「一」词表（含人名/番号/量词短语）
WORDS = (
    "进一步", "一个", "一次", "一般", "一切", "一直", "一样", "一边", "一带", "一行", "一支", "一名",
    "一对", "一系列", "一致", "一共", "一齐", "一同", "一律", "一旦", "一层", "一片", "一线", "一日",
    "一年", "一月", "一起", "一再", "一贯", "一定", "一流", "一体", "一并", "一览", "一经", "一心",
    "一手", "一头", "一批", "一类", "一种", "一条", "一座", "一道", "一时", "一所", "一格", "一页",
    "一号", "一节", "一班", "一组", "一队", "一例", "一色", "一揽子", "一回事", "一览表", "一应",
    "一隅", "一斑", "一脉", "一席", "一端", "一侧", "一转", "一瞬", "一准", "一总", "一五", "一化",
    "一平", "一期", "一村", "一区", "一校", "一厂", "一站", "一军", "一营", "一团", "一族",
    "一科", "一属", "一系", "一夜", "一块", "一届", "一路", "一番", "一栋", "一棵", "一孔", "一张",
    "一幅", "一帧", "一册", "一本", "一卷", "一部", "一处", "一局", "一县", "一市", "一省", "一国",
    "一乡", "一镇", "一街", "一型", "一式", "一级", "一等", "一波", "一阵", "一场", "一趟", "一回",
    "一顿", "一口", "一户", "一家", "一间", "一室", "一厅", "一楼", "一桥", "一坝", "一渠", "一塘",
    "一井", "一库", "一院", "一版", "一台", "一套", "一宗", "一轴", "一柱", "一旅", "一师", "一排",
    "一壁", "一则", "一者", "一斑", "一统", "一任", "一似", "一霎", "一晌", "一早", "一晚", "一夕",
    "一朝", "一翼", "一环", "一遇", "一些", "一半", "一份", "一是", "一言", "一色", "一事",
    "一句", "一字", "一步", "一笔", "一束", "一叠", "一览", "一干", "一空", "一发", "一动", "一举",
    # 人名/番号/专名
    "刘一麟", "刁一民", "王一勋", "泰一", "峰本一", "一一二", "一四一", "一七三", "一六一", "五一八",
    "一大队", "一中队", "一小队", "一分队", "一支队", "一纵队", "一军团", "一兵团", "一连一",
    "六七一", "五十七", "八十二", "二十一", "十一",
    # 第二轮复核补充（2026-10-02，逐行目视后加入）
    "一株", "合一", "一度", "一社", "一面", "一至", "一大", "一庄", "一女", "一巨", "一位", "这一",
    "一点", "一遍", "一钱", "一斤", "一堆", "一床", "某一", "一天", "一品", "一生", "一人", "一丈",
    "一尺", "一章", "一句", "一圈", "一清", "一段", "一滩", "一锅", "一灶", "一倍", "每一", "一廪",
    "一店", "一挑", "一二十", "一犯", "一伙", "一拥", "一查", "一案", "一报", "一孕", "一工", "一郎",
    "一教师", "一大步", "一档", "一熟", "一病", "一虫", "一九", "一九四", "一连一营", "一营一连",
    "一一五", "一一一", "一一六", "一一八", "一例", "一里", "一农", "一二师",
    "为一", "一阅", "一周年", "一播", "一栽",
)
WORDS = tuple(dict.fromkeys(WORDS))
# 词尾形式（X一）：如 十一/第一/统一/唯一/单一/不一/万一/之一/其一
TAILS = ("十一", "第一", "统一", "同一", "唯一", "之一", "其一", "单一", "不一", "万一", "划一", "均一",
         "专一", "纯一", "如一", "数一", "二一", "三一", "四一", "五一", "六一", "七一", "八一", "九一",
         "一百一", "千一", "亿一")
# 固定结构
MIDS = ("一一", "一五一十", "数一数二", "说一不二", "一分为二", "合二为一", "三位一体", "一机五用")
# 显式保留（人工裁定：这些 token 是真汉字，不随行改动）
KEEP_NEIGHBORS = ("些", "份", "半", "种", "般", "样", "致", "律", "并", "览", "经", "旦", "层", "片")


def is_word(line: str, i: int) -> bool:
    """token line[i] == '一' 是否属于真汉字（词表/词尾/固定结构/叠字）。"""
    for w in WORDS:
        for off in range(len(w)):
            if w[off] == "一" and i - off >= 0 and line[i - off:i - off + len(w)] == w:
                return True
    for w in TAILS:
        if i - len(w) + 1 >= 0 and line[i - len(w) + 1:i + 1] == w:
            return True
    for w in MIDS:
        if w in line[max(0, i - 4):i + 5]:
            return True
    if (i > 0 and line[i - 1] == "一") or (i + 1 < len(line) and line[i + 1] == "一"):
        return True
    return False


# 显式保留（行号→token 文本）：人工裁定为真汉字，不随行改动
KEEP_TOKENS = {
    ("第四十三卷至第五十一卷（下part01）.md", 2001): ("一连",),   # 一营一连、二连
    ("第四十三卷至第五十一卷（下part01）.md", 1795): ("一二",),   # 五十七军一二师（疑原书/OCR 缺一，另行待核）
}


# B 类：同位语「一一」→「——」（人工裁定，逐条）
B_APPOSITIVE = {
    ("第四十三卷至第五十一卷（下part01）.md", 4423): "组织一一陇海",
    ("第四十三卷至第五十一卷（下part01）.md", 4779): "路一一一连云港市",
    ("第四十三卷至第五十一卷（下part01）.md", 6053): "密集区一一赣榆县",
    ("第四十三卷至第五十一卷（下part01）.md", 6449): "遗传学一一一人类染色体",
    ("第四十三卷至第五十一卷（下part01）.md", 6457): "利尿药一一一甘露醇",
}
# C 类：叠字「一一」→「一」（人工裁定，逐条）
C_DOUBLED = {
    ("第三十卷至第四十二卷（中part02）.md", 1515): "最大的一一个",
    ("第三十卷至第四十二卷（中part02）.md", 1625): "组成了一一个",
    ("第三十卷至第四十二卷（中part02）.md", 10157): "第一一次会",
    ("第五十二卷至第六十卷及附录（下part02）.md", 209): "云台山一一带",
    ("第五十二卷至第六十卷及附录（下part02）.md", 505): "民间一一直",
    ("第五十二卷至第六十卷及附录（下part02）.md", 8863): "以一一个中等",
    ("第十七卷至第二十九卷（中part01）.md", 4465): "一一直没有形成",
    ("第十七卷至第二十九卷（中part01）.md", 6503): "一一切用户",
    ("第十七卷至第二十九卷（中part01）.md", 8663): "的一一种税",
}


# 线路/走向类行：分隔符一律归并为单个「—」（原书为单连接号）
ROUTE_LINES = {
    ("第三十卷至第四十二卷（中part02）.md", 837), ("第三十卷至第四十二卷（中part02）.md", 965),
    ("第三十卷至第四十二卷（中part02）.md", 989), ("第三十卷至第四十二卷（中part02）.md", 1007),
    ("第三十卷至第四十二卷（中part02）.md", 1287), ("第三十卷至第四十二卷（中part02）.md", 1307),
    ("第三十卷至第四十二卷（中part02）.md", 1837),
    ("第十七卷至第二十九卷（中part01）.md", 8231),
}

# 显式逐条修正（页图核定）：(文件, 行号) → (旧片段, 新片段)
EXPLICIT = {
    ("第三十卷至第四十二卷（中part02）.md", 3095): ("专业浴池一新浦第池", "专业浴池——新浦第一池"),
    ("第十七卷至第二十九卷（中part01）.md", 8231): (
        "连云港—中国香港、澳门、连云港西非、连云港一朝鲜、连云港一苏联、连云港一中国台湾、连云港一地中海、连云港一日本、连云港—西北欧、连云港—东南亚、连云港大洋洲、连云港—新加坡、马来西亚、连云港一美国东岸、连云港一孟加拉湾、连云港一美国西岸、连云港一波斯湾、连云港一加拿大、连云港一东非红海、连云港一中南美。",
        "连云港—中国香港、澳门、连云港—西非、连云港—朝鲜、连云港—苏联、连云港—中国台湾、连云港—地中海、连云港—日本、连云港—西北欧、连云港—东南亚、连云港—大洋洲、连云港—新加坡、马来西亚、连云港—美国东岸、连云港—孟加拉湾、连云港—美国西岸、连云港—波斯湾、连云港—加拿大、连云港—东非红海、连云港—中南美。"),
}


# 线路行扫掠：保护真词后，把 CJK 之间的 [-—一] 串归并为单个「—」
PROTECT = ("第一条", "第二条", "第三条", "统一", "一定", "一并", "一次", "一趟", "一般", "一个", "一行")


def sweep_route_line(line: str) -> str:
    for k, w in enumerate(PROTECT):
        line = line.replace(w, f"{k}")
    line = re.sub(r"(?<=[一-鿿）】])[-—一]+(?=[一-鿿])", "—", line)
    for k, w in enumerate(PROTECT):
        line = line.replace(f"{k}", w)
    return line


def candidates(line: str) -> list[int]:
    """返回该行应改为「—」的 token 位置。"""
    pos = set()
    has_dash = "—" in line
    for mm in DASH_CHAIN.finditer(line):
        for i in range(mm.start(), mm.end()):
            if line[i] == "一" and not is_word(line, i):
                pos.add(i)
    if has_dash:
        for mm in LONE.finditer(line):
            i = mm.start() + 1
            if line[i] != "一":
                continue
            if is_word(line, i):
                continue
            pos.add(i)
    # 破折号双写：…一一《…》/ 圣树一一… → 「——」（仅这两类，避免误伤番号与「一一个」叠字）
    if "一一" in line and (line.find("一一《") >= 0 or "圣树一一" in line):
        for mm in re.finditer("一一《|圣树一一", line):
            pos.add(mm.start())
            pos.add(mm.start() + 1)
    return sorted(pos)


def plan() -> list[tuple[Path, int, str, str]]:
    changes = []
    for f in sorted(Path(p) for p in glob.glob(str(V2 / "*.md"))):
        for ln, line in enumerate(io.open(f, encoding="utf-8").read().splitlines(), 1):
            if ANCH.search(line) or "{{STRUCTURED_TABLE" in line:
                continue
            key = (f.name, ln)
            if key in EXPLICIT:
                old_frag, new_frag = EXPLICIT[key]
                if old_frag in line:
                    changes.append((f, ln, line, line.replace(old_frag, new_frag, 1)))
                continue
            pos = candidates(line)
            if key in B_APPOSITIVE:
                frag = B_APPOSITIVE[key]
                if frag in line:
                    base = line.find(frag)
                    for k in range(len(frag) - 1):
                        if frag[k] == "一" and frag[k + 1] == "一":
                            pos += [base + k, base + k + 1]
            if not pos:
                continue
            new = list(line)
            for i in pos:
                new[i] = "—"
            newline = "".join(new)
            if (f.name, ln) in ROUTE_LINES:
                newline = sweep_route_line(newline)
            changes.append((f, ln, line, newline))
    return changes


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()
    changes = plan()
    total = sum(len(re.findall("—", n)) - len(re.findall("—", o)) for _, _, o, n in changes)
    print(f"C 类叠字修正 {len(C_DOUBLED)} 条（一一→一）")
    print(f"涉及 {len(changes)} 行，替换 token {total} 个")
    if not args.apply:
        for f, ln, old, new in changes[:8]:
            print(f"--- {f.name} L{ln}")
            print("  old:", old[:110])
            print("  new:", new[:110])
        print("（dry-run，未写回）")
        return
    # C 类先做（字符串级）
    c_applied = 0
    for (fname, ln), frag in C_DOUBLED.items():
        f = V2 / fname
        ls = io.open(f, encoding="utf-8").read().splitlines()
        if frag in ls[ln - 1]:
            ls[ln - 1] = ls[ln - 1].replace(frag, frag.replace("一一", "一"), 1)
            io.open(f, "w", encoding="utf-8", newline=NL).write(NL.join(ls) + NL)
            c_applied += 1
    print(f"C 类写回 {c_applied}/{len(C_DOUBLED)}")
    # 写回 v2
    from collections import defaultdict
    by_file = defaultdict(list)
    for f, ln, old, new in changes:
        by_file[f].append((ln, new))
    for f, items in by_file.items():
        ls = io.open(f, encoding="utf-8").read().splitlines()
        for ln, new in items:
            ls[ln - 1] = new
        io.open(f, "w", encoding="utf-8", newline=NL).write(NL.join(ls) + NL)
        print(f"v2 写回 {f.name}: {len(items)} 行")
    rt = io.open(READER, encoding="utf-8").read()
    hit = 0
    for f, ln, old, new in changes:
        if old in rt:
            rt = rt.replace(old, new, 1)
            hit += 1
    io.open(READER, "w", encoding="utf-8", newline=NL).write(rt)
    print(f"阅读版写回 {hit}/{len(changes)} 行（未命中行可能因 HTML 内分块）")


if __name__ == "__main__":
    main()
