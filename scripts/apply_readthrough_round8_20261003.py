# -*- coding: utf-8 -*-
"""逐卷通读第8轮（外事侨务/社团/教育/科技）批量修正（定稿版，均已回源 300dpi 核对）。

用法：
  py -3 scripts/apply_readthrough_round8_20261003.py --dry
  py -3 scripts/apply_readthrough_round8_20261003.py
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

# (old, new_v2, new_html, expect_v2)   new_html=None → 与 new_v2 相同
FIXES = [
    # ---- 第四十八卷 外事侨务（回源核对） ----
    ("秦代方土徐福", "秦代方士徐福", None, 1),
    ("学向僧圆仁", "学问僧圆仁", None, 1),
    ("宫员陪同考察", "官员陪同考察", None, 1),
    ("植物学博土", "植物学博士", None, 1),
    ("竟然悔辱中方渔民", "竟然侮辱中方渔民", None, 1),
    ("强行驶人连云港", "强行驶入连云港", None, 1),
    ("纷纷皇文通电", "纷纷呈文通电", None, 1),
    ("早稽田大学", "早稻田大学", None, 1),
    ("日本新官市市长", "日本新宫市市长", None, 1),
    ("高岛屋界店", "高岛屋堺店", None, 1),
    ("特写重要港湾", "特定重要港湾", None, 1),
    ("《连云港一一海洋大门》", "《连云港——海洋大门》", None, 1),
    ("连云港一日本大阪府", "连云港—日本大阪府", None, 1),
    ("东光刃号", "东光丸号", None, 1),
    ("横崛克已", "横崛克己", None, 1),
    ("联络联谊，弓引进资金与人才", "联络联谊，引进资金与人才", None, 1),
    ("拨经费?9.21万元", "拨经费9.21万元", None, 1),
    # ---- 第四十九卷 社团（回源核对） ----
    ("锦屏公同矿工", "锦屏公司矿工", None, 1),
    ("人民的睡弃", "人民的唾弃", None, 1),
    ("因文化大革命”于扰", "因“文化大革命”干扰", None, 1),
    ("火柴广进行民主改革", "火柴厂进行民主改革", None, 1),
    ("火柴产、印刷厂", "火柴厂、印刷厂", None, 1),
    ("拨河", "拔河", None, 2),
    ("选拨154名运动员", "选拔154名运动员", None, 1),
    ("打播比武", "打擂比武", None, 2),
    ("一场冰雷", "一场冰雹", None, 1),
    ("共植树75方株", "共植树75万株", None, 1),
    ("10.8方人", "10.8万人", None, 1),
    ("隆泰商号国积的日货", "隆泰商号囤积的日货", None, 1),
    ("孙友仁企图包底", "孙友仁企图包庇", None, 1),
    ("《关手目前形势与今后任务的报告，", "《关于目前形势与今后任务的报告》，", None, 1),
    ("全国二八红旗集体", "全国三八红旗集体", None, 1),
    ("优秀团员加人中国共产党", "优秀团员加入中国共产党", None, 1),
    ("跨台不少", "垮台不少", None, 1),
    ("儿年来，全国各地", "几年来，全国各地", None, 1),
    ("“一一胎化”", "“一胎化”", None, 1),
    ("炮艇2嫂", "炮艇2艘", None, 1),
    ("云台区、连云会", "云台区、连云区", None, 1),
    ("建全市第个工人俱乐部", "建全市第一个工人俱乐部", None, 1),
    ("个体劳动者协会第届理事会", "个体劳动者协会第一届理事会", None, 1),
    ("5月2831日", "5月28～31日", None, 1),
    ("7月1720日", "7月17～20日", None, 1),
    ("三等奖。19831986年", "三等奖。1983～1986年", None, 1),
    ("工会组织一一陇海铁路", "工会组织——陇海铁路", None, 1),
    ("路———连云港市农村妇女", "路——连云港市农村妇女", None, 1),
    ("唐贯到会讲话", "唐贯淮到会讲话", None, 1),
    ("王准、苏鸣芝", "王淮、苏鸣芝", None, 1),
    ("顾一一萍", "顾一萍", None, 1),
    ("徐哗宇", "徐晔宇", None, 1),
    ("肆业所", "肄业所", None, 2),
    # ---- 第五十卷 教育（回源核对） ----
    ("江苏省立十中学", "江苏省立第十一中学", None, 1),
    ("海州十中学", "海州十一中学", None, 1),
    ("本知识与参加社会实践", "书本知识与参加社会实践", None, 1),
    ("侵略政策、儿何", "侵略政策、几何", None, 1),
    ("私垫进行改良", "私塾进行改良", None, 1),
    ("私垫消失", "私塾消失", None, 1),
    ("《百家姓、", "《百家姓》、", None, 1),
    ("十儿个", "十几个", None, 4),
    ("自强不息的校风", "自强不息”的校风", None, 1),
    ("藏书5方册", "藏书5万册", None, 1),
    ("赣榆县中：学", "赣榆县中学", None, 1),
    ("新县小学一一年级", "新县小学一年级", None, 1),
    ("补考2206·后成绩", "补考后成绩", None, 1),
    ("有定专业知识", "有一定专业知识", None, 1),
    ("1：9.1982年调查", "1：9。1982年调查", None, 1),
    ("创建票真中学", "创建崇真中学", None, 1),
    ("肆讲堂3间", "肄讲堂3间", None, 1),
    ("赣榆县城赣马镇西关", "原在赣榆县城赣马镇西关", None, 1),
    # ---- 第五十一卷 科技（回源核对） ----
    ("郑城", "郯城", None, 6),
    ("海州沭阳县主薄沈括", "海州沭阳县主簿沈括", None, 1),
    ("疏述水为百渠九堰", "疏沭水为百渠九堰", None, 1),
    ("薄膜苦盖晒盐", "薄膜苫盖晒盐", None, 1),
    ("普升工资1~2级", "晋升工资1~2级", None, 1),
    ("各普升工资2级", "各晋升工资2级", None, 1),
    ("选拨在职干部", "选拔在职干部", None, 1),
    ("蔬菜裁培手册", "蔬菜栽培手册", None, 1),
    ("高产裁培模式图", "高产栽培模式图", None, 1),
    ("准盐科技通讯》", "《淮盐科技通讯》", None, 1),
    ("条斑紫莱", "条斑紫菜", None, 1),
    ("裙带莱小苗", "裙带菜小苗", None, 1),
    ("中华绒鳌蟹", "中华绒螯蟹", None, 3),
    ("对虾孤菌病", "对虾弧菌病", None, 1),
    ("早丰.1号辣椒", "早丰1号辣椒", None, 1),
    ("之豇28一2虹豆", "之豇28-2豇豆", None, 1),
    ("海州水泡萝卡", "海州水泡萝卜", None, 1),
    ("十漠二苯醚", "十溴二苯醚", None, 1),
    ("EVAL粉未粘合剂", "EVAL粉末粘合剂", None, 1),
    ("开发井投产", "开发并投产", None, 1),
    ("连云港制革广", "连云港制革厂", None, 1),
    ("市农机广", "市农机厂", None, 1),
    ("连云港饮料广", "连云港饮料厂", None, 1),
    ("葡葡酿酒", "葡萄酿酒", None, 1),
    ("凯威于白葡萄酒", "凯威干白葡萄酒", None, 1),
    ("广东浮云硫铁矿", "广东云浮硫铁矿", None, 1),
    ("真有优良的视听效果", "具有优良的视听效果", None, 1),
    ("真有较好的经济效益", "具有较好的经济效益", None, 1),
    ("《金遗要略讲义》", "《金匮要略讲义》", None, 1),
    ("脾牌切除", "脾脏切除", None, 1),
    ("离肉切除术", "胬肉切除术", None, 1),
    ("颌下腮", "颌下腺", None, 2),
    ("亚甲兰", "亚甲蓝", None, 1),
    ("基地细胞癌", "基底细胞癌", None, 1),
    ("市级奖453项", "市级奖482项", None, 1),
    ("19781990年", "1978～1990年", None, 2),
    ("19861990年", "1986～1990年", None, 1),
    ("19751976年", "1975～1976年", None, 1),
    ("19801982年", "1980～1982年", None, 1),
    ("19851986年", "1985～1986年", None, 1),
    ("重大变革一一一四季结晶", "重大变革——四季结晶", None, 1),
    ("郎之万一汪德昭", "郎之万—汪德昭", None, 1),
    # ---- 跨卷偶遇 ----
    ("云台山清未尚有", "云台山清末尚有", None, 1),
    ("清未民初，境内有名气的菜肴", "清末民初，境内有名气的菜肴", None, 1),
    ("戊戍变法", "戊戌变法", None, 1),
    ("唐贯准", "唐贯淮", None, 4),
    # ---- 残文修复（回源核对，v2 与 html 结构不同） ----
    (
        "工人阶级宣传队、弱学生文化学习。",
        "工人阶级宣传队、贫下中农宣传队（简称“军宣队”、“工宣队”、“贫宣队”，下同），师生过多参加政治运动，削弱学生文化学习。",
        None,
        1,
    ),
    (
        "项目学校。1979年市教育局印发",
        "1975年，新海中学、东海县中学、赣榆县中学、灌云县中学被命名为江苏省体育传统项目学校。1979年市教育局印发",
        None,
        1,
    ),
    (
        "学生1751人c五、东海县中学位于东海县牛山镇和平东路。",
        "学生1751人。\n\n五、东海县中学\n\n位于东海县牛山镇和平东路。",
        "学生1751人。</p>\n<p>五、东海县中学</p>\n<p>位于东海县牛山镇和平东路。",
        1,
    ),
    (
        "六、体育民国8年（1919年），海州十中学开设体育课",
        "六、体育\n\n民国8年（1919年），海州十一中学开设体育课",
        "六、体育</p>\n<p>民国8年（1919年），海州十一中学开设体育课",
        1,
    ),
    (
        "七、卫建国后，市教育部门",
        "七、卫生\n\n建国后，市教育部门",
        "七、卫生</p>\n<p>建国后，市教育部门",
        1,
    ),
    (
        "1987究所”。",
        "1987年迁建市内，对内称中国船舶总公司第七研究院第七一六研究所，对外称“江苏自动化研究所”。",
        None,
        1,
    ),
    (
        "从6月下旬位的96%，有2092名会员恢复组织生活发展新会员1861人",
        "从6月下旬开始整顿、组建基层工会，至8月，全县有46个基层工会完成整建任务，占全县应整建单位的96%，有2092名会员恢复组织生活，发展新会员1861人",
        None,
        1,
    ),
    (
        "墟沟海滨浴藤一正来连云港市，采访",
        "墟沟海滨浴场、宿城和港口一带野外考察。1986年1月24~28日，日本《经济新闻》驻北京特派员安藤一正来连云港市，采访",
        None,
        1,
    ),
    (
        "事伊泽公幸率领参观团一行18人",
        "文化新闻界、友好团体人员来访  民国24年（1935年）1月，日本驻青岛商工会所主事伊泽公幸率领参观团一行18人",
        None,
        1,
    ),
]

# 行级残留：整行删除
LINE_DELETE = ["初等教育.2209", "机构与队伍:2263"]
# 行首残留前缀
LINE_STRIP = [(".2194 :学校体育", "学校体育")]

PROBES = [
    "伊泽公幸",
    "事伊泽公幸",
]


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
    total_ok = 0
    print("== 逐条匹配检查 ==")
    for old, new_v2, new_html, exp in FIXES:
        n_v2 = sum(counts(t, old) for t in v2_text.values())
        n_html = counts(html, old)
        files_hit = [os.path.basename(f) for f, t in v2_text.items() if old in t]
        flag = "OK" if n_v2 == exp else "!!"
        if flag == "!!":
            bad.append((old, new_v2, exp, n_v2, n_html, files_hit))
        else:
            total_ok += 1
        print(f"{flag} v2={n_v2} html={n_html} exp={exp} | {old} | {files_hit}")

    print(f"\n可应用: {total_ok} / {len(FIXES)}")

    print("\n== 行级残留检查 ==")
    for s in LINE_DELETE:
        for f, t in v2_text.items():
            for i, line in enumerate(t.split("\n")):
                if line.strip() == s:
                    print(f"  DEL v2 {os.path.basename(f)} L{i+1}: {line!r}")
        print(f"  html {s!r} count={counts(html, s)}")
    for old, new in LINE_STRIP:
        print(f"  STRIP {old!r} v2={sum(counts(t, old) for t in v2_text.values())} html={counts(html, old)}")

    print("\n== 残文锚点上下文（确认替换串） ==")
    for s in PROBES:
        for f, t in v2_text.items():
            i = t.find(s)
            if i >= 0:
                ln = t.count("\n", 0, i) + 1
                print(f"  [{os.path.basename(f)} L{ln}] ...{t[max(0,i-60):i+len(s)+60]}...")

    if args.dry:
        print("\n(dry run, 未写入)")
        return

    n_applied = 0
    for old, new_v2, new_html, exp in FIXES:
        n_v2 = sum(counts(t, old) for t in v2_text.values())
        if n_v2 != exp:
            print(f"SKIP {old} (v2={n_v2} exp={exp})")
            continue
        for f in v2_files:
            if old in v2_text[f]:
                v2_text[f] = v2_text[f].replace(old, new_v2)
        if old in html:
            html = html.replace(old, new_html if new_html is not None else new_v2)
        n_applied += 1

    # 行级清理
    for f in v2_files:
        lines = v2_text[f].split("\n")
        out = []
        for line in lines:
            if line.strip() in LINE_DELETE:
                continue
            out.append(line)
        v2_text[f] = "\n".join(out)
    for s in LINE_DELETE:
        html = html.replace(f"<p>{s}</p>", "")
    for old, new in LINE_STRIP:
        for f in v2_files:
            v2_text[f] = v2_text[f].replace(old, new)
        html = html.replace(old, new)

    for f in v2_files:
        io.open(f, "w", encoding="utf-8", newline="").write(v2_text[f])
    io.open(READER, "w", encoding="utf-8", newline="").write(html)
    print(f"已写入 {n_applied} 组修正 + 行级清理")


if __name__ == "__main__":
    main()
