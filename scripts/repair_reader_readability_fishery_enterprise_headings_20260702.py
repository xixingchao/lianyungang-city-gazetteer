# -*- coding: utf-8 -*-
"""Split flattened enterprise-introduction headings in volume 12 fishery text."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_fishery_enterprise_headings_20260702.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_fishery_enterprise_headings_20260702.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260702_第十二卷水产主要企业简介标题压平修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SOURCE_NOTE = "workbench/body_chapters/paddle_上/第十卷至第十六卷（part03）.md:6687-6719"
SECTION_START = '<h3 id="第十二卷-第二章海洋捕捞">第二章海洋捕捞</h3>'
SECTION_END = '<h3 id="第十二卷-第三章海产品养（增）殖">第三章海产品养（增）殖</h3>'
H4 = '<h4 id="第十二卷-第二章海洋捕捞-第六节主要企业简介">第六节主要企业简介</h4>'
HEADINGS: list[tuple[str, str]] = [
    ("二、东海县太平渔业公司", "公司位于东海县浦南乡太平村"),
    ("三、赣榆县渔业公司", "位于赣榆县海头镇"),
    ("四、灌云县渔业公司", "该公司位于燕尾港"),
]
RESIDUALS = [
    "第六节 主要企业简介一、连云港海洋渔业公司",
    "一、连云港海洋渔业公司该公司座落在连云港。",
    "二、东海县太平渔业公司公司位于东海县浦南乡太平村",
    "三、赣榆县渔业公司位于赣榆县海头镇",
    "四、灌云县渔业公司该公司位于燕尾港",
]


def split_section_heading(text: str) -> tuple[str, int]:
    needle = "第六节 主要企业简介一、连云港海洋渔业公司"
    if needle not in text:
        return text, 0
    pos = text.find(needle)
    if text.rfind("<p>", 0, pos) <= text.rfind("</p>", 0, pos):
        return text, 0
    replacement = f"</p>\n{H4}\n<p><strong>一、连云港海洋渔业公司</strong></p>\n<p>"
    text = text[:pos] + replacement + text[pos + len(needle):]
    return text, 1


def split_inline_heading(text: str, heading: str, body_start: str) -> tuple[str, int]:
    strong = f"<p><strong>{heading}</strong></p>"
    needle = heading + body_start
    if needle not in text:
        return text, 0
    pos = text.find(needle)
    inside = text.rfind("<p>", 0, pos) > text.rfind("</p>", 0, pos)
    if inside:
        replacement = f"</p>\n{strong}\n<p>{body_start}"
    else:
        replacement = f"{strong}\n<p>{body_start}"
    text = text[:pos] + replacement + text[pos + len(needle):]
    return text, 1


def cleanup_empty_paragraphs(text: str) -> tuple[str, int]:
    start = text.index(SECTION_START)
    end = text.index(SECTION_END, start)
    section = text[start:end]
    before = section.count("<p></p>")
    section = section.replace("\n<p></p>\n<h4", "\n<h4")
    section = section.replace("\n<p></p>\n<p><strong>", "\n<p><strong>")
    after = section.count("<p></p>")
    return text[:start] + section + text[end:], before - after


def patch_reader() -> dict[str, int]:
    text = HTML.read_text(encoding="utf-8")
    headings_split = 0
    text, count = split_section_heading(text)
    headings_split += count
    for heading, body_start in HEADINGS:
        text, count = split_inline_heading(text, heading, body_start)
        headings_split += count
    remaining = [marker for marker in RESIDUALS if marker in text]
    if remaining:
        raise RuntimeError(f"fishery enterprise heading residue remains: {remaining}")
    text, empty_removed = cleanup_empty_paragraphs(text)
    HTML.write_text(text, encoding="utf-8")
    return {"headings_split": headings_split, "empty_paragraphs_removed": empty_removed}


def write_reports(result: dict[str, int]) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "第十二卷水产 / 第二章海洋捕捞 / 第六节主要企业简介",
        "source": SOURCE_NOTE,
        "reader_path": str(HTML),
        "headings_split_this_run": result["headings_split"],
        "empty_paragraphs_removed_this_run": result["empty_paragraphs_removed"],
        "headings_in_scope": 5,
        "principle": "依据 PaddleOCR 正文汇总中的独立标题行，仅拆分标题边界，不改写正文文字。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    md = f"""# 第十二卷水产主要企业简介标题压平修复

- 时间：{now}
- 范围：`第十二卷水产 / 第二章海洋捕捞 / 第六节主要企业简介`
- 源文依据：`{SOURCE_NOTE}`

## 修复动作

- 拆分 `第六节 主要企业简介一、连云港海洋渔业公司...`，恢复节标题。
- 拆分四个企业小题：`一、连云港海洋渔业公司`、`二、东海县太平渔业公司`、`三、赣榆县渔业公司`、`四、灌云县渔业公司`。
- 清理本段拆分产生的空段落：{result['empty_paragraphs_removed']} 处。
- 本轮只调整段落结构，不重录正文文字，不进行图片核字。
- 本脚本覆盖标题边界：5 处；本次复跑新增拆分：{result['headings_split']} 处。

## 核对说明

- `paddle_上/第十卷至第十六卷（part03）.md` 中上述标题均为独立行。
- 脚本复跑会检查标题与正文首句的粘连残串是否仍存在；若存在则报错。
"""
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")


def update_memory(headings_split: int) -> None:
    marker = "## 2026-07-02 第十二卷水产主要企业简介标题压平修复"
    memory = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker in memory:
        return
    entry = f"""
{marker}

- 对正文可读性审计命中的第十二卷水产 `第六节 主要企业简介一、连云港海洋渔业公司...` 标题压平进行修复。
- 源文依据：`{SOURCE_NOTE}`，确认节标题和四个企业小题在源文中为独立行。
- 阅读版仅拆分标题边界，不重录正文文字；本轮拆分 {headings_split} 处，范围覆盖 5 处标题粘连。
- 报告：`output/reports/reader_readability_fishery_enterprise_headings_20260702.md`。
"""
    MEMORY.write_text(memory.rstrip() + "\n\n" + entry.lstrip(), encoding="utf-8")


def main() -> None:
    result = patch_reader()
    write_reports(result)
    update_memory(result["headings_split"])
    print("fishery enterprise headings repaired")
    print(f"headings_split={result['headings_split']}")
    print(f"empty_paragraphs_removed={result['empty_paragraphs_removed']}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()
