# -*- coding: utf-8 -*-
"""Restore wired broadcast city network section from page OCR."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_broadcast_wired_city_20260703.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_broadcast_wired_city_20260703.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260703_第五十四卷有线广播市区广播网回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SOURCE_NOTE = "workbench/ocr/paddle_ocr/下/part02/page_0145.txt:82-84; page_0146.txt:3-30"
SCOPE_START = '<p>一、市区广播网1951年7月1日，山东省新海连市收音站成立。'
STABLE_SCOPE_START = '<p>一、市区广播网</p>'
SCOPE_END = '<p>建站初期，全县广播信号主要通过电话线路传送。到1957年自架广播线路135杆公里，广播喇叭1000只。</p>'
NEXT_AFTER_SCOPE = '<p>1958年，广播站使用县发电厂交流电源，增加了一台500瓦扩大机和两台磁带录音机。'

NEW_HTML = """<p>一、市区广播网</p>
<p>1951年7月1日，山东省新海连市收音站成立。1952年5月1日在新浦民主路市文化馆建立山东省新海连市有线广播宣传站，只有1间房子、1部扩音机、1只话筒、1部电唱机，工作人员3人。在民主路的电灯杆上装了7只10～25瓦的高音喇叭，转播中央人民广播电台、省人民广播电台的节目，每天播音4～5小时。</p>
<p>1953年，随行政区划调整改名为江苏省新海连市广播宣传站。</p>
<p>1957年在新浦民主路上安装了第一批舌簧小喇叭，共57只，每天广播两次，4小时。</p>
<p>1958年先后在海州、朝阳、连云港、猴嘴等地区的文化馆（站）内建立了4个有线广播站，各配备一名兼职人员。装置50瓦扩大机4部，有20多公里广播线路，安装喇叭1870只，因广播线路还没有和市站连通，所以各自单独转播和自办，平均每天播音4小时。</p>
<p>1959年初，市广播宣传站迁至民主路210号，全天播音10小时20分钟，其中自办节目4小时，转播中央台和省台节目6小时20分钟。</p>
<p>1961年8月，新海连市有线广播站改名为连云港市有线广播站。每天播音8小时，其中自办节目3小时，转中央台、省台节目4个半小时。</p>
<p>1963年春，从新浦到海州用竹杆和木杆架设了一条6公里长的广播专线，接通了第一条信号线，为连云港市广播网连网的开端。</p>
<p>1964年下半年，有线广播网开始全面建设。到1966年4月，先后建立了海州、锦屏、新坝、云台、朝阳、中云、云山、墟沟、连云港、猴嘴等放大站，装置了10部扩大机，计2500瓦；用杂木杆架设广播专用线路165公里，安装7146只喇叭（包括新浦地区）。当时102个大队中通广播的55个，612个生产队中通广播的303个。</p>
<p>1966年6月至1969年8月，有线广播设施遭到严重破坏，专用线路被破坏70%以上，喇叭损失2000多只，自办节目一度停止，主要转播中央人民广播电台和省人民广播电台节目。</p>
<p>1969年9月恢复自办节目，重新建设有线广播网。到1972年6月底，全市应建的15个区、镇、公社广播站和放大站全部建立，人员39人，广播放大机（包括市站在内）22部，9450瓦，市区到各区、镇、公社专线架设98杆公里；区、镇、公社和城镇以下广播线路架设457杆公里，全部是水泥杆和木杆，全市共安装喇叭30014只，基本上实现了院户通广播。</p>
<p>至1990年，市区和云台、海州、连云三区的所有乡镇建立了广播站，村通率达83.6%，喇叭入户率达62.7%，专线总计944杆公里，新浦市区居民中仍有小喇叭3000只。</p>
<p>二、县广播网</p>
<p>赣榆县1950年11月成立县广播收音站。1952年后相继建立了6个收音站。1954年收音网遍布全县大部分区乡。1956年10月1日，在青口镇隆巷内成立赣榆县人民广播站。有1台500瓦扩大机，1台收转机，1台3.6千瓦发电机，4个工作人员。</p>
<p>建站初期，全县广播信号主要通过电话线路传送。到1957年自架广播线路135杆公里，广播喇叭1000只。</p>
"""

EXPECTED_TEXT = [
    "<p>一、市区广播网</p>",
    "1只话筒",
    "每天播音4～5小时",
    "第一批舌簧小喇叭",
    "1959年初，市广播宣传站迁至民主路210号",
    "连云港市有线广播站",
    "有线广播网开始全面建设",
    "喇叭损失2000多只",
    "<p>二、县广播网</p>",
]
RESIDUALS = [
    "一、市区广播网1951年7月1日",
    "话简",
    "每天播音45小时",
    "第-批舌簧",
    "<p>：1958年",
    "<p>：目4小时",
    "有线厂播站",
    "有线厂播网",
    "喇肌叭",
    "节自。",
    "二、县广播网赣榆县",
]


def find_scope(text: str) -> tuple[int, int]:
    start = text.find(STABLE_SCOPE_START)
    if start < 0:
        start = text.index(SCOPE_START)
    end = text.index(NEXT_AFTER_SCOPE, start)
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
    return changed, {"rewrote_scope": changed, "sections_restored": 2}


def write_reports(changed: int, counts: dict[str, int]) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "第五十四卷报刊广播电视 / 第三章广播 / 第一节有线广播 / 市区广播网及县广播网开头",
        "source": SOURCE_NOTE,
        "reader_path": str(HTML),
        "changes_this_run": changed,
        "counts": counts,
        "principle": "依据 PaddleOCR 页级文本重建市区广播网，并拆出县广播网标题。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    md = f"""# 第五十四卷有线广播市区广播网回源修复

- 时间：{now}
- 范围：`第五十四卷报刊广播电视 / 第三章广播 / 第一节有线广播 / 市区广播网及县广播网开头`
- 源文依据：`{SOURCE_NOTE}`

## 修复动作

- 按页级 OCR 重建 `一、市区广播网`，补回 `1959年初，市广播宣传站迁至民主路210号...` 段。
- 修正 `话筒`、`4～5小时`、`第一批`、`有线广播站/网`、`喇叭损失`、`节目` 等明确 OCR 错文。
- 拆开 `二、县广播网` 题名与赣榆县正文粘连。
- 当前核验复跑整段替换：{changed} 处。
"""
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")


def update_memory(changed: int) -> None:
    marker = "## 2026-07-03 第五十四卷有线广播市区广播网回源修复"
    memory = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker in memory:
        return
    entry = f"""
{marker}

- 对第五十四卷报刊广播电视 `第三章广播 / 第一节有线广播 / 市区广播网及县广播网开头` 进行回源修复。
- 源文依据：`{SOURCE_NOTE}`；重建 `一、市区广播网` 并拆出 `二、县广播网` 标题。
- 修正 `话筒`、`4～5小时`、`第一批`、`1959年初市广播宣传站迁至民主路210号` 漏段、`有线广播站/网`、`喇叭损失` 等问题。
- 当前核验复跑整段替换 {changed} 处。
- 报告：`output/reports/reader_readability_broadcast_wired_city_20260703.md`。
"""
    MEMORY.write_text(memory.rstrip() + "\n\n" + entry.lstrip(), encoding="utf-8")


def main() -> None:
    changed, counts = patch_reader()
    write_reports(changed, counts)
    update_memory(changed)
    print(json.dumps({"changed": changed, "counts": counts}, ensure_ascii=False))


if __name__ == "__main__":
    main()
