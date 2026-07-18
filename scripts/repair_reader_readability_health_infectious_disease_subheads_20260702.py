# -*- coding: utf-8 -*-
"""Split flattened infectious-disease subheadings in volume 55."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_health_infectious_disease_subheads_20260702.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_health_infectious_disease_subheads_20260702.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260702_第五十五卷传染病防治标题粘连修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SOURCE_NOTE = (
    "workbench/body_chapters/连云港市志_全书_正文汇总.md:100264-100483; "
    "workbench/body_chapters/第五十二卷至第六十卷及附录（下part02）.md:6966-7139; "
    "workbench/ocr/paddle_ocr/下/part02/page_0173.txt; "
    "workbench/ocr/paddle_ocr/下/part02/page_0174.txt; "
    "workbench/ocr/paddle_ocr/下/part02/page_0175.txt; "
    "workbench/ocr/paddle_ocr/下/part02/page_0176.txt; "
    "workbench/ocr/paddle_ocr/下/part02/page_0177.txt; "
    "workbench/ocr/paddle_ocr/下/part02/page_0178.txt; "
    "workbench/ocr/paddle_ocr/下/part02/page_0179.txt"
)
SCOPE_START = '<h4 id="第五十五卷-第二章常见病防治-第一节传染病防治">第一节传染病防治</h4>'
SCOPE_END = '<h4 id="第五十五卷-第二章常见病防治-第二节寄生虫病防治">第二节寄生虫病防治</h4>'

REPLACEMENTS: list[tuple[str, str, str]] = [
    ("一、天花", "<p>一、天花海州地区", "<p><strong>一、天花</strong></p>\n<p>海州地区"),
    ("二、霍乱、副霍乱", "<p>二、霍乱、副霍乱民国9年", "<p><strong>二、霍乱、副霍乱</strong></p>\n<p>民国9年"),
    ("三、伤寒、副伤寒", "<p>三、伤寒、副伤寒解放前", "<p><strong>三、伤寒、副伤寒</strong></p>\n<p>解放前"),
    ("四、流行性脑脊髓膜炎", "<p>四、流行性脑脊髓膜炎1957年", "<p><strong>四、流行性脑脊髓膜炎</strong></p>\n<p>1957年"),
    ("五、流行性乙型脑炎", "<p>五、流行性乙型脑炎1954年", "<p><strong>五、流行性乙型脑炎</strong></p>\n<p>1954年"),
    ("六、病毒性肝炎", "<p>六、病毒性肝炎1950年", "<p><strong>六、病毒性肝炎</strong></p>\n<p>1950年"),
    ("七、细菌性痢疾", "<p>七、细菌性痢疾1952年", "<p><strong>七、细菌性痢疾</strong></p>\n<p>1952年"),
    ("八、流行性出血热", "<p>八、流行性出血热1972年", "<p><strong>八、流行性出血热</strong></p>\n<p>1972年"),
    ("九、流行性感冒", "<p>九、流行性感冒1954年", "<p><strong>九、流行性感冒</strong></p>\n<p>1954年"),
    ("十、白喉", "<p>十、白民国28年至29年", "<p><strong>十、白喉</strong></p>\n<p>民国28年至29年"),
    ("十一、百日咳", "<p>十一、百日咳自1949年", "<p><strong>十一、百日咳</strong></p>\n<p>自1949年"),
    ("十二、麻疹", "<p>十二、麻疹麻疹在", "<p><strong>十二、麻疹</strong></p>\n<p>麻疹在"),
    ("十三、脊髓灰质炎", "<p>十三、脊髓灰质炎建国前", "<p><strong>十三、脊髓灰质炎</strong></p>\n<p>建国前"),
    ("十四、结核病", "<p>十四、结核病结核病，主要是", "<p><strong>十四、结核病</strong></p>\n<p>结核病，主要是"),
    ("十五、狂犬病", "<p>十五、狂犬病民国期间", "<p><strong>十五、狂犬病</strong></p>\n<p>民国期间"),
    ("十六、猩红热", "<p>十六、猩红热从民国11年", "<p><strong>十六、猩红热</strong></p>\n<p>从民国11年"),
    ("十七、回归热", "<p>十七、回归热民国23年", "<p><strong>十七、回归热</strong></p>\n<p>民国23年"),
    (
        "十八、钩端螺旋体病",
        "<p>十八、钩端螺旋体病站，在新浦区向阳大队调查。",
        "<p><strong>十八、钩端螺旋体病</strong></p>\n<p>1970年以前连云港市未见有钩端螺旋体病记载。1971年1月，市卫生局会同市兽医站，在新浦区向阳大队调查。",
    ),
    ("十九、麻风", "<p>十九、麻麻风病在", "<p><strong>十九、麻风</strong></p>\n<p>麻风病在"),
    ("二十、性病", "<p>二十、性病市内性病", "<p><strong>二十、性病</strong></p>\n<p>市内性病"),
]

RESIDUALS = [needle.removeprefix("<p>") for _, needle, _ in REPLACEMENTS]
EXPECTED_FINALS = [f"<p><strong>{label}</strong></p>" for label, _, _ in REPLACEMENTS]


def split_headings(segment: str) -> tuple[str, int, dict[str, int]]:
    changed = 0
    counts: dict[str, int] = {}
    for label, needle, replacement in REPLACEMENTS:
        count = segment.count(needle)
        if count:
            segment = segment.replace(needle, replacement)
            counts[label] = count
            changed += count

    remaining = [marker for marker in RESIDUALS if marker in segment]
    if remaining:
        raise RuntimeError(f"infectious-disease heading residue remains: {remaining}")
    missing = [marker for marker in EXPECTED_FINALS if marker not in segment]
    if missing:
        raise RuntimeError(f"infectious-disease heading markers missing: {missing}")
    return segment, changed, counts


def patch_reader() -> tuple[int, dict[str, int]]:
    text = HTML.read_text(encoding="utf-8")
    start = text.index(SCOPE_START)
    end = text.index(SCOPE_END, start)
    segment = text[start:end]
    new_segment, changed, counts = split_headings(segment)
    if new_segment != segment:
        HTML.write_text(text[:start] + new_segment + text[end:], encoding="utf-8")
    return changed, counts


def write_reports(changed: int, counts: dict[str, int]) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "第五十五卷卫生 / 第二章常见病防治 / 第一节传染病防治",
        "source": SOURCE_NOTE,
        "reader_path": str(HTML),
        "paragraph_boundaries_split_this_run": changed,
        "target_paragraph_boundaries": len(REPLACEMENTS),
        "target_headings": len(REPLACEMENTS),
        "counts": counts,
        "source_backed_title_corrections": ["十、白喉", "十九、麻风"],
        "source_backed_body_restore": "十八、钩端螺旋体病首句：1970年以前连云港市未见有钩端螺旋体病记载。1971年1月，市卫生局会同市兽医站，在新浦区向阳大队调查。",
        "principle": "依据正文汇总和 PaddleOCR 页级文本，仅修复标题边界及源文明确缺字缺句；未批量改正文内其它 OCR 字词和数值。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    md = f"""# 第五十五卷传染病防治标题粘连修复

