# -*- coding: utf-8 -*-
"""Repair source-verified OCR slips in Volume 25 power industry."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_power_batch_20260704.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_power_batch_20260704.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260704_第二十五卷电力工业高置信错识回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SCOPE_START = '<h2 id="第二十五卷-电力工业">第二十五卷电力工业</h2>'
SCOPE_END = '<h2 id="第二十六卷-矿产">第二十六卷矿产</h2>'
SOURCE = "workbench/ocr/paddle_ocr/中/part01/page_0333.txt:21-39; page_0369.txt:25-40; page_0370.txt:1-7"

REPLACEMENTS = [
    ("负荷单位", "4.6万干瓦", "4.6万千瓦"),
    ("设计班子厂名", "新海发电广4个单位", "新海发电厂4个单位"),
    ("7号机组设计容量", "工程的设计容量为千瓦、电压为6.3干伏的发电机", "工程的设计容量为1.2万千瓦（编为7号机组），安装1台容量为1.2万千瓦的凝汽式汽轮机；1台容量为1.2万千瓦、电压为6.3千伏的发电机"),
    ("进入安装阶段", "1973年6月下旬进人安装阶段", "1973年6月下旬进入安装阶段"),
    ("电厂低压低周", "电广经常低压低周运行", "电厂经常低压低周运行"),
    ("四期扩建缺句", "江苏省水利电力局下达在新海发锅炉的蒸发量为130吨/时", "江苏省水利电力局下达在新海发电厂扩建两台2.5万千瓦汽轮发电机组的任务。1974年11月，通过设计审查，2台配套锅炉的蒸发量为130吨/时"),
    ("四期安装阶段", "1975年10月4日破土动工，7月下旬进人安装阶段", "1975年10月4日破土动工，7月下旬进入安装阶段"),
    ("农村用电单位", "农村用电6方千瓦时", "农村用电6万千瓦时"),
    ("农村电气化引号", "在农村电气化”运动中", "在“农村电气化”运动中"),
    ("旱田改水田", "农村“阜田改水田”全面推广", "农村“旱田改水田”全面推广"),
    ("农村用电1985单位", "达19377万于瓦时", "达19377万千瓦时"),
]

SKIPPED = [
    "`2.56千瓦` 疑似应为 `2.56万千瓦`，但页级 OCR 仍拆行为 `2.56` + `千瓦`，本批不凭常识猜改。",
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
        "principle": "仅修复页级 OCR 或同页上下文清楚支撑的第二十五卷错识；疑似但无源证据的数值单位不猜改。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# 第二十五卷电力工业高置信错识回源修复",
        "",
        f"- 时间：{now}",
        f"- 范围：{payload['scope']}",
        f"- 源文：`{SOURCE}`",
        f"- 阅读器：`{HTML}`",
        f"- 本批核验修复：{verified_items} 项",
        f"- 本次脚本复跑实际改写：{current_changes} 处",
        "- 重点：修正新海发电厂扩建段厂名、7号机组容量句、四期扩建缺句、农村用电单位和引号错识。",
        "- 保留：`2.56千瓦` 疑似缺 `万`，但页级 OCR 未直接确认，本批不猜改。",
        "",
    ]
    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")
    PROGRESS.write_text("\n".join(lines), encoding="utf-8")
    memory = f"""
## 2026-07-04 第二十五卷电力工业高置信错识回源修复

- 对第二十五卷电力工业进行小批回源修复，范围限定在 `第二十五卷-电力工业` 到 `第二十六卷-矿产` 前。
- 源文依据：`{SOURCE}`。
- 修复示例：`新海发电广4个单位`→`新海发电厂4个单位`，补回 `工程的设计容量为1.2万千瓦（编为7号机组）...`，`电广经常低压低周运行`→`电厂经常低压低周运行`，补回 `新海发电厂扩建两台2.5万千瓦汽轮发电机组的任务`，`农村用电6方千瓦时`→`农村用电6万千瓦时`，`阜田改水田`→`旱田改水田`。
- 本批核验修复 {verified_items} 项；`2.56千瓦` 疑似缺 `万`，但页级 OCR 未直接确认，本批保留。
- 报告：`output/reports/reader_readability_power_batch_20260704.md`。
"""
    append_once(MEMORY, "## 2026-07-04 第二十五卷电力工业高置信错识回源修复", memory)


def main() -> None:
    counts = patch_reader()
    write_reports(counts)
    print(json.dumps({"current_run_replacements": sum(counts.values()), "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
