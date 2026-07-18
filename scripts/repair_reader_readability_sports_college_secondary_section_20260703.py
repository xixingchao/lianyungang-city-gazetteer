# -*- coding: utf-8 -*-
"""Restore sports college and secondary-school section from page OCR."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_sports_college_secondary_section_20260703.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_sports_college_secondary_section_20260703.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260703_第五十六卷高校中专学校体育回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SOURCE_NOTE = (
    "workbench/ocr/paddle_ocr/下/part02/page_0230.txt:81-96; "
    "workbench/ocr/paddle_ocr/下/part02/page_0231.txt:3-28"
)
SCOPE_START = '<h4 id="第五十六卷-第二章学校体育-第四节高校、中专学校体育">第四节高校、中专学校体育</h4>'
SCOPE_END = '<h3 id="第五十六卷-第三章运动项目">第三章运动项目</h3>'

NEW_HTML = """<p><strong>一、体育竞赛和体育设施</strong></p>
<p>民国3年（1914年），江苏省第八师范在灌云县板浦镇成立。该校设体育课，开展课外体育活动，校内定期举行运动会。课余时间，师范学生还和当时驻海州的盐务税警团官兵进行篮球比赛，体育活动较活跃。民国8年5月，在南京体育场举行江苏省立学校第五次联合运动会，江苏省第八师范学生王一五获跳远和110码跑第一名。民国9年4月，在南京体育场举行江苏省立学校第六次联合运动会，王一五又获跳远、100码和220码第一名，并获个人总分第一名。民国18年，赣榆县创建县立师范学校，配有专职体育教员，开设体育课。学校体育设施有篮球场、排球场、棒球场、网球场、足球场和乒乓球台，经常开展球类比赛。民国31年，伪淮海省在徐州举行运动会，东海师范郭化吉获学生男子组100米第一名，孙希桂获学生女子组400米和800米两项第一名，武可惠获学生女子组100米和200米两项第一名。</p>
<p>1963年，在市第四届中学生田径运动会上，海州师范获高中男子组第一名。</p>
<p>1981年，连云港化学矿业专科学校在江苏省高校徐州协作区乒乓球比赛中，获女子团体冠军。1984年，连云港化学矿业专科学校在省八届大学生田径赛上，获1500米、5000米、10000米三项第一名，并荣获“精神文明”队称号。1986年，连云港化学矿业专科学校在省高校徐州协作区篮球赛中，男、女队均获冠军。同年，海州师范参加全省中等师范学校首届田径运动会，获得甲组男、女团体总分第二名和乙组男子团体总分第二名。</p>
<p>1987年，淮海工学院体育教研室主任、副教授丁义美，带领5名学生长跑运动员，从新浦跑到徐州，路程200多公里。1988年，淮海工学院建成400米标准田径场，能够承担省级以上大型田径运动会比赛任务。</p>
<p>1989年，淮海工学院在江苏省苏北高校第一届田径运动会上，获男、女团体总分第三名。该校学生分别获得跳高和撑竿跳高第一名。该校在连云港市第八届田径运动会上，又获大、中专部男、女团体冠军。连云港师范获团体亚军。连云港职业大学建成400米标准田径场，并召开学校首届田径运动会。</p>
<p>1990年，在省十二届运动会高校甲组比赛中，省淮海工学院分别获得撑竿跳高和链球冠军。连云港化学矿业专科学校获高校乙组跳远第一名。连云港师范建成400米标准田径场，该校学生在市1990年元旦长跑比赛中获团体亚军、男子个人冠军。</p>
<p><strong>二、推行“劳卫制”</strong></p>
<p>1954年下半年，东海师范开展“劳卫制”预备级工作。1956年，开始推行“劳卫制”，学生积极参加。</p>
<p>1959年，市体委、市文教联合举办大、中学生运动会，比赛项目有篮球、排球、田径、体操、自行车等。</p>
<p>1960年底，各校根据上级规定，停止等级测验和大运动量活动，调整了体育课教学和课外活动。</p>
<p>1975年，推行《国家体育锻炼标准》，“劳卫制”活动终止。</p>
<p><strong>三、推行《国家体育锻炼标准》</strong></p>
<p>1975年开始，全市大、中专学校实施《国家体育锻炼标准》。连云港市化学矿业专科学校“达标”率1984～1989年分别是：92.45%、91.82%、93.50%、95.50%、93.70%、97.30%；海州师范学生“达标”率，每年均在97%以上，连云港师范学生“达标”率逐年上升，1990年已达97%。</p>"""

EXPECTED_TEXT = [
    "<p><strong>一、体育竞赛和体育设施</strong></p>",
    "王一五又获跳远、100码和220码第一名",
    "1987年，淮海工学院体育教研室主任",
    "淮海工学院建成400米标准田径场",
    "连云港职业大学建成400米标准田径场",
    "<p><strong>二、推行“劳卫制”</strong></p>",
    "<p><strong>三、推行《国家体育锻炼标准》</strong></p>",
    "连云港市化学矿业专科学校“达标”率1984～1989年分别是",
]
RESIDUALS = [
    "一、体育竞赛和体育设施民国3年",
    "220码第名",
    "准海工学院体育教研室",
    "1989年，准海工学院",
    "400米标田径场",
    "二、推行“劳卫制”1954年",
    "三、推行《国家体育锻炼标准》1975年",
    "专科学校达标”率",
    "1984~1989年",
    "施行学校应测适龄467643797855901生总数",
    "施行学校病残生数12(人)施行学校应测适龄",
    "占全市应测95.6193.1296.9096.0192.80适龄生总数",
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
        raise RuntimeError(f"sports college/secondary expected text missing: {missing}")
    remaining = [item for item in RESIDUALS if item in segment]
    if remaining:
        raise RuntimeError(f"sports college/secondary residue remains: {remaining}")
    return changed, {"rewrote_scope": changed, "removed_table_residue": changed}


def write_reports(changed: int, counts: dict[str, int]) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "第五十六卷体育 / 第二章学校体育 / 第四节高校、中专学校体育",
        "source": SOURCE_NOTE,
        "reader_path": str(HTML),
        "changes_this_run": changed,
        "counts": counts,
        "principle": "依据 PaddleOCR 页级文本重建高校、中专学校体育正文，修复小标题粘连、错识和表格残留。",
        "notes": [
            "表56-4、表56-45 已在当前结构化表 JSON 中有 verified 条目，但未嵌在本节正文当前位置；本脚本只移除混入正文的表格残行，不移动结构化表。",
            "表56-3 连云港市技工校推行《国家体育锻炼标准》发展人数统计表未在当前结构化表 JSON 中发现独立条目；本脚本不新增表格数据。",
        ],
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    md = f"""# 第五十六卷高校中专学校体育回源修复

