# -*- coding: utf-8 -*-
"""Restore professional periodicals entries 1-9 from page OCR."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_media_professional_periodicals_01_09_20260703.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_media_professional_periodicals_01_09_20260703.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260703_第五十四卷专业刊物一至九回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SOURCE_NOTE = "workbench/ocr/paddle_ocr/下/part02/page_0141.txt:15-36; page_0142.txt:3-34; page_0143.txt:3-11"
SCOPE_START = '<h4 id="第五十四卷-第二章刊物-第二节专业刊物">第二节专业刊物</h4>'
SCOPE_END = '<p>十、连云港工运1987年1月创刊，连云港市总工会主办。季刊，铅印，16开本，50页。主编邓元伦。</p>'

NEW_HTML = """<h4 id="第五十四卷-第二章刊物-第二节专业刊物">第二节专业刊物</h4>
<p>一、情报指挥控制系统与仿真技术</p>
<p>1965年创办。中国船舶总公司第七研究院第七一六研究所主办。公开发行。</p>
<p>二、化工矿山技术</p>
<p>1973年创办。化工部化工矿山设计院主办。公开发行。</p>
<p>三、苏盐科技</p>
<p>1974年9月创刊，江苏省盐业公司主管。季刊，16开本，铅印。自办发行，期发行量1200份。国内统一刊号CN32-1252。主编沈敏。</p>
<p>《苏盐科技》的前身为《淮盐科技通讯》。主办单位为江苏省海盐科技情报中心站和江苏生产建设兵团淮北盐务管理局科学研究所。负责人杨锦涛。</p>
<p>1979年11月开始，主办单位增加了江苏省轻工学会盐业分会。1980年3月17～19日，省海盐科技情报中心站召开江苏省海盐科技情报工作座谈会，会上成立《淮盐科技通讯》编委会，主任委员徐汉。</p>
<p>1983年开始，主办单位改为淮北盐务管理局科学技术协会和江苏省海盐科技情报中心站。</p>
<p>1984年12月，经江苏省科学技术委员会批准，《淮盐科技通讯》为省级自然科学期刊。</p>
<p>1987年，《淮盐科技通讯》更名为《苏盐科技》。主办单位为江苏省海盐科技情报中心站。</p>
<p>该刊旨在振兴江苏盐业，主要介绍海水制盐、井矿盐生产、盐化工业、水产养殖、经营管理等方面的科技成果，传播先进技术、科技信息，交流学术研究论文，提供科技情报。刊物设“专论与综述”、“祖国盐业”、“制盐技术”、“企业管理”、“盐化战线”、“水产养殖”等栏目。</p>
<p>四、国外化工矿山动态</p>
<p>1974年创刊，化工部矿山科技情报中心站主办。16开本，每期10页，铅印。主编蔡领权、顾词。江苏省内部报刊准印证号为（JS）第3448号。每年出版18期。每期印1000份。化工部矿山设计研究院印刷厂印刷。</p>
<p>该刊介绍国外化学矿山生产建设、科学技术动态、科学管理知识等，为国内有关领导和科技人员组织进出口化学矿产品提供参考资料。</p>
<p>五、化工矿山通讯</p>
<p>1979年6月创刊，化工部化工矿山科技情报中心站主办。月刊，16开本，16页。主编方华曙。江苏省内部报刊准印证号为（JS）第3447号。每期印2000份。化工部化工矿山设计研究院印刷厂印刷。办公地址设在新浦幸福路18号。</p>
<p>《化工矿山通讯》报道化工矿山方面国内外科技情报和研究成果等。</p>
<p>六、连云港论坛</p>
<p>1979年12月创刊，连云港市哲学社会科学联合会主办。季刊，铅印，16开本，60页，主编王其泰。前身为《研究》，1986年年初更名《连云港论坛》。江苏省内部报刊准印证号为（JS）第3226号。每期印2000份，灌南县印刷厂印刷，由连云港报社发行部代办发行。</p>
<p>《连云港论坛》发表政治、社科、历史、教育、法律等基本理论的研究成果；本市经济、科技、社会发展战略方面的研究文章；以及市内名山、名水、名人、名作等乡土教材。截至1990年，发表论文550篇，240万多字。市财政每年拨给经费2万元。</p>
<p>七、现代企业管理</p>
<p>1983年4月创刊，连云港市企业管理协会、企业家协会主办。季刊，铅印，16开本，48页。主编赵治中。江苏省内部报刊准印证号为（JS）第3225号。每期印2300册。在市机关印刷厂印刷。</p>
<p>《现代企业管理》介绍企业现代化管理方法、先进经验。</p>
<p>八、连云港财会</p>
<p>1985年9月创刊，连云港市财政局、连云港市会计学会、连云港市珠算协会主办。季刊，16开本，50页。主编盛子荣、汪洪元。江苏省内部报刊准印证号为（JS）第3253号。每期印1400册。赣榆县中学印刷厂印刷。社址设在新浦海昌路南首。</p>
<p>《连云港财会》宣传国家和省有关财会工作的方针政策，介绍市财政、会计、税务、审计、珠算等基本理论研究成果，交流财产管理、会计核算方面的论文和调查报告。辟有“专论”、“财政论述”、“会计研究”、“珠算天地”、“财政法规”、“审计论坛”、“财经文摘”、“业务与技术”、“简讯”等栏目。</p>
<p>九、连云港宣传</p>
<p>创刊于1986年，中共连云港市委宣传部主办。月刊，32开本，40页，铅印。主编张殿臣。江苏省内部报刊准印证号为（JS）第3222号。彩色胶印封面，每期印数7900份。赣榆县中学印刷厂印刷。连云港报社发行部代办发行。</p>
<p>《连云港宣传》传达中共中央有关指示精神、引导社会舆论，交流国内和本市的宣传思想工作的经验、信息，为基层宣传干部、党务工作者提供学习参考资料。</p>
<p>《连云港宣传》辟有“中央领导近期言论”、“编辑部吹风”、“宣传论坛”、“形势教育”、“党课教育”、“理论之窗”、“经验交流”等栏目。</p>
"""

EXPECTED_TEXT = [
    "<p>一、情报指挥控制系统与仿真技术</p>",
    "《淮盐科技通讯》编委会",
    "淮北盐务管理局科学技术协会",
    "刊物设“专论与综述”",
    "<p>四、国外化工矿山动态</p>",
    "江苏省内部报刊准印证号为（JS）第3448号",
    "<p>五、化工矿山通讯</p>",
    "江苏省内部报刊准印证号为（JS）第3447号",
    "<p>九、连云港宣传</p>",
    "基层宣传干部、党务工作者",
    "“中央领导近期言论”、“编辑部吹风”",
]
RESIDUALS = [
    "情报指挥控制系统与仿真技术1965年创办",
    "化工矿山技术1973年创办",
    "苏盐科技1974年9月创刊",
    "《准盐科技通讯",
    "科技通讯>",
    "改为北盐务管理局",
    "刊，，，，，目",
    "国外化工矿山动态1974年创刊",
    "准印证号（JS）第3447号",
    "现代企业管理1983年4月创刊",
    "印刷广印刷",
    "连云港财会1985年9月创刊",
    "“专论”“财政论述”",
    "连云港宣传创刊于1986年",
    "宣传于部",
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
    return changed, {"rewrote_scope": changed, "entries_restored": 9}


def write_reports(changed: int, counts: dict[str, int]) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "第五十四卷报刊广播电视 / 第二章刊物 / 第二节专业刊物 / 一至九",
        "source": SOURCE_NOTE,
        "reader_path": str(HTML),
        "changes_this_run": changed,
        "counts": counts,
        "principle": "依据 PaddleOCR 页级文本重建专业刊物一至九，停止在十、连云港工运前。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    md = f"""# 第五十四卷专业刊物一至九回源修复

