# -*- coding: utf-8 -*-
"""Split and source-correct the Chinese medicine section in volume 55."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_health_chinese_medicine_20260702.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_health_chinese_medicine_20260702.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260702_第五十五卷中医标题与OCR修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SOURCE_NOTE = (
    "workbench/body_chapters/连云港市志_全书_正文汇总.md:100608-100638; "
    "workbench/body_chapters/第五十二卷至第六十卷及附录（下part02）.md:7307-7338; "
    "workbench/ocr/paddle_ocr/下/part02/page_0182.txt; "
    "workbench/ocr/paddle_ocr/下/part02/page_0183.txt"
)
SCOPE_START = '<h4 id="第五十五卷-第三章医疗-第一节中医">第一节中医</h4>'
SCOPE_END = '<h4 id="第五十五卷-第三章医疗-第二节西医">第二节西医</h4>'

REPLACEMENTS: list[tuple[str, str, str]] = [
    ("一、源流标题", "<p>一、源流灌云县境内伊芦山", "<p><strong>一、源流</strong></p>\n<p>灌云县境内伊芦山"),
    ("源流字形", "迁人者有周藩西", "迁入者有周藩西"),
    ("源流字形", "中医土9人", "中医士9人"),
    (
        "二、医术与内科标题",
        "<p>二、医　术内科市内一些著名医家诊疗及用药各有特色。",
        "<p><strong>二、医术</strong></p>\n<p><strong>内科</strong></p>\n<p>市内一些著名医家诊疗及用药各有特色。",
    ),
    ("儿科标题", "<p>儿科朱少亭", "<p><strong>儿科</strong></p>\n<p>朱少亭"),
    ("外科标题", "<p>外科戴镜波", "<p><strong>外科</strong></p>\n<p>戴镜波"),
    ("外科字形", "名日“掌心雷”", "名曰“掌心雷”"),
    (
        "妇科缺句",
        "<p>母子平安。</p>",
        "<p><strong>妇科</strong></p>\n<p>李达生擅长妇科，曾为一患梅毒的孕妇诊治，以大剂量银花泡水做茶饮，产后母子平安。</p>",
    ),
    ("针灸标题", "<p>针灸冯瑛", "<p><strong>针灸</strong></p>\n<p>冯瑛"),
]

RESIDUALS = [
    "一、源流灌云县境内",
    "迁人者有周藩西",
    "中医土9人",
    "二、医　术内科",
    "儿科朱少亭",
    "外科戴镜波",
    "名日“掌心雷”",
    "<p>母子平安。</p>",
    "针灸冯瑛",
]
EXPECTED_HEADINGS = ["一、源流", "二、医术", "内科", "儿科", "外科", "妇科", "针灸"]


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
        raise RuntimeError(f"Chinese medicine heading markers missing: {missing}")
    remaining = [marker for marker in RESIDUALS if marker in segment]
    if remaining:
        raise RuntimeError(f"Chinese medicine OCR residue remains: {remaining}")
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
        "scope": "第五十五卷卫生 / 第三章医疗 / 第一节中医",
        "source": SOURCE_NOTE,
        "reader_path": str(HTML),
        "changes_this_run": changed,
        "counts": counts,
        "target_headings": EXPECTED_HEADINGS,
        "principle": "依据 PaddleOCR 页级文本，拆分中医小节标题，并补回本节内源文明确支持的缺句和 OCR 字形错误；未处理第二节西医。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    md = f"""# 第五十五卷中医标题与 OCR 修复

- 时间：{now}
- 范围：`第五十五卷卫生 / 第三章医疗 / 第一节中医`
- 源文依据：`{SOURCE_NOTE}`

## 修复动作

- 拆分 `一、源流`、`二、医术` 2 个主条目标题。
- 拆分 `内科`、`儿科`、`外科`、`妇科`、`针灸` 5 个医术分项标题。
- 依据 PaddleOCR `page_0183.txt`，补回当前读者版缺失的妇科段落：`李达生擅长妇科，曾为一患梅毒的孕妇诊治，以大剂量银花泡水做茶饮，产后母子平安。`
- 依据 PaddleOCR `page_0182.txt` 与 `page_0183.txt`，修复 `迁入者`、`中医士9人`、`名曰“掌心雷”` 等可证字词。
- 本次复跑新增替换：{changed} 处。
- 本轮未处理第二节 `西医`。

## 核对说明

- PaddleOCR `page_0182.txt` 确认第三章医疗、第一节中医、一、源流及源流正文。
- PaddleOCR `page_0183.txt` 确认 `二、医术`，以及内科、儿科、外科、妇科、针灸各分项内容。
"""
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")


def update_memory(changed: int) -> None:
    marker = "## 2026-07-02 第五十五卷中医标题与OCR修复"
    memory = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker in memory:
        return
    entry = f"""
{marker}

- 对第五十五卷卫生第三章第一节 `中医` 进行回源修复。
- 源文依据：`{SOURCE_NOTE}`；确认 `一、源流`、`二、医术` 及 `内科/儿科/外科/妇科/针灸` 为独立标题或分项起点。
- 阅读版拆分 7 个标题/分项，并补回 `妇科李达生...产后母子平安。` 缺失句；修复 `迁入者`、`中医士9人`、`名曰“掌心雷”` 等页级 OCR 可证字词。
- 本轮新增替换 {changed} 处；第二节 `西医` 未在本脚本中处理。
- 报告：`output/reports/reader_readability_health_chinese_medicine_20260702.md`。
"""
    MEMORY.write_text(memory.rstrip() + "\n\n" + entry.lstrip(), encoding="utf-8")


def main() -> None:
    changed, counts = patch_reader()
    write_reports(changed, counts)
    update_memory(changed)
    print("Chinese medicine section repaired")
    print(f"changes={changed}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()
