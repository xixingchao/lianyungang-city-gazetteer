# -*- coding: utf-8 -*-
"""Restore sports farmer section from page OCR."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_sports_farmer_section_20260703.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_sports_farmer_section_20260703.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260703_第五十六卷农民体育回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SOURCE_NOTE = (
    "workbench/ocr/paddle_ocr/下/part02/page_0221.txt:14-40; "
    "workbench/ocr/paddle_ocr/下/part02/page_0222.txt:3-26"
)
SCOPE_START = '<h4 id="第五十六卷-第一章社会体育-第三节农民体育">第三节农民体育</h4>'
SCOPE_END = '<h4 id="第五十六卷-第一章社会体育-第四节老年人体育">第四节老年人体育</h4>'

NEW_HTML = """<p>连云港市的农民体育起步较晚。1953年，在全市农村结合民兵训练，利用农闲季节开展篮球、武术、长跑等体育活动。1956年，赣榆县召开第一届农民体育运动会，有200名运动员参赛。1956年和1958年，东海县举办了两届农民运动会。</p>
<p>1958年，赣榆县人民委员会派专人到农村组织开展广播操、武术、球类等活动。东辛农场职工利用节假日举办球类和拔河比赛，职工广播操出勤率达85%。灌云县龙苴公司被评为“全国农村体育运动红旗”单位，省体委于12月在龙苴公司召开农村体育工作现场会。同年，该公社派员参加全国农村体育经济交流会。市体委在农村重点试行“劳卫制”，是年，通过“劳卫制”的有156人。</p>
<p>1959年1月1日，新海连市第一届农（渔）民体育运动会在新浦举行。215名运动员参赛。同年1月11～28日，徐州专区第一届农民体育运动会徐州市举行，新海连市组织77名运动员参赛，赣榆县农民代表队获得团体总分第二名。同年，共青团灌云县龙苴乡委员会被评为“江苏省农村体育先进单位”，并出席第二次全国青年社会主义积极分子大会全国文教群英会。</p>
<p>1965年，农村结合民兵训练，组织开展投掷、拔河等活动和民间体育传统项目运动。12月5～12日，市举办农民篮球赛。</p>
<p>1970年，赣榆县农村相继开展游泳、摔跤、武术、棋类、拔河、球类等项活动。1972年春节，市体委举办农民篮球和拔河比赛。1975年5月1日，海州区洪门大队举办第一届农民运动会，进行田径、篮球和拔河比赛，有500人参赛，其中年龄最大的60岁，最小的10岁。1976年，市体委训练农村体育干部60人、裁判员40人。全市农村有体育代表队100人，队员1500人，开基层运动会4次，洪门大队召开第二届农村运动会。1977年，农村有50%青年参加1～2项体育活动，各公社、农场组织1～2个业余代表队，共成立97个篮球队。同年，市体委与市农委举行农民篮球赛，有18个男、女队对赛，新浦农场获得男、女队冠军。1979年，锦屏、朝阳、宿城公社建立农民体育协会，有兼职体育干部7人，建立射击、篮球、长跑等业余体育队40个，队员450人。各公社、农场还组织一些锻炼小组，坚持常年活动。1978年和1979年，在省中长跑比赛中，洪门大队运动员王增兵、范永贵分别获得5000米和10000米第一名。</p>
<p>1980年，洪门大队、高公岛公社被评为市体育先进单位。1983年，全市有82个乡建立文化站，开展文化、体育活动。东海县白塔埠和洪庄两个乡开展武术和游泳活动，灌云县龙苴乡60%的人经常参加体育活动，赣榆县大岭乡双城大队自筹经费2万元开展文体活动。1月27至2月2日，市举办1983年“青农杯”男子篮球赛，新浦农场获得冠军。</p>
<p>1985年，赣榆、东海、灌云3县积极开展争创“全国体育先进县、乡镇”活动。赣榆县举办农民运动会，东海县浦南乡把体育工作列入“五好”家庭、文明村、校评比条件。在1985年江苏省县级田径赛中，东海县获得连云港赛区团体总分第二名。同年，在东海县兴办的农民运动会上，14个乡镇、400多名运动员对赛，浦南乡获得男子篮球和田径总分第一名。</p>
<p>1986年，灌云县被省体委命名为“江苏省体育先进县”，并接受全国体育先进县检查组验收。灌云县龙苴大队运动员代表市参加省农民乒乓球赛，获团体奖；代表市参加省农民篮球赛，获“精神文明队”称号。东海县24个乡镇利用节假日举办乡镇农民运动会。东海县浦南乡被命名为“江苏省体育先进乡”，并派代表出席在北京举行的全国农民运动会。1986～1987年，东海县举办两届农民篮球赛，有10个乡镇男、女代表队参赛。东海县白塔埠镇女子篮球队两次代表市参加省“丰收杯”篮球赛，均获第二名。</p>
<p>1988年，灌云县被国家体委命名为“全国体育先进县”。云台区花果山乡农民代表队在市农民田径运动会上获得团体总分第一名，在市“农民杯”乒乓球比赛中，获团体冠军。1989～1990年，连云区院前村篮球队两次获市农民篮球赛冠军。</p>
<p>1990年，云台区花果山乡被命名为“江苏省体育先进乡”。</p>
<p>至1990年，东海县农民篮球队曾6次参加地（市）级比赛，男队获冠军1次，亚军3次；女队获冠军3次。</p>"""

EXPECTED_TEXT = [
    "赣榆县召开第一届农民体育运动会",
    "球类和拔河比赛",
    "“全国农村体育运动红旗”单位，省体委于12月在龙苴公司召开农村体育工作现场会",
    "共青团灌云县龙苴乡委员会",
    "开展游泳、摔跤、武术",
    "建立射击、篮球、长跑等业余体育队40个",
    "获得5000米和10000米第一名",
    "灌云县龙苴乡60%的人经常参加体育活动",
    "列入“五好”家庭、文明村、校评比条件。在1985年江苏省县级田径赛中",
    "1986～1987年，东海县举办两届农民篮球赛",
    "云台区花果山乡被命名为“江苏省体育先进乡”",
]
RESIDUALS = [
    "第届农民体育运动会",
    "球类和拨河比赛",
    "全国农村体育运动红旗单位",
    "龙公司召开",
    "龙乡委员会",
    "摔、武术",
    "射击、得篮球",
    "第～名",
    "灌云县龙乡60%",
    "列入五好”",
    "在1985年：",
    "19861987年",
    "命名为江苏省体育先进乡”",
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
        raise RuntimeError(f"sports farmer expected text missing: {missing}")
    remaining = [item for item in RESIDUALS if item in segment]
    if remaining:
        raise RuntimeError(f"sports farmer residue remains: {remaining}")
    return changed, {"rewrote_scope": changed}


def write_reports(changed: int, counts: dict[str, int]) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "第五十六卷体育 / 第一章社会体育 / 第三节农民体育",
        "source": SOURCE_NOTE,
        "reader_path": str(HTML),
        "changes_this_run": changed,
        "counts": counts,
        "principle": "依据 PaddleOCR 页级文本重建农民体育整节，修复错识、漏引号和跨页断裂。",
        "notes": [
            "保留 OCR 可见但语义待复核的“全国农村体育经济交流会”和“徐州市举行”表述。",
            "“射击、得篮球、长跑”按项目并列上下文校正为“射击、篮球、长跑”。",
        ],
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    md = f"""# 第五十六卷农民体育回源修复

