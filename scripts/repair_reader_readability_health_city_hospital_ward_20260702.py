# -*- coding: utf-8 -*-
"""Split ward management headings and OCR slips in city hospital management."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_health_city_hospital_ward_20260702.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_health_city_hospital_ward_20260702.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260702_第五十五卷城市医院病区管理标题与OCR修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SOURCE_NOTE = (
    "workbench/body_chapters/连云港市志_全书_正文汇总.md:101072-101088; "
    "workbench/body_chapters/第五十二卷至第六十卷及附录（下part02）.md:7768-7784; "
    "workbench/ocr/paddle_ocr/下/part02/page_0194.txt:24-37; "
    "workbench/ocr/paddle_ocr/下/part02/page_0195.txt:4-16"
)
SCOPE_START = '<h4 id="第五十五卷-第四章医政 药政-第三节城市医院管理">第三节城市医院管理</h4>'
SCOPE_END = "<p>三、急救和输血管理"

REPLACEMENTS: list[tuple[str, str, str]] = [
    (
        "二、病区管理与管理体制标题",
        "<p>二、病区管理管理体制民国8年（1919年），海州义德医院",
        "<p><strong>二、病区管理</strong></p>\n<p><strong>管理体制</strong></p>\n<p>民国8年（1919年），海州义德医院",
    ),
    (
        "工作、管理制度标题",
        "<p>工作、管理制度义德医院在病区建立",
        "<p><strong>工作、管理制度</strong></p>\n<p>义德医院在病区建立",
    ),
    ("病人入院", "病人人院预交保证金", "病人入院预交保证金"),
    ("入院规则", "以及人院规则、出院规则", "以及入院规则、出院规则"),
    ("统一全市", "按《江苏省病历书写规范》要求，统全市住院病历", "按《江苏省病历书写规范》要求，统一全市住院病历"),
]

EXPECTED_TEXT = [
    "<p><strong>二、病区管理</strong></p>",
    "<p><strong>管理体制</strong></p>",
    "<p><strong>工作、管理制度</strong></p>",
    "病人入院预交保证金",
    "以及入院规则、出院规则",
    "统一全市住院病历书写格式",
]
RESIDUALS = [
    "二、病区管理管理体制",
    "工作、管理制度义德医院",
    "病人人院预交保证金",
    "以及人院规则、出院规则",
    "统全市住院病历",
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
        raise RuntimeError(f"city hospital ward expected text missing: {missing}")
    remaining = [marker for marker in RESIDUALS if marker in segment]
    if remaining:
        raise RuntimeError(f"city hospital ward residue remains: {remaining}")
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
        "scope": "第五十五卷卫生 / 第四章医政 药政 / 第三节城市医院管理 / 二、病区管理",
        "source": SOURCE_NOTE,
        "reader_path": str(HTML),
        "changes_this_run": changed,
        "counts": counts,
        "principle": "依据 PaddleOCR 页级文本拆分病区管理小节及分项标题，并修正入院、统一全市等明确 OCR 错字；未处理三、急救和输血管理。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    md = f"""# 第五十五卷城市医院病区管理标题与 OCR 修复

- 时间：{now}
- 范围：`第五十五卷卫生 / 第四章医政 药政 / 第三节城市医院管理 / 二、病区管理`
- 源文依据：`{SOURCE_NOTE}`

## 修复动作

- 拆分 `二、病区管理` 小节标题。
- 拆分 `管理体制`、`工作、管理制度` 两个分项标题。
- 修正 `病人人院预交保证金` 为 `病人入院预交保证金`。
- 修正 `人院规则` 为 `入院规则`。
- 修正 `统全市住院病历书写格式` 为 `统一全市住院病历书写格式`。
- 本次复跑新增替换：{changed} 处。
- 本轮未处理 `三、急救和输血管理`。

## 核对说明

- PaddleOCR `page_0194.txt` 确认 `二、病区管理`、`管理体制`、`工作、管理制度` 及 `病人入院预交保证金`。
- PaddleOCR `page_0195.txt` 确认 `入院规则`、`统一全市住院病历书写格式`。
"""
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")


def update_memory(changed: int) -> None:
    marker = "## 2026-07-02 第五十五卷城市医院病区管理标题与 OCR 修复"
    memory = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker in memory:
        return
    entry = f"""
{marker}

- 对第五十五卷卫生第四章第三节 `城市医院管理` 的 `二、病区管理` 进行回源修复。
- 源文依据：`{SOURCE_NOTE}`；拆分 `二、病区管理`、`管理体制`、`工作、管理制度` 标题。
- 修正 `病人入院预交保证金`、`入院规则`、`统一全市住院病历书写格式` 三处 OCR 明确错字。
- 本轮新增替换 {changed} 处；`三、急救和输血管理` 未在本脚本中处理。
- 报告：`output/reports/reader_readability_health_city_hospital_ward_20260702.md`。
"""
    MEMORY.write_text(memory.rstrip() + "\n\n" + entry.lstrip(), encoding="utf-8")


def main() -> None:
    changed, counts = patch_reader()
    write_reports(changed, counts)
    update_memory(changed)
    print("city hospital ward section repaired")
    print(f"changes={changed}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()
