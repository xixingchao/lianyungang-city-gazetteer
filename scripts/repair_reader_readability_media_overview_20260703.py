# -*- coding: utf-8 -*-
"""Restore volume 54 overview from page OCR."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_media_overview_20260703.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_media_overview_20260703.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260703_第五十四卷概述回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SOURCE_NOTE = "workbench/ocr/paddle_ocr/下/part02/page_0125.txt:5-31; page_0126.txt:3-39; page_0127.txt:3-9"
SCOPE_START = '<h3 id="第五十四卷-概述">概述</h3>'
SCOPE_END = '<h3 id="第五十四卷-第一章报纸">第一章报纸</h3>'

NEW_HTML = """<h3 id="第五十四卷-概述">概述</h3>
<p>连云港市报刊业始于20世纪20年代中期，广播业起步于40年代末，电视业始于70年代初。</p>
<p>民国15年（1926年）12月创办的《共进周刊》是连云港市最早的刊物。民国18年，连云港第一张报纸《东海民报》在海州问世。该报主笔陈嗣衡撰文揭露驻军独立第四旅旅长谭曙卿的劣迹，在“冷箭”专栏上发表。东海县总工会常委张劲枢和陈嗣衡竟被谭枪杀，报纸旋即停刊。惨案发生后震惊全国，《申报》、《新闻报》、《中央日报》纷纷披露，被称为“海报事件”。</p>
<p>民国23年（1934年），《飞轮》创办。这是一份由中共地下组织——“社联”主席陈兆明主办的文艺刊物。它公开提出文艺的战斗性，宣传无产阶级文艺思想。陈兆明等地下党员因“赤嫌”被捕。《飞轮》办了五期，于当年底停刊。</p>
<p>20世纪30年代，连云港先后办有8种报纸、1种刊物。这些报刊的办报（刊）宗旨虽然各不相同，但受时局的影响，都旗帜鲜明地宣传抗日。民国27年（1938年）创办的《抗日导报》是由赣榆县县长朱爱周邀请由共产党人组建的县政府政训处主办。在《纪念“九·一八”七周年》专刊上，发表共产党员和爱国青年的文章，论述抗战必胜的道理。《抗日导报》当时被誉为赣榆县国共两党携手抗日的一面旗帜。</p>
<p>连云港沦陷期间，报刊事业萎缩萧条，只有一张伪办《海州日报》，宣扬奴化思想。</p>
<p>抗日战争胜利后，连云港报业有所复苏，先后办有6种报纸。这些报纸全用中央通讯社消息，多数旨在宣传国民党的政策、法令，有的攻击共产党，作歪曲事实的宣传。</p>
<p>连云港解放后，市区一度无地方报纸。民国37年（1948年）4月中共两淮盐场特区委员会创办《盐场大众》。虽然这是一张企业报纸，但在当时却担负着综合性报纸的任务，市区重大活动都有采访报道。连云港解放初期，境内设有两个新华社支社：一个是新华社淮北盐场支社，隶属于新华社华中分社；一个是新华社新海连支社，隶属于新华社鲁中南分社。1956年9月，《新华日报》在新海连市设记者站。这个时期的报纸、通讯社、记者站，宣传中国共产党的政策，人民政府的法令，以及各项政治活动，巩固人民民主专政，促进地方国民经济的恢复和发展。</p>
<p>1958年3月，中共新海连市委员会创办《新海连市报》（后改为《新海连日报》、《连云日报》、《连云港报》）。“文化大革命”期间，《连云日报》一度改为电讯版，1972年9月奉命停刊，自此，连云港6年多无地方报纸。1979年3月，《连云港报》复刊，为中共连云港市委机关报。以后，连云港新创办的报刊有：《苏盐科技》、《科技汇报》、《国外化工矿山动态》、《连云港文学》、《连云港港报》、《连云港广播电视报》以及《情报指挥控制系统与仿真技术》等。从民国37年11月到1990年底，连云港创办的全国发行报纸8种，刊物5种，设立通讯社2家，记者站28家，报刊的期发行量远远超过解放前各报刊的期发行量。</p>
<p>建国后40多年间，连云港的报刊宣传党的理论、方针、政策；传播科学文化知识，丰富人民群众生活，反映全市各条战线斗争的实践和成果。1958～1960年，《连云日报》由于受“大跃进”的影响，一度宣传过“浮夸风”和“共产风”。“文化大革命”前期，《连云日报》在“以阶级斗争为纲”的理论指导下，宣传了“左”的错误思想。中共十一届三中全会以后，连云港的报刊在坚持四项基本原则的基础上，不断改革报刊的编排，充实报刊的内容，采用先进的印刷技术，质量不断提高。</p>
<p>民国38年（1949年）3月，灌云县广播收音站成立，连云港开始有广播宣传。1951年7月新海连市收音站成立（后改为连云港市有线广播站）。开播时只有1台电唱机，7只高音喇叭，以转播中央人民广播电台和山东人民广播电台的节目为主。1958年后，先后在海州、朝阳、连云港、猴嘴建立4个广播站，各自单独转播中央台的节目。1964年又先后在海州、锦屏、新坝、云台、朝阳、中云、云山、墟沟、连云港、猴嘴等地建立广播放大站，使市区的55个生产大队、303个生产队通了广播。1966年6月至1969年9月，因“文化大革命”的影响，有线广播遭到严重破坏，广播网基本处于瘫痪状态。1969年9月以后，重建有线广播网，至1972年6月，市区有15个区、镇、公社建立广播站和放大站。1990年，市区所有乡镇建立了广播站，形成了以市广播站为中心的城乡有线广播网。广播节目以自办为主，广播时间每天达11小时35分。1959年5月，新海连市人民广播电台（后改为连云港市人民广播电台）成立，架设57米高的木杆发射天线。1971年6月在海拔15米的孔望山建成发射台，架设83米高的发射天线一副。1978年11月建成中波发射台。1990年，全市无线广播节目以自办为主，覆盖人口312.36万，覆盖率达91.8%，播音时间每天达13小时50分。1985年6月连云港调频台建成开播，至1990年覆盖率达100%。至此，连云港形成了转播与播发、一套调频与三套中波广播的规模。</p>
<p>1970年，连云港人民广播电台组建电视收测组，1971年10月试转山东电视台节目。1983年8月转播江苏电视台节目。1985年5月连云港电视台成立，开始自办电视节目。至1990年，全市电视覆盖率达100%，电视节目从开始转播二个频道增为四个频道，每周播放的时间为33小时56分，逐步完善电视摄像、录像、编辑系统，能够摄制和播放各类自办节目。至此，连云港形成有线与无线广播并举，广播与电视兼具的声像传播系统。</p>
<p>1977年9月，连云港市广播事业局成立，1983年10月改为连云港市广播电视局。</p>
<p>1990年底，市广播电视局及所属单位共有职工228人，其中工程技术人员34人，采编播及录制人员54人。</p>
<p>各县的广播电视事业也相应发展。至1990年底，广播喇叭总数为61.3万只，喇叭平均入户率为70%，广播专线达5858杆公里。东海县于1981年12月建成县电视差转台，转播市电视台节目，1986年1月开始电视摄像采访，1987年成立县电视转播台，1988年底电视覆盖半径为25公里。</p>
"""

EXPECTED_TEXT = [
    "<p>连云港市报刊业始于20世纪20年代中期",
    "陈嗣衡竟被谭枪杀",
    "中共地下组织——“社联”",
    "新华社淮北盐场支社",
    "1956年9月，《新华日报》在新海连市设记者站",
    "《连云港文学》、《连云港港报》、《连云港广播电视报》以及《情报指挥控制系统与仿真技术》",
    "架设83米高的发射天线一副",
    "东海县于1981年12月建成县电视差转台",
]
RESIDUALS = [
    "报刊连云港市报刊业",
    "竟竞被谭枪杀",
    "中共地下组织一—“社联”",
    "新华社准北盐场支社",
    "新华日报>",
    "国外化工矿山动态》、等",
    "发射天线副",
    "<东海民报",
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
        "scope": "第五十四卷报刊广播电视 / 概述",
        "source": SOURCE_NOTE,
        "reader_path": str(HTML),
        "changes_this_run": changed,
        "counts": counts,
        "principle": "依据 PaddleOCR 页级文本重建第五十四卷概述，停止在第一章报纸前。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    md = f"""# 第五十四卷概述回源修复

