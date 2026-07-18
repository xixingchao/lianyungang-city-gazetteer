# -*- coding: utf-8 -*-
"""Restore sports overview and social sports opening from page OCR."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_sports_overview_social_start_20260703.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_sports_overview_social_start_20260703.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260703_第五十六卷体育概述社会体育开头回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SOURCE_NOTE = (
    "workbench/ocr/paddle_ocr/下/part02/page_0216.txt:3-32; "
    "workbench/ocr/paddle_ocr/下/part02/page_0217.txt:3-35; "
    "workbench/ocr/paddle_ocr/下/part02/page_0218.txt:3-36; "
    "workbench/ocr/paddle_ocr/下/part02/page_0219.txt:3-35"
)

OVERVIEW_START = '<h3 id="第五十六卷-概述">概述</h3>'
OVERVIEW_END = '<h3 id="第五十六卷-第一章社会体育">第一章社会体育</h3>'
SOCIAL_START = '<h3 id="第五十六卷-第一章社会体育">第一章社会体育</h3>'
SOCIAL_END = '<h4 id="第五十六卷-第一章社会体育-第一节民间传统体育">第一节民间传统体育</h4>'
TRADITIONAL_START = '<h4 id="第五十六卷-第一章社会体育-第一节民间传统体育">第一节民间传统体育</h4>'
TRADITIONAL_END = '<h4 id="第五十六卷-第一章社会体育-第二节职工体育">第二节职工体育</h4>'
WORKER_START = '<h4 id="第五十六卷-第一章社会体育-第二节职工体育">第二节职工体育</h4>'
WORKER_END = '<h4 id="第五十六卷-第一章社会体育-第三节农民体育">第三节农民体育</h4>'

NEW_OVERVIEW = """<p>连云港市民间传统体育历史悠久，项目繁多，早在1800年前，已有武术活动。唐代，海州创建儒学堂，武术和游戏等健身活动进入教育领域。清代光绪二十八年（1902年）颁布的小学堂教育宗旨指出“援以道德及一切有益身体之事”，学堂课程中设置“体操”一科，每年在海州小校场举行一次比武活动。</p>
<p>民间传统体育项目除武术外，还有登山、游泳、拔河、爬绳、举石锁、跳绳、踢毽子、放风筝等，娱乐体育有舞龙灯、舞狮子、玩旱船、踩高跷、抽陀螺、捣拐、踢瓦、滚铁环、抖空竹、掷沙包、捉迷藏等，此外还有“憋死茅”、“四步顶”、“六步洲”等乡土棋。</p>
<p>民国5年（1916年），海州开始有了现代体育活动。中、小学校开设了体育课，校际之间经常开展球类比赛。民国21年，赣榆县城民众自发组建国术研究社，研究各种套路器械20种；驻灌云税警团也聘请名师教拳。民国23年，东海县农民教育馆成立，下设国术团，教授少林拳，当时的《东海农报》经常介绍中国武术知识。民国24年，驻海州的税警团成立励志社，这是海州第一个专门从事群众性现代体育活动的组织。民国25年，新浦创办建华体育会，同时成立健华篮球队。民国25～27年间，海州建起体育场；民国29年，在新浦成立体友篮球队，不久“建强”、“虎啸”、“试试看”等篮球队相继成立，赛事频繁，推动了海属地区篮球活动的开展。</p>
<p>1949～1959年间，为促进体育事业发展，人民政府对体育部门基建共投资11万余元，下拨体育活动经费17万余元。1955年4月成立了市体育运动委员会，举办大型市级体育竞赛125次，有32758人次参加活动；全市建立基层体育协会105个，会员21362人；举办各种体育积极分子、体育干部训练班84期，培训2511人次；全市开展的体育活动项目有25个，有基层篮球队795个，球场341个；积极推行广播操、《准备劳动与卫国体育制度》（简称“劳卫制”）、国家等级运动员制度和裁判员制度。</p>
<p>1960～1962年，人民生活困难，群众体育活动减少。“文化大革命”开始后，工厂停产，学校停课，体育事业受到干扰和破坏，到了“文化大革命”后期，篮球、排球、足球、乒乓球以及群众性游泳、长跑活动才有所开展。</p>
<p>1977年始，全市各级学校认真贯彻、落实全国学校体育、卫生工作经验交流会精神，绝大部分学校坚持每天一小时体育锻炼时间，能坚持“两课”（每周两节体育课）、“两操”（每天做广播操和眼保健操）、“两活动”（每周两节课外体育活动）。全市推行《国家体育锻炼标准》的“达标”率连续五年获省第一名，东海县连续七年获省“达标”率第一名。体育传统项目学校办学质量明显提高，1984～1989年，东海县牛山小学、东海县中学、新浦中学被评为全国体育传统项目学校先进集体。市、县（区）学校每年都要举行一二次田径运动会，学生体质普遍增强，体育竞赛成绩不断提高。至1990年，全市中、小学校中，有省级体育传统项目学校13所，市级体育传统项目学校22所。县、区级体育传统项目学校48所。</p>
<p>全市机关、厂矿企事业单位普遍建立体育组织，开展夏游泳、秋登山、冬长跑、常年做广播操等多种多样群众性体育活动。全市农村40%以上乡镇成立农民体育协会、文化中心等组织，普遍兴建篮球场、乒乓球室、棋室，购置多种体育器材。市举办了全民运动会、职工运动会、农民运动会、老年人运动会、伤残人运动会，三县也办过规模较大的农民运动会。东海县浦南乡每年举办一届运动会，比赛项目有20多个，成为远近闻名的体育先进乡。市化工公司、涤纶厂分别于1984年和1985年被评为全国职工体育先进集体。1985年，国家体育运动委员会（简称“国家体委”）授予连云港市赵国祥、马德胜、李兴忠、顾洪伦、汪金奎、许友堂“新中国体育开拓者”荣誉证书。1988年，灌云县被国家体委命名为“全国体育先进县”，该县乡镇建起18个灯光球场，出现了篮球村、篮球乡。</p>
<p>1986年，新建了以培养体育人才为重点的连云港市体育运动学校和连云港市云峰中学，会同原有的连云港市少年儿童业余体校，形成“一条龙”式的新的训练体制，提高了训练水平。1990年，经市政府批准，成立体育3项（柔道、摔跤、田径）专业队。连云港市开展的体育项目中，男子篮球、女子排球、女子足球、无线电测向、柔道、摔跤等在全省一直保持优势。1978～1990年，市体育代表团（队）参加省、全国比赛，共获得金牌155块、银牌156块、铜牌131块。在第五届、第六届全运会上，连云港市籍运动员夺得金牌数和团体总分分别列全省第二位和第六位。自1956年以来，连云港市向国家、省输送体育优秀运动员181人，如韩永年现任国家田径队总教练、领队，为中国田径事业作出了贡献。</p>
<p>建国后，省、市政府多次拨款兴建和整修体育活动场所。市区先后兴建了体育馆、训练馆、游泳池、人民体育场和主席台楼、体育服务综合楼、室外灯光球场、旱冰场、游泳馆、海滨浴场。三县四区也先后投资兴建体育设施，如东海县建了乒乓训练房、灯光球场、田径场和三层楼主席台、游泳池。赣榆县和灌云县建了田径场、灯光球场和游泳馆。淮海工学院、连云港矿业化学专科学校、连云港职业大学、新海中学、连云港师范学校，也先后建成400米标准田径场。这些体育场所的兴建和整修，为体育的普及和提高创造了条件。</p>"""

NEW_SOCIAL = """<p>20世纪初，现代体育传入市内，由学校向社会发展。30年代篮球、排球、足球、田径等项体育运动逐渐有所开展，但工人、农民生活难以维持，未参加体育活动。</p>
<p>建国后，民间传统体育和职工、农民、老年人、残疾人体育均得到发展。参加打球、跑步、操拳、舞剑、游泳等项活动的人越来越多，体育深入社会、深入家庭。</p>
<p>在1956年和1984年两届省职工运动会上，市职工代表队共获得田径5项冠军，男子篮球队获两次亚军。东海县老年门球队1986～1990年，参加市、省、全国比赛，共获金牌5块、银牌2块、铜牌1块。在1984年和1987年两届省残疾人运动会上，市残疾人运动员获得金牌14块、银牌15块、铜牌9块。残疾人李扬3次参加乒乓球国际比赛，获得金牌3块、银牌3块和“最佳运动员”称号。市武术和风筝代表队，在历次比赛中也取得较好成绩。</p>"""

NEW_TRADITIONAL = """<p><strong>一、武术</strong></p>
<p>民国23年（1934年），东海县农民教育馆成立，下设国术团，由东海县驼峰乡武师传授少林拳。后来，国术团成员投入抗日洪流，与日军浴血奋战。民国21年，云台区蝙蝠山头有人请山东武师在家开设拳堂，当地23人学拳术，民国28年日军入侵后，拳堂解散。同年，赣榆县城民众自发组建国术研究社，研究各种套路器械20种；驻灌云县税警团也请名师教拳。</p>
<p>建国后，人民政府重视武术事业，组织市武术队，在市少年业余体校设武术班，配有专职教练，参加省和国家武术比赛和观摩表演大会，均取得较好成绩。1959年，江苏省第五届运动会武术比赛在南京举行，徐州专区代表队获武术团体冠军，新海连市张风山参赛。</p>
<p>1973年，省武术观摩赛在沛县举行，陈克俭、王振庭获传统拳术、大刀优秀项目奖。</p>
<p>1982年，江苏省第十届运动会在南京举行，张浩获男子全能、长拳两项第一名。1982年5月，全国武术观摩交流会在西安举行，张浩获醉剑冠军。1984年4月，在江苏省武术挖掘整理普查展览暨老拳师和稀有拳种观摩表演大会上，赣榆县农民刘洪锦的世传器械“夹子矛”和套路“旋风八卦掌”被确认为稀有器械和拳种，并摄制录相片存档，刘洪锦赴南京五台山体育馆献艺。1984年省第二届职工武术比赛、省第一届农民运动会、1990年省十二届运动会武术比赛，连云港市武术运动员均参赛，共获铜牌3块。</p>
<p>赣榆县拳师徐小龙自幼习武，后与其兄徐小义加入上海市武术协会，其“梅花拳”威震上海滩。徐小龙曾出访日本、美国、香港献艺并参加多部武侠影片的拍摄，颇受赞赏。</p>
<p><strong>二、民俗体育</strong></p>
<p><strong>拔河</strong>连云港市沿海渔民及船民历来有拔河习俗，这与沿海渔猎及水乡拉纤有关。</p>
<p>建国后，市历届职工、农民、妇女运动会上，都把拔河作为竞赛项目，学校也经常开展拔河比赛。</p>
<p><strong>爬绳（或爬竿）</strong>连云港市城乡中小学校里，大都设置吊绳或吊竿。至1990年，一些大、中专学校也设置吊绳或吊竿，供师生课外活动锻炼身体。</p>
<p><strong>踢毽子</strong>连云港市的踢毽子活动，在青少年中开展广泛，每年冬季，三五成群，相聚在一起，以踢毽子为乐、取暖，有时也互比高低。建国后，踢毽之风更盛，技巧更高。冬季在学校中普遍开展踢毽子活动，并进行个人和集体比赛。1987年，省教育委员会（简称“省教委”）和省体育运动委员会（简称“省体委”）号召全省中小学在冬季开展长跑、跳绳、踢毽子三项活动，并举行通讯比赛，全市中小学生积极响应。</p>
<p><strong>跳绳</strong>境内明、清时代就有跳绳活动，且花样很多，有短绳、长绳各种跳法。全市城乡中小学、幼儿园冬季常举办跳绳比赛。此项运动久盛不衰。</p>
<p><strong>放风筝</strong>放风筝是连云港市人民普遍喜爱的一种活动。1988年，海州区代表队赴潍坊参加全国第三届风筝比赛。1989年，海州区风筝协会成立。同年海州区风筝代表队代表市参加在南通举办的全国“紫琅杯”风筝邀请赛，参加潍坊中国风筝精英大奖赛，参加北京第二届国际风筝邀请赛，有4人获得两项冠军、两项亚军。1990年7月，海州区风筝代表队在第三届北京国际风筝邀请赛中，获得团体总分第二名，单项获金牌3块、银牌2块、铜牌5块。</p>
<p><strong>趣棋（又名乡土棋）</strong>连云港市城乡人们世代喜欢下趣味棋，如“憋死茅”、“四步顶”、“六步洲”等。棋盘随处可画，棋子为砖块、石子，随处可寻，简便易学，道旁、田头、庭院、公园，都是下棋的好场所。</p>
<p><strong>娱乐体育</strong>有舞龙灯、舞狮子、玩旱船、踩高跷、捉迷藏、荡秋千、抽陀螺、打梭、捣拐、踢瓦、滚铁环、掷沙包、抖空竹、跳皮筋、练石担、石锁等。</p>"""

WORKER_REPLACEMENTS = [
    (
        "<p>等行业职工篮球队参加宣传购买人民胜利折实公债、劝募寒衣、抗美援朝捐献等义赛活动。",
        "<p>1950年“五一”节，新海连市举办首届工人“劳动杯”篮球赛。并先后组织盐场、银行等行业职工篮球队参加宣传购买人民胜利折实公债、劝募寒衣、抗美援朝捐献等义赛活动。",
    ),
    ("准北盐场职工男子排球队", "淮北盐场职工男子排球队"),
    ("开展劳卫制”锻炼", "开展“劳卫制”锻炼"),
]

EXPECTED_TEXT = [
    "颁布的小学堂教育宗旨指出“援以道德及一切有益身体之事”",
    "掷沙包、捉迷藏等，此外还有“憋死茅”",
    "农民运动会。东海县浦南乡每年举办一届运动会",
    "体育3项（柔道、摔跤、田径）专业队",
    "1978～1990年，市体育代表团",
    "在第五届、第六届全运会上",
    "体育深入社会、深入家庭",
    "市职工代表队共获得田径5项冠军",
    "<strong>一、武术</strong>",
    "投入抗日洪流",
    "两项第一名",
    "挖掘整理普查展览暨老拳师和稀有拳种观摩表演大会",
    "<strong>二、民俗体育</strong>",
    "全国“紫琅杯”风筝邀请赛",
    "1950年“五一”节，新海连市举办首届工人“劳动杯”篮球赛",
]
RESIDUALS = [
    "颁每年在海州小校场",
    "抖空竹、掷民国5年",
    "《准备劳动与卫国体育制度》概述2501",
    "农民运动乡",
    "柔道摔、由径",
    "19781990年",
    "柔道、摔等",
    "全运全上",
    "体育深人社会",
    "乒丘球",
    "一、武　术民国23年",
    "投人抗日洪流",
    "两项第名",
    "二、民俗体育拔河",
    "踢键子",
    "代京第二届国际风筝邀请赛",
    "荡秋干",
    "<p>等行业职工篮球队参加宣传购买",
    "准北盐场职工男子排球队",
    "开展劳卫制”锻炼",
]


def replace_scope(text: str, start_marker: str, end_marker: str, new_html: str) -> tuple[str, int]:
    start = text.index(start_marker) + len(start_marker)
    end = text.index(end_marker, start)
    new_segment = "\n" + new_html + "\n"
    changed = int(text[start:end] != new_segment)
    if changed:
        text = text[:start] + new_segment + text[end:]
    return text, changed


def patch_reader() -> tuple[int, dict[str, int]]:
    text = HTML.read_text(encoding="utf-8")
    changes = 0
    text, changed = replace_scope(text, OVERVIEW_START, OVERVIEW_END, NEW_OVERVIEW)
    changes += changed
    text, changed = replace_scope(text, SOCIAL_START, SOCIAL_END, NEW_SOCIAL)
    changes += changed
    text, changed = replace_scope(text, TRADITIONAL_START, TRADITIONAL_END, NEW_TRADITIONAL)
    changes += changed

    worker_start = text.index(WORKER_START) + len(WORKER_START)
    worker_end = text.index(WORKER_END, worker_start)
    worker_segment = text[worker_start:worker_end]
    worker_changes = 0
    for before, after in WORKER_REPLACEMENTS:
        if before in worker_segment:
            worker_segment = worker_segment.replace(before, after)
            worker_changes += 1
    if worker_changes:
        text = text[:worker_start] + worker_segment + text[worker_end:]
        changes += worker_changes

    if changes:
        HTML.write_text(text, encoding="utf-8")

    text = HTML.read_text(encoding="utf-8")
    start = text.index(OVERVIEW_START) + len(OVERVIEW_START)
    end = text.index(WORKER_END, start)
    segment = text[start:end]
    missing = [item for item in EXPECTED_TEXT if item not in segment]
    if missing:
        raise RuntimeError(f"sports expected text missing: {missing}")
    remaining = [item for item in RESIDUALS if item in segment]
    if remaining:
        raise RuntimeError(f"sports residue remains: {remaining}")
    return changes, {"scopes_rewritten": 3, "worker_front_replacements": worker_changes}


def write_reports(changes: int, counts: dict[str, int]) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "第五十六卷体育 / 概述、第一章社会体育开头、第一节民间传统体育、第二节职工体育首段",
        "source": SOURCE_NOTE,
        "reader_path": str(HTML),
        "changes_this_run": changes,
        "counts": counts,
        "principle": "依据 PaddleOCR 页级文本补回漏句、去除页眉串入、拆分小标题，并修正明确 OCR 错识。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    md = f"""# 第五十六卷体育概述社会体育开头回源修复

