# -*- coding: utf-8 -*-
"""Restore Fifth十五卷公共卫生第二节劳动卫生 from page OCR."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_health_labor_hygiene_20260703.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_health_labor_hygiene_20260703.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260703_第五十五卷公共卫生劳动卫生回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SOURCE_NOTE = "workbench/ocr/paddle_ocr/下/part02/page_0167.txt:20-37; page_0168.txt:3-39; page_0169.txt:3-6"
SCOPE_START = '<h4 id="第五十五卷-第一章公共卫生-第二节劳动卫生">第二节劳动卫生</h4>'
SCOPE_END = '<h4 id="第五十五卷-第一章公共卫生-第三节食品卫生">第三节食品卫生</h4>'

NEW_HTML = """<h4 id="第五十五卷-第一章公共卫生-第二节劳动卫生">第二节劳动卫生</h4>
<p><strong>一、粉尘监测与矽肺病防治</strong></p>
<p>1956年，新海连市卫生防疫部门对陇东火柴厂、新海电厂、新海印刷厂、新海植物油厂等产生粉尘工厂进行浓度测定，均超过标准，最高的超标31倍，最低的超标2倍，对此提出采取降尘措施的建议。1957年，对市内10家厂矿进行粉尘测定，平均超标25.5倍，最高的超标114倍，最低的超标2倍。1958年，经市卫生防疫站测定，采用土法上马的工矿企业粉尘浓度又有上升，由于防尘得不到有效控制，矽肺病不断发展。1964年，组建连云港市职业病诊断小组，对矽肺病治疗与防治进行研究讨论，定期对厂矿企业与粉尘接触的工人进行体格检查。1972年，连云港市卫生防疫站、化学工业部化工矿山设计研究院、锦屏磷矿共同研究，将锦屏磷矿生产时的泥土爆破改为水封爆破，使粉尘浓度降低60.9%。1976年，在市内20家工矿企业开展防尘达标工作，效果显著。1986年，对全市78家工厂生产性粉尘进行测定，粉尘浓度最高的每立方米2526毫克，最低的每立方米0.3毫克，平均粉尘浓度每立方米130毫克，超标率达80.5%。1990年，全市接触粉尘的工人19437人，其中矽肺病人364人；一期病人310人，占85.16%；二期病人41人，占11.26%；三期病人13人，占3.58%。在364名矽肺病人中已死亡53名，死亡率为14.56%。对矽肺病患者都调换工作，生活上予以照顾，采取各种方法治疗。</p>
<p><strong>二、职业中毒监督和防治</strong></p>
<p>建国前，市内职业中毒时有发生，谈不上防治。1950～1960年，全市21家厂矿有30个有毒作业场所，工人2000人。有毒物有各种农药、磷化合物、氯化合物、氟化合物、碘化合物、铅、苯、汞、铬等。市防疫站从1958年开始对各厂矿接毒作业工人进行健康检查。</p>
<p>1963年，对锦屏化工厂磷作业工人检查中，发现有49.2%接磷者的下颌骨有病理性致病。</p>
<p>1967年，市锦屏化工厂有23人次发生急性磷化氢中毒。1969年，市农药厂有22名工人发生急性五硫化二磷中毒。1974年在市塑料厂152名接触三盐基铅的作业工人中发现有47人有轻度铅中毒症状。1984年，市水产养殖公司25人患急性磷化氢中毒。1986年，市卫生防疫站对全市产生铅、汞、铬及有机磷等有毒物质的厂矿生产过程进行调查。全市有18家工厂28个铅作业点，各个铅作业点的铅烟最高浓度为每立方米2.4毫克，最低为0.001毫克，平均浓度为每立方米0.86毫克，超标27.6倍；铅尘最高浓度每立方米6.3毫克，最低浓度为0.01毫克，超标率为67.8%，对接触铅烟、铅尘486名工人的健康检查中发现有19人尿铅增高，诊断为铅吸收。全市有46家工厂85个苯作业点，苯的最高浓度为每立方米1361毫克，最低浓度为3.1毫克，平均浓度为每立方米324.9毫克，超标7.1倍，超标率66%。对64个工厂933名苯作业工人进行体检，共查出慢性苯中毒12人，观察对象18人。普查中查出全市接汞作业工人45人中有3人为汞吸收。1989年5月4日，市食品厂11名工人患溴甲烷中毒。以上中毒病例都进行治疗，有的调换了工种。</p>
<p><strong>三、物理因素职业危害防治</strong></p>
<p>1957年6月，对全市10个工矿企业单位的15处高温作业点进行辐射热测定，发现辐射热最高为1.76卡/平方厘米/分钟，超过国家1.0卡/平方厘米/分钟卫生标准。1962年，对全市1078名高温作业工人进行健康检查，将其中38人调离高温作业场所。1975年，开始对噪声危害进行监测和预防，市卫生防疫站、锦屏磷矿职工医院、徐州医学院协作，对锦屏磷矿井下噪声进行测定，测得噪声值为108～110分贝（A）；对81名井下作业工人的听力测试，发现有80%的作业工人有不同程度的听力减退现象。1983年，对13家工厂563个噪声产生点的作业工人进行健康检查，发现有耳鸣的占49.6%，耳痛的占2.8%，神经衰弱的占5.5%，语言和高频听力减退的分别占68.3%和92.1%。1986年，对全市101家工厂的613个噪声作业点测试，其中352个作业点的噪声超过国家卫生标准，超标率为57.10%。噪声强度最高者118分贝（A），最低者67分贝（A）。对超标的噪声，各行业采取措施控制。如纺织行业采用无梭织机代替有梭织机，市电线厂在噪声较大的车间采用超细玻璃棉吸收噪声，使噪声由93分贝下降到89.5分贝（A）。</p>
<p><strong>四、农药中毒防治</strong></p>
<p>1952年起，在爱国卫生运动中，用敌敌涕、“六六六”农药杀虫，由于加强防护，未发现中毒现象。1960年以后，氯化乐果、“1605”、“3911”、“甲基605”等农药投入使用。1980年以后，又有辛硫磷、“苏化203”、“呋喃丹”等投入使用。因品种多、毒性强、使用者的安全用药知识差等原因，经常发生中毒事故。市人民政府及其所辖县（区）人民政府均成立农药中毒防治领导小组，由各级政府主要负责人任组长，公安、供销、农业、卫生等部门负责人为小组成员，协调开展农药中毒防治工作。县（区）、乡医院成立农药中毒抢救小组，配备抢救器械和药品。卫生部门对农村使用和保管农药的人员进行专题培训，利用宣传媒介进行农药使用知识的普及教育。1982年，全市共发生生产性农药中毒929人，1985年降至345人，1989年降至60人。1990年按国家卫生部颁布的《农村农药中毒卫生管理办法》，对农药中毒卫生进行防治和管理。1990年，全市农药生产性中毒406人。</p>
"""

EXPECTED_TEXT = [
    "1956年，新海连市卫生防疫部门对陇东火柴厂",
    "工矿企业粉尘浓度又有上升",
    "市塑料厂152名接触三盐基铅",
    "1957年6月，对全市10个工矿企业单位的15处高温作业点进行辐射热测定",
    "锦屏磷矿井下噪声进行测定",
    "1983年，对13家工厂563个噪声产生点的作业工人进行健康检查",
    "各行业采取措施控制",
]
RESIDUALS = [
    "一、粉尘监测与矽肺病防治厂等",
    "粉尘浓度文有上升",
    "二、职业中毒监督和防治建国前",
    "市塑料广152",
    "三、物理因素职业危害防治射热",
    "锦屏磷矿并下",
    "13家工神经衰弱",
    "四、农药中毒防治1952年",
]


def find_scope(text: str) -> tuple[int, int]:
    start = text.index(SCOPE_START)
    end = text.index(SCOPE_END, start)
    return start, end


def patch_reader() -> tuple[int, dict[str, int]]:
    text = HTML.read_text(encoding="utf-8")
    start, end = find_scope(text)
    changed = int(text[start:end] != NEW_HTML)
    if changed:
        HTML.write_text(text[:start] + NEW_HTML + text[end:], encoding="utf-8")

    text = HTML.read_text(encoding="utf-8")
    start, end = find_scope(text)
    segment = text[start:end]
    missing = [item for item in EXPECTED_TEXT if item not in segment]
    if missing:
        raise RuntimeError(f"expected text missing: {missing}")
    remaining = [item for item in RESIDUALS if item in segment]
    if remaining:
        raise RuntimeError(f"residue remains: {remaining}")
    return changed, {"rewrote_scope": changed, "subheads_restored": 4, "paragraphs_restored": 7}


def append_once(path: Path, marker: str, content: str) -> None:
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker not in old:
        path.write_text(old.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")


def write_reports(changed: int, counts: dict[str, int]) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "第五十五卷卫生 / 第一章公共卫生 / 第二节劳动卫生",
        "source": SOURCE_NOTE,
        "reader_path": str(HTML),
        "changes_this_run": changed,
        "counts": counts,
        "principle": "依据 PaddleOCR 页级文本重建劳动卫生节，停止在第三节食品卫生前。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    REPORT_MD.write_text(
        "\n".join([
            "# 第五十五卷公共卫生劳动卫生回源修复",
            "",
            f"- 时间：{now}",
            f"- 范围：{payload['scope']}",
            f"- 源文：`{SOURCE_NOTE}`",
            f"- 阅读器：`{HTML}`",
            f"- 本次是否改写：{changed}",
            "- 修复：恢复四个小标题，补回粉尘监测和物理因素段首漏文，修正 `文有上升`、`塑料广`、`并下噪声`、`13家工神经衰弱` 等 OCR 残留。",
            "",
        ]),
        encoding="utf-8",
    )
    PROGRESS.write_text(
        f"""# 第五十五卷公共卫生劳动卫生回源修复

