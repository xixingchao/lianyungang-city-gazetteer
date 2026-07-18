# -*- coding: utf-8 -*-
"""Restore sports school intro and kindergarten section from page OCR."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_sports_school_intro_kindergarten_20260703.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_sports_school_intro_kindergarten_20260703.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260703_第五十六卷学校体育幼儿体育回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SOURCE_NOTE = (
    "workbench/ocr/paddle_ocr/下/part02/page_0224.txt:10-40; "
    "workbench/ocr/paddle_ocr/下/part02/page_0225.txt:3-28"
)
SCOPE_START = '<h3 id="第五十六卷-第二章学校体育">第二章学校体育</h3>'
SCOPE_END = '<h4 id="第五十六卷-第二章学校体育-第二节小学体育">第二节小学体育</h4>'

NEW_HTML = """<p>清朝末年，废科举、兴学堂，在学堂中开设体操课。民国12年（1923年），体操课改为体育课，教学内容有体操、田径、球类、国术和游戏。由于体育师资缺、设备差等原因，学校体育开设的项目和参加活动的学生都不多。建国后，全市大、中、小学和幼儿体育开始得到重视和发展，体育设施逐步改善，开展的体育项目和参加活动的人数不断增加。“文化大革命”期间，学校体育活动受到干扰和破坏。1979年贯彻《全国学校体育、卫生工作经验交流会议纪要》，各级教育行政部门和学校领导进一步加强了对体育工作的领导，增加体育经费，改善体育设施，认真坚持“两课”、“两操”、“两活动”，推行《国家体育锻炼标准》，加强体育传统项目学校建设，竞赛成绩不断提高，学生体质普遍增强，并向国家和省输送一批优秀运动员。</p>
<h4 id="第五十六卷-第二章学校体育-第一节幼儿体育">第一节幼儿体育</h4>
<p><strong>一、幼儿园体育活动</strong></p>
<p>建国前，市内没有正规的幼儿体育活动。建国后，幼儿教育事业得到较快发展，幼儿体育活动也随之开展起来。幼儿园体育包括早操、体育课和户外体育活动三个方面。全市各幼儿园均按照国家颁布的《幼儿园教育纲要》和根据《幼儿园教育纲要》编写的体育教材进行教学安排。</p>
<p>早操进行的时间为10分钟。小班以模仿操为主，中、大班以徒手操为主。有的选学轻器械操，每学期更换1～2套，有的用2～3套操交换做。体育课每天一节（15～30分钟）。</p>
<p>户外体育活动是幼儿一天生活中不可缺少的内容。每天保证了两小时户外体育活动时间，一般安排在晨间、上课后和午睡后进行。</p>
<p>各幼儿园每学期除按体育课教材进行教学外，还安排一些小型的体育比赛，如举办运动会、单项比赛，排练文娱节目和团体操等。</p>
<p>1986年后，根据幼儿园教具配备目录，市、县（区）各个幼儿园添置了玩具和各类体育器材。</p>
<p>市机关幼儿园运动场上大型玩具有滑梯、转椅、荡船、小飞机、攀登架、压压板等，室内还有各种玩具。市钟声幼儿园三个运动场设有旋转亭、吊环、爬竿、攀登架、系列玩具、金鱼滑梯、转椅等。</p>
<p><strong>二、幼儿体育竞赛和表演</strong></p>
<p>1955年6月1～2日，市举办少年儿童运动会。1963年6月1～2日，市体委、市文教局，团市委联合举办小篮球、乒乓球、跳皮筋比赛。1974年，市体委与市文教局、市妇女联合会、市卫生局、团市委联合举办市首届幼儿运动会。有11所幼儿园400多名幼儿参加，比赛项目有：田径、小橡皮球、拔河、蹬三轮车。按年龄分甲、乙两组进行比赛。1975年，小学生和幼儿体育运动分区进行活动，开展竞赛项目有田径、球类、广播操、拔河、技巧、小三轮车等。在“六一”儿童节前后，对全市幼儿园、托儿所的儿童，普遍进行一次健康检查。</p>
<p>1976年6月1日，市体委、市教育局、市妇女联合会联合举办了市幼儿运动会。1978年7月，市体委、市教育局等单位联合举办幼儿体育比赛。内容为：幼儿大型团体操（要求在音乐伴奏下，有队列变化）和幼儿徒手操比赛、幼儿体育游戏、幼儿运动会。项目有小皮球运球跑，小自行车比赛，障碍跑等。</p>
<p>1981年和1982年，“六一”儿童节期间，市体委、市教育局等单位联合举办了幼儿体操表演和庆“六一”文体活动。市“六一”幼儿园表演的“火炬操”，钟声幼儿园表演的“椅子操”、市汽车公司幼儿园表演的“游泳操”，市商业幼儿园表演的“花束操”和“葵花操”均获得观众的好评。1984年，市体委、市教育局等单位联合举办了幼儿体操比赛。小班比赛“竹竿操”，中班比赛拍手赛，大班比赛徒手操。新浦区中心幼儿园小班获“竹竿操”一等奖。1985年，市举行幼儿体操比赛，新浦区中心幼儿园小班获“模仿操”一等奖。1989年，市区举办幼儿体育游戏比赛。新浦区中心幼儿园表演的“小小飞行员”、市“六一”幼儿园表演的“小小消防队员”、云台区中心幼儿园表演的“炸碉堡”、省盐务局机关幼儿园表演的“小老鼠偷粮食”，均获得大会的好评。</p>
<p>1990年，各县、区安排小型多样的幼儿体育活动。</p>"""

EXPECTED_TEXT = [
    "<p><strong>一、幼儿园体育活动</strong></p>",
    "体育课每天一节（15～30分钟）。",
    "<p><strong>二、幼儿体育竞赛和表演</strong></p>",
    "比赛项目有：田径、小橡皮球、拔河、蹬三轮车",
    "有队列变化）和幼儿徒手操比赛",
    "项目有小皮球运球跑，小自行车比赛，障碍跑等",
    "“六一”儿童节期间",
    "表演的“小小飞行员”",
]
RESIDUALS = [
    "一、幼儿园体育活动建国前",
    "二、幼儿体育竞赛和表演1955年",
    "拨河、瞪三轮车",
    "拨河、蹬三轮车",
    "有队列变化和幼儿徒手操比赛",
    "项自有小皮球",
    "“六~”儿童节期间",
    "表演的”小小飞行员”",
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
        raise RuntimeError(f"sports school kindergarten expected text missing: {missing}")
    remaining = [item for item in RESIDUALS if item in segment]
    if remaining:
        raise RuntimeError(f"sports school kindergarten residue remains: {remaining}")
    return changed, {"rewrote_scope": changed}


def write_reports(changed: int, counts: dict[str, int]) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "第五十六卷体育 / 第二章学校体育 / 章首与第一节幼儿体育",
        "source": SOURCE_NOTE,
        "reader_path": str(HTML),
        "changes_this_run": changed,
        "counts": counts,
        "principle": "依据 PaddleOCR 页级文本重建学校体育章首和幼儿体育整节，修复小标题粘连、括号断裂和明确 OCR 错识。",
        "notes": ["1974年比赛项目中的“拨河”按同段体育项目上下文校正为“拔河”。"],
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    md = f"""# 第五十六卷学校体育幼儿体育回源修复

