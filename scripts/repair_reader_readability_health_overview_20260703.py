# -*- coding: utf-8 -*-
"""Restore Fifth十五卷 health overview from page OCR."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_health_overview_20260703.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_health_overview_20260703.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260703_第五十五卷卫生概述回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SOURCE_NOTE = "workbench/ocr/paddle_ocr/下/part02/page_0164.txt:8-28; page_0165.txt:3-34"
SCOPE_START = '<h3 id="第五十五卷-概述">概述</h3>'
SCOPE_END = '<h3 id="第五十五卷-第一章公共卫生">第一章公共卫生</h3>'

NEW_HTML = """<h3 id="第五十五卷-概述">概述</h3>
<p>市境内中医治病源远流长，相传灌云县伊芦山为商朝大臣伊尹隐居地，在此著《汤液本草》。宋元明清至民国期间境内出现数十位名医，著有《颐生秘旨》、《内经辑要》等医学名著。光绪三十四年（1908年），美国传教士慕庚扬受美国南方长老会派遣来海州开办义德医院，境内始有西医。</p>
<p>清末至民国期间，战乱频仍，劳动人民长期处于被剥削被奴役的地位，饥寒交迫，哀鸿遍野，霍乱、天花、伤寒、麻疹、黑热病、丝虫病等传染病在市境内经常流行。民国20年（1931年）市内霍乱流行40多天，死亡人数无法计算，构成了“牛郎欲问瘟神事，一样悲欢逐逝波”的悲惨画面。</p>
<p>对于疾病预防和公共卫生管理，民国地方政府是排不上议事日程的。民国18年（1929年）东海县中医公会成立。地方政府通过中医公会管理医务。民国23年，刘一麟留学德国获医学博士学位后，在新浦开设益龄医院，是当时海属地区医术最强颇具影响的私人医院。民国25年，东海县立医院在海州成立，为全县吸毒者戒烟和防治传染病。民国27年，市内开设中医诊所55家，西医诊所和医院共22家。民国地方政府对卫生工作未设立专门管理机构，各项卫生事业无显著政绩。</p>
<p>日伪统治期间，海州建立伪华北防疫委员会海州诊疗所，在连云、新浦各建一所同仁会医院。民国30年（1941年）12月，伪东海县政府将义德医院接管，改为东海县立医院。</p>
<p>伪东海县警察局设卫生股，管理饮食、理发、浴池、妓院、清道夫等行业的清洁卫生工作，市内居民开始使用自来水。日伪统治期间的卫生措施，是为日本帝国主义者预防治疗疾病工作服务的，广大贫苦人民仍然是多灾多难。</p>
<p>民国34年（1945年），抗日战争胜利后，新浦同仁会医院由江苏省第八区行政督察专员公署接收，改称海属新浦公立医院。连云同仁会医院由连云市政府接收，改称连云市立医院。东海县立医院恢复为义德医院。地方政府未设立卫生管理机构。民国35年，东海县警察局对新浦、海州摊贩进行卫生管理，在新浦定时定点管理垃圾、粪便。当时社会环境卫生管理极差。民国37年11月，市内有个体中医诊所37家、个体西医诊所131家，及1所教会医院和17家联合诊所性质的小型医院，从业人员390人，病床151张。</p>
<p>民国37年（1948年）11月，新海连特区专署设卫生局，由山东滨海医院和滨海卫生队调来50余人接管海属新浦公立医院，改为新海连特区医院，接管连云市医院，并且建立新海连特区卫生学校；动员私立诊所开诊；接受淮海前线转来的伤病员医疗康复工作；派医务人员参加舟山群岛战役中的医务工作；对私立医院和诊所调查、登记；对患有传染病的贫苦市民免费治疗。解放初期，地方卫生部门为支援解放战争，整顿地方医疗机构和为劳苦大众解除疾病痛苦等方面成绩卓著，增强了党和人民政府在人民中的威望。</p>
<p>1951年，市卫生科成立。此后，各区卫生所、妇幼保健站、交通检疫所、市工人医院、市卫生防疫站相继成立。接办海州义德医院，改为新海连市立医院。将个体开业医生组成中医联合诊所、西医联合诊所、中西医联合诊所、妇婴联合诊所。为反对美帝国主义发动的细菌战，在全市范围内开展以除“四害”、讲卫生、灭疾病为内容的爱国卫生运动，全市环境卫生大为改观；开展预防接种，传染病得到控制，人民健康水平普遍提高。</p>
<p>1961年，国民经济困难时，市卫生局组织中西医对营养不良性浮肿病、小儿营养性不良病、妇女病进行防治，对副霍乱防治采取果断措施。扩建或新建连云港市卫生检疫所、市药品检验所、市结核病防治院、市麻风病防治所、市公费医疗门诊部等医疗机构。组织农村卫生工作队分赴市境内和周边县开展防治疾病、计划生育、基层卫生人员培训、改善环境卫生等工作，受到农民欢迎。“文化大革命”期间，卫生组织机构和制度遭到破坏。</p>
<p>1969年底，中国人民解放军毛泽东思想宣传队进驻卫生行政部门，成立革命委员会，卫生组织、制度恢复，市郊105个农（渔）生产大队建立合作医疗制度。</p>
<p>中国共产党十一届三中全会以后，全市医疗卫生工作跨入新的历史时期，建立市中医院、市精神病防治院、市妇幼保健院，各综合医院医疗技术装备逐步齐全，医疗质量大为提高。继续开展爱国卫生运动，创建国家卫生城市。在劳动保护、食品监督、饮用水水质卫生监测、垃圾、粪便处理方面都形成管理制度，并不断完善。对传染病、寄生虫病、地方病的防治成绩显著，消灭了天花、霍乱、黑热病、血丝虫病，计划免疫工作得到落实。医政、药政管理机构健全、措施得力。妇女、儿童和干部保健工作得到重视。医学教育不断发展，医学科研成果中的有些项目获得省部级以上的奖励，全市医疗卫生事业得到长足的发展，方兴未艾。</p>
"""

EXPECTED_TEXT = [
    "民国20年（1931年）市内霍乱流行40多天",
    "一样悲欢逐逝波",
    "江苏省第八区行政督察专员公署接收",
    "接受淮海前线转来的伤病员医疗康复工作",
    "中国共产党十一届三中全会以后",
]
RESIDUALS = [
    "民国20年逐逝波",
    "行政督察专概述",
    "接受准海前线",
    "十一届兰中全会",
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
    return changed, {"rewrote_scope": changed, "overview_paragraphs_restored": 11}


def append_once(path: Path, marker: str, content: str) -> None:
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker not in old:
        path.write_text(old.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")


def write_reports(changed: int, counts: dict[str, int]) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "第五十五卷卫生 / 概述",
        "source": SOURCE_NOTE,
        "reader_path": str(HTML),
        "changes_this_run": changed,
        "counts": counts,
        "principle": "依据 PaddleOCR 页级文本重建卫生卷概述，停止在第一章公共卫生前。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    REPORT_MD.write_text(
        "\n".join([
            "# 第五十五卷卫生概述回源修复",
            "",
            f"- 时间：{now}",
            f"- 范围：{payload['scope']}",
            f"- 源文：`{SOURCE_NOTE}`",
            f"- 阅读器：`{HTML}`",
            f"- 本次是否改写：{changed}",
            "- 修复：补回民国20年霍乱流行完整句，移除页眉误入，修正淮海前线、十一届三中全会等错字。",
            "",
        ]),
        encoding="utf-8",
    )
    PROGRESS.write_text(
        f"""# 第五十五卷卫生概述回源修复

