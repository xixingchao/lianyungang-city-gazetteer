# -*- coding: utf-8 -*-
"""Restore Jiangsu Salt Industry News entry from page OCR."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_media_industry_jiangsu_salt_20260703.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_media_industry_jiangsu_salt_20260703.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260703_第五十四卷江苏盐业报回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SOURCE_NOTE = "workbench/ocr/paddle_ocr/下/part02/page_0135.txt:72-87; page_0136.txt:3-31"
SCOPE_START = '<p>一、江苏盐业报民国37年（1948年）4月5日创刊，原名《盐场大众》，由中共两准盐场特区委员会（简称盐特委)于陈家港创办。'
STABLE_SCOPE_START = '<p>一、江苏盐业报</p>'
SCOPE_END = '<p>二、连云港卫生创刊于1975年，市卫生防疫站和市爱国卫生运动委员会办公室主办，负责人厉章定。</p>'

NEW_HTML = """<p>一、江苏盐业报</p>
<p>民国37年（1948年）4月5日创刊，原名《盐场大众》，由中共两淮盐场特区委员会（简称盐特委）于陈家港创办。这是一份面向干部群众的通俗性小报，一头毛驴、两块石板，几乎是报社的全部家当。八开四版，周二刊，石印。盐特委宣传部部长朱士俊兼主编，后由许战夫任主编。</p>
<p>《盐场大众》创刊初期，盐特委、盐务局的主要领导经常为报纸撰稿。报纸的主要内容：一是形势教育，连续报道东北、华北、西北大捷，特别是收复延安的胜利消息，全盐场群情振奋，用增产、多销原盐的实际行动庆祝胜利。此外，经常披露敌占区盐民受迫害情况，提高群众的思想觉悟，搞好生产支援前线。二是进行群众观点、群众路线教育，增强干部全心全意为人民服务的思想。三是交流盐业生产、运销经验，促进生产发展，加强运销管理工作。民国37年（1948年）7月，人民解放军撤出陈家港，出了30期的《盐场大众》停刊。1949年11月1日《盐场大众》复刊，为中共淮北盐特委机关报。八开四版，铅印，五日刊，公开发行（经华东邮政登记认为第一类新闻纸类、山东省邮政管理局执照第十二号）。</p>
<p>社址设在新浦。中共华东局宣传部部长舒同为报纸题写了报头。盐特委宣传部长王正萍兼任党报委员会主任、报社社长。采编人员多为华中新闻专科学校调来的一批毕业生和已撤销的新华社淮北盐场支社的部分干部。</p>
<p>1953年5月1日，《盐场大众》更名为《淮北盐工报》。舒同第二次题写报名。四开四版、周二刊。总编刘政。报社设四组一室：地方新闻组、时政组、文化生活组、群众工作组和资料室，采编人员20人，淮北盐务管理局所属各盐场均设通讯干事。鉴于解放初期广大盐工文化水平不高的状况，报社推行大众化的办报方针，力求通俗化、口语化，文艺副刊多刊登盐工们喜闻乐见的大鼓词、说唱材料。报社十分重视通联工作和群众工作，来信来稿篇篇有回复、件件有着落。1958年以前，新海连地区无报，《淮北盐工报》担负部分综合性报纸的任务，政治、经济、时事、文化内容兼有。市内的重大活动，《淮北盐工报》派记者采访报道。</p>
<p>1958年12月，淮北盐场机构调整，《淮北盐工报》停刊。新海连市盐务局办内部发行的《新海连盐业》，八开二版、周二刊，隶属局宣传部。负责人金同俭。</p>
<p>1962年1月，《新海连盐业》更名为《盐场情况》，隶属于局办公室，铅印，十日刊，八开二版。</p>
<p>1964年7月30日，《盐场情况》更名为《淮北盐场报》，铅印、周刊、八开二版，有时出四版。</p>
<p>1967年1月27日，《淮北盐场报》停刊。1969年11月，淮北盐务管理局实行军管，1970年出版油印的《盐场情况》。</p>
<p>1974年6月，《淮北盐工报》复刊。八开四版，铅印，十日刊。1976年，成立编辑室，赵广全和于少泉任副主任。四开四版，周刊。报头原为黑体字，后采用拼集的郭沫若手书。</p>
<p>1984年1月，经中共江苏省委宣传部批准，《淮北盐工报》公开发行，成立《淮北盐工报》社。赵广全任总编。</p>
<p>1986年5月5日，《淮北盐工报》更名为《江苏盐业报》。中共江苏省盐业公司委员会主办。舒同第三次题写报名。是年7月1日，恢复了周二刊，四开四版，铅印。国内统一刊号CN32-0039，是目前国内盐业系统唯一公开发行的报纸。总编孙荣章。1988年初，张效良任总编。1988年8月，于少泉任总编。报社设采访部、编辑部、通联部、印刷厂。</p>
<p>《江苏盐业报》继承发扬了老一辈新闻工作者的光荣传统，坚持党的基本路线，遵守新闻纪律，做好通联工作。1988年，在全国大型企业报理论研讨会上，《江苏盐业报》提出将企业报办成开放型报纸。1988～1989年度的全国轻工记协好新闻评选中，《江苏盐业报》获奖等级及获奖数，均为123家企业报中的第一名。</p>
"""

EXPECTED_TEXT = [
    "一、江苏盐业报</p>",
    "中共两淮盐场特区委员会",
    "受迫害情况",
    "新华社淮北盐场支社",
    "《淮北盐工报》担负部分综合性报纸",
    "1962年1月，《新海连盐业》更名为《盐场情况》",
    "《淮北盐场报》停刊",
    "《淮北盐工报》复刊",
    "1988～1989年度",
]
RESIDUALS = [
    "一、江苏盐业报民国37年",
    "两准盐场特区委员会",
    "简称盐特委)",
    "受追害情况",
    "新华社北盐场支社",
    "《准北盐工报》",
    "准北盐务管理局",
    "<p>二版。</p>",
    "《准北盐场报》停刊",
    "。淮北盐工报》复刊",
    "19881989年度",
]


def find_scope(text: str) -> tuple[int, int]:
    start = text.find(STABLE_SCOPE_START)
    if start < 0:
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
    start, end = text.index(NEW_HTML), text.index(SCOPE_END, text.index(NEW_HTML))
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
        "scope": "第五十四卷报刊广播电视 / 第一章报纸 / 第二节行(专)业报纸 / 一、江苏盐业报",
        "source": SOURCE_NOTE,
        "reader_path": str(HTML),
        "changes_this_run": changed,
        "counts": counts,
        "principle": "依据 PaddleOCR 页级文本重建江苏盐业报条目，停止在二、连云港卫生前。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    md = f"""# 第五十四卷江苏盐业报回源修复

