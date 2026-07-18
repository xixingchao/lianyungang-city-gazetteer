# -*- coding: utf-8 -*-
"""Restore sports competition city-level section from page OCR."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_sports_competition_city_section_20260703.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_sports_competition_city_section_20260703.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260703_第五十六卷体育竞赛市级体育竞赛回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SOURCE_NOTE = (
    "workbench/ocr/paddle_ocr/下/part02/page_0241.txt:31-35; "
    "workbench/ocr/paddle_ocr/下/part02/page_0242.txt:3-40; "
    "workbench/ocr/paddle_ocr/下/part02/page_0243.txt:3-14"
)
SCOPE_START = '<h3 id="第五十六卷-第四章体育竞赛">第四章体育竞赛</h3>'
SCOPE_END = '<h4 id="第五十六卷-第四章体育竞赛-第二节参加省体育竞赛">第二节参加省体育竞赛</h4>'

NEW_HTML = """<p>民国8年（1919年），省第八师范就有人参加省级竞赛。20世纪30年代，赣榆、东海、灌云3县都举办过运动会，40年代，在新浦举办过两届运动会，曾派运动员3次参加伪淮海省运动会。</p>
<p>建国后，体育部门十分重视体育竞赛，把开展体育竞赛作为推动体育普及和促进运动技术水平提高的重要措施。至1990年，举办市全民体育运动会8届、职工运动会7届、中学生田径运动会23届，多次承办省和全国性比赛。1978～1990年，市体育代表团（队）参加全省、全国比赛，获得金牌155块、银牌156块、铜牌131块，连云港市籍运动员在国际体育竞赛中，也取得可喜成绩。</p>
<h4 id="第五十六卷-第四章体育竞赛-第一节市级体育竞赛">第一节市级体育竞赛</h4>
<p><strong>一、市体育运动大会</strong></p>
<p>1949～1990年，连云港市共举办市体育运动大会八届。1952年、1955年、1956年分别举行一、二、三届。第四至五届情况查无资料。六至八届情况是：</p>
<p>1972年10月，市第六届体育运动大会在新浦举行。比赛项目有田径、自行车、排球、乒乓球、拔河五项。21个系统代表队，1546名运动员参赛，共有37人次打破市18项纪录。文教系统男、女代表队均获团体总分第一名。</p>
<p>1981年10月1～4日，市第七届体育运动大会在市体育场举行。比赛项目：田径。分成年和学生两大组进行，参赛人数578人。</p>
<p>1989年10月1～3日，市第八届体育运动大会在新浦举行。比赛设中小学部、高校中专（技）校部、职工部。比赛项目：中小学部有田径、篮球、排球、举重、摔跤、柔道、无线电测向；高校中专（技）校部有田径、羽毛球；职工部有田径、篮球、排球、乒乓球、棋类。参赛人数716人。</p>
<p><strong>二、市职工运动会</strong></p>
<p>1954～1984年，连云港市共举办职工运动会7届。</p>
<p>1954年“五一”节，市首届职工运动会在新浦举行。参赛运动员286人，进行田径、拔河、广播操、民族体育比赛和表演。有21个项目破市纪录。</p>
<p>1955年“五一”节，市职工第二届运动会在新浦举行。比赛项目：男子19个、女子13个。李增玺、李英杰打破铅球、手榴弹两项省纪录。</p>
<p>1956年5月1日，市第三届职工运动会在新浦举行。有4人分别创铅球、铁饼、标枪、手榴弹市纪录。</p>
<p>1957年5月1日，市第四届职工运动会在新浦举行。有2人分别创10000米和5000米市纪录，1人创最轻量级举重最高纪录。</p>
<p>1958年5月1日，市第五届职工运动会在新浦举行。比赛项目有田径、篮球、自行车、举重、拔河等，有300名运动员参赛。</p>
<p>1984年10月1～5日，市第七届职工运动会在新浦举行。选拔组建篮球、排球、足球、田径、武术、游泳、举重等8个项目代表队，参加省第二届职工运动会。</p>
<p><strong>三、市中学生田径运动会</strong></p>
<p>1958～1989年，连云港市共举办中学生田径运动会23届（一般都在每届中学生田径运动会同时举办小学生田径运动会）。</p>
<p>1958年6月，市首届中学生田径运动会在新浦举行。有8所学校384名运动员参赛。</p>
<p>1965年，市第六届中学生田径运动会在新浦举行。初中组有20人次打破16项次市纪录，高中组有17人次打破13项次市纪录。初中组有两人打破两项省纪录，高中组有3人打破3项省纪录。</p>
<p>1977年9月，市第十一届中学生田径运动会在新浦举行，有两人打破两项市纪录。</p>
<p>1979年，市第十四届中学田径运动会在新浦举行。</p>
<p>1983年10月，市第十七届中学生田径运动会在新浦举行，有6人打破6项市纪录。</p>
<p>1989年10月，市第二十三届中学生田径运动会在新浦举行。这届运动会分高中部、初中部、小学部男、女六组进行比赛。</p>"""

EXPECTED_TEXT = [
    "<p><strong>一、市体育运动大会</strong></p>",
    "比赛项目有田径、自行车、排球、乒乓球、拔河五项",
    "摔跤、柔道、无线电测向",
    "<p><strong>二、市职工运动会</strong></p>",
    "1955年“五一”节，市职工第二届运动会",
    "比赛项目有田径、篮球、自行车、举重、拔河等",
    "<p><strong>三、市中学生田径运动会</strong></p>",
    "1979年，市第十四届中学田径运动会在新浦举行。",
]
RESIDUALS = [
    "一、市体育运动大会1949",
    "二、市职工运动会1954",
    "三、市中学生田径运动会1958",
    "摔、柔道",
    "拨河",
    "1955年五一”节",
    "比赛项自有",
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
        raise RuntimeError(f"sports competition city expected text missing: {missing}")
    remaining = [item for item in RESIDUALS if item in segment]
    if remaining:
        raise RuntimeError(f"sports competition city residue remains: {remaining}")
    return changed, {"rewrote_scope": changed}


def write_reports(changed: int, counts: dict[str, int]) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "第五十六卷体育 / 第四章体育竞赛 / 导语与第一节市级体育竞赛",
        "source": SOURCE_NOTE,
        "reader_path": str(HTML),
        "changes_this_run": changed,
        "counts": counts,
        "principle": "依据 PaddleOCR 页级文本重建第四章导语和第一节，修复小标题粘连、漏句和明确错识。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    md = f"""# 第五十六卷体育竞赛市级体育竞赛回源修复

