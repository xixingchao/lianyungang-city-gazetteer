# -*- coding: utf-8 -*-
"""Restore the front part of the comprehensive newspapers section from page OCR."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_media_newspapers_front_20260703.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_media_newspapers_front_20260703.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260703_第五十四卷综合报纸前段回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SOURCE_NOTE = "workbench/ocr/paddle_ocr/下/part02/page_0127.txt:10-38; page_0128.txt; page_0129.txt:3-32"
SCOPE_START = '<h4 id="第五十四卷-第一章报纸-第一节综合报纸">第一节综合报纸</h4>'
SCOPE_END = '<p>八、灌云日报民国27年（1938年）创刊，四开四版，初为油印，后改为铅印。灌云青年救亡工作团主办，胡灏任社长兼主编。社址设在板浦大南门外合兴堆栈，后因日军飞机轰炸，迁至善后河南岸葛庄。</p>'

NEW_HTML = """<h4 id="第五十四卷-第一章报纸-第一节综合报纸">第一节综合报纸</h4>
<p>一、东海民报</p>
<p>国民党东海县党部机关报，民国18年（1929年）1月创刊。主笔陈嗣衡，编辑杨光鉴。社址设在新浦王巷。铅印，三日刊，四开四版，日发行量千余份。第一版以广告为主，右下方辟《冷箭》专栏。第二版为国内外时事新闻。第三版为地方社会新闻，报道民间生活琐事。第四版为东海县政府的公文批复、广告及《晨钟》副刊。</p>
<p>民国18年（1929年）7月26日，陈嗣衡撰文《虎髯蓝领搂着个粉白黛绿》发表在《冷箭》专栏上，揭露驻军独立第四旅旅长谭曙卿劣迹。谭以“宣传赤化”的罪名将陈嗣衡和东海县总工会常委张劲枢枪杀，《东海民报》停刊。江苏省和东海县的国民党党部为此成立“东海惨案后援会”赴京告状，并在南京召开“东海惨案新闻发布会”，《申报》、《新闻报》、《中央日报》都发了消息。“东海惨案”震惊全国。社会上称之为“海报事件”。</p>
<p>二、海州日报</p>
<p>国民党东海县党部主办，民国19年（1930年）创刊。主办人高秉杰。社址设在海州东大街。铅印，对开二版。版面除国内外新闻、地方新闻外，设有《海声》、《晚虹》（星期天专版）、《雄鸡》副刊及《教育》等专刊。东海县农民教育馆主编的《乡谈》，曾以《海州日报》名义单独发行。《海州日报》因被东海县党部夏铸禹（夏鼎文）控制，故称之为“夏派报纸”。民国21年停刊。</p>
<p>三、东海农报</p>
<p>民国19年（1930年）创刊，东海县农民教育馆主办。主编吴鲁星。社址设在海州刘顶村。半月刊，每期六至八版，石印，16开活页，售价为4个铜板。第一版为时事报道；第二版传播科学常识，破除封建迷信，宣传天文地理，介绍作物栽培知识等；第三版为文化娱乐，介绍中国武术，或刊登农教馆农校学员的日记、文艺作品；第四版为地理沿革；第五、六、七版为地方乡土知识；第八版为简明新闻和刊载地方传奇人物，如苗坦之、雷百万、吉果等。</p>
<p>《东海农报》刊头题字经常由农民教育馆农校学生书写。这些学生原是不识字的庄稼汉、石匠。民国22年停刊。</p>
<p>四、连云报</p>
<p>民国21年（1932年）创刊，日报，四开二版，振东印书馆印刷，发行量2000余份。社址设在新浦津海巷。</p>
<p>《连云报》原由中共地下党员李翘鸥发起创办。李翘鸥通过其东海十一中学的同学、国民党东海县党部监察委员武葆岑办了登记注册手续。武葆岑为谋取“执行委员”头衔，积极与李翘鸥合作办报以扩大自已在社会中影响，致使该报出刊后即成了国民党东海县党部的官办报纸。武葆岑利用官职，以报社名义募捐、拉广告，将所得钱财攫为己有。</p>
<p>《连云报》主编陈楚之，系国民党东海县党部夏铸禹所安插，陈楚之弟弟陈星明任该报记者。李翘鸥为副刊编辑。编采人员有王养元、周静生、戴诵仁、陈新明、李鹏年、姚焕玉、李玉东、武若愚、李尚农、李玉东等。</p>
<p>《连云报》的经理原是卞家其，后换李岳青（李歧嵩）。身兼新浦汽车公司经理的李岳青，每日清晨将《连云报》随车送往海、赣、沭、灌各地，当日下午又随车带回各地通讯员稿件。报纸新闻时效性较强，上述各地又能读到当天报纸，故深受读者欢迎，发行量猛增，广告业务增多，曾增扩为四开八版。</p>
<p>《连云报》节假日为对开四版，第一版为国内外新闻、广告；第二版登国内外新闻、地方新闻；第三版为地方新闻；第四版为各种专版及文艺副刊《艺舟》、《海市》和广告。文艺副刊曾发表李石华（李庆华）与曹禺合编的《戏剧周刊》、孙佳讯的《海国诗钞》、女诗人蔻红的《蔻红睡余》专栏，以及陈新明的新体诗《蔓陀罗》等。《连云报》靠一台收音机接收《中央日报》电讯稿。民国28年初停刊。</p>
<p>五、新海报</p>
<p>民国24年（1935年）1月25日创刊，日刊，铅印，四开二版，主编胡饰磐兼编辑部主任。登记证字号为“中宣会中字第2349号”、“内政部警字第4242号”。陈立夫题写报头。报社几移社址，先后设在新浦王巷、新闻巷、中正路（现解放路）等处。新华印刷局承印。</p>
<p>《新海报》为国民党东海县党部庞寿峰主办的官方报纸，社会上称为“庞派报纸”。日发行量千余份。一版为国内外重要新闻和地方消息，胡饰磐负责编发；二版为文艺副刊《战线》、《文苑》及广告。文艺副刊编辑有应若冰（应似红）、孙佳讯、孙存楼、姚湛汪（姚槐青）。记者有赵筱川、李尚农、吕延贵等。</p>
<p>民国27年（1938年）6月13日，《新海报》因发表文章揭露国民党江苏省第八行政督察专员兼第九游击战区司令郝国玺用轿车贩运烟土，被郝国玺派人查封，并逮捕胡饰磐。《苏报》、《徐报》、《淮报》随即发表文章声援《新海报》。郝国玺迫于舆论压力，释放胡饰磐，赔偿新海报社的经济损失，社会上称之为“新海报事件”。</p>
<p>民国27年（1938年）底，因日军轰炸，报纸一度停刊。停刊前一期，《新海报》与《连云报》出联合版。民国28年2月终刊。</p>
<p>民国36年（1947年）9月1日，《新海报》复刊，由三青团东海县总部主办。社址设在新浦中正路。因经济困难，改为油印，四开四版，仍为日报。编采人员有陈拙、赵筱川、王树云、徐传瑶、姚焕愚、杨守仁等。</p>
<p>复刊的《新海报》辟有《敌区回忆录》专栏，揭露日军占领时期的伪市长邵竞生、维持会会长韩淑援、大队长杨九洲等的丑行。社会反映强烈。</p>
<p>《新海报》于民国37年（1948年）11月停刊。</p>
<p>六、抗战报</p>
<p>民国26年（1937年）创刊，四开二版，日报。国民党五十七军一一二师（东北军）主办，社址设在海州西大岭。除编发电讯外，有地方新闻、市场物价及文艺副刊等。由于日军轰炸海州，《新海报》与《连云报》曾暂时停刊。《抗战报》填补了海属报纸中的空白。民国27年秋，《抗战报》停刊。</p>
<p>七、抗日导报</p>
<p>创刊于民国27年（1938年）秋（后改为《新赣报》）。油印，八开单页，不定期出版。国民党赣榆县政府政训处主办，县长朱爱周题写报头。内容以抗日为主，民国27年9月8日，出《纪念“九·一八”七周年》专刊，发表共产党人和爱国青年文章，论述抗战必胜的道理。《抗日导报》当时被誉为赣榆县国共两党携手抗日的一面旗帜。民国29年停刊。</p>
"""

EXPECTED_TEXT = [
    "一、东海民报</p>",
    "编辑杨光鉴",
    "7月26日，陈嗣衡撰文《虎髯蓝领搂着个粉白黛绿》",
    "《东海农报》刊头题字经常",
    "所得钱财攫为己有",
    "经理原是卞家其",
    "海、赣、沭、灌各地",
    "第一版为国内外新闻、广告",
    "民国27年（1938年）6月13日，《新海报》因发表文章",
    "社会上称之为“新海报事件”",
    "七、抗日导报</p>",
    "民国27年9月8日，出《纪念“九·一八”七周年》专刊",
]
RESIDUALS = [
    "一、东海民报国民党",
    "杨光签",
    "7.月26日",
    "楼着个粉白黛绿",
    "题学经常",
    "不识学的庄稼汉",
    "为已有",
    "卡家其",
    "海、赣、沐、灌",
    "第一一版",
    "登记证字号为中宣会",
    "报社儿移社址",
    "且发行量千余份",
    "逮捕胡饰磐。</p>",
    "七、抗日导报创刊于",
    "9月8理",
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
    return changed, {"rewrote_scope": changed}


def write_reports(changed: int, counts: dict[str, int]) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "第五十四卷报刊广播电视 / 第一章报纸 / 第一节综合报纸（一至七）",
        "source": SOURCE_NOTE,
        "reader_path": str(HTML),
        "changes_this_run": changed,
        "counts": counts,
        "principle": "依据 PaddleOCR 页级文本重建综合报纸前七条，停止在八、灌云日报前。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    md = f"""# 第五十四卷综合报纸前段回源修复