- 时间：{now}
- 范围：`第五十五卷卫生 / 第二章常见病防治 / 第一节传染病防治`
- 源文依据：`{SOURCE_NOTE}`

## 修复动作

- 拆分 `一、天花` 至 `二十、性病` 共 {len(REPLACEMENTS)} 个病种标题，使读者版标题与正文分段显示。
- 依据 PaddleOCR `page_0176.txt` 将 `十、白` 补正为 `十、白喉`。
- 依据 PaddleOCR `page_0178.txt` 将 `十九、麻` 补正为 `十九、麻风`。
- 依据 PaddleOCR `page_0178.txt` 补回 `十八、钩端螺旋体病` 起始句：`1970年以前连云港市未见有钩端螺旋体病记载。1971年1月，市卫生局会同市兽医站，在新浦区向阳大队调查。`
- 本轮目标边界 {len(REPLACEMENTS)} 处；本次复跑新增拆分：{changed} 处。
- 本轮未批量改正文内其它 OCR 字词和数值。

## 核对说明

- 正文汇总 100264-100483 行显示 `第一节传染病防治` 下 20 个病种条目为独立小标题。
- PaddleOCR `page_0173` 至 `page_0179` 确认 20 个病种标题的页面顺序和标题文本，其中 `十、白喉`、`十八、钩端螺旋体病`、`十九、麻风` 在当前读者版存在缺字或缺句。
- 读者版原来将标题压成 `一、天花海州地区...`、`十、白民国28...`、`十八、钩端螺旋体病站，在...`、`十九、麻麻风病...`、`二十、性病市内性病...` 等连续正文，本轮已按源文拆开。
"""
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")


def update_memory(changed: int) -> None:
    marker = "## 2026-07-02 第五十五卷传染病防治标题粘连修复"
    memory = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker in memory:
        return
    entry = f"""
{marker}

- 对第五十五卷卫生第二章第一节 `传染病防治` 的 20 个病种标题压平问题进行修复。
- 源文依据：`{SOURCE_NOTE}`，确认 `一、天花` 至 `二十、性病` 均为独立标题行。
- 依据 PaddleOCR 补正 `十、白喉`、`十九、麻风`，并补回 `十八、钩端螺旋体病` 起始句；未批量改其它正文 OCR 字词和数值。
- 本轮目标边界 20 处，本次复跑新增拆分 {changed} 处。
- 报告：`output/reports/reader_readability_health_infectious_disease_subheads_20260702.md`。
"""
    MEMORY.write_text(memory.rstrip() + "\n\n" + entry.lstrip(), encoding="utf-8")


def main() -> None:
    changed, counts = patch_reader()
    write_reports(changed, counts)
    update_memory(changed)
    print("infectious-disease subheadings repaired")
    print(f"paragraph_boundaries_split={changed}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()
