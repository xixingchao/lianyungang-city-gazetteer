# -*- coding: utf-8 -*-
"""Split and source-correct the front part of the western medicine section."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_health_western_medicine_front_20260702.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_health_western_medicine_front_20260702.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260702_第五十五卷西医前段标题与OCR修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SOURCE_NOTE = (
    "workbench/body_chapters/连云港市志_全书_正文汇总.md:100638-100704; "
    "workbench/body_chapters/第五十二卷至第六十卷及附录（下part02）.md:7338-7404; "
    "workbench/ocr/paddle_ocr/下/part02/page_0183.txt; "
    "workbench/ocr/paddle_ocr/下/part02/page_0184.txt; "
    "workbench/ocr/paddle_ocr/下/part02/page_0185.txt"
)
SCOPE_START = '<h4 id="第五十五卷-第三章医疗-第二节西医">第二节西医</h4>'
SCOPE_END = '<p>普外科'

REPLACEMENTS: list[tuple[str, str, str]] = [
    ("一、起源和发展标题", "<p>一、起源和发展清光绪三十四年", "<p><strong>一、起源和发展</strong></p>\n<p>清光绪三十四年"),
    (
        "二、诊疗技术与心血管内科标题",
        "<p>二、诊疗技术心血管内科1954年，",
        "<p><strong>二、诊疗技术</strong></p>\n<p><strong>心血管内科</strong></p>\n<p>1954年，",
    ),
    ("心血管字形", "建立心迦管实验室", "建立心血管实验室"),
    ("心血管缺字", "置入心脏起搏消化内科1958年", "置入心脏起搏器。</p>\n<p><strong>消化内科</strong></p>\n<p>1958年"),
    ("消化内科字形", "透人疗法", "透入疗法"),
    ("消化内科字形", "消化道导物取出", "消化道异物取出"),
    ("消化内科字形", "1990年,对责门失弛缓症", "1990年，对贲门失弛缓症"),
    ("呼吸内科标题", "<p>呼吸内科1952年", "<p><strong>呼吸内科</strong></p>\n<p>1952年"),
    ("呼吸内科标点", "1960年,用", "1960年，用"),
    ("呼吸内科标点", "1975年,市结核", "1975年，市结核"),
    ("呼吸内科字形", "治疗略血", "治疗咯血"),
    ("呼吸内科标点", "1978年,采用", "1978年，采用"),
    ("呼吸内科标点", "1981年,开展", "1981年，开展"),
    ("肾内科标题", "<p>肾内科1963年", "<p><strong>肾内科</strong></p>\n<p>1963年"),
    ("肾内科字形", "抢救成功-肾功能衰竭", "抢救成功一肾功能衰竭"),
    ("神经内科标题", "<p>神经内科1977年", "<p><strong>神经内科</strong></p>\n<p>1977年"),
    ("神经内科字形", "格林巴利综合症", "格林一巴利综合症"),
    ("内分泌科标题", "<p>内分泌科1959年", "<p><strong>内分泌科</strong></p>\n<p>1959年"),
    ("内分泌科字形", "1985年，并展尿", "1985年，开展尿"),
    ("内分泌科字形", "B2微球蛋白", "B2-微球蛋白"),
]

RESIDUALS = [
    "一、起源和发展清光绪",
    "二、诊疗技术心血管内科",
    "心迦管实验室",
    "置入心脏起搏消化内科",
    "透人疗法",
    "消化道导物取出",
    "责门失弛缓症",
    "呼吸内科1952年",
    "治疗略血",
    "肾内科1963年",
    "抢救成功-肾功能衰竭",
    "神经内科1977年",
    "格林巴利综合症",
    "内分泌科1959年",
    "并展尿",
    "B2微球蛋白",
]
EXPECTED_HEADINGS = [
    "一、起源和发展",
    "二、诊疗技术",
    "心血管内科",
    "消化内科",
    "呼吸内科",
    "肾内科",
    "神经内科",
    "内分泌科",
]


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
        raise RuntimeError(f"western medicine front heading markers missing: {missing}")
    remaining = [marker for marker in RESIDUALS if marker in segment]
    if remaining:
        raise RuntimeError(f"western medicine front OCR residue remains: {remaining}")
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
        "scope": "第五十五卷卫生 / 第三章医疗 / 第二节西医前段",
        "source": SOURCE_NOTE,
        "reader_path": str(HTML),
        "changes_this_run": changed,
        "counts": counts,
        "target_headings": EXPECTED_HEADINGS,
        "principle": "依据 PaddleOCR 页级文本，拆分西医前段标题，并修复起源、心血管、消化、呼吸、肾、神经、内分泌相关可证 OCR 错误；未处理普外科及后续。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    md = f"""# 第五十五卷西医前段标题与 OCR 修复

- 时间：{now}
- 范围：`第五十五卷卫生 / 第三章医疗 / 第二节西医` 前段，至 `普外科` 前
- 源文依据：`{SOURCE_NOTE}`

## 修复动作

- 拆分 `一、起源和发展`、`二、诊疗技术` 2 个主条目标题。
- 拆分 `心血管内科`、`消化内科`、`呼吸内科`、`肾内科`、`神经内科`、`内分泌科` 6 个诊疗技术分项标题。
- 依据 PaddleOCR `page_0184.txt`，补回心血管内科末尾 `置入心脏起搏器。`，并拆出 `消化内科`。
- 依据 PaddleOCR `page_0184.txt` 至 `page_0185.txt`，修复 `心血管实验室`、`透入疗法`、`消化道异物取出`、`贲门失弛缓症`、`治疗咯血`、`抢救成功一肾功能衰竭`、`B2-微球蛋白` 等可证字词。
- 本次复跑新增替换：{changed} 处。
- 本轮未处理 `普外科` 及后续外科系统。

## 核对说明

- PaddleOCR `page_0183.txt` 至 `page_0184.txt` 确认 `第二节西医 / 一、起源和发展 / 二、诊疗技术` 及心血管、消化、呼吸、肾内科边界。
- PaddleOCR `page_0185.txt` 确认神经内科、内分泌科边界及本轮修复字词。
"""
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")


def update_memory(changed: int) -> None:
    marker = "## 2026-07-02 第五十五卷西医前段标题与OCR修复"
    memory = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker in memory:
        return
    entry = f"""
{marker}

- 对第五十五卷卫生第三章第二节 `西医` 前段进行回源修复，范围截至 `普外科` 前。
- 源文依据：`{SOURCE_NOTE}`；确认 `一、起源和发展`、`二、诊疗技术` 及心血管、消化、呼吸、肾、神经、内分泌科为独立标题或分项起点。
- 阅读版拆分 8 个标题/分项，并补回心血管内科末尾 `置入心脏起搏器。`；修复 `心血管实验室`、`消化道异物取出`、`贲门失弛缓症`、`治疗咯血`、`B2-微球蛋白` 等页级 OCR 可证字词。
- 本轮新增替换 {changed} 处；`普外科` 及后续外科系统未在本脚本中处理。
- 报告：`output/reports/reader_readability_health_western_medicine_front_20260702.md`。
"""
    MEMORY.write_text(memory.rstrip() + "\n\n" + entry.lstrip(), encoding="utf-8")


def main() -> None:
    changed, counts = patch_reader()
    write_reports(changed, counts)
    update_memory(changed)
    print("western medicine front section repaired")
    print(f"changes={changed}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()
