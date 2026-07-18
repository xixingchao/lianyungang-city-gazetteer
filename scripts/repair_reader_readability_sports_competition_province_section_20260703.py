# -*- coding: utf-8 -*-
"""Restore sports competition province-level section from page OCR."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_sports_competition_province_section_20260703.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_sports_competition_province_section_20260703.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260703_第五十六卷参加省体育竞赛回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SOURCE_NOTE = (
    "workbench/ocr/paddle_ocr/下/part02/page_0243.txt:14-39; "
    "workbench/ocr/paddle_ocr/下/part02/page_0244.txt:3-20"
)
SCOPE_START = '<h4 id="第五十六卷-第四章体育竞赛-第二节参加省体育竞赛">第二节参加省体育竞赛</h4>'
SCOPE_END = '<h3 id="第五十六卷-第五章训练 队伍">第五章训练 队伍</h3>'

NEW_HTML = """<p>民国8年（1919年）5月，江苏省中等学校联合运动会在南京举行。东海中学的殷学礼获撑杆跳高第一名，成绩2.81米。民国20年9月，江苏省第四届运动会在镇江省立体育场举行。东海、灌云、赣榆、沭阳四县选拔运动员参赛。民国24年9月，江苏省第四届运动会在镇江省立体育场举行。灌云县的李延祥打破400米省纪录，代表省参加在上海举行的全国运动会。民国25年于金孝代表中国队参加远东运动会，100米赛的成绩11\"6。</p>
<p>民国30年至民国33年伪淮海省在徐州举办一至三届运动会，伪海州市（包括新浦、海州）运动员滕子复获一至三届男子成年组100米、200米第一名。男子篮球队获第一、二届冠军，第三届亚军。</p>
<p>1950年11月，山东省第一届运动会在济南市人民体育场举行。新海连市部分运动员参加临沂地区组队参赛。</p>
<p>1955年10月，江苏省第二届运动会在南京公园路体育场举行。新海连市组队参赛。</p>
<p>1957年9月，江苏省第三届运动会在南京举行。新海连市参加田径、举重两项比赛，获金牌1块、铜牌1块。</p>
<p>1958年，江苏省第四届运动会在南京举行。新海连市当时属徐州专区管辖，运动员参加徐州专区组队。参加项目：田径、篮球、排球、射击。新海连市运动员获银牌2块、铜牌1块。</p>
<p>1959年5月，江苏省第五届运动会在南京举行。新海连市运动员仍参加徐州专区组队。参加项目：田径、篮球、足球、射击。连云港市获金牌4块、银牌2块、铜牌1块。</p>
<p>1960年9月，江苏省第六届运动会在南京举行。新海连市获团体总分第六名，获金牌5块，铜牌2块。</p>
<p>1964年10月，江苏省第七届运动会在南京举行。连云港市组队参加田径、篮球、排球、乒乓球、射击5个项目比赛。女子篮球队获冠军，男子篮球队获亚军。</p>
<p>1974年9月，江苏省第八届运动会在南京举行。连云港市组成200余人体育代表团参加田径、篮球、排球、足球、自行车、体操、举重、乒乓球8个项目比赛。获银牌2块、铜牌2块，打破4项省青少年组纪录。</p>
<p>1978年9月，江苏省第九届运动会在南京举行。连云港市组成200多人体育代表团，参加田径、篮球、排球、足球、乒乓球、体操、射击、举重8项比赛，获金牌4块，银牌1块，铜牌11块，有2人破省少年组纪录。其中男子篮球队获得冠军。</p>
<p>1982年9月，江苏省第十届运动会在南京举行。连云港市组成200多人体育代表团，参加田径、篮球、排球、足球、乒乓球、举重、击剑、武术、射击、无线电测向10个项目比赛，获金牌11块、银牌14块、铜牌3块。打破6项省少年组纪录。</p>
<p>1986年，江苏省第十一届运动会在徐州市举行。比赛分中小学部、高校部、职工部、优秀运动员部。连云港市参加田径、游泳、篮球等16个项目比赛，获金牌9块、银牌31块、铜牌21块，打破2项省少年组纪录。在田径比赛中，中小学部青年组获团体总分第二名。</p>
<p>1990年9月，江苏省第十二届运动会在南京举行。连云港市组成300人的体育代表团，参加田径、篮球、举重等12个项目比赛。在田径比赛中获青少年部男子A组团体总分第一名。获金牌19块、银牌22块，有3人获“精神文明运动员”称号，田径赛成年组、少年组打破省纪录各1次。</p>
<p>此外，连云港籍优秀运动员或代表省参加了全国性比赛，或代表国家参加了国际比赛，都取得了优异的成绩。</p>"""

EXPECTED_TEXT = [
    "100米赛的成绩11\"6",
    "男子篮球队获第一、二届冠军，第三届亚军。",
    "参加田径、篮球、排球、足球、自行车、体操、举重、乒乓球8个项目比赛",
    "青少年部男子A组团体总分第一名",
    "此外，连云港籍优秀运动员或代表省参加了全国性比赛",
]
RESIDUALS = [
    "成绩116",
    "冠军,第三届亚军",
    "8个项自比赛",
    "第一一名",
    "连云港市运动员竞赛成绩一览表",
    "表56-6",
    "<p>2530</p>",
    "体育竞赛: 2531",
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
        raise RuntimeError(f"sports competition province expected text missing: {missing}")
    remaining = [item for item in RESIDUALS if item in segment]
    if remaining:
        raise RuntimeError(f"sports competition province residue remains: {remaining}")
    return changed, {"rewrote_scope": changed}


def write_reports(changed: int, counts: dict[str, int]) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "第五十六卷体育 / 第四章体育竞赛 / 第二节参加省体育竞赛",
        "source": SOURCE_NOTE,
        "reader_path": str(HTML),
        "changes_this_run": changed,
        "counts": counts,
        "principle": "依据 PaddleOCR 页级文本重建第二节正文，撤出阅读版中的表格残片和页眉页码残留。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    md = f"""# 第五十六卷参加省体育竞赛回源修复

