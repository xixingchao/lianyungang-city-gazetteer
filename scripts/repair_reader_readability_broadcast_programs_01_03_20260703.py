# -*- coding: utf-8 -*-
"""Restore broadcast program setting sections 1-3 from page OCR."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_broadcast_programs_01_03_20260703.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_broadcast_programs_01_03_20260703.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260703_第五十四卷广播节目设置一至三回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SOURCE_NOTE = "workbench/ocr/paddle_ocr/下/part02/page_0149.txt:25-37; page_0150.txt:3-39"
SCOPE_START = '<h4 id="第五十四卷-第三章广播-第三节广播节目设置">第三节广播节目设置</h4>'
SCOPE_END = '<p>四、服务性节目1983年，服务性节目有“节目预告”、“天气预报”、“影剧之窗”、“广播体操”、“广告”等。1990年，服务性节目共4个。每年的广告费净收入，从1983年的1.5万元增至1990年的11万元。</p>'

NEW_HTML = """<h4 id="第五十四卷-第三章广播-第三节广播节目设置">第三节广播节目设置</h4>
<p>连云港广播电台的节目设置，初期以转播中央台和省台为主，1959年市人民广播电台成立后，逐步以自办节目为主。“文化大革命”中一度停办。1979年恢复自办节目。</p>
<p>1983年为适应改革开放的需要，对节目作了大的调整，增加滚动新闻，举办主持人节目。</p>
<p>自办节目分为四类：新闻性节目、社会教育性节目、服务性节目和文艺性节目。</p>
<p>一、新闻性节目</p>
<p>“本市新闻”为新闻节目的主体。1952～1982年曾先后以“新闻”、“新闻和市报摘要”、“新海连生活”、“简明新闻”、“今日连云港”、“青少年之友”、“对郊区农村广播”等栏目名称出现。1983年为贯彻中共中央（1983）37号文件精神，以新闻改革为突破口，联系实际，丰富节目内容，创办了“今日快讯”、“农村节目”。1985年6月，新闻节目改用小板块式，增设“报刊摘要”（1987年1月更名为“各地之声”），一周六档。1989年5月开办板块式新闻性组合节目“星期半小时”，采用节目主持人形式，融新闻性、知识性、趣味性、服务性于一体。1990年底新闻性节目共有7个，其中“新闻”、“港城风貌”、“各地之声”、“星期半小时”影响较大。“星期半小时”栏目曾被选载入1990年的《中国广播电视年鉴》。</p>
<p>新闻录音报道。1959年《连云港军民庆祝建国十周年盛况》、1981年6月通讯《深山药场二十年》，被中央人民广播电台播用。1990年1月，两名记者深入港口，历时3个月录制成系列通讯《“东方鹿特丹”纪行》，包括《老码头焕发青春》、《三突堤异军突起》、《煤码头蜚声内外》、《新码头又再崛起》、《西大堤展现英姿》等篇目，播出后，社会反响较大，受到听众好评。</p>
<p>新闻性专题节目。1983年8月，为贯彻中共中央宣传部、中共中央书记处研究室《关于加强爱国主义宣传教育的意见》精神，结合本市实际制定《爱国主义宣传报道计划》，选题有：重点工程4个，如《60万吨碱厂工地见闻》等；名牌产品17个，如《水晶之乡说水晶》等；革命斗争史话35个，如《刘少奇在大树村》等；港城名胜14个，如《世外桃源宿城》等；名人轶事7个，如《〈镜花缘〉作者李汝珍》等；新闻人物13个，如《全国劳模李传花》等；农村水利14个，如《人定胜天的凯歌》等；……总共123个选题，一年内实施完成。</p>
<p>二、社会教育性节目</p>
<p>1959年5月至1962年5月，社会教育性节目有“政策讲座”、“文化生活”、“知识与生活”等3个。1979年7月开办“业余日语广播讲座”、“听众园地”、“学习”节目。1980年7月开设“对少儿广播”节目，播送寓言、故事和少儿习作。1981年6月开办“英语广播讲座”。1990年底有“文化与生活”、“对少儿广播”、“法制园地”、“日语广播讲座”和“英语广播讲座”等。“法制园地”曾被选载入1988年的《中国广播电视年鉴》。</p>
<p>三、文艺性节目</p>
<p>文艺性节目在整个节目量中约占一半以上。初期主要是播放唱片。1959年5月，有线广播站与电台共办一套文艺节目，每天播送2个小时，有音乐、戏剧、相声等。</p>
<p>1979年7月开设“每周一歌”、“戏曲”、“音乐”、“文艺”4个节目。1981年6月增设“听众点播”、“小说连播”节目。</p>
<p>1985年起文艺性节目进行了大幅度的调整和充实，有“音乐”、“文学”、“戏曲”、“曲艺”、“戏曲之友”、“广播剧院”、“曲艺晚会”、“每周一歌”、“听众点播”、“艺林漫步”、“长篇小说连播”等11个节目。1987年底又增加“影视欣赏”、“周末家庭晚会”。</p>
<p>1988年9月撤销“周末家庭晚会”、“戏曲之友”，增设“文艺乐园”。1990年底，文艺性节目共12个。其中“听众点播”、“长篇小说连播”影响较大。“听众点播”采用主持人形式，用男女对讲的方法述说听众的心声和要求，平均每年收到国内外听众来信达16000多封，并于1987年被选载入《中国广播电视年鉴》。截至1990年底，有保存价值的文艺节目均妥善存放，计有盘式带14000盒，盒式带2000盘。</p>
<p>至1990年，自己制作的广播剧共有17部。儿童短剧《熊猫咪咪》在1990年江苏省10家电台联办的广播剧评奖会上被评为二等奖。</p>
<p>连云港调频台调频立体声广播，创办于1989年5月，内容有中外名曲、抒情歌曲、通俗歌曲、戏曲选段和相声、童话故事等。听众普遍反映：声音悦耳动听，立体感强，特别是音域宽广的音乐效果更佳。</p>
"""

EXPECTED_TEXT = [
    "对节目作了大的调整",
    "社会教育性节目",
    "<p>一、新闻性节目</p>",
    "“新海连生活”、“简明新闻”、“今日连云港”",
    "更名为“各地之声”",
    "《深山药场二十年》",
    "《煤码头蜚声内外》",
    "《60万吨碱厂工地见闻》",
    "《〈镜花缘〉作者李汝珍》",
    "<p>二、社会教育性节目</p>",
    "英语广播讲座”等。“法制园地”",
    "<p>三、文艺性节目</p>",
    "文艺性节目共12个",
    "平均每年收到国内外听众来信达16000多封",
    "自己制作的广播剧共有17部",
]
RESIDUALS = [
    "对节自作了大的调整",
    "社会教育性节自",
    "一、新闻性节目“本市新闻”",
    "新闻和市报摘要”、出现",
    "更名为各地之声”",
    "深山制成系列通讯",
    "煤码头董声内外",
    "60万吨碱广工地见闻",
    "《《镜花缘》作者李汝珍",
    "二、社会教育性节目活”",
    "英语广三、文艺性节目",
    "文艺性节自共12个",
    "采用主持人形封",
    "选载人《中国广播电视年鉴》",
    "自已制作",
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
    return changed, {"rewrote_scope": changed, "program_sections_restored": 3}


def write_reports(changed: int, counts: dict[str, int]) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "第五十四卷报刊广播电视 / 第三章广播 / 第三节广播节目设置 / 一至三",
        "source": SOURCE_NOTE,
        "reader_path": str(HTML),
        "changes_this_run": changed,
        "counts": counts,
        "principle": "依据 PaddleOCR 页级文本重建广播节目设置一至三，停止在四、服务性节目前。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    md = f"""# 第五十四卷广播节目设置一至三回源修复

