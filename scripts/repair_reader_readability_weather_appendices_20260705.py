# -*- coding: utf-8 -*-
"""Split first-volume weather appendix headings in final reader."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_weather_appendices_20260705.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_weather_appendices_20260705.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260705_第一卷气象附录标题版式修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = {
    "<p>附1-1：连云港市气象探测通讯地面气象测报": "<h4>附1-1：连云港市气象探测通讯</h4>\n<p><strong>地面气象测报</strong>",
    "<p>通讯 连云港市气象通讯业务始于": "<p><strong>通讯</strong> 连云港市气象通讯业务始于",
    "<p>填图 市气象台填图业务分两个阶段。": "<p><strong>填图</strong> 市气象台填图业务分两个阶段。",
    "<p>农业气象在1983年实行市管县以后，": "<p><strong>农业气象</strong>在1983年实行市管县以后，",
    "<p>附1-2：连云港市天气预报短期天气预报 ": "<h4>附1-2：连云港市天气预报</h4>\n<p><strong>短期天气预报</strong> ",
    "<p>短时天气预报12小时以内的短时天气预报，": "<p><strong>短时天气预报</strong>12小时以内的短时天气预报，",
    "<p>中长期天气预报1955年开始制作长期天气预报，": "<p><strong>中长期天气预报</strong>1955年开始制作长期天气预报，",
}
RESIDUALS = list(REPLACEMENTS)


def append_once(path: Path, marker: str, content: str) -> None:
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker not in old:
        path.write_text(old.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")


def patch_html() -> int:
    text = HTML.read_text(encoding="utf-8")
    changed = 0
    for old, new in REPLACEMENTS.items():
        count = text.count(old)
        if count != 1:
            raise RuntimeError(f"expected one match for {old!r}, got {count}")
        text = text.replace(old, new, 1)
        changed += 1
    for residue in RESIDUALS:
        if residue in text:
            raise RuntimeError(f"weather appendix residue remains: {residue}")
    HTML.write_text(text, encoding="utf-8")
    return changed


def main() -> None:
    changed = patch_html()
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "第一卷自然环境：附1-1 气象探测通讯、附1-2 天气预报",
        "html_boundaries_split": changed,
        "source_evidence": ["workbench/body_chapters/paddle_上/第一卷_自然环境.md:2376-2445"],
        "notes": ["仅拆最终 HTML 标题和源文段首小标题边界，不改正文文字。"],
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    md = f"""# 第一卷气象附录标题版式修复

- 时间：{now}
- 范围：第一卷自然环境，附1-1、附1-2。
- 本次拆分边界：{changed} 处。

## 修复

- 将 `附1-1：连云港市气象探测通讯` 与 `附1-2：连云港市天气预报` 从段首粘连中恢复为独立附录标题。
- 将 `地面气象测报`、`通讯`、`填图`、`农业气象`、`短期天气预报`、`短时天气预报`、`中长期天气预报` 恢复为段首强调小标题。
- 仅恢复版式边界，不改正文文字。

## 依据

- `workbench/body_chapters/paddle_上/第一卷_自然环境.md:2376-2445`
"""
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")
    marker = "## 2026-07-05 第一卷气象附录标题版式修复"
    append_once(
        MEMORY,
        marker,
        f"""
{marker}
- 修复第一卷自然环境 `附1-1`、`附1-2` 在最终阅读版中附录标题和段首小标题粘正文的问题。
- 按 PaddleOCR 源文边界恢复附录标题，并将 `地面气象测报`、`通讯`、`填图`、`农业气象`、`短期天气预报`、`短时天气预报`、`中长期天气预报` 标为段首小标题。
- 仅恢复版式边界，不改正文文字；鱼类/贝类/地震等后续附录另批回源。
- 报告：`output/reports/reader_readability_weather_appendices_20260705.md`。
""",
    )
    print(f"html_boundaries_split={changed}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()
