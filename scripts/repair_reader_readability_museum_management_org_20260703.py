# -*- coding: utf-8 -*-
"""Restore cultural relics management organization section from page OCR."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_museum_management_org_20260703.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_museum_management_org_20260703.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260703_第五十三卷文物管理机构回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SOURCE_NOTE = "workbench/ocr/paddle_ocr/下/part02/page_0122.txt:13-31"
SCOPE_START = '<h4 id="第五十三卷-第六章文物管理与保护-第一节管理机构">第一节管理机构</h4>'
SCOPE_END = '<h4 id="第五十三卷-第六章文物管理与保护-第二节文物普查">第二节文物普查</h4>'

NEW_HTML = """<h4 id="第五十三卷-第六章文物管理与保护-第一节管理机构">第一节管理机构</h4>
<p>一、连云港市文物保护管理委员会</p>
<p>连云港市文物保护管理委员会（简称文管会）成立于1980年11月12日，它代表市政府负责全市的文物保护管理工作。其下设办公室，为常设机构，处理日常事务。办公室主任由市文化局分管文博的局长兼任，代表市政府行使对文物的保护、管理、监督权，推行文物保护的法律法规和各项政策。</p>
<p>文管会办公室原设于市博物馆，由馆内人员兼任。1987年，从博物馆分出，定编5人，属市文化局管理。</p>
<p>文管会下设孔望山摩崖造像文保所、海清寺塔文保所。</p>
<p>二、新浦区文物管理委员会</p>
<p>第一届委员会成立于1987年5月，由13名委员组成，副区长陈东美任主任委员，办公室主任则由区文教局文化科长俞秀云兼任。</p>
<p>三、海州区文物管理委员会</p>
<p>首届委员会成立于1989年7月6日，由副区长高重云任主任委员，文教局局长武逸之兼任办公室主任。</p>
"""

EXPECTED_TEXT = [
    "一、连云港市文物保护管理委员会</p>",
    "二、新浦区文物管理委员会</p>",
    "第一届委员会成立于1987年5月",
    "三、海州区文物管理委员会</p>",
]
RESIDUALS = [
    "一、连云港市文物保护管理委员会连云港市",
    "二、新浦区文物管理委员会第届委员会",
    "三、海州区文物管理委员会首届委员会",
]


def find_scope(text: str) -> tuple[int, int]:
    start = text.index(SCOPE_START)
    end = text.index(SCOPE_END, start)
    return start, end


def patch_reader() -> tuple[int, dict[str, int]]:
    text = HTML.read_text(encoding="utf-8")
    start, end = find_scope(text)
    changed = int(text[start:end] != NEW_HTML)
    if changed:
        HTML.write_text(text[:start] + NEW_HTML + text[end:], encoding="utf-8")

    text = HTML.read_text(encoding="utf-8")
    start, end = find_scope(text)
    segment = text[start:end]
    missing = [item for item in EXPECTED_TEXT if item not in segment]
    if missing:
        raise RuntimeError(f"expected text missing: {missing}")
    remaining = [item for item in RESIDUALS if item in segment]
    if remaining:
        raise RuntimeError(f"residue remains: {remaining}")
    return changed, {"rewrote_scope": changed}


def write_reports(changed: int, counts: dict[str, int]) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "第五十三卷文物 / 第六章文物管理与保护 / 第一节管理机构",
        "source": SOURCE_NOTE,
        "reader_path": str(HTML),
        "changes_this_run": changed,
        "counts": counts,
        "principle": "依据 PaddleOCR 页级文本重建管理机构节，停止在第二节文物普查前。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    md = f"""# 第五十三卷文物管理机构回源修复

- 时间：{now}
- 范围：`第五十三卷文物 / 第六章文物管理与保护 / 第一节管理机构`
- 源文依据：`{SOURCE_NOTE}`

## 修复动作

- 按页级 OCR 重建 `第一节管理机构`，停止在 `第二节文物普查` 前。
- 拆开 `一、连云港市文物保护管理委员会`、`二、新浦区文物管理委员会`、`三、海州区文物管理委员会` 与正文粘连，修正 `第一届委员会`。
- 当前核验复跑整段替换：{changed} 处。

## 核对说明

- 仅处理管理机构节，后续 `第二节文物普查` 不在本脚本范围内。
"""
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")


def update_memory(changed: int) -> None:
    marker = "## 2026-07-03 第五十三卷文物管理机构回源修复"
    memory = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker in memory:
        return
    entry = f"""
{marker}

- 对第五十三卷文物 `第六章文物管理与保护 / 第一节管理机构` 进行回源修复。
- 源文依据：`{SOURCE_NOTE}`；重建至 `第二节文物普查` 前，未触碰后续普查条目。
- 拆开 `一、连云港市文物保护管理委员会`、`二、新浦区文物管理委员会`、`三、海州区文物管理委员会` 与正文粘连，修正 `第一届委员会`。
- 当前核验复跑整段替换 {changed} 处。
- 报告：`output/reports/reader_readability_museum_management_org_20260703.md`。
"""
    MEMORY.write_text(memory.rstrip() + "\n\n" + entry.lstrip(), encoding="utf-8")


def main() -> None:
    changed, counts = patch_reader()
    write_reports(changed, counts)
    update_memory(changed)
    print("museum management organization repaired")
    print(f"changes={changed}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()