- 时间：{now}
- 范围：`第五十六卷体育 / 第二章学校体育 / 章首与第一节幼儿体育`
- 源文依据：`{SOURCE_NOTE}`

## 修复动作

- 按页级 OCR 重建 `第二章学校体育` 章首和 `第一节幼儿体育`。
- 拆分 `一、幼儿园体育活动`、`二、幼儿体育竞赛和表演` 小标题。
- 修正 `蹬三轮车`、`项目有`、`六一`、`小小飞行员` 引号，并补齐 1978 年团体操括号闭合。
- 1974 年比赛项目中的 `拨河` 按同段体育项目上下文校正为 `拔河`。
- 本次复跑新增整段替换：{changed} 处。
- 本轮未处理 `第二节小学体育`。

## 核对说明

- PaddleOCR `page_0224.txt` 确认第二章章首和幼儿园体育活动开头。
- PaddleOCR `page_0225.txt` 确认幼儿体育竞赛和表演全段，并给出第二节边界。
"""
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")


def update_memory(changed: int) -> None:
    marker = "## 2026-07-03 第五十六卷学校体育幼儿体育回源修复"
    memory = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker in memory:
        return
    entry = f"""
{marker}

- 对第五十六卷体育 `第二章学校体育` 章首和 `第一节幼儿体育` 进行回源修复。
- 源文依据：`{SOURCE_NOTE}`；重建范围，拆分 `一、幼儿园体育活动`、`二、幼儿体育竞赛和表演`，修正 `蹬三轮车`、`项目有`、`六一`、`小小飞行员` 引号，并补齐 1978 年团体操括号闭合。
- 1974 年比赛项目中的 `拨河` 按同段体育项目上下文校正为 `拔河`。
- 本轮新增整段替换 {changed} 处；`第二节小学体育` 未在本脚本中处理。
- 报告：`output/reports/reader_readability_sports_school_intro_kindergarten_20260703.md`。
"""
    MEMORY.write_text(memory.rstrip() + "\n\n" + entry.lstrip(), encoding="utf-8")


def main() -> None:
    changed, counts = patch_reader()
    write_reports(changed, counts)
    update_memory(changed)
    print("sports school intro and kindergarten repaired")
    print(f"changes={changed}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()