- 时间：{now}
- 范围：`第五十六卷体育 / 第四章体育竞赛 / 第二节参加省体育竞赛`
- 源文依据：`{SOURCE_NOTE}`

## 修复动作

- 按页级 OCR 重建 `第二节参加省体育竞赛` 正文，停止在 `第五章训练 队伍` 前。
- 修正 `11\"6`、`冠军，第三届亚军`、`8个项目比赛`、`第一名` 等明确错识。
- 撤出阅读版中紧随正文的 `连云港市运动员竞赛成绩一览表`、`表56-6` 及页眉页码残片；该表续页已有结构化条目 `LYG-下-T087`、`LYG-下-T088`，首页未在本轮补录。
- 首次运行已完成 1 处整段替换；稳定复跑新增整段替换：{changed} 处。

## 核对说明

- PaddleOCR `page_0243.txt` 确认第二节起始至 1974 年省八运会段。
- PaddleOCR `page_0244.txt` 确认 1978 年至第二节正文结束，并确认后续进入 `表56-6`。
"""
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")


def update_memory(changed: int) -> None:
    marker = "## 2026-07-03 第五十六卷参加省体育竞赛回源修复"
    memory = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker in memory:
        return
    entry = f"""
{marker}

- 对第五十六卷体育第四章体育竞赛 `第二节参加省体育竞赛` 进行回源修复。
- 源文依据：`{SOURCE_NOTE}`；重建正文至 `第五章训练 队伍` 前。
- 修正 `11\"6`、`冠军，第三届亚军`、`8个项目比赛`、`第一名` 等明确错识。
- 撤出阅读版中的 `连云港市运动员竞赛成绩一览表`、`表56-6` 及页眉页码残片；表56-6续页已有 `LYG-下-T087`、`LYG-下-T088`，首页未在本轮补录。
- 首次运行已完成 1 处整段替换；稳定复跑新增整段替换 {changed} 处。
- 报告：`output/reports/reader_readability_sports_competition_province_section_20260703.md`。
"""
    MEMORY.write_text(memory.rstrip() + "\n\n" + entry.lstrip(), encoding="utf-8")


def main() -> None:
    changed, counts = patch_reader()
    write_reports(changed, counts)
    update_memory(changed)
    print("sports competition province section repaired")
    print(f"changes={changed}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()
