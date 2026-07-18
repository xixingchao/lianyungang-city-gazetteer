# -*- coding: utf-8 -*-
"""Restore sports military-sports section from page OCR."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_sports_military_section_20260703.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_sports_military_section_20260703.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260703_第五十六卷军体类回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SOURCE_NOTE = (
    "workbench/ocr/paddle_ocr/下/part02/page_0238.txt:8-40; "
    "workbench/ocr/paddle_ocr/下/part02/page_0239.txt:3-40; "
    "workbench/ocr/paddle_ocr/下/part02/page_0240.txt:3-6"
)
SCOPE_START = '<h4 id="第五十六卷-第三章运动项目-第三节军体类">第三节军体类</h4>'
SCOPE_END = '<h4 id="第五十六卷-第三章运动项目-第四节其它类">第四节其它类</h4>'

NEW_HTML = """<p><strong>一、射击</strong></p>
<p>1958年，新海连市开展射击运动，成立了市射击运动俱乐部，新建一个简易射击场，举办射击训练班，共培养普通射手1973人。1959年，市举办射击比赛两次，有136人参赛。参加省和专区比赛5次，有30人参赛。在徐州专区射击比赛中，新海连市获团体冠军和5个单项冠军。</p>
<p>1960年，通过培训，达到普通射手及格水平的有6309人（其中社员1973人）。市新海印刷厂组织200名职工参加射击活动。1961年，市射击与航海、航空模型、航海模型4个俱乐部合并为连云港市国防体育俱乐部。1963年，市举办5期射击训练班，培训骨干2981人。全市有49个单位1479人开展民兵射击活动。市国防体育俱乐部会同市武装部组织学生参加军事野营训练，有499人达到普通射手水平。市组队参加1963年江苏省射击锦标赛，男子组获第11名，女子组获第10名。1964年元旦，举办7单位（市眼镜厂、新海中学及5个街道居委会）射击对抗赛，市眼镜厂和民主街居委会分获男、女团体第一名。</p>
<p>同年6月，举办市射击锦标赛。锦屏矿校和新浦中学分获男、女团体第一名。6月，江苏省国防体育俱乐部物色优秀运动员，连云港市有2人被录取。7月，市举办职工民兵射击赛，有250名男、女运动员参赛，市造纸厂和市眼镜厂分获男、女团体第一名。1965年，在全市大力开展四项运动（射击、游泳、登山、通讯）和军事野营活动，举办射击训练班，有3003人达到普通射手及格水平。市举办射击竞赛4次。</p>
<p>“文化大革命”期间，射击场地、器材、设备遭到破坏，活动中断。</p>
<p>1976年，市体委成立军体科，负责管理军事体育活动，俱乐部工作终止。射击运动恢复活动，与民兵训练结合，举办小型射击比赛。1976～1983年，市举办3次中学生射击比赛、5次小学生射击比赛，还举办了职工射击比赛。有36人次创9项市射击新纪录，43人次破10项市纪录，参加省射击比赛15次，有3人破省纪录，其中纪树清1978年以98环成绩破男子小口径普通枪10发卧射省纪录，王共岭1981年以345环成绩破男子汽步枪10米40发立射省纪录，袁亚玲1982年以585环成绩破女子小口径标准步枪60发射击省纪录。向省队输送3名优秀运动员。</p>
<p>1983年，市体委机构调整，撤销军体科，射击训练及活动划归市少儿业余体校管理。</p>
<p><strong>二、无线电报务、工程、测向</strong></p>
<p>1958年，市成立无线电俱乐部，举办训练班，受训550人。1959年，新海连市运动员龚弱男参加第一届全运会，获女子无线电机抄全能第六名。“文化大革命”期间活动中断。</p>
<p>1979年，市人武部、市体委、市教育局等单位举办连云港市无线电工程训练班，受训100人。1979年国家体委举办无线电测向培训班，连云港市教练员张群代表江苏省参加学习，回来后举办训练班，无线电测向活动展开。1983年，江苏省无线电报务选拔赛在丹徒举行。连云港市运动员获成年男子通报第一名，成年男子发报第一名、成年男子个人全能第二名。至1990年，连云港市共承办1次全国、3次江苏省无线电测向比赛。市无线电测向运动员在全国、全省比赛中共获得金牌20块，女队2次获省团体第一名，共向省输送优秀运动员4人，其中张新霞在1987年的第六届全运会上获女子80米波段的冠军，两次入选国家集训队。</p>
<p><strong>三、航海</strong></p>
<p>1958年，新海连市开展航海运动，成立了市航海运动俱乐部，在墟沟海头湾建8间平房作办公用，共投资4万元，自建航海舢板2只，购买6只。有专职教练员2人，举办航海训练班，符合航海训练大纲要求，视觉通讯50人，海军武器30人，水上多项200人。1959年，举办4期业余训练班，受训107人，举办1次航海多项竞赛，有4个学校8个队80人参赛。1960年，组织8806人参加航海多项活动（其中2000人参加划船活动），连云区组织900名渔民参加航海活动。</p>
<p>“文化大革命”期间该活动中断。</p>
<p>1983年，航海运动划归市少儿业余体校管理。1986年，江苏省第十一届运动会赛艇、皮划艇比赛在南京举行。连云港市贾秀珍获女子组2000米赛艇赛第二名，成绩10'5"5；穆道波获男子组2000米赛艇赛第四名，成绩10'10"；刘大海获男子组皮划艇赛第六名，成绩3'14"7。</p>
<p><strong>四、航空模型、航海模型</strong></p>
<p>1958年，新海连市开展航空模型、航海模型活动，成立了市航空模型俱乐部，市航海模型俱乐部，共有专职教练员3人（其中航空模型教练员2人），分别举办骨干培训班，市区规模较大的中、小学和海州师范、市“少年之家”都成立了航空模型小组，利用课外活动和课余时间开展活动。1959年，举办两期航空模型训练班，学员40人，凡参加学习的都能制造二级牵引；举办两次航空模型比赛，比赛项目：弹射模型滑翔机，一级、二级牵引模型滑翔机，有60人参赛。市航空模型代表队参加1959年江苏省航空模型锦标赛，朱云龙获橡筋模型飞机（F1B）第二名，刘永磊获模型滑翔机（F1A）第三名。同年，市航空模型队在市体育场举行航空模型表演，项目：弹射模型滑翔机，一级、二级牵引模型滑翔机，国际级牵引模型滑翔机，国际级橡筋模型飞机，国际级自由飞模型飞机，初级无线电遥控模型飞机，观众达万人次。市航海模型俱乐部也举办了训练班和竞赛活动。</p>
<p>“文化大革命”期间活动中断至1990年。</p>
<p><strong>五、摩托车</strong></p>
<p>1977年，连云港市开展摩托车业余训练，有12名学员（男8、女4），通过训练、考核，全部达到国家规定的普通摩托车手合格标准，并颁发了证书。1979年，开始培训特等摩托车手，并同时组建摩托车运动队，同年，参加在连云港市举行的江苏省摩托车选拔赛，获团体第四名，叶建群获男子个人第三名。至1980年，训练摩托车手62人（男39、女23），其中特等摩托车手11人（男8、女3）。1981年该项目撤销。</p>"""

EXPECTED_TEXT = [
    "<p><strong>一、射击</strong></p>",
    "<p><strong>二、无线电报务、工程、测向</strong></p>",
    "江苏省无线电报务选拔赛",
    "共向省输送优秀运动员4人，其中张新霞在1987年的第六届全运会上获女子80米波段的冠军，两次入选国家集训队",
    "<p><strong>三、航海</strong></p>",
    "自建航海舢板2只",
    "成绩10'10\"",
    "<p><strong>四、航空模型、航海模型</strong></p>",
    "一级、二级牵引模型滑翔机",
    "<p><strong>五、摩托车</strong></p>",
]
RESIDUALS = [
    "一、射击1958年",
    "二、无线电报务、工程、测向1958年",
    "选拨赛",
    "共向省输送入选国家集训队",
    "三、航海1958年",
    "航海板2只",
    "成绩10°10",
    "四、航空模型、航海模型1958年",
    "项目：弹射模型滑翔机，级、二级牵引模型滑翔机",
    "五、摩托车1977年",
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
        raise RuntimeError(f"sports military expected text missing: {missing}")
    remaining = [item for item in RESIDUALS if item in segment]
    if remaining:
        raise RuntimeError(f"sports military residue remains: {remaining}")
    return changed, {"rewrote_scope": changed}


def write_reports(changed: int, counts: dict[str, int]) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "第五十六卷体育 / 第三章运动项目 / 第三节军体类",
        "source": SOURCE_NOTE,
        "reader_path": str(HTML),
        "changes_this_run": changed,
        "counts": counts,
        "principle": "依据 PaddleOCR 页级文本重建军体类整节，修复小标题粘连、漏句和明确错识。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    md = f"""# 第五十六卷军体类回源修复

