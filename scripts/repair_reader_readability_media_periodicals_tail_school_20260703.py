# -*- coding: utf-8 -*-
"""Restore professional periodicals tail and school periodicals from page OCR."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_media_periodicals_tail_school_20260703.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_media_periodicals_tail_school_20260703.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260703_第五十四卷专业刊物尾段和校刊回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SOURCE_NOTE = "workbench/ocr/paddle_ocr/下/part02/page_0143.txt:12-33; page_0144.txt:3-20"
SCOPE_START = '<p>十、连云港工运1987年1月创刊，连云港市总工会主办。季刊，铅印，16开本，50页。主编邓元伦。</p>'
STABLE_SCOPE_START = '<p>十、连云港工运</p>'
SCOPE_END = '<p>1951年7月1日，新海连市收音站成立。翌年5月1日改为有线广播宣传站。</p>'

NEW_HTML = """<p>十、连云港工运</p>
<p>1987年1月创刊，连云港市总工会主办。季刊，铅印，16开本，50页。主编邓元伦。江苏省内部报刊准印证号为（JS）第3223号。每期印4000册。连云港报社印刷厂印刷。</p>
<p>《连云港工运》传达上级工会指示，交流工会工作经验，反映职工呼声，为基层工会服务。刊物发至市各基层工会和国内有关单位交流。</p>
<p>十一、连云港团讯</p>
<p>1987年7月创刊，共青团连云港市委员会主办。双月刊，铅印，32开本，50页。主编杨东新。江苏省内部报刊准印证号为（JS）第3254号。每期印100册。连云港报社印刷厂印刷。</p>
<p>《连云港团讯》辟有“团的工作”、“支部生活”、“团干论坛”、“调查与研究”、“信息博览”、“体育看台”等栏目。</p>
<p>十二、开放·经济·管理</p>
<p>1987年创刊，中共连云港市委政策研究室主办。铅印，双月刊，16开本，64页。主编郭守常。江苏省内部报刊准印证号为（JS）第3227号。每期发行5000册。连云港报社印刷厂印刷。</p>
<h4 id="第五十四卷-第二章刊物-第三节校刊">第三节校刊</h4>
<p>一、教学与研究</p>
<p>1985年1月创刊，原名《连云港教育学院学报》。连云港教育学院主办。铅印，16开本，100页。一年出版3期（2期文科、1期理科），每期印1000册。主编沈伟民。江苏省内部报刊准印证号为（JS）第3224号。赣榆县中学印刷厂印刷。1988年改刊名为《教学与研究》。</p>
<p>《教学与研究》发表连云港教育学院教师的科研文章，同时面向全市中学教师。</p>
<p>二、高等教育研究</p>
<p>1987年创刊，连云港化工矿业专科学校高教研究室主办。半年刊，16开本，70页。主编汪银生。江苏省内部报刊准印证号为（JS）第3228号。每期印1000册。连云港报社印刷厂印刷。</p>
<p>《高等教育研究》辟有“专科教育研究”、“教学研究”、“专业方向探讨”、“高教研究文摘”以及“译文”等栏目。</p>
<p>三、连云港职业大学学报</p>
<p>1988年8月创刊，时称《高教研究》，连云港职业大学主办。半年刊，铅印，16开，100页。主编王万侠。每期印300册。江苏省内部报刊准印证号为（JS）第3229号。1990年12月更名为《连云港职业大学学报》。</p>
<p>四、连云港党校学刊</p>
<p>1989年7月创刊，中共连云港市委党校主办。季刊，16开本，48页，铅印。主编郑遵武。江苏省内部报刊准印证号为（JS）第3468号。每期印1000册。连云港市机关印刷厂印刷。</p>
<p>《连云港党校学刊》结合社会主义建设的实际，从理论到实践上对社会科学进行研究探索。辟有“学习论坛”、“探索与争鸣”、“经济研究”、“领导科学”、“中国文化研究”、“调查报告”、“改革纵横”、“海边拾贝”等栏目。</p>