- 时间：{now}
- 范围：`第五十四卷报刊广播电视 / 第三章广播 / 第三节广播节目设置 / 一至三`
- 源文依据：`{SOURCE_NOTE}`

## 修复动作

- 按页级 OCR 重建广播节目设置开头、新闻性节目、社会教育性节目和文艺性节目，停止在 `四、服务性节目` 前。
- 补回新闻栏目列表、新闻录音报道和社会教育性节目开头，修正栏目名、书名号、省略号和 `自己制作` 等明确错文。
- 当前核验复跑整段替换：{changed} 处。
"""
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")


def update_memory(changed: int) -> None:
    marker = "## 2026-07-03 第五十四卷广播节目设置一至三回源修复"
    memory = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker in memory:
        return
    entry = f"""
{marker}

- 对第五十四卷报刊广播电视 `第三章广播 / 第三节广播节目设置 / 一至三` 进行回源修复。
- 源文依据：`{SOURCE_NOTE}`；重建至 `四、服务性节目` 前。
- 修正节目/节自、新闻栏目列表漏失、`各地之声` 引号、`深山药场二十年`、`煤码头蜚声内外`、`碱厂`、`〈镜花缘〉`、社会教育性节目开头、文艺性节目统计和 `自己制作` 等问题。
- 当前核验复跑整段替换 {changed} 处。
- 报告：`output/reports/reader_readability_broadcast_programs_01_03_20260703.md`。
"""
    MEMORY.write_text(memory.rstrip() + "\n\n" + entry.lstrip(), encoding="utf-8")


def main() -> None:
    changed, counts = patch_reader()
    write_reports(changed, counts)
    update_memory(changed)
    print(json.dumps({"changed": changed, "counts": counts}, ensure_ascii=False))


if __name__ == "__main__":
    main()
