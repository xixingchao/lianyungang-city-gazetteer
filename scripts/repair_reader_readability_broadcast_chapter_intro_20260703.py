# -*- coding: utf-8 -*-
"""Move and restore broadcast chapter intro from page OCR."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_broadcast_chapter_intro_20260703.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_broadcast_chapter_intro_20260703.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260703_第五十四卷广播章概述错位回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SOURCE_NOTE = "workbench/ocr/paddle_ocr/下/part02/page_0145.txt:71-80"
OLD_BLOCK = """<p>1951年7月1日，新海连市收音站成立。翌年5月1日改为有线广播宣传站。</p>
<p>1959年5月1日，新海连人民广播电台开始播音，用1350千赫频率，转播中央和江苏人民广播电台部分节目，自办部分节目，初步形成全市城乡广播网。</p>
<p>1971年，海州孔望山中波发射台建成。1978年，锦屏山调频广播发射台开始转播江苏人民广播电台一套节目。1985年6月，市调频广播电台开播。1989年6月开始播发调频立体声节目。至1990年，全市有调频广播转播台3座，微波站1座，县级广播电台3座，有线广播站7个，乡镇广播电视站80个，通讯员820人，编辑18人，来稿23652篇。</p>
<h3 id="第五十四卷-第三章广播">第三章广播</h3>"""
STABLE_BLOCK = """<h3 id="第五十四卷-第三章广播">第三章广播</h3>
<p>民国38年（1949年）3月、1950年11月和1952年12月，灌云、赣榆、东海三县分别建立广播站。</p>"""
NEW_BLOCK = """<h3 id="第五十四卷-第三章广播">第三章广播</h3>
<p>民国38年（1949年）3月、1950年11月和1952年12月，灌云、赣榆、东海三县分别建立广播站。</p>
<p>1951年7月1日，新海连市收音站成立。翌年5月1日改为有线广播宣传站。</p>
<p>1959年5月1日，新海连人民广播电台开始播音，用1350千赫频率，转播中央和江苏人民广播电台部分节目，自办部分节目，初步形成全市城乡广播网。</p>
<p>1971年，海州孔望山中波发射台建成。1978年，锦屏山调频广播发射台开始转播江苏人民广播电台一套节目。1985年6月，市调频广播电台开播。1989年6月开始播发调频立体声节目。至1990年，全市有调频广播转播台3座，微波站1座，县级广播电台3座，有线广播站7个，乡镇广播电视站80个，通讯员820人，编辑18人，来稿23652篇。</p>"""

EXPECTED_TEXT = [
    "<h3 id=\"第五十四卷-第三章广播\">第三章广播</h3>",
    "民国38年（1949年）3月、1950年11月和1952年12月，灌云、赣榆、东海三县分别建立广播站。",
    "1951年7月1日，新海连市收音站成立。翌年5月1日改为有线广播宣传站。",
]
RESIDUALS = [
    "<p>1951年7月1日，新海连市收音站成立。翌年5月1日改为有线广播宣传站。</p>\n<p>1959年5月1日，新海连人民广播电台开始播音",
]


def patch_reader() -> tuple[int, dict[str, int]]:
    text = HTML.read_text(encoding="utf-8")
    if OLD_BLOCK in text:
        text = text.replace(OLD_BLOCK, NEW_BLOCK, 1)
        changed = 1
        HTML.write_text(text, encoding="utf-8")
    elif STABLE_BLOCK in text:
        changed = 0
    else:
        raise RuntimeError("broadcast intro scope not found")

    text = HTML.read_text(encoding="utf-8")
    start = text.index('<h3 id="第五十四卷-第三章广播">第三章广播</h3>')
    end = text.index('<h4 id="第五十四卷-第三章广播-第一节有线广播">第一节有线广播</h4>', start)
    segment = text[start:end]
    missing = [item for item in EXPECTED_TEXT if item not in segment]
    if missing:
        raise RuntimeError(f"expected text missing: {missing}")
    remaining = [item for item in RESIDUALS if item in text[:start]]
    if remaining:
        raise RuntimeError(f"pre-title residue remains: {remaining}")
    return changed, {"moved_intro_after_chapter_title": changed}


def write_reports(changed: int, counts: dict[str, int]) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "第五十四卷报刊广播电视 / 第三章广播 / 章前概述",
        "source": SOURCE_NOTE,
        "reader_path": str(HTML),
        "changes_this_run": changed,
        "counts": counts,
        "principle": "依据 PaddleOCR 页级文本恢复广播章概述首句，并将概述置于章标题后。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    md = f"""# 第五十四卷广播章概述错位回源修复

- 时间：{now}
- 范围：`第五十四卷报刊广播电视 / 第三章广播 / 章前概述`
- 源文依据：`{SOURCE_NOTE}`

## 修复动作

- 补回 `民国38年（1949年）3月、1950年11月和1952年12月...` 概述首句。
- 将原先位于 `第三章广播` 标题前的三段概述移动到章标题后。
- 未改动 `表54-3` 结构化表数据。
- 当前核验复跑整段替换：{changed} 处。
"""
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")


def update_memory(changed: int) -> None:
    marker = "## 2026-07-03 第五十四卷广播章概述错位回源修复"
    memory = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker in memory:
        return
    entry = f"""
{marker}

- 对第五十四卷报刊广播电视 `第三章广播` 概述错位进行回源修复。
- 源文依据：`{SOURCE_NOTE}`；补回广播章概述首句，并将三段概述置于 `第三章广播` 标题之后。
- 未改动 `表54-3` 结构化表；表54-3续表仍由 `LYG-下-T081` 交付。
- 当前核验复跑整段替换 {changed} 处。
- 报告：`output/reports/reader_readability_broadcast_chapter_intro_20260703.md`。
"""
    MEMORY.write_text(memory.rstrip() + "\n\n" + entry.lstrip(), encoding="utf-8")


def main() -> None:
    changed, counts = patch_reader()
    write_reports(changed, counts)
    update_memory(changed)
    print(json.dumps({"changed": changed, "counts": counts}, ensure_ascii=False))


if __name__ == "__main__":
    main()
