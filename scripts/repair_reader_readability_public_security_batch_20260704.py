# -*- coding: utf-8 -*-
"""Repair source-verified OCR slips in Volume 44 public security and justice."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_public_security_batch_20260704.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_public_security_batch_20260704.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260704_第四十四卷治安司法高置信错识回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SCOPE_START = '<h2 id="第四十四卷-治安司法">第四十四卷治安司法</h2>'
SCOPE_END = '<h2 id="第四十五卷-军事">第四十五卷军事</h2>'
SOURCE = (
    "workbench/ocr/paddle_ocr/下/part01/page_0062.txt; page_0066.txt; "
    "page_0068.txt; page_0071.txt; page_0072.txt; page_0073.txt; "
    "page_0074.txt; page_0079.txt; page_0082.txt; page_0084.txt; "
    "page_0085.txt; page_0086.txt; page_0089.txt; page_0097.txt; "
    "page_0098.txt; page_0099.txt; page_0101.txt; page_0102.txt; "
    "page_0108.txt; page_0110.txt; page_0111.txt; page_0117.txt; "
    "page_0138.txt"
)

REPLACEMENTS = [
    ("概述强奸", "打击流窜、盗窃、流氓、强好等各类犯罪", "打击流窜、盗窃、流氓、强奸等各类犯罪", "page_0062.txt:32"),
    ("反动党团逮捕", "藏枪事，速捕后交出长枪73支", "藏枪事，逮捕后交出长枪73支", "page_0066.txt:26"),
    ("会道门依法逮捕", "依法速捕一批从事反革命破坏活动的道首", "依法逮捕一批从事反革命破坏活动的道首", "page_0068.txt:21"),
    ("会道门海州道首", "依法速捕海州一贯道道首6人", "依法逮捕海州一贯道道首6人", "page_0068.txt:22"),
    ("会道门道首", "市公安局速捕一贯道道首5人", "市公安局逮捕一贯道道首5人", "page_0068.txt:22-23"),
    ("会道门东海道首", "共速捕道首35人", "共逮捕道首35人", "page_0068.txt:24-25"),
    ("会道门1953", "市公安局速捕一贯道道首9人", "市公安局逮捕一贯道道首9人", "page_0068.txt:25-26"),
    ("会道门玄修门", "速捕玄修门门首1人", "逮捕玄修门门首1人", "page_0068.txt:26"),
    ("文物档案编目入库", "登记、鉴定、编自、人库、使用和调拨", "登记、鉴定、编目、入库、使用和调拨", "page_0071.txt:12-13"),
    ("文物清理入库", "文物集中清理人库", "文物集中清理入库", "page_0071.txt:14"),
    ("文物出入库", "文物出人库登记", "文物出入库登记", "page_0071.txt:25-26"),
    ("重大事故逮捕一", "火灾事故直接责任者依法速捕", "火灾事故直接责任者依法逮捕", "page_0072.txt:27-28"),
    ("重大事故逮捕二", "主要责任者被依法速捕", "主要责任者被依法逮捕", "page_0072.txt:31-32"),
    ("殷某", "反革命分子般某，杀害", "反革命分子殷某，杀害", "page_0072.txt:35-36"),
    ("抢劫案件错字", "1989年，全市共发生抢动案件104起", "1989年，全市共发生抢劫案件104起", "page_0073.txt:33; context section is 抢劫案件"),
    ("捅死", "持刀将其捕死，抢走现金", "持刀将其捅死，抢走现金", "page_0073.txt:36"),
    ("未逞", "两次行刺厉某未后潜逃", "两次行刺厉某未逞后潜逃", "page_0073.txt:37"),
    ("拦路强奸", "拦路强，案发后", "拦路强奸，案发后", "page_0074.txt:15"),
    ("罪犯逮捕归案", "将罪犯速捕归案", "将罪犯逮捕归案", "page_0074.txt:15-16"),
    ("强奸1984", "1984年，全市共发生强好案件111起", "1984年，全市共发生强奸案件111起", "page_0074.txt:20"),
    ("强奸1987", "1987~1989年，全市共发生强好案件308起", "1987~1989年，全市共发生强奸案件308起", "page_0074.txt:23"),
    ("强奸1990", "全市共发生强案件154起", "全市共发生强奸案件154起", "page_0074.txt:25"),
    ("重大强奸1990", "特别重大强好案件发生4起", "特别重大强奸案件发生4起", "page_0074.txt:25-26"),
    ("暂住人口纳入", "纳人暂住人口管理", "纳入暂住人口管理", "page_0079.txt:16"),
    ("公共场所纳入", "公共场所纳人特种行业管理", "公共场所纳入特种行业管理", "page_0082.txt:16"),
    ("特种行业隐患", "发现隐惠1170处", "发现隐患1170处", "page_0082.txt:5"),
    ("禁赌逮捕", "速捕15人，劳动教养16人", "逮捕15人，劳动教养16人", "page_0084.txt:7-8"),
    ("封建迷信逮捕", "首犯李某被市公安局依法速捕", "首犯李某被市公安局依法逮捕", "page_0085.txt:21-22"),
    ("拐卖人口逮捕", "依法速捕。7月18日", "依法逮捕。7月18日", "page_0086.txt:7-8"),
    ("自行车纳入", "自行车纳人户口管理", "自行车纳入户口管理", "page_0089.txt:6"),
    ("预审逮捕开头", "市区公安机关速捕人犯须经检察机关批准，速捕、拘留、搜查人犯", "市区公安机关逮捕人犯须经检察机关批准，逮捕、拘留、搜查人犯", "page_0097.txt:6-7"),
    ("预审顾某", "受理顾某拦路强案中", "受理顾某拦路强奸案中", "page_0097.txt:28"),
    ("预审供述", "顾犯补充交代拦路强、抢劫作案", "顾犯补充交代拦路强奸、抢劫作案", "page_0097.txt:30"),
    ("上半年受理逮捕", "上半年受理速捕、拘留案件", "上半年受理逮捕、拘留案件", "page_0097.txt:33"),
    ("受理逮捕案犯", "全市公安机关受理速捕案犯审结率", "全市公安机关受理逮捕案犯审结率", "page_0097.txt:39-40"),
    ("查破逮捕", "查破刑事案件45起，速捕犯罪分子17人", "查破刑事案件45起，逮捕犯罪分子17人", "page_0098.txt:2"),
    ("看守所隐患", "查出事故隐惠987起", "查出事故隐患987起", "page_0099.txt:9"),
    ("批准逮捕决定一", "再作批准速捕决定", "再作批准逮捕决定", "page_0101.txt:30"),
    ("不批准逮捕一", "不批准速捕的决定", "不批准逮捕的决定", "page_0102.txt:15"),
    ("批准逮捕决定二", "批准速捕或不批准逮捕", "批准逮捕或不批准逮捕", "page_0102.txt:16"),
    ("法纪强奸", "破坏山林2件、强好2件", "破坏山林2件、强奸2件", "page_0108.txt:39-40"),
    ("监所隐患", "发现有隐惠，及时建议和协助监管场所消除隐惠", "发现有隐患，及时建议和协助监管场所消除隐患", "page_0110.txt:37"),
    ("控申逮捕", "速捕反革命犯2人、强奸犯1人、贪污犯1人", "逮捕反革命犯2人、强奸犯1人、贪污犯1人", "page_0111.txt:30-31"),
    ("审结杀人", "每年审结杀案件均未超过5件", "每年审结杀人案件均未超过5件", "page_0117.txt:8"),
    ("法院补逮捕证", "法院补速捕证26件", "法院补逮捕证26件", "page_0138.txt:16"),
]

SKIPPED = [
    "`速捕` 在其它卷和人物传中仍有残留，本批仅修第四十四卷且能回源确认为 `逮捕` 的语境。",
    "表44-6 火灾统计表的压平行暂不重建，需另走结构化表/页图专项。",
]


def find_scope(text: str) -> tuple[int, int]:
    start = text.index(SCOPE_START)
    end = text.index(SCOPE_END, start)
    return start, end


def patch_reader() -> dict[str, int]:
    text = HTML.read_text(encoding="utf-8")
    start, end = find_scope(text)
    original = text[start:end]
    segment = original
    counts: dict[str, int] = {}
    for label, old, new, _source in REPLACEMENTS:
        count = segment.count(old)
        if count:
            segment = segment.replace(old, new)
        elif new not in segment:
            raise RuntimeError(f"neither old nor new text found: {label}")
        counts[label] = count
    if segment != original:
        HTML.write_text(text[:start] + segment + text[end:], encoding="utf-8")
    verify_reader()
    return counts


def verify_reader() -> None:
    text = HTML.read_text(encoding="utf-8")
    start, end = find_scope(text)
    segment = text[start:end]
    missing = [new for _label, _old, new, _source in REPLACEMENTS if new not in segment]
    residuals = [old for _label, old, new, _source in REPLACEMENTS if old in segment and old not in new]
    if missing or residuals:
        raise RuntimeError(f"verification failed: missing={missing}, residuals={residuals}")


def upsert_memory(path: Path, marker: str, content: str) -> None:
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker not in old:
        path.write_text(old.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")
        return
    start = old.index(marker)
    next_start = old.find("\n## ", start + 1)
    replacement = content.strip()
    if next_start == -1:
        new = old[:start].rstrip() + "\n\n" + replacement + "\n"
    else:
        new = old[:start].rstrip() + "\n\n" + replacement + "\n\n" + old[next_start:].lstrip()
    path.write_text(new, encoding="utf-8")


def write_reports(counts: dict[str, int]) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    items = [
        {"label": label, "old": old, "new": new, "source": source, "count": counts[label]}
        for label, old, new, source in REPLACEMENTS
    ]
    payload = {
        "time": now,
        "scope": "第四十四卷治安司法",
        "source": SOURCE,
        "reader_path": str(HTML),
        "verified_items": len(REPLACEMENTS),
        "current_run_replacements": sum(counts.values()),
        "items": items,
        "skipped": SKIPPED,
        "principle": "仅修复页级 OCR 或强上下文可支持的第四十四卷短错识，不重建表格残段。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# 第四十四卷治安司法高置信错识回源修复",
        "",
        f"- 时间：{now}",
        f"- 范围：{payload['scope']}",
        f"- 源文：`{SOURCE}`",
        f"- 阅读器：`{HTML}`",
        f"- 本批核验修复：{payload['verified_items']} 项",
        f"- 本次脚本复跑实际改写：{payload['current_run_replacements']} 处",
        "- 重点：修正 `强好/强/拦路强` 为强奸语境，`速捕/依法速捕` 为逮捕语境，`编自/人库/纳人/隐惠` 等短错识。",
        "- 保留：火灾统计表压平残段和证据不足的表格问题，后续按结构化表专项处理。",
        "",
    ]
    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")
    PROGRESS.write_text("\n".join(lines), encoding="utf-8")
    memory = f"""
## 2026-07-04 第四十四卷治安司法高置信错识回源修复

- 对第四十四卷治安司法进行小范围回源修复，范围限定在 `第四十四卷-治安司法` 到 `第四十五卷-军事` 前。
- 源文依据：`{SOURCE}`。
- 修复示例：`强好/强/拦路强`→`强奸/拦路强奸`，`速捕/依法速捕`→`逮捕/依法逮捕`，`编自、人库`→`编目、入库`，`纳人`→`纳入`，`隐惠`→`隐患`，`审结杀案件`→`审结杀人案件`。
- 本批核验修复 {len(REPLACEMENTS)} 项；火灾统计表压平残段暂留给结构化表/页图专项。
- 报告：`output/reports/reader_readability_public_security_batch_20260704.md`。
"""
    upsert_memory(MEMORY, "## 2026-07-04 第四十四卷治安司法高置信错识回源修复", memory)


def main() -> None:
    counts = patch_reader()
    write_reports(counts)
    print(json.dumps({"current_run_replacements": sum(counts.values()), "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
