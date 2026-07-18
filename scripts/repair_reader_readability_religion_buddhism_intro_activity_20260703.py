# -*- coding: utf-8 -*-
"""Restore religion Buddhism intro and first section from page OCR."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_religion_buddhism_intro_activity_20260703.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_religion_buddhism_intro_activity_20260703.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260703_第五十七卷佛教传布与活动回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SOURCE_NOTE = (
    "workbench/ocr/paddle_ocr/下/part02/page_0258.txt:17-34; "
    "workbench/ocr/paddle_ocr/下/part02/page_0259.txt:3-41; "
    "workbench/ocr/paddle_ocr/下/part02/page_0260.txt:3-18"
)
SCOPE_START = '<h3 id="第五十七卷-第一章佛教">第一章佛教</h3>'
SCOPE_END = '<h4 id="第五十七卷-第一章佛教-第二节著名佛教建筑物">第二节著名佛教建筑物</h4>'

NEW_HTML = """<p>自东汉佛教传入境内，即建有寺庙，僧人修持传教，且与海内外交往。唐宋时期士大夫喜谈禅学，百姓仿效，崇信释老，企求福祉，官府不断兴建庙宇。明清两代对云台山三元宫屡次重修，在云台山一带形成佛教建筑群体。</p>
<p>解放前，海州城内佛教寺庙20余处，素有“九庵十八庙”之称。乡村集镇，多建有寺庙。抗日战争前，东海县境内有中小型寺院近200处，至解放时尚存59座庙宇共385间，有僧尼150人。赣榆县有寺庙35座，僧尼137人。云台区有寺院101座，绝大多数为佛教寺院。灌云县大伊山有寺庙35座。以上佛教寺院不少毁于战火。</p>
<p>解放后，境内庙宇因年久失修，僧尼大多还俗，宗教活动停止。80年代以后，落实宗教政策，修复庙宇。僧尼入寺住持，恢复正常的佛教活动。</p>
<p>1979年，赣榆县有和尚8人，尼姑13人。80年代以后，市区修整复原龙洞庵、百子庵、观音庵、碧霞宫、三元宫、阿育王塔等佛教建筑。1990年，市区有僧尼22人。东海县王沟大殿尚存3间，和尚5人，居士1人。</p>
<h4 id="第五十七卷-第一章佛教-第一节传布与活动">第一节传布与活动</h4>
<p><strong>一、传布</strong></p>
<p>东汉时佛教已从西域传入境内，宿城法起寺为汉代所建，孔望山摩崖石刻为汉代佛教造像。法起寺僧人与古康居国僧人有交往，寺内鹫峰石塔、罗汉墓即是埋葬灭度于此的康居国高僧的墓塔。三国魏齐王正始元年（240年）前后，康居国高僧康僧会经宿城时曾题额纪念。</p>
<p>魏晋南北朝时，佛教在境内为统治阶级所提倡。隋唐时，释学在士大夫阶层广为传播，百姓也普遍信奉。隋末唐初，法起寺已成为境内及周边地区研究、传播大乘教义的主要寺庙之一，并选派学问僧到内地学习深造。宝逻法师在唐初被派到成都多宝塔寺向道因法师学教，学成归来，在法起寺弘扬光大大乘教义。唐贞观十七年（643年），新罗国高僧慈藏法师经鹰游门回国。唐开成四年（839年）三月二十九日，日本入唐求法僧圆仁途经宿城，在朝阳兴国寺寻求佛法。唐神龙元年（705年），在孔望山建龙兴寺。境内佛教奉行大乘佛教禅宗一派，唐末开始信奉曹洞宗，宋代确立曹洞宗正宗体系。传至二十七世为嵩乳，二十八世为佛光、灵焰，二十九世为省闻，三十世为义云，三十一世为淇源，三十二世为心慧。心慧高僧“大启禅宗、远迩稽首，皈依者弥众”，法起寺成为“不二法门，十万丛林，有德者居之”。传到三十五世，为镇海寺的润梅、雪公和尚。</p>
<p>宋天圣元年（1023年），阿育王塔在大村建造。宋时，淮安的有藏禅师在南城活动，安抚使张汉英在城内为其建造普照寺。</p>
<p>明洪武十五年（1382年），海州、赣榆设僧正司、僧会司管理教务。成化元年（1465年），鲁王孙到云台山青峰顶出家修行，自号清风。在三元宫清风传净善，净善传道融，道融传德连，四代衣钵传袭，香火益旺。万历十五年（1587年），淮安谢淳扩建三元宫，随之出家，自号无相，更号德证，以与德连为同师。扩建三元宫庙群期间，皇帝颁降经敕谕，由钦差大臣专程护送到云台山。随赐《大藏经》一部678函，佛像3轴，紫衣1袭，锦幡3联，经幅1方，银宝1锭。至此，云台山三元宫香火逾2万家，佛教在境内传播达到鼎盛期。</p>
<p>（三元宫尚存《大藏经》刻本34函78种317册，计1343卷。）涟水人杨珊，字碧溪，在宿城山顶建悟道庵。明崇祯二年（1629年），嵩乳和尚在保驾山下法起寺再振宗风。</p>
<p>清顺治十八年（1661年）裁海，庙废，僧众迁居他乡，佛教顿衰。康熙十六年（1677年）复海，佛教活动恢复，康熙三十一年，玄烨亲书“遥镇洪流”匾额赐三元宫，康熙三十八年，太监五哥上山进香，云台山一带佛教为之中兴。康熙五十二年起，法起寺大规模修建，到雍正十三年（1735年），形成24进规模的寺院。乾隆二十七年（1762年），普爱（字天庚）在连岛建镇海寺，殿宇、廊院百余间，并将坐落在孙家山庙岭上的祗园寺（古观音堂）修为下院。佛教在此再度兴起，直到民国初期。</p>
<p>清末民国初，僧尼群集云台山寺院，悟五、厚庵相继住持三元宫，上下几百人，分24个房头分居各寺院。民国初年，犯有命案的振亚和尚住持法起寺，增广僧众，扩充庙产，修桥补路，重建寺院。同时，振亚和尚勾结官府，组建武装，欺压百姓，兼并土地。民国20年（1931年），振亚被捕，庙产被抄，大部分庙产被没收，僧众逃散。民国27年5～6月，日军飞机连续轰炸法起寺，只留下残垣断壁。民国28年7月14日开始，日军数次围剿三元宫，纵火焚烧庙宇，僧人组织反击，护庙法师仁芳被杀，仁益等4名法师被活埋，雁朋、襄言等法师侥幸逃脱。民国28年8月13日，日军制造“南城惨案”，屠杀无辜百姓，南城西山顶上碧霞宫王和尚愤书千字文章，悲壮自焚，与正殿同归于尽。民国28年至民国37年，云台山僧尼生活无着，星散山间，勉强维持香火。</p>
<p>建国后，宗教活动得到初步恢复，但规模不大。“文化大革命”期间，宗教活动被取缔。80年代开始落实宗教政策，修复寺院。各修复寺院有僧尼住持。1981年3月，连云港市僧人代表参加江苏省佛教协会第一次代表大会。1990年底，全市有僧尼22人。</p>
<p><strong>二、法事活动</strong></p>
<p>佛门弟子每日做早课、晚课、坐禅。农历四月初八日佛诞节各地有庙会，尤以海州白虎山庙会为盛。农历腊月初八日成道节，寺院僧尼煮腊八粥，以香、花、烛、果供佛。农历二月十五日，寺院举行涅槃法会，诵《遗教经》，祭吊释迦牟尼。每年十一月“打佛七”，每个“佛七”诵经7天，共“三七”21天。</p>
<p>僧尼受请为死者“超度亡魂”，在安葬死者前举行，僧人若干名身着袈裟，演奏乐器，念经“超度鬼魂脱离苦难”，名之曰“放焰口”。</p>
<p>农历七月十五日为佛教盂兰盆会，是佛教徒追荐祖先的节日，佛徒施斋供僧，搭经坛，和尚举办水陆道场，放焰口，念经超度孤魂。解放初期，增加祝愿世界和平，为正义战争死难烈士祈祷等内容。</p>
<p>解放前，苏北江淮一带的香客来云台山进香者络绎不绝，市境内参加烧香会民间组织，朝山进香的人也为数不少，尤以每年农历正月十五日前后的迎神赛会活动期间为盛。</p>
<p>解放后，这一活动逐渐停止。50年代后，僧尼仅在寺庙内接收香火和捐赠。</p>"""

EXPECTED_TEXT = [
    "企求福祉",
    "<p><strong>一、传布</strong></p>",
    "传入境内，宿城法起寺",
    "康居国高僧的墓塔。三国魏齐王正始元年",
    "传至二十七世为嵩乳",
    "随赐《大藏经》一部678函",
    "祗园寺（古观音堂）",
    "侥幸逃脱",
    "修复寺院。各修复寺院有僧尼住持",
    "<p><strong>二、法事活动</strong></p>",
    "涅槃法会",
    "身着袈裟",
    "盂兰盆会",
]
RESIDUALS = [
    "福证",
    "一、传布东汉时",
    "传人境内",
    "康额纪念",
    "土大夫",
    "隋未唐初",
    "传至二十七世为乳",
    "省闻.三十世",
    "随赐《大藏经》-部",
    "上的园寺（古观音堂）",
    "饶幸逃脱",
    "愤书于字文章",
    "修复院。",
    "二、法事活动佛门弟子",
    "涅躲法会",
    "裂裟",
    "名之白“放焰口”",
    "孟兰盆会",
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
        raise RuntimeError(f"religion buddhism expected text missing: {missing}")
    remaining = [item for item in RESIDUALS if item in segment]
    if remaining:
        raise RuntimeError(f"religion buddhism residue remains: {remaining}")
    return changed, {"rewrote_scope": changed}


def write_reports(changed: int, counts: dict[str, int]) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "第五十七卷宗教 / 第一章佛教 / 章序与第一节传布与活动",
        "source": SOURCE_NOTE,
        "reader_path": str(HTML),
        "changes_this_run": changed,
        "counts": counts,
        "principle": "依据 PaddleOCR 页级文本重建佛教章序和第一节，修复明确错识和小标题粘连。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    md = f"""# 第五十七卷佛教传布与活动回源修复

