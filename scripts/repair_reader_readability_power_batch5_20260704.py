# -*- coding: utf-8 -*-
"""Repair fifth source-verified batch in Volume 25 power industry."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_power_batch5_20260704.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_power_batch5_20260704.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260704_第二十五卷电力工业表25-5残表头及高置信错识回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SCOPE_START = '<h2 id="第二十五卷-电力工业">第二十五卷电力工业</h2>'
SCOPE_END = '<h2 id="第二十六卷-矿产">第二十六卷矿产</h2>'
SOURCE = "workbench/ocr/paddle_ocr/中/part01/page_0363.txt; page_0366.txt; page_0367.txt; page_0368.txt; page_0371.txt; page_0372.txt; page_0375.txt; page_0376.txt"

REPLACEMENTS = [
    ("表25-5残表头", "\n\n<p>线损率（%）</p>\n<p>线损率（%）</p>\n\n", "\n\n"),
    ("居民生活用电", "年用电11040方千瓦时", "年用电11040万千瓦时"),
    ("1960食品业用电", "食品业用电971方千瓦时", "食品业用电971万千瓦时"),
    ("1985食品工业用电", "食品工业用电9243方千瓦时", "食品工业用电9243万千瓦时"),
    ("1990采盐业用电", "采盐业用电5775万干瓦时", "采盐业用电5775万千瓦时"),
    ("1990化工用电", "化工用电34299方千瓦时", "化工用电34299万千瓦时"),
    ("农电3.3千伏", "配电电压为3.3于伏", "配电电压为3.3千伏"),
    ("电力平衡淮海盐一", "并入准海盐电网运行", "并入淮海盐电网运行"),
    ("电力平衡淮海盐二", "由准海盐电网中心调度所", "由淮海盐电网中心调度所"),
    ("电力平衡淮海盐三", "占准海盐电网总负荷", "占淮海盐电网总负荷"),
    ("电力平衡淮海盐四", "准海盐电网并人省电网运行", "淮海盐电网并入省电网运行"),
    ("电力平衡统一分配", "负荷由省统一一分配", "负荷由省统一分配"),
    ("1990社会节电", "比省定指标2800方千瓦时", "比省定指标2800万千瓦时"),
    ("业务一条龙", "对用户实行一一条龙服务", "对用户实行一条龙服务"),
    ("业务容量", "容量为2287.18于瓦", "容量为2287.18千瓦"),
    ("电度表校验", "10万于瓦时及以上半年1次", "10万千瓦时及以上半年1次"),
]

SKIPPED = [
    "表25-5正文残表头已删；表25-4及其它长段压平问题继续按后续专项处理。",
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
    missing = [new for _label, _old, new in REPLACEMENTS if new and new not in segment]
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
    payload = {
        "time": now,
        "scope": "第二十五卷电力工业",
        "source": SOURCE,
        "reader_path": str(HTML),
        "verified_items": len(REPLACEMENTS),
        "current_run_replacements": current_changes,
        "counts": counts,
        "skipped": SKIPPED,
        "principle": "删除已由 LYG-中-T036 verified 表承接的表25-5残表头；其余仅修页级 OCR 清楚给出的短错识。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# 第二十五卷电力工业表25-5残表头及高置信错识回源修复",
        "",
        f"- 时间：{now}",
        f"- 范围：{payload['scope']}",
        f"- 源文：`{SOURCE}`",
        f"- 阅读器：`{HTML}`",
        f"- 本批核验修复：{payload['verified_items']} 项",
        f"- 本次脚本复跑实际改写：{current_changes} 处",
        "- 表格：删除已由 `LYG-中-T036` verified 结构化表承接的表25-5正文残表头。",
        "- 短错识：修正用电结构、电力平衡、营业和电能计量段落中的 `方/干/于/准/一一` 类 OCR 错识。",
        "- 保留：表25-4及其它长段压平问题继续按后续专项处理。",
        "",
    ]
    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")
    PROGRESS.write_text("\n".join(lines), encoding="utf-8")
    memory = f"""
## 2026-07-04 第二十五卷电力工业表25-5残表头及高置信错识回源修复

- 继续对第二十五卷电力工业做小批回源修复，范围限定在 `第二十五卷-电力工业` 到 `第二十六卷-矿产` 前。
- 源文依据：`{SOURCE}`。
- 删除正文中已由 `workbench/table_entries/中/data/LYG-中-T036.json` verified 表承接的表25-5残表头 `线损率（%）` 两行。
- 修复示例：`11040方千瓦时/971方千瓦时/5775万干瓦时/3.3于伏/准海盐电网并人省电网/一一条龙服务/2287.18于瓦` 等。
- 本批核验修复 {payload['verified_items']} 项；表25-4及其它长段压平问题继续保留给后续专项。
- 报告：`output/reports/reader_readability_power_batch5_20260704.md`。
"""
    append_once(MEMORY, "## 2026-07-04 第二十五卷电力工业表25-5残表头及高置信错识回源修复", memory)


def main() -> None:
    counts = patch_reader()
    write_reports(counts)
    print(json.dumps({"current_run_replacements": sum(counts.values()), "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
