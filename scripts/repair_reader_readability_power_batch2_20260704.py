# -*- coding: utf-8 -*-
"""Repair second source-verified OCR slip batch in Volume 25 power industry."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_power_batch2_20260704.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_power_batch2_20260704.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260704_第二十五卷电力工业高置信错识第二批回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SCOPE_START = '<h2 id="第二十五卷-电力工业">第二十五卷电力工业</h2>'
SCOPE_END = '<h2 id="第二十六卷-矿产">第二十六卷矿产</h2>'
SOURCE = "workbench/ocr/paddle_ocr/中/part01/page_0330.txt:17-28; page_0331.txt:4-18; page_0334.txt:36-40; page_0337.txt:37-38; page_0351.txt:12-23; page_0353.txt:17-24; page_0354.txt:11-16; page_0356.txt:35; page_0359.txt:7-10"

REPLACEMENTS = [
    ("20万机组投入", "已于1990年1月投人运行", "已于1990年1月投入运行"),
    ("10千伏配电网络", "10干伏配电网络", "10千伏配电网络"),
    ("海连线投入", "首次投人运行", "首次投入运行"),
    ("淮阴淮海盐电网", "准阴、连云港、盐城组成了以110干伏设备为主要骨架的准海盐电网", "淮阴、连云港、盐城组成了以110千伏设备为主要骨架的淮海盐电网"),
    ("自己的变电所", "各自以自已的110千伏变电所", "各自以自己的110千伏变电所"),
    ("概述淮海盐并入", "1982年，准海盐电网并人省电网运行。1987年", "1982年，淮海盐电网并入省电网运行。1987年"),
    ("35千伏供电网络", "35干伏供电网络", "35千伏供电网络"),
    ("概述进入80年代", "进人80年代，市政建设", "进入80年代，市政建设"),
    ("发电容量单位", "8.6万干瓦", "8.6万千瓦"),
    ("自备电厂容量", "4.16方千瓦", "4.16万千瓦"),
    ("自备电厂发电量", "1.18亿于瓦时", "1.18亿千瓦时"),
    ("5号机投入", "1961年，重新安装的5号机投人运行", "1961年，重新安装的5号机投入运行"),
    ("新海发电厂调相机", "1966年，新海发电广将1号1600于瓦汽轮发电机", "1966年，新海发电厂将1号1600千瓦汽轮发电机"),
    ("两台2.5万千瓦", "两台2.5万于瓦机组", "两台2.5万千瓦机组"),
    ("发电厂并入淮海盐", "新海发电厂并入准海盐电网", "新海发电厂并入淮海盐电网"),
    ("列入反事故", "列人反事故措施计划", "列入反事故措施计划"),
    ("刘顶淮海盐", "110干伏刘顶变电所通过110千伏淮海线并人准海盐电网运行", "110千伏刘顶变电所通过110千伏淮海线并入淮海盐电网运行"),
    ("淮海盐供电", "部分由准海盐电网供电", "部分由淮海盐电网供电"),
    ("海刘联络淮海盐", "与准海盐电网联络的关系", "与淮海盐电网联络的关系"),
    ("淮海线供电", "以110千伏准海线供电为主", "以110千伏淮海线供电为主"),
    ("调度沿革淮海盐", "建成准海盐电网，调度业务直接受准海盐电力调度组领导", "建成淮海盐电网，调度业务直接受淮海盐电力调度组领导"),
    ("调度所撤销", "1982年，准海盐电网并人省电网运行，准海盐电网调度所被撤销", "1982年，淮海盐电网并入省电网运行，淮海盐电网调度所被撤销"),
    ("远动调度所", "送至准海盐电网调度所", "送至淮海盐电网调度所"),
]

SKIPPED = [
    "保留统计表压平残文、长段断裂，以及未找到直接源页支撑的疑似数值单位。",
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
    for label, old, new in REPLACEMENTS:
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
    missing = [new for _label, _old, new in REPLACEMENTS if new not in segment]
    residuals = [old for _label, old, new in REPLACEMENTS if old in segment and old not in new]
    if missing or residuals:
        raise RuntimeError(f"verification failed: missing={missing}, residuals={residuals}")


def append_once(path: Path, marker: str, content: str) -> None:
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker not in old:
        path.write_text(old.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")


def write_reports(counts: dict[str, int]) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    current_changes = sum(counts.values())
    verified_items = len(REPLACEMENTS)
    payload = {
        "time": now,
        "scope": "第二十五卷电力工业",
        "source": SOURCE,
        "reader_path": str(HTML),
        "verified_items": verified_items,
        "current_run_replacements": current_changes,
        "counts": counts,
        "skipped": SKIPPED,
        "principle": "仅修复页级 OCR 清楚给出正确写法的第二十五卷短错识；统计表残文和无源证据数值不猜改。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# 第二十五卷电力工业高置信错识第二批回源修复",
        "",
        f"- 时间：{now}",
        f"- 范围：{payload['scope']}",
        f"- 源文：`{SOURCE}`",
        f"- 阅读器：`{HTML}`",
        f"- 本批核验修复：{verified_items} 项",
        f"- 本次脚本复跑实际改写：{current_changes} 处",
        "- 重点：修正概述、运行、电网调度和淮海盐电网相关段落中的 `干/于/方/准/人/自已` 类 OCR 错识。",
        "- 保留：统计表压平残文、长段断裂、以及未找到直接源页支撑的疑似数值单位。",
        "",
    ]
    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")
    PROGRESS.write_text("\n".join(lines), encoding="utf-8")
    memory = f"""
## 2026-07-04 第二十五卷电力工业高置信错识第二批回源修复

- 继续对第二十五卷电力工业做小批回源修复，范围限定在 `第二十五卷-电力工业` 到 `第二十六卷-矿产` 前。
- 源文依据：`{SOURCE}`。
- 修复示例：`投人/进人/列人`→`投入/进入/列入`，`10干伏/35干伏/1600于瓦`→`10千伏/35千伏/1600千瓦`，`准阴/准海盐电网/准海线`→`淮阴/淮海盐电网/淮海线`，`自已`→`自己`，`4.16方千瓦`→`4.16万千瓦`。
- 本批核验修复 {verified_items} 项；统计表压平残文和无直接源证据的疑似数值单位继续保留。
- 报告：`output/reports/reader_readability_power_batch2_20260704.md`。
"""
    append_once(MEMORY, "## 2026-07-04 第二十五卷电力工业高置信错识第二批回源修复", memory)


def main() -> None:
    counts = patch_reader()
    write_reports(counts)
    print(json.dumps({"current_run_replacements": sum(counts.values()), "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