- 时间：{now}
- 范围：`第五十七卷宗教 / 第一章佛教 / 章序与第一节传布与活动`
- 源文依据：`{SOURCE_NOTE}`

## 修复动作

- 按页级 OCR 重建佛教章序和 `第一节传布与活动`，停止在 `第二节著名佛教建筑物` 前。
- 拆分 `一、传布`、`二、法事活动` 小标题。
- 修正 `福祉`、`传入境内`、`康居国高僧的墓塔`、`嵩乳`、`《大藏经》一部`、`祗园寺`、`侥幸逃脱`、`涅槃法会`、`袈裟`、`盂兰盆会` 等明确错识。
- 首次运行已完成 1 处整段替换；稳定复跑新增整段替换：{changed} 处。

## 核对说明

- PaddleOCR `page_0258.txt` 确认佛教章序和第一节开头。
- PaddleOCR `page_0259.txt` 确认传布段主体。
- PaddleOCR `page_0260.txt` 确认法事活动和第二节边界。
"""
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")


def update_memory(changed: int) -> None:
    marker = "## 2026-07-03 第五十七卷佛教传布与活动回源修复"
    memory = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker in memory:
        return
    entry = f"""
{marker}

- 对第五十七卷宗教 `第一章佛教 / 章序与第一节传布与活动` 进行回源修复。
- 源文依据：`{SOURCE_NOTE}`；重建至 `第二节著名佛教建筑物` 前，未触碰建筑物条目。
- 拆分 `一、传布`、`二、法事活动` 小标题；修正 `福祉`、`传入境内`、`康居国高僧的墓塔`、`嵩乳`、`《大藏经》一部`、`祗园寺`、`侥幸逃脱`、`涅槃法会`、`袈裟`、`盂兰盆会` 等明确错识。
- 首次运行已完成 1 处整段替换；稳定复跑新增整段替换 {changed} 处。
- 报告：`output/reports/reader_readability_religion_buddhism_intro_activity_20260703.md`。
"""
    MEMORY.write_text(memory.rstrip() + "\n\n" + entry.lstrip(), encoding="utf-8")


def main() -> None:
    changed, counts = patch_reader()
    write_reports(changed, counts)
    update_memory(changed)
    print("religion buddhism intro/activity repaired")
    print(f"changes={changed}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()
