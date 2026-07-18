# -*- coding: utf-8 -*-
"""Split and source-correct parasitic-disease subheadings in volume 55."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_health_parasitic_disease_subheads_20260702.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_health_parasitic_disease_subheads_20260702.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260702_第五十五卷寄生虫病防治标题与OCR修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SOURCE_NOTE = (
    "workbench/body_chapters/连云港市志_全书_正文汇总.md:100498-100557; "
    "workbench/body_chapters/第五十二卷至第六十卷及附录（下part02）.md:7198-7257; "
    "workbench/ocr/paddle_ocr/下/part02/page_0179.txt; "
    "workbench/ocr/paddle_ocr/下/part02/page_0180.txt; "
    "workbench/ocr/paddle_ocr/下/part02/page_0181.txt"
)
SCOPE_START = '<h4 id="第五十五卷-第二章常见病防治-第二节寄生虫病防治">第二节寄生虫病防治</h4>'
SCOPE_END = '<h4 id="第五十五卷-第二章常见病防治-第三节地方病防治">第三节地方病防治</h4>'

REPLACEMENTS: list[tuple[str, str, str]] = [
    ("一、疟疾标题与首句", "<p>一、疮疾市内症疾流行已久", "<p><strong>一、疟疾</strong></p>\n<p>市内疟疾流行已久"),
    ("疟疾段落字形", "疮疾病抗复发治疗", "疟疾病抗复发治疗"),
    ("疟疾段落字形", "应用乙胺啶和氯奎", "应用乙胺嘧啶和氯奎"),
    ("疟疾段落字形", "进行抗症治疗", "进行抗疟治疗"),
    ("疟疾段落字形", "北方地区疾防治技术方案", "北方地区疟疾防治技术方案"),
    ("疟疾段落字形", "疮疾休止期", "疟疾休止期"),
    ("疟疾段落字形", "纳人苏鲁皖豫鄂五省症疾联防范围", "纳入苏鲁皖豫鄂五省疟疾联防范围"),
    ("疟疾段落字形", "统一一安排", "统一安排"),
    ("疟疾段落字形", "消灭症疾病标准", "消灭疟疾病标准"),
    ("疟疾段落字形", "市区症疾发病率", "市区疟疾发病率"),
    ("疟疾段落字形", "全年未发生症疾", "全年未发生疟疾"),
    ("二、黑热病标题", "<p>二、黑热病民国9年", "<p><strong>二、黑热病</strong></p>\n<p>民国9年"),
    ("黑热病段落字形", "新斯波霜", "新斯锑波霜"),
    ("黑热病段落字形", "日军侵人市境", "日军侵入市境"),
    ("黑热病断行", "伪同仁会华北中：</p>\n<p>央防疫处技术员", "伪同仁会华北中央防疫处技术员"),
    ("黑热病段落字形", "采用敌敌沸、", "采用敌敌涕、"),
    ("黑热病段落字形", "灭龄面积", "灭蛉面积"),
    ("三、丝虫病标题", "<p>三、丝虫病建国前", "<p><strong>三、丝虫病</strong></p>\n<p>建国前"),
    ("丝虫病段落字形", "微丝蝴", "微丝蚴"),
    ("丝虫病段落字形", "微丝阳性者", "微丝蚴阳性者"),
    ("丝虫病段落字形", "微丝坳阳性率", "微丝蚴阳性率"),
    ("四、蛔虫病标题", "<p>四、虫病蛔虫病自古即有", "<p><strong>四、蛔虫病</strong></p>\n<p>蛔虫病自古即有"),
    ("蛔虫病段落字形", "进行虫病感染情况调查", "进行蛔虫病感染情况调查"),
    ("蛔虫病段落字形", "按“国际儿童年要求", "按“国际儿童年”要求"),
    ("蛔虫病段落字形", "发现虫阳性者", "发现蛔虫阳性者"),
    ("蛔虫病段落字形", "国家卫生部全国人体寄生虫分布调查”任务", "国家卫生部“全国人体寄生虫分布调查”任务"),
    ("蛔虫病段落字形", "的虫总阳性率", "的蛔虫总阳性率"),
    ("蛔虫病段落字形", "进行虫调查", "进行蛔虫调查"),
    ("五、钩虫病标题", "<p>五、钩虫病1955年", "<p><strong>五、钩虫病</strong></p>\n<p>1955年"),
]

RESIDUALS = [
    "一、疮疾市内症疾",
    "二、黑热病民国9年",
    "三、丝虫病建国前",
    "四、虫病蛔虫病",
    "五、钩虫病1955年",
    "疮疾",
    "症疾",
    "抗症",
    "乙胺啶",
    "新斯波霜",
    "侵人市境",
    "华北中：</p>",
    "敌敌沸",
    "灭龄面积",
    "微丝蝴",
    "微丝坳",
    "发现虫阳性者",
    "的虫总阳性率",
    "进行虫调查",
]
EXPECTED_HEADINGS = [
    "一、疟疾",
    "二、黑热病",
    "三、丝虫病",
    "四、蛔虫病",
    "五、钩虫病",
]


def patch_segment(segment: str) -> tuple[str, int, dict[str, int]]:
    changed = 0
    counts: dict[str, int] = {}
    for label, needle, replacement in REPLACEMENTS:
        count = segment.count(needle)
        if count:
            segment = segment.replace(needle, replacement)
            counts[label] = counts.get(label, 0) + count
            changed += count

    missing = [h for h in EXPECTED_HEADINGS if f"<p><strong>{h}</strong></p>" not in segment]
    if missing:
        raise RuntimeError(f"parasitic-disease heading markers missing: {missing}")
    remaining = [marker for marker in RESIDUALS if marker in segment]
    if remaining:
        raise RuntimeError(f"parasitic-disease OCR residue remains: {remaining}")
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
        "scope": "第五十五卷卫生 / 第二章常见病防治 / 第二节寄生虫病防治",
        "source": SOURCE_NOTE,
        "reader_path": str(HTML),
        "changes_this_run": changed,
        "target_headings": EXPECTED_HEADINGS,
        "counts": counts,
        "principle": "依据 PaddleOCR 页级文本，拆分寄生虫病防治条目标题，并修复本节内源文明确支持的 OCR 字形错误；未处理下一节。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    md = f"""# 第五十五卷寄生虫病防治标题与 OCR 修复

