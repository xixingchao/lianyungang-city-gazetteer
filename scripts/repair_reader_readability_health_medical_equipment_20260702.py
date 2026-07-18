# -*- coding: utf-8 -*-
"""Split and source-correct the medical equipment subsection."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_health_medical_equipment_20260702.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_health_medical_equipment_20260702.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260702_第五十五卷医疗器械设备标题与OCR修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SOURCE_NOTE = (
    "workbench/body_chapters/连云港市志_全书_正文汇总.md:100868-100910; "
    "workbench/body_chapters/第五十二卷至第六十卷及附录（下part02）.md:7568-7612; "
    "workbench/ocr/paddle_ocr/下/part02/page_0189.txt; "
    "workbench/ocr/paddle_ocr/下/part02/page_0190.txt"
)
SCOPE_START_OPTIONS = ('<p>三、医疗器械设备', '<p><strong>三、医疗器械设备</strong></p>')
SCOPE_END = '<h4 id="第五十五卷-第三章医疗-第三节中西医结合">第三节中西医结合</h4>'

REPLACEMENTS: list[tuple[str, str, str]] = [
    (
        "三、医疗器械设备与放射诊断设备标题",
        "<p>三、医疗器械设备放射诊断设备民国5年",
        "<p><strong>三、医疗器械设备</strong></p>\n<p><strong>放射诊断设备</strong></p>\n<p>民国5年",
    ),
    ("放射诊断设备字形", "市第-人民医院", "市第一人民医院"),
    ("检验诊断设备标题", "<p>检验诊断设备民国3年", "<p><strong>检验诊断设备</strong></p>\n<p>民国3年"),
    ("其它诊断设备标题", "<p>其它诊断设备民国35年", "<p><strong>其它诊断设备</strong></p>\n<p>民国35年"),
    (
        "其它诊断设备缺文",
        "1984年后，各医院又添置二维心音监护仪、体外反搏装置、动态心电图机、心脏急救监护仪等。",
        "1984年后，各医院又添置二维心超、多功能脑立体定位仪、肺功能自动诊断仪、多功能程控心脏刺激仪、床边监护仪、胎心音监护仪、体外反搏装置、动态心电图机、心脏急救监护仪等。",
    ),
    ("外科治疗设备标题", "<p>外科治疗设备新浦", "<p><strong>外科治疗设备</strong></p>\n<p>新浦"),
    ("五官科治疗器械标题", "<p>五官科治疗器械建国前", "<p><strong>五官科治疗器械</strong></p>\n<p>建国前"),
    ("五官科治疗器械年份", "19501960年", "1950～1960年"),
    ("五官科治疗器械字形", "遂步添置", "逐步添置"),
    ("其它治疗设备标题", "<p>其它治疗设备建国前", "<p><strong>其它治疗设备</strong></p>\n<p>建国前"),
    ("其它治疗设备字形", "氨氯激光治疗机", "氮氖激光治疗机"),
]

EXPECTED_HEADINGS = [
    "三、医疗器械设备",
    "放射诊断设备",
    "检验诊断设备",
    "其它诊断设备",
    "外科治疗设备",
    "五官科治疗器械",
    "其它治疗设备",
]
RESIDUALS = [
    "三、医疗器械设备放射诊断设备",
    "<p>检验诊断设备民国3年",
    "<p>其它诊断设备民国35年",
    "<p>外科治疗设备新浦",
    "<p>五官科治疗器械建国前",
    "<p>其它治疗设备建国前",
    "市第-人民医院",
    "二维心音监护仪",
    "19501960年",
    "遂步添置",
    "氨氯激光治疗机",
]


def find_scope(text: str) -> tuple[int, int]:
    starts = [text.find(marker) for marker in SCOPE_START_OPTIONS]
    valid_starts = [start for start in starts if start != -1]
    if not valid_starts:
        raise RuntimeError("medical equipment scope start not found")
    start = min(valid_starts)
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

    missing = [h for h in EXPECTED_HEADINGS if f"<p><strong>{h}</strong></p>" not in segment]
    if missing:
        raise RuntimeError(f"medical equipment heading markers missing: {missing}")
    remaining = [marker for marker in RESIDUALS if marker in segment]
    if remaining:
        raise RuntimeError(f"medical equipment OCR residue remains: {remaining}")
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
        "scope": "第五十五卷卫生 / 第三章医疗 / 第二节西医 / 三、医疗器械设备",
        "source": SOURCE_NOTE,
        "reader_path": str(HTML),
        "changes_this_run": changed,
        "counts": counts,
        "target_headings": EXPECTED_HEADINGS,
        "principle": "依据 PaddleOCR 页级文本拆分医疗器械设备主标题与分项标题，并修复源页可证 OCR 错字和缺文。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    md = f"""# 第五十五卷医疗器械设备标题与 OCR 修复

- 时间：{now}
- 范围：`第五十五卷卫生 / 第三章医疗 / 第二节西医 / 三、医疗器械设备`
- 源文依据：`{SOURCE_NOTE}`

## 修复动作

- 拆分 `三、医疗器械设备` 主标题。
- 拆分 `放射诊断设备`、`检验诊断设备`、`其它诊断设备`、`外科治疗设备`、`五官科治疗器械`、`其它治疗设备` 6 个设备分项标题。
- 依据 PaddleOCR `page_0189.txt` 修复 `市第一人民医院`，并补正 `二维心超、多功能脑立体定位仪、肺功能自动诊断仪、多功能程控心脏刺激仪、床边监护仪、胎心音监护仪` 等设备名缺文。
- 依据 PaddleOCR `page_0190.txt` 修复 `1950～1960年`、`逐步添置`、`氮氖激光治疗机` 等可证字词。
- 本次复跑新增替换：{changed} 处。
- 本轮未处理 `第三节中西医结合` 及后续内容。

## 核对说明

- PaddleOCR `page_0189.txt` 确认 `三、医疗器械设备`、放射诊断设备、检验诊断设备、其它诊断设备、外科治疗设备边界。
- PaddleOCR `page_0190.txt` 确认外科治疗设备续段、五官科治疗器械、其它治疗设备及 `第三节中西医结合` 边界。
"""
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")


def update_memory(changed: int) -> None:
    marker = "## 2026-07-02 第五十五卷医疗器械设备标题与OCR修复"
    memory = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker in memory:
        return
    entry = f"""
{marker}

- 对第五十五卷卫生第三章第二节 `西医` 的 `三、医疗器械设备` 段进行回源修复。
- 源文依据：`{SOURCE_NOTE}`；确认主标题和 6 个设备分项标题，并据页级 OCR 修复 `市第一人民医院`、`二维心超...胎心音监护仪`、`1950～1960年`、`逐步添置`、`氮氖激光治疗机` 等可证字词。
- 本轮新增替换 {changed} 处；`第三节中西医结合` 及后续内容未在本脚本中处理。
- 报告：`output/reports/reader_readability_health_medical_equipment_20260702.md`。
"""
    MEMORY.write_text(memory.rstrip() + "\n\n" + entry.lstrip(), encoding="utf-8")


def main() -> None:
    changed, counts = patch_reader()
    write_reports(changed, counts)
    update_memory(changed)
    print("medical equipment section repaired")
    print(f"changes={changed}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()
