# -*- coding: utf-8 -*-
"""Restore child growth survey subsection from page OCR."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_health_child_growth_survey_20260702.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_health_child_growth_survey_20260702.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260702_第五十五卷儿童体格发育调查回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SOURCE_NOTE = (
    "workbench/ocr/paddle_ocr/下/part02/page_0205.txt:4-12; "
    "workbench/body_chapters/连云港市志_全书_正文汇总.md:101466-101473; "
    "workbench/body_chapters/第五十二卷至第六十卷及附录（下part02）.md:8161-8168"
)
SCOPE_START_OPTIONS = (
    '<p>三、儿童体格发育调查',
    '<p><strong>三、儿童体格发育调查</strong></p>',
)
SCOPE_END = '<h4 id="第五十五卷-第五章保健疗养-第三节干部保健">第三节干部保健</h4>'

NEW_HTML = """<p><strong>三、儿童体格发育调查</strong></p>
<p>1979年5月，由市妇幼保健所和各综合医院儿科医生15人组成调查组，对城区和郊区的3122名儿童进行体检，对其中2781名儿童调查资料分类统计。发现体重均值在中等以上者有2427人，占87.5%；身长在中等以上者2344人，占84.3%。与1975年全国平均值相比较，体重较重而身高较低，为矮胖型。1985年，根据全国儿童体格发育调查方案，以市妇幼保健所为主组成调查组，共检查8152名儿童，建立合格统计卡片6620人份。调查共分为22个年龄组，检测指标分为体重、身长、坐高、头围、胸围、臂围6个方面。经分析，发现前5项指标的平均值均比1975年全国均值高。</p>"""

EXPECTED_TEXT = [
    '<p><strong>三、儿童体格发育调查</strong></p>',
    "共检查8152名儿童，建立合格统计卡片6620人份。调查共分为22个年龄组",
    "检测指标分为体重、身长、坐高、头围、胸围、臂围6个方面。经分析",
]
RESIDUALS = [
    "三、儿童体格发育调查1979年",
    "</p>\n<p>分析，发现前5项指标",
]


def find_scope(text: str) -> tuple[int, int]:
    starts = [text.find(marker) for marker in SCOPE_START_OPTIONS]
    valid_starts = [start for start in starts if start != -1]
    if not valid_starts:
        raise RuntimeError("child growth survey scope start not found")
    start = min(valid_starts)
    end = text.index(SCOPE_END, start)
    return start, end


def patch_reader() -> tuple[int, dict[str, int]]:
    text = HTML.read_text(encoding="utf-8")
    start, end = find_scope(text)
    new_segment = NEW_HTML + "\n"
    changed = int(text[start:end] != new_segment)
    if changed:
        HTML.write_text(text[:start] + new_segment + text[end:], encoding="utf-8")

    text = HTML.read_text(encoding="utf-8")
    start, end = find_scope(text)
    segment = text[start:end]
    missing = [item for item in EXPECTED_TEXT if item not in segment]
    if missing:
        raise RuntimeError(f"child growth survey expected text missing: {missing}")
    remaining = [item for item in RESIDUALS if item in segment]
    if remaining:
        raise RuntimeError(f"child growth survey residue remains: {remaining}")
    return changed, {"rewrote_scope": changed}


def write_reports(changed: int, counts: dict[str, int]) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "第五十五卷卫生 / 第五章保健疗养 / 第二节儿童保健 / 三、儿童体格发育调查",
        "source": SOURCE_NOTE,
        "reader_path": str(HTML),
        "changes_this_run": changed,
        "counts": counts,
        "principle": "依据 PaddleOCR 页级文本拆分标题并补回正文汇总漏失的检测指标句。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    md = f"""# 第五十五卷儿童体格发育调查回源修复

- 时间：{now}
- 范围：`第五十五卷卫生 / 第五章保健疗养 / 第二节儿童保健 / 三、儿童体格发育调查`
- 源文依据：`{SOURCE_NOTE}`

## 修复动作

- 拆分 `三、儿童体格发育调查` 小节标题。
- 依据页级 OCR 补回 `调查共分为22个年龄组，检测指标分为体重、身长、坐高、头围、胸围、臂围6个方面`。
- 合并误断开的 `分析，发现前5项指标...`。
- 本次复跑新增整段替换：{changed} 处。
- 本轮未处理 `第三节干部保健`。

## 核对说明

- PaddleOCR `page_0205.txt` 确认本小节标题、完整指标句和 `第三节干部保健` 边界。
- 正文汇总文件缺失 `调查共分为22个年龄组...` 句，本次以页级 OCR 为准。
"""
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")


def update_memory(changed: int) -> None:
    marker = "## 2026-07-02 第五十五卷儿童体格发育调查回源修复"
    memory = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker in memory:
        return
    entry = f"""
{marker}

- 对第五十五卷卫生第五章第二节 `儿童保健` 的 `三、儿童体格发育调查` 进行回源修复。
- 源文依据：`{SOURCE_NOTE}`；拆分标题，并按页级 OCR 补回 `调查共分为22个年龄组...` 指标句。
- 本轮新增整段替换 {changed} 处；`第三节干部保健` 未在本脚本中处理。
- 报告：`output/reports/reader_readability_health_child_growth_survey_20260702.md`。
"""
    MEMORY.write_text(memory.rstrip() + "\n\n" + entry.lstrip(), encoding="utf-8")


def main() -> None:
    changed, counts = patch_reader()
    write_reports(changed, counts)
    update_memory(changed)
    print("child growth survey section repaired")
    print(f"changes={changed}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()
