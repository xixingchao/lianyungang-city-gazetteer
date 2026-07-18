# -*- coding: utf-8 -*-
"""Restore sports other-events section from page OCR."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_sports_other_section_20260703.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_sports_other_section_20260703.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260703_第五十六卷其它类回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SOURCE_NOTE = (
    "workbench/ocr/paddle_ocr/下/part02/page_0240.txt:7-40; "
    "workbench/ocr/paddle_ocr/下/part02/page_0241.txt:3-32"
)
SCOPE_START = '<h4 id="第五十六卷-第三章运动项目-第四节其它类">第四节其它类</h4>'
SCOPE_END = '<h3 id="第五十六卷-第四章体育竞赛">第四章体育竞赛</h3>'

NEW_HTML = """<p><strong>一、游泳</strong></p>
<p>1965年，在毛泽东主席提出“到江、河、湖、海去游泳”的号召下，连云港市于7～8月间组织三次大规模游泳活动；7月底3000人畅游蔷薇河，8月初5000人畅游沂沭新河（含400人武装泗渡），8月底10000人渡海游泳。全年全市有5万人参加游泳，学会游泳有8000人。市制碘厂6～9月组织职工游泳15次（全厂性4次、班组11次），下水127人，占全厂职工81%。</p>
<p>1972年7月16日，纪念毛泽东畅游长江六周年，市组织12000人参加游泳活动。1978年8月，市举办游泳比赛，分成年组（男、女）、少年组（男、女），共设24个比赛项目。锦屏公社和锦屏磷矿分获成年组和少年组团体总分第一名。1987年，市举办小学体育传统项目学校游泳比赛。市站北街小学获女子组团体总分第一名（代表市参加省比赛，获第11名）；锦屏小学获男子组团体总分第一名。1988年，市举办游泳传统校游泳比赛，赣榆县代表队获男、女团体冠军，并获得14项中的13块金牌。</p>
<p>1990年9月，在江苏省第12届运动会游泳比赛中，连云港市运动员在男11岁组个人混合泳中获两个第四名，在女10岁组个人混合泳中获第二名、第三名、第四名各1个。同年，少儿业余体校游泳班有学员41人（在重点业余体校8人、普通业余体校33人）。</p>
<p><strong>二、帆板</strong></p>
<p>1984年4月，连云港市组建帆板运动队，属省队市办。建队后即去青岛学习。同年7月，参加在秦皇岛举行的全国帆板锦标赛，并请各运动队的教练和高水平的运动员讲授训练知识，使这一新项目在训练方法和技术掌握上有了一定的基础。1986年，在全国优秀选手赛中，连云港市运动员陈永明获男子组三角绕标第五名。1987年，在全国沿海城市少年帆板比赛中，陈作涛获男子长距离第三名。同年，在全国帆板锦标赛中，陈永明获男子三角绕标第三名。</p>
<p><strong>三、摔跤、柔道</strong></p>
<p>1985年1月，连云港市组建摔跤队，有男运动员16人，后增至20人，人员以海州中学学生为主及蔷薇中学、幸福路中学的学生，训练地点在海州中学。为迎接1986年江苏省十一届运动会，于1985年底把摔跤队集中到市业余体校训练，列为市业余体校一个训练项目。同年，在江苏省十一届运动会上，市摔跤队获金牌1块，银牌4块，铜牌3块。1987年4月，组建连云港市柔道队，设7个级别，共有运动员12人。同年，在徐州举行的省摔跤、柔道锦标赛上，连云港市获摔跤金牌8块、银牌4块，获柔道金牌2块、银牌3块。至1987年底，摔跤和柔道2个队增至38人，其中女运动员14人。1988年，在连云港市举行的省摔跤、柔道锦标赛上，连云港市获摔跤金牌5块（男3、女2）、银牌8块（男5、女3），获柔道金牌2块（男、女各1）、银牌4块。</p>
<p>1990年，在江苏省十二届运动会上，连云港市摔跤队获团体总分第三名，在单项比赛中获金牌1块、银牌3块，柔道获男子团体第一名，女子团体第三名，在单项比赛中获金牌3块（男2、女1）、银牌2块（男）、银牌4块（男、女各2）。</p>
<p><strong>四、举重</strong></p>
<p>建国前，市内城乡民间均有举石担、石锁活动。建国后，开展举重业余训练。1957年，在江苏省第三届运动会上，将举重列为正式比赛项目。在这届运动会上，新海连市李增玺获重量级推举（72.5公斤）、抓举（75公斤）、挺举（90公斤）、总成绩（237.5公斤）4个第一名。</p>
<p>1974年，在江苏省第八届运动会上，连云港市张成宝破青少年组（次轻量级）省纪录，成绩：抓举78公斤，挺举95.5公斤，总成绩173.5公斤。1978年，在江苏省第九届运动会上，连云港市谢观怀获轻重量级第一名，成绩抓举110公斤，挺举145公斤，总成绩255公斤。1979年，市组建举重代表队，队员13人，隶属市业余体校。</p>
<p>1982年，在江苏省第十届运动会上，连云港市刘光明、孟丁柱、刘建军3人破7项次省少年组举重纪录，徐彬获少年组60公斤总成绩和抓举第一名。</p>
<p>1990年，在江苏省十二届运动会上，刘长柱破男子乙组56公斤级挺举省纪录（成绩85公斤，原纪录75公斤），茆庆勇破男子乙组60公斤级挺举省纪录（成绩85公斤，原纪录80公斤），董自亮破男子乙组75公斤级抓举、挺举、总成绩三项省纪录（抓举58.5公斤，挺举78.5公斤，总成绩137公斤，原纪录抓举57公斤，挺举77.5公斤，总成绩134.5公斤）。</p>
<p><strong>五、信鸽</strong></p>
<p>1985年5月，连云港市成立了信鸽协会，有会员30人，信鸽1200羽。此后，市多次派队参加了全国、省信鸽竞翔。1989年在郑州“建国杯”全国信鸽大赛中，一羽获雄鸽冠军。</p>
<p>1990年，在参加全国500公里和200公里信鸽竞翔中，获2项冠军、1项亚军和2项第三名。至1990年，信鸽协会会员已发展到400人，有5万羽信鸽。</p>"""

EXPECTED_TEXT = [
    "<p><strong>一、游泳</strong></p>",
    "提出“到江、河、湖、海去游泳”的号召",
    "1990年9月，在江苏省第12届运动会游泳比赛中",
    "<p><strong>二、帆板</strong></p>",
    "<p><strong>三、摔跤、柔道</strong></p>",
    "组建摔跤队",
    "蔷薇中学",
    "省摔跤、柔道锦标赛",
    "<p><strong>四、举重</strong></p>",
    "茆庆勇破男子乙组60公斤级挺举省纪录",
    "<p><strong>五、信鸽</strong></p>",
]
RESIDUALS = [
    "一、游泳1965年",
    "提出到江、河、湖、海去游泳”",
    "体育传统项：目学校",
    "<p>混合泳中获两个第四名",
    "二、帆板1984年",
    "三、摔、柔道",
    "组建摔队",
    "蕃薇中学",
    "省摔、柔道锦标赛",
    "<p>：1990年",
    "连云港市摔队",
    "四、举重建国前",
    "，庆勇破男子乙组60公斤级",
    "五、信　鸽",
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
        raise RuntimeError(f"sports other expected text missing: {missing}")
    remaining = [item for item in RESIDUALS if item in segment]
    if remaining:
        raise RuntimeError(f"sports other residue remains: {remaining}")
    return changed, {"rewrote_scope": changed}


def write_reports(changed: int, counts: dict[str, int]) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "第五十六卷体育 / 第三章运动项目 / 第四节其它类",
        "source": SOURCE_NOTE,
        "reader_path": str(HTML),
        "changes_this_run": changed,
        "counts": counts,
        "principle": "依据 PaddleOCR 页级文本重建其它类整节，修复小标题粘连、漏句和明确错识。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    md = f"""# 第五十六卷其它类回源修复

