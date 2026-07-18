# -*- coding: utf-8 -*-
"""Split and source-correct endemic-disease subheadings in volume 55."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_health_endemic_disease_subheads_20260702.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_health_endemic_disease_subheads_20260702.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260702_第五十五卷地方病防治标题与OCR修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SOURCE_NOTE = (
    "workbench/body_chapters/连云港市志_全书_正文汇总.md:100567-100578; "
    "workbench/body_chapters/第五十二卷至第六十卷及附录（下part02）.md:7267-7278; "
    "workbench/ocr/paddle_ocr/下/part02/page_0181.txt"
)
SCOPE_START = '<h4 id="第五十五卷-第二章常见病防治-第三节地方病防治">第三节地方病防治</h4>'
SCOPE_END = '<h4 id="第五十五卷-第二章常见病防治-第四节计划免疫">第四节计划免疫</h4>'

REPLACEMENTS: list[tuple[str, str, str]] = [
    ("一、地方性氟中毒标题", "<p>一、地方性氟中毒1983年", "<p><strong>一、地方性氟中毒</strong></p>\n<p>1983年"),
    ("地方性氟中毒字形", "受益65.13方人", "受益65.13万人"),
    ("二、地方性甲状腺肿标题", "<p>二、地方性甲状腺肿1983年", "<p><strong>二、地方性甲状腺肿</strong></p>\n<p>1983年"),
    ("地方性甲状腺肿字形", "甲状腺1~I度", "甲状腺Ⅰ~Ⅱ度"),
    ("地方性甲状腺肿标点", "1985年,对", "1985年，对"),
    ("地方性甲状腺肿标点", "下降17.6% 。", "下降17.6%。"),
]

RESIDUALS = [
    "一、地方性氟中毒1983年",
    "二、地方性甲状腺肿1983年",
    "65.13方人",
    "甲状腺1~I度",
    "1985年,对",
    "17.6% 。",
]
EXPECTED_HEADINGS = ["一、地方性氟中毒", "二、地方性甲状腺肿"]


def patch_segment(segment: str) -> tuple[str, int, dict[str, int]]:
    changed = 0
    counts: dict[str, int] = {}
    for label, needle, replacement in REPLACEMENTS:
        count = segment.count(needle)
        if count:
            segment = segment.replace(needle, replacement)
            counts[label] = count
            changed += count

    missing = [h for h in EXPECTED_HEADINGS if f"<p><strong>{h}</strong></p>" not in segment]
    if missing:
        raise RuntimeError(f"endemic-disease heading markers missing: {missing}")
    remaining = [marker for marker in RESIDUALS if marker in segment]
    if remaining:
        raise RuntimeError(f"endemic-disease OCR residue remains: {remaining}")
    return segment, changed, counts


def patch_reader() -> tuple[int, dict[str, int]]:
    text = HTML.read_text(encoding="utf-8")
    start = text.index(SCOPE_START)
    end = text.index(SCOPE_END, start)
    segment = text[start:end]
    new_segment, changed, counts = patch_segment(segment)
    if new_segment != segment:
        HTML.write_text(text[:start] + new_segment + text[end:], encoding="utf-8")
    return changed, counts


def write_reports(changed: int, counts: dict[str, int]) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "第五十五卷卫生 / 第二章常见病防治 / 第三节地方病防治",
        "source": SOURCE_NOTE,
        "reader_path": str(HTML),
        "changes_this_run": changed,
        "target_headings": EXPECTED_HEADINGS,
        "counts": counts,
        "principle": "依据 PaddleOCR 页级文本，拆分地方病防治条目标题，并修复本节内源文明确支持的少量 OCR 字形和标点错误；未处理第四节。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    md = f"""# 第五十五卷地方病防治标题与 OCR 修复

- 时间：{now}
- 范围：`第五十五卷卫生 / 第二章常见病防治 / 第三节地方病防治`
- 源文依据：`{SOURCE_NOTE}`

## 修复动作

- 拆分 `一、地方性氟中毒`、`二、地方性甲状腺肿` 2 个条目标题。
- 依据 PaddleOCR `page_0181.txt`，修复 `受益65.13方人` 为 `受益65.13万人`。
- 依据 PaddleOCR `page_0181.txt`，修复 `甲状腺1~I度` 为 `甲状腺Ⅰ~Ⅱ度`，并同步清理本节内可证标点。
- 本轮目标标题 2 个；本次复跑新增替换：{changed} 处。
- 本轮未处理第四节 `计划免疫`。

## 核对说明

- 正文汇总与下册 part02 正文均显示 `地方性氟中毒`、`地方性甲状腺肿` 为独立条目标题。
- PaddleOCR `page_0181.txt` 确认 `65.13万人`、`甲状腺Ⅰ~Ⅱ度`、`下降17.6%。` 等字词与标点。
"""
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")


def update_memory(changed: int) -> None:
    marker = "## 2026-07-02 第五十五卷地方病防治标题与OCR修复"
    memory = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker in memory:
        return
    entry = f"""
{marker}

- 对第五十五卷卫生第二章第三节 `地方病防治` 进行回源修复。
- 源文依据：`{SOURCE_NOTE}`；确认 `地方性氟中毒`、`地方性甲状腺肿` 为独立条目标题。
- 阅读版拆分 2 个标题，并补正 `65.13万人`、`甲状腺Ⅰ~Ⅱ度` 等页级 OCR 可证字词。
- 本轮新增替换 {changed} 处；第四节 `计划免疫` 未在本脚本中处理。
- 报告：`output/reports/reader_readability_health_endemic_disease_subheads_20260702.md`。
"""
    MEMORY.write_text(memory.rstrip() + "\n\n" + entry.lstrip(), encoding="utf-8")


def main() -> None:
    changed, counts = patch_reader()
    write_reports(changed, counts)
    update_memory(changed)
    print("endemic-disease section repaired")
    print(f"changes={changed}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()