- 时间：{now}
- 范围：`第五十五卷卫生 / 第二章常见病防治 / 第二节寄生虫病防治`
- 源文依据：`{SOURCE_NOTE}`

## 修复动作

- 拆分 `一、疟疾`、`二、黑热病`、`三、丝虫病`、`四、蛔虫病`、`五、钩虫病` 5 个条目标题。
- 依据 PaddleOCR `page_0179.txt` 至 `page_0181.txt`，修复本节中明确的 OCR 字形错误：`疮疾/症疾` 误识为 `疟疾`，`微丝蝴/微丝坳` 误识为 `微丝蚴`，`四、虫病` 补为 `四、蛔虫病`。
- 修复黑热病段落的分页断裂 `华北中：/央防疫处`，补正 `新斯锑波霜`、`敌敌涕`、`灭蛉` 等源页可证字词。
- 修复蛔虫病段落漏字和引号边界：`蛔虫病感染情况调查`、`蛔虫阳性者`、`蛔虫总阳性率`、`全国人体寄生虫分布调查`。
- 本轮目标标题 5 个；本次复跑新增替换：{changed} 处。
- 本轮未处理下一节 `地方病防治`。

## 核对说明

- 当前正文汇总仍保留部分 OCR 误识；本轮以 PaddleOCR 页级文本为主要字形依据。
- PaddleOCR `page_0179.txt` 显示 `第二节寄生虫病防治 / 一、疟疾`，并给出疟疾段落末尾跨页前半。
- PaddleOCR `page_0180.txt` 显示 `二、黑热病`、`三、丝虫病`、`四、蛔虫病`，确认相关疾病名称与段落字词。
- PaddleOCR `page_0181.txt` 显示 `五、钩虫病` 及下一节 `第三节地方病防治`，确认本节边界。
"""
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")


def update_memory(changed: int) -> None:
    marker = "## 2026-07-02 第五十五卷寄生虫病防治标题与OCR修复"
    memory = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker in memory:
        return
    entry = f"""
{marker}

- 对第五十五卷卫生第二章第二节 `寄生虫病防治` 进行回源修复。
- 源文依据：`{SOURCE_NOTE}`；以 PaddleOCR 页级文本校正正文汇总中遗留的 OCR 误识。
- 阅读版拆分 `一、疟疾`、`二、黑热病`、`三、丝虫病`、`四、蛔虫病`、`五、钩虫病` 5 个标题，并修复本节内可证的疾病名、虫名、药名和断行错误。
- 本轮新增替换 {changed} 处；下一节 `地方病防治` 未在本脚本中处理。
- 报告：`output/reports/reader_readability_health_parasitic_disease_subheads_20260702.md`。
"""
    MEMORY.write_text(memory.rstrip() + "\n\n" + entry.lstrip(), encoding="utf-8")


def main() -> None:
    changed, counts = patch_reader()
    write_reports(changed, counts)
    update_memory(changed)
    print("parasitic-disease section repaired")
    print(f"changes={changed}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()