- 时间：{now}
- 范围：`第五十四卷报刊广播电视 / 第二章刊物 / 第二节专业刊物 / 一至九`
- 源文依据：`{SOURCE_NOTE}`

## 修复动作

- 按页级 OCR 重建专业刊物一至九，停止在 `十、连云港工运` 前。
- 拆开条目题名与正文粘连，修正 `淮盐科技通讯`、`淮北盐务管理局`、栏目列表、准印证号和印刷厂等源页明确内容。
- 修正 `宣传干部`、`中央领导近期言论` 等被误识别或漏失的文字。
- 当前核验复跑整段替换：{changed} 处。
"""
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")


def update_memory(changed: int) -> None:
    marker = "## 2026-07-03 第五十四卷专业刊物一至九回源修复"
    memory = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker in memory:
        return
    entry = f"""
{marker}

- 对第五十四卷报刊广播电视 `第二章刊物 / 第二节专业刊物 / 一至九` 进行回源修复。
- 源文依据：`{SOURCE_NOTE}`；重建至 `十、连云港工运` 前。
- 修正条目题名粘连、`淮盐科技通讯` 被误作 `准盐科技通讯`、`淮北盐务管理局` 缺字、栏目整行塌陷、`印刷厂`、`宣传干部` 等问题。
- 当前核验复跑整段替换 {changed} 处。
- 报告：`output/reports/reader_readability_media_professional_periodicals_01_09_20260703.md`。
"""
    MEMORY.write_text(memory.rstrip() + "\n\n" + entry.lstrip(), encoding="utf-8")


def main() -> None:
    changed, counts = patch_reader()
    write_reports(changed, counts)
    update_memory(changed)
    print(json.dumps({"changed": changed, "counts": counts}, ensure_ascii=False))


if __name__ == "__main__":
    main()
