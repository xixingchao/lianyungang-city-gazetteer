# -*- coding: utf-8 -*-
"""Restore front subsections of women's healthcare from OCR."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_health_women_care_front_20260702.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_health_women_care_front_20260702.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260702_第五十五卷妇女保健前两小节回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SOURCE_NOTE = (
    "workbench/body_chapters/连云港市志_全书_正文汇总.md:101327-101387; "
    "workbench/body_chapters/第五十二卷至第六十卷及附录（下part02）.md:8023-8081; "
    "workbench/ocr/paddle_ocr/下/part02/page_0201.txt:12-35; "
    "workbench/ocr/paddle_ocr/下/part02/page_0202.txt:3-38; "
    "workbench/ocr/paddle_ocr/下/part02/page_0203.txt:3-4"
)
SCOPE_START = '<h4 id="第五十五卷-第五章保健疗养-第一节妇女保健">第一节妇女保健</h4>'
SCOPE_END_OPTIONS = ("<p>三、妇女“四期”保护", "<p><strong>三、妇女“四期”保护</strong></p>")

NEW_HTML = """<p><strong>一、接生</strong></p>
<p>民国以前，市境内均为旧法接生，在产妇家接生，使用的剪刀、褥单等均不消毒，常见产褥热及新生儿破伤风。民国3年（1914年），海州义德医院妇科新法接生，新法接生大大降低产褥热、破伤风的发病率。由于旧的传统思想影响和经济情况，接受新法接生的为少数妇女。解放后，新海连特区专员公署成立妇婴保健委员会，推广新法接生。1950年3月，市政府公立医院在云台区举办新法接生员培训班，培训对象为粗通文字、个人卫生情况较好、有一定接生经验、在群众中有威信的接生婆，共28人，时间1个月。</p>
<p>5月，新海县卫生院设妇幼保健室，配备3名专职干部负责旧产婆的培训改造和新法接生的宣传和推广，并实行贫苦产妇免费接生制度。1952年，全市共新法接生1747人，新法接生率21.6%。1953年，市内各区妇幼保健站陆续建立，组织辅导接生人员的业务学习和技术操作，制订工作制度。市卫生科在云台、海州、龙尾、盐河和连云5个区开展新法接生补助费评定工作，共评定397人享受补助，共发补助费411.5元。1954年，全市已有经培训的旧接生婆和新培训的新法接生员102人，共组成6个接生站和44个接生组。全年新法接生率64.7%。1957年，全市新法接生技术人员350人，组成35个接生站和36个接生组。接生员中已掌握产前检查技术的147人，占总数的44.01%。全年共新法接生7235人次，新法接生率88.9%，产前检查达12925人次。1958年，全市复训接生员81人。除原有的接生站（组）外，全市还开办农村人民公社产院15处，共设产床55张。农村产妇进产院分娩，享受免费待遇，发营养补助费2元，当年全市新法接生率91%。1960~1970年，新法接生的优越性已普遍被群众所接受，全市新法接生率逐年提高，旧法接生在市内已很少见到。</p>
<p>1972年，对全市接生员进行整顿，停止部分年老体弱者的工作，从乡村女赤脚医生中培养接生员，恢复和建立规章制度。1976年，开始提出把好产前检查关、消毒接生关、产后访视关和做到接生与妇女病查治相结合、接生与计划生育相结合的工作方针，在各村卫生室中建立妇产室，市妇幼保健所对全市的女赤脚医生接生员进行接生技术复训，全市开始使用统一印发的出生证。1979年，全市新法接生率达99%。1980年后，随着人民生活水平的提高和科学知识的普及，孕产妇要求住院分娩的人数逐年增多。1981年，各医院接收产妇5412人，住院分娩率67.3%。1982年，开始推行科学接生，要求接生人员在助产时，除做好技术操作，还必须做好对整个产程的观察，对处理过程作详细记录。1990年，全市住院分娩率73.9%，产妇死亡率4.6/万，新生儿破伤风发病率0.19%o。</p>
<p><strong>二、妇女病普查普治</strong></p>
<p>建国前，市内未见有妇女病普查普治的情况资料。1952年，市卫生科组织医务人员对陇东火柴厂的女工进行首次疾病普查，查有28名女工患有各类妇女病，即采取措施进行治疗。1953年，该厂建立女工卫生室。1956年，市妇幼保健所在陇东火柴厂和新海印刷厂进行妇女滴虫性阴道炎的查治。两厂共检查344名女工，查出滴虫性阴道炎患者39人，患病率11.7%。经治疗，当年痊愈29人。1959年开始，市卫生部门将妇女病普查普治列为每年常规工作之一，查治对象以工厂女工和农村妇女为主。1960年，市妇幼保健所和市妇女联合会组建子宫脱垂病防治组，先在朝阳公社新县大队试点，然后扩大到全市。普查结束后，将子宫脱垂病人分期分批集中到墟沟治疗。至1961年，共治疗1495名患者中的1331人，治愈889人，治愈率66.79%。对子宫脱垂病查治持续到1966年。1966年，妇女病查治工作中断，至1970年逐渐恢复。</p>
<p>1973年，将防癌作为妇女病查治工作重点。市妇幼保健所组成由17名医生、助产士、检验员的查治小分队，先在新浦区75个单位试点调查，举办查治人员学习班，培训查治人员121人，组成15个妇女病普查普治小分队，共检查10868名妇女，占全市应查妇女总数的13.7%。共查出患者5966人，总患病率54.9%。其中以宫颈炎患者最多，为4242例，占患病人数的71.1%；滴虫性和霉菌性阴道炎患者次之，为816例，占患病总人数的13.68%；宫颈癌病人6名，占0.1%。普查期间，全市共设17个妇女病治疗点，为1250名宫颈炎和阴道炎病人治疗，治愈448人,好转801人。</p>
<p>1977年4月，市妇女病普查普治领导小组成立，各区、公社和较大的厂矿、企事业单位均成立普查领导小组。5月，普查工作在全市展开，1978年8月结束。检查已婚妇女28894人，查出各种妇女病患者14736人，其中慢性宫颈糜烂8643人，滴虫性霉菌性阴道炎1701人。还查出宫颈癌22例，尿瘘1例，均进行手术治疗。1978年3月，市妇幼保健所对市区70处公共浴室调查，发现女浴室的91%为通池，没有淋浴设施。凡用通池洗澡的女工，其滴虫性（或霉菌性）阴道炎的发病率均较高。如市绝缘材料厂的女工发病率为23.7%；凡使用淋浴的女工该病发病率均较低，如市罐头厂的女工发病率为1.6%。就此问题向有关方面提出改进意见。1979年后，市区妇女病查治每年进行一次。1985年，举办一期阴道细胞检验学习班，有7个基层妇幼保健单位11人参加。1986年，市区妇女病发病率为37.6%，较1985年降低10.9%。1990年，妇女病发病率较1984年下降1.5%。</p>"""

EXPECTED_TEXT = [
    "<p><strong>一、接生</strong></p>",
    "全市住院分娩率73.9%",
    "新生儿破伤风发病率0.19%o。",
    "<p><strong>二、妇女病普查普治</strong></p>",
    "新海印刷厂进行妇女滴虫性阴道炎的查治。两厂共检查344名女工",
    "查治对象以工厂女工和农村妇女为主",
    "集中到墟沟治疗。至1961年，共治疗1495名患者中的1331人",
    "占患病总人数的13.68%；宫颈癌病人6名，占0.1%",
]
RESIDUALS = [
    "一、接生民国以前",
    "住院分娩率.73.9%",
    "发病率0.19%0二、妇女病普查普治",
    "新海印刷广",
    "两广共检查",
    "工广女工",
    "集中到沟治疗",
    "共治疗1495名：",
    "占患病总人数的宫颈炎",
]


def find_scope(text: str) -> tuple[int, int]:
    start = text.index(SCOPE_START) + len(SCOPE_START)
    ends = [text.find(marker, start) for marker in SCOPE_END_OPTIONS]
    valid_ends = [end for end in ends if end != -1]
    if not valid_ends:
        raise RuntimeError("women care front scope end not found")
    return start, min(valid_ends)


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
        raise RuntimeError(f"women care front expected text missing: {missing}")
    remaining = [item for item in RESIDUALS if item in segment]
    if remaining:
        raise RuntimeError(f"women care front residue remains: {remaining}")
    return changed, {"rewrote_scope": changed}


def write_reports(changed: int, counts: dict[str, int]) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "第五十五卷卫生 / 第五章保健疗养 / 第一节妇女保健 / 一、接生；二、妇女病普查普治",
        "source": SOURCE_NOTE,
        "reader_path": str(HTML),
        "changes_this_run": changed,
        "counts": counts,
        "principle": "依据 PaddleOCR 页级文本整体复原妇女保健前两小节；未处理三、妇女四期保护。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    md = f"""# 第五十五卷妇女保健前两小节回源修复

