# -*- coding: utf-8 -*-
"""逐卷通读第9轮（文化/报刊广电/卫生/体育/宗教）批量修正。

用法：
  py -3 scripts/apply_readthrough_round9_20261003.py --dry
  py -3 scripts/apply_readthrough_round9_20261003.py
"""
import argparse
import glob
import io
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V2_GLOB = os.path.join(ROOT, "workbench", "body_chapters_v2", "*.md")
READER = os.path.join(ROOT, "output", "final_reader", "连云港市志_全书.html")

# (old, new, expect_v2)
FIXES = [
    # ---- 第五十二卷 文化 ----
    ("苏轼、张来、石曼卿", "苏轼、张耒、石曼卿", 1),
    ("季汝珍", "李汝珍", 3),
    ("《胸雅》", "《朐雅》", 1),
    ("《沦海吟余》", "《沧海吟余》", 1),
    ("刘一珍的玉辅遗稿》", "刘一珍的《玉辅遗稿》", 1),
    ("145方多字", "145万多字", 1),
    ("粗扩", "粗犷", 4),
    ("浮磐（轻石制的磐）", "浮磬（轻石制的磬）", 1),
    ("《燕乐考源》", "《燕乐考原》", 2),
    ("鞘公", "艄公", 1),
    ("莲云港市", "连云港市", 3),
    ("生、旦、净、未、丑", "生、旦、净、末、丑", 1),
    ("巫现活动", "巫觋活动", 1),
    ("巫巍活动", "巫觋活动", 1),
    ("文名王小业", "又名王小业", 1),
    ("形成手20世纪20年代", "形成于20世纪20年代", 1),
    ("多至数干人", "多至数千人", 1),
    ("郊城、新沂", "郯城、新沂", 1),
    ("流传手东海县境内", "流传于东海县境内", 1),
    ("轿露头角", "崭露头角", 1),
    ("张道凌", "张道陵", 1),
    ("跌人低谷", "跌入低谷", 1),
    ("滩阴专区", "淮阴专区", 1),
    ("榔子剧团", "梆子剧团", 1),
    ("郴子剧团", "梆子剧团", 1),
    ("防囊角度", "防震角度", 1),
    ("较偏避", "较偏僻", 1),
    ("天伊山大庆路", "大伊山大庆路", 1),
    ("谈谐的语言", "诙谐的语言", 1),
    ("民简舞蹈", "民间舞蹈", 1),
    ("婉蜓的火龙", "蜿蜒的火龙", 1),
    ("谱谋", "谱牒", 1),
    ("准盐机构", "淮盐机构", 2),
    ("惠裕宇", "惠浴宇", 1),
    ("战路任务", "战略任务", 1),
    ("所在地一一新浦市民路", "所在地——新浦市民路", 1),
    ("编自检索", "编目检索", 1),
    ("检索工真", "检索工具", 1),
    ("沈云需", "沈云沛", 22),
    ("蓬莱万丈有无间", "蓬莱方丈有无间", 1),
    ("长恨双鬼去莫攀", "长恨双凫去莫攀", 1),
    ("请阿到家里", "请阿訇到家里", 1),
    ("的一周节目十一、连云港团讯1987年7月创刊，共青团连云港市委员会主办。，以及主要文艺节目及剧情。"
     , "的一周节目，以及主要文艺节目及剧情。", 1),
    ("武若愚、李尚农、李玉东等", "武若愚、李尚农等", 1),
    # ---- 第五十五卷 卫生 ----
    ("寒、热、湿、凉", "寒、热、温、凉", 1),
    ("固湿药", "固涩药", 1),
    ("肾功能衰弱", "肾功能衰竭", 1),
    ("阿米妥纳", "阿米妥钠", 1),
    ("低湿下肾切开", "低温下肾切开", 1),
    ("肾母细胞病根治", "肾母细胞瘤根治", 1),
    ("麦粘肿", "麦粒肿", 1),
    ("针拔白内障", "针拨白内障", 1),
    ("菌陈汤", "茵陈汤", 1),
    ("早会、堂对、交接班", "早会、查对、交接班", 1),
    ("进行交换班", "进行交接班", 1),
    ("西医个体行业10家", "西医个体行医10家", 1),
    ("格林一巴利", "格林—巴利", 1),
    # ---- 第五十七卷 宗教 ----
    ("十万丛林", "十方丛林", 1),
    ("懿峰石塔", "鹫峰石塔", 1),
    ("方历二十二年", "万历二十二年", 1),
    ("毁于兵爽", "毁于兵燹", 1),
    ("蓄薇河", "蔷薇河", 2),
    ("题字日：仙人洞", "题字曰：仙人洞", 1),
    ("供奉天营、地宫、水宫", "供奉天官、地官、水官", 1),
    ("一般在清真等举行", "一般在清真寺举行", 1),
    ("阿休息室", "阿訇休息室", 2),
    ("贝锦章包底藏匿", "贝锦章包庇藏匿", 1),
    ("明未至清嘉庆", "明末至清嘉庆", 1),
    ("票真中学", "崇真中学", 1),
    ("苏准中华基督教大会", "苏淮中华基督教大会", 1),
    ("按职典礼", "按立典礼", 1),
    ("闻声、慕庚杨", "闻声、慕庚扬", 1),
    # ---- 第五十四卷 报刊广播电视 ----
    ("青口——赣马", "青口—赣马", 1),
    ("国家新闻总署批准", "国家新闻出版署批准", 1),
    # ---- 第五十六卷 体育 ----
    ("选拨赛", "选拔赛", 1),
    ("武装泗渡", "武装泅渡", 1),
    ("沥清篮球场", "沥青篮球场", 1),
    ("中班比赛拍手赛", "中班比赛拍手操", 1),
    ("龙苴公司被评为", "龙苴公社被评为", 1),
    ("健华篮球队", "建华篮球队", 1),
    ("体育代表队100人，队员1500人", "体育代表队100个，队员1500人", 1),
    ("池身1.2米至1.6米", "池深1.2米至1.6米", 1),
]