- 时间：{now}
- 范围：`第五十六卷体育 / 第四章体育竞赛 / 导语与第一节市级体育竞赛`
- 源文依据：`{SOURCE_NOTE}`

## 修复动作

- 按页级 OCR 重建 `第四章体育竞赛` 导语和 `第一节市级体育竞赛`，停止在 `第二节参加省体育竞赛` 前。
- 拆分 `一、市体育运动大会`、`二、市职工运动会`、`三、市中学生田径运动会` 小标题。
- 修正 `摔跤、柔道`、`拔河`、`1955年“五一”节`、`比赛项目` 等明确错识。
- 补回 `1979年，市第十四届中学田径运动会在新浦举行。`
- 首次运行已完成 1 处整段替换；稳定复跑新增整段替换：{changed} 处。

## 核对说明

- PaddleOCR `page_0241.txt` 确认第四章起始导语。
- PaddleOCR `page_0242.txt` 确认第一节前两小节和第三小节起始。
- PaddleOCR `page_0243.txt` 确认第三小节尾段和 `第二节参加省体育竞赛` 边界。
"""
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")


def update_memory(changed: int) -> None:
    marker = "## 2026-07-03 第五十六卷体育竞赛市级体育竞赛回源修复"
    memory = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker in memory:
        return
    entry = f"""
{marker}

- 对第五十六卷体育第四章体育竞赛 `导语与第一节市级体育竞赛` 进行回源修复。
- 源文依据：`{SOURCE_NOTE}`；重建至 `第二节参加省体育竞赛` 前，未触碰第二节正文。
- 拆分 `一、市体育运动大会`、`二、市职工运动会`、`三、市中学生田径运动会` 小标题；修正 `摔跤、柔道`、`拔河`、`1955年“五一”节`、`比赛项目` 等明确错识。
- 补回 `1979年，市第十四届中学田径运动会在新浦举行。`
- 首次运行已完成 1 处整段替换；稳定复跑新增整段替换 {changed} 处。
- 报告：`output/reports/reader_readability_sports_competition_city_section_20260703.md`。
"""
    MEMORY.write_text(memory.rstrip() + "\n\n" + entry.lstrip(), encoding="utf-8")


def main() -> None:
    changed, counts = patch_reader()
    write_reports(changed, counts)
    update_memory(changed)
    print("sports competition city section repaired")
    print(f"changes={changed}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()
