# -*- coding: utf-8 -*-
"""Split and source-correct the tail specialties in the western medicine section."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_health_western_medicine_specialties_tail_20260702.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_health_western_medicine_specialties_tail_20260702.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260702_第五十五卷西医后续专科标题与OCR修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SOURCE_NOTE = (
    "workbench/body_chapters/连云港市志_全书_正文汇总.md:100794-100867; "
    "workbench/body_chapters/第五十二卷至第六十卷及附录（下part02）.md:7493-7568; "
    "workbench/ocr/paddle_ocr/下/part02/page_0187.txt; "
    "workbench/ocr/paddle_ocr/下/part02/page_0188.txt; "
    "workbench/ocr/paddle_ocr/下/part02/page_0189.txt"
)
SCOPE_START_OPTIONS = ('<p>耳鼻咽喉科', '<p><strong>耳鼻咽喉科</strong></p>')
SCOPE_END = '<p>三、医疗器械设备'

REPLACEMENTS: list[tuple[str, str, str]] = [
    ("耳鼻咽喉科标题", "<p>耳鼻咽喉科民国7年", "<p><strong>耳鼻咽喉科</strong></p>\n<p>民国7年"),
    ("耳鼻咽喉科字形", "橙骨切除并安装人工骨", "镫骨切除并安装人工镫骨"),
    ("耳鼻咽喉科字形", "非植人型电子", "非植入型电子"),
    ("口腔科标题", "<p>口腔科清光绪三十四年", "<p><strong>口腔科</strong></p>\n<p>清光绪三十四年"),
    ("口腔科字形", "下领骨切除", "下颌骨切除"),
    ("眼科标题", "<p>眼科1951年", "<p><strong>眼科</strong></p>\n<p>1951年"),
    ("眼科字形", "脸内翻", "睑内翻"),
    ("眼科字形", "裔肉切除", "胬肉切除"),
    ("眼科字形", "上脸下垂", "上睑下垂"),
    ("眼科字形", "治疗脸下垂", "治疗睑下垂"),
    ("眼科字形", "双脸重建", "双睑重建"),
    ("皮肤科标题", "<p>皮肤科1960年", "<p><strong>皮肤科</strong></p>\n<p>1960年"),
    ("皮肤科字形", "血管性化性肉芽肿", "血管性化脓性肉芽肿"),
    ("皮肤科字形", "脸黄疣", "睑黄疣"),
    ("皮肤科字形", "皮肤赞生物", "皮肤赘生物"),
    ("皮肤科缺字", "锶90治疗血管瘤，60治疗皮肤鳞状上癌", "锶90治疗血管瘤，钴60治疗皮肤鳞状上癌"),
    ("检验科标题", "<p>检验科民国3年", "<p><strong>检验科</strong></p>\n<p>民国3年"),
    ("检验科标点", "1988年,进行", "1988年，进行"),
    ("放射科标题", "<p>放射科民国15年", "<p><strong>放射科</strong></p>\n<p>民国15年"),
]

EXPECTED_HEADINGS = ["耳鼻咽喉科", "口腔科", "眼科", "皮肤科", "检验科", "放射科"]
RESIDUALS = [
    "<p>耳鼻咽喉科民国7年",
    "<p>口腔科清光绪三十四年",
    "<p>眼科1951年",
    "<p>皮肤科1960年",
    "<p>检验科民国3年",
    "<p>放射科民国15年",
    "橙骨切除并安装人工骨",
    "非植人型电子",
    "下领骨切除",
    "脸内翻",
    "裔肉切除",
    "上脸下垂",
    "治疗脸下垂",
    "双脸重建",
    "血管性化性肉芽肿",
    "脸黄疣",
    "皮肤赞生物",
    "锶90治疗血管瘤，60治疗皮肤鳞状上癌",
    "1988年,进行",
]
DEFERRED_UNCERTAIN = ["凳下腺", "麦粘肿", "丙酮酸嗨", "B2一微蛋白"]


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
        raise RuntimeError(f"western medicine tail specialty heading markers missing: {missing}")
    remaining = [marker for marker in RESIDUALS if marker in segment]
    if remaining:
        raise RuntimeError(f"western medicine tail specialty OCR residue remains: {remaining}")
    return segment, changed, counts


def patch_reader() -> tuple[int, dict[str, int]]:
    text = HTML.read_text(encoding="utf-8")
    starts = [text.find(marker) for marker in SCOPE_START_OPTIONS]
    valid_starts = [start for start in starts if start != -1]
    if not valid_starts:
        raise RuntimeError("western medicine tail specialty scope start not found")
    start = min(valid_starts)
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
        "scope": "第五十五卷卫生 / 第三章医疗 / 第二节西医 / 耳鼻咽喉科至放射科",
        "source": SOURCE_NOTE,
        "reader_path": str(HTML),
        "changes_this_run": changed,
        "counts": counts,
        "target_headings": EXPECTED_HEADINGS,
        "deferred_uncertain_ocr": DEFERRED_UNCERTAIN,
        "principle": "依据 PaddleOCR 页级文本拆分西医尾段专科标题，并仅修复源页 OCR 能明确支持的字词；OCR 未给出可靠正形者暂缓。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    md = f"""# 第五十五卷西医后续专科标题与 OCR 修复

