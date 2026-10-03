# -*- coding: utf-8 -*-
"""逐卷通读第17轮（盐业/轻（手）工业/纺织工业/皮塑工业）批量修正。"""
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
    # ---- 第十三卷 盐业 ----
    ("阖间", "阖闾", 4),
    ("清除于净", "清除干净", 1),
    ("柳斗库水", "柳斗戽水", 1),
    ("天津溏沽", "天津塘沽", 1),
    ("0C小组", "QC小组", 1),
    ("人亡改息", "人亡政息", 1),
    ("祖庸使", "租庸使", 1),
    ("每禀数千担", "每廪数千担", 1),
    ("大原、裕通", "大源、裕通", 1),
    ("封筷", "封跳", 1),
    ("封旐", "封跳", 1),
    ("戚墅堰机床车辆厂", "戚墅堰机车车辆厂", 1),
    ("卢州府", "庐州府", 1),
    ("辆流泵", "轴流泵", 1),
    ("万历四十五年（1517年）", "万历四十五年（1617年）", 1),
    ("颖上、霍邱", "颍上、霍邱", 1),
    # ---- 第十六卷 皮塑工业 ----
    ("黑龙宽、吉林", "黑龙江、吉林", 1),
    ("烙鞣", "铬鞣", 2),
    ("泥合鞣", "混合鞣", 1),
    ("拷胶", "栲胶", 2),
    ("绷植机", "绷楦机", 1),
    ("裁断枯机", "裁断机", 1),
    ("绷檀", "绷楦", 1),
    ("炳烯单丝", "丙烯单丝", 1),
    ("输囟管", "输卤管", 1),
    ("二辛脂", "二辛酯", 3),
    ("2379脂", "2379酯", 1),
    ("聚脂拉链", "聚酯拉链", 3),
    ("聚脂单丝", "聚酯单丝", 3),
    ("南京航天航空大学", "南京航空航天大学", 1),
    # ---- 第十四卷 轻（手）工业 ----
    ("聚内烯编织袋", "聚丙烯编织袋", 1),
    ("工私合营新浦铁工厂", "公私合营新浦铁工厂", 1),
    ("B665创床", "B665刨床", 1),
    ("李浊尘", "李烛尘", 1),
    ("囟钨灯", "卤钨灯", 1),
    ("碘镥灯管", "碘钨灯管", 1),
    ("洒瓶", "酒瓶", 2),
    ("约纹", "绉纹", 4),
    ("连云区0.37件", "连云区0.37万件", 1),
    ("碘包灯管", "碘钨灯管", 1),
    ("新增固定资产103亿元", "新增固定资产1.03亿元", 1),
    ("年产1.8亿万印", "年产1.8亿印", 1),
    ("凸板纸", "凸版纸", 2),
    ("磨沙", "磨砂", 5),
    ("L-～1型", "L-1型", 1),
    ("1配件50万套", "配件50万套", 1),
    ("控压机、站", "空压机站", 1),
    ("内销省内及、福建", "内销省内及福建", 1),
    # ---- 第十五卷 纺织工业 ----
    ("涤沦厂", "涤纶厂", 1),
    ("年产3200吨氨纶抽丝", "年产320吨氨纶抽丝", 1),
    ("1尺相当于3米", "1尺相当于0.33米", 1),
    ("靛兰牛仔布", "靛蓝牛仔布", 1),
    ("漂白一清洗", "漂白—清洗", 1),
    ("风糜服装面料", "风靡服装面料", 1),
    ("聚乙稀等化纤袋", "聚乙烯等化纤袋", 1),
    ("桑茧丝及其交织品", "桑蚕丝及其交织品", 1),
    ("双约", "双绉", 3),
    ("素约缎", "素绉缎", 1),
    ("纯棉夫绸、防缩柔软夫绸", "纯棉府绸、防缩柔软府绸", 1),
    ("条纤维粗绳", "杂纤维粗绳", 1),
    ("简子三道工序", "筒子三道工序", 1),
    ("电力地杆传动", "电力地杠传动", 1),
    ("有光导形丝", "有光异形丝", 1),
    ("树酯", "树脂", 18),
    ("制\">第一节体制", "第一节体制", 1),
    ("熔触常规纺丝法", "熔融常规纺丝法", 1),
    ("融高速纺丝法", "熔融高速纺丝法", 1),
    ("ZZ11棉毛机", "Z211棉毛机", 1),
    ("晾晒于燥", "晾晒干燥", 1),
    ("热电型机", "热定型机", 1),
    ("毛卷、乔其纱", "毛圈、乔其纱", 1),
    ("美国圣佳公司", "美国胜家公司", 1),
]

PROBES = ["树酯", "约纹", "磨沙", "双约", "第一节体制", "阖间"]


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
                while i >= 0 and n < 3:
                    ln = t.count("\n", 0, i) + 1
                    print(f"  [{s}] {os.path.basename(f)} L{ln}: ...{t[max(0,i-45):i+len(s)+45]}...")
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
