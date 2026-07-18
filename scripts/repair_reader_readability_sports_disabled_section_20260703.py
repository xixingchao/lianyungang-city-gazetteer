# -*- coding: utf-8 -*-
"""Restore sports disabled section from page OCR."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_sports_disabled_section_20260703.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_sports_disabled_section_20260703.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260703_第五十六卷残疾人体育回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SOURCE_NOTE = (
    "workbench/ocr/paddle_ocr/下/part02/page_0223.txt:19-40; "
    "workbench/ocr/paddle_ocr/下/part02/page_0224.txt:3-9"
)
SCOPE_START = '<h4 id="第五十六卷-第一章社会体育-第五节残疾人体育">第五节残疾人体育</h4>'
SCOPE_END = '<h3 id="第五十六卷-第二章学校体育">第二章学校体育</h3>'

NEW_HTML = """<p>1954年，新浦区聋哑人夜校有15名聋哑青年组织篮球队开展活动。1956年在新浦盐河区篮球赛中，聋哑人篮球队获第二名。1958年在新浦龙尾区篮球赛中，聋哑人篮球队获得第三名。1959年，省第一届聋哑人男子篮球选拔赛在苏州举行，新海连市聋哑皮革厂职工篮球队代表新海连市参赛，获得亚军。1960年10月，省举办聋哑人田径通讯比赛，新海连市男子参赛10个项目，女子参赛8个项目。</p>
<p>1982年6月，在泰州举行的苏北六市聋哑人乒乓球比赛中，市聋哑学校范红获得女子单打亚军。1983年5月，省体委委托连云港市体委承办12个沿海城市聋哑人中国象棋友谊邀请赛，连云港市队获团体第三名。同年12月，市聋哑人男、女乒乓球代表队应邀参加无锡市聋哑友好邀请赛，市聋哑学校获得女子团体亚军。1984年2月，市残疾人协会、市体委联合举办连云港市首届残疾人运动会，有21名盲人、聋哑人运动员参加比赛。同年7月，江苏省第一届残疾人运动会在常州市举行，连云港市聋哑人代表队有11名运动员参赛，获得金牌8块、银牌3块、铜牌4块，田径总分第二名，共9次打破省残疾人田径纪录。同年，省举办残疾人乒乓球赛，连云港市聋哑学校获团体亚军。1985年7月，在泰州市举行的省聋哑学校游泳比赛中，连云港市聋哑学校获得4×100米接力赛第一名、仰泳第五名。1986年4月，在铜山县举行陇海沿线城市徐州、铜山、砀山、连云港四所聋哑学校男子篮球邀请赛，连云港市聋哑人代表队获第二名。1987年7月，江苏省第二届残疾人运动会在东台举行。连云港市聋哑人代表队共打破6项残疾人省田径纪录，夺得金牌6块、银牌12块、铜牌5块。3人被授予“精神文明运动员”称号，有3人被选拔参加全国残疾人运动会。1988年5月，淮海工学院残疾人李扬代表中国赴意大利、法国访问，并参加法国国际残疾人乒乓球邀请赛，获得金牌1块、银牌2块，并获本届邀请赛唯一“最佳运动员”称号，受到法国总统密特朗的接见。同年10月，李扬又代表中国赴韩国汉城参加世界残疾人奥运会，被奥运会裁判长赞誉为“亚洲残疾人乒坛的代表”。</p>
<p>1989年9月，李扬代表中国赴日本神户参加第五届远东及南太平洋地区伤残人运动会，获乒乓球赛金牌2块、银牌1块，为祖国争光，受到中央、省、市领导的表彰。同年，在省聋哑学校田径运动会上，连云港市聋哑学校获团体总分第二名，女子组杜芳获1500米第一名，钱红萍获铅球第一名、标枪第一名。至1990年，东海县聋哑学校先后参加省级以上各类比赛7次，共获得金牌12块，银牌10块，铜牌及其它奖牌33块。</p>"""

EXPECTED_TEXT = [
    "新浦区聋哑人夜校有15名聋哑青年组织篮球队开展活动",
    "省第一届聋哑人男子篮球选拔赛在苏州举行",
    "淮海工学院残疾人李扬代表中国赴意大利、法国访问",
    "第五届远东及南太平洋地区伤残人运动会",
]
RESIDUALS = [
    "新浦区哑人夜校",
    "省第届聋哑人男子篮球选拔赛",
    "准海工学院残疾人李扬",
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
        raise RuntimeError(f"sports disabled expected text missing: {missing}")
    remaining = [item for item in RESIDUALS if item in segment]
    if remaining:
        raise RuntimeError(f"sports disabled residue remains: {remaining}")
    return changed, {"rewrote_scope": changed}


def write_reports(changed: int, counts: dict[str, int]) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "第五十六卷体育 / 第一章社会体育 / 第五节残疾人体育",
        "source": SOURCE_NOTE,
        "reader_path": str(HTML),
        "changes_this_run": changed,
        "counts": counts,
        "principle": "依据 PaddleOCR 页级文本重建残疾人体育整节，修复明确 OCR 错识。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    md = f"""# 第五十六卷残疾人体育回源修复

- 时间：{now}
- 范围：`第五十六卷体育 / 第一章社会体育 / 第五节残疾人体育`
- 源文依据：`{SOURCE_NOTE}`

## 修复动作

- 按页级 OCR 重建 `第五节残疾人体育` 整节。
- 修正 `新浦区哑人夜校` 为 `新浦区聋哑人夜校`。
- 修正 `省第届聋哑人男子篮球选拔赛` 为 `省第一届聋哑人男子篮球选拔赛`。
- 修正 `准海工学院残疾人李扬` 为 `淮海工学院残疾人李扬`。
- 本次复跑新增整段替换：{changed} 处。
- 本轮未处理 `第二章学校体育`。

## 核对说明

- PaddleOCR `page_0223.txt` 确认第五节开头至 1988 年李扬赴法国访问段。
- PaddleOCR `page_0224.txt` 确认 1988 年尾至 1990 年段，并给出第二章边界。
"""
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")


def update_memory(changed: int) -> None:
    marker = "## 2026-07-03 第五十六卷残疾人体育回源修复"
    memory = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker in memory:
        return
    entry = f"""
{marker}

- 对第五十六卷体育第一章社会体育 `第五节残疾人体育` 进行回源修复。
- 源文依据：`{SOURCE_NOTE}`；重建整节，修正 `聋哑人夜校`、`省第一届聋哑人男子篮球选拔赛`、`淮海工学院残疾人李扬` 等明确错识。
- 本轮新增整段替换 {changed} 处；`第二章学校体育` 未在本脚本中处理。
- 报告：`output/reports/reader_readability_sports_disabled_section_20260703.md`。
"""
    MEMORY.write_text(memory.rstrip() + "\n\n" + entry.lstrip(), encoding="utf-8")


def main() -> None:
    changed, counts = patch_reader()
    write_reports(changed, counts)
    update_memory(changed)
    print("sports disabled section repaired")
    print(f"changes={changed}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()
