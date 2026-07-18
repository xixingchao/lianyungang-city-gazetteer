# -*- coding: utf-8 -*-
"""Restore sports primary school section from page OCR."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_sports_primary_section_20260703.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_sports_primary_section_20260703.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260703_第五十六卷小学体育回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SOURCE_NOTE = (
    "workbench/ocr/paddle_ocr/下/part02/page_0225.txt:30-40; "
    "workbench/ocr/paddle_ocr/下/part02/page_0226.txt:3-40; "
    "workbench/ocr/paddle_ocr/下/part02/page_0227.txt:3-15"
)
SCOPE_START = '<h4 id="第五十六卷-第二章学校体育-第二节小学体育">第二节小学体育</h4>'
SCOPE_END = '<h4 id="第五十六卷-第二章学校体育-第三节中学体育">第三节中学体育</h4>'

NEW_HTML = """<p><strong>一、体育教学和活动</strong></p>
<p>民国2年（1913年），在新浦创办国民小学一所，民国3年招生开学，开设课程除国语、算术、社会常识等课程外，还开设体育和音乐课程。民国25年，国民政府规定小学体育训练项目，高年级：跳远、跳高、短跑、远足、投掷、球类、礼仪训练，团体操；中年级：远足、快走、球类、礼仪训练、团体操；低年级：郊游、游戏、礼仪训练。境内各小学由于师资、设施和人民生活困苦等原因，很少有学校按规定训练项目进行活动。上体育课时，一般是简单队列操练、赛跑、游戏、打球等；课余活动时，做游戏或打球。有时也举办运动会或进行郊游。</p>
<p>建国后，小学体育课每周两节，主要内容为简单的队列操练和游戏等，早晨做早操，下午开展课外活动。各校逐步添置了体育器材。</p>
<p>1954年，国家体委推行第一套少年广播体操，全市各小学立即组织实施。1956年，国家教育部颁布《小学体育教学大纲》（草案），市文教科于10月举办小学体育教师训练班进行学习。市区6个班以上的完全小学下半年试行了《小学体育教学大纲》（草案）。</p>
<p>“文化大革命”期间，小学体育教学和活动遭到干扰和破坏。</p>
<p>1979年，全市各小学贯彻执行国家教育部等部门制定的《中、小学体育工作暂行规定》（草案）、《中、小学卫生工作暂行规定》（草案）和省制定的《小学体育教学基本要求》，加强对体育工作的领导，注重体育经费投入。各小学都能坚持“两课”、“两操”、“两活动”，保证学生每天有一小时体育锻炼时间，并把体育活动情况作为评定“三好”学生和先进集体重要条件之一。还开展体育教学评估活动，促进了体育教学和改革的深入发展。1986～1990年，市共举办小学田径运动会10次，单项体育竞赛约30次。三县四区每年也举办小学生田径运动会和单项体育竞赛。</p>
<p><strong>二、推行《国家体育锻炼标准》</strong></p>
<p>1978年后，在学校中推行《国家体育锻炼标准》，开展“达标”活动。全市有5所小学先行一步。1979年，全市小学中“达标”数为2241人（其中少年二组73人，少年一组187人，儿童组1981人）。1980年，市体委、市教育局发出《关于进一步推行国家体育锻炼标准的意见》，市每学年举办一次“达标”运动会。1981年，全市开展“达标”活动的小学占小学总数的25.8%，“达标”人数占应测适龄生29.5%，超过省规定指标，名列全省第二。1983年，赣榆、东海、灌云三县划归连云港市管辖，全市小学“达标”人数为93358人（及格级48605人，良好级38036人，优秀级6717人）。1985～1990年，全市小学“达标”率一直名列全省第一。</p>
<p><strong>三、体育传统项目学校建设</strong></p>
<p>20世纪60年代以后，全市一部分小学在群众性体育活动的基础上，形成自己的体育传统项目。</p>
<p>1979年12月，市体委、市教委联合拟定了《中小学校开展体育重点项目试行条例》，要求各校重视开展体育重点项目。1982年，有部分小学开展体育传统项目活动，1983年，开始命名体育传统项目学校。同年，全市小学有体育传统项目学校46所。1984年，东海县牛山小学男子队参加全国重点省、市小学篮球赛，获第四名，先后6次被评为江苏省先进集体。</p>
<p>1985年，市体育传统项目学校田径赛，灌云县实验小学获小学男子组第一名，东海县工农兵小学获小学女子组第一名。同年，市“萌芽杯”足球赛，海头湾小学男女足球队均获冠军，该校被评为江苏省1985年体育传统项目学校先进集体。1986年，市体育传统项目学校球类比赛，市墟沟小学获女子足球赛冠军，东海县牛山小学获男子篮球赛冠军。同年，市解放路小学、市墟沟小学、东海县牛山小学被评为江苏省1986年体育传统项目学校先进集体。</p>
<p>东海县牛山小学是省级篮球传统项目学校，二年级以上班级成立小篮球队，队员达150人，占全校学生数的25%。至1990年，参加地、市级比赛5次，男队获冠军3次，亚军2次，女队获冠军3次，亚军1次。参加省级比赛7次，男队获冠军5次，女队获冠军1次，亚军3次。又被国家教育部、国家体委评为全国体育传统项目学校先进集体。</p>
<p>1990年，全市被批准命名为省级体育传统项目学校8所，即：连云港市解放路小学（田径、篮球），连云港市墟沟小学（足球），海州师范附属小学（足球、田径），东海县实验小学（田径、乒乓球），东海县牛山小学（篮球），东海县工农兵小学（田径），东海县白塔小学（篮球）；灌云县实验小学（田径、篮球）。被批准命名为市级体育传统项目学校13所，即：连云港市盐坨小学（田径），连云港市海头湾小学（足球），连云港市临海路小学（篮球），连云港市砚台小学（排球），连云港市通灌路小学（田径），连云港市建国路小学（篮球），连云港市民主小学（排球），赣榆县实验小学（田径），赣榆县海头小学（篮球），赣榆县青口小学（篮球），东海县房山小学（田径），东海县桃林小学（田径、篮球），灌云县苏光小学（田径）。</p>"""

EXPECTED_TEXT = [
    "<p><strong>一、体育教学和活动</strong></p>",
    "1954年，国家体委推行第一套少年广播体操",
    "《小学体育教学大纲》（草案）",
    "《小学体育教学基本要求》",
    "注重体育经费投入",
    "<p><strong>二、推行《国家体育锻炼标准》</strong></p>",
    "“达标”人数占应测适龄生29.5%",
    "<p><strong>三、体育传统项目学校建设</strong></p>",
    "形成自己的体育传统项目",
    "1985年，市体育传统项目学校田径赛",
    "队员达150人",
    "女队获冠军3次，亚军1次",
    "赣榆县实验小学（田径），赣榆县海头小学（篮球）",
]
RESIDUALS = [
    "一、体育教学和活动民国2年",
    "<p>家教育部颁布《小学体育教学大纲》",
    "《小学体育教学大纲》草案）",
    "《小学体育教学基本要求）",
    "经费投人",
    "二、推行《国家体育锻炼标准》1978年",
    "三、体育传统项目学校建设20世纪",
    "自已的体育传统项目",
    "<p>工农兵小学获小学女子组第一名。同年",
    "队员达: 2511150人",
    "冠军3.次",
    "获冠军 5次",
    "占全市应测99.3098.5798.7997.4395.94适龄生总数",
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
        raise RuntimeError(f"sports primary expected text missing: {missing}")
    remaining = [item for item in RESIDUALS if item in segment]
    if remaining:
        raise RuntimeError(f"sports primary residue remains: {remaining}")
    return changed, {"rewrote_scope": changed, "removed_table_residue": changed}


def write_reports(changed: int, counts: dict[str, int]) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "第五十六卷体育 / 第二章学校体育 / 第二节小学体育",
        "source": SOURCE_NOTE,
        "reader_path": str(HTML),
        "changes_this_run": changed,
        "initial_run_rewrote_scope": True,
        "counts": counts,
        "principle": "依据 PaddleOCR 页级文本重建小学体育正文，修复小标题粘连、跨页漏句、页眉串入和表格残留。",
        "notes": [
            "表56-1 连云港市小学推行《国家体育锻炼标准》发展人数统计表在当前结构化表 JSON 中未发现独立条目；本脚本只移除混入正文的表格尾行残留，不新增表格数据。",
            "赣榆县实验小学与赣榆县海头小学之间按同句学校名单并列结构补入顿读逗号。",
        ],
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    md = f"""# 第五十六卷小学体育回源修复

