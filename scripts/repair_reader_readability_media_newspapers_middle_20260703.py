# -*- coding: utf-8 -*-
"""Restore the middle part of the comprehensive newspapers section from page OCR."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_media_newspapers_middle_20260703.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_media_newspapers_middle_20260703.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260703_第五十四卷综合报纸中段回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SOURCE_NOTE = "workbench/ocr/paddle_ocr/下/part02/page_0129.txt:33-38; page_0130.txt; page_0131.txt:3-34"
SCOPE_START = '<p>八、灌云日报</p>'
SCOPE_END = '<p>十六、工商日报民国37年（1948年）初创刊，铅印。对开四版。东海县商会主办、商会会长李岳青任社长，主编张云家，采编人员有杨庆谊、张琪、陈亚甫等。除报道国内外新闻外，均刊登地方商业信息、广告。自印，发行量千余份。仅办3个月即停刊。</p>'

NEW_HTML = """<p>八、灌云日报</p>
<p>民国27年（1938年）创刊，四开四版，初为油印，后改为铅印。灌云青年救亡工作团主办，胡灏任社长兼主编。社址设在板浦大南门外合兴堆栈，后因日军飞机轰炸，迁至善后河南岸葛庄。</p>
<p>编采人员有许家屯、吴建、沙衡、周特夫、冯化农、孙存华、洪斌、戴茂斋等人。设国际新闻、国内新闻、地方新闻、副刊等版面。副刊上经常刊登抗日救亡歌曲，成为当地学校教材。发行量近千份。</p>
<p>民国28年（1939年）2月初，日军从灌河口登陆，报社人员转移至灌云南乡，雇一民船将印刷机器、铅字转移至小李集，途中被日本汽船击沉，机器、铅字皆坠入河中，遂停刊。</p>
<p>民国35年（1946年）12月，国民党灌云县党部主办《灌云日报》，登记证字号为“京警苏字第80号”。主编不详。油印，八开二版，一版为新闻，二版为文艺副刊。发行人王友生，编采人员有孙玉辉、席德生等。民国37年停刊。</p>
<p>九、大众三日刊</p>
<p>民国27年（1938年）创刊，东海县青年抗日救国团主办。油印，八开单页。编采人员有周晓江、郇华民、李铁民、周镜涵、周朝、马楠、刘锡九、徐用斋、王子成等。社址设在东海牛山郇圩小学，由郇华民家为办报人员提供吃住及办报经费。</p>
<p>《大众三日刊》刊登地方抗日新闻及有关抗日的评论文章，转载收音机里的讯息，以及其它报刊上的有关抗日文章。民国28年停刊。</p>
<p>十、海州日报</p>
<p>原为青岛《大新民报·东海版》，民国28年（1939年）7月1日创刊。伪国民党东海县政府主办。日报，铅印，四开四版，社址设在新浦德康巷（今民主路新华书店西巷内南首）。社长初为杨泽生，民国29年为姚湛汪，编采人员有许寅生、洪斌等。郝鹏举任伪淮海省省长时，报纸改名为《海州日报》，并由郝题写报头。第一版国内外新闻，第二版地方新闻，第三版商业信息，第四版文艺副刊、广告。日发行量2000余份。报社有印刷厂。该报是日军占领海属地区时唯一公开发行的报纸，民国34年8月日军投降后停刊。</p>
<p>十一、云台日报</p>
<p>民国34年（1945年）9月1日创刊，国民党中央陆军新编第六路军军长兼第一师师长徐继泰主办。《云台日报》接收日伪时期的《海州日报》财产，社址设在新浦德康巷。对开四版，铅印。主编朱冰华，发行人周振勃。日发行量数百份。采编人员有许晓虹（许慰祖）、陈拙、杜云海等。民国35年春因亏本停刊。</p>
<p>十二、大中报</p>
<p>民国34年（1945年）9月创刊，日报，对开四版。初为油印，民国35年改铅印。国民党第十战区苏北挺进军海灌军区司令部主办，发行人朱祥符，经理许拯寰，总编胡饰磐，社址三次搬迁，最后设在新浦中正路8号。报纸登记证号为“京警苏字第95号”。第一版每天大都有时事评论，余皆广告；第二、三版国内外新闻和地方新闻；第四版副刊和广告；中缝刊登广告。报头由国民党整编五十七师师长段霖茂题写。工作人员有朱冰华、吴挺枝、陈拙、赵筱川、刘树东、韩刚、王剑虹、姚静宜、毕律明等近30人。报社印刷厂有工人10多人，一台四开机、一台圆盘机。有一部电台，由刘克广负责接收电讯，为海属地区最早应用电台的报社。民国36年物价飞涨，办报经费入不敷出，不能按时发薪，工作人员生活拮据。</p>
<p>印刷厂年轻工人因吃不上饭而罢工，被许拯寰责罚跪在报社院中。民国36年底停刊。</p>
<p>十三、今日新闻</p>
<p>民国35年（1946年）6月1日创刊，日报，油印，四开二版。王馥桂（王实秋）主办，并担任发行人。社址设在灌云县板浦顾家巷盐业公司。国民党江苏省党部登记证“京警苏字第84号”。编采人员有洪斌、周玉书、邬厚机等。第一版国内外新闻、广告；第二版地方新闻和文艺副刊。发行于灌云县境内及新浦、盐区等地，发行量1000多份。民国37年秋停刊。</p>
<p>十四、和平日报</p>
<p>民国35年（1946年）秋创刊，铅印，对开四版。国民党驻军师长段霖茂主办。社长李梯清，经理陈云善，社址设在新浦中正路。编辑有徐漫、王宝善，记者有陈吉桂、吴挺枝、陈亚甫、王养元等。第一版国内外新闻，第二、三版为社会新闻，第四版为副刊、广告。报社有7个印刷工人，借用新华印刷局的机器印报。《和平日报》出刊两月余发行千余份。国民党部队整编四十四师调防新浦，师长王泽浚将报名换为《建国日报》。民国36年6月，因四十四师调防而停刊。</p>
<p>十五、海报</p>
<p>原为《苏报·海州版》，民国35年（1946年）1月创刊，国民党东海县党部机关报。日报，铅印，四开二版。社长孙肖韩，主编胡饰磐、朱冰华，经理吴稚南。报纸登记证为“中宣部登记证中字第491号”。民国37年7月7日奉国民党江苏省党部指示更名为《海报》，登记证字号为“京警苏字第226号”。社址原在新浦中正路1号，后搬至新浦中正路通灌路口。报头每日套红。第一版国内外新闻电讯稿和该报的社论及广告，第二版地方社会新闻、商业信息、副刊、广告。报社有印刷厂。发行量3000余份，编采人员有顾东石、戴诵仁、姚焕愚、孙建国、吕一鸣、陈亚甫、张琪、汪中文、张河、陈振家、吕善之、丁宝和、韩宇言、谢远东、汪鸿奎、倪儿彦等。</p>
<p>民国36年（1947年）夏成立董事会，董事长武葆岑，董事有孙肖韩、颜振流、李歧嵩、倪爱棠、夏为善、吴稚南等。</p>
<p>《海报》为海属地区日军投降后至解放前一张颇有影响的报纸。民国35年（1946年）中共地下党员顾东石利用《海报》记者身份，搜集国民党部队、政府重要情报，并发展中共地下党员。民国37年7月，顾东石被国民党整编四十四师逮捕，11月被杀害。</p>
"""

EXPECTED_TEXT = [
    "八、灌云日报</p>",
    "九、大众三日刊</p>",
    "郇华民",
    "十、海州日报</p>",
    "改名为《海州日报》",
    "十二、大中报</p>",
    "工作人员生活拮据",
    "十三、今日新闻</p>",
    "民国35年（1946年）6月1日创刊",
    "十四、和平日报</p>",
    "记者有陈吉桂、吴挺枝",
    "《和平日报》出刊两月余",
    "十五、海报</p>",
    "报社有印刷厂",
    "顾东石被国民党整编四十四师逮捕",
]
RESIDUALS = [
    "八、灌云日报民国27年",
    "九、大众三日刊民国27年",
    "郁华民",
    "郁圩小学",
    "十、海州日报原为",
    "《大新民报·东海版)",
    "改名为（海州日报》",
    "十一、云台日报民国34年",
    "十二、大中报民国34年",
    "生活括据",
    "十三、今日新闻民国35年（1946年6月1日",
    "十四、和平日报民国35年",
    "昊挺枝",
    "（和平日报》",
    "十五、海报原为",
    "印刷广",
    "整编四十四师速捕",
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
        "scope": "第五十四卷报刊广播电视 / 第一章报纸 / 第一节综合报纸（八至十五）",
        "source": SOURCE_NOTE,
        "reader_path": str(HTML),
        "changes_this_run": changed,
        "counts": counts,
        "principle": "依据 PaddleOCR 页级文本重建综合报纸八至十五条，停止在十六、工商日报前。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    md = f"""# 第五十四卷综合报纸中段回源修复