- 时间：{now}
- 范围：`第五十五卷卫生 / 第三章医疗 / 第二节西医` 的 `耳鼻咽喉科` 至 `放射科`
- 源文依据：`{SOURCE_NOTE}`

## 修复动作

- 拆分 `耳鼻咽喉科`、`口腔科`、`眼科`、`皮肤科`、`检验科`、`放射科` 6 个分项标题。
- 依据 PaddleOCR `page_0187.txt` 修复 `镫骨切除并安装人工镫骨`、`非植入型电子耳蜗`、`下颌骨切除` 等可证字词。
- 依据 PaddleOCR `page_0188.txt` 修复 `睑内翻`、`胬肉切除`、`上睑下垂`、`睑下垂`、`双睑重建`、`血管性化脓性肉芽肿`、`睑黄疣`、`皮肤赘生物`、`钴60` 等可证字词。
- 本次复跑新增替换：{changed} 处。
- 暂缓未改：`凳下腺`、`麦粘肿`、`丙酮酸嗨`、`B2一微蛋白`，原因是当前 OCR 文本未给出足够可靠的源页正形。
- 本轮未处理 `三、医疗器械设备` 及后续设备分项。

## 核对说明

- PaddleOCR `page_0187.txt` 确认耳鼻咽喉科、口腔科前段及其边界。
- PaddleOCR `page_0188.txt` 确认口腔科续段、眼科、皮肤科、检验科和放射科起始。
- PaddleOCR `page_0189.txt` 确认放射科续段与 `三、医疗器械设备` 边界。
"""
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")


def update_memory(changed: int) -> None:
    marker = "## 2026-07-02 第五十五卷西医后续专科标题与OCR修复"
    memory = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker in memory:
        return
    entry = f"""
{marker}

- 对第五十五卷卫生第三章第二节 `西医` 的 `耳鼻咽喉科` 至 `放射科` 段进行回源修复。
- 源文依据：`{SOURCE_NOTE}`；确认 6 个后续专科分项标题，并据页级 OCR 修复 `镫骨`、`非植入型`、`下颌骨`、`睑内翻`、`胬肉`、`睑黄疣`、`赘生物`、`钴60` 等可证字词。
- 本轮新增替换 {changed} 处；`三、医疗器械设备` 及后续设备分项未在本脚本中处理。
- 当前暂缓 `凳下腺`、`麦粘肿`、`丙酮酸嗨`、`B2一微蛋白` 等 OCR 文本未能可靠给出正形的词。
- 报告：`output/reports/reader_readability_health_western_medicine_specialties_tail_20260702.md`。
"""
    MEMORY.write_text(memory.rstrip() + "\n\n" + entry.lstrip(), encoding="utf-8")


def main() -> None:
    changed, counts = patch_reader()
    write_reports(changed, counts)
    update_memory(changed)
    print("western medicine tail specialties repaired")
    print(f"changes={changed}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()
