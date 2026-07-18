# -*- coding: utf-8 -*-
"""Restore wired broadcast county network section from page OCR."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_broadcast_wired_counties_20260703.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_broadcast_wired_counties_20260703.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260703_第五十四卷有线广播县广播网回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SOURCE_NOTE = "workbench/ocr/paddle_ocr/下/part02/page_0147.txt:3-36"
SCOPE_START = '<p>1979年2月，赣榆县广播站被江苏省人民政府授予“广播系统先进集体”称号。1984年，1300平方米广播业务楼建成。'
SCOPE_END = '<h4 id="第五十四卷-第三章广播-第二节无线广播">第二节无线广播</h4>'

NEW_HTML = """<p>1979年2月，赣榆县广播站被江苏省人民政府授予“广播系统先进集体”称号。1984年，1300平方米广播业务楼建成。1987年，按部颁甲级标准架设青口——赣马5.5杆公里专线，采用铝包钢线条，是全市第一条高质量的广播信号线路。</p>
<p>1990年村通率达99.3%，装喇叭的农户达18.56万户，喇叭入户率为78%，专线传输1725杆公里。在1989年和1990年省广播电视厅组织的有线广播检查评比中连续两年获一等奖。</p>
<p>东海县1952年11月成立县广播收音站。1956年6月13日建立县有线广播站，职工25名，地址设在海州城北。设备有1部150瓦扩大机，2台收音机，1部旧发电机，利用电话线传送广播。全县线路只有3条，喇叭100只，每天晚上播发2个小时节目。1957年11月，县有线广播站随县政府迁往牛山镇，设在县大会堂二楼。</p>
<p>1959年，全县先后有石榴、房山等6个乡建立广播放大站，安装喇叭2800只。</p>
<p>1960～1963年初，受国民经济困难影响，全县6个广播放大站先后停播。1964年8月，石榴等广播放大站恢复转播并建起广播专线4条，即县城至双店、白塔、青湖和房山，共62杆公里，有50个生产大队通广播，广播普及率仅12%。</p>
<p>1966年9月15日，东海县有线广播站改称为东海县人民广播站。同年10月1日起自办节目停办，全部转播中央台和省台节目（天气预报除外）。</p>
<p>1970年7月1日恢复自办节目，每天30分钟。年底，社社建立了广播放大站，总数达21个，架设广播专用信号线242杆公里，全县共安装广播喇叭122300只。</p>
<p>1980年，904平方米的县广播业务楼主体工程建成。全县有广播放大站（包括岗埠农场、种畜场）24个，550瓦扩音机30部（套），总输出功率为16500瓦，架设县至乡（场）广播放大站专线242杆公里，共有喇叭10万只。至1989年8月，全县24个乡镇2个场（岗埠农场、种畜场）全部建立了广播放大站。1990年除种畜场外，均改为广播电视站。至此，有16.37万农户安装喇叭，入户率达67%，专线达1902杆公里。在1989～1990年省广播电视厅组织的有线广播检查评比中连续两年获一等奖。</p>
<p>灌云县民国38年（1949年）3月15日成立县广播收音站。1956年夏成立县有线广播站，地址在伊山镇万巷子。初建时利用电话杆线在县城附近连通伊山、东王集、板浦、陡沟、仲集等乡的广播，安装喇叭300只，每天广播2～3小时。1958年初，全县架设广播专线360杆公里，安装喇叭1000多只。1964年，全县实现社社通广播，安装喇叭7000多只。</p>
<p>1965年3月，县有线广播站更名为灌云人民广播站。到1968年底，全县有县站至燕尾港等4条专线，安装喇叭12000只。1972年入户率达80%，共装喇叭12万多只。</p>
<p>1984年9月，700平方米的县广播站业务楼建成。至1990年，全县喇叭总数达15.37万只，专线达2231杆公里。</p>
"""

EXPECTED_TEXT = [
    "青口——赣马5.5杆公里专线",
    "喇叭入户率为78%",
    "职工25名",
    "利用电话线传送广播",
    "中央台和省台节目（天气预报除外）",
    "岗埠农场、种畜场）全部建立",
    "1989～1990年省广播电视厅",
    "每天广播2～3小时",
]
RESIDUALS = [
    "青口-—赣马",
    "5.5杆公，里",
    "喇叭人户率",
    "职25名",
    "传送厂播",
    "省台节自",
    "种畜场)全部建立",
    "1989~1990年省广播",
    "每天广播2~3小时",
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
    return changed, {"rewrote_scope": changed, "county_segments_restored": 3}


def write_reports(changed: int, counts: dict[str, int]) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "第五十四卷报刊广播电视 / 第三章广播 / 第一节有线广播 / 县广播网后续",
        "source": SOURCE_NOTE,
        "reader_path": str(HTML),
        "changes_this_run": changed,
        "counts": counts,
        "principle": "依据 PaddleOCR 页级文本重建县广播网赣榆后续、东海、灌云段，停止在无线广播前。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    md = f"""# 第五十四卷有线广播县广播网回源修复

- 时间：{now}
- 范围：`第五十四卷报刊广播电视 / 第三章广播 / 第一节有线广播 / 县广播网后续`
- 源文依据：`{SOURCE_NOTE}`

## 修复动作

- 按页级 OCR 重建赣榆县后续、东海县、灌云县有线广播段，停止在 `第二节无线广播` 前。
- 修正 `青口——赣马`、`喇叭入户率`、`职工25名`、`传送广播`、`节目`、括号和年份连接符等明确内容。
- 当前核验复跑整段替换：{changed} 处。
"""
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")


def update_memory(changed: int) -> None:
    marker = "## 2026-07-03 第五十四卷有线广播县广播网回源修复"
    memory = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker in memory:
        return
    entry = f"""
{marker}

- 对第五十四卷报刊广播电视 `第三章广播 / 第一节有线广播 / 县广播网后续` 进行回源修复。
- 源文依据：`{SOURCE_NOTE}`；重建赣榆县后续、东海县、灌云县段，停止在 `第二节无线广播` 前。
- 修正 `青口——赣马`、`喇叭入户率`、`职工25名`、`传送广播`、`节目`、括号和年份连接符等问题。
- 当前核验复跑整段替换 {changed} 处。
- 报告：`output/reports/reader_readability_broadcast_wired_counties_20260703.md`。
"""
    MEMORY.write_text(memory.rstrip() + "\n\n" + entry.lstrip(), encoding="utf-8")


def main() -> None:
    changed, counts = patch_reader()
    write_reports(changed, counts)
    update_memory(changed)
    print(json.dumps({"changed": changed, "counts": counts}, ensure_ascii=False))


if __name__ == "__main__":
    main()
