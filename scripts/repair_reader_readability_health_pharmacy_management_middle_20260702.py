# -*- coding: utf-8 -*-
"""Restore middle subsections of pharmacy administration from OCR."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_health_pharmacy_management_middle_20260702.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_health_pharmacy_management_middle_20260702.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260702_第五十五卷药政管理中段回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SOURCE_NOTE = (
    "workbench/body_chapters/连云港市志_全书_正文汇总.md:101210-101247; "
    "workbench/body_chapters/第五十二卷至第六十卷及附录（下part02）.md:7906-7943; "
    "workbench/ocr/paddle_ocr/下/part02/page_0198.txt:12-39; "
    "workbench/ocr/paddle_ocr/下/part02/page_0199.txt:3-18"
)
SCOPE_START = '<h4 id="第五十五卷-第四章医政 药政-第四节药政管理">第四节药政管理</h4>'
SCOPE_END_OPTIONS = ("<p>五、特殊药品管理", "<p><strong>五、特殊药品管理</strong></p>")

NEW_HTML = """<p><strong>三、药品经营质量管理</strong></p>
<p>民国18年（1929年），开始按国民政府公布的《管理药商规则》规定境内各药店须经东海县政府注册登记并领取营业执照后方能开业经营，各药店经营业务由东海县中医公会管理。建国前，各药店的行业管理由新成立的药业同业公会负责。新海连特区卫生局负责各药店的药品质量检查，并数次发出通知，责令各药店停止销售并销毁变质失效药品。</p>
<p>1951年，各药店由卫生行政部门登记颁发营业执照。1954年，市政府卫生科通知各药店，对安眠、镇静药品限量出售。</p>
<p>1957年1月，市公安局、卫生局联合发出《关于加强社会流动行医卖药人员管理的联合通知》，规定凡外地来境内卖药者，必须持有所在地人民政府发给的开业执照或市、县以上卫生行政部门发给的行医卖药证明文件，卖药地点由公安、卫生部门指定，所卖药品由卫生部门质量鉴定。1970年，市卫生局不定期对各药品经营单位检查。1985年，《中华人民共和国药品管理法》颁布后，对药品经营过程中质量管理逐步加强，按省卫生厅颁发的《核发药品经营企业许可证的条件》、《审查登记药工人员的条件》，对65家药品经营企业检查整顿，有45个药品经营单位取得《药品经营企业许可证》。1988年后，市卫生局每年对药品经营单位进行一次回访检查。</p>
<p><strong>四、医院用药管理</strong></p>
<p><strong>药房工作管理</strong></p>
<p>解放前，各医院无完整的药品调配及使用方面的管理制度。解放初，新海连特区专员公署卫生局督促各医院药房对药品的购进、贮存、发放、处方书写都有规定。</p>
<p>1954年，各医院开始执行江苏省卫生厅制订的《综合医院规章制度（草案）》。1958年，各医院的药房成为直接受院长领导的独立科室。1961年，贯彻执行国家卫生部的《关于医院药剂工作的若干规定》，药房开始执行“三查七对两交待”制度。1979年，按省卫生厅药剂工作规定，调整药房的组织结构，明确药房人员的职责及药品管理制度。1982年，各医院推行药剂科岗位责任制。1984年，各医院建立院药事管理委员会，药房管理工作达到制度化、规范化要求。1986年，乡级以上医院建立院药事管理委员会（小组）。市卫生局制订《连云港市县以上医院中药房整顿验收标准》，对各医院药房检查验收。1987年3月，市卫生局颁发《连云港市村卫生室药品管理规定》、《村卫生室基本用药品种目录》，对县以上医院药房管理、人员等方面检查。1989年，全市92所乡镇卫生院药房中有40个通过市卫生局检查验收，取得《药房合格证》。1990年，县级以上18个医院的药剂科已有7个通过江苏省卫生厅及市卫生局检查验收。93个乡镇卫生院中有84个通过验收，取得《药房合格证》。</p>
<p><strong>制剂管理</strong></p>
<p>建国初对市内医院制剂的管理仅限于一般质量要求。1964年，市卫生局针对市内各医院的制剂室设备普遍较差及制剂处方来源各异、配制方法不一、质量不高等情况，制订《连云港市医院药房制剂操作规程（试行本）》，各医院制剂室均按此操作规程中所列的87种内服药、74种外用药和17种注射剂的处方和配制操作规程进行配制作业及质量检验。1980年后，贯彻江苏省卫生厅颁布的《药政管理条例（试行）江苏省实施办法》，规定各医院制剂室所制药品只能供医院自己使用，不得对外销售，各公社卫生院及大队医疗站一律停止各种注射剂配制。1983年，市卫生局对各医院的制剂进行全面调查和登记，制发《连云港市医院制剂手册》，规定179种制剂的处方、操作规程和质量检验方法。</p>
<p>1984年，实行医院制剂报批制度。1985年，根据《中华人民共和国药品管理法》，对各医院制剂室核发《制剂许可证》。1987年，实行医院制剂注册登记制度。1988年，为适应医院制剂室改革工作的需要，放宽医院制剂的部分管理政策，市卫生局制订《医院制剂横向联合管理暂行办法》。</p>"""

EXPECTED_TEXT = [
    "<p><strong>三、药品经营质量管理</strong></p>",
    "领取营业执照后方能开业经营",
    "对65家药品经营企业检查整顿，有45个药品经营单位取得《药品经营企业许可证》",
    "<p><strong>四、医院用药管理</strong></p>",
    "<p><strong>药房工作管理</strong></p>",
    "<p><strong>制剂管理</strong></p>",
    "所制药品只能供医院自己使用",
]
RESIDUALS = [
    "三、药品经营质量管理民国18年",
    "并领营业执照后方能开业经营",
    "对65家药品经营企业对药品经营单位进行一次回访检查",
    "四、医院用药管理药房工作管理",
    "制剂管理建国初",
    "医院自已使用",
]


def find_scope(text: str) -> tuple[int, int]:
    base = text.index(SCOPE_START)
    start_markers = ("<p>三、药品经营质量管理", "<p><strong>三、药品经营质量管理</strong></p>")
    starts = [text.find(marker, base) for marker in start_markers]
    valid_starts = [start for start in starts if start != -1]
    if not valid_starts:
        raise RuntimeError("pharmacy management middle scope start not found")
    start = min(valid_starts)
    ends = [text.find(marker, start) for marker in SCOPE_END_OPTIONS]
    valid_ends = [end for end in ends if end != -1]
    if not valid_ends:
        raise RuntimeError("pharmacy management middle scope end not found")
    return start, min(valid_ends)


def patch_reader() -> tuple[int, dict[str, int]]:
    text = HTML.read_text(encoding="utf-8")
    start, end = find_scope(text)
    new_segment = NEW_HTML + "\n"
    changed = int(text[start:end] != new_segment)
    if changed:
        text = text[:start] + new_segment + text[end:]
        HTML.write_text(text, encoding="utf-8")

    text = HTML.read_text(encoding="utf-8")
    start, end = find_scope(text)
    segment = text[start:end]
    missing = [item for item in EXPECTED_TEXT if item not in segment]
    if missing:
        raise RuntimeError(f"pharmacy management middle expected text missing: {missing}")
    remaining = [item for item in RESIDUALS if item in segment]
    if remaining:
        raise RuntimeError(f"pharmacy management middle residue remains: {remaining}")
    return changed, {"rewrote_scope": changed}


def write_reports(changed: int, counts: dict[str, int]) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "第五十五卷卫生 / 第四章医政 药政 / 第四节药政管理 / 三、药品经营质量管理；四、医院用药管理",
        "source": SOURCE_NOTE,
        "reader_path": str(HTML),
        "changes_this_run": changed,
        "counts": counts,
        "principle": "依据 PaddleOCR 页级文本整体复原药政管理中段；未处理五、特殊药品管理。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    md = f"""# 第五十五卷药政管理中段回源修复

