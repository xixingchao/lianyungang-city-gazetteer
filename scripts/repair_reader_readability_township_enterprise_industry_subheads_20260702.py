# -*- coding: utf-8 -*-
"""Split flattened township-enterprise industry subheadings in volume 27."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_township_enterprise_industry_subheads_20260702.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_township_enterprise_industry_subheads_20260702.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260702_第二十七卷乡镇企业产业结构小标题粘连修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SOURCE_NOTE = (
    "workbench/body_chapters/连云港市志_全书_正文汇总.md:142470-142536; "
    "workbench/ocr/paddle_ocr/中/part01/page_0397.txt; "
    "workbench/ocr/paddle_ocr/中/part01/page_0399.txt"
)
SCOPE_START = '<h4 id="第二十七卷-第一章企业结构-第二节产业结构">第二节产业结构</h4>'
SCOPE_END = '<h3 id="第二十七卷-第二章经营管理">第二章经营管理</h3>'

HEADINGS: list[tuple[str, str, str | None]] = [
    ("一、农副产品加工业", "改革开放以后", None),
    ("二、建筑业", "建筑产业", None),
    ("三、交通运输业", "1984年", None),
    ("四、商业、饮食、服务业", "饮食企业98家", None),
    ("五、工", "1984年", "五、工业"),
    ("建材", "建材工业", None),
]

RESIDUALS = [
    "一、农副产品加工业改革开放以后",
    "二、建筑业建筑产业",
    "三、交通运输业1984年",
    "四、商业、饮食、服务业饮食企业98家",
    "五、工1984年",
    "建材建材工业",
]


def split_headings_in_scope(segment: str) -> tuple[str, int, dict[str, int]]:
    changed = 0
    split_counts: dict[str, int] = {}
    for source_heading, body_start, normalized_heading in HEADINGS:
        display_heading = normalized_heading or source_heading
        needle = f"<p>{source_heading}{body_start}"
        replacement = f"<p><strong>{display_heading}</strong></p>\n<p>{body_start}"
        count = segment.count(needle)
        if count:
            segment = segment.replace(needle, replacement)
            split_counts[f"{source_heading}{body_start}"] = count
            changed += count

    remaining = [marker for marker in RESIDUALS if marker in segment]
    if remaining:
        raise RuntimeError(f"township enterprise industry heading residue remains: {remaining}")
    return segment, changed, split_counts


def patch_reader() -> tuple[int, dict[str, int]]:
    text = HTML.read_text(encoding="utf-8")
    start = text.index(SCOPE_START)
    end = text.index(SCOPE_END, start)
    segment = text[start:end]
    new_segment, changed, split_counts = split_headings_in_scope(segment)
    if new_segment != segment:
        text = text[:start] + new_segment + text[end:]
        HTML.write_text(text, encoding="utf-8")
    return changed, split_counts


def write_reports(changed: int, split_counts: dict[str, int]) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    total = len(HEADINGS)
    payload = {
        "time": now,
        "scope": "第二十七卷乡镇企业 / 第一章企业结构 / 第二节产业结构",
        "source": SOURCE_NOTE,
        "reader_path": str(HTML),
        "headings_split_this_run": changed,
        "headings_in_scope": total,
        "split_counts": split_counts,
        "normalizations": {
            "五、工": "五、工业",
            "建材建材工业": "建材 / 建材工业",
        },
        "principle": "依据正文汇总和 PaddleOCR 页级文本中的独立标题行，仅拆分标题边界；缺字仅在 OCR 证据明确处补正。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    md = f"""# 第二十七卷乡镇企业产业结构小标题粘连修复

- 时间：{now}
- 范围：`第二十七卷乡镇企业 / 第一章企业结构 / 第二节产业结构`
- 源文依据：`{SOURCE_NOTE}`

## 修复动作

- 拆分产业结构 5 个产业小题：`一、农副产品加工业`、`二、建筑业`、`三、交通运输业`、`四、商业、饮食、服务业`、`五、工业`。
- 拆分工业段下 `建材` 小题，修正阅读版 `建材建材工业...` 粘连为 `建材` 标题和 `建材工业...` 正文。
- `五、工` 依据 `workbench/ocr/paddle_ocr/中/part01/page_0399.txt` 中 `五、工业` 补正为完整标题。
- 本脚本覆盖标题边界：{total} 处；本次复跑新增拆分：{changed} 处。
- 仅调整段落结构和明确缺字标题，不改写正文统计数值或后续行业细目。

## 核对说明

- 正文汇总 142470-142536 行显示上述标题与正文为分行结构。
- PaddleOCR 页级文本 0397、0399 页确认 `一、农副产品加工业`、`五、工业` 与 `建材 建材工业...` 的版面边界。
- 本轮不处理后续 `【砖瓦】`、`【水泥及制品】` 等行业细目，避免扩大改动范围。
"""
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")


def update_memory(changed: int) -> None:
    marker = "## 2026-07-02 第二十七卷乡镇企业产业结构小标题粘连修复"
    memory = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker in memory:
        return
    total = len(HEADINGS)
    entry = f"""
{marker}

- 对正文可读性审计命中的第二十七卷乡镇企业第一章第二节 `产业结构` 小标题压平进行修复。
- 源文依据：`{SOURCE_NOTE}`，确认 5 个产业小题和工业段下 `建材` 为独立标题边界。
- 阅读版仅拆分标题边界；`五、工` 依据 PaddleOCR 页级文本补正为 `五、工业`；本轮拆分 {changed} 处，范围覆盖 {total} 处标题粘连。
- 后续 `【砖瓦】`、`【水泥及制品】` 等行业细目未改，留待后续按源文单独核对。
- 报告：`output/reports/reader_readability_township_enterprise_industry_subheads_20260702.md`。
"""
    MEMORY.write_text(memory.rstrip() + "\n\n" + entry.lstrip(), encoding="utf-8")


def main() -> None:
    changed, split_counts = patch_reader()
    write_reports(changed, split_counts)
    update_memory(changed)
    print("township enterprise industry subheadings repaired")
    print(f"headings_split={changed}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()
