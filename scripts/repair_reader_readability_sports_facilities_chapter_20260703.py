# -*- coding: utf-8 -*-
"""Restore sports facilities chapter from page OCR."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_sports_facilities_chapter_20260703.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_sports_facilities_chapter_20260703.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260703_第五十六卷体育设施回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SOURCE_NOTE = (
    "workbench/ocr/paddle_ocr/下/part02/page_0251.txt:4-35; "
    "workbench/ocr/paddle_ocr/下/part02/page_0252.txt:3-36; "
    "workbench/ocr/paddle_ocr/下/part02/page_0253.txt:3-19"
)
SCOPE_START = '<h3 id="第五十六卷-第六章体育设施">第六章体育设施</h3>'
SCOPE_END = '<!-- VERIFIED-STRUCTURED-TABLES-START -->'

NEW_HTML = """<p>民国3年至民国25年（1914～1936年）期间，海属地区曾陆续建设了一批体育场馆，开展田径、球类、体操等活动。民国28年后，多数体育设施被日本侵略军毁坏。抗日战争胜利后，因经费窘迫，场地无力修复。建国后，对旧场地进行更新、改建，并逐步新建了一大批体育设施，为群众体育活动广泛开展和训练竞赛创造了条件。</p>
<h4 id="第五十六卷-第六章体育设施-第一节市区公共体育场所">第一节市区公共体育场所</h4>
<p>民国24年（1935年），驻海州税警团成立“励志社”，建立篮球场、足球场、游泳池等体育设施。民国25年，上海东亚体专毕业生杨构在海州参府衙门旧址建立体育场，内有篮球场、足球场及单双杠等。新浦南广场是群众活动场所。民国34年场上有一副足球门，场南面有简单体育器械，平时无专人管理，每逢县或学校开运动会，画跑道和赛区。</p>
<p>青年体育馆又名草棚球场，该场地原是一片洼坑，20世纪50年代初，是由团市委、市总工会动员全市青年义务劳动垫起来的。1953年先建成简易球场，1957年市投资2.8万元建成青年体育馆。1960年将草顶换成石棉瓦顶，屋面1650平方米，竹质结构，四周墙是柴笆，石灰粉墙，泥土球场。坐落在市解放路中段，面积2000平方米，可容观众2000人，场内除可作为篮球、排球、乒乓球、羽毛球等项活动外，还可作市里集会场所。后废弃不用。</p>
<p>1956年建市人民体育场。市人民体育场东西长302米，南北宽161米，面积48622平方米，省投资2.5万元。建有田径场一个，有8条400米煤渣跑道，内设足球场，还有投掷、跳高、跳远等区，可供各种田径项目的训练和比赛，还可进行足球比赛。1958年9月又投资4000元，建成场内主席台，现在主席台改至北面，建成600平方米的主席台楼，楼上可供市体委办公用。</p>
<p>1965年建市体育馆。市体育馆位于新浦中心地段，在市人民体育场西侧，1966年10月建成。建筑面积1377平方米，使用面积1208平方米，房屋跨度32.04米，房屋结构是混凝土砖结构，石棉瓦屋面，看台是使用钢筋混凝土预制板。可容观众2449人，看台下房屋建筑面积480平方米。比赛场地高8米、长32米、宽18米，可进行篮球、排球、羽毛球活动。1972年场地更新为拼木地板，又装千瓦白炽灯、电子记分牌，体育馆内顶和墙壁加隔音板1479平方米，该馆总投资30万元。</p>
<p>1972年建练习馆。练习馆又名排球房，在市人民体育场东南侧，面积792平方米，长36米，宽22米，檐高7米，可供篮球、排球、乒乓球、摔跤教学训练用，总造价8万元。</p>
<p>1980年建旱冰场。旱冰场又名滑轮场，位于人民体育场北面，建筑面积1461平方米，实用面积1300平方米，可容500人活动，投资4.5万元。已废弃。</p>
<p>1981年建市游泳池。市游泳池范围22575平方米，建筑面积1410平方米，钢筋混凝土池身，水面积50米×25米，水深1.3～1.8米，容积1887立方米。每年7～10月开放，可容纳200人活动。有更衣室、办公室、浴室、厕所等，共投资14万元。</p>
<p>1982年兴建市海滨浴场。1959年建的简易浴场，文化大革命中遭毁坏。海滨浴场位于连云区墟沟镇海棠大队一个自然海湾，浴场三面倚山，一面朝海，水面积443米×422米，水深1～8米，有两道防鲨设施。并建有办公室、休息室2000平方米，更衣室1000平方米，淋浴室400平方米，还有救生器材、服务部和停车场，每年夏秋季开放。该场由市属单位集资建成。1984年省拨款10万元作海滨浴场基建维修费。</p>
<p>1986年连云区在墟沟镇建灯光球场，有观众席位2500个。</p>
<h4 id="第五十六卷-第六章体育设施-第二节县公共体育场所">第二节县公共体育场所</h4>
<p><strong>一、赣榆县</strong></p>
<p>民国20年（1931年），赣榆县在县城南门外开辟县公共体育场。</p>
<p>1981年建灯光球场。该场位于青口镇，水泥地面。1989年在球场西面、南面建水泥看台，有观众席位780个。以后县内各乡镇又辟建水泥篮球场5处。</p>
<p>1983年建人民体育场。该场有8条跑道，县政府拨款5万元，建在赣榆中学小花园旧址，建成后与赣榆中学共用。</p>
<p>1984年建溜冰场。该场位于青口镇，可容200多人活动。1986年青口镇水上公园又辟建一处圆形水泥溜冰场。宋庄、罗阳、墩尚等乡也兴建溜冰娱乐场。</p>
<p>1987年建室内游泳池。该池坐落于县城青口镇，建筑面积525平方米，屋架跨度15米，室内高度4.5米，专作训练用。池身钢筋混凝土结构，池长25米，宽11米，池身1.2米至1.6米，有灯光设备，投资25万元。</p>
<p><strong>二、东海县</strong></p>
<p>1966年建室内训练房。在东海县中操场南侧，面积522平方米，又名乒乓球房。</p>
<p>1968年，县工会在院内建一灯光球场，还有可容纳数百人的看台。1978年10月，在青湖镇建灯光球场，面积114平方米，可容观众1500人。</p>
<p>1985年11月建人民体育场。人民体育场位于县城西，征地112亩，投资110万元。1986年3月建成8条煤渣铺垫的跑道，有标枪、铁饼、铅球、跳高等比赛场地8块，3个跳远沙坑。1986年6月建成主席台、会议室、接待室。1988年7月，建成可容纳3000人的田径场看台，建筑面积1100平方米，看台下面有15间平房，可供乒乓球运动员训练活动和放置体育器材。1989年建成4块门球场，2块沥清篮球场，共占地5500平方米。</p>
<p>1989年建射击场。该场在县体育场北面，有10个靶位，5间室内汽手枪训练房。</p>
<p><strong>三、灌云县</strong></p>
<p>民国18年（1929年），在县城板浦建立县公共体育场。</p>
<p>1974年，在县城伊山镇建看台灯光球场。该场建在县体育场内，有1100个观众座位。</p>
<p>1978年又建室外篮球场，面积420平方米。1986年县投资30万元在各乡镇共建灯光球场18个。</p>
<p>1975年建田径场。该场在县城伊山镇，土跑道。1984年又投资7.5万元，建成有400米跑道的标准田径场。1985年又投资10万元建成综合利用的主席台，两侧楼房作县体委办公用。</p>
<p>1975年建乒乓球房。该房坐落伊山镇县体育场内，建筑面积246平方米。</p>
<p>1988年建室内游泳池。该池在县城伊山镇，建筑面积615平方米，屋架跨度15米，室内场地高度7.4米，池身钢筋混凝土结构，池长25米、宽12米、池深1.3至1.8米，有灯光设备，投资32万元，1988年6月建成。</p>
<h4 id="第五十六卷-第六章体育设施-第三节学校体育场地">第三节学校体育场地</h4>
<p>民国16年（1927年），江苏省第八师范学校迁海州，学校建一简易操场。民国5年，崇真中学开始建篮球、排球场及单杠、双杠、跳马等体育设施。民国17年，新浦普爱小学竖起新浦第一副篮球架。民国32年，东海县初级中学开办，民国33年迁址新浦西外，建一个简易运动场，有篮球、排球、足球及其他体育器械。</p>
<p>建国后，各学校都新建了体育场地。这些场馆的修建，为连云港市群众性体育活动的开展和专业成绩的提高起到了很大的促进作用。</p>"""

EXPECTED_TEXT = [
    "后废弃不用。",
    "柴笆，石灰粉墙",
    "摔跤教学训练用",
    "海滨浴场位于连云区墟沟镇海棠大队一个自然海湾",
    "<p><strong>一、赣榆县</strong></p>",
    "<p><strong>二、东海县</strong></p>",
    "<p><strong>三、灌云县</strong></p>",
    "池身钢筋混凝土结构，池长25米、宽12米",
]
RESIDUALS = [
    "后废弃不1956年",
    "柴芭",
    "摔教学训练用",
    "海滨浴场位米",
    "一、赣榆县民国20年",
    "二、东海县1966年",
    "三、灌云县民国18年",
    "池长钢筋混凝土结构，池长25米",
    "1953~1990年部分年份连云港市体育经费一览表",
    "表56-8",
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
        raise RuntimeError(f"sports facilities expected text missing: {missing}")
    remaining = [item for item in RESIDUALS if item in segment]
    if remaining:
        raise RuntimeError(f"sports facilities residue remains: {remaining}")
    return changed, {"rewrote_scope": changed}


def write_reports(changed: int, counts: dict[str, int]) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "第五十六卷体育 / 第六章体育设施",
        "source": SOURCE_NOTE,
        "reader_path": str(HTML),
        "changes_this_run": changed,
        "counts": counts,
        "principle": "依据 PaddleOCR 页级文本重建第六章正文，修复漏字、明确错识和小标题粘连。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    md = f"""# 第五十六卷体育设施回源修复

