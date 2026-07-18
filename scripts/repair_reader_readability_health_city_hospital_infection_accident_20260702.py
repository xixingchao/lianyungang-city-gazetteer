# -*- coding: utf-8 -*-
"""Split infection/medical-accident headings in city hospital management."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_health_city_hospital_infection_accident_20260702.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_health_city_hospital_infection_accident_20260702.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260702_第五十五卷城市医院院感与医疗事故标题修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SOURCE_NOTE = (
    "workbench/body_chapters/连云港市志_全书_正文汇总.md:101140-101168; "
    "workbench/body_chapters/第五十二卷至第六十卷及附录（下part02）.md:7836-7864; "
    "workbench/ocr/paddle_ocr/下/part02/page_0196.txt:15-39; "
    "workbench/ocr/paddle_ocr/下/part02/page_0197.txt:3-10"
)
SCOPE_START = '<h4 id="第五十五卷-第四章医政 药政-第三节城市医院管理">第三节城市医院管理</h4>'
SCOPE_END = '<h4 id="第五十五卷-第四章医政 药政-第四节药政管理">第四节药政管理</h4>'

REPLACEMENTS: list[tuple[str, str, str]] = [
    (
        "四、院内交叉感染管理标题",
        "<p>四、院内交叉感染管理1983年，市卫生局责成",
        "<p><strong>四、院内交叉感染管理</strong></p>\n<p>1983年，市卫生局责成",
    ),
    (
        "五、医疗差错事故标题",
        "<p>五、医疗差错事故的防止和处理民国时期已有",
        "<p><strong>五、医疗差错事故的防止和处理</strong></p>\n<p>民国时期已有",
    ),
    ("肠套叠患儿", "一肠套登惠儿行空气压力灌肠复位手术", "一肠套叠患儿行空气压力灌肠复位手术"),
]

EXPECTED_TEXT = [
    "<p><strong>四、院内交叉感染管理</strong></p>",
    "<p><strong>五、医疗差错事故的防止和处理</strong></p>",
    "一肠套叠患儿行空气压力灌肠复位手术",
]
RESIDUALS = [
    "四、院内交叉感染管理1983年",
    "五、医疗差错事故的防止和处理民国时期",
    "一肠套登惠儿行空气压力灌肠复位手术",
]


def find_scope(text: str) -> tuple[int, int]:
    start = text.index(SCOPE_START)
    end = text.index(SCOPE_END, start)
    return start, end


def patch_segment(segment: str) -> tuple[str, int, dict[str, int]]:
    changed = 0
    counts: dict[str, int] = {}
    for label, needle, replacement in REPLACEMENTS:
        count = segment.count(needle)
        if count:
            segment = segment.replace(needle, replacement)
            counts[label] = count
            changed += count

    missing = [text for text in EXPECTED_TEXT if text not in segment]
    if missing:
        raise RuntimeError(f"city hospital infection/accident expected text missing: {missing}")
    remaining = [marker for marker in RESIDUALS if marker in segment]
    if remaining:
        raise RuntimeError(f"city hospital infection/accident residue remains: {remaining}")
    return segment, changed, counts


def patch_reader() -> tuple[int, dict[str, int]]:
    text = HTML.read_text(encoding="utf-8")
    start, end = find_scope(text)
    segment = text[start:end]
    new_segment, changed, counts = patch_segment(segment)
    if new_segment != segment:
        HTML.write_text(text[:start] + new_segment + text[end:], encoding="utf-8")
    return changed, counts


def write_reports(changed: int, counts: dict[str, int]) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "第五十五卷卫生 / 第四章医政 药政 / 第三节城市医院管理 / 四、院内交叉感染管理；五、医疗差错事故的防止和处理",
        "source": SOURCE_NOTE,
        "reader_path": str(HTML),
        "changes_this_run": changed,
        "counts": counts,
        "principle": "依据 PaddleOCR 页级文本拆分两个小节标题，并修正肠套叠患儿一处明确 OCR 错字；未处理第四节药政管理。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    md = f"""# 第五十五卷城市医院院感与医疗事故标题修复

- 时间：{now}
- 范围：`第五十五卷卫生 / 第四章医政 药政 / 第三节城市医院管理 / 四、院内交叉感染管理；五、医疗差错事故的防止和处理`
- 源文依据：`{SOURCE_NOTE}`

## 修复动作

- 拆分 `四、院内交叉感染管理` 小节标题。
- 拆分 `五、医疗差错事故的防止和处理` 小节标题。
- 修正 `肠套登惠儿` 为 `肠套叠患儿`。
- 本次复跑新增替换：{changed} 处。
- 本轮未处理 `第四节药政管理`。

## 核对说明

- PaddleOCR `page_0196.txt` 确认两个小节标题边界和 `肠套叠患儿`。
- PaddleOCR `page_0197.txt` 确认医疗事故小节延续至 `第四节药政管理` 前。
"""
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")


def update_memory(changed: int) -> None:
    marker = "## 2026-07-02 第五十五卷城市医院院感与医疗事故标题修复"
    memory = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker in memory:
        return
    entry = f"""
{marker}

- 对第五十五卷卫生第四章第三节 `城市医院管理` 的 `四、院内交叉感染管理`、`五、医疗差错事故的防止和处理` 进行回源修复。
- 源文依据：`{SOURCE_NOTE}`；拆分两个小节标题。
- 修正 `肠套叠患儿` 一处 OCR 明确错字。
- 本轮新增替换 {changed} 处；`第四节药政管理` 未在本脚本中处理。
- 报告：`output/reports/reader_readability_health_city_hospital_infection_accident_20260702.md`。
"""
    MEMORY.write_text(memory.rstrip() + "\n\n" + entry.lstrip(), encoding="utf-8")


def main() -> None:
    changed, counts = patch_reader()
    write_reports(changed, counts)
    update_memory(changed)
    print("city hospital infection/accident section repaired")
    print(f"changes={changed}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()