- 时间：{now}
- 源文依据：`{SOURCE_NOTE}`。
- 修复范围：`第五十五卷卫生 / 第一章公共卫生 / 第二节劳动卫生` 至 `第三节食品卫生` 前。
- 修复内容：恢复 `一、粉尘监测与矽肺病防治`、`二、职业中毒监督和防治`、`三、物理因素职业危害防治`、`四、农药中毒防治` 小标题；补回段首漏文；修正 `粉尘浓度文有上升`、`市塑料广152`、`锦屏磷矿并下`、`13家工神经衰弱` 等残留。
- 报告：`output/reports/reader_readability_health_labor_hygiene_20260703.md`。
""".strip() + "\n",
        encoding="utf-8",
    )
    memory = f"""
## 2026-07-03 第五十五卷公共卫生劳动卫生回源修复

- 对第五十五卷卫生 `第一章公共卫生 / 第二节劳动卫生` 进行回源修复。
- 源文依据：`{SOURCE_NOTE}`；重建至 `第三节食品卫生` 前。
- 恢复四个小标题，补回粉尘监测和物理因素段首漏文，修正 `文有上升`、`塑料广`、`并下噪声`、`13家工神经衰弱` 等 OCR 残留。
- 当前核验复跑整段替换 {changed} 处。
- 报告：`output/reports/reader_readability_health_labor_hygiene_20260703.md`。
"""
    append_once(MEMORY, "## 2026-07-03 第五十五卷公共卫生劳动卫生回源修复", memory)


def main() -> None:
    changed, counts = patch_reader()
    write_reports(changed, counts)
    print(json.dumps({"changed": changed, "counts": counts, "source": SOURCE_NOTE}, ensure_ascii=False))


if __name__ == "__main__":
    main()