- 时间：{now}
- 范围：`第五十五卷卫生 / 第五章保健疗养 / 第一节妇女保健 / 一、接生；二、妇女病普查普治`
- 源文依据：`{SOURCE_NOTE}`

## 修复动作

- 拆分 `一、接生`、`二、妇女病普查普治` 两个小节标题。
- 修正 `住院分娩率73.9%`、`新生儿破伤风发病率0.19%o`。
- 修正 `新海印刷厂`、`两厂`、`工厂女工`、`墟沟治疗`、`1495名患者` 等 OCR 错误。
- 复原 `占患病总人数的13.68%；宫颈癌病人6名，占0.1%` 统计句。
- 本次复跑新增整段替换：{changed} 处。
- 本轮未处理 `三、妇女“四期”保护`。

## 核对说明

- PaddleOCR `page_0201.txt` 确认 `第一节妇女保健`、`一、接生` 起始。
- PaddleOCR `page_0202.txt` 确认 `接生` 跨页尾段、`二、妇女病普查普治` 和主体文字。
- PaddleOCR `page_0203.txt` 确认下一小节 `三、妇女“四期”保护` 边界。
"""
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")


def update_memory(changed: int) -> None:
    marker = "## 2026-07-02 第五十五卷妇女保健前两小节回源修复"
    memory = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker in memory:
        return
    entry = f"""
{marker}

- 对第五十五卷卫生第五章第一节 `妇女保健` 的 `一、接生`、`二、妇女病普查普治` 进行回源修复。
- 源文依据：`{SOURCE_NOTE}`；拆分两个小节标题，并按 OCR 复原跨页断句和统计句。
- 本轮新增整段替换 {changed} 处；`三、妇女“四期”保护` 未在本脚本中处理。
- 报告：`output/reports/reader_readability_health_women_care_front_20260702.md`。
"""
    MEMORY.write_text(memory.rstrip() + "\n\n" + entry.lstrip(), encoding="utf-8")


def main() -> None:
    changed, counts = patch_reader()
    write_reports(changed, counts)
    update_memory(changed)
    print("women care front section repaired")
    print(f"changes={changed}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()
