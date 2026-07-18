# -*- coding: utf-8 -*-
"""Remove remaining duplicated OCR residue around 表1-1 in the final reader."""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_geology_table_remaining_residue_20260701.md"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_geology_table_remaining_residue_20260701.json"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260701_第一卷地层系统表剩余残文修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

TABLE_START = '<table class="structured-table"><caption>表1-1 连云港市地层系统表</caption>'
VERIFIED_MARKER = 'id="table-LYG-上-T001"'
STRUCTURE_PARAGRAPH = (
    '<p>三、构造市境所处大地构造位置，属于中朝准地台南缘的胶辽台隆的南段，'
    '是秦岭褶皱系的东延部分，北有青岛一日照断裂，南有淮阴一响水口断裂，与扬子准地台为界。'
    '西部因郯庐断裂的平移，将市境与秦岭褶皱东段分成两个不相连的部分。</p>'
)

RESIDUE_BLOCK_RE = re.compile(
    r"(?P<first_table><table class=\"structured-table\"><caption>表1-1 连云港市地层系统表</caption>.*?</table>)\s*"
    r"<p>（米）</p>\s*"
    r"<p>全新亚粘土、粉细砂夹粗砂、灰黑色淤Q40～25统泥.*?</p>\s*"
    r"<p>下更亚粘土夹泥质粉砂.*?</p>\s*"
    r"<p>上第三系灰黑色微密.*?</p>\s*"
    r"<p>砾岩上段：紫红色薄到中厚层细粒砂.*?</p>\s*"
    r"<p>动物足迹印痕界下段.*?</p>\s*"
    r"<p>未见顶灰、灰白色白云.*?</p>\s*"
    r"<table class=\"structured-table\"><caption>表1-1 连云港市地层系统表</caption>.*?</table>\s*"
    r"<p>（米）</p>\s*"
    r"<p>dhb底部为含透辉石石英岩.*?</p>\s*"
    r"<p>混合岩化作用后为二长混合岩，条带状混合岩、混合片麻岩三、构造(?P<structure>市境所处大地构造位置，属于中朝准地台南缘的胶辽台隆的南段，是秦岭褶皱系的东延部分，北有青岛一日照断裂，南有淮阴一响水口断裂，与扬子准地台为界。西部因郯庐断裂的平移，将市境与秦岭褶皱东段分成两个不相连的部分。)</p>",
    re.S,
)

RESIDUE_MARKERS = [
    "全新亚粘土、粉细砂夹粗砂、灰黑色淤Q40",
    "dhb底部为含透辉石石英岩",
    "混合岩化作用后为二长混合岩，条带状混合岩、混合片麻岩三、构造",
]


def repair() -> dict[str, object]:
    text = HTML.read_text(encoding="utf-8")
    if VERIFIED_MARKER not in text:
        raise SystemExit("verified table LYG-上-T001 is missing")
    before_inline_tables = text.count(TABLE_START)
    before_markers = {marker: text.count(marker) for marker in RESIDUE_MARKERS}

    def repl(match: re.Match[str]) -> str:
        return match.group("first_table") + "\n" + STRUCTURE_PARAGRAPH + "\n"

    new_text, replaced = RESIDUE_BLOCK_RE.subn(repl, text, count=1)
    if replaced:
        HTML.write_text(new_text, encoding="utf-8")

    after = HTML.read_text(encoding="utf-8")
    return {
        "replaced_blocks": replaced,
        "inline_table_count_before": before_inline_tables,
        "inline_table_count_after": after.count(TABLE_START),
        "residue_markers_before": before_markers,
        "residue_markers_after": {marker: after.count(marker) for marker in RESIDUE_MARKERS},
    }


def write_reports(result: dict[str, object]) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "reader": "output/final_reader/连云港市志_全书.html",
        "verified_table": "workbench/table_entries/上/data/LYG-上-T001.json",
        **result,
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    md = f"""# 第一卷地层系统表剩余残文修复

- 时间：{now}
- 阅读版：`output/final_reader/连云港市志_全书.html`
- 结构化表：`workbench/table_entries/上/data/LYG-上-T001.json`

## 修复动作

- 保留第一卷正文中第一张 `表1-1 连云港市地层系统表` 结构化表。
- 删除其后重复出现的表格、单位残片、续表 OCR 残文和 `dhb...夹山组...` 尾段残文。
- 将被残文粘住的 `三、构造` 段恢复为正文开头。

## 结果

- 替换块数：{result['replaced_blocks']}
- 正文内 `表1-1` 结构化表数量：{result['inline_table_count_before']} -> {result['inline_table_count_after']}
- 残文标记：`{json.dumps(result['residue_markers_after'], ensure_ascii=False)}`
"""
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")


def update_memory(result: dict[str, object]) -> None:
    marker = "## 2026-07-01 第一卷地层系统表剩余残文修复"
    memory = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker in memory:
        return
    entry = f"""
{marker}

- 新增脚本：`scripts/repair_reader_readability_geology_table_remaining_residue_20260701.py`。
- 针对用户贴出的 `表1-1 连云港市地层系统表` OCR 线性化残文，保留第一卷正文内第一张可读结构化表，撤出后续重复表、单位残片、续表尾段和 `dhb...夹山组...` 残文。
- 将被残文粘连的 `三、构造` 段恢复到正文开头；verified 表 `LYG-上-T001` 仍保留。
- 本次替换块数：{result['replaced_blocks']}；报告：`output/reports/reader_readability_geology_table_remaining_residue_20260701.md`。
"""
    MEMORY.write_text(memory.rstrip() + "\n\n" + entry.lstrip(), encoding="utf-8")


def main() -> None:
    result = repair()
    write_reports(result)
    update_memory(result)
    print(f"replaced_blocks={result['replaced_blocks']}")
    print(f"inline_table_count={result['inline_table_count_before']}->{result['inline_table_count_after']}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()