- 时间：{now}
- 范围：`第五十六卷体育 / 第二章学校体育 / 第四节高校、中专学校体育`
- 源文依据：`{SOURCE_NOTE}`

## 修复动作

- 按页级 OCR 重建 `第四节高校、中专学校体育` 正文，拆分 `一、体育竞赛和体育设施`、`二、推行“劳卫制”`、`三、推行《国家体育锻炼标准》` 小标题。
- 修正 `220码第一名`、`淮海工学院`、`400米标准田径场`、`“达标”率` 等明确错识。
- 清除正文中残留的 `表56-45` 数字行；`表56-4`、`表56-45` 已在结构化表 JSON 中有 verified 条目，但未嵌在本节正文当前位置，本轮不移动结构化表。
- `表56-3 连云港市技工校推行《国家体育锻炼标准》发展人数统计表` 未在当前结构化表 JSON 中发现独立条目；本脚本不新增表格数据，留待表格核录流程处理。
- 首次运行已完成 1 处整段替换；稳定复跑新增整段替换：{changed} 处。
- 本轮未处理 `第三章运动项目`。

## 核对说明

- PaddleOCR `page_0230.txt` 确认第四节开头和民国时期段落。
- PaddleOCR `page_0231.txt` 确认 1986 年跨页尾句至 `三、推行《国家体育锻炼标准》` 末段，并给出 `表56-3` 表题边界。
"""
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")


def update_memory(changed: int) -> None:
    marker = "## 2026-07-03 第五十六卷高校中专学校体育回源修复"
    memory = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker in memory:
        return
    entry = f"""
{marker}

- 对第五十六卷体育第二章学校体育 `第四节高校、中专学校体育` 进行回源修复。
- 源文依据：`{SOURCE_NOTE}`；重建正文，拆分三个小标题，修正 `220码第一名`、`淮海工学院`、`400米标准田径场`、`“达标”率` 等明确错识。
- 清除正文中的 `表56-45` 数字行残留；`表56-4`、`表56-45` 已在结构化表 JSON 中有 verified 条目但未嵌在本节正文当前位置，本轮不移动结构化表。
- `表56-3 连云港市技工校推行《国家体育锻炼标准》发展人数统计表` 未在当前结构化表 JSON 中发现独立条目，本轮不新增表格数据，留待表格核录流程处理。
- 首次运行已完成 1 处整段替换；稳定复跑新增整段替换 {changed} 处；`第三章运动项目` 未在本脚本中处理。
- 报告：`output/reports/reader_readability_sports_college_secondary_section_20260703.md`。
"""
    MEMORY.write_text(memory.rstrip() + "\n\n" + entry.lstrip(), encoding="utf-8")


def main() -> None:
    changed, counts = patch_reader()
    write_reports(changed, counts)
    update_memory(changed)
    print("sports college/secondary section repaired")
    print(f"changes={changed}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()