- 时间：{now}
- 范围：`第五十六卷体育 / 第三章运动项目 / 第三节军体类`
- 源文依据：`{SOURCE_NOTE}`

## 修复动作

- 按页级 OCR 重建 `第三节军体类` 整节，拆分 `一、射击`、`二、无线电报务、工程、测向`、`三、航海`、`四、航空模型、航海模型`、`五、摩托车` 小标题。
- 补回无线电段尾 `优秀运动员4人`、`张新霞在1987年的第六届全运会上获女子80米波段的冠军，两次入选国家集训队`。
- 修正 `选拔赛`、`航海舢板2只`、`成绩10'10"`、`一级、二级牵引模型滑翔机` 等明确错识。
- 首次运行已完成 1 处整段替换；稳定复跑新增整段替换：{changed} 处。
- 本轮未处理 `第四节其它类`。

## 核对说明

- PaddleOCR `page_0238.txt` 确认第三节开头和射击段。
- PaddleOCR `page_0239.txt` 确认无线电、航海、航空模型段。
- PaddleOCR `page_0240.txt` 确认摩托车尾段和第四节边界。
"""
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")


def update_memory(changed: int) -> None:
    marker = "## 2026-07-03 第五十六卷军体类回源修复"
    memory = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker in memory:
        return
    entry = f"""
{marker}

- 对第五十六卷体育第三章运动项目 `第三节军体类` 进行回源修复。
- 源文依据：`{SOURCE_NOTE}`；重建整节，拆分 `一、射击`、`二、无线电报务、工程、测向`、`三、航海`、`四、航空模型、航海模型`、`五、摩托车` 小标题。
- 补回无线电段尾 `优秀运动员4人`、`张新霞在1987年的第六届全运会上获女子80米波段的冠军，两次入选国家集训队`；修正 `选拔赛`、`航海舢板2只`、`成绩10'10"`、`一级、二级牵引模型滑翔机` 等明确错识。
- 首次运行已完成 1 处整段替换；稳定复跑新增整段替换 {changed} 处；`第四节其它类` 未在本脚本中处理。
- 报告：`output/reports/reader_readability_sports_military_section_20260703.md`。
"""
    MEMORY.write_text(memory.rstrip() + "\n\n" + entry.lstrip(), encoding="utf-8")


def main() -> None:
    changed, counts = patch_reader()
    write_reports(changed, counts)
    update_memory(changed)
    print("sports military section repaired")
    print(f"changes={changed}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()
