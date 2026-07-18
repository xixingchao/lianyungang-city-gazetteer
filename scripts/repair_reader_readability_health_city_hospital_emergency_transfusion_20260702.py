# -*- coding: utf-8 -*-
"""Split emergency/transfusion headings and an OCR slip in city hospital management."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_health_city_hospital_emergency_transfusion_20260702.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_health_city_hospital_emergency_transfusion_20260702.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260702_第五十五卷城市医院急救输血管理标题与OCR修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SOURCE_NOTE = (
    "workbench/body_chapters/连云港市志_全书_正文汇总.md:101102-101128; "
    "workbench/body_chapters/第五十二卷至第六十卷及附录（下part02）.md:7798-7824; "
    "workbench/ocr/paddle_ocr/下/part02/page_0195.txt:17-40; "
    "workbench/ocr/paddle_ocr/下/part02/page_0196.txt:3-11"
)
SCOPE_START = '<h4 id="第五十五卷-第四章医政 药政-第三节城市医院管理">第三节城市医院管理</h4>'
SCOPE_END = "<p>四、院内交叉感染管理"

REPLACEMENTS: list[tuple[str, str, str]] = [
    (
        "三、急救和输血管理与急救标题",
        "<p>三、急救和输血管理急救1955年以前",
        "<p><strong>三、急救和输血管理</strong></p>\n<p><strong>急救</strong></p>\n<p>1955年以前",
    ),
    ("除颤起搏器", "呼吸机、心电图机、除起搏器、电动吸引器", "呼吸机、心电图机、除颤起搏器、电动吸引器"),
    (
        "输血标题",
        "<p>输血民国37年（1948年)以前",
        "<p><strong>输血</strong></p>\n<p>民国37年（1948年）以前",
    ),
    ("邳县", "还担负县、新沂县、东海县、赣榆县用血", "还担负邳县、新沂县、东海县、赣榆县用血"),
    ("淮阴", "省内准阴等地发展献血员", "省内淮阴等地发展献血员"),
]

EXPECTED_TEXT = [
    "<p><strong>三、急救和输血管理</strong></p>",
    "<p><strong>急救</strong></p>",
    "<p><strong>输血</strong></p>",
    "呼吸机、心电图机、除颤起搏器、电动吸引器",
    "还担负邳县、新沂县、东海县、赣榆县用血",
    "省内淮阴等地发展献血员",
]
RESIDUALS = [
    "三、急救和输血管理急救1955年以前",
    "呼吸机、心电图机、除起搏器、电动吸引器",
    "<p>输血民国37年",
    "还担负县、新沂县",
    "省内准阴等地发展献血员",
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
        raise RuntimeError(f"city hospital emergency/transfusion expected text missing: {missing}")
    remaining = [marker for marker in RESIDUALS if marker in segment]
    if remaining:
        raise RuntimeError(f"city hospital emergency/transfusion residue remains: {remaining}")
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
        "scope": "第五十五卷卫生 / 第四章医政 药政 / 第三节城市医院管理 / 三、急救和输血管理",
        "source": SOURCE_NOTE,
        "reader_path": str(HTML),
        "changes_this_run": changed,
        "counts": counts,
        "principle": "依据 PaddleOCR 页级文本拆分急救和输血标题，并修正除颤起搏器、邳县、淮阴等明确 OCR 错字；未处理四、院内交叉感染管理。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    md = f"""# 第五十五卷城市医院急救输血管理标题与 OCR 修复

- 时间：{now}
- 范围：`第五十五卷卫生 / 第四章医政 药政 / 第三节城市医院管理 / 三、急救和输血管理`
- 源文依据：`{SOURCE_NOTE}`

## 修复动作

- 拆分 `三、急救和输血管理` 小节标题。
- 拆分 `急救`、`输血` 两个分项标题。
- 修正 `除起搏器` 为 `除颤起搏器`。
- 修正 `担负县、新沂县` 为 `担负邳县、新沂县`。
- 修正 `准阴` 为 `淮阴`。
- 本次复跑新增替换：{changed} 处。
- 本轮未处理 `四、院内交叉感染管理`。

## 核对说明

- PaddleOCR `page_0195.txt` 确认标题边界、`除颤起搏器` 和 `输血` 起始。
- PaddleOCR `page_0196.txt` 确认 `邳县`、`淮阴` 两处地名。
"""
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")


def update_memory(changed: int) -> None:
    marker = "## 2026-07-02 第五十五卷城市医院急救输血管理标题与 OCR 修复"
    memory = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker in memory:
        return
    entry = f"""
{marker}

- 对第五十五卷卫生第四章第三节 `城市医院管理` 的 `三、急救和输血管理` 进行回源修复。
- 源文依据：`{SOURCE_NOTE}`；拆分 `三、急救和输血管理`、`急救`、`输血` 标题。
- 修正 `除颤起搏器`、`邳县`、`淮阴` 三处 OCR 明确错字。
- 本轮新增替换 {changed} 处；`四、院内交叉感染管理` 未在本脚本中处理。
- 报告：`output/reports/reader_readability_health_city_hospital_emergency_transfusion_20260702.md`。
"""
    MEMORY.write_text(memory.rstrip() + "\n\n" + entry.lstrip(), encoding="utf-8")


def main() -> None:
    changed, counts = patch_reader()
    write_reports(changed, counts)
    update_memory(changed)
    print("city hospital emergency/transfusion section repaired")
    print(f"changes={changed}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()