- 时间：{now}
- 范围：`第五十六卷体育 / 第二章学校体育 / 第二节小学体育`
- 源文依据：`{SOURCE_NOTE}`

## 修复动作

- 按页级 OCR 重建 `第二节小学体育` 正文，拆分 `一、体育教学和活动`、`二、推行《国家体育锻炼标准》`、`三、体育传统项目学校建设` 小标题。
- 补回 1954 年和 1956 年段落开头，修正 `《小学体育教学大纲》（草案）`、`《小学体育教学基本要求》`、`经费投入`、`自己的体育传统项目`。
- 补回 1985 年体育传统项目学校田径赛段首，清除 `2511` 页眉串入造成的 `队员达: 2511150人`，恢复为 `队员达150人`。
- 清除正文中残留的 `占全市应测99.30...适龄生总数（%）` 表格尾行。
- `表56-1 连云港市小学推行《国家体育锻炼标准》发展人数统计表` 在当前结构化表 JSON 中未发现独立条目；本脚本不新增表格数据，后续如走表格核录流程再处理。
- 首次运行已完成 1 处整段替换；稳定复跑新增整段替换：{changed} 处。
- 本轮未处理 `第三节中学体育`。

## 核对说明

- PaddleOCR `page_0225.txt` 确认第二节开头至建国后段落。
- PaddleOCR `page_0226.txt` 确认 1954 年至 1986～1990 年段落、`二` 与 `三` 小标题及体育传统项目学校建设前段。
- PaddleOCR `page_0227.txt` 确认 `队员达150人`、省级/市级体育传统项目学校名单，并给出 `表56-1` 表题边界。
"""
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")


def update_memory(changed: int) -> None:
    marker = "## 2026-07-03 第五十六卷小学体育回源修复"
    memory = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker in memory:
        return
    entry = f"""
{marker}

- 对第五十六卷体育第二章学校体育 `第二节小学体育` 进行回源修复。
- 源文依据：`{SOURCE_NOTE}`；重建正文，拆分三个小标题，补回 1954/1956 年段首和 1985 年段首，修正 `《小学体育教学大纲》（草案）`、`《小学体育教学基本要求》`、`经费投入`、`自己的体育传统项目`。
- 清除 `2511` 页眉串入造成的 `队员达: 2511150人`，恢复为 `队员达150人`；移除正文中的 `表56-1` 尾行残留。
- `表56-1 连云港市小学推行《国家体育锻炼标准》发展人数统计表` 未在当前结构化表 JSON 中发现独立条目，本轮不新增表格数据，留待表格核录流程处理。
- 首次运行已完成 1 处整段替换；稳定复跑新增整段替换 {changed} 处；`第三节中学体育` 未在本脚本中处理。
- 报告：`output/reports/reader_readability_sports_primary_section_20260703.md`。
"""
    MEMORY.write_text(memory.rstrip() + "\n\n" + entry.lstrip(), encoding="utf-8")


def main() -> None:
    changed, counts = patch_reader()
    write_reports(changed, counts)
    update_memory(changed)
    print("sports primary section repaired")
    print(f"changes={changed}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()