- 时间：{now}
- 范围：`第五十四卷报刊广播电视 / 第一章报纸 / 第一节综合报纸（八至十五）`
- 源文依据：`{SOURCE_NOTE}`

## 修复动作

- 按页级 OCR 重建 `八、灌云日报` 至 `十五、海报`，停止在 `十六、工商日报` 前。
- 拆开八个条目题名与正文粘连。
- 修正 `郇华民/郇圩小学`、`《大新民报·东海版》`、`《海州日报》`、`拮据`、`民国35年（1946年）6月1日`、`吴挺枝`、`《和平日报》`、`印刷厂`、`逮捕` 等源页明确内容。
- 当前核验复跑整段替换：{changed} 处。

## 核对说明

- 本次只处理第一节中段，`十六、工商日报` 及以后仍需后续单独回源核对。
"""
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")


def update_memory(changed: int) -> None:
    marker = "## 2026-07-03 第五十四卷综合报纸中段回源修复"
    memory = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker in memory:
        return
    entry = f"""
{marker}

- 对第五十四卷报刊广播电视 `第一章报纸 / 第一节综合报纸` 中段进行回源修复。
- 源文依据：`{SOURCE_NOTE}`；重建 `八、灌云日报` 至 `十五、海报`，停止在 `十六、工商日报` 前。
- 修正条目题名粘连、`郇华民/郇圩小学`、`《大新民报·东海版》`、`《海州日报》`、`拮据`、`今日新闻` 创刊日期括号、`吴挺枝`、`《和平日报》`、`印刷厂`、`逮捕` 等问题。
- 当前核验复跑整段替换 {changed} 处。
- 报告：`output/reports/reader_readability_media_newspapers_middle_20260703.md`。
"""
    MEMORY.write_text(memory.rstrip() + "\n\n" + entry.lstrip(), encoding="utf-8")


def main() -> None:
    changed, counts = patch_reader()
    write_reports(changed, counts)
    update_memory(changed)
    print(json.dumps({"changed": changed, "counts": counts}, ensure_ascii=False))


if __name__ == "__main__":
    main()