- 时间：{now}
- 范围：`第五十五卷卫生 / 第四章医政 药政 / 第四节药政管理 / 三、药品经营质量管理；四、医院用药管理`
- 源文依据：`{SOURCE_NOTE}`

## 修复动作

- 拆分 `三、药品经营质量管理`、`四、医院用药管理` 小节标题。
- 拆分 `药房工作管理`、`制剂管理` 分项标题。
- 复原 `领取营业执照`、`检查整顿，有45个药品经营单位取得...` 等漏损文字。
- 修正 `医院自已使用` 为 `医院自己使用`。
- 本次复跑新增整段替换：{changed} 处。
- 本轮未处理 `五、特殊药品管理`。

## 核对说明

- PaddleOCR `page_0198.txt` 确认 `药品经营质量管理`、`医院用药管理`、`药房工作管理` 及经营质量管理尾句。
- PaddleOCR `page_0199.txt` 确认药房工作管理跨页尾段、`制剂管理` 和 `五、特殊药品管理` 边界。
"""
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")


def update_memory(changed: int) -> None:
    marker = "## 2026-07-02 第五十五卷药政管理中段回源修复"
    memory = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker in memory:
        return
    entry = f"""
{marker}

- 对第五十五卷卫生第四章第四节 `药政管理` 的 `三、药品经营质量管理`、`四、医院用药管理` 进行回源修复。
- 源文依据：`{SOURCE_NOTE}`；拆分小节与分项标题，并按 OCR 复原经营质量管理和医院用药管理中段文字。
- 本轮新增整段替换 {changed} 处；`五、特殊药品管理` 未在本脚本中处理。
- 报告：`output/reports/reader_readability_health_pharmacy_management_middle_20260702.md`。
"""
    MEMORY.write_text(memory.rstrip() + "\n\n" + entry.lstrip(), encoding="utf-8")


def main() -> None:
    changed, counts = patch_reader()
    write_reports(changed, counts)
    update_memory(changed)
    print("pharmacy management middle repaired")
    print(f"changes={changed}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()