- 时间：{now}
- 范围：`第五十六卷体育 / 第六章体育设施`
- 源文依据：`{SOURCE_NOTE}`

## 修复动作

- 按页级 OCR 重建 `第六章体育设施` 正文，停止在体育卷已核结构化表格区前。
- 修正 `后废弃不用`、`柴笆`、`摔跤教学训练用`、`海滨浴场位于连云区墟沟镇海棠大队一个自然海湾` 等明确错漏。
- 拆分 `一、赣榆县`、`二、东海县`、`三、灌云县` 小标题。
- 撤出正文范围内可能混入的 `表56-8` 残片；结构化表区未在本轮修改。
- 首次运行已完成 1 处整段替换；稳定复跑新增整段替换：{changed} 处。

## 核对说明

- PaddleOCR `page_0251.txt` 确认第六章导语和第一节前段。
- PaddleOCR `page_0252.txt` 确认第一节尾段与第二节主体。
- PaddleOCR `page_0253.txt` 确认第二节尾段、第三节和表56-8边界。
"""
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")


def update_memory(changed: int) -> None:
    marker = "## 2026-07-03 第五十六卷体育设施回源修复"
    memory = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker in memory:
        return
    entry = f"""
{marker}

- 对第五十六卷体育 `第六章体育设施` 进行回源修复。
- 源文依据：`{SOURCE_NOTE}`；重建至体育卷已核结构化表格区前，未修改结构化表数据。
- 修正 `后废弃不用`、`柴笆`、`摔跤教学训练用`、`海滨浴场位于连云区墟沟镇海棠大队一个自然海湾` 等明确错漏。
- 拆分 `一、赣榆县`、`二、东海县`、`三、灌云县` 小标题；`表56-8` 仍由结构化表流程管理。
- 首次运行已完成 1 处整段替换；稳定复跑新增整段替换 {changed} 处。
- 报告：`output/reports/reader_readability_sports_facilities_chapter_20260703.md`。
"""
    MEMORY.write_text(memory.rstrip() + "\n\n" + entry.lstrip(), encoding="utf-8")


def main() -> None:
    changed, counts = patch_reader()
    write_reports(changed, counts)
    update_memory(changed)
    print("sports facilities chapter repaired")
    print(f"changes={changed}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()
