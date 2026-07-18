# -*- coding: utf-8 -*-
"""Restore the missing tail sentence in the private practice management section."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_health_private_practice_tail_20260702.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_health_private_practice_tail_20260702.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260702_第五十五卷个体行医管理漏文修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SOURCE_NOTE = (
    "workbench/body_chapters/连云港市志_全书_正文汇总.md:100963-100987; "
    "workbench/body_chapters/第五十二卷至第六十卷及附录（下part02）.md:7662-7686; "
    "workbench/ocr/paddle_ocr/下/part02/page_0192.txt"
)
SCOPE_START = '<h4 id="第五十五卷-第四章医政 药政-第一节个体行医管理">第一节个体行医管理</h4>'
SCOPE_END = '<h4 id="第五十五卷-第四章医政 药政-第二节农村医疗管理">第二节农村医疗管理</h4>'
NEEDLE = "江苏省卫生厅颁发《江苏省个体开业医生管理暂行办法》，要求对申请开业者</p>"
REPLACEMENT = (
    "江苏省卫生厅颁发《江苏省个体开业医生管理暂行办法》，要求对申请开业者"
    "均须由当地卫生主管部门经过考试考核后方可发证。1990年，市区个体开业者22人。</p>"
)
EXPECTED = "均须由当地卫生主管部门经过考试考核后方可发证。1990年，市区个体开业者22人。"


def patch_reader() -> tuple[int, dict[str, int]]:
    text = HTML.read_text(encoding="utf-8")
    start = text.index(SCOPE_START)
    end = text.index(SCOPE_END, start)
    segment = text[start:end]
    count = segment.count(NEEDLE)
    if count:
        segment = segment.replace(NEEDLE, REPLACEMENT)
    if EXPECTED not in segment:
        raise RuntimeError("private practice tail sentence missing after repair")
    if count:
        HTML.write_text(text[:start] + segment + text[end:], encoding="utf-8")
    return count, {"漏文补回": count} if count else {}


def write_reports(changed: int, counts: dict[str, int]) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "第五十五卷卫生 / 第四章医政 药政 / 第一节个体行医管理",
        "source": SOURCE_NOTE,
        "reader_path": str(HTML),
        "changes_this_run": changed,
        "counts": counts,
        "principle": "依据 PaddleOCR 页级文本补回第一节末尾漏文；未处理第二节农村医疗管理。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    md = f"""# 第五十五卷个体行医管理漏文修复

- 时间：{now}
- 范围：`第五十五卷卫生 / 第四章医政 药政 / 第一节个体行医管理`
- 源文依据：`{SOURCE_NOTE}`

## 修复动作

- 依据 PaddleOCR `page_0192.txt`，补回第一节末尾漏文：`均须由当地卫生主管部门经过考试考核后方可发证。1990年，市区个体开业者22人。`
- 本次复跑新增补回：{changed} 处。
- 本轮未处理 `第二节农村医疗管理`。

## 核对说明

- 阅读版原停在 `要求对申请开业者`。
- PaddleOCR `page_0192.txt` 第 16-17 行确认完整句子和下一节边界。
"""
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")


def update_memory(changed: int) -> None:
    marker = "## 2026-07-02 第五十五卷个体行医管理漏文修复"
    memory = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker in memory:
        return
    entry = f"""
{marker}

- 对第五十五卷卫生第四章第一节 `个体行医管理` 进行回源修复。
- 源文依据：`{SOURCE_NOTE}`；阅读版原停在 `要求对申请开业者`，补回 `均须由当地卫生主管部门经过考试考核后方可发证。1990年，市区个体开业者22人。`
- 本轮新增补回 {changed} 处；`第二节农村医疗管理` 未在本脚本中处理。
- 报告：`output/reports/reader_readability_health_private_practice_tail_20260702.md`。
"""
    MEMORY.write_text(memory.rstrip() + "\n\n" + entry.lstrip(), encoding="utf-8")


def main() -> None:
    changed, counts = patch_reader()
    write_reports(changed, counts)
    update_memory(changed)
    print("private practice tail restored")
    print(f"changes={changed}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()