- 时间：{now}
- 范围：`第五十六卷体育 / 概述`、`第一章社会体育` 开头、`第一节民间传统体育`、`第二节职工体育` 首段
- 源文依据：`{SOURCE_NOTE}`

## 修复动作

- 按页级 OCR 补回概述开头 `小学堂教育宗旨` 句和民间体育项目漏文。
- 清除 `概述2501` 页眉串入，修正 `农民运动会`、`柔道、摔跤、田径`、`1978～1990年`、`全运会上` 等错识。
- 补回社会体育开头省职工运动会成绩句，修正 `深入`、`乒乓球`。
- 拆分 `一、武术`、`二、民俗体育` 及民俗体育分项，并补回风筝邀请赛漏文。
- 补回 `第二节职工体育` 首段被截断的 `1950年“五一”节...` 起句。
- 稳定复跑新增改动：{changes} 处；首次执行已写入 3 个整段范围和 3 处职工体育首段替换，后因自检残留词过宽中止，已修正自检后复跑为 0。
- 本轮未处理 `第二节职工体育` 主体后续段落和 `第三节农民体育`。

## 核对说明

- PaddleOCR `page_0216.txt` 确认第五十六卷标题、概述开头和 1949～1959 年段落。
- PaddleOCR `page_0217.txt` 确认概述尾段和 `第一章社会体育` 前边界。
- PaddleOCR `page_0218.txt` 确认社会体育开头、残疾人乒乓球句、民间传统体育和武术段。
- PaddleOCR `page_0219.txt` 确认民俗体育段和职工体育首段。
"""
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")


def update_memory(changes: int) -> None:
    marker = "## 2026-07-03 第五十六卷体育概述社会体育开头回源修复"
    memory = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker in memory:
        return
    entry = f"""
{marker}

- 对第五十六卷体育 `概述`、`第一章社会体育` 开头、`第一节民间传统体育` 和 `第二节职工体育` 首段进行回源修复。
- 源文依据：`{SOURCE_NOTE}`；补回页级 OCR 确认的漏句，清除 `概述2501` 页眉串入，修正 `柔道、摔跤、田径`、`1978～1990年`、`深入`、`乒乓球`、`投入` 等错识，并拆分民间传统体育小标题。
- 首次执行写入 3 个整段范围和 3 处职工体育首段替换；修正自检后稳定复跑新增改动 {changes} 处。职工体育主体后续段落和农民体育未在本脚本中处理。
- 报告：`output/reports/reader_readability_sports_overview_social_start_20260703.md`。
"""
    MEMORY.write_text(memory.rstrip() + "\n\n" + entry.lstrip(), encoding="utf-8")


def main() -> None:
    changes, counts = patch_reader()
    write_reports(changes, counts)
    update_memory(changes)
    print("sports overview and social sports opening repaired")
    print(f"changes={changes}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()
