# -*- coding: utf-8 -*-
"""Restore sports worker section from page OCR."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_sports_worker_section_20260703.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_sports_worker_section_20260703.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260703_第五十六卷职工体育回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SOURCE_NOTE = (
    "workbench/ocr/paddle_ocr/下/part02/page_0219.txt:27-40; "
    "workbench/ocr/paddle_ocr/下/part02/page_0220.txt:3-40; "
    "workbench/ocr/paddle_ocr/下/part02/page_0221.txt:3-13"
)
SCOPE_START = '<h4 id="第五十六卷-第一章社会体育-第二节职工体育">第二节职工体育</h4>'
SCOPE_END = '<h4 id="第五十六卷-第一章社会体育-第三节农民体育">第三节农民体育</h4>'

NEW_HTML = """<p>1950年“五一”节，新海连市举办首届工人“劳动杯”篮球赛。并先后组织盐场、银行等行业职工篮球队参加宣传购买人民胜利折实公债、劝募寒衣、抗美援朝捐献等义赛活动。1951年，新海连市职工篮球队参加临沂地区篮球赛获冠军。1954年，市体育分会筹委会在面粉厂进行工间操试点工作。截止年底，有70%职工参加做操并成立锻炼小组开展体育活动。</p>
<p>1955年，市体育分会、市工会贯彻全国职工体育运动会议精神。全市职工中组织各种运动锻炼队311个，还组织体操队去厂矿巡回表演，推动厂矿体育活动的开展。淮北盐场职工男子排球队参加在天津举行的全国盐业系统排球赛，获亚军。</p>
<p>1956年，组织工人代表队参加省第一届马拉松比赛。盐场职工男子排球队到大连参加四大盐区排球赛，获得第三名。1957年，全市有26个单位开展“劳卫制”锻炼，参加职工2804人。建成篮球场127个。全年举办了职工篮球、排球、乒乓球、田径、举重、自行车、拔河、象棋8种单项比赛，参加职工2578人。冬季举办万名职工长跑活动。1958年3月，省马拉松对抗赛在常熟举行，新海连市职工许友堂以2小时30分2秒8的成绩获得冠军。</p>
<p>10月，职工乔富国在常熟参加省马拉松比赛，又以2小时52分24秒成绩获得第一名。</p>
<p>1959年冬季，据30个厂矿统计，参加冬锻的职工有9800人。</p>
<p>1960年初，新海连市人民委员会发出开展工间操通知，各机关企业事业单位组织实施，出现了一批先进单位，如市麻纺厂职工人人都做工间操，市汽车公司全体职工上班前十分钟做广播操。全市每年还开展群众性冬季锻炼活动，开展得较好的单位有淮北盐场、化肥厂、新海电厂等28个，组织职工运动锻炼队488个，有4576人参加活动。10～12月，在江苏省篮、排、足、手球等级赛中，市男、女篮球队分别获得新海连和南通赛区冠军，市男、女手球队双双获得淮阴赛区的亚军。1961年，厂矿企业开展广播操、太极拳等运动量小、形式简便、小型分散的体育活动。市射击场每逢星期日对外免费开放，至年底，市眼镜厂、市邮电局、市印刷厂、市汽车公司、市绝缘材料厂等16个单位有70人达到普通射手水平。</p>
<p>1962年2月，在青年体育馆进行职工“胜利杯”乒乓球赛，有9个队参赛，市财贸系统职工获得冠军。“三八”妇女节举办五项体育竞赛，盐场工人获得篮球和拔河两项冠军。</p>
<p>1963年，厂矿企业普遍开展广播操活动。各单位举办单项体育竞赛95次，参加职工达4775人次。1964年元旦，举办7单位射击对抗赛，4月举办市职工公路自行车选拔赛，7月举办职工射击赛，有50名运动员参赛。1965年，职工继续开展以广播操为主的小型多样体育活动。新浦、海州两区分别在市造纸厂、新海电厂等23个单位开展工间操活动，做到定人、定时、定期检查评比。市体育运动委员会（简称“市体委”）于4月至11月举办职工“劳动杯”篮球赛、职工自行车锦标赛、职工乒乓球比赛。</p>
<p>“文化大革命”前期，职工体育活动一度处于停滞状态。</p>
<p>1972年，在体育馆举办职工拔河比赛，有41个单位参赛，锦屏公社、省盐务管理局职工分获男、女冠军。1973年10月，市体委承办全国举重比赛，连云港市有9名运动员参赛。1976年，全市厂矿企业普遍恢复了广播操活动，有30%的职工还经常参加球类、跑步、游泳、打太极拳等活动。涌现出市造纸厂、市锅炉厂、市光明碳素厂等先进单位。同年举办市职工运动会1次，基层运动会250次。</p>
<p>1978年11月，市体委与工会举办职工排球赛，并派市代表队参加省春季长跑比赛，男、女队员11人均进入前6名。4月6日省体委批准市变压器厂、麻纺厂等8个厂矿为体育学大庆式企业。1979年，职工体育抓一操（广播操）、一跑（长跑）、一球（篮球）活动，70%职工参加活动，建立业余队162个，队员1258人。</p>
<p>1981年，在职工中推广第六套广播操，市体委举办7期领操员训练班，培训230人。开展解放路一条街“开门操”体育活动，有15个单位近千名职工参加。1982年，市体委举办11期领操员训练班，有800人参加。有18万职工去海滨浴场和游泳池游泳，787人参加元旦迎春长跑，五个操拳活动站有350名职工参加活动。1984年，市造纸厂、市罐头厂、锦屏磷矿、市涤纶厂、市农药厂、市化工公司、市体委群体科被省体委、省总工会授予“江苏省职工体育先进集体”称号。</p>
<p>1985年，全市厂矿企业单位、产业系统和各区共举办体育竞赛活动2312次，参加活动47600人次。是年，锦屏磷矿男篮获得华东地区化工矿山篮球赛冠军，并代表省参加全国化工矿山篮球赛。市粮食系统男篮获省粮食系统篮球赛第一名。市体委还承办了省键球比赛。1986年，职工健美运动，在部分厂矿企业逐渐开展起来。市电化厂工人张惠民两次参加全国健美比赛，分别获得无级别冠军和70公斤级冠军。连云港港务局陈永明参加全国海上帆板比赛获第三名。1987年，连云港市组织职工参加全国万名职工冬季长跑活动。1988年，连云港市“劳动杯”篮球赛于5月20日至27日在市体育馆举行，并选出代表队参加省第二届“劳动杯”篮球赛。市举办元旦长跑赛。</p>
<p>1989年，全国总工会宣传部、国家体委授予连云港市“万名职工冬季长跑活动先进城市”称号，授予化工部化工矿山设计研究院“冬季职工长跑先进基层单位”称号。同年10月，连云区首届职工运动会在墟沟举行，设田径、乒乓球、射击等项目，参赛运动员675人。</p>
<p>1990年10月，连云区举办第二届职工运动会，项目与第一届运动会相同。</p>"""

EXPECTED_TEXT = [
    "职工乔富国在常熟参加省马拉松比赛",
    "市男、女手球队双双获得淮阴赛区的亚军",
    "1961年，厂矿企业开展广播操、太极拳等运动量小、形式简便、小型分散的体育活动",
    "市眼镜厂、市邮电局、市印刷厂",
    "1963年，厂矿企业普遍开展广播操活动。各单位举办单项体育竞赛95次",
    "选拔赛",
    "1981年，在职工中推广第六套广播操",
    "职工健美运动，在部分厂矿企业逐渐开展起来",
    "连云区首届职工运动会在墟沟举行",
    "项目与第一届运动会相同",
]
RESIDUALS = [
    "职工养富国",
    "手球队型分散",
    "市体育活动。市射击场",
    "市眼镜广",
    "选拨赛",
    "遂渐开展",
    "同年10月，连1990年",
    "第届运动会相同",
]


def find_scope(text: str) -> tuple[int, int]:
    start = text.index(SCOPE_START) + len(SCOPE_START)
    end = text.index(SCOPE_END, start)
    return start, end


def patch_reader() -> tuple[int, dict[str, int]]:
    text = HTML.read_text(encoding="utf-8")
    start, end = find_scope(text)
    new_segment = "\n" + NEW_HTML + "\n"
    changed = int(text[start:end] != new_segment)
    if changed:
        HTML.write_text(text[:start] + new_segment + text[end:], encoding="utf-8")

    text = HTML.read_text(encoding="utf-8")
    start, end = find_scope(text)
    segment = text[start:end]
    missing = [item for item in EXPECTED_TEXT if item not in segment]
    if missing:
        raise RuntimeError(f"sports worker expected text missing: {missing}")
    remaining = [item for item in RESIDUALS if item in segment]
    if remaining:
        raise RuntimeError(f"sports worker residue remains: {remaining}")
    return changed, {"rewrote_scope": changed}


def write_reports(changed: int, counts: dict[str, int]) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "第五十六卷体育 / 第一章社会体育 / 第二节职工体育",
        "source": SOURCE_NOTE,
        "reader_path": str(HTML),
        "changes_this_run": changed,
        "counts": counts,
        "principle": "依据 PaddleOCR 页级文本重建职工体育整节，补回跨页漏句并修正明确 OCR 错识。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    md = f"""# 第五十六卷职工体育回源修复

