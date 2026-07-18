# -*- coding: utf-8 -*-
"""Source-correct and lightly split the integrated Chinese-Western medicine section."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_health_integrated_medicine_20260702.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_health_integrated_medicine_20260702.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260702_第五十五卷中西医结合OCR修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SOURCE_NOTE = (
    "workbench/body_chapters/连云港市志_全书_正文汇总.md:100910-100934; "
    "workbench/body_chapters/第五十二卷至第六十卷及附录（下part02）.md:7612-7638; "
    "workbench/ocr/paddle_ocr/下/part02/page_0190.txt; "
    "workbench/ocr/paddle_ocr/下/part02/page_0191.txt"
)
SCOPE_START = '<h4 id="第五十五卷-第三章医疗-第三节中西医结合">第三节中西医结合</h4>'
SCOPE_END = '<h4 id="第五十五卷-第三章医疗-第四节护理">第四节护理</h4>'

REPLACEMENTS: list[tuple[str, str, str]] = [
    ("患者字形", "毒蛇咬伤惠者成功", "毒蛇咬伤患者成功"),
    ("黄疸字形", "传染性黄疽性肝炎", "传染性黄疸性肝炎"),
    ("碎颅缺字", "肠梗阻、碎、胃切除", "肠梗阻、碎颅、胃切除"),
    (
        "新医科缺文",
        "1976年，市新浦人民医院建立新医科诊开诊。",
        "1976年，市新浦人民医院建立新医科（中西医结合科），设床位30张，配备3名西医学中医班毕业的高年资医师，中西医结合门诊开诊。",
    ),
    ("安蛔汤缺字", "用安汤（黄连、甘草", "用安蛔汤（黄连、甘草"),
]

SPLITS: list[tuple[str, str]] = [
    ("。1958年，各医院", "。</p>\n<p>1958年，各医院"),
    ("。1970年，市内", "。</p>\n<p>1970年，市内"),
    ("。1977年，开始针刺", "。</p>\n<p>1977年，开始针刺"),
    ("。1982～1984年，市海州", "。</p>\n<p>1982～1984年，市海州"),
]

RESIDUALS = [
    "毒蛇咬伤惠者成功",
    "传染性黄疽性肝炎",
    "肠梗阻、碎、胃切除",
    "新医科诊开诊",
    "用安汤（黄连、甘草",
]
EXPECTED_TEXT = [
    "毒蛇咬伤患者成功",
    "传染性黄疸性肝炎",
    "肠梗阻、碎颅、胃切除",
    "中西医结合门诊开诊",
    "用安蛔汤（黄连、甘草",
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

    split_count = 0
    for needle, replacement in SPLITS:
        count = segment.count(needle)
        if count:
            segment = segment.replace(needle, replacement)
            split_count += count
            changed += count
    if split_count:
        counts["自然段拆分"] = split_count

    missing = [text for text in EXPECTED_TEXT if text not in segment]
    if missing:
        raise RuntimeError(f"integrated medicine expected corrections missing: {missing}")
    remaining = [marker for marker in RESIDUALS if marker in segment]
    if remaining:
        raise RuntimeError(f"integrated medicine OCR residue remains: {remaining}")
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
        "scope": "第五十五卷卫生 / 第三章医疗 / 第三节中西医结合",
        "source": SOURCE_NOTE,
        "reader_path": str(HTML),
        "changes_this_run": changed,
        "counts": counts,
        "principle": "依据 PaddleOCR 页级文本修复中西医结合节内可证 OCR 错误，并按年代叙述轻量拆分自然段；未处理第四节护理。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    md = f"""# 第五十五卷中西医结合 OCR 修复

- 时间：{now}
- 范围：`第五十五卷卫生 / 第三章医疗 / 第三节中西医结合`
- 源文依据：`{SOURCE_NOTE}`

## 修复动作

- 依据 PaddleOCR `page_0190.txt` 修复 `毒蛇咬伤患者`、`传染性黄疸性肝炎`、`碎颅`、`新医科（中西医结合科）...中西医结合门诊开诊`、`安蛔汤` 等可证字词和缺文。
- 将原单个超长段按年代叙述拆成 5 个自然段。
- 本次复跑新增替换/拆分：{changed} 处。
- 本轮未处理 `第四节护理`。

## 核对说明

- PaddleOCR `page_0190.txt` 确认本节主体段落及上述修复字词。
- PaddleOCR `page_0191.txt` 确认本节尾句和 `第四节护理` 边界。
"""
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")


def update_memory(changed: int) -> None:
    marker = "## 2026-07-02 第五十五卷中西医结合OCR修复"
    memory = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker in memory:
        return
    entry = f"""
{marker}

- 对第五十五卷卫生第三章第三节 `中西医结合` 进行回源修复。
- 源文依据：`{SOURCE_NOTE}`；修复 `毒蛇咬伤患者`、`黄疸性肝炎`、`碎颅`、`新医科（中西医结合科）...门诊开诊`、`安蛔汤` 等页级 OCR 可证字词和缺文。
- 将原单个超长段按年代叙述拆成 5 个自然段；本轮新增替换/拆分 {changed} 处。
- `第四节护理` 未在本脚本中处理。
- 报告：`output/reports/reader_readability_health_integrated_medicine_20260702.md`。
"""
    MEMORY.write_text(memory.rstrip() + "\n\n" + entry.lstrip(), encoding="utf-8")


def main() -> None:
    changed, counts = patch_reader()
    write_reports(changed, counts)
    update_memory(changed)
    print("integrated medicine section repaired")
    print(f"changes={changed}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()