- 时间：{now}
- 范围：`第五十六卷体育 / 第三章运动项目 / 第四节其它类`
- 源文依据：`{SOURCE_NOTE}`

## 修复动作

- 按页级 OCR 重建 `第四节其它类` 整节，拆分 `一、游泳`、`二、帆板`、`三、摔跤、柔道`、`四、举重`、`五、信鸽` 小标题。
- 补回 `1990年9月，在江苏省第12届运动会游泳比赛中` 段首。
- 修正游泳号召引号、`体育传统项目学校`、`摔跤队`、`蔷薇中学`、`省摔跤、柔道锦标赛`、`茆庆勇`、`信鸽` 等明确错识。
- 首次运行已完成 1 处整段替换；稳定复跑新增整段替换：{changed} 处。
- 本轮未处理 `第四章体育竞赛`。

## 核对说明

- PaddleOCR `page_0240.txt` 确认第四节开头至摔跤、柔道前段。
- PaddleOCR `page_0241.txt` 确认摔跤、柔道尾段、举重、信鸽和第四章边界。
"""
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")


def update_memory(changed: int) -> None:
    marker = "## 2026-07-03 第五十六卷其它类回源修复"
    memory = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker in memory:
        return
    entry = f"""
{marker}

- 对第五十六卷体育第三章运动项目 `第四节其它类` 进行回源修复。
- 源文依据：`{SOURCE_NOTE}`；重建整节，拆分 `一、游泳`、`二、帆板`、`三、摔跤、柔道`、`四、举重`、`五、信鸽` 小标题。
- 补回 `1990年9月，在江苏省第12届运动会游泳比赛中` 段首；修正游泳号召引号、`体育传统项目学校`、`摔跤队`、`蔷薇中学`、`省摔跤、柔道锦标赛`、`茆庆勇`、`信鸽` 等明确错识。
- 首次运行已完成 1 处整段替换；稳定复跑新增整段替换 {changed} 处；`第四章体育竞赛` 未在本脚本中处理。
- 报告：`output/reports/reader_readability_sports_other_section_20260703.md`。
"""
    MEMORY.write_text(memory.rstrip() + "\n\n" + entry.lstrip(), encoding="utf-8")


def main() -> None:
    changed, counts = patch_reader()
    write_reports(changed, counts)
    update_memory(changed)
    print("sports other section repaired")
    print(f"changes={changed}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()
