# -*- coding: utf-8 -*-
"""Repair fourth source-verified OCR slip batch in Volume 25 power industry."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_power_batch4_20260704.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_power_batch4_20260704.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260704_第二十五卷电力工业高置信错识第四批回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SCOPE_START = '<h2 id="第二十五卷-电力工业">第二十五卷电力工业</h2>'
SCOPE_END = '<h2 id="第二十六卷-矿产">第二十六卷矿产</h2>'
SOURCE = "workbench/ocr/paddle_ocr/中/part01/page_0343.txt:8-19; page_0344.txt:36-39; page_0347.txt:1-40; page_0348.txt:1-40; page_0349.txt:1-37; page_0350.txt:24-40; page_0351.txt:1-40; page_0352.txt:1-40; page_0353.txt:1-40; page_0359.txt:1-15; page_0360.txt:1-40; page_0362.txt:1-40; page_0364.txt:1-8"

REPLACEMENTS = [
    ("东山发电厂竣工", "该厂始建于1974年10月，工于1976年5月", "该厂始建于1974年10月，竣工于1976年5月"),
    ("东山6000千瓦", "初建时投产1台6000于瓦发电机组", "初建时投产1台6000千瓦发电机组"),
    ("东山主变容量", "35千伏升压站主变容量为8000于伏安", "35千伏升压站主变容量为8000千伏安"),
    ("自备柴油发电", "1988年发电分别为32、19、41、79方千瓦时", "1988年发电分别为32、19、41、79万千瓦时"),
    ("刘灌线淮海", "110千伏准海线投运后", "110千伏淮海线投运后"),
    ("海平线自己设计", "由连云港供电局自已设计、施工", "由连云港供电局自己设计、施工"),
    ("平茅线投入", "1987年11月4日投人运行", "1987年11月4日投入运行"),
    ("平山10千伏", "至1987年10于伏出线又增加3条", "至1987年10千伏出线又增加3条"),
    ("牛山10千伏", "有一条10于伏出线", "有一条10千伏出线"),
    ("刘顶10千伏母线", "10干伏母线采用单母线接线", "10千伏母线采用单母线接线"),
    ("茅口投入", "1987年11月5日投人运行", "1987年11月5日投入运行"),
    ("茅口220开关", "220干伏开关2组", "220千伏开关2组"),
    ("茅口220进线", "进线为220干伏平茅线", "进线为220千伏平茅线"),
    ("茅口110供电", "平山等110于伏变电所供电", "平山等110千伏变电所供电"),
    ("茅口35母线", "110千伏和35干伏均采用双母线", "110千伏和35千伏均采用双母线"),
    ("调度茅口投入", "220千伏茅口变电所投人运行", "220千伏茅口变电所投入运行"),
    ("运行35东辛", "35干伏东辛线88~93号", "35千伏东辛线88~93号"),
    ("运行220带电", "掌握220干伏带电落瓶清扫技能", "掌握220千伏带电落瓶清扫技能"),
    ("运行220茅口", "首次对220于伏茅口变电所", "首次对220千伏茅口变电所"),
    ("运行220线路", "更换220于伏线路耐张零值瓷瓶", "更换220千伏线路耐张零值瓷瓶"),
    ("检修35油断路器", "35干伏及以上油断路器", "35千伏及以上油断路器"),
    ("检修自己动手", "通过学习、探索，自已动手改造", "通过学习、探索，自己动手改造"),
    ("检修系统完好率", "10干伏至35干伏用电系统", "10千伏至35千伏用电系统"),
    ("线损主变损失", "主变损失53万于瓦时", "主变损失53万千瓦时"),
    ("线损10千伏", "20条10干伏配电线路", "20条10千伏配电线路"),
    ("线损节电1981", "节电294方千瓦时", "节电294万千瓦时"),
    ("线损淮海盐", "撤销准海盐调度所后", "撤销淮海盐调度所后"),
    ("线损淮海线", "原110千伏刘灌线（原准海线一部分）", "原110千伏刘灌线（原淮海线一部分）"),
    ("线损节电1988", "节电809万于瓦时", "节电809万千瓦时"),
    ("线损节电1990", "节电377.7方千瓦时", "节电377.7万千瓦时"),
    ("线损农网", "农网损失电量3732方于瓦时", "农网损失电量3732万千瓦时"),
    ("安全投入", "即投人运行的配电变压器烧毁", "即投入运行的配电变压器烧毁"),
]

SKIPPED = [
    "继续保留表25-4、表25-5及线损率长段的表格压平问题，后续按表格/长段专项处理。",
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
        "principle": "仅修复页级 OCR 清楚给出正确写法的第二十五卷短错识；表格压平残文另行专项。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# 第二十五卷电力工业高置信错识第四批回源修复",
        "",
        f"- 时间：{now}",
        f"- 范围：{payload['scope']}",
        f"- 源文：`{SOURCE}`",
        f"- 阅读器：`{HTML}`",
        f"- 本批核验修复：{verified_items} 项",
        f"- 本次脚本复跑实际改写：{current_changes} 处",
        "- 重点：继续修正发电、主干线路、变电所、运行检修和线损率段落中的 `于/干/方/准/自已/投人` 类 OCR 错识。",
        "- 保留：表25-4、表25-5及线损率长段的表格压平问题，后续按表格/长段专项处理。",
        "",
    ]
    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")
    PROGRESS.write_text("\n".join(lines), encoding="utf-8")
    memory = f"""
## 2026-07-04 第二十五卷电力工业高置信错识第四批回源修复

- 继续对第二十五卷电力工业做小批回源修复，范围限定在 `第二十五卷-电力工业` 到 `第二十六卷-矿产` 前。
- 源文依据：`{SOURCE}`。
- 修复示例：`工于1976年5月`→`竣工于1976年5月`，`6000于瓦/8000于伏安/10干伏/220干伏` 等单位错识，`准海盐/准海线`→`淮海盐/淮海线`，以及 `自已/投人` 等错识。
- 本批核验修复 {verified_items} 项；表25-4、表25-5及线损率长段压平残文继续保留给后续专项。
- 报告：`output/reports/reader_readability_power_batch4_20260704.md`。
"""
    append_once(MEMORY, "## 2026-07-04 第二十五卷电力工业高置信错识第四批回源修复", memory)


def main() -> None:
    counts = patch_reader()
    write_reports(counts)
    print(json.dumps({"current_run_replacements": sum(counts.values()), "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