"""

EXPECTED_TEXT = [
    "<p>十、连云港工运</p>",
    "江苏省内部报刊准印证号为（JS）第3223号",
    "<p>十二、开放·经济·管理</p>",
    "<p>一、教学与研究</p>",
    "原名《连云港教育学院学报》",
    "更名为《连云港职业大学学报》",
    "“学习论坛”、“探索与争鸣”",
]
RESIDUALS = [
    "十、连云港工运1987年1月创刊",
    "十一、连云港团讯1987年7月创刊",
    "十二、开放·经济·管理1987年创刊",
    "一、教学与研究1985年1月创刊",
    "原名《连云港教育学院学报。",
    "二、高等教育研究1987年创刊",
    "三、连云港职业大学学报1988年8月创刊",
    "更名为连云港职业大学学报）",
    "四、连云港党校学刊1989年7月创刊",
    "“学习论坛”“探索与争鸣”",
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
    start, end = find_scope(text)
    segment = text[start:end]
    missing = [item for item in EXPECTED_TEXT if item not in segment]
    if missing:
        raise RuntimeError(f"expected text missing: {missing}")
    remaining = [item for item in RESIDUALS if item in segment]
    if remaining:
        raise RuntimeError(f"residue remains: {remaining}")
    return changed, {"rewrote_scope": changed, "entries_restored": 7}


def write_reports(changed: int, counts: dict[str, int]) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "第五十四卷报刊广播电视 / 第二章刊物 / 专业刊物尾段与校刊",
        "source": SOURCE_NOTE,
        "reader_path": str(HTML),
        "changes_this_run": changed,
        "counts": counts,
        "principle": "依据 PaddleOCR 页级文本重建专业刊物十至十二及校刊一至四，停止在广播章概述残段前。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    md = f"""# 第五十四卷专业刊物尾段和校刊回源修复

- 时间：{now}
- 范围：`第五十四卷报刊广播电视 / 第二章刊物 / 专业刊物尾段与校刊`
- 源文依据：`{SOURCE_NOTE}`

## 修复动作

- 按页级 OCR 重建专业刊物十至十二及校刊一至四，停止在后续广播章概述残段前。
- 拆开条目题名与正文粘连，修正 `连云港教育学院学报`、`连云港职业大学学报`、`学习论坛` 栏目顿号等明确内容。
- 当前核验复跑整段替换：{changed} 处。

## 注意

- 本次未处理后续 `表54-3` / 广播章之间疑似缺失或错位内容，后续需单独核对。
"""
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")


def update_memory(changed: int) -> None:
    marker = "## 2026-07-03 第五十四卷专业刊物尾段和校刊回源修复"
    memory = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker in memory:
        return
    entry = f"""
{marker}

- 对第五十四卷报刊广播电视 `第二章刊物 / 专业刊物尾段与校刊` 进行回源修复。
- 源文依据：`{SOURCE_NOTE}`；重建专业刊物十至十二及校刊一至四，停止在后续广播章概述残段前。
- 修正条目题名粘连、`连云港教育学院学报` 书名号残缺、`连云港职业大学学报` 更名句残缺、`学习论坛` 栏目顿号漏失等问题。
- 注意：后续 `表54-3` / 广播章之间疑似缺失或错位内容尚需单独核对。
- 当前核验复跑整段替换 {changed} 处。
- 报告：`output/reports/reader_readability_media_periodicals_tail_school_20260703.md`。
"""
    MEMORY.write_text(memory.rstrip() + "\n\n" + entry.lstrip(), encoding="utf-8")


def main() -> None:
    changed, counts = patch_reader()
    write_reports(changed, counts)
    update_memory(changed)
    print(json.dumps({"changed": changed, "counts": counts}, ensure_ascii=False))


if __name__ == "__main__":
    main()