LINE_DELETE = ["天主教:2553", ".2554 ."]

PROBES = ["请阿到", "请阿訇", "十一、连云港团讯", "李玉东", "全部收入的"]
PROBE_LIMIT = 4


def counts(text, s):
    return text.count(s)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry", action="store_true")
    args = ap.parse_args()

    v2_files = sorted(glob.glob(V2_GLOB))
    v2_text = {f: io.open(f, encoding="utf-8").read() for f in v2_files}
    html = io.open(READER, encoding="utf-8").read()

    bad = []
    ok = 0
    print("== 逐条匹配检查 ==")
    for old, new, exp in FIXES:
        n_v2 = sum(counts(t, old) for t in v2_text.values())
        n_html = counts(html, old)
        files_hit = [os.path.basename(f) for f, t in v2_text.items() if old in t]
        if n_v2 != exp:
            bad.append((old, new, exp, n_v2, n_html, files_hit))
            print(f"!! v2={n_v2} html={n_html} exp={exp} | {old}")
        else:
            ok += 1
    print(f"\n可应用: {ok} / {len(FIXES)}")

    print("\n== 行级检查 ==")
    for s in LINE_DELETE:
        for f, t in v2_text.items():
            for i, line in enumerate(t.split("\n")):
                if line.strip() == s:
                    print(f"  DEL v2 {os.path.basename(f)} L{i+1}: {line!r}")
        print(f"  html {s!r} count={counts(html, s)}")

    print("\n== 探针 ==")
    for s in PROBES:
        n = 0
        for f, t in v2_text.items():
            i = t.find(s)
            while i >= 0 and n < PROBE_LIMIT:
                ln = t.count("\n", 0, i) + 1
                print(f"  [{s}] {os.path.basename(f)} L{ln}: ...{t[max(0,i-70):i+len(s)+70]}...")
                n += 1
                i = t.find(s, i + 1)

    if args.dry:
        print("\n(dry run, 未写入)")
        return

    n_applied = 0
    for old, new, exp in FIXES:
        if sum(counts(t, old) for t in v2_text.values()) != exp:
            print(f"SKIP {old}")
            continue
        for f in v2_files:
            if old in v2_text[f]:
                v2_text[f] = v2_text[f].replace(old, new)
        if old in html:
            html = html.replace(old, new)
        n_applied += 1

    for f in v2_files:
        lines = v2_text[f].split("\n")
        v2_text[f] = "\n".join(l for l in lines if l.strip() not in LINE_DELETE)
    for s in LINE_DELETE:
        html = html.replace(f"<p>{s}</p>", "")

    for f in v2_files:
        io.open(f, "w", encoding="utf-8", newline="").write(v2_text[f])
    io.open(READER, "w", encoding="utf-8", newline="").write(html)
    print(f"已写入 {n_applied} 组修正 + 行级清理")


if __name__ == "__main__":
    main()
