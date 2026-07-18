# -*- coding: utf-8 -*-
"""Repair flattened business-tax subheadings in volume 39."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_tax_business_subheads_20260702.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_tax_business_subheads_20260702.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260702_第三十九卷工商各税前半段标题粘连修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SOURCE_NOTE = (
    "workbench/body_chapters/连云港市志_全书_正文汇总.md:79921-80007; "
    "workbench/ocr/paddle_ocr/中/part02/page_0318.txt; "
    "workbench/ocr/paddle_ocr/中/part02/page_0319.txt; "
    "workbench/ocr/paddle_ocr/中/part02/page_0320.txt"
)
SCOPE_START = '<h4 id="第三十九卷-第二章税种税率-第二节工商各税">第二节工商各税</h4>'
SCOPE_END = '<h4 id="第三十九卷-第二章税种税率-第三节盐税">第三节盐税</h4>'

# source heading, body start, display heading
HEADINGS: list[tuple[str, str, str | None]] = [
    ("五、工商统一税", "1958年9月", None),
    ("六、工商税", "1973年", None),
    ("七、产品税", "1984年10月起", None),
    ("九、利息所得税", "1950年4月", None),
    ("十、工商所得税", "1950年", None),
    ("十、国营企业所得税和调节税", "1983年", "十一、国营企业所得税和调节税"),
    ("十二、集体企业、私营企业和城乡个体工商户所得税", "1985年起", None),
]

LAND_USE_BAD = "1990年9月起增设“土地四、货物税明清时海州货物税有盐税、茶税、酒醋课等。"
LAND_USE_FIXED = (
    "1990年9月起增设“土地使用权转让及出售建筑物”和“经济权益转让”两个税目。</p>\n"
    "<p><strong>四、货物税</strong></p>\n"
    "<p>明清时海州货物税有盐税、茶税、酒醋课等。"
)

VAT_BAD = "<p>八、增值税率分别为10%和6%。"
VAT_FIXED = (
    "<p><strong>八、增值税</strong></p>\n"
    "<p>1983年起，在全市机器机械及其零配件和农业机具及其零配件行业试征增值税，"
    "税率分别为10%和6%。"
)

RESIDUALS = [
    LAND_USE_BAD,
    VAT_BAD,
    "五、工商统一税1958年9月",
    "六、工商税1973年",
    "七、产品税1984年10月起",
    "九、利息所得税1950年4月",
    "十、工商所得税1950年",
    "十、国营企业所得税和调节税1983年",
    "十二、集体企业、私营企业和城乡个体工商户所得税1985年起",
]


def split_headings(segment: str) -> tuple[str, int, dict[str, int]]:
    changed = 0
    counts: dict[str, int] = {}

    land_use_count = segment.count(LAND_USE_BAD)
    if land_use_count:
        segment = segment.replace(LAND_USE_BAD, LAND_USE_FIXED)
        counts["营业税末句缺行并拆出四、货物税"] = land_use_count
        changed += land_use_count

    vat_count = segment.count(VAT_BAD)
    if vat_count:
        segment = segment.replace(VAT_BAD, VAT_FIXED)
        counts["八、增值税缺首句"] = vat_count
        changed += vat_count

    for source_heading, body_start, display_heading in HEADINGS:
        shown = display_heading or source_heading
        needle = f"<p>{source_heading}{body_start}"
        replacement = f"<p><strong>{shown}</strong></p>\n<p>{body_start}"
        count = segment.count(needle)
        if count:
            segment = segment.replace(needle, replacement)
            counts[f"{source_heading}{body_start}"] = count
            changed += count

    remaining = [marker for marker in RESIDUALS if marker in segment]
    if remaining:
        raise RuntimeError(f"business-tax heading residue remains: {remaining}")
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
    total = len(HEADINGS) + 2
    payload = {
        "time": now,
        "scope": "第三十九卷税务 / 第二章税种税率 / 第二节工商各税前半段",
        "source": SOURCE_NOTE,
        "reader_path": str(HTML),
        "changes_this_run": changed,
        "boundaries_or_omissions_in_scope": total,
        "counts": counts,
        "normalizations": {
            "十、国营企业所得税和调节税": "十一、国营企业所得税和调节税",
            "八、增值税率分别为10%和6%": "八、增值税 + 补回试征增值税首句",
            "土地四、货物税": "补回营业税末句后拆出四、货物税",
        },
        "principle": "依据正文汇总和 PaddleOCR 页级文本，只修复标题边界与页级 OCR 可证的缺漏，不扩展到后半段税种。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    md = f"""# 第三十九卷工商各税前半段标题粘连修复

- 时间：{now}
- 范围：`第三十九卷税务 / 第二章税种税率 / 第二节工商各税前半段`
- 源文依据：`{SOURCE_NOTE}`

## 修复动作

- 补回营业税末句 `土地使用权转让及出售建筑物`、`经济权益转让` 两个税目，并拆出 `四、货物税`。
- 拆分 `五、工商统一税`、`六、工商税`、`七、产品税`、`九、利息所得税`、`十、工商所得税`、`十二、集体企业、私营企业和城乡个体工商户所得税`。
- 补回 `八、增值税` 首句：`1983年起，在全市机器机械及其零配件和农业机具及其零配件行业试征增值税...`。
- 依据 `page_0320.txt` 与税种序号，将 `十、国营企业所得税和调节税` 修正并拆分为 `十一、国营企业所得税和调节税`。
- 本脚本覆盖标题边界或缺漏点：{total} 处；本次复跑新增修复：{changed} 处。
- 本轮不处理 `十四、合资企业所得税` 之后的后半段税种，留待后续单独核对。

## 核对说明

- `page_0318.txt` 显示营业税末句完整为两个新增税目，随后另起 `四、货物税`。
- `page_0319.txt` 显示 `五、工商统一税` 至 `十、工商所得税` 为独立税种标题，并补出增值税首句。
- `page_0320.txt` 显示该页标题为 `十一、国营企业所得税和调节税`，随后为 `十二、集体企业、私营企业和城乡个体工商户所得税`。
"""
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")


def update_memory(changed: int) -> None:
    marker = "## 2026-07-02 第三十九卷工商各税前半段标题粘连修复"
    memory = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker in memory:
        return
    total = len(HEADINGS) + 2
    entry = f"""
{marker}

- 对第三十九卷税务第二章第二节 `工商各税` 前半段做小批修复。
- 源文依据：`{SOURCE_NOTE}`；补回营业税末句两个新增税目，拆出 `四、货物税`，并补回 `八、增值税` 首句。
- 阅读版拆分 `五、工商统一税` 至 `十二、集体企业、私营企业和城乡个体工商户所得税` 相关标题；`十一、国营企业所得税和调节税` 依据页级 OCR 和序号修正。
- 本轮修复 {changed} 处，范围覆盖 {total} 处标题边界或缺漏点；后半段税种未改，留待后续单独核对。
- 报告：`output/reports/reader_readability_tax_business_subheads_20260702.md`。
"""
    MEMORY.write_text(memory.rstrip() + "\n\n" + entry.lstrip(), encoding="utf-8")


def main() -> None:
    changed, counts = patch_reader()
    write_reports(changed, counts)
    update_memory(changed)
    print("business-tax subheadings repaired")
    print(f"changes={changed}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()
