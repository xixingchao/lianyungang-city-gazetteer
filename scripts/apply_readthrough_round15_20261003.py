# -*- coding: utf-8 -*-
"""逐卷通读第15轮（城乡建设/环境保护/经济综情/经济综合管理）批量修正。"""
import argparse
import glob
import io
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V2_GLOB = os.path.join(ROOT, "workbench", "body_chapters_v2", "*.md")
READER = os.path.join(ROOT, "output", "final_reader", "连云港市志_全书.html")

FIXES = [
    # ---- 第五卷 城乡建设 ----
    ("全市第-一部城市规划", "全市第一部城市规划", 1),
    ("城市总体规划（1980～2000））（见图5-1）", "城市总体规划（1980～2000）（见图5-1）", 1),
    ("《东海县县城总体规划草案，主要内容", "《东海县县城总体规划草案》，主要内容", 1),
    ("同意求口水厂建设规模", "同意茅口水厂建设规模", 1),
    ("船体水下部分蛆烂严重", "船体水下部分腐烂严重", 1),
    ("津海港、裕隆巷", "津海巷、裕隆巷", 1),
    ("载种行道树法桐", "栽种行道树法桐", 1),
    ("民国15年（1926年）9月，连云港一号码头筑成", "民国25年（1936年）9月，连云港一号码头筑成", 1),
    ("民国34年（1935年）", "民国34年（1945年）", 2),
    ("新浦新华电灯公司", "新浦新东电灯公司", 1),
    ("5“级小三角点", "5″级小三角点", 1),
    ("疏滩", "疏浚", 4),
    ("其前，海州、云台和连云都没有", "此前，海州、云台和连云都没有", 1),
    ("海州知府唐仲冕主持开掘甲子河", "海州知州唐仲冕主持开掘甲子河", 1),
    ("临洪潮挡闸", "临洪挡潮闸", 1),
    ("荷载标准-15，挂-80.", "荷载标准汽-15，挂-80。", 1),
    ("“九洲第一窟”", "“九州第一窟”", 1),
    ("上层十昂五踩", "上层重昂五踩", 1),
    ("及施放气", "及弛放气", 1),
    ("举办水平测试学习班", "举办水平衡测试学习班", 1),
    ("规划年限和城市规划为", "规划年限和城市规模为", 1),
    # ---- 第六卷 环境保护 ----
    ("三月毂旦", "三月谷旦", 2),
    ("震旦雅雀", "震旦鸦雀", 4),
    ("防治棉铃虫和芽虫", "防治棉铃虫和蚜虫", 1),
    ("核型多体病毒", "核型多角体病毒", 1),
    ("交通枢枢纽区", "交通枢纽区", 1),
    ("北纬33°44′～34°49‘", "北纬34°44′～34°49′", 1),
    ("火烧蕊式", "火烧芯式", 1),
    ("集中联电供热", "集中联片供热", 1),
    ("汇同市科技报社", "会同市科技报社", 1),
    ("Ca⁺+（钙离子）、Mg⁺⁺（镁离子）", "Ca²⁺（钙离子）、Mg²⁺（镁离子）", 1),
    ("SO₄⁻", "SO₄²⁻", 1),
    ("粉煤质毛面贴墙砖", "粉煤灰毛面贴墙砖", 1),
    # ---- 第七卷 经济综情 ----
    ("频临黄海", "濒临黄海", 1),
    ("海洲湾", "海州湾", 1),
    ("廖廖无几", "寥寥无几", 2),
    ("执行第五个五年计划时期", "执行第七个五年计划时期", 1),
    ("第三年五年计划", "第三个五年计划", 1),
    ("有力地支持了。民族解放战争。", "有力地支持了民族解放战争。", 1),
    ("牛羊肉2.8斤", "牛羊肉2.8公斤", 1),
    # ---- 第八卷 经济综合管理 ----
    ("通货恶性膨涨", "通货恶性膨胀", 1),
    ("逐步过度到建立", "逐步过渡到建立", 1),
    ("销售销售价格", "销售价格", 1),
    ("文化产流的门户", "文化交流的门户", 1),
    ("《农业机构年末拥用量》", "《农业机械年末拥有量》", 1),
    ("滥发资金、实物", "滥发奖金、实物", 1),
    ("核减不实奖金22514万元", "核减不实资金22514万元", 1),
    ("占签证份数的88.6%", "占鉴证份数的88.6%", 1),
    ("市工商行、市革委会", "市工商局、市革委会", 1),
    ("70馀万元", "70余万元", 1),
    ("合同签定履行情况", "合同签订履行情况", 1),
    ("友好访华团-行31人", "友好访华团一行31人", 1),
    ("《标准化工作守则》", "《标准化工作导则》", 1),
    ("市管县制体制", "市管县体制", 1),
    ("水份", "水分", 10),
    ("生产生产修建工程", "生产修建工程", 1),
    ("（试行））18条", "（试行）》18条", 1),
    ("1954销售额", "1954年销售额", 1),
    ("设备价格压到549万美元", "设备价格涨到549万美元", 1),
    ("1980年，基本建设新增年报2种", "1986年，基本建设新增年报2种", 1),
]

PROBES = ["疏滩", "海洲湾", "水份", "SO₄", "施放气"]


def counts(text, s):
    return text.count(s)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry", action="store_true")
    args = ap.parse_args()

    v2_files = sorted(glob.glob(V2_GLOB))
    v2_text = {f: io.open(f, encoding="utf-8").read() for f in v2_files}
    html = io.open(READER, encoding="utf-8").read()

    ok = 0
    for old, new, exp in FIXES:
        n_v2 = sum(counts(t, old) for t in v2_text.values())
        if n_v2 == exp:
            ok += 1
        else:
            files_hit = [os.path.basename(f) for f, t in v2_text.items() if old in t]
            print(f"!! v2={n_v2} html={counts(html, old)} exp={exp} | {old} | {files_hit}")
    print(f"可应用: {ok} / {len(FIXES)}")
    if args.dry:
        for s in PROBES:
            n = 0
            for f, t in v2_text.items():
                i = t.find(s)
                while i >= 0 and n < 4:
                    ln = t.count("\n", 0, i) + 1
                    print(f"  [{s}] {os.path.basename(f)} L{ln}: ...{t[max(0,i-50):i+len(s)+50]}...")
                    n += 1
                    i = t.find(s, i + 1)
        print("(dry)")
        return

    n = 0
    for old, new, exp in FIXES:
        if sum(counts(t, old) for t in v2_text.values()) != exp:
            print(f"SKIP {old}")
            continue
        for f in v2_files:
            if old in v2_text[f]:
                v2_text[f] = v2_text[f].replace(old, new)
        if old in html:
            html = html.replace(old, new)
        n += 1
    for f in v2_files:
        io.open(f, "w", encoding="utf-8", newline="").write(v2_text[f])
    io.open(READER, "w", encoding="utf-8", newline="").write(html)
    print(f"已写入 {n} 组修正")


if __name__ == "__main__":
    main()