- 时间：{now}
- 范围：`第五十六卷体育 / 第一章社会体育 / 第二节职工体育`
- 源文依据：`{SOURCE_NOTE}`

## 修复动作

- 按页级 OCR 重建 `第二节职工体育` 整节。
- 补回 `1961年` 小型分散体育活动、`1963年` 单项竞赛和 `1981年` 第六套广播操等漏句。
- 修正 `乔富国`、`手球队双双获得淮阴赛区的亚军`、`眼镜厂`、`选拔赛`、`逐渐`、`连云区首届职工运动会`、`第一届运动会` 等错识。
- 本次复跑新增整段替换：{changed} 处。
- 本轮未处理 `第三节农民体育`。

## 核对说明

- PaddleOCR `page_0219.txt` 确认第二节开头至 1957 年段。
- PaddleOCR `page_0220.txt` 确认 1957 年尾至 1985 年开头。
- PaddleOCR `page_0221.txt` 确认 1985 年尾至 1990 年连云区第二届职工运动会，并给出第三节边界。
"""
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")


def update_memory(changed: int) -> None:
    marker = "## 2026-07-03 第五十六卷职工体育回源修复"
    memory = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker in memory:
        return
    entry = f"""
{marker}

- 对第五十六卷体育第一章社会体育 `第二节职工体育` 进行回源修复。
- 源文依据：`{SOURCE_NOTE}`；重建整节，补回 1961、1963、1981 年漏句，并修正 `乔富国`、`手球队双双获得淮阴赛区的亚军`、`眼镜厂`、`选拔赛`、`逐渐`、`连云区首届职工运动会` 等错识。
- 本轮新增整段替换 {changed} 处；`第三节农民体育` 未在本脚本中处理。
- 报告：`output/reports/reader_readability_sports_worker_section_20260703.md`。
"""
    MEMORY.write_text(memory.rstrip() + "\n\n" + entry.lstrip(), encoding="utf-8")


def main() -> None:
    changed, counts = patch_reader()
    write_reports(changed, counts)
    update_memory(changed)
    print("sports worker section repaired")
    print(f"changes={changed}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()
