# -*- coding: utf-8 -*-
"""Restore wireless broadcast AM section from page OCR."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_broadcast_wireless_am_20260703.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_broadcast_wireless_am_20260703.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260703_第五十四卷无线广播中波段回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SOURCE_NOTE = "workbench/ocr/paddle_ocr/下/part02/page_0148.txt:4-36"
SCOPE_START = '<h4 id="第五十四卷-第三章广播-第二节无线广播">第二节无线广播</h4>'
SCOPE_END = '<p>二、调频广播（含调频立体声）</p>'

NEW_HTML = """<h4 id="第五十四卷-第三章广播-第二节无线广播">第二节无线广播</h4>
<p>一、中波广播</p>
<p>连云港人民广播电台1959年5月1日成立，台址初与有线广播站一起在新浦民主路210号一栋40年代建造的四合院式两层楼上，面积200平方米。建台时，包括有线广播站计有27人，有631录音机两台、9管收音机两只，1千瓦中波发射机1部，200瓦发射机1部。架设高57米的木杆发射天线。呼号为新海连人民广播电台，频率为1350千赫，和有线广播站共办一套节目，全天播音10小时20分，其中转播中央台和省台节目6小时20分，自办节目4小时。</p>
<p>1961年1月，市电台与《新海连日报》合并办公（1969年分开）。1962年6月1日，停止播音。</p>
<p>1965年10月恢复播音。除天气预报外，主要转播中央台及省台的节目。</p>
<p>1970年9月，经省、市革命委员会批准，在海州孔望山筹建发射台，海拔15米，方位：北纬34°34′20″，东经119°09′56″，占地面积3.33公顷。至1971年6月底，完成了1000平方米的土建工程任务；同年，新架设高83米的发射天线1幅。1972年1月1日，新台正式起用，原发射台停止播音。</p>
<p>1978年3月1日，连云港人民广播电台广播业务楼在新浦解放西路落成使用，方位：北纬34°16′15″，东经119°09′40″。内设大演播室1个、小播音室2个以及节目制作用房2个，并配有暖气、地下室等设施。</p>
<p>1979年7月1日，连云港人民广播电台恢复自办节目，两台1千瓦中波发射机为主、备机，频率为1350千赫，呼号为连云港人民广播电台。</p>
<p>1984年12月10日，广播业务楼与孔望山中波发射台架设双路供电设施竣工。</p>
<p>1987年底计有L-635、L-637等录音机26台，日本山水录音机1台，中华音箱1只，412型调音台等，在省广播电视厅组织的检查评比中获一等奖。1988年底，中波和传音在省组织的检查评比中获一等奖。1989年9月，从日本购进小谷505录音机两台，10路调音台1台。1990年购进美产EV5212调音台1台，形成三条档次较高的节目制作线。发射功率仍为1千瓦（主、备机各1千瓦），覆盖人口149.52万人，覆盖率达44%。</p>
<p>中波转播台1959年成立至1978年，一直用1350千赫频率部分转播中央台第一套节目。1978年10月，开始以567千赫转播中央台第一套节目。1990年，建立卫星地面接收站（使用4.5米反馈天线和卫星节目解调器），接收中央台第一套、第二套节目。转播中央台第一套节目的发射功率主机为10千瓦，备机为1千瓦。</p>
<p>中波同步广播网1978年11月23日，中波发射台正式建成702千赫广播同步网，与省台第一套节目702千赫同步广播。至1990年底，有702千赫的主机10千瓦1部，备机1千瓦1部，覆盖人口312.36万，覆盖率达91.8%。</p>
"""

EXPECTED_TEXT = [
    "<p>一、中波广播</p>",
    "包括有线广播站计有27人",
    "全天播音10小时20分",
    "北纬34°34′20″，东经119°09′56″，占地面积3.33公顷",
    "北纬34°16′15″，东经119°09′40″",
    "恢复自办节目",
    "供电设施竣工",
    "中央台第一套节目的发射功率",
    "省台第一套节目702千赫同步广播",
]
RESIDUALS = [
    "一、中波广播连云港人民广播电台",
    "有线广机1部",
    "10:小时20",
    "1969年分开）。·1962",
    "北纬34°3420",
    "东经1190956",
    "公项",
    "北纬34°1615",
    "东经119°09°40",
    "恢复自办节自",
    "峻工",
    "第-一套节目",
    "接：收站",
    "第一套节自",
    "省台第套节目",
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
    return changed, {"rewrote_scope": changed, "subsections_restored": 3}


def write_reports(changed: int, counts: dict[str, int]) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "第五十四卷报刊广播电视 / 第三章广播 / 第二节无线广播 / 一、中波广播",
        "source": SOURCE_NOTE,
        "reader_path": str(HTML),
        "changes_this_run": changed,
        "counts": counts,
        "principle": "依据 PaddleOCR 页级文本重建无线广播中波段，停止在二、调频广播前。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    md = f"""# 第五十四卷无线广播中波段回源修复

- 时间：{now}
- 范围：`第五十四卷报刊广播电视 / 第三章广播 / 第二节无线广播 / 一、中波广播`
- 源文依据：`{SOURCE_NOTE}`

## 修复动作

- 按页级 OCR 重建 `一、中波广播`，停止在 `二、调频广播` 前。
- 补回建台设备人数与设备清单，修正经纬度、`公顷`、`节目`、`竣工`、中央台/省台第一套节目等明确错文。
- 当前核验复跑整段替换：{changed} 处。
"""
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")


def update_memory(changed: int) -> None:
    marker = "## 2026-07-03 第五十四卷无线广播中波段回源修复"
    memory = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker in memory:
        return
    entry = f"""
{marker}

- 对第五十四卷报刊广播电视 `第三章广播 / 第二节无线广播 / 一、中波广播` 进行回源修复。
- 源文依据：`{SOURCE_NOTE}`；重建至 `二、调频广播` 前。
- 修正建台设备人数与设备清单漏失、经纬度、`公顷`、`节目`、`竣工`、中央台/省台第一套节目等问题。
- 当前核验复跑整段替换 {changed} 处。
- 报告：`output/reports/reader_readability_broadcast_wireless_am_20260703.md`。
"""
    MEMORY.write_text(memory.rstrip() + "\n\n" + entry.lstrip(), encoding="utf-8")


def main() -> None:
    changed, counts = patch_reader()
    write_reports(changed, counts)
    update_memory(changed)
    print(json.dumps({"changed": changed, "counts": counts}, ensure_ascii=False))


if __name__ == "__main__":
    main()
