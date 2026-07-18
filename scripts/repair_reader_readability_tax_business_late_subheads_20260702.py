# -*- coding: utf-8 -*-
"""Split late flattened business-tax subheadings in volume 39."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_tax_business_late_subheads_20260702.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_tax_business_late_subheads_20260702.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260702_第三十九卷工商各税后半段标题粘连修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SOURCE_NOTE = (
    "workbench/body_chapters/连云港市志_全书_正文汇总.md:80010-80169; "
    "workbench/ocr/paddle_ocr/中/part02/page_0321.txt; "
    "workbench/ocr/paddle_ocr/中/part02/page_0322.txt; "
    "workbench/ocr/paddle_ocr/中/part02/page_0323.txt; "
    "workbench/ocr/paddle_ocr/中/part02/page_0324.txt; "
    "workbench/ocr/paddle_ocr/中/part02/page_0325.txt"
)
SCOPE_START = '<h4 id="第三十九卷-第二章税种税率-第二节工商各税">第二节工商各税</h4>'
SCOPE_END = '<h4 id="第三十九卷-第二章税种税率-第三节盐税">第三节盐税</h4>'

HEADINGS: list[tuple[str, str]] = [
    ("十四、合资企业所得税", "中外合资经营企业"),
    ("十五、外国企业所得税", "1982年"),
    ("十六、个人所得税个人收入调节税", "1984年起"),
    ("十七、城镇土地使用税", "1989年起"),
    ("十八、房地产税", "境内开征房捐"),
    ("十九、契税", "明代海州田房税契"),
    ("二十、屠宰税", "清代"),
    ("二十一、营业牌照税", "民国初期"),
    ("二十二、席、娱乐、文化娱乐税", "民国24年"),
    ("二十三、车船使用牌照税", "民国24年"),
    ("二十四、印花税", "民国初"),
    ("二十五、交易税", "建国初期"),
]

RESIDUALS = [f"{heading}{body_start}" for heading, body_start in HEADINGS]


def split_headings(segment: str) -> tuple[str, int, dict[str, int]]:
    changed = 0
    counts: dict[str, int] = {}
    for heading, body_start in HEADINGS:
        needle = f"<p>{heading}{body_start}"
        replacement = f"<p><strong>{heading}</strong></p>\n<p>{body_start}"
        count = segment.count(needle)
        if count:
            segment = segment.replace(needle, replacement)
            counts[f"{heading}{body_start}"] = count
            changed += count

    remaining = [marker for marker in RESIDUALS if marker in segment]
    if remaining:
        raise RuntimeError(f"late business-tax heading residue remains: {remaining}")
    return segment, changed, counts


def patch_reader() -> tuple[int, dict[str, int]]:
    text = HTML.read_text(encoding="utf-8")
    start = text.index(SCOPE_START)
    end = text.index(SCOPE_END, start)
    segment = text[start:end]
    new_segment, changed, counts = split_headings(segment)
    if new_segment != segment:
        text = text[:start] + new_segment + text[end:]
        HTML.write_text(text, encoding="utf-8")
    return changed, counts


def write_reports(changed: int, counts: dict[str, int]) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    total = len(HEADINGS)
    payload = {
        "time": now,
        "scope": "第三十九卷税务 / 第二章税种税率 / 第二节工商各税后半段",
        "source": SOURCE_NOTE,
        "reader_path": str(HTML),
        "headings_split_this_run": changed,
        "headings_in_scope": total,
        "counts": counts,
        "principle": "依据正文汇总和 PaddleOCR 页级文本中的独立标题行，仅拆分标题边界，不改写税制正文和数值。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    md = f"""# 第三十九卷工商各税后半段标题粘连修复

- 时间：{now}
- 范围：`第三十九卷税务 / 第二章税种税率 / 第二节工商各税后半段`
- 源文依据：`{SOURCE_NOTE}`

## 修复动作

- 拆分 `十四、合资企业所得税` 至 `二十五、交易税` 共 {total} 个税种小题。
- 本轮仅处理标题与正文首句粘连，不补改正文内 OCR 错字、不调整已由前序脚本处理的 `二十六、建筑税` 等小题。
- 本脚本覆盖标题边界：{total} 处；本次复跑新增拆分：{changed} 处。

## 核对说明

- 正文汇总 80010-80169 行显示上述税种标题为独立行。
- PaddleOCR 页级文本 0321-0325 页确认 `十四、合资企业所得税`、`十五、外国企业所得税`、`十六、个人所得税个人收入调节税`、`十七、城镇土地使用税`、`十八、房地产税`、`十九、契税`、`二十、屠宰税`、`二十一、营业牌照税`、`二十二、席、娱乐、文化娱乐税`、`二十三、车船使用牌照税`、`二十四、印花税`、`二十五、交易税` 均为独立标题。
- `二十六、建筑税` 及后续三项已由 `reader_readability_tax_subheads_20260702` 覆盖，本轮不重复处理。
"""
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")


def update_memory(changed: int) -> None:
    marker = "## 2026-07-02 第三十九卷工商各税后半段标题粘连修复"
    memory = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker in memory:
        return
    total = len(HEADINGS)
    entry = f"""
{marker}

- 对第三十九卷税务第二章第二节 `工商各税` 后半段标题压平进行修复。
- 源文依据：`{SOURCE_NOTE}`，确认 `十四、合资企业所得税` 至 `二十五、交易税` 共 {total} 个税种小题为独立标题行。
- 阅读版仅拆分标题边界，不改写税制正文和数值；本轮拆分 {changed} 处。
- `二十六、建筑税` 及后续三项已由前序税务小标题脚本覆盖，本轮不重复处理。
- 报告：`output/reports/reader_readability_tax_business_late_subheads_20260702.md`。
"""
    MEMORY.write_text(memory.rstrip() + "\n\n" + entry.lstrip(), encoding="utf-8")


def main() -> None:
    changed, counts = patch_reader()
    write_reports(changed, counts)
    update_memory(changed)
    print("late business-tax subheadings repaired")
    print(f"headings_split={changed}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()