- 时间：{now}
- 范围：`第五十四卷报刊广播电视 / 第一章报纸 / 第二节行(专)业报纸 / 一、江苏盐业报`
- 源文依据：`{SOURCE_NOTE}`

## 修复动作

- 按页级 OCR 重建 `一、江苏盐业报`，停止在 `二、连云港卫生` 前。
- 拆开条目题名与正文粘连，修正 `两淮盐场特区委员会`、`受迫害情况`、`新华社淮北盐场支社`、`淮北盐工报`、`淮北盐务管理局`、`淮北盐场报` 等源页明确内容。
- 补回漏失的 `1962年1月，《新海连盐业》更名为《盐场情况》...` 段，修正 `1988～1989年度` 年份连接。
- 当前核验复跑整段替换：{changed} 处。

## 核对说明

- 本次只处理 `一、江苏盐业报`，后续 `二、连云港卫生` 及以下行业报纸条目另行核对。
"""
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")


def update_memory(changed: int) -> None:
    marker = "## 2026-07-03 第五十四卷江苏盐业报回源修复"
    memory = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker in memory:
        return
    entry = f"""
{marker}

- 对第五十四卷报刊广播电视 `第一章报纸 / 第二节行(专)业报纸 / 一、江苏盐业报` 进行回源修复。
- 源文依据：`{SOURCE_NOTE}`；重建至 `二、连云港卫生` 前，未触碰后续行业报纸条目。
- 修正题名粘连、`两淮盐场特区委员会`、`受迫害情况`、`新华社淮北盐场支社`、`淮北盐工报/淮北盐务管理局/淮北盐场报` 等问题，补回 `1962年1月《新海连盐业》更名为《盐场情况》` 段。
- 当前核验复跑整段替换 {changed} 处。
- 报告：`output/reports/reader_readability_media_industry_jiangsu_salt_20260703.md`。
"""
    MEMORY.write_text(memory.rstrip() + "\n\n" + entry.lstrip(), encoding="utf-8")


def main() -> None:
    changed, counts = patch_reader()
    write_reports(changed, counts)
    update_memory(changed)
    print(json.dumps({"changed": changed, "counts": counts}, ensure_ascii=False))


if __name__ == "__main__":
    main()
