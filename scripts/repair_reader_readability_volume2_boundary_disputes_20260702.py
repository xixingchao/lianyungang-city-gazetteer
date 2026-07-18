# -*- coding: utf-8 -*-
"""Split flattened boundary-dispute headings in volume 2 reader text."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_volume2_boundary_disputes_20260702.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_volume2_boundary_disputes_20260702.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260702_第二卷界域争议标题压平修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SOURCE_NOTE = "workbench/body_chapters/paddle_上/第二卷_建置区划.md:1041-1187"

HEADINGS: list[tuple[str, str]] = [
    ("附2-1：界域争议", "一、东海、灌云县分治划界争议"),
    ("一、东海、灌云县分治划界争议", "民国初"),
    ("二、前三岛归属争议", "前三岛系指"),
    ("三、篙子山归属争议", "赣榆县之北"),
    ("四、石塘山归属争议", "东海县石埠乡"),
    ("五、新沭河柴地归属争议", "争端地位于"),
]

RESIDUALS = [heading + body_start for heading, body_start in HEADINGS]


def split_one_heading(text: str, heading: str, body_start: str) -> tuple[str, int]:
    strong = f"<p><strong>{heading}</strong></p>"
    needle = heading + body_start
    if needle not in text:
        return text, 0

    pos = text.find(needle)
    open_pos = text.rfind("<p>", 0, pos)
    close_pos = text.rfind("</p>", 0, pos)
    inside_paragraph = open_pos > close_pos

    if inside_paragraph:
        paragraph_prefix = text[open_pos + len("<p>"):pos]
        if paragraph_prefix.strip():
            replacement = f"</p>\n{strong}\n<p>{body_start}"
            text = text[:pos] + replacement + text[pos + len(needle):]
        else:
            replacement = f"{strong}\n<p>{body_start}"
            text = text[:open_pos] + replacement + text[pos + len(needle):]
    else:
        replacement = f"{strong}\n<p>{body_start}"
        text = text[:pos] + replacement + text[pos + len(needle):]
    return text, 1


def patch_reader() -> int:
    text = HTML.read_text(encoding="utf-8")
    changed = 0
    for heading, body_start in HEADINGS:
        text, count = split_one_heading(text, heading, body_start)
        changed += count

    remaining = [residual for residual in RESIDUALS if residual in text]
    if remaining:
        raise RuntimeError(f"volume 2 boundary-dispute heading residue remains: {remaining}")

    HTML.write_text(text, encoding="utf-8")
    return changed


def write_reports(changed: int) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "第二卷建置区划 / 附2-1 界域争议",
        "source": SOURCE_NOTE,
        "reader_path": str(HTML),
        "headings_split_this_run": changed,
        "headings_in_scope": len(HEADINGS),
        "principle": "依据 PaddleOCR 正文汇总中的独立标题行，仅拆分阅读版标题粘连，不改写正文内容。",
        "note": "附2-1 前表2-7的线性表格残留本轮未重录，留待表格专项回源处理。幂等复跑时 headings_split_this_run 可为 0。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    md = f"""# 第二卷界域争议标题压平修复

- 时间：{now}
- 范围：`第二卷建置区划 / 附2-1 界域争议`
- 源文依据：`{SOURCE_NOTE}`

## 修复动作

- 拆分 `附2-1：界域争议一、东海、灌云县分治划界争议...`。
- 拆分五个分项标题：`一、东海、灌云县分治划界争议`、`二、前三岛归属争议`、`三、篙子山归属争议`、`四、石塘山归属争议`、`五、新沭河柴地归属争议`。
- 本轮只调整段落结构，不重录正文文字，不进行图片核字。
- `附2-1` 前的表2-7线性表格残留未在本轮改写，后续按表格专项回源处理。
- 本脚本覆盖标题边界：{len(HEADINGS)} 处；本次复跑新增拆分：{changed} 处。

## 核对说明

- `paddle_上/第二卷_建置区划.md` 中上述标题均为独立行。
- 脚本复跑会检查上述标题与正文首句的粘连残串是否仍存在；若存在则报错。
"""
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")


def update_memory(changed: int) -> None:
    marker = "## 2026-07-02 第二卷界域争议标题压平修复"
    memory = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker in memory:
        return
    entry = f"""
{marker}

- 对正文可读性审计命中的第二卷建置区划 `附2-1：界域争议` 标题压平进行修复。
- 源文依据：`{SOURCE_NOTE}`，确认 `附2-1：界域争议` 及五个分项标题在源文中为独立行。
- 阅读版仅拆分标题边界，不重录正文文字；本轮拆分 {changed} 处，范围覆盖 {len(HEADINGS)} 处标题粘连。
- `附2-1` 前的表2-7线性表格残留暂未改写，留待表格专项回源处理。
- 报告：`output/reports/reader_readability_volume2_boundary_disputes_20260702.md`。
"""
    MEMORY.write_text(memory.rstrip() + "\n\n" + entry.lstrip(), encoding="utf-8")


def main() -> None:
    changed = patch_reader()
    write_reports(changed)
    update_memory(changed)
    print("volume 2 boundary-dispute headings repaired")
    print(f"headings_split={changed}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()
