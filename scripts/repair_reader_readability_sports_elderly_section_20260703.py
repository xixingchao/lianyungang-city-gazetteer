# -*- coding: utf-8 -*-
"""Restore sports elderly section from page OCR."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_sports_elderly_section_20260703.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_sports_elderly_section_20260703.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260703_第五十六卷老年人体育回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SOURCE_NOTE = (
    "workbench/ocr/paddle_ocr/下/part02/page_0222.txt:27-40; "
    "workbench/ocr/paddle_ocr/下/part02/page_0223.txt:3-18"
)
SCOPE_START = '<h4 id="第五十六卷-第一章社会体育-第四节老年人体育">第四节老年人体育</h4>'
SCOPE_END = '<h4 id="第五十六卷-第一章社会体育-第五节残疾人体育">第五节残疾人体育</h4>'

NEW_HTML = """<p>建国前，连云港市参加体育活动的老年人不多。建国后，随着人民生活的提高，越来越多的老年人参加体育锻炼。</p>
<p>1973年，市体委举办练功十八法、太极剑训练班11期，共培训615人次。1974～1977年，市体委举办两期简化太极拳训练班，学员260人，多数是老年人。通过学习与锻炼，很多人治好慢性病。1979年，市体委配合卫生部门在中老年中开展医疗保健体育。同年，市举办老人（走或跑）500米、1000米，累计全程3万米到6万米比赛。</p>
<p>1980年11月24日，在市体育场举办老年人长跑比赛，分1500米、3000米两项。1981年，成立老年中长跑队4个，队员480人，举办操拳学习班12期，学习人数1116人次，开展练功十八法、气功等一些医疗体育活动。1982年，连云港市老年长跑队参加省长跑比赛，新浦磷矿职工李宁远获冠军。1983年，全市举办鹤翔庄气功训练班20个，有4990人次参加。是年，东海县春节环城赛跑有万名老人参加。</p>
<p>1984年，有操拳辅导站15个，举办操拳训练班100期，参加学习人数2万人次，其中退离休干部、老年工人占多数。1985年，连云港市有7位老人被省评为“健康老人”。是年，东海县成立老年人体育协会，有会员140人，举办登山、自行车旅游、乒乓球等项比赛。1985年，省举办第三届老人长中比赛，新浦磷矿职工李宁远又获1万米比赛第一名。1986年，老年门球在全市逐步推广。东海县老年门球活动比较活跃，县体委还举办门球训练班。到1987年全县有17个门球队，队员共109人，建门球场15块。1986年市体委举办中老年妇女健美操和老年迪斯科健身操培训班6期，参加培训的老年妇女有450人次。新浦地区有100个单位、3000名中老年参加健身操活动。1987年，连云港市举办老年象棋、钓鱼、游泳、乒乓球、门球、篮球6项7次比赛。市老年门球队于1987年组成，共有队员64人，同年5月，在商丘淮海经济区“九龙杯”门球赛中获第四名。东海县老年门球队在1987年省门球赛中夺取冠军，并代表江苏省参加全国门球比赛。1988年，评选“江苏健康老人”，连云港市沈俊丰等10名老人入选。市退休职工管理委员会决定，从1988年起，每年举办一次退休职工体育活动。同年，市退休职工运动会在市文化宫举行。比赛项目有象棋、扑克、乒乓球、钓鱼等。10月，江苏省第三届老年门球赛在东海县举行，东海县派出两个队，分别代表连云港市和东海县参赛，分别获得第二名和第三名。东海县门球队先后参加全国和省、市比赛15次，共获金牌5块，银牌2块，铜牌1块，其中获全国银牌1块，省金牌2块、银牌1块。</p>
<p>1990年，在徐州市举办的全省老干部门球赛中，市老年门球队获得冠军。</p>"""

EXPECTED_TEXT = [
    "新浦磷矿职工李宁远又获1万米比赛第一名",
    "在商丘淮海经济区“九龙杯”门球赛中获第四名",
    "连云港市沈俊丰等10名老人入选",
    "比赛项目有象棋、扑克、乒乓球、钓鱼等",
    "全省老干部门球赛中，市老年门球队获得冠军",
]
RESIDUALS = [
    "1万来比赛第一名",
    "“九龙杯门球赛",
    "老人人选",
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
        raise RuntimeError(f"sports elderly expected text missing: {missing}")
    remaining = [item for item in RESIDUALS if item in segment]
    if remaining:
        raise RuntimeError(f"sports elderly residue remains: {remaining}")
    return changed, {"rewrote_scope": changed}


def write_reports(changed: int, counts: dict[str, int]) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "第五十六卷体育 / 第一章社会体育 / 第四节老年人体育",
        "source": SOURCE_NOTE,
        "reader_path": str(HTML),
        "changes_this_run": changed,
        "counts": counts,
        "principle": "依据 PaddleOCR 页级文本重建老年人体育整节，修复明确 OCR 错识和引号断裂。",
        "notes": ["保留两套 OCR 均读为“老人长中比赛”的表述，后续如有更高置信源再复核。"],
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    md = f"""# 第五十六卷老年人体育回源修复

- 时间：{now}
- 范围：`第五十六卷体育 / 第一章社会体育 / 第四节老年人体育`
- 源文依据：`{SOURCE_NOTE}`

## 修复动作

- 按页级 OCR 重建 `第四节老年人体育` 整节。
- 修正 `1万来比赛` 为 `1万米比赛`、补齐 `“九龙杯”门球赛` 引号、修正 `老人入选` 与 `比赛项目`。
- 保留两套 OCR 均读为 `老人长中比赛` 的表述，后续如有更高置信源再复核。
- 本次复跑新增整段替换：{changed} 处。
- 本轮未处理 `第五节残疾人体育`。

## 核对说明

- PaddleOCR `page_0222.txt` 确认第四节开头至 1984 年前。
- PaddleOCR `page_0223.txt` 确认 1984 年至 1990 年段，并给出第五节边界。
"""
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")


def update_memory(changed: int) -> None:
    marker = "## 2026-07-03 第五十六卷老年人体育回源修复"
    memory = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker in memory:
        return
    entry = f"""
{marker}

- 对第五十六卷体育第一章社会体育 `第四节老年人体育` 进行回源修复。
- 源文依据：`{SOURCE_NOTE}`；重建整节，修正 `1万米比赛`、`“九龙杯”门球赛`、`老人入选`、`比赛项目` 等明确错识和引号断裂。
- 两套 OCR 均读为 `老人长中比赛`，本轮保留该表述，后续如有更高置信源再复核。
- 本轮新增整段替换 {changed} 处；`第五节残疾人体育` 未在本脚本中处理。
- 报告：`output/reports/reader_readability_sports_elderly_section_20260703.md`。
"""
    MEMORY.write_text(memory.rstrip() + "\n\n" + entry.lstrip(), encoding="utf-8")


def main() -> None:
    changed, counts = patch_reader()
    write_reports(changed, counts)
    update_memory(changed)
    print("sports elderly section repaired")
    print(f"changes={changed}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()