- 时间：{now}
- 源文依据：`{SOURCE_NOTE}`。
- 修复范围：`第五十五卷卫生 / 概述` 至 `第一章公共卫生` 前。
- 修复内容：补回 `民国20年（1931年）市内霍乱流行40多天...一样悲欢逐逝波` 完整句；清除页眉 `概述·2449` 误入；修正 `行政督察专员公署` 断裂、`淮海前线`、`十一届三中全会` 等。
- 报告：`output/reports/reader_readability_health_overview_20260703.md`。
""".strip() + "\n",
        encoding="utf-8",
    )
    memory = f"""
## 2026-07-03 第五十五卷卫生概述回源修复

- 对第五十五卷卫生 `概述` 进行回源修复。
- 源文依据：`{SOURCE_NOTE}`；重建至 `第一章公共卫生` 前。
- 修正 `民国20年逐逝波` 漏句、页眉 `概述·2449` 误入、`行政督察专员公署` 断裂、`准海前线`、`十一届兰中全会` 等问题。
- 当前核验复跑整段替换 {changed} 处。
- 报告：`output/reports/reader_readability_health_overview_20260703.md`。
"""
    append_once(MEMORY, "## 2026-07-03 第五十五卷卫生概述回源修复", memory)


def main() -> None:
    changed, counts = patch_reader()
    write_reports(changed, counts)
    print(json.dumps({"changed": changed, "counts": counts, "source": SOURCE_NOTE}, ensure_ascii=False))


if __name__ == "__main__":
    main()
