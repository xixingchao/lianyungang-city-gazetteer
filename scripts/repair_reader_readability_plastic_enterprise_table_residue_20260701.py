# -*- coding: utf-8 -*-
"""Remove duplicated flattened residue for 表16-3 from the final reader."""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_plastic_enterprise_table_residue_20260701.md"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_plastic_enterprise_table_residue_20260701.json"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260701_第十六卷塑料工业企业表残文修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

VERIFIED_MARKERS = [
    'id="table-LYG-上-T044"',
    "表16-3 1990年连云港市塑料工业企业基本情况表",
    "连云港市印刷包装厂",
    "连云港市华东铝塑制品工业公司",
]

RESIDUE_RE = re.compile(
    r"\s*<p>（人）</p>\s*"
    r"<p>（万元）</p>\s*"
    r"<p>（万元）</p>\s*"
    r"<p>连云港市印刷包云台区海滨路市轻工公司编织袋/15万条/22\.521\.001\.50.*?连云港市新海塑海州洪门乡海州洪门乡打包带/6536\.003\.00料厂</p>\s*"
    r"(?:<table class=\"structured-table\"><thead><tr><th>企业名称</th><th>所在地</th><th>职工人数</th><th>主要产品</th><th>工业产值\(万元\)</th><th>利税\(万元\)</th></tr></thead><tbody>.*?</tbody></table>\s*){1,3}"
    r"<p>O</p>\s*",
    re.S,
)

RESIDUE_MARKERS = [
    "连云港市印刷包云台区海滨路市轻工公司",
    "海水综合利用厂",
    "<p>O</p>",
]


def repair() -> dict[str, object]:
    text = HTML.read_text(encoding="utf-8")
    missing = [marker for marker in VERIFIED_MARKERS if marker not in text]
    if missing:
        raise RuntimeError(f"verified table markers missing: {missing}")
    before = {marker: text.count(marker) for marker in RESIDUE_MARKERS}
    new_text, count = RESIDUE_RE.subn("\n", text, count=1)
    if new_text != text:
        HTML.write_text(new_text, encoding="utf-8")
    after_text = HTML.read_text(encoding="utf-8")
    return {
        "removed_blocks": count,
        "residue_markers_before": before,
        "residue_markers_after": {marker: after_text.count(marker) for marker in RESIDUE_MARKERS},
    }


def write_reports(result: dict[str, object]) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "reader": "output/final_reader/连云港市志_全书.html",
        "verified_table": "workbench/table_entries/上/data/LYG-上-T044.json",
        **result,
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    md = f"""# 第十六卷塑料工业企业表残文修复

- 时间：{now}
- 阅读版：`output/final_reader/连云港市志_全书.html`
- 覆盖表：`workbench/table_entries/上/data/LYG-上-T044.json`

## 修复动作

- 确认 verified 表 `LYG-上-T044` 已在阅读版后部展示，题为 `表16-3 1990年连云港市塑料工业企业基本情况表`。
- 从正文中撤出单位残片、OCR 串行残文、旧版未核重复表和孤立 `O` 段。
- 未改动 verified 表数据。

## 结果

- 删除块数：{result['removed_blocks']}
- 残文标记：`{json.dumps(result['residue_markers_after'], ensure_ascii=False)}`
"""
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")


def update_memory(result: dict[str, object]) -> None:
    marker = "## 2026-07-01 第十六卷塑料工业企业表残文修复"
    memory = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker in memory:
        return
    entry = f"""
{marker}

- 新增脚本：`scripts/repair_reader_readability_plastic_enterprise_table_residue_20260701.py`。
- 针对第十六卷皮塑工业中 `表16-3 1990年连云港市塑料工业企业基本情况表` 的重复残留，确认 verified 表 `LYG-上-T044` 已存在后，撤出单位残片、OCR 串行残文、旧版未核重复表和孤立 `O` 段。
- 本次删除块数：{result['removed_blocks']}；未改动 verified 表数据。
- 报告：`output/reports/reader_readability_plastic_enterprise_table_residue_20260701.md`。
"""
    MEMORY.write_text(memory.rstrip() + "\n\n" + entry.lstrip(), encoding="utf-8")


def main() -> None:
    result = repair()
    write_reports(result)
    update_memory(result)
    print(f"removed_blocks={result['removed_blocks']}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()
