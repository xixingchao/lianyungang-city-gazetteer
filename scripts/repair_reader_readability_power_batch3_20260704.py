# -*- coding: utf-8 -*-
"""Repair third source-verified OCR slip batch in Volume 25 power industry."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_power_batch3_20260704.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_power_batch3_20260704.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260704_第二十五卷电力工业高置信错识第三批回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SCOPE_START = '<h2 id="第二十五卷-电力工业">第二十五卷电力工业</h2>'
SCOPE_END = '<h2 id="第二十六卷-矿产">第二十六卷矿产</h2>'
SOURCE = "workbench/ocr/paddle_ocr/中/part01/page_0333.txt:18-21; page_0341.txt:11-32; page_0342.txt:7-16; page_0346.txt:10,34; page_0350.txt:17-35; page_0351.txt:12-28; page_0354.txt:4,11-17,28-29; page_0369.txt:25-40; page_0370.txt:4-38"

REPLACEMENTS = [
    ("1966发电机容量", "扩建1台6000干瓦的发电机组", "扩建1台6000千瓦的发电机组"),
    ("1966主变容量", "3台容量为2600于伏安的单相变压器", "3台容量为2600千伏安的单相变压器"),
    ("1966进入安装", "7月中旬进人安装阶段", "7月中旬进入安装阶段"),
    ("新浦热电并入", "升压至35千伏并人地区电网运行", "升压至35千伏并入地区电网运行"),
    ("新浦热电发电量", "1987年发电量为224万于瓦时", "1987年发电量为224万千瓦时"),
    ("水电总容量", "总容量为5580干瓦", "总容量为5580千瓦"),
    ("肖岭总容量", "总容量为1026(5×200+1×26)于瓦", "总容量为1026(5×200+1×26)千瓦"),
    ("肖岭1990发电", "1990年发电7万于瓦时", "1990年发电7万千瓦时"),
    ("1954配变容量", "总容量562.5干伏安", "总容量562.5千伏安"),
    ("1958升压", "电网电压由22千伏升到35干伏", "电网电压由22千伏升到35千伏"),
    ("刘顶6千伏出线", "架设6干伏出线3条", "架设6千伏出线3条"),
    ("1958升压站投入", "于同年6月30日投人运行", "于同年6月30日投入运行"),
    ("35千伏变电所5座", "35于伏变电所5座", "35千伏变电所5座"),
    ("1970淮海盐", "组成以110干伏设备为主要骨架的准海盐电网", "组成以110千伏设备为主要骨架的淮海盐电网"),
    ("1976新海发电厂", "新海发电广增建2台2.5方千瓦发电机组", "新海发电厂增建2台2.5万千瓦发电机组"),
    ("牛山变电所110千伏", "110于伏牛山变电所", "110千伏牛山变电所"),
    ("110千伏变电所5座", "110千伏变电所5公单", "110千伏变电所5座"),
    ("110千伏中心电源", "以110于伏变电所为中心电源", "以110千伏变电所为中心电源"),
    ("淮海盐联入", "准海盐电网联人省电网", "淮海盐电网联入省电网"),
    ("220系统联入", "地区电网联人省220千伏系统运行", "地区电网联入省220千伏系统运行"),
    ("全年供电1987", "全年供电113858万于瓦时", "全年供电113858万千瓦时"),
    ("35千伏变电所86座", "35于伏变电所86座", "35千伏变电所86座"),
    ("全年供电1990", "全年供电121800万于瓦时", "全年供电121800万千瓦时"),
    ("35千伏主干", "35干伏变电工程", "35千伏变电工程"),
    ("刘灌线主通道", "为准海盐电网的主通道之一", "为淮海盐电网的主通道之一"),
    ("淮海线上T接", "准海线上T接110千伏伊山变电所", "淮海线上T接110千伏伊山变电所"),
    ("牛山升压", "对原35于伏牛山变电所进行升压改造", "对原35千伏牛山变电所进行升压改造"),
    ("刘顶进线", "进线为110千伏准海线", "进线为110千伏淮海线"),
    ("新海发电厂联络", "以海磷线和新海发电广联络", "以海磷线和新海发电厂联络"),
    ("海刘配套", "扩建新海发电广2×25000千瓦发电机组", "扩建新海发电厂2×25000千瓦发电机组"),
    ("海刘进线", "又增加1条110干伏进线", "又增加1条110千伏进线"),
    ("伊山淮海线", "进线T接于110千伏准海线上", "进线T接于110千伏淮海线上"),
    ("淮阴电网", "该变电所主要接受阴电网电力", "该变电所主要接受淮阴电网电力"),
    ("输入电能", "地区电网输人电能", "地区电网输入电能"),
    ("伊山35千伏出线", "该所共有35于伏出线5条", "该所共有35千伏出线5条"),
    ("新牛线发电厂", "形成了新海发电广通过海白线", "形成了新海发电厂通过海白线"),
    ("海磷线35千伏", "通过35干伏海磷线", "通过35千伏海磷线"),
    ("标准电压等级", "10于伏、6千伏4个标准电压等级", "10千伏、6千伏4个标准电压等级"),
    ("淮阴电网联络", "和准阴电网联络", "和淮阴电网联络"),
    ("平东线110千伏", "由110于伏平东线主供", "由110千伏平东线主供"),
    ("淮海线停止", "如果110千伏准海线停止运行", "如果110千伏淮海线停止运行"),
    ("220平茅线", "当220于伏平茅线", "当220千伏平茅线"),
    ("农副业用电", "农副业用电6932万干瓦时", "农副业用电6932万千瓦时"),
    ("林业用电", "林业用电147方千瓦时", "林业用电147万千瓦时"),
    ("渔业用电", "渔业用电404方千瓦时", "渔业用电404万千瓦时"),
    ("交通装接容量", "装接容量为22652于瓦", "装接容量为22652千瓦"),
    ("市政年用电", "年用电11万干瓦时", "年用电11万千瓦时"),
    ("市政生活电量", "市政生活年用电5604方千瓦时", "市政生活年用电5604万千瓦时"),
    ("调荷供电所", "新海发电广供电所", "新海发电厂供电所"),
]

SKIPPED = [
    "继续保留表25-4、线损率等统计长段的压平残文，后续按表格/长段专项处理。",
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
        "principle": "仅修复页级 OCR 清楚给出正确写法的第二十五卷短错识；统计长段和表格残文另行专项。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# 第二十五卷电力工业高置信错识第三批回源修复",
        "",
        f"- 时间：{now}",
        f"- 范围：{payload['scope']}",
        f"- 源文：`{SOURCE}`",
        f"- 阅读器：`{HTML}`",
        f"- 本批核验修复：{verified_items} 项",
        f"- 本次脚本复跑实际改写：{current_changes} 处",
        "- 重点：修正发电、供电网络、水电站、变电所和用电结构段落中的 `干/于/方/准/人/阴` 类 OCR 错识。",
        "- 保留：表25-4、线损率等统计长段压平残文，后续按表格/长段专项处理。",
        "",
    ]
    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")
    PROGRESS.write_text("\n".join(lines), encoding="utf-8")
    memory = f"""
## 2026-07-04 第二十五卷电力工业高置信错识第三批回源修复

- 继续对第二十五卷电力工业做小批回源修复，范围限定在 `第二十五卷-电力工业` 到 `第二十六卷-矿产` 前。
- 源文依据：`{SOURCE}`。
- 修复示例：`6000干瓦/2600于伏安/35干伏/110于伏/方千瓦时` 等单位错识，`准海盐电网/准海线/准阴电网`→`淮海盐电网/淮海线/淮阴电网`，以及 `新海发电广/输人/进人/投人` 等错识。
- 本批核验修复 {verified_items} 项；表25-4、线损率等统计长段压平残文继续保留给后续专项。
- 报告：`output/reports/reader_readability_power_batch3_20260704.md`。
"""
    append_once(MEMORY, "## 2026-07-04 第二十五卷电力工业高置信错识第三批回源修复", memory)


def main() -> None:
    counts = patch_reader()
    write_reports(counts)
    print(json.dumps({"current_run_replacements": sum(counts.values()), "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