- 时间：{now}
- 范围：`第五十四卷报刊广播电视 / 概述`
- 源文依据：`{SOURCE_NOTE}`

## 修复动作

- 按页级 OCR 重建 `概述`，停止在 `第一章报纸` 前。
- 删除卷名残留造成的 `报刊连云港...` 正文粘连。
- 修正 `竟竞被谭枪杀`、`新华日报>`、`准北盐场支社`、`发射天线副`、报刊名缺失等源页明确错误。
- 移出误串入概述末尾的 `第一章报纸` 开章文字，保留其后正式章节锚点不变。
- 当前核验复跑整段替换：{changed} 处。

## 核对说明

- 本次只处理 `概述`，`第一章报纸 / 第一节综合报纸` 仍需后续单独回源核对。
"""
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")


def update_memory(changed: int) -> None:
    marker = "## 2026-07-03 第五十四卷概述回源修复"
    memory = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker in memory:
        return
    entry = f"""
{marker}

- 对第五十四卷报刊广播电视 `概述` 进行回源修复。
- 源文依据：`{SOURCE_NOTE}`；重建至 `第一章报纸` 前，未触碰第一节综合报纸正文。
- 修正 `报刊连云港...` 粘连、`竟竞被谭枪杀`、`新华日报>`、`准北盐场支社`、`发射天线副`、报刊名缺失等源页明确问题，并移出误串入概述末尾的第一章开章文字。
- 当前核验复跑整段替换 {changed} 处。
- 报告：`output/reports/reader_readability_media_overview_20260703.md`。
"""
    MEMORY.write_text(memory.rstrip() + "\n\n" + entry.lstrip(), encoding="utf-8")


def main() -> None:
    changed, counts = patch_reader()
    write_reports(changed, counts)
    update_memory(changed)
    print(json.dumps({"changed": changed, "counts": counts}, ensure_ascii=False))


if __name__ == "__main__":
    main()