- 时间：{now}
- 范围：`第五十四卷报刊广播电视 / 第一章报纸 / 第一节综合报纸（一至七）`
- 源文依据：`{SOURCE_NOTE}`

## 修复动作

- 按页级 OCR 重建 `一、东海民报` 至 `七、抗日导报`，停止在 `八、灌云日报` 前。
- 拆开七个条目题名与正文粘连。
- 修正 `杨光鉴`、`7月26日`、`搂着个粉白黛绿`、`题字`、`不识字`、`攫为己有`、`卞家其`、`沭`、`第一版` 等源页明确内容。
- 补回 `新海报事件` 相关整段，修正并补全 `抗日导报` 中 `民国27年9月8日，出《纪念“九·一八”七周年》专刊`。
- 当前核验复跑整段替换：{changed} 处。

## 核对说明

- 本次只处理第一节前七条，`八、灌云日报` 及以后仍需后续单独回源核对。
"""
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")


def update_memory(changed: int) -> None:
    marker = "## 2026-07-03 第五十四卷综合报纸前段回源修复"
    memory = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker in memory:
        return
    entry = f"""
{marker}

- 对第五十四卷报刊广播电视 `第一章报纸 / 第一节综合报纸` 前段进行回源修复。
- 源文依据：`{SOURCE_NOTE}`；重建 `一、东海民报` 至 `七、抗日导报`，停止在 `八、灌云日报` 前。
- 修正条目题名粘连、`杨光鉴`、`7月26日`、`搂着个粉白黛绿`、`题字/不识字`、`攫为己有`、`卞家其`、`海、赣、沭、灌`、`第一版` 等问题，并补回 `新海报事件` 整段和 `抗日导报` 专刊句。
- 当前核验复跑整段替换 {changed} 处。
- 报告：`output/reports/reader_readability_media_newspapers_front_20260703.md`。
"""
    MEMORY.write_text(memory.rstrip() + "\n\n" + entry.lstrip(), encoding="utf-8")


def main() -> None:
    changed, counts = patch_reader()
    write_reports(changed, counts)
    update_memory(changed)
    print(json.dumps({"changed": changed, "counts": counts}, ensure_ascii=False))


if __name__ == "__main__":
    main()
