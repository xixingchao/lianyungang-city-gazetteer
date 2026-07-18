# -*- coding: utf-8 -*-
"""Restore health convalescence section from page OCR."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_health_convalescence_20260702.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_health_convalescence_20260702.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260702_第五十五卷疗养回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SOURCE_NOTE = (
    "workbench/ocr/paddle_ocr/下/part02/page_0206.txt:4-13; "
    "workbench/body_chapters/连云港市志_全书_正文汇总.md:101500-101509; "
    "workbench/body_chapters/第五十二卷至第六十卷及附录（下part02）.md:8195-8204"
)
SCOPE_START = '<h4 id="第五十五卷-第五章保健疗养-第五节疗养">第五节疗养</h4>'
SCOPE_END = '<h3 id="第五十五卷-第六章教育 科研">第六章教育 科研</h3>'

NEW_HTML = """<p>1955年，淮北盐务管理局在海州城内建立工人疗养所，设床位50张。1961年8月，市干部疗养院在海州建立。1963年，江苏省工人连云港疗养院在海州建立。70年代，济南铁路局疗养院在北崮山东南坡建成。1980年12月，江苏省工人连云港疗养院在陶庵重新建立，设床位100张。1982年6月，齐齐哈尔铁路局疗养院在北崮山建成，设床位300张。</p>
<p>同年，江苏省连云港海滨疗养院建成，设床位150张。1986年，国家化工部疗养院在北崮山东坡建立，设床位250张。至1990年，全市各疗养院的床位共1075张，工作人员505人，其中卫生技术人员188人。疗养方法和器械设备有：物理疗法、针灸、推拿、按摩、运动、气功，还有声疗、蜂疗、海水浴、腊疗、磁疗等。</p>"""

EXPECTED_TEXT = [
    "1955年，淮北盐务管理局在海州城内建立工人疗养所",
    "1961年8月，市干部疗养院在海州建立",
    "济南铁路局疗养院在北崮山东南坡建成",
    "1986年，国家化工部疗养院在北崮山东坡建立",
]
RESIDUALS = [
    "准北盐务管理局",
    "市于部疗养院",
    "北阖山东南坡",
    "北固山东坡",
]


def find_scope(text: str) -> tuple[int, int]:
    start = text.index(SCOPE_START) + len(SCOPE_START)
    end = text.index(SCOPE_END, start)
    return start, end


def patch_reader() -> tuple[int, dict[str, int]]:
    text = HTML.read_text(encoding="utf-8")
    start, end = find_scope(text)
    new_segment = "\n" + NEW_HTML + "\n"
    changed = int(text[start:end] != new_segment)
    if changed:
        HTML.write_text(text[:start] + new_segment + text[end:], encoding="utf-8")

    text = HTML.read_text(encoding="utf-8")
    start, end = find_scope(text)
    segment = text[start:end]
    missing = [item for item in EXPECTED_TEXT if item not in segment]
    if missing:
        raise RuntimeError(f"convalescence expected text missing: {missing}")
    remaining = [item for item in RESIDUALS if item in segment]
    if remaining:
        raise RuntimeError(f"convalescence residue remains: {remaining}")
    return changed, {"rewrote_scope": changed}


def write_reports(changed: int, counts: dict[str, int]) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "第五十五卷卫生 / 第五章保健疗养 / 第五节疗养",
        "source": SOURCE_NOTE,
        "reader_path": str(HTML),
        "changes_this_run": changed,
        "counts": counts,
        "principle": "依据 PaddleOCR 页级文本复原疗养节地名和机构名；未处理第六章教育科研。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    md = f"""# 第五十五卷疗养回源修复

- 时间：{now}
- 范围：`第五十五卷卫生 / 第五章保健疗养 / 第五节疗养`
- 源文依据：`{SOURCE_NOTE}`

## 修复动作

- 修正 `准北盐务管理局` 为 `淮北盐务管理局`。
- 修正 `市于部疗养院` 为 `市干部疗养院`。
- 修正 `北阖山东南坡`、`北固山东坡` 为 `北崮山东南坡`、`北崮山东坡`。
- 本次复跑新增整段替换：{changed} 处。
- 本轮未处理 `第六章教育科研`。

## 核对说明

- PaddleOCR `page_0206.txt` 确认本节完整文字和 `第六章教育科研` 边界。
- 正文汇总文件保留同样错识，本次以页级 OCR 为准。
"""
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")


def update_memory(changed: int) -> None:
    marker = "## 2026-07-02 第五十五卷疗养回源修复"
    memory = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker in memory:
        return
    entry = f"""
{marker}

- 对第五十五卷卫生第五章第五节 `疗养` 进行回源修复。
- 源文依据：`{SOURCE_NOTE}`；修正 `淮北盐务管理局`、`市干部疗养院`、`北崮山` 等机构名和地名错识。
- 本轮新增整段替换 {changed} 处；`第六章教育科研` 未在本脚本中处理。
- 报告：`output/reports/reader_readability_health_convalescence_20260702.md`。
"""
    MEMORY.write_text(memory.rstrip() + "\n\n" + entry.lstrip(), encoding="utf-8")


def main() -> None:
    changed, counts = patch_reader()
    write_reports(changed, counts)
    update_memory(changed)
    print("convalescence section repaired")
    print(f"changes={changed}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()
