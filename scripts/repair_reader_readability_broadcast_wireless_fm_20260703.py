# -*- coding: utf-8 -*-
"""Restore wireless broadcast FM section from page OCR."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_broadcast_wireless_fm_20260703.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_broadcast_wireless_fm_20260703.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260703_第五十四卷无线广播调频段回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SOURCE_NOTE = "workbench/ocr/paddle_ocr/下/part02/page_0149.txt:4-25"
SCOPE_START = '<p>二、调频广播（含调频立体声）</p>'
SCOPE_END = '<h4 id="第五十四卷-第三章广播-第三节广播节目设置">第三节广播节目设置</h4>'

NEW_HTML = """<p>二、调频广播（含调频立体声）</p>
<p>连云港调频广播发射台设于锦屏山马耳峰上，海拔425米，方位：北纬34°32′58″，东经119°07′56″，与电视共塔。</p>
<p>调频省转播台1975年建台，时有GCP-2-2型差转式调频发射机1部。1978年购置差转式调频发射机1部，以97兆赫转播省台第一套节目，同时，为中波发射台提供省台第一套节目的信号源。</p>
<p>连云港调频广播电台1985年6月开通，以1千瓦94.4兆赫转发市电台节目（含立体声），发射机为GCP-1-1型单声道调频发射机，发射天线为二层八面的角锥天线。</p>
<p>市台调频广播节目的任务是和中波台1350千赫一起完成市台节目对全市的覆盖，每天播出时间9小时25分。</p>
<p>1989年6月，市调频广播电台利用94.4兆赫开通调频立体声节目，所用发射设备仍是单声道调频发射机，配用了LSB-1型立体声解码器，但左右声道隔离度差。1989年底，购进TBV311型调频立体声发射机，质量明显提高。并从瑞士思德利公司购进B-215录音座两台，B-2696路调音台1台，作为播出设备。</p>
<p>立体声节目播出时间为中午12:00到13:00。</p>
<p>调频台1987年覆盖人口324.06万，覆盖率达99.7%。1990年覆盖率达100%。1988～1990年，连续三年在省广播电视厅组织的全省检查评比中获一等奖。</p>
<p>墟沟、连岛转播台1989年10月，墟沟北崮山电视转播台安装了TF7100型调频发射机1台，频率为98.3兆赫，发射功率为50瓦。1990年2月，连岛电视转播台安装了TF7150型调频发射机1台，频率为105.9兆赫，发射功率为50瓦。至此，东部港口地区全部转播连云港台节目。</p>
"""

EXPECTED_TEXT = [
    "海拔425米",
    "北纬34°32′58″，东经119°07′56″",
    "省台第一套节目的信号源",
    "GCP-1-1型单声道调频发射机",
    "1350千赫一起完成",
    "B-2696路调音台1台",
    "1988～1990年，连续三年在省广播电视厅",
    "墟沟北崮山电视转播台",
]
RESIDUALS = [
    "海拨425米",
    "东经1190756",
    "第一一套节目",
    "GCP-1一1型",
    "一一起完成",
    "9小时25分。：",
    "B2696路调音台",
    "1988~1990年",
    "省厂播电视厅",
    "北窗山",
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
    return changed, {"rewrote_scope": changed, "subsections_restored": 4}


def write_reports(changed: int, counts: dict[str, int]) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "第五十四卷报刊广播电视 / 第三章广播 / 第二节无线广播 / 二、调频广播",
        "source": SOURCE_NOTE,
        "reader_path": str(HTML),
        "changes_this_run": changed,
        "counts": counts,
        "principle": "依据 PaddleOCR 页级文本重建无线广播调频段，停止在第三节广播节目设置前。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    md = f"""# 第五十四卷无线广播调频段回源修复

- 时间：{now}
- 范围：`第五十四卷报刊广播电视 / 第三章广播 / 第二节无线广播 / 二、调频广播`
- 源文依据：`{SOURCE_NOTE}`

## 修复动作

- 按页级 OCR 重建 `二、调频广播（含调频立体声）`，停止在 `第三节广播节目设置` 前。
- 修正海拔、经纬度、省台第一套节目、设备型号、检查评比、北崮山等明确错文。
- 当前核验复跑整段替换：{changed} 处。
"""
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")


def update_memory(changed: int) -> None:
    marker = "## 2026-07-03 第五十四卷无线广播调频段回源修复"
    memory = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker in memory:
        return
    entry = f"""
{marker}

- 对第五十四卷报刊广播电视 `第三章广播 / 第二节无线广播 / 二、调频广播` 进行回源修复。
- 源文依据：`{SOURCE_NOTE}`；重建至 `第三节广播节目设置` 前。
- 修正海拔、经纬度、省台第一套节目、设备型号、检查评比、北崮山等问题。
- 当前核验复跑整段替换 {changed} 处。
- 报告：`output/reports/reader_readability_broadcast_wireless_fm_20260703.md`。
"""
    MEMORY.write_text(memory.rstrip() + "\n\n" + entry.lstrip(), encoding="utf-8")


def main() -> None:
    changed, counts = patch_reader()
    write_reports(changed, counts)
    update_memory(changed)
    print(json.dumps({"changed": changed, "counts": counts}, ensure_ascii=False))


if __name__ == "__main__":
    main()