- 时间：{now}
- 范围：`第五十六卷体育 / 第一章社会体育 / 第三节农民体育`
- 源文依据：`{SOURCE_NOTE}`

## 修复动作

- 按页级 OCR 重建 `第三节农民体育` 整节。
- 修正 `第一届农民体育运动会`、`拔河`、`全国农村体育运动红旗` 引号、`龙苴公司`、`龙苴乡`、`摔跤`、`第一名`、`1986～1987年`、`江苏省体育先进乡` 等错识和断裂。
- 将 `射击、得篮球、长跑` 按项目并列上下文校正为 `射击、篮球、长跑`。
- 保留 OCR 可见但仍可后续复核的 `全国农村体育经济交流会` 与 `徐州市举行` 表述。
- 本次复跑新增整段替换：{changed} 处。
- 本轮未处理 `第四节老年人体育`。

## 核对说明

- PaddleOCR `page_0221.txt` 确认第三节开头至 1979 年段。
- PaddleOCR `page_0222.txt` 确认 1979 年跨页尾句至 1990 年段，并给出第四节边界。
"""
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")


def update_memory(changed: int) -> None:
    marker = "## 2026-07-03 第五十六卷农民体育回源修复"
    memory = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker in memory:
        return
    entry = f"""
{marker}

- 对第五十六卷体育第一章社会体育 `第三节农民体育` 进行回源修复。
- 源文依据：`{SOURCE_NOTE}`；重建整节，修正 `第一届农民体育运动会`、`拔河`、`全国农村体育运动红旗` 引号、`龙苴公司`、`龙苴乡`、`摔跤`、`第一名`、`1986～1987年`、`江苏省体育先进乡` 等错识和断裂。
- `射击、得篮球、长跑` 按项目并列上下文校正为 `射击、篮球、长跑`；`全国农村体育经济交流会`、`徐州市举行` 保留 OCR 可见表述，后续如有更高置信源再复核。
- 本轮新增整段替换 {changed} 处；`第四节老年人体育` 未在本脚本中处理。
- 报告：`output/reports/reader_readability_sports_farmer_section_20260703.md`。
"""
    MEMORY.write_text(memory.rstrip() + "\n\n" + entry.lstrip(), encoding="utf-8")


def main() -> None:
    changed, counts = patch_reader()
    write_reports(changed, counts)
    update_memory(changed)
    print("sports farmer section repaired")
    print(f"changes={changed}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()
